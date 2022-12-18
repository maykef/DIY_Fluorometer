import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib import animation

custom_date_parser = lambda x: datetime.strptime(x, "%d-%m-%Y %H:%M_%S.%f")


df = pd.read_csv('18-01-2022_19_52.csv',  parse_dates=['Timestamp'], date_parser=custom_date_parser)
x = df['Timestamp']
y = df['Mean_values']

fig, ax = plt.subplots()
line, = ax.plot([], [], 'k-')
ax.margins(0.005)

def init():
    line.set_data(x[:2],y[:2])
    return line,

def animate(i):
    i = min(i, x.size)
    xdata = x[:i]
    ydata = y[:i]
    line.set_data(xdata, ydata)
    ax.relim()
    ax.autoscale()
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50)

plt.show()
