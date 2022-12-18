#!/usr/bin/python3

import numpy as np
import cv2
import sys
import csv
from datetime import datetime


cap = cv2.VideoCapture(0 + cv2.CAP_V4L)

i=0

#file_exists = os.path.isfile('results.csv')

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
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0) # turn off RGB conversion
cap.set(cv2.CAP_PROP_BRIGHTNESS, 8)
cap.set(cv2.CAP_PROP_EXPOSURE, 0) #Not Supported
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*'Y16 '))

filename = datetime.now().strftime("/media/nvidia/External_SSD_1TB/Fluorometer/%d-%m-%Y_%H_%M.csv")

with open(filename, 'a') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Mean_values'])

# Create the mask
# Gray out both binaries and enable _, binary in order to create the mask.
# after the mask has been obtained, gray out _, binary and enable both binary to
# retrieve the mask.
#binary = cv2.imread('Masked_Image.png')
#binary = binary[:,:,1]
print('Width = ', cap.get(3),' Height = ', cap.get(4),' fps = ', cap.get(5))


# Save the orint text to the original standard output
original_stdout = sys.stdout


while True:
    _, frame = cap.read()
    bf8 = np.array(frame//16, dtype = np.uint8)
    #binary = cv2.imread('Masked_Image.png', 0)
    _, binary = cv2.threshold(bf8, 30, 255, cv2.THRESH_BINARY)
    im3 = cv2.bitwise_and(bf8,binary)
    im3[binary==0] = 0
    # Normalize the image
    bf8_2_color = cv2.applyColorMap(im3, cv2.COLORMAP_PARULA)
    # Display the image, print image size and fps and save each frame
    #cv2.imshow('Masked_Image', im3)
    cv2.imshow("Opencv Video See3Cam_CU51 Color", bf8_2_color)
    Mean = cv2.mean(im3, bf8)[:1]
    Stdev = cv2.meanStdDev(bf8, im3)[:1]
    cv2.imshow('Opencv Binary Image', binary)
    #cv2.imwrite('Frame'+str(i)+'.jpg',im3)
    i += 1
    print('Pixels =', cv2.countNonZero(im3))," \r",
    print('Mean =', *Mean[:1], sep='')," \r",
    print('Standard Deviation =',*Stdev[:1], sep='')," \r",
    with open(filename, 'a') as file:
        headers = ['Timestamp', 'Mean_values']
        writer = csv.DictWriter(file, delimiter=',', lineterminator='\n', fieldnames=headers)
        now = datetime.now().strftime("%d-%m-%Y %H:%M_%S.%f")
        Mean = str(Mean).translate({ord('('):'', ord(')'):''})
        writer.writerow({'Timestamp':now, 'Mean_values':Mean.replace(',', '')})
    # detect waitkey of q to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

