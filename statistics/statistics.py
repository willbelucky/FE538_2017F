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
    market_capitalization_sums = get_market_capitalization_sum(high_volatility_stock_masters)
    portions = list(market_capitalization_sums['portion'].values)

    test_result = stats.f_oneway(*portions)
    return test_result


if __name__ == '__main__':
    print(do_anova_test(5, 80))
# 높은 변동성 그룹을 가져온다.



# 그 그룹들로 비율을 뽑는다.

# 비율로 아노바 테스트를 돌린다.

# 아노바 테스트 결과를 리턴한다.

#




