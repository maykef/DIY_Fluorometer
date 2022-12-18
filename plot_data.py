import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


# A parser is required to translate the timestamp
def custom_date_parser(x):
    return datetime.strptime(x, '%d-%m-%Y %H:%M_%S.%f')
# custom_date_parser = lambda x: pd.to_datetime(x).strftime("%d-%m-%Y_%H:%M_%S.%f")


df1 = pd.read_csv('Basil_Trial/23-06-22/23-06-2022_05_00.csv',
                  parse_dates=['Timestamp'], date_parser=custom_date_parser)
# x3 = df7['Timestamp']
y1 = df1['Mean_values']

df2 = pd.read_csv('Basil_Trial/24-06-22/24-06-2022_05_00.csv',
                  parse_dates=['Timestamp'], date_parser=custom_date_parser)
# x2 = df6['Timestamp']
y2 = df2['Mean_values']

df3 = pd.read_csv('Basil_Trial/25-06-22/25-06-2022_05_00.csv',
                  parse_dates=['Timestamp'], date_parser=custom_date_parser)
# x2 = df7['Timestamp']
y3 = df3['Mean_values']

df4 = pd.read_csv('Basil_Trial/26-06-22/26-06-2022_05_00.csv',
                  parse_dates=['Timestamp'], date_parser=custom_date_parser)
# x2 = df7['Timestamp']
y4 = df4['Mean_values']

df5 = pd.read_csv('Basil_Trial/27-06-22/27-06-2022_05_00.csv',
                  parse_dates=['Timestamp'], date_parser=custom_date_parser)
# x2 = df7['Timestamp']
y5 = df5['Mean_values']

df6 = pd.read_csv('Basil_Trial/28-06-22/28-06-2022_05_00.csv',
                  parse_dates=['Timestamp'], date_parser=custom_date_parser)
# x2 = df7['Timestamp']
y6 = df6['Mean_values']

df7 = pd.read_csv('Basil_Trial/29-06-22/29-06-2022_05_00.csv',
                  parse_dates=['Timestamp'], date_parser=custom_date_parser)
# x2 = df7['Timestamp']
y7 = df7['Mean_values']

df8 = pd.read_csv('Basil_Trial/01-07-22/01-07-2022_05_00.csv',
                  parse_dates=['Timestamp'], date_parser=custom_date_parser)
# x2 = df7['Timestamp']
y8 = df8['Mean_values']

df9 = pd.read_csv('Basil_Trial/02-07-22/02-07-2022_05_00.csv',
                  parse_dates=['Timestamp'], date_parser=custom_date_parser)
# x2 = df7['Timestamp']
y9 = df9['Mean_values']

plt.plot(y1, 'g', linewidth=9, label='23 Jun')
plt.plot(y2, 'r', linewidth=8, label='24 Jun')
plt.plot(y3, 'b', linewidth=7, label='25 Jun')
plt.plot(y4, 'y', linewidth=6, label='26 Jun')
plt.plot(y5, 'm', linewidth=5, label='27 Jun')
plt.plot(y6, 'c', linewidth=4, label='28 Jun')
plt.plot(y7, 'c', linewidth=3, label='29 Jun')
plt.plot(y8, 'w', linewidth=2, label='01 Jul')
plt.plot(y9, 'k', linewidth=1, label='02 Jul')
plt.grid()
plt.legend()
plt.show()

