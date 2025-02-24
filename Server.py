import image_processing
import cv2
import os
import datetime
import Common
import socket
import threading
import subprocess
import shutil

client_socket = None

def monitor(port):
    global client_socket
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
        current_time = datetime.datetime.now();
        print(f"[{current_time.hour}:{current_time.minute}:{current_time.second}][From {client_address[0]}]: {data.decode()}")  # Print received message



    client_socket.close()
    server_socket.close()

def userInput():
    global client_socket
    while True:
        response = input()  # Send a response
        print(f"Transmitting: {response}")
        client_socket.sendall(response.encode())


monitorThread = threading.Thread(target=monitor, args=(5000,))
monitorThread.start()

userInputThread = threading.Thread(target=userInput)
userInputThread.start()



