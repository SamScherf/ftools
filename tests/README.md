# Daniell

The first step in calculating daniell's periodogram is to detrend the data because we are only interested in the periodic signals meaning polynomials will only cause leakage. We do this using the apply_detrend function which does the following:
