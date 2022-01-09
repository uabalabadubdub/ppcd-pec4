"""Data wrangling

This module allows the user to make a genearak analyse of the audio
features data set charged using module `data_input`.

This module accepts `pandas` dataframes. Is itended to be used on
dataframe charged using `data_input.data_denormalizer`.

This script requires that `pandas`be installed within the Python
environment you are running this script in.

This file is intended to be imported as a module and contains the 
following functions:

    * count_tracks_by_artist - returns count of tracks given
        dataframe and artist name; dataframe has to have
        `name_artist` and `track_id` columns
    * count_tracks_containing - returns count of tracks containing
        given pattern on their name and dataframe to work on;
        dataframe has to have `name_track` and `track_id` columns
    * count_tracks_in_album_from - returns count of tracks on
        albums published over given decade and dataframe;
        dataframe has to have `release_year` and `track_id` columns
    * most_popular_track_last_n_years - returns most popular track
        of the given n last years and dataframe; dataframe has to
        have `release_year`, `name_track`, `name_artist` and
        `popularity_track` columns
    * most_prolifict_artists_since - returns artists with at least
        one track per decade from given decade to date and dataframe;
        dataframe has to have `release_year` and `name_artist`
        columns
"""

import pandas as pd
import datetime as dt


def count_tracks_by_artist(df, artist):
    """returns count of tracks given dataframe and artist name;
    dataframe has to have `name_artist` and `track_id` columns"""
    mask = df["name_artist"] == artist
    return df.loc[mask, "track_id"].count()


def count_tracks_containing(df, pattern):
    """returns count of tracks containing given pattern on their
    name and dataframe to work on; dataframe has to have `name_track`
    and `track_id` columns."""
    mask = df["name_track"].str.contains(pattern, False)
    return df.loc[mask, "track_id"].count()


def count_tracks_in_album_from(df, decade_year):
    """returns count of tracks on albums published over given
    decade and dataframe; dataframe has to have `release_year`
    and `track_id` columns."""
    years = [decade_year + y for y in range(10)]
    mask = df["release_year"].isin(years)
    return df.loc[mask, "track_id"].count()


def most_popular_track_last_n_years(df, years):
    """returns most popular track of the given n last years
    and dataframe; dataframe has to have `release_year`,
    `name_track`, `name_artist` and `popularity_track` columns."""
    current_year = dt.datetime.now().year
    lookup_years = [current_year - y for y in range(years)]
    mask = df["release_year"].isin(lookup_years)
    tracks = (
        df.loc[mask,
        ["name_track", "name_artist", "popularity_track"]]
        .sort_values("name_track"))
    most_popular_mask = (
        tracks["popularity_track"]
        == tracks["popularity_track"].max())
    most_popular_track = tracks.loc[most_popular_mask, "name_track"]
    return most_popular_track.tolist()


def most_prolifict_artists_since(df, year_decade_lookup):
    """returns artists with at least one track per decade from given
    decade to date and dataframe; dataframe has to have
    `release_year` and `name_artist` columns."""
    current_year = dt.datetime.now().year
    n_years = current_year - year_decade_lookup
    n_decades = n_years // 10
    lookup_decades = [year_decade_lookup +
                      d for d in range(0, n_decades * 10 + 1, 10)]
    artists = set(df["name_artist"].sort_values())
    for id in range(n_decades):
        mask = (df["release_year"] <= lookup_decades[id]) & (
            df["release_year"] < lookup_decades[id + 1])
        filtered_df = df.loc[mask, "name_artist"]
        artists = [artist for artist in artists if artist in set(filtered_df)]

    return artists
