import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# A parser is required to translate the timestamp
def custom_date_parser(a):
    return datetime.strptime(a, '%d-%m-%Y %H:%M_%S.%f')


df = pd.read_csv(
    '18-12-2022_05_00.csv',
    parse_dates=['Timestamp'],
    date_parser=custom_date_parser)
x = df['Timestamp']
y = df['Mean_values']

fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))

# As per accepted answer here:
# https://stackoverflow.com/questions/1713335/peak-finding-algorithm-for-python-scipy
peaks, _ = find_peaks(y, prominence=6)

ax1.plot(x[peaks], y[peaks], "ob")
ax1.plot(x, y)
ax1.grid()
ax1.legend(['Fm'])

# Invert the data to find the lowest points of peaks as per answer here:
# https://stackoverflow.com/questions/61365881/is-there-an-opposite-version-of-scipy-find-peaks
valleys, _ = find_peaks(-y, prominence=1)

# valley in the short time period before a peak
# set time window, e.g., for 200 ms
time_window_size = pd.Timedelta(4000, unit="ms")
time_of_peaks = x[peaks]
peak_start = x.searchsorted(time_of_peaks - time_window_size)
# in case of evenly spaced data points, this can be simplified,
# and you just add n data points to your peak index array
# peak_start = peaks - n
true_valleys = peaks.copy()
for i, (start, stop) in enumerate(zip(peak_start, peaks)):
    true_valleys[i] = start + y[start:stop].argmin()

# Find the first peak and valley to calculate NPQ
first_peak = y[peaks[0]]
first_valley = y[true_valleys[0]]

# Find the latest peak and valley to calculate PSII
last_peak = y[peaks[-1]]
last_valley = y[true_valleys[-1]]

# Assign numbers to each peak and valley value using enumerate
for index, val in enumerate(y[peaks], start=1):
    print(index, val)

# Assign numbers to each valley value using enumerate
for index, val in enumerate(y[true_valleys], start=1):
    print(index, val)

# PSII Formula Fq'/Fm' (as per nomenclature of Murchie & Lawson 2013)
PSII = (last_peak - last_valley) / last_peak

# NPQ Formula (Fm - Fm')/Fm' as per Murchie & Lawson 2013
NPQ = (first_peak - last_peak) / last_peak

print(first_peak)
print(first_valley)
print(last_peak)
print(last_valley)
print('The PSII is:', PSII)
print('The NPQ is:', NPQ)
pd.DataFrame({'True Valleys': y[true_valleys], 'Peaks': y[peaks]})\
    .to_csv('18-12-2022_05_00_peaks_valleys.csv', index=False)
ax2.plot(x[true_valleys], y[true_valleys], "sr")
ax2.plot(x, y)
ax2.legend(['F′'])
ax2.grid()
plt.show()
