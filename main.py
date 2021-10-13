import os
from os.path import join
from time import sleep
from typing import List

import pyautogui

from config import ROOT_PATH
from ct import CTAutoTest
from dx import DXAutoTest
from px import PXAutoTest
from tmj import TMJAutoTest
from utils import weight_choice
from utils_email import SendEmailWithAttachment


class CBCTAutoTest:
    def __init__(self, ps_num: int, ps_wait: float, weights: List[int], is_send_email: bool, receiver: str):
        # 总共拍摄次数
        self.ps_num = ps_num
        # 每次拍摄间隔时间 单位：分钟
        self.ps_wait = ps_wait
        # 四种模式权重列表
        self.weights = weights
        # 是否发送邮件通知
        self.is_send_email = is_send_email
        # 邮件消息接收者
        self.receiver = receiver

    def start(self):

        for i in range(self.ps_num):
            model = weight_choice(self.weights)
            if model == 'A':
                ct = CTAutoTest(i + 1)
                ct.start_test()
            elif model == 'B':
                px = PXAutoTest(i + 1)
                px.start_test()
            elif model == 'C':
                dx = DXAutoTest(i + 1)
                dx.start_test()
            else:
                tmj = TMJAutoTest(i + 1)
                tmj.start_test()
            print(f"----第{str(i + 1)}次拍摄结束----")
            sleep(self.ps_wait * 60)

        if self.is_send_email:
            try:
                result_screenshot = join(ROOT_PATH, 'screenshot.jpg')
                if os.path.exists(result_screenshot):
                    os.remove(result_screenshot)
                pyautogui.screenshot().save(result_screenshot)
                pyautogui.sleep(1)
                SendEmailWithAttachment(['cyjmmy@foxmail.com'], '老化测试结果', '老化测试完成', result_screenshot).start()
                print('正在发送邮件')
            except Exception as e:
                print(e)


def main():
    auto_test = CBCTAutoTest()
    auto_test.start()


if __name__ == '__main__':
    main()
