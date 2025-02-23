import time
import board
import busio
import adafruit_bno055

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BNO055 sensor
sensor = adafruit_bno055.BNO055_I2C(i2c)

def read_sensor():
    """Reads and prints data from the BNO055 sensor."""
    print("Temperature: {}°C".format(sensor.temperature))
    print("Accelerometer (m/s²): {}".format(sensor.acceleration))
    print("Magnetometer (µT): {}".format(sensor.magnetic))
    print("Gyroscope (°/s): {}".format(sensor.gyro))
    print("Euler angles: {}".format(sensor.euler))
    print("Quaternion: {}".format(sensor.quaternion))
    print("Linear Acceleration (m/s²): {}".format(sensor.linear_acceleration))
    print("Gravity (m/s²): {}".format(sensor.gravity))
    print("-" * 40)

try:
    while True:
        read_sensor()
        time.sleep(1)  # Read data every second

except KeyboardInterrupt:
    print("Sensor reading stopped.")
