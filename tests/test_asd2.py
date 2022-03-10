"""
file: test_asd.py

This file tests the asd2 function of ftools
"""

from ftools import asd2
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

AMPLITUDE_1 = 2
AMPLITUDE_2 = 1
AMPLITUDE_3 = 0.5


def main():
    # Get time series
    sample_rate = 2048
    start_time = 0
    end_time = 95
    time_series = sample(start_time, end_time, sample_rate)

    # Get local times
    N = len(time_series)
    t = np.linspace(0, N/sample_rate, num=N)

    # Get asd
    freq, mag = asd2(time_series, sample_rate, smooth_width=9, detrend=0)

    # Check RMS
    check_RMS(freq, mag)

    # Plot ASD and Time Series
    plot(t, time_series, freq, mag)


def plot(t, time_series, freq, mag):
    # Set up subplots
    figure, axis = plt.subplots(2, 1)
    figure.set_figheight(10)
    figure.set_figwidth(8)
    figure.suptitle("Demonstration of asd2 function")

    # Plot original function
    axis[0].set_title("Time Series")
    axis[0].set_ylabel("Motion [m]")
    axis[0].set_xlabel("Time [s]")
    axis[0].plot(t, time_series)

    # Plot ASD
    axis[1].set_title("Amplitude Spectral Density")
    axis[1].set_ylabel("Displacement [m/sqrt(Hz)]")
    axis[1].set_xlabel("Frequency [Hz]")
    axis[1].semilogx()
    axis[1].plot(freq, np.abs(mag))

    plt.savefig("image.png")


def check_RMS(freq, mag):
    # Get observed and expected RMS
    observed_RMS = np.sqrt(integrate.trapezoid(mag**2, x=freq))
    expected_RMS = 0.707*np.sqrt(AMPLITUDE_1**2+AMPLITUDE_2**2+AMPLITUDE_3**2)

    # Display observed and expected RMS
    print(f"The expected RMS is {expected_RMS}")
    print(f"The RMS from numerical integration is {observed_RMS}")


def sample(start, end, sample_rate):

    # Get range of time
    t = np.linspace(start, end, num=(end-start)*sample_rate)

    # Return function evaluated at point
    return signal_generator(t)


def signal_generator(t):
    # Set frequency and get period of sin function
    freq_1 = 2
    period_1 = freq_1*2*np.pi

    freq_2 = 0.1
    period_2 = freq_2*2*np.pi

    freq_3 = 50
    period_3 = freq_3*2*np.pi

    # Lets just say units of m
    signal = AMPLITUDE_1*np.sin(period_1*t)
    signal += AMPLITUDE_2*np.sin(period_2*t)
    signal += AMPLITUDE_3*np.sin(period_3*t)
    signal += trend(t)

    return signal


def trend(t):
    return 0.00005*(t-100)**2


if __name__ == "__main__":
    main()
