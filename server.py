# TCP Server from the book
from socket import *
from threading import *
import os
from sys import *

# Default Settings
FILE = "index.html"
ENCODE_FORMAT = "utf-8"

# Set the socket parameters
host = "localhost"
port = 8080

# Create a TCP socket
server = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the port
try:
    server.bind((host, port))
except error as e:
    print(str(e))
    exit()

# Start listening for incoming connections
server.listen()

# Server should be up and running and listening to the incoming connections
print(f'Server listening on {host}:{port}\n')


def handle_client(connection, address):
    # Receive the data from the client
    request = connection.recv(1024).decode(ENCODE_FORMAT)

    # Parse the request
    headers = {}
    for line in request.split("\r\n"):
        headers[line[0:line.find(" ")]] = line[line.find(" ") + 1:]

    # Print the request
    print(f"Connection info: {connection}")

    # Find the file
    file = headers["GET"].split()[0]
    if file.startswith("//pages/") or file.startswith("/pages/"):
        path = "." + file
    else:
        path = './pages' + file

    print(f"Requested file: {path}")

    # 404 Status
    if not os.path.exists(path):
        response = "HTTP/1.1 404 Not Found\r\n"
        response += "Content-Type: text/html\r\n\r\n"

        with open("./pages/404.html", 'r') as f:
            body = f.read()
            print(f"Response body: {body}")
            response += body

        connection.send(response.encode(ENCODE_FORMAT))
        connection.close()
        return

    # 301 Status
    if file != "/" + FILE:
        response = "HTTP/1.1 301 Moved Permanently\r\n"
        response += f"Location: /{FILE}\r\n\r\n"
        connection.send(response.encode(ENCODE_FORMAT))
        connection.close()
        return

    # 200 Status
    with open(path, 'r') as f:
        body = f.read()
        connection.send(
            f"HTTP/1.1 200 OK\r\n\r\n{body}".encode(ENCODE_FORMAT))

    # Close the connection
    connection.close()
    print()


# Listen for incoming connections
while True:
    connection, address = server.accept()
    thread = Thread(target=handle_client, args=(connection, address))
    thread.start()
    print(f"Active connections: {active_count() - 1}")
