# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 21.
"""
from K_means.k_means import get_highest_volatility_group
from data.data_reader import get_market_capitalization_sum

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


def do_anova_test(n, k):
    """

    ANOVA 테스트를 수행하여 (n, k)로 구한 p_1 = p_2 = ... = p_{740-n}을 검증한다.
    검증 결과 같지 않은 portion이 있다면 False를 return하고 모두 같다면 True를 리턴한다.

    :param n: (int) size of an window.
    :param k: (int) size of group of K_means

    :return test_result: (Boolean) ANOVA 테스트의 결과.
        p_1 = p_2 = ... = p_{740-n}이면 True, 아니면 False
    """
    high_volatility_stock_masters = get_highest_volatility_group(n, k)
    market_capitalization_sums = get_market_capitalization_sum(high_volatility_stock_masters)[::2]
    market_capitalization_sums['rolling']=pd.rolling_mean(market_capitalization_sums['portion'],window=20)
    market_capitalization_sums.dropna(inplace=True)
    portions = list(market_capitalization_sums['rolling'].values)
    return portions

if __name__ == '__main__':
    K=80
    for days in range(5,9):
        print("{}일 {}개의 center를 이용한 test결과는".format(days,K))
        print(stats.mstats.normaltest(do_anova_test(days, K)))
        plt.hist(do_anova_test(days, K),bins=30)
        plt.show()
        #fig=plt.figure()
        #ax=fig.add_subplot(111)
        #stats.probplot(do_anova_test(days, K),plot=ax)
        #plt.show()




