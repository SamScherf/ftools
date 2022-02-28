"""
file: test_window.py

This file tests the apply_window function of ftools
"""
from ftools.asd2 import apply_window
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
    windowed = apply_window(raw_time_series, window_name="hanning")

    # Plot
    plot(t, raw_time_series, windowed)


def plot(t, raw_time_series, windowed):

    # Set up subplots
    figure, axis = plt.subplots(2, 1)
    figure.set_figheight(10)
    figure.set_figwidth(8)
    figure.suptitle("Demonstration of apply_window function")

    # Plot original function
    axis[0].set_title("Non-windowed Data")
    axis[0].set_ylabel("Motion [m]")
    axis[0].set_xlabel("Time [s]")
    axis[0].plot(t, raw_time_series, label="Raw Time Series")
    axis[0].legend()

    # Plot de-trended function
    axis[1].set_title("Windowed Data")
    axis[1].set_ylabel("Motion [m]")
    axis[1].set_xlabel("Time [s]")
    axis[1].plot(t, windowed, label="Detrended function")
    axis[1].legend()

    plt.savefig("image.png")


def sample(start, end, sample_rate):

    # Get range of time
    t = np.linspace(start, end, num=(end-start)*sample_rate)

    # Return function evaluated at point
    return signal_generator(t)


def signal_generator(t):
    return sin_wave(t)


def sin_wave(t):
    # Set frequency and amplitude
    freq = 0.1
    amplitude = 4

    # Return sin wave
    return amplitude*np.sin(2*np.pi*freq*t)


if __name__ == "__main__":
    main()
