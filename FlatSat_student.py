#complete CAPITALIZED sections

#AUTHOR: Aakash Senthilnathan
#DATE: 3/15/22

from tkinter.tix import IMAGETEXT
import libraries
import time
from time import sleep
import os
import board
import busio
import adafruit_bno055
from git import Repo
from picamera import PiCamera

setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
camera = PiCamera()
camera.start_preview()

#bonus: function for uploading image to Github
def git_push():
    try:
        repo = Repo('/home/pi/FlatSatChallenge') #PATH TO YOUR GITHUB REPO
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
threshold = 50


#read acceleration
while True:
    accelX, accelY, accelZ = sensor.acceleration
    print("acceleration: ", sensor.acceleration)
    print("Threshold: ", threshold)
     #CHECK IF READINGS ARE ABOVE THRESHOLD
    if threshold < sensor.acceleration:
        camera.start_preview()
        #PAUSE
        sleep(5)
        #take a photo
        camera.capture(imgname)

   

    
        #TAKE/SAVE/UPLOAD A PICTURE 
        name = "SenthilnathanA"     #Last Name, First Initial  ex. FoxJ
        
        if name:
            t = time.strftime("_%H%M%S")      # current time string
            imgname = ('/home/pi/FlatSatChallenge/Images/FileSource/%s%s' % (name,t)) #change directory to your folder

            #<YOUR CODE GOES HERE>#
            git_push()    
            camera.stop_preview()
    #PAUSE
