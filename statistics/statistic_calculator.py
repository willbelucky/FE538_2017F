# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 21.
"""
import traceback

import pandas as pd
import scipy.stats as stats
from sqlalchemy.exc import SQLAlchemyError

from clustering.k_means import get_highest_volatility_group
from data.data_reader import get_market_capitalization_sum
from utils.db import get_connection


def do_stats(window, k, confidence=0.95):
    """
    t-distribution을 사용하여 평균과 신뢰구간을 구한다.

    :param window: (int) the size of an window.
    :param k: (int) the size of group of clustering.
    :param confidence: (float, default=0.95) the confidence level.

    :return ci_low: (float) the low bound of the confidence interval.
    :return mean: (float) mean of portions.
    :return ci_high: (float) the high bound of the confidence interval.
    :return interval: (float) the length from ci_high to ci_low.
    """
    schema_name = 'highvol_stats'
    select_sql = "SELECT * FROM {} WHERE `window` = {} AND `k`= {}".format(schema_name, window, k)
    stats_result = pd.DataFrame()
    connection = get_connection()

    try:
        # If the table does not exist, create the table.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS `{}` (
                `window` INT NOT NULL,
                `k` INT NOT NULL,
                `ci_low` DOUBLE NOT NULL,
                `mean` DOUBLE NOT NULL,
                `ci_high` DOUBLE NOT NULL,
                `interval` DOUBLE NOT NULL,
                PRIMARY KEY (`window`, `k`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """.format(schema_name))

        # get all stock codes from the db.
        stats_result = pd.read_sql(select_sql, connection)

        if stats_result.empty:
            stats_result = pd.DataFrame(columns=['window', 'k', 'ci_low', 'mean', 'ci_high', 'interval'])
            # 높은 변동성 그룹을 가져온다.
            high_volatility_stock_masters = get_highest_volatility_group(window, k)
            # 그 그룹들로 시총의 비율을 뽑는다.
            market_capitalization_sums = get_market_capitalization_sum(high_volatility_stock_masters)
            portions = market_capitalization_sums['portion'].values

            # 통계를 돌린다.
            mean, sigma = portions.mean(), portions.std()
            ci_low, ci_high = stats.norm.interval(confidence, loc=mean, scale=sigma)
            interval = ci_high - ci_low

            stats_result.loc[0] = [window, k, ci_low, mean, ci_high, interval]

            connection.execute("""
                INSERT IGNORE INTO `{}` (`window`, `k`, `ci_low`, `mean`, `ci_high`, `interval`)
                VALUES ({}, {}, {}, {}, {}, {})
            """.format(schema_name, window, k, ci_low, mean, ci_high, interval))

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    assert len(stats_result) == 1

    _, _, ci_low, mean, ci_high, interval = stats_result.loc[0]
    return ci_low, mean, ci_high, interval


def get_stats_results(window_from, window_to, k_from, k_to):
    """

    :param window_from:
    :param window_to:
    :param k_from:
    :param k_to:
    :return stats_results: (DataFrame)
        columns     window      | (int) The size of an window.
                    k           | (int) The size of group of clustering.
                    ci_low      | (float) The low bound of the confidence interval.
                    mean        | (float) the mean of portions.
                    ci_high     | (float) The high bound of the confidence interval.
                    interval    | (float) The length from ci_high to ci_low.
    """
    schema_name = 'highvol_stats'
    select_sql = "SELECT * FROM {} WHERE `window` BETWEEN {} AND {} AND `k` BETWEEN {} AND {}".format(schema_name,
                                                                                                      window_from,
                                                                                                      window_to, k_from,
                                                                                                      k_to)
    stats_result = pd.DataFrame()
    connection = get_connection()

    try:
        # If the table does not exist, create the table.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS `{}` (
                `window` INT NOT NULL,
                `k` INT NOT NULL,
                `ci_low` DOUBLE NOT NULL,
                `mean` DOUBLE NOT NULL,
                `ci_high` DOUBLE NOT NULL,
                `interval` DOUBLE NOT NULL,
                PRIMARY KEY (`window`, `k`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """.format(schema_name))

        # get all stock codes from the db.
        stats_result = pd.read_sql(select_sql, connection)

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    assert len(stats_result) == (window_to - window_from + 1) * (k_to - k_from + 1)

    return stats_result
