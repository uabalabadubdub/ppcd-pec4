import pandas as pd
import zipfile as zf
import numpy as np
import time
import matplotlib.pyplot as plt


def data_denormalizer(data_folder):
    with zf.ZipFile(data_folder, 'r') as zip_f:
        zip_f.extractall("data")

    albums_norm_df = pd.read_csv("data/albums_norm.csv", sep=";")
    artists_norm_df = pd.read_csv("data/artists_norm.csv", sep=";")
    tracks_norm_df = pd.read_csv("data/tracks_norm.csv", sep=";")

    artists_norm_df["name"] = artists_norm_df["name"].str.title()

    null_count = tracks_norm_df["popularity"].isna().sum()
    avg_popularity = tracks_norm_df["popularity"].mean()
    tracks_norm_df["popularity"].replace(np.nan, avg_popularity, inplace=True)

    denorm_tracks = tracks_norm_df.merge(
        artists_norm_df[["artist_id", "name",
                         "popularity", "followers", "total_albums"]],
        on='artist_id',
        suffixes=("_track", "_artist"))
    denorm_tracks = denorm_tracks.merge(
        albums_norm_df[["album_id", "name", "popularity",
                        "release_year", "total_tracks"]],
        on='album_id',
        suffixes=("_track", "_album"))

    denorm_tracks.rename(
        {"name": "name_album", "popularity": "popularity_album"}, axis=1, inplace=True)

    print(f"nº of tracks: {denorm_tracks.shape[0]}")
    print(f"nº of columns: {denorm_tracks.shape[1]}")
    print(f"nº of tracks lacking popularity value: {null_count}")
    return denorm_tracks


def get_column_pandas(path, separator, column_name):
    "implementará la lectura mediante pandas."
    column = pd.read_csv(path, sep=separator, usecols=[column_name])
    return column.values.tolist()


def get_column_iostream(path, separator, column_name):
    """implementará la lectura mediante el método escogido
por vosotros. Debéis sustituir {your_method} con un nombre que identifique de
alguna manera el algoritmo escogido."""
    with open(path, "r") as f:
        header = f.readline().split(sep=separator)
        col_num = header.index(column_name)
        column = []
        for line in f.readlines():
            column.append(line.split(separator)[col_num])

    return column


def time_it():
    paths = ["data/artists_norm.csv",
             "data/albums_norm.csv", "data/tracks_norm.csv"]
    columns = ["artist_id", "album_id", "track_id"]
    pd_rows, io_rows = [], []
    pd_times, io_times = [], []
    for path, column in zip(paths, columns):
        start = time.time()
        column_result = get_column_pandas(path, ";", column)
        end = time.time()
        pd_rows.append(len(column_result)), pd_times.append(end - start)
        start = time.time()
        column_result = get_column_iostream(path, ";", column)
        end = time.time()
        io_rows.append(len(column_result)), io_times.append(end - start)

    fig, ax = plt.subplots()
    ax.plot(pd_rows, pd_times)
    ax.plot(io_rows, io_times)
    ax.set_xlabel('nr of rows')
    ax.set_ylabel('t (s)')
    ax.set_title("Method comparaison")
    ax.legend(["pandas", "iostream"])
    fig.savefig('images/column_input_methods_comparative.png')
    plt.show(block=True)
