#!/usr/bin/python
# -*- coding: utf-8 -*-

# Socket Python Doc: https://docs.python.org/2.7/library/socket.html

# first of all import the socket library
import socket

# next create a socket object
ipv4 = socket.AF_INET
udp = socket.SOCK_DGRAM
sock = socket.socket(ipv4, udp)
print "Socket successfully created"

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

# Next bind to the port
sock.bind(('127.0.0.1', port))
print "socket binded to %s" %(port)

data, addr = sock.recvfrom(1024)
print 'Got connection from', addr

# Send the data
print data
sock.sendto(str('Hi Client'), addr)