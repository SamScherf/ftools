"""
file: asd2.py
"""
from ._utils import apply_detrend, apply_window, average_bins
from .asd import asd
import numpy as np

# Define windows dictionary
WINDOWS = dict()
WINDOWS['hanning'] = np.hanning


def daniell(ts, fs=1, bin_width=9, detrend=1,
            window='hanning'):
    """daniell calculates smoothed, windowed ASD of a time series

    Input:
    -------
    ts             the time series,
    fs             the sampling frequency (rate) in Hz (samples per second)
    bin_width      number of raw fft bins to average across
    detrend        order of polynomial to be removed from the data
    window         name of window to use (currently only hanning is supported)

    Output:
    -------
    asd            the amplitude spectral density of the signal
    freq           the corresponding freq list for the asd

    How it Works:
    -----------
    This function detrends the time series and applies a window
    so it can take an ASD of the entire time series. It splits
    the ASD up into adjacent bins which are rms averaged together

    Why do this?
    ------------
    We average across freq bins, rather than averaging sequential
    time series. This reduces the impact of the shenanigans which
    result from windows, drifts and offsets. This can be quite
    important if the spectra are not white.

    Recap:
    -------
    1) detrend the time series
    2) apply a single window to the whole time series,
    3) take the ASD of the detrended, windowed, data
    4) average the ASD by adjecent bins.
    """

    # 0) Check input
    check_input(ts, fs, bin_width, window)

    # 1) De-trend the time series
    ts = apply_detrend(ts, order=detrend)

    # 2) Window the time series
    ts = apply_window(ts, window_name=window)

    # 3) Take ASD
    freq, mag = asd(ts, fs=fs)

    # 4) Average over adjacent bins
    freq, mag = average_bins(freq, mag, bin_width)

    # Return frequency and magnitude of ASD
    return freq, mag


def check_input(ts, fs, bin_width, window):
    """This function check that the input values are valid
    """

    # Check if list empty
    if len(ts) == 0:
        raise Exception("Input ts is empty")

    # Check if sample_rate is empty
    if fs == "":
        raise Exception("Input fs is empty")

    # Check if smooth rate is less than 1
    if bin_width < 1:
        raise Exception("Input bin_width must be >= 1")

    # Check if window is supported
    if window not in WINDOWS.keys():
        raise Exception(f"The window '{window}' is not supported")
