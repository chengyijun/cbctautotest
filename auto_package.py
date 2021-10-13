import os
import shutil

"""
注意：执行此自动打包脚本 现需要给ide超级管理员权限 以便文件操作顺利进行
"""


class AutoPackage:
    # pyinstaller 所在位置
    pyinstaller_path = r'D:\venvs\py38\Scripts\pyinstaller.exe'
    # 被打包程序的入口文件
    main_file = 'CBCTAutoTest.py'
    # 需要拷贝的data文件 不需要就填写 空列表[]
    datas = ['cp_images', 'theme', 'ico', 'config', 'locate_pos']
    # 指定ico图标文件 不需要图标就填写 空字符串''
    ico_file = r'ico/ico.ico'
    # 是否显示调试窗口 显示-True  不显示-False
    is_show_console = False

    def __init__(self):
        if os.path.exists('./build'):
            shutil.rmtree('./build')
        if os.path.exists('./dist'):
            shutil.rmtree('./dist')

    def handle_is_show_console(self):
        if self.is_show_console:
            return ''
        return '-w'

    def handle_ico(self) -> str:
        if self.ico_file == '':
            return ''
        return rf'-i {self.ico_file}'

    def handle_add_datas(self) -> str:
        if len(self.datas) == 0:
            return ''
        res = ''
        for data in self.datas:
            res += f'--add-data {data};{data} '
        return res

    def package(self) -> None:
        add_data_str = self.handle_add_datas()
        ico_file_str = self.handle_ico()
        is_show_console_window = self.handle_is_show_console()
        res = os.system(
            rf"{self.pyinstaller_path} {add_data_str} {ico_file_str} {is_show_console_window} {self.main_file}"
        )
        if res == 0:
            print('打包成功')
        else:
            print('打包失败', res)


def main():
    AutoPackage().package()


if __name__ == '__main__':
    main()
