# Import socket module
import socket


def func_1():
    # Define the port on which you want to connect
    host = "217.144.106.32"
    port = 43256
    i = 0
    ccv = 20.0
    while i != 1000:
        data = f"^MC:MT01,SN:TWM01,CV:20,CCV:{ccv}"
        print(i, data)
        # send_req = input('send a request? (y/n, q:quit): ')
        # if send_req != 'y':
        #     if send_req == 'q':
        #         break
        #     continue
        # connect to the server on local computer
        # Create a socket object
        s = socket.socket()
        s.connect((host, port))
        s.send(data.encode())
        # receive data from the server and decoding to get the string.
        print(s.recv(1024).decode())
        # close the connection
        s.close()
        i += 1
        ccv += 20


def func_5():
    # Define the port on which you want to connect
    host = "217.144.106.32"
    port = 43256
    i = 0
    ccv = 20.0
    while i != 1000:
        data = f"^MC:MT03,SN:TWM05,CV:20,CCV:{ccv}"
        print(i, data)
        # send_req = input('send a request? (y/n, q:quit): ')
        # if send_req != 'y':
        #     if send_req == 'q':
        #         break
        #     continue
        # connect to the server on local computer
        # Create a socket object
        s = socket.socket()
        s.connect((host, port))
        s.send(data.encode())
        # receive data from the server and decoding to get the string.
        print(s.recv(1024).decode())
        # close the connection
        s.close()
        i += 1
        ccv += 20


def func_6():
    # Define the port on which you want to connect
    host = "217.144.106.32"
    port = 43256
    i = 0
    ccv = 20.0
    while i != 1000:
        data = f"^MC:MT03,SN:TWM06,CV:20,CCV:{ccv}"
        print(i, data)
        # send_req = input('send a request? (y/n, q:quit): ')
        # if send_req != 'y':
        #     if send_req == 'q':
        #         break
        #     continue
        # connect to the server on local computer
        # Create a socket object
        s = socket.socket()
        s.connect((host, port))
        s.send(data.encode())
        # receive data from the server and decoding to get the string.
        print(s.recv(1024).decode())
        # close the connection
        s.close()
        i += 1
        ccv += 20


func_1()
func_5()
func_6()
