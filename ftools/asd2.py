"""
file: asd2.py
"""
import numpy as np

# Define windows dictionary
WINDOWS = dict()
WINDOWS['hanning'] = np.hanning


def asd2(time_series, sample_rate, smooth_width=9, detrend=1,
         window='hanning'):
    """ASD2 calculates SMOOTHED, WINDOWED ASD of a time series

    Input:
    -------
    time_series    the time series,
    sample_rate    the sampling rate in Hz (samples per second)
    smooth_width   number of raw fft bins to average across (e.g. 9) -
                   this is like the number of averages. MUST BE ODD!
    detrend        order of polynomial to be removed from the data,
                   (we use polyfit) 0 = DC, 1 = DC and best fit line,
                   2 = DC, line, and parabola, etc.  (1 is good)
    window         name of window to use (currently only hanning is supported)

    Output:
    -------
    amp_spect_den  the amplitude spectral density of the signal, and
    freq           an optional output parameter, the corresonding freq vector

    Notes:
    -------
    1. the final bin width will be
    BW = number of averages / length of time series in sec.
    e.g. a 1000 sec time series with 50 averages will return an
    asd with bin width (freq resolution) of 50/(1000 sec) = 50 mHz

    2. The averaging does funny stuff to the DC term - don't trust it.

    How it Works:
    -----------
    1. The function gets an ASD of the entire time series and
    then adjacent bins (smooth_width) are rms averaged together

    2. WINDOWS - the default window is the hanning window (@hann)
    and the default option we use for the hanning window is 'periodic'
    All windows are normalized so that the expected average power of a
    stationary signal will not change. i.e. NOT the Default matlab
    windows have a max amp of 1.
    The scaling is done per:
        normalized_window = sqrt(1/mean(raw_window.^2)) * raw_window;
        (so the mean of the normalized_window.^2 is 1)

    To use a DIFFERENT WINDOW, call with the window pointer to the window
    you want (e.g. the tukey window is called with @tukeywin)
    and add the options, as defined in >> help window,
    e.g.
        asd2(time_series, sample_rate,  9, 3, @tukeywin, 0.2)
        or
        asd2(time_series, sample_rate,  9, 3, @hann, 'symmetric')

    Why do this?
    ------------
    We average across freq bins, rather than averaging sequential
    time series. This reduces the impact of the shenanigans which
    result from windows, drifts and offsets. This can be quite
    important if the spectra are not white.


    Developer note:
    --------------
    Conor and BTL have adjusted the row/column direction of the outputs.
    If the input time series is a row, then freq and amp_spect_den are rows
    If the input is a column, then both outputs are columns.
    The old version had the freq vector as a row, requiring lots of freq.'
        in analysis. this should now be just freq.
        this is a pain, because all of your old code will break.
        To run old code, you can replace asd2 with asd2_pre20170929


    Recap:
    -------
    0) Check input
    1) detrend the time series
        by default we remove a 1st order poly, i.e. mean and slope,
        but the user can pick something else.
    2) apply a single window to the whole time series,
       periodic hann window by default (0 at one end, one point away from 0
       at the other), user can pick. The window is normalized so that the
       mean POWER (amplitude squared) of the window is 1.
    3) take the ASD of the detrended, windowed, data
    4) average the ASD by adjecent bins.
    """

    # 0) Clean input
    check_input(time_series, sample_rate, smooth_width, window)

    # 1) De-trend the time series
    time_series = apply_detrend(time_series, order=detrend)

    # 2) Window the time series
    # time_series = apply_window(time_series, window_name=window)

    return time_series


def apply_window(time_series, window_name='hanning'):
    """ This function applies a window to the time series
    """

    # Get window function
    window_function = WINDOWS[window_name](len(time_series))

    # Normalize window function
    window_function *= np.mean(window_function**2)**(-0.5)

    # Apply window function
    return time_series*window_function


def apply_detrend(time_series, order=1):
    """ This function de-trends a time series

    This function removes the poly_fit_term order polynomial
    for the time_series. I.e. if poly_fit_term = 1, it removes
    the mean and slope.
    """
    # Get 'x values' for poly fit
    x = np.arange(len(time_series))

    # Get coefficients for polynomial fit
    coefficients = np.polyfit(x, time_series, order)

    # Remove polynomial from time series
    return time_series - np.polyval(coefficients, x)


def check_input(time_series, sample_rate, smooth_width, window):
    """This function check that the input values are valid
    """

    # Check if list empty
    if len(time_series) == 0:
        raise Exception("Input time_series is empty")

    # Check if sample_rate is empty
    if sample_rate == "":
        raise Exception("Input sample_rate is empty")

    # Check if smooth rate is less than 1
    if smooth_width < 1:
        raise Exception("Input smooth_width must be >= 1")

    # Check if window is supported
    if window not in WINDOWS.keys():
        raise Exception(f"The window '{window}' is not supported")
