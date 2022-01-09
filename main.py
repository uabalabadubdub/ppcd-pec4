import data_input.data_input as dsn
import data_wrangling.data_wrangling as dw
import audiofeature_analysis.audiofeature_analysis as fa


path = "data/data.zip"
print(f"Charging data from {path}...")
df = dsn.data_denormalizer(path)

print("Comparing alternative methods for data input...")
dsn.time_it()
print("Results on images/")

print("\nBasic data analysis:")
# ¿Cuántas tracks hay del artista Radiohead?
radiohead_tracks = dw.count_tracks_by_artist(df, "Radiohead")
print(f"How many tracks has Radiohead: {radiohead_tracks}")
# ¿Cuántas tracks contienen la palabra ‘police’ en el título?
police_tracks = dw.count_tracks_containing(df, "police")
print(f"How many tracks have police in his name: {police_tracks}")
# ¿Cuántas tracks son de álbumes publicados en la década del 1990?
nineties_album_tracks = dw.count_tracks_in_album_from(df, 1990)
print(
    f"""How many tracks were published in the
 nineties: {nineties_album_tracks}""")
# ¿Cuál es la track con más popularidad de los últimos 10 años?
last10years_most_pop_tracks = dw.most_popular_track_last_n_years(df, 10)
print(
    f"""What's the most popular track of the last
 10 years (song, artist): {last10years_most_pop_tracks.values}""")
# ¿Qué artistas tienen tracks en cada una de las décadas desde el 1960?
most_prolifict_artist_since1960 = dw.most_prolifict_artists_since(df, 1960)
print(
    f"""Which artists have at least one track for
 each decade since 1960: {most_prolifict_artist_since1960}""")

print("\nAudio feature analysis:")
metallica_basic_stats = fa.feature_basic_statistics(
    df, "energy", artist_filter="Metallica")
print(
    f"""Metallica tracks energy feature min, max and average:
 {metallica_basic_stats}""")
print("Average danceability for Coldplay albums...")
fa.feature_mean_by_album_for_group(df, "danceability", "Coldplay")
print("Results on images/")
print("Acousticness distribution of probability for Ed Sheeran tracks...")
fa.feature_prob_dens_histogram(df, "acousticness", "Ed Sheeran")
print("Results on images/")
print("""Energy distribution of probability comparaison between Adele and
 Extremoduro tracks...""")
fa.feature_hist_comparaison(df, "energy", "Adele", "Extremoduro")
print("Results on images/")
print("General artists euclidian similarity comparaison...")
fa.artist_similarity_comparaison(
       df,
       ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
       'time_signature'])
print("General artists cosine similarity comparaison...")
fa.artist_similarity_comparaison(
       df,
       ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
       'time_signature'],
       similarity='cosine')
print("Results on images/")
