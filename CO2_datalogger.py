import serial
import csv
from datetime import datetime
import time
import os
import glob

# Start the Clock
start = time.time()

# Establish the period of time to run
Time_Period = 86300 # 23.9 hours

ser = serial.Serial("/dev/ttyACM1", 9600)
ser.flushInput()

filename = datetime.now().strftime("CO2_data_%d-%m-%Y_%H_%M.csv")

def new_folder():
    """Creates a new folder each time the script runs"""
    imagepath = os.path.join('/media/nvidia/External_SSD_1TB/Fluorometer')
    if os.path.exists(imagepath):
        datetime.now().strftime('%Y-%m-%d')
        now = datetime.now()
        newdirname = now.strftime('%Y-%m-%d')
        os.mkdir(os.path.join(imagepath, newdirname))
        print('Creating ' + newdirname + ' folder')


def create_file():
    for dir in glob.glob('/media/nvidia/External_SSD_1TB/Fluorometer'):
        if os.path.isdir(dir):
            latest_folder = os.path.getctime(dir)
            folder_time = datetime.fromtimestamp(latest_folder).strftime('%Y-%m-%d')
            newdir = os.path.join(folder_time)
            file = os.path.join('/media/nvidia/External_SSD_1TB/Fluorometer', newdir, filename)
            with open(file, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'CO2_Value'])



def get_data():
    getVal = ser.readline()
    getVal = getVal.rstrip()
    getVal = getVal.decode()
    print(getVal)
    with open(filename, "a") as f:
        now = datetime.now()
        writer = csv.writer(f, delimiter=",")
        writer.writerow([now, getVal])


if __name__ == "__main__":
    new_folder()
    create_file()
    final_path = os.path.join('/media/nvidia/External_SSD_1TB/Fluorometer')
    if os.path.exists(final_path):
        latest_folder = os.path.getctime(final_path)
        folder_time = datetime.fromtimestamp(latest_folder).strftime('%Y-%m-%d')
        newdir = os.path.join(folder_time)
        os.chdir(os.path.join(final_path, newdir))
        while True:
            get_data()
            if time.time() > start + Time_Period:
                quit()
