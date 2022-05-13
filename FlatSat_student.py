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
import numpy as np

rep_time = 10
run_time = 30

start_time = time.time()

i = 1 
tol = 0.01



# setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
camera = PiCamera()

#bonus: function for uploading image to Github
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

#SET THRESHOLD
threshold = 0 # m/s^2 (Estimated Acceleration felt at LEO)
photoPauseTime = 1 # s
loopPauseTime = 1 # s


while run_time > (time.time() - start_time):
    target_time = i*rep_time
 #TAKE/SAVE/UPLOAD A PICTURE 
    if abs(target_time-(time.time() - start_time)) < tol:
        print("hello world")
        
        i += 1
   
        name = "Satickens"   #Last Name, First Initial  ex. FoxJ
        
        if name:
            t = time.strftime("_%H%M%S")      # current time string
            imgname = ('/home/pi/MITCubeSatSatickens/hi/%s%d' % (name,i)) #change directory to your folder 
            img = camera.capture(imgname+ ".jpg") #take a photo
            
    #PAUSE

git_push()
    
