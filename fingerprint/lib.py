from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import maximum_filter, gaussian_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion
from fingerprint.Fingerprint import Fingerprint
from fingerprint.fingerprint_config import DEFAULT_SAMPLING_RATE, DEFAULT_PEAK_COUNT, TIME_GAP, TIME_LIMIT


def generate_fingerprints(sound, sampling_rate, origin: str, new_sampling_rate=DEFAULT_SAMPLING_RATE, plot=False,
                          n=DEFAULT_PEAK_COUNT):
    sound = _down_sampling(sound, sampling_rate, new_sampling_rate)

    f, t, Sxx = signal.spectrogram(sound, new_sampling_rate)
    if plot:
        _plot(Sxx)

    filtered_Sxx = gaussian_filter(Sxx, sigma=3.5)

    peaks_mask = _detect_peaks(filtered_Sxx)
    masked_filtered_Sxx = filtered_Sxx * peaks_mask

    if plot:
        _plot(filtered_Sxx)
        _plot(masked_filtered_Sxx)

    peaks = _mask_to_peaks(Sxx, peaks_mask, n)

    if plot:
        _plot(Sxx, peaks)

    fingerprints = _peaks_to_fingerprints(peaks, origin)

    return fingerprints


def _peaks_to_fingerprints(peaks, origin):
    fingerprints = []
    # naive search, but size is small
    for i in np.arange(len(peaks)):
        for j in np.arange(len(peaks)):
            time_1 = peaks[i][1]
            time_2 = peaks[j][1]
            freq_1 = peaks[i][0]
            freq_2 = peaks[j][0]

            if peaks[i] != peaks[j] and time_1 + TIME_GAP < time_2 < time_1 + TIME_LIMIT:
                fingerprints.append(Fingerprint(time_1, time_2, freq_1, freq_2, origin))

    return fingerprints


def _mask_to_peaks(Sxx, peaks_mask, n):
    peaks = []
    peaks_data = np.where(peaks_mask)
    for t, f in zip(peaks_data[0], peaks_data[1]):
        peaks.append((Sxx[t][f], t, f))

    # Find n most intense points
    peaks.sort(key=lambda tup: tup[0], reverse=True)
    peaks = peaks[:n]

    # Sort by time
    peaks = [x[1:] for x in peaks]
    peaks.sort(key=lambda tup: tup[0])

    return peaks


def _plot(Sxx, peaks=None):
    plt.pcolormesh(Sxx)
    plt.ylabel('F [Hz]')
    plt.xlabel('T [sec]')

    if peaks:
        for t, f in peaks:
            plt.plot(f, t, "gx")

    plt.show()


def _down_sampling(sound, sampling_rate, new_sampling_rate):
    ratio = new_sampling_rate / sampling_rate
    return signal.resample(sound, int(len(sound) * ratio))


def _detect_peaks(spectrogram):
    neighborhood = generate_binary_structure(2, 2)

    local_max = maximum_filter(spectrogram, footprint=neighborhood) == spectrogram

    background = (spectrogram < 2000000)

    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    detected_peaks = ~(local_max ^ eroded_background)

    return detected_peaks
