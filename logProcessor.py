import os
import time
import re
from PyQt5.QtCore import *


class bountyCountThread(QThread):
    signal_totalIncome = pyqtSignal(str)
    signal_ESSIncome = pyqtSignal(str)

    def __init__(self):
        super(bountyCountThread, self).__init__()
        self.is_running = True
        self.count = 0
        self.aimCount = 0
        self.totalCount = 0
        self.ESSCount = 0

    def find_numbers_and_commas(self, text):
        index_isk = text.find('ISK')  # 找到ISK的位置
        if index_isk >= 13:  # 确保在ISK之前至少有10个字符
            start_index = index_isk - 10  # 开始位置
            relevant_text = text[start_index:index_isk]  # 获取前10个字符
            numbers_and_commas = [char for char in relevant_text if char.isdigit() or char == ',']  # 提取数字和逗号
            return ''.join(numbers_and_commas)  # 将列表中的字符连接成一个字符串
        else:
            return None

    def getLogFile(self):
        user_folder = os.path.expanduser("~")
        eveLogFolder = os.path.join(user_folder, "Documents", "EVE", "logs", "Gamelogs")
        # 获取文件夹中所有文件的路径和最后修改时间
        files = [(os.path.join(eveLogFolder, f), os.path.getmtime(os.path.join(eveLogFolder, f))) for f in
                 os.listdir(eveLogFolder)]
        # 如果文件夹中有文件
        if files:
            # 找到最后一次修改的文件
            latest_file = max(files, key=lambda x: x[1])

            # 获取最后一次修改的文件名
            latest_file_name = os.path.basename(latest_file[0])

            print("最后一次修改的文件名是:", latest_file_name)
        else:
            print("文件夹中没有文件")
            return
            # 指定日志文件路径
        log_file_path = os.path.join(eveLogFolder, latest_file_name)
        return log_file_path

    def run(self):
        with open(self.getLogFile(), "r") as file:
            # 指定初始文件指针位置
            file.seek(0, 2)  # 将文件指针移动到文件末尾

            while self.is_running:
                where = file.tell()  # 记录当前文件指针位置
                line = file.readline()
                if not line:
                    time.sleep(0.1)  # 如果没有新内容，等待一段时间后继续
                    file.seek(where)  # 将文件指针移动到记录的位置
                else:
                    if 'bounty' in line:
                        match = self.find_numbers_and_commas(line)
                        if match:
                            number = int(match.replace(',', ''))  # 将包含逗号的数字字符串转换为整数
                            self.totalCount = self.totalCount + number
                            self.ESSCount = int(self.ESSCount + (number * 0.59723))
                            tmp = "Get income: " + str(number) + " ，Total Count till now is " + str(
                                self.totalCount) + " ,with ESSPayout: " + str(number * 0.59723)
                            print(tmp)
                            self.signal_totalIncome.emit(str(self.totalCount))
                            self.signal_ESSIncome.emit(str(self.ESSCount))
                            self.aimCount = self.aimCount + 1
                            if self.aimCount == 5:
                                tmp = "For now you got " + str(
                                    self.totalCount) + "ISK, Consider Corp Tax Rate 10%, final income is " + str(
                                    self.totalCount * 0.9) + "ISK" + ", ESS has " + str(self.ESSCount) + "ISK"
                                print(tmp)
                                self.aimCount = 0
                        else:
                            print('Error!' + line, end='')  # 处理读取到的日志内容
    def stop(self):
        self.is_running = False
        print('stopping thread...')
        self.terminate()