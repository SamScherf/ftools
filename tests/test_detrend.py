"""
file: test_detrend.py

This file tests the apply_detrend function of ftools
"""

from ftools._utils import apply_detrend
from ftools.asd import asd
import numpy as np
import matplotlib.pyplot as plt


def main():
    # Set time series parameters
    sample_rate = 128
    start_time = 0
    end_time = 60

    # Get time series
    raw_ts = sample(start_time, end_time, sample_rate)

    # Get local times
    N = len(raw_ts)
    t = np.linspace(0, N/sample_rate, num=N)

    # De-trend time series
    detrended_ts = apply_detrend(raw_ts, order=2)

    # Get original wave and trend
    orginal_wave = sin_wave(t)
    trend = get_trend(t)

    # Plot
    plot(t, raw_ts, detrended_ts, trend, orginal_wave, sample_rate)


def plot(t, raw_ts, detrended_ts, trend, orginal_wave, fs):

    # Set up subplots
    figure, axis = plt.subplots(2, 2)
    figure.set_figheight(10)
    figure.set_figwidth(16)
    figure.suptitle("Demonstration of apply_detrend function")

    # Plot original function
    axis[0, 0].set_title("Non-detrended Time Series")
    axis[0, 0].set_ylabel("Motion [m]")
    axis[0, 0].set_xlabel("Time [s]")
    axis[0, 0].plot(t, raw_ts, label="Raw Time Series")
    axis[0, 0].plot(t, trend, label="Applied Trend")
    axis[0, 0].legend()

    # Plot de-trended function
    axis[1, 0].set_title("Detrended Time Series")
    axis[1, 0].set_ylabel("Motion [m]")
    axis[1, 0].set_xlabel("Time [s]")
    axis[1, 0].plot(t, detrended_ts, label="Detrended function")
    axis[1, 0].plot(t, orginal_wave, label="Original Sin Wave")
    axis[1, 0].legend()

    # Plot original asd
    freq, mag = asd(raw_ts, fs=fs)

    # Get y min and max
    y_min = min(mag)*1/2
    y_max = max(mag)*2

    axis[0, 1].set_title("Non-detrended ASD")
    axis[0, 1].set_ylabel("Displacement [m/sqrt(Hz)]")
    axis[0, 1].set_ylim([y_min, y_max])
    axis[0, 1].set_xlabel("Frequency [Hz]")
    axis[0, 1].loglog()
    axis[0, 1].plot(freq, mag)

    # Plot de-trended asd
    freq, mag = asd(detrended_ts, fs=fs)

    axis[1, 1].set_title("Detrended ASD")
    axis[1, 1].set_ylabel("Displacement [m/sqrt(Hz)]")
    axis[1, 1].set_ylim([y_min, y_max])
    axis[1, 1].set_xlabel("Frequency [Hz]")
    axis[1, 1].loglog()
    axis[1, 1].plot(freq, mag)

    plt.savefig("detrend.png")


def sample(start, end, sample_rate):

    # Get range of time
    t = np.linspace(start, end, num=(end-start)*sample_rate)

    # Return function evaluated at point
    return signal_generator(t)


def signal_generator(t):
    # Combine trend and sin wave
    return sin_wave(t) + get_trend(t)


def sin_wave(t):
    # Set frequency and amplitude
    freq = 0.1
    amplitude = 4

    # Return sin wave
    return amplitude*np.sin(2*np.pi*freq*t)


def get_trend(t):
    return 0.005*t**2


if __name__ == "__main__":
    main()
