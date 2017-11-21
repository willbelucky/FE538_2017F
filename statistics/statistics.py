# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 21.
"""


def do_anova_test(n, k):
    """
    ANOVA 테스트를 수행하여 (n, k)로 구한 p_1 = p_2 = ... = p_{740-n}을 검증한다.
    검증 결과 같지 않은 portion이 있다면 False를 return하고 모두 같다면 True를 리턴한다.

    :param n: (int) size of an window.
    :param k: (int) size of group of K_means

    :return test_result: (Boolean) ANOVA 테스트의 결과.
        p_1 = p_2 = ... = p_{740-n}이면 True, 아니면 False
    """
    test_result = False
    return test_result
