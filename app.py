from os import path
from fingerprint import lib
from fingerprint.query_by_fingerprint import query_by_fingerprint
from util.sound_utils import music_to_array
import config
import pickle
from os import listdir
from os.path import isfile, join

# init library
song_dir = path.join(config.ROOT_DIR, "sounds")
song_paths = [path.join(song_dir, f) for f in listdir(song_dir) if isfile(join(song_dir, f))]

FROM_SAVED = False

if FROM_SAVED:
    pickle_off = open("song_library.p", "rb")
    library = pickle.load(pickle_off)
else:
    library = []
    for song_path in song_paths:
        signal, sample_rate = music_to_array(song_path)
        fingerprints = lib.generate_fingerprints(signal, sample_rate, n=100, origin=song_path, plot=True)

        for fingerprint in fingerprints:
            library.append(fingerprint)

    pickle.dump(library, open("song_library.p", "wb"))

# create query fingerprint
query_song_path = path.join(config.ROOT_DIR, "query_sounds", "jack.min.wav")

signal, sample_rate = music_to_array(query_song_path)
query_fingerprints = lib.generate_fingerprints(signal, sample_rate, n=20, origin=query_song_path)

# find_matching_song
matching_song_origin = query_by_fingerprint(library, query_fingerprints)

print(matching_song_origin)


