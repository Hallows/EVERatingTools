from UI_settings import Ui_settings
from PyQt5.QtWidgets import QWidget


class settingWindow(Ui_settings,QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def set_save(self):
        print("saved")

    def set_cancel(self):
        print("cancel")
