#!/usr/bin/python
# -*- coding: utf-8 -*-

# Socket Python Doc: https://docs.python.org/2.7/library/socket.html

# First of all import the socket library
import socket

# Next create a TCP/IP socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket successfully created"

# Reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

# Next bind to the port
sock.bind(('localhost', port))
print "socket binded to %s" %(port)

# Put the socket into listening mode
sock.listen(1)
print "socket is listening"

while True:
    # Establish connection with client.
    conn, addr = sock.accept()
    print 'Got connection from', addr

    # Send a thank you message to the client.
    conn.send('Thank you for connecting')

    # Close the connection with the client
    conn.close()
