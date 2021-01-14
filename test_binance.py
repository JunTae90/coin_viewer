import ccxt
from binance.client import Client

binance = ccxt.binance()
markets = binance.fetch_tickers()

binanceList = list()
for i in markets.keys():
    for j in i.split('/'):
        binanceList.append(j)

binanceList = list(set(binanceList))
print(binanceList)

# client = Client()
# prices = dict()
#
# for i in client.get_all_tickers():
#     prices[i['symbol']] = i['price']
#
# orderbooks = dict()
# for i in client.get_orderbook_tickers():
#     orderbooks[i['symbol']] = dict()
#     orderbooks[i['symbol']]['bidPrice'] = i['bidPrice']
#     orderbooks[i['symbol']]['bidQty'] = i['bidQty']
#     orderbooks[i['symbol']]['askPrice'] = i['askPrice']
#     orderbooks[i['symbol']]['askQty'] = i['askQty']
#
# binanceList = list()
#
# for i in client.get_all_tickers():
#     symbol = i['symbol']
#     if 'BTC' in symbol:
#         print(symbol)

# if 'BTC' in 'BTCUSDT':
#     print('BTCUSDT'.replace('BTC', ''))