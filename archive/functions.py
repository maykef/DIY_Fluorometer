from time import sleep
import serial
import cv2



def flash():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    sleep(3)
    ser.write(b'1')
    print('Initial flash of 1000 umoles started')
    sleep(5)
    ser.write(b'd')
    print("Light On")
    while True:
        ser.write(b'1')
        sleep(10)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            ser.write(b'@')
            ser.close()
            break



flash()