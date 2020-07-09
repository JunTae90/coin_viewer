import pybithumb

binance_list = ['ADA/BTC', 'ADX/BTC', 'AE/BTC', 'AION/BTC', 'ANKR/BTC', 'ARDR/BTC', 'ARK/BTC', 'ARPA/BTC', 'ATOM/BTC', 'BAT/BTC', 'BCD/BTC', 'BCH/BTC', 'BTC/USDT', 'BTG/BTC', 'BTT/USDT', 'CHR/BTC', 'CHZ/BTC', 'COS/BTC', 'CTXC/BTC', 'CVC/BTC', 'DASH/BTC', 'DCR/BTC', 'ELF/BTC', 'ENJ/BTC', 'EOS/BTC', 'ETC/BTC', 'ETH/BTC', 'GAS/BTC', 'GNT/BTC', 'GRS/BTC', 'GTO/BTC', 'HBAR/BTC', 'ICX/BTC', 'INS/BTC', 'IOST/BTC', 'IOTA/BTC', 'KMD/BTC', 'KNC/BTC', 'LINK/BTC', 'LOOM/BTC', 'LRC/BTC', 'LSK/BTC', 'LTC/BTC', 'MANA/BTC', 'MBL/BTC', 'MCO/BTC', 'MFT/ETH', 'MTL/BTC', 'NEO/BTC', 'NPXS/ETH', 'OMG/BTC', 'ONG/BTC', 'ONT/BTC', 'OST/BTC', 'PIVX/BTC', 'POLY/BTC', 'POWR/BTC', 'QKC/BTC', 'QTUM/BTC', 'REP/BTC', 'SC/BTC', 'SNT/BTC', 'STEEM/BTC', 'STMX/BTC', 'STORJ/BTC', 'STPT/BTC', 'STRAT/BTC', 'SXP/BTC', 'TFUEL/BTC', 'THETA/BTC', 'TRX/BTC', 'VET/BTC', 'WAVES/BTC', 'WTC/BTC', 'XEM/BTC', 'XLM/BTC', 'XRP/BTC', 'ZEC/BTC', 'ZIL/BTC', 'ZRX/BTC']
upbit_list = ['KRW-ADA', 'KRW-ADX', 'KRW-ANKR', 'KRW-ARDR', 'KRW-ARK', 'KRW-ATOM', 'KRW-BAT', 'KRW-BCH', 'KRW-BTC', 'KRW-BTG', 'KRW-BTT', 'KRW-CHZ', 'KRW-CVC', 'KRW-DCR', 'KRW-ELF', 'KRW-ENJ', 'KRW-EOS', 'KRW-ETC', 'KRW-ETH', 'KRW-GAS', 'KRW-GNT', 'KRW-GRS', 'KRW-GTO', 'KRW-HBAR', 'KRW-ICX', 'KRW-IOST', 'KRW-IOTA', 'KRW-KMD', 'KRW-KNC', 'KRW-LOOM', 'KRW-LSK', 'KRW-LTC', 'KRW-MANA', 'KRW-MBL', 'KRW-MCO', 'KRW-MFT', 'KRW-MTL', 'KRW-NEO', 'KRW-NPXS', 'KRW-OMG', 'KRW-ONG', 'KRW-ONT', 'KRW-OST', 'KRW-POLY', 'KRW-POWR', 'KRW-QKC', 'KRW-QTUM', 'KRW-REP', 'KRW-SC', 'KRW-SNT', 'KRW-STEEM', 'KRW-STMX', 'KRW-STORJ', 'KRW-STPT', 'KRW-STRAT', 'KRW-TFUEL', 'KRW-THETA', 'KRW-TRX', 'KRW-VET', 'KRW-WAVES', 'KRW-XEM', 'KRW-XLM', 'KRW-XRP', 'KRW-ZIL', 'KRW-ZRX']
bithumb_list = ['ADA', 'AE', 'AION', 'AMO', 'ANKR', 'AOA', 'APIX', 'ARPA', 'BASIC', 'BAT', 'BCD', 'BCH', 'BOA', 'BTC', 'BTG', 'BTT', 'BZNT', 'CHR', 'CON', 'COS', 'COSM', 'CRO', 'CTXC', 'DAC', 'DAD', 'DASH', 'DVP', 'EGG', 'EL', 'ELF', 'EM', 'ENJ', 'EOS', 'ETC', 'ETH', 'FAB', 'FCT', 'FLETA', 'FNB', 'FX', 'GNT', 'GXC', 'HDAC', 'HYC', 'ICX', 'INS', 'IOST', 'IPX', 'ITC', 'KNC', 'LAMB', 'LBA', 'LINK', 'LOOM', 'LRC', 'LTC', 'LUNA', 'MBL', 'MCO', 'META', 'MIX', 'MTL', 'MXC', 'NPXS', 'OGO', 'OMG', 'ORBS', 'PCM', 'PIVX', 'PLX', 'POWR', 'QBZ', 'QKC', 'QTUM', 'REP', 'RNT', 'SNT', 'SOC', 'STEEM', 'STRAT', 'SXP', 'THETA', 'TMTG', 'TRUE', 'TRV', 'TRX', 'VALOR', 'VET', 'VSYS', 'WAVES', 'WAXP', 'WET', 'WICC', 'WOM', 'WTC', 'XEM', 'XLM', 'XPR', 'XRP', 'XSR', 'ZEC', 'ZIL', 'ZRX']


bithumb = pybithumb.Bithumb

prices = bithumb.get_current_price('ALL')
orderbooks = bithumb.get_orderbook('ALL')
orderbooks = orderbooks['data']
for i in bithumb_list:
    current_price = prices[i]['closing_price']
    orderbook = orderbooks[i]
    print(current_price)
    print(orderbook)
