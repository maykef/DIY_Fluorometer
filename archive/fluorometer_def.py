import numpy as np
import cv2
from multiprocessing import Process
from uvctypes import *
import serial
import csv
try:
  from queue import Queue
except ImportError:
  from Queue import Queue

#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def camera_monochrome():
    i = 0
    cap = cv2.VideoCapture(0 + cv2.CAP_V4L)
    print('Width = ', cap.get(3), ' Height = ', cap.get(4), ' fps = ', cap.get(5))
    rows = 640
    cols = 480
    # Set parameters for the camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cols)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, rows)
    cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)  # turn off RGB conversion
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 50)
    cap.set(cv2.CAP_PROP_CONTRAST, 80)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*'Y16 '))
    if cap.isOpened():
        window_handle = cv2.namedWindow("See3Cam_50", cv2.WINDOW_AUTOSIZE)
        # Window
        while cv2.getWindowProperty("See3Cam_50", 0) >= 0:
            _, img = cap.read()
            bf8 = np.array(img // 16, dtype=np.uint8)
            binary = cv2.imread('Masked_Image.png',0)
            #_, binary = cv2.threshold(bf8, 50, 255, cv2.THRESH_BINARY)
            im3 = cv2.bitwise_and(bf8, binary)
            im3[binary == 0] = 0
            # Normalize the image
            bf8_2_color = cv2.applyColorMap(im3, cv2.COLORMAP_PARULA)
            #im_final = cv2.vconcat([im3, bf8_2_color])
            # Display the image, print image size and fps and save each frame
            cv2.imshow('Masked_Image', im3)
            cv2.imshow("See3Cam_50", bf8_2_color)
            Mean = cv2.mean(bf8, im3)[:1]
            Stdev = cv2.meanStdDev(bf8, im3)[:1]
            #cv2.imwrite('Frame' + str(i) + '.jpg', im3)
            i += 1
            print('Pixels =', cv2.countNonZero(im3)), " \r",
            print('Mean =', *Mean[:1], sep=''), " \r",
            print('Standard Deviation =', *Stdev[:1], sep=''), " \r",
            with open('results.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(Mean)
            # detect waitkey of q to quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
    else:
        print("Unable to open camera")


BUF_SIZE = 2
q = Queue(BUF_SIZE)

def py_frame_callback(frame, userptr):

  array_pointer = cast(frame.contents.data, POINTER(c_uint16 * (frame.contents.width * frame.contents.height)))
  data = np.frombuffer(
    array_pointer.contents, dtype=np.dtype(np.uint16)
  ).reshape(
    frame.contents.height, frame.contents.width
  )

  if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
    return

  if not q.full():
    q.put(data)

PTR_PY_FRAME_CALLBACK = CFUNCTYPE(None, POINTER(uvc_frame), c_void_p)(py_frame_callback)

def ktof(val):
  return (1.8 * ktoc(val) + 32.0)

def ktoc(val):
  return (val - 27315) / 100.0

def raw_to_8bit(data):
  cv2.normalize(data, data, 0, 65535, cv2.NORM_MINMAX)
  np.right_shift(data, 8, data)
  return cv2.cvtColor(np.uint8(data), cv2.COLOR_GRAY2RGB)

def display_temperature(img, val_k, loc, color):
  val = ktoc(val_k)
  cv2.putText(img,"{0:.1f} degC".format(val), loc, cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
  x, y = loc
  cv2.line(img, (x - 2, y), (x + 2, y), color, 1)
  cv2.line(img, (x, y - 2), (x, y + 2), color, 1)

def main():
  ctx = POINTER(uvc_context)()
  dev = POINTER(uvc_device)()
  devh = POINTER(uvc_device_handle)()
  ctrl = uvc_stream_ctrl()

  res = libuvc.uvc_init(byref(ctx), 0)
  if res < 0:
    print("uvc_init error")
    exit(1)

  try:
    res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
    if res < 0:
      print("uvc_find_device error")
      exit(1)

    try:
      res = libuvc.uvc_open(dev, byref(devh))
      if res < 0:
        print("uvc_open error")
        exit(1)

      print("device opened!")

      print_device_info(devh)
      print_device_formats(devh)

      frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)
      if len(frame_formats) == 0:
        print("device does not support Y16")
        exit(1)

      libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
        frame_formats[0].wWidth, frame_formats[0].wHeight, int(1e7 / frame_formats[0].dwDefaultFrameInterval)
      )

      res = libuvc.uvc_start_streaming(devh, byref(ctrl), PTR_PY_FRAME_CALLBACK, None, 0)
      if res < 0:
        print("uvc_start_streaming failed: {0}".format(res))
        exit(1)

      try:
        while True:
          data = q.get(True, 500)
          if data is None:
            break
          data = cv2.resize(data[:,:], (640, 480))
          minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(data)
          img = raw_to_8bit(data)
          display_temperature(img, minVal, minLoc, (255, 0, 0))
          display_temperature(img, maxVal, maxLoc, (0, 0, 255))
          cv2.imshow('Lepton Radiometry', img)
          cv2.waitKey(1)

        cv2.destroyAllWindows()
      finally:
        libuvc.uvc_stop_streaming(devh)

      print("done")
    finally:
      libuvc.uvc_unref_device(dev)
  finally:
    libuvc.uvc_exit(ctx)

if __name__ == "__main__":
    #ser.write(b'2')
    p1 = Process(target=camera_monochrome)
    p1.start()
    p2 = Process(target=main)
    p2.start()
    p1.join()
    p2.join()