import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import sys

custom_date_parser = lambda x: datetime.strptime(x, "%d-%m-%Y %H:%M_%S.%f")


df = pd.read_csv('results.csv',  parse_dates=['Timestamp'], date_parser=custom_date_parser)
df2 = df[0:0]

plt.ion()
fig, ax = plt.subplots()
i=0
while i < len(df):
    df2 = df2.append(df[i:i+1])
    ax.clear()
    df2.plot(x="Timestamp", y="Mean_values", ax=ax)
    plt.draw()
    plt.pause(0.001)
    i+=1
plt.show()