import data_input.data_input as dsn
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from functools import reduce
import numpy as np
import seaborn as sns


def feature_basic_statistics(df, feature, artist_filter=None):
    if artist_filter:
        mask = df["name_artist"] == artist_filter
    else:
        mask = [True] * df.shape[0]

    min = df.loc[mask, feature].min()
    max = df.loc[mask, feature].max()
    avg = df.loc[mask, feature].mean()
    return (min, max, avg)


def feature_mean_by_album_for_group(df, feature, artist):
    mask_artist = df["name_artist"] == artist
    avg_by_album = df.loc[mask_artist, [
        "name_album", feature]].groupby("name_album").mean()
    fig, ax = plt.subplots()
    ax.bar(avg_by_album.index, reduce(
        lambda x, y: x + y, avg_by_album.values.tolist()))
    ax.set_xlabel('albums')
    ax.set_ylabel(f'avg {feature}')
    ax.set_title(f"Avg {feature} by album for {artist}")
    plt.xticks(rotation=90)
    plt.tight_layout()
    fig.savefig(f"images/avg_{feature}_by_album_for_{artist}.png")
    plt.show(block=True)


def feature_prob_dens_histogram(df, feature, artist, fig=None, save=True):
    mask_artist = df["name_artist"] == artist
    data = df.loc[mask_artist, feature]

    if not fig:
        fig, ax = plt.subplots()
        ax.hist(data, density=True, color='b', label=artist, alpha=0.5)
        ax.set_xlabel(f'{feature}')
        ax.set_ylabel(f'probability')
        ax.set_title(f"Histogram of {feature} for {artist}")
        ax.legend()
        if save:
            fig.savefig(f"images/hist_{feature}_{artist}.png")
    else:
        ax = fig.get_axes()[0]
        ax.hist(data, density=True, color='g', alpha=0.4, label=artist)
        ax.legend()
        if save:
            fig.savefig(f"images/hist_{feature}_comparison.png")
    return fig


def feature_hist_comparaison(df, feature, artist_1, artist_2):
    fig = feature_prob_dens_histogram(df, feature, artist_1, save=False)
    feature_prob_dens_histogram(df, feature, artist_2, fig)


def euclidian_similarity(vector1, vector2):
    dist = np.linalg.norm(vector1 - vector2)
    similarity = 1 / (1 + dist)
    return similarity


def cosine_similarity(vector1, vector2):
    similarity = np.sum(np.multiply(vector1, vector2)) / \
        (np.sqrt(np.sum(vector1**2)) * np.sqrt(np.sum(vector2**2)))
    return similarity


def artist_similarity_comparaison(df, feature_list, artist_list=None, similarity='euclidian'):
    """
    similarity: euclidian or cosine
    """
    if artist_list:
        mask_artists = df["name_artist"].isin(artist_list)
    else:
        mask_artists = [True] * df.shape[0]
    
    data = df.loc[mask_artists, ["name_artist"] + feature_list]
    feature_means_by_artist = data.groupby("name_artist").mean()
    comparaisons = {}
    for artist in feature_means_by_artist.index:
        comparaisons[artist] = []
        v1 = feature_means_by_artist.loc[artist, :]
        for artist2 in feature_means_by_artist.index:
            v2 = feature_means_by_artist.loc[artist2, :]
            if similarity == 'euclidian':
                comparaisons[artist].append(euclidian_similarity(v1, v2))
            else:
                comparaisons[artist].append(cosine_similarity(v1, v2))
    
    heat_map_data = pd.DataFrame(comparaisons, index=feature_means_by_artist.index)
    fig, ax = plt.subplots(figsize=(16, 16))
    ax = sns.heatmap(heat_map_data, ax=ax)
    ax.set_title(f"Artists {similarity} similarity heatmap")
    fig.savefig("images/artists_similarity_heatmap.png")
    return fig
