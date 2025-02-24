from operator import truediv
from socket import socket
from Common import MessageType
import socket
import threading
import time
from time import sleep
import board
import busio
import adafruit_bno055
from git import Repo
from picamera2 import Picamera2  # UPDATED TO USE PICAMERA2
from PIL import Image
#import libraries
import time
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from enum import IntFlag
from enum import Enum
import datetime

class Axis(IntFlag):
    X = 1
    Y = 2
    Z = 4


class Command(Enum):
    NoCommand = 0
    Picture = 1
    StartSequence = 2
    StopSequence = 3
    Arm = 4
    Disarm = 5




shouldExit = False
isConnected = False
client_socket = None


currentCommand = Command.NoCommand
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

AwaitStartAxis = Axis.Y | Axis.Z

def monitor(ip, PORT):
    # Set the server's IP address (replace with the actual IP of the server)
    global shouldExit
    global AwaitStartAxis
    global currentCommand
    # Create a socket (IPv4, TCP)
    global client_socket
    client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((ip, PORT))
    print(f"Connected to server at {ip}:{PORT}")
    global isConnected
    isConnected = True
    while not shouldExit:

        response = client_socket.recv(1024).decode()  # Receive response
        transmit_message(response)
        print(f"Server says: {response}")

        if response == str(MessageType.Exit.value):
            shouldExit = True
        elif response == str(MessageType.Picture.value):
            currentCommand = Command.Picture
        elif response == str(MessageType.AxisX.value):
            AwaitStartAxis = AwaitStartAxis ^ Axis.X
            transmit_message(f"Axis: {bin(AwaitStartAxis)[2:]}")
        elif response == str(MessageType.AxisY.value):
            AwaitStartAxis = AwaitStartAxis ^ Axis.Y
            transmit_message(f"Axis: {bin(AwaitStartAxis)[2:]}")
        elif response == str(MessageType.AxisZ.value):
            AwaitStartAxis = AwaitStartAxis ^ Axis.Z
            transmit_message(f"Axis: {bin(AwaitStartAxis)[2:]}")
        elif response == str(MessageType.StartSequence.value):
            currentCommand = Command.StartSequence
        elif response == str(MessageType.StopSequence.value):
            currentCommand = Command.StopSequence
        elif response == str(MessageType.Arm.value):
            currentCommand = Command.Arm
        elif response == str(MessageType.Disarm.value):
            currentCommand = Command.Disarm

    client_socket.close()
    return


def transmit_message(msg):
    print( f"[Transmitting]: {msg}")
    if isConnected:
        client_socket.sendall(msg.encode())


def close_connection():
    global shouldExit
    shouldExit = True

monitorThread = threading.Thread(target=monitor, args=("192.168.86.33", 5000))
monitorThread.start()

sleep(2)

# setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
# sensor = adafruit_bno055.BNO055_I2C(i2c)  # Uncomment if using IMU
camera = Picamera2()  # UPDATED TO USE PICAMERA2
camera_config = camera.create_still_configuration()
camera.configure(camera_config)
camera.start()
time.sleep(2)
full_res = list(camera.camera_properties['PixelArraySize'])
camera.set_controls({'ScalerCrop': [0, 0] + full_res})


# bonus: function for uploading image to GitHub
def git_push():
    try:
        repo = Repo('/home/TaftHS/MITCubeSatVTEC')  # PATH TO YOUR GITHUB REPO
        repo.git.add('New Images')  # PATH TO YOUR IMAGES FOLDER WITHIN YOUR GITHUB REPO
        repo.index.commit('New Photo')
        # print('Made the commit')

        # Get the remote origin
        origin = repo.remote('origin')
        # print('added remote')
        # Push the changes to your branch (adjust the branch name if needed)
        startTime = time.time()
        origin.push()
        endTime = time.time()

        # print('pushed changes')
        return endTime - startTime
    except Exception as e:
        print(f"Couldn't upload to git: {e}")
        import traceback
        traceback.print_exc()


# SET THRESHOLD
threshold = 0  # m/s^2 (Estimated Acceleration felt at LEO)
loopPauseTime = 0.1  # s


def mainLoop(num, delay):

    i = 0  # Photo counter
    transmit_message("entering main loop!")
    start_time = time.time()
    while i < num:

        # TAKE/SAVE/UPLOAD A PICTURE
        if (i * delay) - (time.time() - start_time) < 0:
            transmit_message("capturing photo")

            # Name for the photo
            name = "Img"  # Last Name, First Initial  ex. FoxJ
            if name:
                # Save the photo with a unique name
                imgname = f'/home/TaftHS/MITCubeSatVTEC/New Images/{name}{i}.jpg'  # Change directory to your folder
                camera.capture_file(imgname)  # UPDATED TO USE PICAMERA2
                i += 1
                transmit_message("captured photo")
        # Pause between iterations
        sleep(loopPauseTime)


def loadAndCompressImages(i):
    for j in range(int(i)):
        name = "Img"
        imgname = f'/home/TaftHS/MITCubeSatVTEC/New Images/{name}{j}.jpg'
        image = Image.open(imgname)
        image_resized = image.resize((1920, 1080))
        image_resized.save(imgname)

def takeAndUploadSinglePicture(filename):
    if filename:
        # Save the photo with a unique name
        imgname = f'/home/TaftHS/MITCubeSatVTEC/egg/{filename}.jpg'  # Change directory to your folder
        camera.capture_file(imgname)  # UPDATED TO USE PICAMERA2
        transmit_message("captured photo")
        image = Image.open(imgname)
        image_resized = image.resize((1920, 1080))
        image_resized.save(imgname)
        git_push()

def test(num, delay):
    mainLoop(num, delay)
    loadAndCompressImages(num)

    return "img count: " + str(num) + " | Time: " + str(git_push())



def testSequence():
    while True:
        if currentCommand == Command.StopSequence:
            return
        accelx, accely, accelz = accel_gyro.acceleration

        accelSqaredMag = (accelx * accelx) + (accely * accely) + (accelz * accelz)

def armedSimpleloop():
    continueLoop = True
    while continueLoop:
        accelx, accely, accelz = accel_gyro.acceleration

        accelSqaredMag = (accelx * accelx) + (accely * accely)
        if accelSqaredMag > 3:
            mainLoop(2, 5)
            continueLoop = False


def advancedMainLoop():
    while True:
        if currentCommand == Command.Picture:
            name = "Test"
            current_time = datetime.datetime.now()

            takeAndUploadSinglePicture(f"{current_time.hour}:{current_time.minute}:{current_time.second}")
        if currentCommand == Command.StartSequence:
            testSequence()
        if currentCommand == Command.Arm:
            armedSimpleloop()