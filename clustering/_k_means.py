import numpy as np
import time


def initialize_centroids(k):
    """
    Initialization
    """
    np.random.seed(seed=int(time.time()))
    centroids = {
        i + 1: np.random.rand()
        for i in range(k)
    }
    return centroids


def assignment(df, centroids, days):
    """
    Assignment Stage
    """
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


def update(df, centroids):
    """
    Update Stage
    """
    for i in centroids.keys():
        if i in np.array(df['closest']):
            centroids[i] = np.mean(df[df['closest'] == i]['distance_from_{}'.format(i)])
        else:
            continue
    return centroids


def k_means_clustering(df, k, days):
    centroids = initialize_centroids(k)
    df = assignment(df, centroids, days)
    updated_centroids = update(df, centroids)
    while centroids != updated_centroids:
        centroids = updated_centroids
        df = assignment(df, centroids, days)
        updated_centroids = update(df, centroids)
    return updated_centroids
