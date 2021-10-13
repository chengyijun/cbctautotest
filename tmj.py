# -*- coding:utf-8 -*-
"""
@author: chengyijun
@contact: cyjmmy@foxmail.com
@file: CBCT Auto Test 之CT自动化拍摄流程脚本
@time: 2021/3/22 11:45
@desc:
"""

import pyautogui

from tmj_helper import select_patient, select_body_type, select_electricity_min, select_teeth_shape
from utils import click_action, click_double_action, wait_until_checkpoint_appear, select_app, add_patient, \
    wait_before_qrps, wait_before_ps_ui_load, wait_before_tmj_second_ps, \
    wait_before_rebuild, get_pos


class TMJAutoTest:

    def __init__(self, no: int):
        self.no = no

    def create_chufang(self):
        # 定位【设备类型】 578,518
        click_action(*get_pos('device_type_pos'))
        x, y = get_pos('tmj_model')
        pyautogui.moveRel(xOffset=x, yOffset=y, duration=0.5)
        pyautogui.click()

        click_action(*get_pos('model_type_detail'))
        x2, y2 = get_pos('tmj_model_2')
        pyautogui.moveRel(xOffset=x2, yOffset=y2, duration=0.5)
        pyautogui.click()

        # 点击【登记】
        click_action(*get_pos('add_record_btn_pos'))

    def image_collect(self):
        # 点击【影像中心】55 515
        click_action(*get_pos('image_center_pos'))
        print("患者登记状态检查点")
        wait_until_checkpoint_appear("cp0.png")
        # 双击选择第一个记录
        click_double_action(*get_pos('first_record_pos'))
        wait_before_ps_ui_load()
        # 患者类型
        select_patient()
        # 患者体型
        select_body_type()
        # 牙列形状
        select_teeth_shape()
        # 调整电流电压
        # select_electricity()
        select_electricity_min()

        # 点击【机器准备】 sleep 33秒+5
        # 挂起2s等待拍摄页面加载完毕

        print("机器准备检查点")
        wait_until_checkpoint_appear("cp1_jqzb.png")

        # sleep(2)
        click_action(*get_pos('machine_ready'))
        # sleep(33 + 15)
        # 点击【确认拍摄】 sleep 40+5
        print("确认拍摄检查点")
        wait_until_checkpoint_appear("cp2_qrps.png")
        wait_before_qrps()
        click_action(*get_pos('take_shot'))
        # 第一次曝光结束之后等待机器准备完成
        # wait_until_checkpoint_appear("cp_tmj_b1end.png")
        wait_before_tmj_second_ps()
        print("确认第二次拍摄检查点")
        wait_until_checkpoint_appear("cp2_qrps.png")
        wait_before_qrps()
        click_action(*get_pos('take_shot'))

        # sleep(40 + 15)
        # 点击【推出拍摄】 sleep 40+5
        print("完成拍摄检查点")
        wait_until_checkpoint_appear("cp3_wcps.png")
        wait_before_qrps()
        click_action(*get_pos('finish_take_shot'))
        wait_before_rebuild()
        print("拍片完成")

    def start_test(self):
        # 定位CBCT软件
        select_app()
        # # 添加用户
        add_patient(self.no)
        # # 创建处方
        self.create_chufang()
        # 拍摄
        self.image_collect()


def main():
    tmj = TMJAutoTest(5)
    tmj.start_test()


if __name__ == '__main__':
    main()
