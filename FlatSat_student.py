#complete CAPITALIZED sections

#AUTHOR: Hyunwoo Lee/Aakash Senthilnathan
#DATE: 3/15/22

#import libraries
from numpy import sqrt
import math
import time
from time import sleep
import os
import board
import busio
import adafruit_bno055
from git import Repo
from picamera import PiCamera
from .cv2 import cv
import numpy as np

# setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
camera = PiCamera()

#bonus: function for uploading image to Github
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

#SET THRESHOLD
threshold = 12 # m/s^2 (Estimated Acceleration felt at LEO)
photoPauseTime = 5 # s
loopPauseTime = 5 # s

#read acceleration
while True:
 #TAKE/SAVE/UPLOAD A PICTURE 
    accelX, accelY, accelZ = sensor.acceleration
    accel=sqrt(accelX**2 + accelY**2 + accelZ**2)
    
     #CHECK IF READINGS ARE ABOVE THRESHOLD
    if accel>threshold:
        print("Taking picture in 5 seconds")
        sleep(photoPauseTime)
        name = "Satickens"   #Last Name, First Initial  ex. FoxJ
        
        if name:
            t = time.strftime("_%H%M%S")      # current time string
            imgname = ('/home/pi/MITCubeSatSatickens/Images/%s%s' % (name,t)) #change directory to your folder   
            img = camera.capture(imgname+ ".jpg") #take a photo
            img = cv.imread(img)
            git_push()
    #PAUSE
    sleep(loopPauseTime)
