from socket import socket

import Common
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


shouldExit = False
isConnected = False
client_socket: socket = None

def monitor(ip, PORT):
    # Set the server's IP address (replace with the actual IP of the server)

    # Create a socket (IPv4, TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((ip, PORT))
    print(f"Connected to server at {ip}:{PORT}")
    isConnected = True
    while not shouldExit:

        response = client_socket.recv(1024)  # Receive response
        print(f"Server says: {response.decode()}")
    client_socket.close()
    return


def transmit_message(msg):
    print(msg)
    if isConnected:
        client_socket.sendall(msg.encode())


def close_connection():
    shouldExit = True

monitorThread = threading.Thread(target=monitor, args=("192.168.86.33", 5000))
monitorThread.start()

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
        repo.git.add('egg')  # PATH TO YOUR IMAGES FOLDER WITHIN YOUR GITHUB REPO
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
        imgname = f'/home/TaftHS/MITCubeSatVTEC/New Images/{name}{j + 1}.jpg'
        image = Image.open(imgname)
        image_resized = image.resize((1920, 1080))
        image_resized.save(imgname)


def test(num, delay):
    mainLoop(num, delay)
    loadAndCompressImages(num)

    return "img count: " + str(num) + " | Time: " + str(git_push())


transmit_message(test(10, 2.5))