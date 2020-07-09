from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QThread, QWaitCondition, QMutex, pyqtSignal
import requests
from bs4 import BeautifulSoup
from binance.client import Client
import os

class binanceThread(QThread):
    binance_data = pyqtSignal(dict)
    def __init__(self):
        QThread.__init__(self)
        self.mutex = QMutex()
        self.url = 'http://finance.naver.com/'
        self.client = Client()

    def __del__(self):
        self.wait()
    
    def get_symbol_list(self):
        DATA_DIR = './data'
        try:
            with open(os.path.join(DATA_DIR, 'binance_list.txt'), 'r') as f:
                binance_list = f.read().split('\n')
                if '' in binance_list:
                    binance_list.remove('')
                return binance_list
    
        except Exception as e:
            print(e)
            return None

    def get_dollor(self):
        try:
            res = requests.get(self.url)
            text = res.text
            soup = BeautifulSoup(text, 'html.parser')
            td = soup.select_one("#content > div.article2 > div.section1 > div.group1 > table > tbody > tr > td")
            exchange_rate = ''
            for i in td.text:
                if i == ',':
                    pass
                else:
                    exchange_rate += i
            exchange_rate = float(exchange_rate)
            return exchange_rate
        except Exception as e:
            print(e)
            return None
    
    def get_orderbooks(self):
        try:
            orderbooks = dict()
            for i in self.client.get_orderbook_tickers():
                orderbooks[i['symbol']] = dict()
                orderbooks[i['symbol']]['bidPrice'] = i['bidPrice']
                orderbooks[i['symbol']]['bidQty'] = i['bidQty']
                orderbooks[i['symbol']]['askPrice'] = i['askPrice']
                orderbooks[i['symbol']]['askQty'] = i['askQty']
            return orderbooks
        except Exception as e:
            print(e)
            return None

    
    def get_prices(self):
        try:
            prices = dict()
            for i in self.client.get_all_tickers():
                prices[i['symbol']] = i['price']
            return prices
        except Exception as e:
            print(e)
            return None
    
    def calculate_krw(self, price, btc_usdt, exchange_rate):
        return str(round(float(price) * btc_usdt * exchange_rate, 2))

    def run(self):
        while True:
            self.mutex.lock()
            try:
                binance_dict = dict()
                symbol_list = self.get_symbol_list()
                exchange_rate = self.get_dollor()
                prices = self.get_prices()
                orderbooks = self.get_orderbooks()

                if exchange_rate and prices and orderbooks and symbol_list:
                    btc_usdt = float(prices['BTCUSDT'])
                    binance_dict['BTC'] = dict()
                    binance_dict['BTC']['price'] = str(round(btc_usdt * exchange_rate, 2))
                    binance_dict['BTC']['ask'] = self.calculate_krw(orderbooks['BTCUSDT']['askPrice'], btc_usdt, exchange_rate)+'/'+str(round(float(orderbooks['BTCUSDT']['askQty']), 2))
                    binance_dict['BTC']['bid'] = self.calculate_krw(orderbooks['BTCUSDT']['bidPrice'], btc_usdt, exchange_rate)+'/'+str(round(float(orderbooks['BTCUSDT']['bidQty']), 2))
                    for i in symbol_list:
                        symbol = i.replace('BTC', '')
                        binance_dict[symbol] = dict()
                        binance_dict[symbol]['price'] = self.calculate_krw(prices[i], btc_usdt, exchange_rate)
                        binance_dict[symbol]['ask'] = self.calculate_krw(orderbooks[i]['askPrice'], btc_usdt, exchange_rate)+'/'+str(round(float(orderbooks[i]['askQty']), 2))
                        binance_dict[symbol]['bid'] = self.calculate_krw(orderbooks[i]['bidPrice'], btc_usdt, exchange_rate)+'/'+str(round(float(orderbooks[i]['bidQty']), 2))
                    self.binance_data.emit(binance_dict)
            except Exception as e:
                print(e)
                continue
            self.mutex.unlock()