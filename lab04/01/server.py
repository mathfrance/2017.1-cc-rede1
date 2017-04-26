#!/usr/bin/python
# -*- coding: utf-8 -*-

# Socket Python Doc: https://docs.python.org/2.7/library/socket.html

# first of all import the socket library
import socket

# next create a socket object
sock = socket.socket()
print "Socket successfully created"

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

# Next bind to the port
sock.bind(('localhost', port))
print "socket binded to %s" %(port)

# put the socket into listening mode
sock.listen(1)
print "socket is listening"

# Establish connection with client.
conn, addr = sock.accept()
print 'Got connection from', addr

# send a thank you message to the client.
conn.send('Thank you for connecting')

# Close the connection with the client
conn.close()
