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
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
sock.bind(('', port))
print "socket binded to %s" %(port)

# put the socket into listening mode
sock.listen(1)
print "socket is listening"

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    conn, addr = sock.accept()
    print 'Got connection from', addr

    # send a thank you message to the client.
    conn.send('Thank you for connecting')

    # Close the connection with the client
    conn.close()
