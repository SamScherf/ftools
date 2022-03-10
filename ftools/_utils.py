"""
file: _utils.py

This file implements the various functions needed for ftools
"""
import numpy as np

# Define windows dictionary
WINDOWS = dict()
WINDOWS['hanning'] = np.hanning


def average_bins(freq, mag, bin_width):
    """ This function averages over adjacent frequency bins

    The ASD is broke into bins of width 'smooth_width'
    and then averaged together
    """

    # Get number of current points and new points
    N = len(freq)
    new_N = int(np.floor(N/bin_width))

    # Initialize new frequency domain and new mag
    new_freq = np.zeros(new_N)
    new_mag = np.zeros(new_N)

    # Populate new frequencies and magnitudes
    for i in range(new_N):

        # Get freq/mag bin
        freq_bin = freq[i*bin_width:(i+1)*bin_width]
        mag_bin = mag[i*bin_width:(i+1)*bin_width]

        # Set new freq to linear average and set new mag to RMS average
        new_freq[i] = np.mean(freq_bin)
        new_mag[i] = np.sqrt(np.mean(mag_bin**2))

    # Return new frequency and magnitude
    return new_freq, new_mag


def apply_window(ts, window_name='hanning'):
    """ This function applies a window to the time series
    """

    # Get window function
    window_function = WINDOWS[window_name](len(ts))

    # Normalize window function
    window_function *= np.mean(window_function**2)**(-0.5)

    # Apply window function
    return ts*window_function


def apply_detrend(ts, order=1):
    """ This function de-trends a time series

    This function removes the poly_fit_term order polynomial
    for the time_series. I.e. if poly_fit_term = 1, it removes
    the mean and slope.
    """
    # Get 'x values' for poly fit
    x = np.arange(len(ts))

    # Get coefficients for polynomial fit
    coefficients = np.polyfit(x, ts, order)

    # Remove polynomial from time series
    return ts - np.polyval(coefficients, x)
