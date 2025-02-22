import image_processing
import cv2
import os
import Common
import socket
import threading
import subprocess
import shutil

def monitor(port):
    # Server configuration
    HOST = "0.0.0.0"  # Listen on all available network interfaces
    # Create a socket (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, port))
    server_socket.listen(1)

    print(f"Server listening on port {port}...")

    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    while True:
        data = client_socket.recv(1024)  # Receive data (max 1024 bytes)
        if not data:
            break  # Exit if client disconnects
        print(f"Received: {data.decode()}")  # Print received message



    client_socket.close()
    server_socket.close()


monitorThread = threading.Thread(target=monitor, args=(5000,))
monitorThread.start()


def check_for_changes():
    try:
        # Fetch the latest changes from the remote without merging
        subprocess.run(['git', 'fetch'], check=True)

        # Compare local branch with the remote branch to see if there are updates
        result = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True)

        # Check if the local branch is behind the remote
        if "Your branch is behind" in result.stdout:
            return True  # There are new changes
        else:
            return False  # No new changes
    except subprocess.CalledProcessError as e:
        print(f"Error checking repository status: {e}")
        return False

def pull_changes():
    try:
        # Pull the latest changes from the remote repository
        subprocess.run(['git', 'pull'], check=True)
        print("Successfully pulled new changes.")
        # Run your custom function after pulling changes
    except subprocess.CalledProcessError as e:
        print(f"Error pulling changes: {e}")

def list_files_in_directory(directory_path):
    try:
        # Get all files and directories in the specified directory
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        return files
    except FileNotFoundError:
        print(f"Error: The directory {directory_path} does not exist.")
        return []
    except PermissionError:
        print(f"Error: Permission denied to access {directory_path}.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


while True:
    if check_for_changes():
        images = list_files_in_directory("New Images")
        for image in images:
            shutil.copy(f"New Images/{image}", f"Old Images/{image}")
        pull_changes()
        image_processing.possess_image(cv2.imread("Old Images/Img1.jpg"), cv2.imread("New Images/Img1.jpg"))

