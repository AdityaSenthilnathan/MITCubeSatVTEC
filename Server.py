import image_processing

import socket

# Server configuration
HOST = "0.0.0.0"  # Listen on all available network interfaces
PORT = 12345       # Port to listen on

# Create a socket (IPv4, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on port {PORT}...")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

while True:
    data = client_socket.recv(1024)  # Receive data (max 1024 bytes)
    if not data:
        break  # Exit if client disconnects
    print(f"Received: {data.decode()}")  # Print received message

    response = input("Reply to client: ")  # Send a response
    client_socket.sendall(response.encode())

client_socket.close()
server_socket.close()