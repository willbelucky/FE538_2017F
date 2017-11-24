# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 23.
"""
from data.data_reader import get_stock_price, get_stock_master, STOCK_PRICE_CACHE, get_highest_volatility

if __name__ == '__main__':
    import threading

    print('{} is started...'.format('Caching'))

    for code, name in get_stock_master().iterrows():
        print(code)
        STOCK_PRICE_CACHE[code] = get_stock_price([code])

    print('{} is done!!'.format('Caching'))

    # Save highest volatility data for preparing future.
    print('{} is started...'.format('get_highest_volatility'))
    stock_masters = get_stock_master()
    threads = []
    for window in range(20, 101):
        # highest_volatilities = get_highest_volatility(window, stock_masters)
        thread = threading.Thread(target=get_highest_volatility, args=(window, stock_masters))
        thread.start()
        # print(highest_volatilities.head())
    print('{} is done!!'.format('get_highest_volatility'))
