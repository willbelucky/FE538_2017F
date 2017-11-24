# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 21.
"""
import matplotlib.pyplot as plt

from statistics.statistic_calculator import get_stats_results


def show_plot(window_from, window_to, k_from, k_to):
    """
    Show the change of trends.
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

    plt.show()
