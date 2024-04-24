import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import *
from datetime import datetime
from settings import settingWindow
from configControl import *

from UI_mainWindow import Ui_MainWindow
from logProcessor import *
from Algorithm import seconds_to_hms

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.settingWindow = settingWindow()
        self.setFixedSize(597, 369)
        self.timerCount = 0
        self.avgCount = 0
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerTimeOut)
        self.countThread = bountyCountThread()
        self.countThread.signal_totalIncome.connect(self.set_label_totalIncome)
        self.countThread.signal_ESSIncome.connect(self.set_label_ESSIncome)
        self.settingWindow.settingSignal.connect(self.settingUpdate)

    def startCount(self):
        self.countThread.is_running = True
        self.countThread.start()
        self.timer.start(1000)

    def stopCount(self):
        self.countThread.is_running = False
        self.timer.stop()
        self.timerCount = 0
        self.countThread.aimCount = 0
        self.countThread.totalCount = 0
        self.countThread.ESSCount = 0
        self.avgCount = 0

    def timerTimeOut(self):
        self.timerCount = self.timerCount + 1
        self.set_label_rattingTime(seconds_to_hms(self.timerCount))
        if self.timerCount % 300 == 0:
            self.avgCount = self.avgCount + 1
            tmp = str(int(self.countThread.totalCount / self.avgCount)) + "/5mins"
            self.set_label_ISKSpeed(tmp)

    def set_label_totalIncome(self, value):
        self.active_totalIncome.setText(value)
        dailyGoals=self.active_dailyGoals.getText()
        dailyGoals=int(dailyGoals)
        processPercent=int((int(value)/dailyGoals)*100)
        if processPercent>=100:
            self.progressBar.setValue(100)
        else:
            self.progressBar.setValue(processPercent)
        if int(value)>dailyGoals:
            self.active_dailyGoals.setStyleSheet("color:green")

    def set_label_rattingTime(self, value):
        self.active_rattingTime.setText(value)

    def set_label_ESSIncome(self, value):
        self.active_ESSIncome.setText(value)

    def set_label_ISKSpeed(self, value):
        self.active_ISKSpeed.setText(value)

    def showSettings(self):
        self.settingWindow.show()

    def settingUpdate(self):
        data=readConfig()
        self.active_dailyGoals.setText(str(data['dailyGoals']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
