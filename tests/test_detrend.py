"""
file_ test_detrend.py

This file tests the detrend function of ftools
"""
from ftools.asd2 import apply_detrend
import numpy as np
import matplotlib.pyplot as plt


def main():
    # Set time series parameters
    sample_rate = 64
    start_time = 0
    end_time = 60

    # Get time series
    raw_time_series = sample(start_time, end_time, sample_rate)

    # Get local times
    N = len(raw_time_series)
    t = np.linspace(0, N/sample_rate, num=N)

    # De-trend time series
    detrended = apply_detrend(raw_time_series, order=2)

    # Get original wave and trend
    orginal_wave = sin_wave(t)
    trend = get_trend(t)

    # Plot
    plot(t, raw_time_series, trend, orginal_wave, detrended)


def plot(t, raw_time_series, trend, orginal_wave, detrended):

    # Set up subplots
    figure, axis = plt.subplots(2, 1)
    figure.set_figheight(10)
    figure.set_figwidth(8)
    figure.suptitle("Demonstration of apply_detrend function")

    # Plot original function
    axis[0].set_title("Non-detrended Data")
    axis[0].set_ylabel("Motion [m]")
    axis[0].set_xlabel("Time [s]")
    axis[0].plot(t, raw_time_series, label="Raw Time Series")
    axis[0].plot(t, trend, label="Applied Trend")
    axis[0].legend()

    # Plot de-trended function
    axis[1].set_title("Detrended Data")
    axis[1].set_ylabel("Motion [m]")
    axis[1].set_xlabel("Time [s]")
    axis[1].plot(t, detrended, label="Detrended function")
    axis[1].plot(t, orginal_wave, label="Original Sin Wave")
    axis[1].legend()

    plt.savefig("image.png")


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
