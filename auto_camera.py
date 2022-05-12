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

rep_time = 20
run_time = 60
start_time = time.time()
i = 1 
tol_t = 0.01

def git_push():
    try:
        repo = Repo('/home/pi/MITCubeSatSatickens') #PATH TO YOUR GITHUB REPO
        repo.git.add('hi') #PATH TO YOUR IMAGES FOLDER WITHIN YOUR GITHUB REPO
        repo.index.commit('New Photo')
        print('made the commit')
        origin = repo.remote('origin')
        print('added remote')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')


#Code to take a picture at a given offset angle

def capture(which_angle ='pitch', target_angle = 0, method = "am", tol = 0.5, refresh_rate = 50): #tol is tolerance of the angle
    #Calibration lines should remain commented out until you implement calibration
    offset_mag = sc.calibrate_mag()
    offset_gyro =sc.calibrate_gyro()
    initial_angle = sc.set_initial(offset_mag)
    prev_angle = initial_angle
    print("Begin moving camera.")

    img_num = 1
    
    while run_time > (time.time() - start_time):
        target_time = i*rep_time
        accelX, accelY, accelZ = sensor1.acceleration #m/s^2
        magX, magY, magZ = sensor1.magnetic #gauss
    #Calibrate magnetometer readings
        magX = magX - offset_mag[0]
        magY = magY - offset_mag[1]
        magZ = magZ - offset_mag[2]

        gyroX, gyroY, gyroZ = sensor2.gyro #rad/s
        #Convert to degrees and calibrate
        gyroX = gyroX *180/np.pi - offset_gyro[0]
        gyroY = gyroY *180/np.pi - offset_gyro[1]
        gyroZ = gyroZ *180/np.pi - offset_gyro[2]

        #TODO: Everything else! Be sure to not take a picture on exactly a
        #certain angle: give yourself some margin for error. 
        if method == "am":
            if which_angle == 'roll':
                chosen_angle = sc.roll_am(accelX,accelY,accelZ) - prev_angle[0]
            elif which_angle == 'pitch':
                chosen_angle = sc.pitch_am(accelX,accelY,accelZ) - prev_angle[1]
            elif which_angle == "yaw":
                chosen_angle = sc.yaw_am(accelX,accelY,accelZ) - prev_angle[2]
            else:
                print("Invalid Input: Must be roll, pitch, or yaw")
                image = None
                break #abort trying to take an image
                #return None
        elif method == "gyro":
            if which_angle == 'roll':
                chosen_angle = sc.roll_gy(prev_angle[0]) + gyroZ
            elif which_angle == 'pitch':
                chosen_angle = sc.pitch_gy(prev_angle[1]) + gyroY
            elif which_angle == "yaw":
                chosen_angle = sc.yaw_gy(prev_angle[2]) + gyroX
            else:
                print("Invalid Input: Must be roll, pitch, or yaw")
                image = None
                break #abort trying to take an image
                #return None
        else:
            print("Invalid Input: Must be am or gyro")
            image = None
            break #abort trying to take an image

        if np.abs(chosen_angle - target_angle) < tol:
            if abs(target_time-(time.time() - start_time)) < tol_t:
                name = "Chick"
                imgname = ('/home/pi/MITCubeSatSatickens/hi/%s%d' % (name, img_num)) #change directory to your folder   
                image = camera.capture(imgname+ ".jpg") #take a photo
                img_num += 1
                git_push()
                break
    
        time.sleep(1/refresh_rate)

    return image



if __name__ == '__main__':
    capture(*sys.argv[1:])
