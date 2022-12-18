import serial
import time

# Start the Clock
start = time.time()

# Establish the period of time to run
Time_Period = 50400 # 14 hours

# Define the serial port to communicate with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

def light_on():
    ser.write(b'd')
    return

def light_off():
    ser.write(b'@')
    quit()
    return

if __name__ == "__main__":
    while True:
        light_on()
        if time.time() > start + Time_Period:
            light_off()
