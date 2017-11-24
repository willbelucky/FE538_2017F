from clustering._k_means import *
from data.test_data_reader import *


def get_highest_volatility_group(window, k):
    """
    n window로 volatility를 구해서, k_means 돌리고, 가장 높은 volatility group의 stock_master만을 return한다.

    :param window: (int) size of an window.
    :param k: (int) size of group of clustering
    :return highest_volatility_stock_masters: (DataFrame)
        index       code        | (string) 6 digit number string code of stock.
        columns     name        | (string) The name of company.
    """
    stock_masters = get_stock_master()
    highest_volatilities = get_highest_volatility(window=window, stock_masters=stock_masters)
    centroids = initialize_centroids(k)
    df = assignment(highest_volatilities, centroids, window)
    # reassign updated means
    centroids = update(df, centroids)
    df = assignment(df, centroids, window)
    highest_mean = max(centroids, key=centroids.get)
    highest_volatility_stock_masters \
        = stock_masters[stock_masters.index.isin(np.array(df[df['closest'] == highest_mean].index))]
    return highest_volatility_stock_masters
