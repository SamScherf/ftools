from ftools import asd, asd2
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate


def main():
    check_asd2()


def check_asd2():
    # Get time series
    sample_rate = 64
    start_time = 0
    end_time = 60
    time_series = sample(start_time, end_time, sample_rate)

    t, detrended = asd2(time_series, sample_rate, poly_fit_terms=2)

    # Plot ASD
    plt.plot(t, detrended)
    plt.ylabel("Displacement [m/sqrt(Hz)]")
    plt.xlabel("Frequency [Hz]")
    plt.title("ASD")
    plt.savefig("image.png")


def check_asd():
    # Get time series
    sample_rate = 64
    start_time = 0
    end_time = 60
    time_series = sample(start_time, end_time, sample_rate)

    # Get asd
    freq, mag = asd(time_series, sample_rate)

    # Get RMS
    RMS = np.sqrt(integrate.trapezoid(mag**2, x=freq))
    print(RMS)

    # Plot ASD
    plt.plot(freq, np.abs(mag))
    plt.ylabel("Displacement [m/sqrt(Hz)]")
    plt.xlabel("Frequency [Hz]")
    plt.title("ASD")
    plt.savefig("image.png")


def sample(start, end, sample_rate):

    # Get range of time
    t = np.linspace(start, end, num=(end-start)*sample_rate)

    # Return function evaluated at point
    return signal_generator(t)


def signal_generator(t):
    # Set frequency and get period of sin function
    freq = 0.1
    period = freq*2*np.pi

    # Get trend
    trend = 0.005*t**2

    return 4*np.sin(period*t) + trend


def two_waves(t):
    # Set frequency and get period of sin function
    freq_1 = 2
    period_1 = freq_1*2*np.pi

    freq_2 = 4
    period_2 = freq_2*2*np.pi

    # Lets just say units of m
    return 2*np.sin(period_1*t)+np.sin(period_2*t)


if __name__ == "__main__":
    main()
