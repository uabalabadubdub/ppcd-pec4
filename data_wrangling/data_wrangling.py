import pandas as pd
import datetime as dt
import data_input.data_input as dsn


def count_tracks_by_artist(df, artist):
    mask = df["name_artist"] == artist
    return df.loc[mask, "track_id"].count()


def count_tracks_containing(df, pattern):
    mask = df["name_track"].str.contains(pattern, False)
    return df.loc[mask, "track_id"].count()


def count_tracks_in_album_from(df, decade_year):
    years = [decade_year + y for y in range(10)]
    mask = df["release_year"].isin(years)
    return df.loc[mask, "track_id"].count()


def most_popular_track_last_n_years(df, years):
    current_year = dt.datetime.now().year
    lookup_years = [current_year - y for y in range(years)]
    mask = df["release_year"].isin(lookup_years)
    tracks = df.loc[mask, ["name_track", "name_artist", "popularity_track"]]
    most_popular_mask = tracks["popularity_track"] == tracks["popularity_track"].max()
    most_popular_track = tracks.loc[most_popular_mask, [
        "name_track", "name_artist"]]
    return most_popular_track


def most_prolifict_artists_since(df, year_decade_lookup):
    current_year = dt.datetime.now().year
    n_years = current_year - year_decade_lookup
    n_decades = n_years // 10
    lookup_decades = [year_decade_lookup +
                      d for d in range(0, n_decades * 10 + 1, 10)]
    artists = set(df["name_artist"])
    for id in range(n_decades):
        mask = (df["release_year"] <= lookup_decades[id]) & (
            df["release_year"] < lookup_decades[id + 1])
        filtered_df = df.loc[mask, "name_artist"]
        artists = [artist for artist in artists if artist in set(filtered_df)]

    return artists
