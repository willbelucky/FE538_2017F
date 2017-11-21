from K_means._k_means import *
from data.test_data_reader import *
import pandas as pd


def get_highest_volatility_group(n, k):
    """
    n window로 volatility를 구해서, k_means 돌리고, 가장 높은 volatility group의 stock_master만을 return한다.

    :param n: (int) size of an window.
    :param k: (int) size of group of K_means
    :return highest_volatility_stock_masters: (DataFrame)
        index       code        | (string) 6 digit number string code of stock.
        columns     name        | (string) The name of company.
    """
    days=n
    means = k
    stock_masters = get_stock_master()
    highest_volatilities = get_highest_volatility(window=days, stock_masters=stock_masters)
    centroids = initialize_centroids(means)
    df = assignment(highest_volatilities, centroids, days)
    # reassign updated means
    centroids = update(df, centroids)
    df = assignment(df, centroids, days)
    highest_mean = max(centroids, key=centroids.get)
    final_df=stock_masters[stock_masters.index.isin(np.array(df[df['closest'] == highest_mean].index))]
    return final_df


