from mimetypes import init
import adafruit_bno055
import time
import os
import board
import busio
from picamera import PiCamera
import numpy as np
import sys
import sensor_calc as sc
from git import Repo

i2c = busio.I2C(board.SCL, board.SDA)
sensor1 = adafruit_bno055.BNO055_I2C(i2c)
sensor2 = adafruit_bno055.BNO055_I2C(i2c)
camera = PiCamera()

def git_push():
    try:
        repo = Repo('/home/pi/MITCubeSatSatickens') #PATH TO YOUR GITHUB REPO
        repo.git.add('Images') #PATH TO YOUR IMAGES FOLDER WITHIN YOUR GITHUB REPO
        repo.index.commit('New Photo')
        print('made the commit')
        origin = repo.remote('origin')
        print('added remote')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')

#Code to take a picture at a given offset angle
def capture(which_angle ='roll', target_angle = 30, method = "am", tol = 0.5, refresh_rate = 50): #tol is tolerance of the angle
    #Calibration lines should remain commented out until you implement calibration
    offset_mag = sc.calibrate_mag()
    #offset_gyro =calibrate_gyro()
    initial_angle = sc.set_initial(offset_mag)
    #prev_angle = initial_angle
    print("Begin moving camera.")
    while True:
        accelX, accelY, accelZ = sensor1.acceleration #m/s^2
        magX, magY, magZ = sensor1.magnetic #gauss
	#Calibrate magnetometer readings
        magX = magX - offset_mag[0]
        magY = magY - offset_mag[1]
        magZ = magZ - offset_mag[2]

        #gyroX, gyroY, gyroZ = sensor2.gyroscope #rad/s
        #Convert to degrees and calibrate
        #gyroX = gyroX *180/np.pi - offset_gyro[0]
        #gyroY = gyroY *180/np.pi - offset_gyro[1]
        #gyroZ = gyroZ *180/np.pi - offset_gyro[2]

        #TODO: Everything else! Be sure to not take a picture on exactly a
        #certain angle: give yourself some margin for error. 
        if method == "am":
            if which_angle == 'roll':
                chosen_angle = sc.roll_am(accelX,accelY,accelZ) - initial_angle[0]
            elif which_angle == 'pitch':
                chosen_angle = sc.pitch_am(accelX,accelY,accelZ) - initial_angle[1]
            elif which_angle == "yaw":
                chosen_angle = sc.yaw_am(accelX,accelY,accelZ) - initial_angle[2]
            else:
                print("Invalid Input: Must be roll, pitch, or yaw")
                image = None
                break #abort trying to take an image
                #return None
        elif method == "gyro":
            image = None
            break
                #not yet implemented
        else:
            print("Invalid Input: Must be am or gyro")
            image = None
            break #abort trying to take an image

        if np.abs(chosen_angle - target_angle) < tol:
            name = "Satickens"
            t = time.strftime("_%H%M%S")      # current time string
            imgname = ('/home/pi/MITCubeSatSatickens/Images/%s%s' % (name,t)) #change directory to your folder   
            image = camera.capture(imgname+ ".jpg") #take a photo
            git_push()
            break
        time.sleep(1/refresh_rate)

    return image
if __name__ == '__main__':
    capture(*sys.argv[1:])
