import sys
import typing

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QSlider
from system_hotkey import SystemHotkey

from aboutui import Ui_Dialog
from main import CBCTAutoTest
from mainui import Ui_MainWindow
import  rs_rc

class Worker(QThread):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.num = 10
        self.wait = 0
        self.weights = [50, 50, 50, 50]
        self.is_send_email = False
        self.receiver = 'cyjmmy@foxmail.com'

    def task(self):
        auto_test = CBCTAutoTest(self.num, self.wait, self.weights, self.is_send_email, self.receiver)
        auto_test.start()

    def run(self):
        self.task()


class AboutWin(Ui_Dialog, QDialog):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("关于")


class MainWin(Ui_MainWindow, QMainWindow):
    # 自定义 全局快捷键关闭窗口的信号
    my_closed = pyqtSignal(bool)

    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # 滑块初始化
        self.set_qsliders()

        # 挂载任务
        self.worker = Worker()

        # 连接关于的槽函数
        self.actionhelp.triggered.connect(self.show_about)

        # 全局快捷键
        self.set_global_hotkey()

        # 自动连接信号与槽
        QtCore.QMetaObject.connectSlotsByName(self)
        self.set_window_attr()

    def set_window_attr(self):
        # 设置标题
        self.setWindowTitle("CBCT老化测试软件")
        self.setWindowIcon(QIcon(':/icon/ico/ico.ico'))
        # 附加主题
        with open("./theme/MacOS.qss", 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def set_global_hotkey(self):
        # 2. 设置我们的自定义热键响应函数
        self.my_closed.connect(self.hk_handler)
        # 3. 创建快捷键
        self.hk_close = SystemHotkey()
        # 4. 为快捷键绑定处理函数
        self.hk_close.register(('control', '1'), callback=lambda x: self.send_key_event())

    def send_key_event(self):
        self.my_closed[bool].emit(True)

    def hk_handler(self, is_close: bool):
        if is_close:
            self.close()

    def set_qsliders(self):
        self.verticalSlider.setTickPosition(QSlider.TicksRight)
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setValue(50)
        self.verticalSlider.valueChanged.connect(self.change1)
        self.verticalSlider_2.setTickPosition(QSlider.TicksRight)
        self.verticalSlider_2.setMinimum(0)
        self.verticalSlider_2.setMaximum(100)
        self.verticalSlider_2.setValue(50)
        self.verticalSlider_2.valueChanged.connect(self.change2)
        self.verticalSlider_3.setTickPosition(QSlider.TicksRight)
        self.verticalSlider_3.setMinimum(0)
        self.verticalSlider_3.setMaximum(100)
        self.verticalSlider_3.setValue(50)
        self.verticalSlider_3.valueChanged.connect(self.change3)
        self.verticalSlider_4.setTickPosition(QSlider.TicksRight)
        self.verticalSlider_4.setMinimum(0)
        self.verticalSlider_4.setMaximum(100)
        self.verticalSlider_4.setValue(50)
        self.verticalSlider_4.valueChanged.connect(self.change4)

    def show_about(self):
        print("about")
        about_win = AboutWin(self)
        about_win.exec_()

    def show_task(self, msg: str):
        print(msg)

    def end_task(self, is_end):
        if is_end:
            print("任务结束")
            self.statusbar.showMessage("任务结束")

    def change1(self, value: int):
        self.label_7.setText(str(value))

    def change2(self, value: int):
        self.label_8.setText(str(value))

    def change3(self, value: int):
        self.label_9.setText(str(value))

    def change4(self, value: int):
        self.label_10.setText(str(value))

    @pyqtSlot()
    def on_pushButton_clicked(self):
        print(self.lineEdit.text())
        print(self.lineEdit_2.text())
        print(self.verticalSlider.value())
        print(self.verticalSlider_2.value())
        print(self.verticalSlider_3.value())
        print(self.verticalSlider_4.value())
        print("start test")
        self.worker.num = int(self.lineEdit.text()) if self.lineEdit.text() != '' else 10
        self.worker.wait = float(self.lineEdit_2.text()) if self.lineEdit_2.text() != '' else 0.5
        self.worker.weights = [self.verticalSlider.value(), self.verticalSlider_2.value(),
                               self.verticalSlider_3.value(),
                               self.verticalSlider_4.value()]

        # 判断是否需要邮件通知结果

        self.worker.is_send_email = self.checkBox.isChecked()
        self.worker.receiver = self.lineEdit_3.text() if self.lineEdit_3.text() != '' else 'cyjmmy@foxmail.com'

        self.worker.start()


def main():
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
