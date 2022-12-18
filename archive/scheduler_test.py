import schedule
import time
import serial
import sys
#import camera_test

def stop_program():
    camera_test.quit()
    sys.exit(0)


schedule.every(3).minute.at(':00').do(stop_program)
schedule.clear()


while True:
    schedule.run_pending()
    time.sleep(1)