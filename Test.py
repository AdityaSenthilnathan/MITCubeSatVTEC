from numpy import sqrt
import math
import time
from time import sleep
import os
import board
import busio
import adafruit_bno055
from git import Repo
import numpy as np
from PIL import Image

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)  # Uncomment if using IMU


while True:
	accelX, accelY, accelZ = sensor.acceleration  # m/s^2
	magX, magY, magZ = sensor.magnetic  # gauss
	print(f"x:{accelX} y:{accelY} z:{accelZ}")