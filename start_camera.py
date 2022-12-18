import cv2
import time
import numpy as np
from datetime import datetime
import csv
import os

# Start the Clock
start = time.time()

# Establish the period of time to run
Time_Period = 50460 # 14 hours

# Define the camera
cap = cv2.VideoCapture(0 + cv2.CAP_V4L)

# Define the name of the file based on timestamp
filename = datetime.now().strftime("%d-%m-%Y_%H_%M.csv")

def create_file():
    with open(filename, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Mean_values'])

def prepare_camera():
    #choose camera resolution
    rows = 640
    cols = 480
    # Set parameters for the camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cols)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, rows)
    cap.set(cv2.CAP_PROP_CONVERT_RGB, 0) # turn off RGB conversion
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 8)
    cap.set(cv2.CAP_PROP_EXPOSURE, 10) #Not Supported
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*'Y16 '))
    print('Width = ', cap.get(3),' Height = ', cap.get(4),' fps = ', cap.get(5))


def camera_run():
    # Create the mask
    # Gray out both binaries and enable _, binary in order to create the mask.
    # after the mask has been obtained, gray out _, binary and enable both binary to
    # retrieve the mask.
    #binary = cv2.imread('Masked_Image.png')
    _, frame = cap.read()
    bf8 = np.array(frame//16, dtype= np.uint8)
    _, binary = cv2.threshold(bf8, 30, 255, cv2.THRESH_BINARY)
    im3 = cv2.bitwise_and(bf8,binary)
    im3[binary==0] = 0
    # Normalize the image
    bf8_2_color = cv2.applyColorMap(im3, cv2.COLORMAP_PARULA)
    # Display the image, print image size and fps and save each frame
    #cv2.imshow("Opencv Video See3Cam_CU51 Color", bf8_2_color)
    #cv2.imshow('Opencv Binary Image', binary)
    Mean = cv2.mean(im3, bf8)[:1]
    Stdev = cv2.meanStdDev(bf8, im3)[:1]
    #cv2.imwrite('Frame'+str(i)+'.jpg',im3)
    print('Pixels =', cv2.countNonZero(im3))," \r",
    print('Mean =', *Mean[:1], sep='')," \r",
    print('Standard Deviation =',*Stdev[:1], sep='')," \r",
    with open(filename, 'a') as file:
        headers = ['Timestamp', 'Mean_values']
        writer = csv.DictWriter(file, delimiter=',', lineterminator='\n', fieldnames=headers)
        now = datetime.now().strftime("%d-%m-%Y %H:%M_%S.%f")
        Mean = str(Mean).translate({ord('('):'', ord(')'):''})
        writer.writerow({'Timestamp':now, 'Mean_values':Mean.replace(',', '')})


if __name__ == "__main__":
    final_path = os.path.join('/media/nvidia/External_SSD_1TB/Fluorometer')
    if os.path.exists(final_path):
        latest_folder = os.path.getctime(final_path)
        folder_time = datetime.fromtimestamp(latest_folder).strftime('%Y-%m-%d')
        newdir = os.path.join(folder_time)
        os.chdir(os.path.join(final_path, newdir))
        create_file()
        prepare_camera()
        while True:
            camera_run()
            if time.time() > start + Time_Period:
                quit()

