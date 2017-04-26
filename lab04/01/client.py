#!/usr/bin/python
# -*- coding: utf-8 -*-

# Socket Python Doc: https://docs.python.org/2.7/library/socket.html

# Import socket module
import socket

# Create a socket object
sock = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
sock.connect(('127.0.0.1', port))

# receive data from the server
print sock.recv(1024)

# close the connection
sock.close()
