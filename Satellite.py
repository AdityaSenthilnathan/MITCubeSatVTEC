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


def monitor(ip, PORT):
    # Set the server's IP address (replace with the actual IP of the server)

    # Create a socket (IPv4, TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((ip, PORT))
    print(f"Connected to server at {ip}:{PORT}")

    while not shouldExit:
        message = input("Enter message to send: ")  # Get user input
        if message.lower() == "exit":
            break  # Exit if the user types "exit"

        client_socket.sendall(message.encode())  # Send the message

        response = client_socket.recv(1024)  # Receive response
        print(f"Server says: {response.decode()}")
    client_socket.close()
    return



monitorThread = threading.Thread(target=monitor, args=("192.168.86.33",5000))
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


# bonus: function for uploading image to Github
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
photoPauseTime = 1  # s
loopPauseTime = 0.1  # s

# Main loop
rep_time = 2


def mainLoop(num, delay):

    i = 0  # Photo counter
    # print("entering main loop!")
    start_time = time.time()
    while i < num:

        # TAKE/SAVE/UPLOAD A PICTURE
        if (i * delay) - (time.time() - start_time) < 0:
            # print("capturing photo")

            # Name for the photo
            name = "Img"  # Last Name, First Initial  ex. FoxJ
            if name:
                # Save the photo with a unique name
                imgname = f'/home/TaftHS/MITCubeSatVTEC/New Images/{name}{i}.jpg'  # Change directory to your folder
                camera.capture_file(imgname)  # UPDATED TO USE PICAMERA2
                i += 1
                # print("captured photo")
        # Pause between iterations
        sleep(loopPauseTime)


def loadAndCompressImages(i):
    for j in range(int(i)):
        name = "Chick"
        imgname = f'/home/TaftHS/MITCubeSatVTEC/egg/{name}{j + 1}.jpg'
        image = Image.open(imgname)
        image_resized = image.resize((1920, 1080))
        image_resized.save(imgname)


def test(num, delay):
    mainLoop(num, delay)
    loadAndCompressImages(num)

    return "img count: " + str(num) + " | Time: " + str(git_push())


print(test(10, 2.5))