from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QThread, QWaitCondition, QMutex, pyqtSignal
import os
import pybithumb

class bithumbThread(QThread):
    bithumb_data = pyqtSignal(dict)
    def __init__(self):
        QThread.__init__(self)
        self.mutex = QMutex()
        self.bithumb = pybithumb.Bithumb

    def __del__(self):
        self.wait()
    
    def get_symbol_list(self):
        DATA_DIR = './data'
        try:
            with open(os.path.join(DATA_DIR, 'bithumb_list.txt'), 'r') as f:
                bithumb_list = f.read().split('\n')
                if '' in bithumb_list:
                        bithumb_list.remove('')
                return bithumb_list
    
        except Exception as e:
            print(e)
            return None
        
    def run(self):
        while True:
            self.mutex.lock()
            try:
                bithumb_dict = dict()
                symbol_list = self.get_symbol_list()
                prices = self.bithumb.get_current_price('ALL')
                orderbooks = self.bithumb.get_orderbook('ALL')['data']
                for i in symbol_list:
                    price = prices[i]['closing_price']
                    orderbook = orderbooks[i]
                    ask = orderbook['asks'][0]['price']+'/'+str(round(float(orderbook['asks'][0]['quantity']), 2))
                    bid = orderbook['bids'][0]['price']+'/'+str(round(float(orderbook['bids'][0]['quantity']), 2))
                    bithumb_dict[i] = dict()
                    bithumb_dict[i]['price'] = price
                    bithumb_dict[i]['ask'] = ask
                    bithumb_dict[i]['bid'] = bid

                self.bithumb_data.emit(bithumb_dict)
            except Exception as e:
                print(e)
                continue
            self.mutex.unlock()
