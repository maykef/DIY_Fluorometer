import time
import serial

# Start the Clock
start = time.time()

# Establish the period of time to run
Time_Period = 50400 # 14 hours

# Define the serial port to communicate with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

def flash_pulse():
    while True:
        ser.write(b'1')
        print('Flash!')
        time.sleep(1800)
        return

if __name__ == "__main__":
    while True:
        flash_pulse()
        if time.time() > start + Time_Period:
            print('Time up!')
            quit()



