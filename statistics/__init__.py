# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 23.
"""
from statistics.statistic_calculator import do_stats

if __name__ == '__main__':
    for window in range(5, 61):
        for k in range(5, 201):
            ci_low, mean, ci_high, interval = do_stats(window, k)
            print("{:6d}\t{:6d}\t{:6f}\t{:6f}\t{:6f}\t{:6f}".format(window, k, ci_low, mean, ci_high, interval))
