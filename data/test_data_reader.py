# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 16.
"""
from unittest import TestCase
from data.data_reader import *


class TestGetStockMaster(TestCase):
    def test_get_stock_master(self):
        print('{} is started...'.format(self._testMethodName))
        stock_masters = get_stock_master()
        self.assertEqual(1976, len(stock_masters))
        print('{} is done!!'.format(self._testMethodName))


class TestGetStockPrice(TestCase):
    def test_get_stock_price_single(self):
        print('{} is started...'.format(self._testMethodName))
        stock_masters = get_stock_master()

        for code, name in stock_masters.sample(n=3).iterrows():
            stock_prices = get_stock_price([code])
            print(code)
            print(stock_prices.head())
            self.assertEqual(739, len(stock_prices))
            self.assertEqual(sorted(['date', 'code']), sorted(stock_prices.index.names))
            self.assertEqual(sorted(['market_capitalization', 'listed_stocks_number', 'adj_close']),
                             sorted(stock_prices.columns.values))

        print('{} is done!!'.format(self._testMethodName))

    def test_get_stock_price_multi(self):
        print('{} is started...'.format(self._testMethodName))
        stock_masters = get_stock_master()

        codes = stock_masters.sample(n=3).index.values
        print(codes)
        stock_prices = get_stock_price(codes)
        print(stock_prices.head())
        self.assertEqual(739 * 3, len(stock_prices))
        self.assertEqual(sorted(['date', 'code']), sorted(stock_prices.index.names))
        self.assertEqual(sorted(['market_capitalization', 'listed_stocks_number', 'adj_close']),
                         sorted(stock_prices.columns.values))

        print('{} is done!!'.format(self._testMethodName))


class TestGetHighestVolatility(TestCase):
    def test_get_highest_volatility(self):
        print('{} is started...'.format(self._testMethodName))
        stock_masters = get_stock_master()
        highest_volatilities = get_highest_volatility(window=7, stock_masters=stock_masters.sample(10))
        print(highest_volatilities.head())
        self.assertEqual(10, len(highest_volatilities))
        self.assertEqual(sorted(['code']), sorted(highest_volatilities.index.names))
        self.assertEqual(sorted(['highest_volatility_7']), sorted(highest_volatilities.columns.values))
        print('{} is done!!'.format(self._testMethodName))


class TestGetMarketCapitalizationSum(TestCase):
    def test_get_market_capitalization_sum(self):
        print('{} is started...'.format(self._testMethodName))
        stock_masters = get_stock_master()
        market_capitalization_sums = get_market_capitalization_sum(stock_masters.sample(n=100))
        print(market_capitalization_sums.head())
        self.assertEqual(739, len(market_capitalization_sums))
        self.assertEqual(sorted(['date']), sorted(market_capitalization_sums.index.names))
        self.assertEqual(sorted(['selected_sum', 'total_sum', 'portion']),
                         sorted(market_capitalization_sums.columns.values))
        print('{} is done!!'.format(self._testMethodName))
