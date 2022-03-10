# Daniell

The first step in calculating daniell's periodogram is to detrend the data because we are only interested in the periodic signals meaning polynomials will only cause leakage. We do this using the apply_detrend function which removes a polynomial of a given order from the time series. An example of this with a polynomial of degree 2 is:

![test_detrend](https://github.com/SamScherf/ftools/blob/main/tests/results/detrend.png)
