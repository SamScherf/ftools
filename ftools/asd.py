"""
file: asd.py

This file implements a function to get the
ASD of a given time series
"""
from scipy.fft import rfft, rfftfreq
import numpy as np


def asd(time_series, sample_rate):
    """ASD calculates the amplitude spectral density of a time series

    This function takes in a time_series and sample_rate:
        time_series: an array of real numbers in time domain
        sample_rate: number of samples per second

    This function returns freq and asd:
        freq: an array of frequencies in Hz
        asd: an asd in units of x/sqrt(Hz) (x is unit of time_series)
    """
    # Get number of points in time series (units of samples)
    N = len(time_series)

    # Get bin width (units of Hz)
    BW = sample_rate/N

    # Get Fourier transform and frequency bins
    dft = rfft(time_series)
    freq = rfftfreq(N, d=1./sample_rate)

    # Convert fft to asd
    asd = np.abs(dft)/N*1/np.sqrt(BW)

    # ffts are double sided and ASDs are single sided so
    # we have to add account for an extra factor of sqrt(2)
    asd *= np.sqrt(2)

    # The DC term and the Nyquist freq term do not have the sqrt(2)
    # since they do not have a conjugate term in the two sided FFT
    asd[0] *= 1/np.sqrt(2)
    if N/2 % 2 == 0:  # if n is even
        asd[-1] *= 1/np.sqrt(2)

    return freq, asd
