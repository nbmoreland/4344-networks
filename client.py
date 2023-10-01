from socket import *
from time import *

# Default Settings
FILE = "index.html"
ENCODE_FORMAT = "utf-8"

# Set the socket parameters
host = "localhost"
port = 8080

# Create a TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host, port))

# Send a message to the client
print(f"Connection info: {clientSocket}\n")

# Start RTT timer and send message to the server
sentTime = time()
clientSocket.send(f"GET /{FILE} HTTP/1.1\r\n\r\n".encode(ENCODE_FORMAT))

# Receive the server's response
response = clientSocket.recv(1024).decode(ENCODE_FORMAT)
status = response[:response.find("\r\n\r\n")]
print(f"Server response: {status}")

# Print body if status is 200 OK
if status == "HTTP/1.1 200 OK":
    body = response[response.find("\r\n\r\n") + 4:]
    print(f"\n {body}")
else:
    print(f"Server response: {status}")
    print(f"Response body: {response}")

# Print RTT
print(f"RTT: {time() - sentTime}")

# Close the socket
clientSocket.close()
