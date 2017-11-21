## Initialization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt





k = 5
# centroids[i] = [x, y]
def initialize_centroids(k):
    centroids = {
        i + 1: [np.random.randint(0, 80), np.random.randint(0, 80)]
        for i in range(k)
        }
    return centroids
## Assignment Stage

def assignment(df, centroids):
    for i in centroids.keys():
        # sqrt((x1 - x2)^2 - (y1 - y2)^2)
        df['distance_from_{}'.format(i)] = (
            np.sqrt(
                (df['x'] - centroids[i][0]) ** 2
                + (df['y'] - centroids[i][1]) ** 2
            )
        )
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
    df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
    return df


## Update Stage

import copy

def update(centroids):
    old_centroids = copy.deepcopy(centroids)
    new_centroids= copy.deepcopy(centroids)
    for i in centroids.keys():
        centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
        centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
    for i in old_centroids.keys():
        old_x = old_centroids[i][0]
        old_y = old_centroids[i][1]
        new_centroids[i][0] = (centroids[i][0] - old_centroids[i][0]) * 0.75
        new_centroids[i][1] = (centroids[i][1] - old_centroids[i][1]) * 0.75
    return new_centroids
def k_means_clustering(df,k):
    centroids = initialize_centroids(k)
    df = assignment(df, centroids)
    centroids=update(centroids)
    return centroids

