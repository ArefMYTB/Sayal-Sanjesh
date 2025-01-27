import socket

data = "something"

def send_message_to_node(data, host="217.144.106.32", port=43256):
    while True:
        # connect to the server on local computer
        # Create a socket object
        s = socket.socket()
        s.connect((host, port))
        s.send(data.encode())
        # receive data from the server and decoding to get the string.
        response = s.recv(1024).decode()
        # close the connection
        s.close()
        return response
