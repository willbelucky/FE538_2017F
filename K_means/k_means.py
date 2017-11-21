from K_means._k_means import *


def get_highest_volatility_group(n, k):
    """
    n window로 volatility를 구해서, k_means 돌리고, 가장 높은 volatility group의 stock_master만을 return한다.

    :param n: (int) size of an window.
    :param k: (int) size of group of K_means
    :return highest_volatility_stock_masters: (DataFrame)
        index       code        | (string) 6 digit number string code of stock.
        columns     name        | (string) The name of company.
    """
    pass
