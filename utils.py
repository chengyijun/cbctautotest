import random
import time
from os.path import join
from time import sleep
from typing import List, Dict, Tuple

import pyautogui
import pyperclip
import win32con
import win32gui
from ruamel import yaml

from config import BASE_CONFIG_PATH
from config import CP_IMAGES_PATH


def click_double_action(x: int, y: int, duration: float = 0.5, wait: float = 0.5) -> None:
    """
    移动到目标位置并双击
    :param x: 横坐标
    :param y: 纵坐标
    :param duration: 鼠标移动时间  默认0.5s
    :param wait: 开始移动前的等待时间 默认0.5s
    :return:
    """
    pyautogui.moveTo(x, y, duration=duration)
    sleep(wait)
    pyautogui.doubleClick()


def click_action(x: int, y: int, duration: float = 0.5, wait: float = 0.5) -> None:
    """
    移动到目标位置并单击
    :param x: 横坐标
    :param y: 纵坐标
    :param duration: 鼠标移动时间  默认0.5s
    :param wait: 开始移动前的等待时间 默认0.5s
    :return:
    """
    pyautogui.moveTo(x, y, duration=duration)
    sleep(wait)
    pyautogui.click()


def type_action(x: int, y: int, txt: str, duration: float = 0.5) -> None:
    """
    移动到目标位置并执行粘贴（模拟输入）
    :param x: 横坐标
    :param y: 纵坐标
    :param txt: 输入的文本
    :param duration: 输入持续时间 默认为0.5s
    :return:
    """
    pyperclip.copy(txt)
    click_action(x, y, duration=duration)
    pyautogui.hotkey('ctrl', 'v')


def wait_until_checkpoint_appear(cp: str) -> None:
    """
    等到图片检查点出现，没有出现之前一直循环等待
    :param cp:
    :return:
    """
    while True:
        # 每次图像检查点比对之前 先将鼠标挪开 以免干扰识别判断
        click_action(100, 100, 0, 0)
        # sleep(1)
        box = pyautogui.locateOnScreen(join(CP_IMAGES_PATH, cp))
        if box is not None:
            print(f"{cp} 检查点通过")
            break


def check_menu_closed(cp: str) -> bool:
    """
    检查菜单初始状态是否是闭合的
    闭合-True
    展开-False
    :param cp:
    :return:
    """

    # 每次图像检查点比对之前 先将鼠标挪开 以免干扰识别判断
    click_action(100, 100, 0, 0)
    # sleep(1)
    box = pyautogui.locateOnScreen(join(CP_IMAGES_PATH, cp))
    if box is not None:
        return True
    return False


def get_timestamp() -> str:
    """
    获取时间戳放大1w后的后四位字符串
    :return:
    """
    return str(int(time.time() * 1000))[-4:]


def add_patient(no: int) -> None:
    # 定位到【影像中心】 53,649
    click_action(*get_pos('image_center_pos'))
    # 点击【登记】 191,611
    click_action(*get_pos('record_btn_pos'))
    # 定位【姓名】 575,319
    x, y = get_pos('patient_name_pos')
    type_action(x, y, f'test_{get_timestamp()}_{str(no)}')


def select_app() -> None:
    # 找到被测窗口才能继续向下进行测试
    config_dict = read_config_data()
    feelin_window_title = config_dict.get('feelin_window_title')
    while True:
        win_handle = win32gui.FindWindow(None, feelin_window_title)
        if win_handle != 0:
            break
        sleep(1)
    # 窗口显示
    win32gui.ShowWindow(win_handle, win32con.SW_SHOWNORMAL)
    # 窗口置顶
    win32gui.SetForegroundWindow(win_handle)


def weight_choice(weight: List[int]) -> str:
    """
    :param weight: list对应的权重序列
    :return:选取的值在原列表里的索引
    """
    targets = ['A', 'B', 'C', 'D']
    t = random.randint(0, sum(weight) - 1)
    for i, val in enumerate(weight):
        t -= val
        if t < 0:
            return targets[i]


def menu_init() -> None:
    """
    菜单初始化
    :return:
    """
    # 选择第一位患者 240 260
    # 先切换到 【全部】
    click_action(248, 80)
    click_action(*get_pos('first_patient_pos'))
    # 点击【处方】
    click_action(*get_pos('prescription_tab_pos'))
    #     441 188
    # 459 216
    is_menu_closed = check_menu_closed("cp_menu.png")
    if not is_menu_closed:
        # 如果菜单未闭合 先进行初始化闭合
        click_double_action(498, 185)
    # 展开一级菜单
    click_double_action(498, 185)
    # 展开二级菜单
    click_double_action(529, 218)


def wait_before_qrps() -> None:
    """
    确认拍摄前等待的时间 秒
    :return:
    """
    sleep(read_config_data().get('wait_before_qrps_value'))


def wait_before_rebuild() -> None:
    """
    重建等待时间
    :return:
    """
    sleep(read_config_data().get('wait_before_rebuild_value'))


def wait_before_ps_ui_load() -> None:
    """
    拍摄页面加载完毕 之前的等待
    :return:
    """
    sleep(read_config_data().get('wait_before_ps_ui_load_value'))


def wait_before_tmj_second_ps() -> None:
    """
    第二次TMJ拍摄 之前的等待
    :return:
    """
    sleep(read_config_data().get('wait_before_tmj_second_ps_value'))


def read_config_data() -> Dict:
    """
    读取配置文件 返回配置字典
    :return:
    """
    with open(join(BASE_CONFIG_PATH, 'base.yaml'), 'r', encoding='utf-8') as f:
        config_data = yaml.load(f, Loader=yaml.Loader)
    return config_data


def get_model_menu_pos(model_config_name: str) -> Tuple[int]:
    """
    获取四种模式菜单项坐标
    :param model_config_name: 四种菜单模式在配置文件中的名字 如ct_pos
    :return:
    """
    return eval(read_config_data().get(model_config_name))


def get_pos(config_name: str) -> Tuple[int]:
    """
    获取四种模式菜单项坐标
    :param config_name: 菜单在配置中的名称
    :return:
    """
    return eval(read_config_data().get(config_name))


def select_doctor(x: int, y: int) -> None:
    """
    处方界面选择医生
    :param x:
    :param y:
    :return:
    """
    click_action(x, y)
    pyautogui.moveRel(xOffset=0, yOffset=80, duration=0.5)
    pyautogui.click()
