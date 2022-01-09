# ppcd-pec4

Package to charge and join into a `pandas.DataFrame` diverse `csv` files with music data (artists, albums, tracks, popularity and audio features) and perform basic visual and statisticall analysis.

Package can be downloaded from this [Github repository](https://github.com/uabalabadubdub/ppcd-pec4).

## Data origin & format
Data intended to be used with this package can be download from [audio features](https://developer.spotify.com/documentation/web-api/reference/#/).  


Formats accepted are comma separated value files (.csv) or a zip compressed folder with comma separated value files inside.  


Comma separated value files have to be inside a folder named `data` under script execution path and have the following names:

    * albums_norm.csv
    * artists_norm.csv
    * tracks_norm.csv


Zip compressed file has to have the following name:
    
    * data.zip  


On charge of module `data_input`, this module will automatically create a `data` and `imanges` folder under main script execution path, and look for any file in main execution script path named `data.zip` and move it to `data` path.


### Format: field names
*tracks_norm.csv*


- artist_id: artist identifier
- album_id: album identifier
- track_id: track identifier
- track_sp_id: spotify track identifier
- name: track name
- number: track order inside album
- disc_number: number of album (in case of double album)
- popularity: popularity metric
- preview_url: URL to prelisten an extract of the song
- duration_ms: track duration in ms
- audio features for track: danceability, energy, key, loudness, mode, speechiness, acousticness,
- instrumentalness, liveness, valence, tempo, time_signature


*albums_norm.csv*


- artist_id: artist identifier
- album_id: album identifier
- album_sp_id: spotify album identifier
- name: album name
- popularity: popularity metric
- release_year: year of release
- total_tracks: number of tracks in album  

*artists_norm.csv*  


- artist_id: artist identifier
- artist_sp_id: spotify artist identifier
- name: artist name
- popularity: popularity metric
- followers: number of followers in Spotify
- total_albums: number of albums

## Modules
This package includes the following modules:
- **data_input** : module with functions to charge the data
- **data_wrangling** : module with functions to perform basic analysis related to artists, albums, tracks, release year and popularity
- **audiofeature_analysis** : module with functions to perform visual and statistical analysis of audio features and comparaisons between artist throught features

## Intended use
On root directory, a `main.py` can be found. This package is intended to be used by having `data.zip` and `main.py` on same path. It can be executed from `terminal` using following command: `python main.py`


This script will authomatically create the needed folders to manage data input and output results, then charge data, perform basic analysis and, finally, perform audio feature analysis.


Visual analysis will be saved as images under `./images` folder. Statistical and basic analysis will be shown on terminal.


To be used, additional python modules have to be installed on your virtual environment (more detail on `requirements.txt`):
- numpy
- pandas
- matplotlib
- seaborn


## Test
`unittest` [library](https://docs.python.org/3/library/unittest.html#module-unittest) is used to perform unit testing. Repo `data` is used for unit testing. Test can be runned on local with the following command: `python -m unittest test/unit_test.py`


Code coverage performed using `coverage` [library](https://coverage.readthedocs.io/en/coverage-5.3/).


**Result**: (can be runned on local with the following command `coverage report -m`)
```
Name                                             Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------
audiofeature_analysis/__init__.py                    0      0   100%
audiofeature_analysis/audiofeature_analysis.py      80      2    98%   53, 162
data_input/__init__.py                              17      6    65%   8-9, 12-13, 18-19
data_input/data_input.py                            57      0   100%
data_wrangling/__init__.py                           0      0   100%
data_wrangling/data_wrangling.py                    31      0   100%
test/__init__.py                                     0      0   100%
test/unit_test.py                                   89      1    99%   186
------------------------------------------------------------------------------
TOTAL                                              274      9    97%
```

## License
This package follows **Creative Commons Zero v1.0 Universal** license.