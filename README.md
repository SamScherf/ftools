# fTools

fTools is a collection of lesser known tools used to analyze signals in the frequency domain. Some of these tools already exist in Matlab so this module is meant to be a python port. Currently the only tool is daniell's periodogram and the supporting tools needed for daniell's periodogram however more tools such as mccs2 are planned in the future.

## How to Use

To install simply, clone the repository and install is with your preferred package manager. If using pip for example:

```bash
git clone https://github.com/SamScherf/ftools.git
pip install ftools/
```

With this you'll have access to daniell like so:

```python
from ftools import daniell

ts = get_time_series(time_range)

freq, asd = daniell(ts, fs=fs, window='hanning', bin_width=9, detrend=1)
```

Where the function arguments represent the following:

### ts

Time series of measurement values for which ASD should be calculated from.

### fs

The sampling frequency/rate in Hz (samples per second)

### bin_width

The number of FFT bins to average across

### detrend

The order of polynomial to be removed from the data

### window

The name of window to use (currently only hanning is supported)


and the function returns:

### freq

The freq array of the ASD

### asd

The amplitude spectral density of the signal

## How it works

### daniell

daniell detrends the time series and applies a window so it can take an
ASD of the entire time series. It splits then the ASD up into adjacent bins
which are rms averaged together

For further explanation, see [tests](https://github.com/SamScherf/ftools/tree/main/tests)
