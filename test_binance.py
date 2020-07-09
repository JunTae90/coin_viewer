import ccxt
from binance.client import Client

client = Client()
prices = dict()
for i in client.get_all_tickers():
    prices[i['symbol']] = i['price']

orderbooks = dict()
for i in client.get_orderbook_tickers():
    orderbooks[i['symbol']] = dict()
    orderbooks[i['symbol']]['bidPrice'] = i['bidPrice']
    orderbooks[i['symbol']]['bidQty'] = i['bidQty']
    orderbooks[i['symbol']]['askPrice'] = i['askPrice']
    orderbooks[i['symbol']]['askQty'] = i['askQty']
print(orderbooks)


if 'BTC' in 'BTCUSDT':
    print('BTCUSDT'.replace('BTC', ''))