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

ser = serial.Serial("/dev/ttyACM2", 115200)
ser.flushInput()

filename = datetime.now().strftime("Hum_Temp_Data_%d-%m-%Y.csv")

def create_file():
    for dir in glob.glob('/media/nvidia/External_SSD_1TB/Fluorometer'):
        if os.path.isdir(dir):
            latest_folder = os.path.getctime(dir)
            folder_time = datetime.fromtimestamp(latest_folder).strftime('%Y-%m-%d')
            newdir = os.path.join(folder_time)
            file = os.path.join('/media/nvidia/External_SSD_1TB/Fluorometer', newdir, filename)
            with open(file, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Humidity', 'Temperature'])

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
