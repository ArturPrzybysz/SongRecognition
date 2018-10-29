import numpy as np
from scipy.io.wavfile import read


def music_to_array(file_path: str):
    sampling_rate, sound = read(file_path)
    single_channel = _combine_channels(sound)

    return single_channel, sampling_rate


def _combine_channels(sound):
    dimensions = len(sound.shape)
    if dimensions == 1:
        return sound
    else:
        return np.sum(sound, axis=1)
