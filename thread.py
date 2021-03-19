from PyQt5.QtCore import QThread, QMutex, pyqtSignal
from binance.client import Client
import pyupbit
import pybithumb

import requests
from bs4 import BeautifulSoup

from debug import debuginfo

class binanceThread(QThread):
    binance_data = pyqtSignal(dict)
    def __init__(self):
        QThread.__init__(self)
        self.mutex = QMutex()
        self.binance = Client()
        self.binanceList = list()
        self.exchange_rate = float(1100)
        self.isRun = True

    def delSymbol(self, symbol):
        if symbol+"BTC" in self.binanceList:
            self.binanceList.remove(symbol+"BTC")

    def _start(self):
        self.isRun = True
        self.start()

    def stop(self):
        self.isRun = False

    def get_symbol_list(self):
        binanceList = list()
        try:
            for i in self.binance.get_all_tickers():
                symbol = i['symbol']
                if symbol[-3:] == 'BTC':
                    binanceList.append(symbol[:-3])
                if symbol == 'BTCUSDT':
                    binanceList.append(symbol[:-4])
        except Exception as e:
            debuginfo(e)
            pass
        return binanceList


    def save_list(self, list):
        for i in list:
            if i == 'BTC':
                self.binanceList.append('BTCUSDT')
            else:
                self.binanceList.append(i+'BTC')

    def get_dollor(self):
        try:
            res = requests.get('http://finance.naver.com/')
            text = res.text
            soup = BeautifulSoup(text, 'html.parser')
            td = soup.select_one(
                "#content > div.article2 > div.section1 > div.group1 > table > tbody > tr > td")
            exchange_rate = ''
            for i in td.text:
                if i == ',':
                    pass
                else:
                    exchange_rate += i
            self.exchange_rate = float(exchange_rate)
        except Exception as e:
            debuginfo(e)

    def get_prices(self):
        prices = dict()
        try:
            for i in self.binance.get_all_tickers():
                prices[i['symbol']] = i['price']
        except Exception as e:
            debuginfo(e)
            pass
        return prices

    def get_orderbooks(self):
        orderbooks = dict()
        try:
            for i in self.binance.get_orderbook_tickers():
                orderbooks[i['symbol']] = dict()
                orderbooks[i['symbol']]['bidPrice'] = i['bidPrice']
                orderbooks[i['symbol']]['bidQty'] = i['bidQty']
                orderbooks[i['symbol']]['askPrice'] = i['askPrice']
                orderbooks[i['symbol']]['askQty'] = i['askQty']
        except Exception as e:
            debuginfo(e)
            pass
        return orderbooks

    def calculate_krw(self, price, BTCUSDT, exchange_rate):
        return str(round(float(price) * BTCUSDT * exchange_rate, 2))

    def run(self):
        while self.isRun:
            self.mutex.lock()
            binanceDict = dict()
            self.get_dollor()
            prices = self.get_prices()
            orderbooks = self.get_orderbooks()

            try:
                BTCUSDT = float(prices['BTCUSDT'])
                binanceDict['BTC'] = dict()
                binanceDict['BTC']['price'] = str(round(BTCUSDT * self.exchange_rate, 2))
                binanceDict['BTC']['ask'] = str(
                    round(float(orderbooks['BTCUSDT']['askPrice']) * self.exchange_rate, 2)) + '/' + str(
                    round(float(orderbooks['BTCUSDT']['askQty']), 2))
                binanceDict['BTC']['bid'] = str(
                    round(float(orderbooks['BTCUSDT']['bidPrice']) * self.exchange_rate, 2)) + '/' + str(
                    round(float(orderbooks['BTCUSDT']['bidQty']), 2))

            except Exception as e:
                debuginfo(e)

            for i in self.binanceList:
                if i == 'BTCUSDT':
                    continue
                try:
                    symbol = i.replace('BTC', '')
                    binanceDict[symbol] = dict()
                    binanceDict[symbol]['price'] = self.calculate_krw(prices[i], BTCUSDT, self.exchange_rate)
                    binanceDict[symbol]['ask'] = self.calculate_krw(orderbooks[i]['askPrice'], BTCUSDT, self.exchange_rate) + '/' + str(round(float(orderbooks[i]['askQty']), 2))
                    binanceDict[symbol]['bid'] = self.calculate_krw(orderbooks[i]['bidPrice'], BTCUSDT, self.exchange_rate) + '/' + str(round(float(orderbooks[i]['bidQty']), 2))
                except Exception as e:
                    debuginfo(e)
                    pass

            self.binance_data.emit(binanceDict)
            self.mutex.unlock()


