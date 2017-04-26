#!/usr/bin/python
# -*- coding: utf-8 -*-

# Socket Python Doc: https://docs.python.org/2.7/library/socket.html

# Import socket module
import socket

# Create a socket object
ipv4 = socket.AF_INET
udp = socket.SOCK_DGRAM
sock = socket.socket(ipv4, udp)

# Define the port on which you want to connect
port = 12345

sock.bind(('localhost', 44444))
# Send the data
sock.sendto("Hi Server", ('127.0.0.1', port))

data, addr = sock.recvfrom(1024)
print data

sock.close()