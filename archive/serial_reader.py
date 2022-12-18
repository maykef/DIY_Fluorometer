from time import sleep
import serial
import os.path

file_exists = os.path.isfile('CO2_data.csv')

ser = serial.Serial("/dev/ttyACM1", 9600)

while True:
    try:
        sleep(2)
        getVal = ser.readline()
        getVal = getVal.rstrip()
        getVal = getVal.decode()
        print(getVal)
    except:
        print("Keyboard Interrupt")
        break

