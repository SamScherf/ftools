"""
file: asd.py

This file implements a function to get the
ASD of a given time series
"""
from scipy.fft import rfft, rfftfreq
import numpy as np


def asd(time_series, sample_rate):
    """ASD calculates the amplitude spectral density of a time series
    time_series    the time series,
    Ts             sampling time in seconds (time between consecutive samples)
    amp_spect_den  the amplitude spectral density of the signal, and
    freq           an optional output parameter, the corresponding freq vector

    WARNING: there is no windowing, you must do it yourself.
    see asd2.m for a more user-friendly function! (BTL Sept 2012)

    if time_series has units of xx, then amp_spect_den has units of xx-rms/rtHz
    (assuming that Ts is in seconds)

    it is computed according to the formula
    asd = sqrt(2) * 1/N * sqrt(sig_fft .* conj(sig_fft)) * 1/sqrt(BW)
    where
    sig_fft = fft(time_series),
    N is the number of points in the time series, and
    BW is the bandwidth of a freq bin (ie the bin width), BW = 1/(N*Ts);
    except for the first and last points,
    The ffts are double sided, and the ASD is single sided, hence the root 2.
    sig_fft is length N, and ASD in length N/2+1.
    The DC term and the Nyquist freq term do not have the sqrt(2)
    since they do not have a conjugate term in the two sided FFT

    BTL Oct 8, 2001

    PS - Remember, when averaging together several ASDs, you must use
        the rms average, not the linear average. Use the linear average
        for power spectra.

    """
    # Get number of points in time series
    N = len(time_series)

    # Get bin width
    BW = sample_rate/N

    # Get Fourier transform and frequency bins
    dft = rfft(time_series)
    freq = rfftfreq(N)*sample_rate

    # Convert fft to asd
    asd = np.sqrt(2)*1/N*np.abs(dft)*1/np.sqrt(BW)
    asd[0] *= 1/np.sqrt(2)

    # If n is even
    if N/2 % 2 == 0:
        asd[-1] *= 1/np.sqrt(2)

    return freq, asd
