# Import socket module
import socket

# Create a socket object
s = socket.socket()
s1 = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect(('127.0.0.1', port))
s1.connect(('127.0.0.1', port))

# Send data to server 'Hello world'

## s.sendall('Hello World')

input_string = input("Enter data you want to send->")
s.sendall(input_string.encode('ascii'))
s1.sendall("S2".encode('ascii'))

# receive data from the server
print(s.recv(1024).decode('ascii'))
print(s1.recv(1024).decode('ascii'))

# close the connection
s.close()
s1.close()
