import socket

# Set the server's IP address (replace with the actual IP of the server)
SERVER_IP = "192.168.86.33"  # Change this to the actual IP of the server
PORT = 12345  # Must match the server's port

# Create a socket (IPv4, TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, PORT))
print(f"Connected to server at {SERVER_IP}:{PORT}")

while True:
    message = input("Enter message to send: ")  # Get user input
    if message.lower() == "exit":
        break  # Exit if the user types "exit"

    client_socket.sendall(message.encode())  # Send the message

    response = client_socket.recv(1024)  # Receive response
    print(f"Server says: {response.decode()}")

client_socket.close()