import unittest
import data_input.data_input as dns
import data_wrangling.data_wrangling as dw
import audiofeature_analysis.audiofeature_analysis as fa
from matplotlib.figure import Figure
import numpy as np


class TestDataInput(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Creating paths")
        cls._zipped_path = "data/data.zip"
        cls._artists_norm = "data/artists_norm.csv"

    def test_data_denormalizer(self):
        print("Starting test_data_denormalizer")
        self.assertEqual(dns.data_denormalizer(
            self._zipped_path).shape, (35574, 30))

    def test_get_column_pandas(self):
        print("Starting test_data_denormalizer")
        self.assertEqual(
            len(
                dns.get_column_pandas(
                    self._artists_norm, ";", "artist_id")),
            68)

    def test_get_column_iostream(self):
        print("Starting test_data_denormalizer")
        self.assertEqual(
            len(dns.get_column_iostream(
                self._artists_norm, ";", "artist_id")),
            68)
    
    def test_time_it(self):
        print("Starting test_time_it")
        self.assertIsInstance(dns.time_it(), Figure)


class TestDataWrangling(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Creating paths")
        cls._zipped_path = "data/data.zip"
        print("Loading dataframe")
        cls._df = dns.data_denormalizer(cls._zipped_path)

    def test_count_tracks_by_artist(self):
        print("Starting test_count_tracks_by_artist")
        self.assertEqual(
            dw.count_tracks_by_artist(self._df, "Radiohead"),
            159)
        self.assertNotEqual(
            dw.count_tracks_by_artist(self._df, "Radiohead"),
            20)

    def test_count_tracks_containing(self):
        print("Starting count_tracks_containing")
        self.assertEqual(
            dw.count_tracks_containing(self._df, "police"),
            11)
        self.assertNotEqual(
            dw.count_tracks_containing(self._df, "police"),
            5)

    def test_count_tracks_in_album_from(self):
        print("Starting test_count_tracks_in_album_from")
        self.assertEqual(
            dw.count_tracks_in_album_from(self._df, 1990),
            4638)
        self.assertNotEqual(
            dw.count_tracks_in_album_from(self._df, 1990),
            90)

    def test_most_popular_track_last_n_years(self):
        print("Starting test_most_popular_track_last_n_years")
        self.assertEqual(
            dw.most_popular_track_last_n_years(self._df, 10),
            ["Beggin'"])
        self.assertNotEqual(
            dw.most_popular_track_last_n_years(self._df, 10),
            ["Paquito el Chocolatero"])

    def test_most_prolifict_artists_since(self):
        print("Starting test_most_prolifict_artists_since")
        self.assertEqual(
            dw.most_prolifict_artists_since(self._df, 1960),
            ['Louis Armstrong', 'Frank Sinatra'])
        self.assertNotEqual(
            dw.most_prolifict_artists_since(self._df, 1960),
            ['Juan Valdez'])


class TestAudiofeatureAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Creating paths")
        cls._zipped_path = "data/data.zip"
        print("Loading dataframe")
        cls._df = dns.data_denormalizer(cls._zipped_path)
        print("Creating vectors")
        cls._v1 = np.array((1, 1, 1))
        cls._v2 = np.array((0, 2, 1))

    def test_feature_basic_statistics(self):
        print("Starting test_feature_basic_statistics")
        self.assertEqual(
            fa.feature_basic_statistics(
                self._df, "energy", artist_filter="Metallica"),
            (0.0533, 0.998, 0.8462655384615385))
        self.assertNotEqual(
            fa.feature_basic_statistics(
                self._df, "energy", artist_filter="Metallica"),
            (1.0, 1.0, 1.0))

    def test_feature_mean_by_album_for_group(self):
        print("Starting test_feature_mean_by_album_for_group")
        self.assertIsInstance(
            fa.feature_mean_by_album_for_group(
                self._df, "danceability", "Coldplay"),
            Figure)

    def test_feature_prob_dens_histogram(self):
        print("Starting test_feature_prob_dens_histogram")
        self.assertIsInstance(
            fa.feature_prob_dens_histogram(
                self._df, "acousticness", "Ed Sheeran"),
            Figure)

    def test_feature_hist_comparaison(self):
        print("Starting test_feature_hist_comparaison")
        self.assertIsInstance(
            fa.feature_hist_comparaison(
                self._df, "energy", "Adele", "Extremoduro"),
            Figure)

    def test_euclidian_similarity(self):
        print("Starting test_euclidian_similarity")
        self.assertEqual(
            fa.euclidian_similarity(self._v1, self._v1),
            1.0)
        self.assertEqual(
            fa.euclidian_similarity(self._v1, self._v2),
            0.4142135623730951)

    def test_cosine_similarity(self):
        print("Starting test_cosine_similarity")
        self.assertEqual(
            fa.cosine_similarity(self._v1, self._v1),
            1.0000000000000002)
        self.assertEqual(
            fa.cosine_similarity(self._v1, self._v2),
            0.7745966692414834)

    def test_artist_similarity_comparaison(self):
        print("Starting test_feature_hist_comparaison")
        self.assertIsInstance(
            fa.artist_similarity_comparaison(
                self._df,
                ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                 'time_signature']),
            Figure)
        self.assertIsInstance(
            fa.artist_similarity_comparaison(
                self._df,
                ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                 'time_signature'],
                similarity='cosine'),
            Figure)
        self.assertIsNone(
            fa.artist_similarity_comparaison(
                self._df,
                ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                 'time_signature'],
                similarity='pepino'))


if __name__ == '__main__':
    unittest.main()
