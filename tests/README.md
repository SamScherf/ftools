# Daniell

The first step in calculating daniell's periodogram is to detrend the data because we are only interested in the periodic signals meaning polynomials will only cause leakage. We do this using the apply_detrend function which removes a polynomial of a given order from the time series. An example of this with a polynomial of degree 2 is:

![test_detrend](https://github.com/SamScherf/ftools/blob/main/tests/results/detrend.png)

Next we apply a window to the entire time series because the FFT algorithm requires that the time series is infinite. To accomplish this, the FFT algorithm repeats the given time series forwards and backwards which will cause lots of problems if the end points don't match. To accomplish this, we simply squish the function at the ends (and stretch at the middle to preserve power) like so:

![test_window](https://github.com/SamScherf/ftools/blob/main/tests/results/window.png)

Finally we take an ASD of the entire detrended-windowed time series using the included ASD function which uses an FFT and perverse power:

![test_asd](https://github.com/SamScherf/ftools/blob/main/tests/results/asd.png)

Simply calling daniell will execute all of the above results which accomplishes the following:

![test_daniell](https://github.com/SamScherf/ftools/blob/main/tests/results/daniell.png)
