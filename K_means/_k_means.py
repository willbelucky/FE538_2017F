## Initialization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



k = 5
# centroids[i] = [x, y]
def initialize_centroids(k):
    centroids = {
        i + 1: np.random.randint(100, 20000)
        for i in range(k)
        }
    return centroids
## Assignment Stage

def assignment(df, centroids,days):
    for i in centroids.keys():
        # sqrt((x1 - x2)^2 - (y1 - y2)^2)
        df['distance_from_{}'.format(i)] = (
            np.sqrt(
                (df['highest_volatility_{}'.format(days)] - centroids[i]) ** 2
            )
        )
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
    df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
    return df


## Update Stage

import copy

def update(df,centroids):
    for i in centroids.keys():
        if i in np.array(df['closest']):
            centroids[i] = np.mean(df[df['closest'] == i]['distance_from_{}'.format(i)])
        else:
            continue
    return centroids
def k_means_clustering(df,k,days):
    centroids = initialize_centroids(k)
    df = assignment(df, centroids,days)
    centroids=update(df,centroids)
    return centroids

