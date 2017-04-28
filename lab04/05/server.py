#!/usr/bin/python
# -*- coding: utf-8 -*-

# Socket Python Doc: https://docs.python.org/2.7/library/socket.html

# Importe o pacote do socket.
import socket

# Cria um objeto socket TCP/IP.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket successfully created"

# Reserve a porta na qual deseja aceitar conexões.
port = 12345

# Ative a porta para o servidor
sock.bind(('localhost', port))
print "Socket binded to %s" %(port)

# Coloque o socket no modo de listening (escuta de conexão).
sock.listen(5)
print "Socket is listening"

while True:
    # Espere estabelecer conexão com um cliente.
    conn, addr = sock.accept()
    print 'Got connection from', addr

    # Envie uma mensagem para o cliente.
    conn.send('Thank you for connecting')

    # Feche a conexão com o cliente.
    conn.close()
