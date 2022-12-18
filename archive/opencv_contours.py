import numpy as np
import cv2

cap = cv2.VideoCapture(1 + cv2.CAP_V4L)

cap.set(cv2.CAP_PROP_CONVERT_RGB, 0) # turn off RGB conversion

while(True):
    # Capture frame-by-frame
    _, frame = cap.read()
    bf81 = np.array(frame // 16, dtype=np.uint8)
    # Create the mask
    #binary = cv2.imread('Masked_Image.png', 0)
    _, binary = cv2.threshold(bf81, 50, 255, cv2.THRESH_BINARY)
    im3 = cv2.bitwise_and(bf81, binary)
    im3[binary == 0] = 0
    Mean = cv2.mean(bf81, binary)
    print('Mean =', *Mean[:1], sep=''), " \r",
    cv2.imshow('Mask', binary)
    cv2.imshow('Original', bf81)
    cv2.imshow('Masked Image', im3)
    # detect waitkey of q to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break