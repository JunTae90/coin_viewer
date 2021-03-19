from PyQt5.QtWidgets import QMainWindow, QScrollArea, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtWidgets
from thread import *

from ui import *

import os
import json

from operator import itemgetter
from debug import debuginfo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.binance = binanceThread()
        self.upbit = upbitThread()
        self.bithumb = bithumbThread()

        self.dir_path = "cfg"
        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)
        self.list_path = "cfg/coin_list.json"
        self.binance_list = list()
        self.upbit_list = list()
        self.bithumb_list = list()
        self.num = self.get_duplicate_list(self.list_path)

        self.binance.binance_data.connect(self.receive_binance)
        self.upbit.upbit_data.connect(self.receive_upbit)
        self.bithumb.bithumb_data.connect(self.receive_bithumb)

        self.binance_dict = dict()
        self.upbit_dict = dict()
        self.bithumb_dict = dict()

        self.scroll = QScrollArea()
        self.widget = MainWidget(num=self.num)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

        self.timer = QTimer()
        self.timer.timeout.connect(self.fusion)
        self.timer.start()

        for i in self.widget.findChildren(CoinWidget):
            i.delSignal.connect(self.delSymbol)
        self.boolSort = False
        self.sortedList = None
        sortBtn = self.widget.findChild(ClickableLabel)
        if sortBtn:
            sortBtn.clicked.connect(self.sortList)

        self.allStart()

    def sortList(self):
        self.boolSort = True

    def delSymbol(self, symbol):
        if symbol != "BTC":
            self.allStop()
            self.binance.delSymbol(symbol)
            self.upbit.delSymbol(symbol)
            self.bithumb.delSymbol(symbol)
            if symbol in self.binance_list:
                self.binance_list.remove(symbol)
            if symbol in self.upbit_list:
                self.upbit_list.remove(symbol)
            if symbol in self.bithumb_list:
                self.bithumb_list.remove(symbol)
            if symbol in self.sortedList:
                self.sortedList.remove(symbol)
            lists = dict()
            lists["binance"] = self.binance_list
            lists["upbit"] = self.upbit_list
            lists["bithumb"] = self.bithumb_list

            with open(self.list_path, 'w') as f:
                json.dump(lists, f)

            self.allStart()

    def allStop(self):
        self.binance.stop()
        self.upbit.stop()
        self.bithumb.stop()
        self.timer.stop()
        while self.binance.isRunning() or self.upbit.isRunning() or self.bithumb.isRunning():
            pass

    def allStart(self):
        self.binance._start()
        self.upbit._start()
        self.bithumb._start()
        self.timer.start()

    def get_duplicate_list(self, path):
        lists = dict()
        if os.path.isfile(path):
            with open(path) as f:
                lists = json.load(f)
            self.binance_list = lists["binance"]
            self.upbit_list = lists["upbit"]
            self.bithumb_list = lists["bithumb"]
        else:
            binanceList = self.binance.get_symbol_list()
            upbitList = self.upbit.get_symbol_list()
            bithumbList = self.bithumb.get_symbol_list()

            binanceUpbitDuplicate = list()
            binanceBithumbDuplicate = list()
            upbitBithumbDuplicate = list()

            for i in binanceList:
                if i in upbitList:
                    binanceUpbitDuplicate.append(i)
                if i in bithumbList:
                    binanceBithumbDuplicate.append(i)

            for i in upbitList:
                if i in bithumbList:
                    upbitBithumbDuplicate.append(i)

            self.binance_list = list(set(binanceUpbitDuplicate + binanceBithumbDuplicate))
            self.upbit_list = list(set(binanceUpbitDuplicate + upbitBithumbDuplicate))
            self.bithumb_list = list(set(binanceBithumbDuplicate + upbitBithumbDuplicate))

            lists["binance"] = self.binance_list
            lists["upbit"] = self.upbit_list
            lists["bithumb"] = self.bithumb_list

            with open(path, 'w') as f:
                json.dump(lists, f)

        self.binance.save_list(self.binance_list)
        self.upbit.save_list(self.upbit_list)
        self.bithumb.save_list(self.bithumb_list)

        num = len(set(lists["binance"] + lists["upbit"] + lists["bithumb"]))
        return num

    def receive_binance(self, data):
        self.binance_dict = data

    def receive_upbit(self, data):
        self.upbit_dict = data

    def receive_bithumb(self, data):
        self.bithumb_dict = data

    def fusion(self):

        try:
            fusion_dict = dict()
            for i in self.binance_dict.keys():
                if "ask" not in self.binance_dict[i].keys():
                    continue
                if "bid" not in self.binance_dict[i].keys():
                    continue
                if (self.binance_dict[i]['ask'] == '0.0/0.0') and (self.binance_dict[i]['bid'] == '0.0/0.0'):
                    continue
                if (i in self.upbit_dict.keys()) or (i in self.bithumb_dict.keys()):
                    calculated_dict = dict()
                    calculated_dict['binance'] = self.binance_dict[i]
                    if i in self.bithumb_dict.keys():
                        calculated_dict['bithumb'] = self.bithumb_dict[i]
                        calculated_dict['bithumb_premium'] = round(((float(
                            self.bithumb_dict[i]['price']) - float(self.binance_dict[i]['price'])) / float(
                            self.binance_dict[i]['price'])) * 100, 2)
                        calculated_dict['main_premium'] = calculated_dict['bithumb_premium']
                    if i in self.upbit_dict.keys():
                        calculated_dict['upbit'] = self.upbit_dict[i]
                        calculated_dict['upbit_premium'] = round(((float(self.upbit_dict[i]['price']) - float(
                            self.binance_dict[i]['price'])) / float(self.binance_dict[i]['price'])) * 100, 2)
                        if 'bithumb_premium' in calculated_dict.keys():
                            if abs(calculated_dict['upbit_premium']) > abs(calculated_dict['bithumb_premium']):
                                calculated_dict['main_premium'] = calculated_dict['upbit_premium']
                        else:
                            calculated_dict['main_premium'] = calculated_dict['upbit_premium']
                    else:
                        calculated_dict['upbit_premium'] = float('inf')
                    fusion_dict[i] = calculated_dict

            if self.boolSort:
                fusion_list = list()
                for i in fusion_dict.keys():
                    data = fusion_dict[i]
                    fusion_list.append({"symbol":i, "upbit_premium":data["upbit_premium"]})
                    fusion_list.sort(key=itemgetter("upbit_premium"))

                self.sortedList = list()
                for j in fusion_list:
                    self.sortedList.append(j["symbol"])

                self.boolSort = False

            if not self.sortedList:
                lists = fusion_dict.keys()
            else:
                lists = self.sortedList

            for i in range(self.num):
                widget_name = "coin_widget_{}".format(i)
                widget = self.findChild(CoinWidget, widget_name)
                widget.clear()
            cnt = 0
            for i in lists:
                data = fusion_dict[i]
                widget_name = "coin_widget_{}".format(cnt)
                widget = self.findChild(CoinWidget, widget_name)
                widget.setData(i, data)
                cnt += 1

        except Exception as e:
            debuginfo(e)
            pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(1280, 800)
    w.show()
    sys.exit(app.exec_())
