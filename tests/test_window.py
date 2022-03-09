"""
file: test_window.py

This file tests the apply_window function of ftools
"""
from ftools.asd2 import apply_window
from ftools import asd
import numpy as np
import matplotlib.pyplot as plt


def main():
    # Set time series parameters
    sample_rate = 128
    start_time = 0
    end_time = 7

    # Get raw time series and asd
    raw_ts = sample(start_time, end_time, sample_rate)
    freq, raw_asd = asd(raw_ts, sample_rate)

    # Get local times
    N = len(raw_ts)
    t = np.linspace(0, N/sample_rate, num=N)

    # Get windowed time series and asd
    windowed_ts = apply_window(raw_ts, window_name="hanning")
    freq, windowed_asd = asd(windowed_ts, sample_rate)

    # Plot
    plot(t, freq, raw_ts, raw_asd, windowed_ts, windowed_asd)


def plot(t, freq, raw_ts, raw_asd, windowed_ts, windowed_asd):

    # Set up subplots
    figure, axis = plt.subplots(2, 2)
    figure.set_figheight(10)
    figure.set_figwidth(16)
    figure.suptitle("Demonstration of apply_window function")

    # Get y min and max
    y_min = min(raw_asd)*1/2
    y_max = max(raw_asd)*2

    # Plot original function
    axis[0, 0].set_title("Non-windowed Time Series")
    axis[0, 0].set_ylabel("Motion [m]")
    axis[0, 0].set_xlabel("Time [s]")
    axis[0, 0].plot(t, raw_ts)

    # Plot de-trended function
    axis[1, 0].set_title("Windowed Time Series")
    axis[1, 0].set_ylabel("Motion [m]")
    axis[1, 0].set_xlabel("Time [s]")
    axis[1, 0].plot(t, windowed_ts)

    # Plot asd of original function
    axis[0, 1].set_title("Non-windowed asd")
    axis[0, 1].set_ylabel("Motion [m]")
    axis[0, 1].set_xlabel("Frequency [Hz]")
    axis[0, 1].plot(freq, raw_asd)
    axis[0, 1].loglog()
    axis[0, 1].set_ylim([y_min, y_max])

    # Plot de-trended function
    axis[1, 1].set_title("Windowed ASD")
    axis[1, 1].set_ylabel("Motion [m]")
    axis[0, 1].set_xlabel("Frequency [Hz]")
    axis[1, 1].plot(freq, windowed_asd)
    axis[1, 1].loglog()
    axis[1, 1].set_ylim([y_min, y_max])

    plt.savefig("image.png")


def sample(start, end, sample_rate):

    # Get range of time
    t = np.linspace(start, end, num=(end-start)*sample_rate)

    # Return function evaluated at point
    return signal_generator(t)


def signal_generator(t):
    return cos_wave(t)


def cos_wave(t):
    # Set frequency and amplitude
    freq = 0.65
    amplitude = 1

    # Return sin wave
    return amplitude*np.cos(2*np.pi*freq*t)


if __name__ == "__main__":
    main()
