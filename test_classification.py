import pyupbit

upbit_list = []
tickers = pyupbit.get_tickers(fiat="KRW")
for i in tickers:
    i = i.split('-')
    upbit_list.append(i[0])
    upbit_list.append(i[1])

upbit_list = sorted(list(set(upbit_list)), key=str.lower)
# print(upbit_list)

import ccxt

binance_list = []
binance = ccxt.binance()
markets = binance.fetch_tickers()
print(markets.keys())
for i in markets.keys():
    i = i.split('/')
    binance_list.append(i[0])
    binance_list.append(i[1])

binance_list = sorted(list(set(binance_list)), key=str.lower)

import pybithumb

bithumb = pybithumb.Bithumb
bithumb_list = sorted(bithumb.get_tickers(), key=str.lower)

binance_classified = []
upbit_classified = []
bithumb_classifed = []
for i in binance_list:
    if i in upbit_list:
        upbit_classified.append(i)
        binance_classified.append(i)
    if i in bithumb_list:
        bithumb_classifed.append(i)
        binance_classified.append(i)
binance_classified = sorted(list(set(binance_classified)), key=str.lower)
# print(binance_classified)
# print(upbit_classified)
# print(bithumb_classifed)

binance_list = []
for i in binance_classified:
    if i == 'BTC':
        i += '/USDT'
    else:
        i+= '/BTC'
    binance_list.append(i)

upbit_list = []
for i in upbit_classified:
    i = 'KRW-' + i
    upbit_list.append(i)

# print(binance_list)
# print(upbit_list)
# print(bithumb_list)
