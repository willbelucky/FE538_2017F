# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 21.
"""
import matplotlib.pyplot as plt

from statistics.statistic_calculator import get_stats_results
from clustering.k_means import get_highest_volatility_group
from data.data_reader import get_market_capitalization_sum


def show_window_k_scatter(window_from, window_to, k_from, k_to):
    """
    Show the intervals by a scatter plot.
    """
    # Get the confidential interval by window and the number of group.
    stats_results = get_stats_results(window_from, window_to, k_from, k_to)

    # Grab some test data.
    x = stats_results['k']
    y = stats_results['window']
    z = stats_results['interval']

    # Plot a basic wireframe.
    scatter = plt.scatter(x, y, c=z)
    plt.colorbar(scatter)
    plt.xlabel('k')
    plt.ylabel('window')
    plt.show()


def show_market_capitalization_line_graph(window, k):
    """
    Show the simple plot
    """
    highest_volatility_group = get_highest_volatility_group(window, k)
    highest_volatility_market_capitalization_sum = get_market_capitalization_sum(highest_volatility_group)

    highest_volatility_market_capitalization_sum['portion'].plot()
    plt.ylim([0, 1])
    plt.title('portion')
    plt.show()

    highest_volatility_market_capitalization_sum['selected_sum'].plot()
    plt.ylim([0, highest_volatility_market_capitalization_sum['selected_sum'].max() * 2])
    plt.title('market capitalization')
    plt.show()


def show_highest_volatility_market_capitalization_portion_graph(window, k):
    """
    Show the portion of market capitalization of a highest volatility group.
    """
    highest_volatility_group = get_highest_volatility_group(window, k)
    highest_volatility_market_capitalization_sum = get_market_capitalization_sum(highest_volatility_group)

    df_x = highest_volatility_market_capitalization_sum.index
    df_y = highest_volatility_market_capitalization_sum['portion']
    plt.ylim([0, 1])
    plt.fill_between(df_x, 0, df_y, facecolor='red', interpolate=True, alpha=0.3)
    plt.fill_between(df_x, df_y, 1, facecolor='blue', interpolate=True, alpha=0.1)
    plt.xlabel("Datetime")
    plt.ylabel("Ratio against the market cap")
    plt.plot(df_x, df_y, color='black', lw=1)
    plt.grid(True)
    plt.show()
