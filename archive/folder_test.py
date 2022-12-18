import os
from datetime import datetime


def new_folder():
    """Creates a new folder each time the script runs"""
    imagepath = os.path.join('/media/nvidia/External_SSD_1TB/Fluorometer')
    if os.path.exists(imagepath):
        datetime.now().strftime('%d-%m-%Y_%H:%M')
        now = datetime.now()
        newdirname = now.strftime('%d-%m-%Y_%H:%M')
        os.mkdir(os.path.join(imagepath, newdirname))
        print('Creating ' + newdirname + ' folder')

if __name__ == "__main__":
    new_folder()