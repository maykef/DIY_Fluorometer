#!/usr/bin/env python

"""
CV2 video capture example from Pure Thermal 1
"""

try:
    import cv2
except ImportError:
    print("ERROR python-opencv must be installed")
    exit(1)

class OpenCvCapture(object):
    """
    Encapsulate state for capture from Pure Thermal 1 with OpenCV
    """

    def __init__(self):
        cv2_cap = cv2.VideoCapture(0)
        if cv2_cap.isOpened():
            print("Thermal Camera Found")
        if not cv2_cap.isOpened():
            print("Thermal Camera not found!")
            exit(1)

        self.cv2_cap = cv2_cap

    def show_video(self):
        """
        Run loop for cv2 capture from lepton
        """
        cv2.namedWindow("lepton", cv2.WINDOW_NORMAL)
        print("Running, ESC or Ctrl-c to exit...")
        while True:
            ret, img = self.cv2_cap.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #_, binary = cv2.threshold(img, 88, 255, cv2.THRESH_BINARY)
            #im3 = cv2.bitwise_and(img, binary)
            #im3[binary == 0] = 0
            blur = cv2.GaussianBlur(img, (5,5),cv2.BORDER_DEFAULT)
            canny = cv2.Canny(blur, 10, 50)
            contours = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
            cnt = contours[4]
            cv2.drawContours()

            if ret == False:
                print("Error reading image")
                break

            cv2.imshow("lepton", cv2.resize(img, (640, 480)))
            if cv2.waitKey(5) == 27:
                break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    OpenCvCapture().show_video()
