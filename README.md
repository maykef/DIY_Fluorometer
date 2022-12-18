# DIY_Fluorometer
Final Repo for the Fluorometer Project

The files start_camera.py, flash_sequence.py and light_sequence.py are all that is required to capture Fluorescence data. The crontab job should start with start_camera.py, followed a couple of minutes later by the flash_sequence, and the third minute by the light_sequence.py. 

There are two sensors in the chamber: A CO2 Sensor and a temperature and humidity sensor. Each of them have their own script that run for almost 24 hours.

The plot data and data sort scripts are used to process the raw fluorescence data produced by start_camera.py.

A create mask script creates a mask every day.
