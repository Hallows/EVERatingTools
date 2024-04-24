from UI_settings import Ui_settings
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import *
from configControl import *


class settingWindow(Ui_settings, QWidget):
    settingSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.dailyGoal = None
        self.setupUi(self)

    def set_save(self):
        try:
            dailyGoal = int(self.LE_set_dailyGoals.text())
            if dailyGoal<=0:
                QMessageBox.warning(self, "Warning", "Daily Goal must bigger than 0!")
                return
        except:
            QMessageBox.warning(self, "Warning", "Daily Goal is not a number!")
            return
        updateConfig_dailyGoals(dailyGoal)
        updateConfig_updateSpeed(self.LE_set_speedUpdate.currentIndex())
        updateConfig_language(self.LE_set_language.currentIndex())
        updateConfig_hideAD(self.CB_set_showAD.isChecked())
        updateConfig_hideProcessBar(self.CB_set_showProcess.isChecked())

        self.settingSignal.emit()
        self.close()

    def set_cancel(self):
        self.close()
