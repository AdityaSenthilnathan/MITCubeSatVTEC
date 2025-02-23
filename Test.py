import time
import board
import math
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo

# Initialize I2C bus
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)



def read_sensor():
    """Reads and prints data from the BNO055 sensor."""
    print("Temperature: {}°C".format(accel_gyro.temperature))
    print("Accelerometer (m/s²): {}".format(accel_gyro.acceleration))
    print("Magnetometer (µT): {}".format(mag.magnetic))
    print("Gyroscope (°/s): {}".format(accel_gyro.gyro))
    print("-" * 40)

try:
    while True:
        read_sensor()
        time.sleep(.1)  # Read data every second

except KeyboardInterrupt:
    print("Sensor reading stopped.")
