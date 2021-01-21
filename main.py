from PyQt5.QtCore import QTimer

from GUI import *
from Thread import binanceThread
from Thread import upbitThread
from Thread import bithumbThread

from operator import itemgetter

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.binance = binanceThread()
        self.upbit = upbitThread()
        self.bithumb = bithumbThread()

        self.get_duplicate_list()
        self.binance.start()
        self.upbit.start()
        self.bithumb.start()

        self.binance.binance_data.connect(self.receive_binance)
        self.upbit.upbit_data.connect(self.receive_upbit)
        self.bithumb.bithumb_data.connect(self.receive_bithumb)

        self.binance_dict = dict()
        self.upbit_dict = dict()
        self.bithumb_dict = dict()

        self.rank = dict()
        self.rank_on = True
        self.ui.pushButton.clicked.connect(self.rank_update)

        self.timer = QTimer()
        self.timer.timeout.connect(self.fusion)
        self.timer.start()

    def rank_update(self):
        if self.rank_on:
            self.rank_on = False
            self.ui.pushButton.setText('Start')
        else:
            self.rank_on = True
            self.ui.pushButton.setText('Stop')

    def fusion(self):
        fusion_list = list()
        try:
            for i in self.binance_dict.keys():
                if (self.binance_dict[i]['ask'] == '0.0/0.0') and (self.binance_dict[i]['bid'] == '0.0/0.0'):
                    continue
                if (i in self.upbit_dict.keys()) or (i in self.bithumb_dict.keys()):
                    calculated_dict = dict()
                    calculated_dict['binance'] = self.binance_dict[i]
                    calculated_dict['symbol'] = i
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
                    fusion_list.append(calculated_dict)
            if len(fusion_list) > 0:
                fusion_list.sort(key=itemgetter('main_premium'))
                if self.rank_on:
                    for i in range(len(fusion_list)):
                        symbol = fusion_list[i]['symbol']
                        rank = i + 1
                        self.rank[symbol] = rank

                for i in fusion_list:
                    symbol = i['symbol']
                    getattr(self.ui, 'coin_{}'.format(self.rank[symbol])).setText(symbol)
                    if 'binance' in i.keys():
                        binance_data = i['binance']
                        getattr(self.ui, 'price_binance_coin_{}'.format(self.rank[symbol])).setText(
                            binance_data['price'])
                        getattr(self.ui, 'ask_binance_coin_{}'.format(self.rank[symbol])).setText(
                            binance_data['ask'])
                        getattr(self.ui, 'bid_binance_coin_{}'.format(self.rank[symbol])).setText(
                            binance_data['bid'])
                    else:
                        getattr(self.ui, 'price_binance_coin_{}'.format(self.rank[symbol])).setText('')
                        getattr(self.ui, 'ask_binance_coin_{}'.format(self.rank[symbol])).setText('')
                        getattr(self.ui, 'bid_binance_coin_{}'.format(self.rank[symbol])).setText('')
                    if 'upbit' in i.keys():
                        upbit_data = i['upbit']
                        getattr(self.ui, 'price_upbit_coin_{}'.format(self.rank[symbol])).setText(
                            upbit_data['price'] + '/' + str(i['upbit_premium']) + '%')
                        getattr(self.ui, 'ask_upbit_coin_{}'.format(self.rank[symbol])).setText(
                            upbit_data['ask'])
                        getattr(self.ui, 'bid_upbit_coin_{}'.format(self.rank[symbol])).setText(
                            upbit_data['bid'])
                    else:
                        getattr(self.ui, 'price_upbit_coin_{}'.format(self.rank[symbol])).setText('')
                        getattr(self.ui, 'ask_upbit_coin_{}'.format(self.rank[symbol])).setText('')
                        getattr(self.ui, 'bid_upbit_coin_{}'.format(self.rank[symbol])).setText('')
                    if 'bithumb' in i.keys():
                        bithumb_data = i['bithumb']
                        getattr(self.ui, 'price_bithumb_coin_{}'.format(self.rank[symbol])).setText(
                            bithumb_data['price'] + '/' + str(i['bithumb_premium']) + '%')
                        getattr(self.ui, 'ask_bithumb_coin_{}'.format(self.rank[symbol])).setText(
                            bithumb_data['ask'])
                        getattr(self.ui, 'bid_bithumb_coin_{}'.format(self.rank[symbol])).setText(
                            bithumb_data['bid'])
                    else:
                        getattr(self.ui, 'price_bithumb_coin_{}'.format(self.rank[symbol])).setText('')
                        getattr(self.ui, 'ask_bithumb_coin_{}'.format(self.rank[symbol])).setText('')
                        getattr(self.ui, 'bid_bithumb_coin_{}'.format(self.rank[symbol])).setText('')

        except Exception as e:
            print(e)
            pass

    def receive_binance(self, data):
        self.binance_dict = data

    def receive_upbit(self, data):
        self.upbit_dict = data

    def receive_bithumb(self, data):
        self.bithumb_dict = data

    def get_duplicate_list(self):
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

        newBinanceList = list(set(binanceUpbitDuplicate + binanceBithumbDuplicate))
        newUpbitList = list(set(binanceUpbitDuplicate + upbitBithumbDuplicate))
        newBithumbList = list(set(binanceBithumbDuplicate + upbitBithumbDuplicate))

        self.binance.save_list(newBinanceList)
        self.upbit.save_list(newUpbitList)
        self.bithumb.save_list(newBithumbList)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())