class upbitThread(QThread):
    upbit_data = pyqtSignal(dict)
    def __init__(self):
        QThread.__init__(self)
        self.mutex = QMutex()
        self.upbit = pyupbit
        self.upbitList = list()
        self.isRun = True

    def delSymbol(self, symbol):
        if "KRW-"+symbol in self.upbitList:
            self.upbitList.remove("KRW-"+symbol)

    def _start(self):
        self.isRun = True
        self.start()

    def stop(self):
        self.isRun = False

    def get_symbol_list(self):
        upbitList = list()
        try:
            for i in self.upbit.get_tickers(fiat="KRW"):
                upbitList.append(i.split('KRW-')[1])
        except Exception as e:
            debuginfo(e)
            pass
        return upbitList

    def save_list(self, list):
        for i in list:
            self.upbitList.append('KRW-'+i)

    def run(self):
        while self.isRun:
            self.mutex.lock()
            upbitDict = dict()
            prices = self.upbit.get_current_price(self.upbitList)
            orderbooks = self.upbit.get_orderbook(self.upbitList)
            if orderbooks and prices:
                for i in orderbooks:
                    try:
                        symbol = i['market'].split('-')[1]
                        orderbook = i['orderbook_units'][0]
                        ask = str(orderbook['ask_price']) + '/' + str(round(orderbook['ask_size'], 2))
                        bid = str(orderbook['bid_price']) + '/' + str(round(orderbook['bid_size'], 2))
                        upbitDict[symbol] = dict()
                        upbitDict[symbol]['price'] = str(round(prices[i['market']], 2))
                        upbitDict[symbol]['ask'] = ask
                        upbitDict[symbol]['bid'] = bid
                    except Exception as e:
                        debuginfo(e)
                self.upbit_data.emit(upbitDict)
            self.mutex.unlock()

class bithumbThread(QThread):
    bithumb_data = pyqtSignal(dict)
    def __init__(self):
        QThread.__init__(self)
        self.mutex = QMutex()
        self.bithumb = pybithumb.Bithumb
        self.bithumbList = list()
        self.isRun = True

    def delSymbol(self, symbol):
        if symbol in self.bithumbList:
            self.bithumbList.remove(symbol)

    def _start(self):
        self.isRun = True
        self.start()

    def stop(self):
        self.isRun = False

    def get_symbol_list(self):
        bithumbList = list()
        try:
            bithumbList = self.bithumb.get_tickers()
        except Exception as e:
            debuginfo(e)
            pass
        return bithumbList

    def save_list(self, list):
        self.bithumbList = list

    def run(self):
        while self.isRun:
            self.mutex.lock()
            bithumbDict = dict()

            prices = self.bithumb.get_current_price('ALL')
            orderbooks = self.bithumb.get_orderbook('ALL')
            if orderbooks and prices:
                orderbooks = orderbooks['data']
                for i in self.bithumbList:
                    try:
                        price = prices[i]['closing_price']
                        orderbook = orderbooks[i]
                        ask = orderbook['asks'][0]['price'] + '/' + str(round(float(orderbook['asks'][0]['quantity']), 2))
                        bid = orderbook['bids'][0]['price'] + '/' + str(round(float(orderbook['bids'][0]['quantity']), 2))
                        bithumbDict[i] = dict()
                        bithumbDict[i]['price'] = price
                        bithumbDict[i]['ask'] = ask
                        bithumbDict[i]['bid'] = bid
                    except Exception as e:
                        debuginfo(e)
                        pass
                self.bithumb_data.emit(bithumbDict)
            self.mutex.unlock()

if __name__ == "__main__":
    binance = binanceThread()
    upbit = upbitThread()
    bithumb = bithumbThread()

    binanceList = binance.get_symbol_list()
    upbitList = upbit.get_symbol_list()
    bithumbList = bithumb.get_symbol_list()

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

    newBinanceList = list(set(binanceUpbitDuplicate+binanceBithumbDuplicate))
    newUpbitList = list(set(binanceUpbitDuplicate+upbitBithumbDuplicate))
    newBithumbList = list(set(binanceBithumbDuplicate+upbitBithumbDuplicate))

    binance.save_list(newBinanceList)
    upbit.save_list(newUpbitList)
    bithumb.save_list(newBithumbList)
