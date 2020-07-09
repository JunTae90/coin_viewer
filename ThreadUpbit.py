from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QThread, QWaitCondition, QMutex, pyqtSignal
import os
import pyupbit

class upbitThread(QThread):
    upbit_data = pyqtSignal(dict)
    def __init__(self):
        QThread.__init__(self)
        self.mutex = QMutex()

    def __del__(self):
        self.wait()
    
    def get_symbol_list(self):
        DATA_DIR = './data'
        try:
            with open(os.path.join(DATA_DIR, 'upbit_list.txt'), 'r') as f:
                upbit_list = f.read().split('\n')
                if '' in upbit_list:
                    upbit_list.remove('')
                return upbit_list
    
        except Exception as e:
            print(e)
            return None
        
    def run(self):
        while True:
            self.mutex.lock()
            try:
                upbit_dict = dict()
                symbol_list = self.get_symbol_list()
                prices = pyupbit.get_current_price(symbol_list)
                orderbooks = pyupbit.get_orderbook(symbol_list)
                for i in orderbooks:
                    symbol = i['market'].split('-')[1]
                    orderbook = i['orderbook_units'][0]
                    ask = str(orderbook['ask_price'])+'/'+str(round(orderbook['ask_size'], 2))
                    bid = str(orderbook['bid_price'])+'/'+str(round(orderbook['bid_size'], 2))
                    upbit_dict[symbol] = dict()
                    upbit_dict[symbol]['price'] = str(round(prices[i['market']],2))
                    upbit_dict[symbol]['ask'] = ask
                    upbit_dict[symbol]['bid'] = bid
                self.upbit_data.emit(upbit_dict)
            except Exception as e:
                print(e)
                continue
            self.mutex.unlock()
