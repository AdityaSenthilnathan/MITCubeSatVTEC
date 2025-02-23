import adafruit_bno055
import time
import os
import board
import busio
from picamera2 import Picamera2  # UPDATED TO USE PICAMERA2
import numpy as np
import sys
import sensor_calc as sc
from git import Repo

i2c = busio.I2C(board.SCL, board.SDA)
sensor1 = adafruit_bno055.BNO055_I2C(i2c)
sensor2 = adafruit_bno055.BNO055_I2C(i2c)
camera = PiCamera()

while True:
	accelX, accelY, accelZ = sensor1.acceleration  # m/s^2
	magX, magY, magZ = sensor1.magnetic  # gauss
	print(f"x:{accelX} y:{accelY} z:{accelZ}")