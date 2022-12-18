import numpy as np
import cv2
import sys
import csv
import time
import serial

cap = cv2.VideoCapture(0 + cv2.CAP_V4L)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# CU51 has the following possible resolution settings
# 640 x 480
# 1280 x 720
# 1920 x 1080
# 2592 x 1944

rows = 640
cols = 480

# Set parameters for the camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cols)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, rows)
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)  # turn off RGB conversion
cap.set(cv2.CAP_PROP_BRIGHTNESS, 5)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*'Y16 '))

ser.write(b'1')
_, frame = cap.read()
# CU51 camera
# convert from 12 bit (4096 levels) to 8 bit (256 levels) 255/4096 = 0.06226
bf81 = np.array(frame // 16, dtype=np.uint8)
# Create the mask
_, binary = cv2.threshold(bf81, 210, 255, cv2.THRESH_BINARY)
im3 = cv2.bitwise_and(bf81, binary)
im3[binary == 0] = 0
cv2.imwrite('Masked_Image.png', binary)
print("Mask Saved")
time.sleep(3)
ser.write(b'@')

cap.release()
cv2.destroyAllWindows()
