#!/usr/bin/python
# -*- coding: utf-8 -*-

# Socket Python Doc: https://docs.python.org/2.7/library/socket.html

# First of all import the socket library
import socket

# Next create a socket object
ipv4 = socket.AF_INET
udp = socket.SOCK_DGRAM
sock = socket.socket(ipv4, udp)
print "Socket successfully created"

# Reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

# Next bind to the port to server
sock.bind(('127.0.0.1', port))
print "socket binded to %s" %(port)

while True:
    # Connect and receive data from client
    data, addr = sock.recvfrom(1024)
    print 'Got connection from', addr

    # Send the data to client
    print data
    sock.sendto(str('Hi Client'), addr)