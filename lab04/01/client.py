#!/usr/bin/python
# -*- coding: utf-8 -*-

# Socket Python Doc: https://docs.python.org/2.7/library/socket.html

# Importe o pacote do socket.
import socket

# Cria um objeto socket por padrão TCP/IP.
sock = socket.socket()

# Defina a porta na qual você deseja se conectar.
port = 12345

# Conecte ao servidor que está executando localmente.
sock.connect(('127.0.0.1', port))

# Receba os dados do servidor.
buffer_size = 1024
print sock.recv(buffer_size)

# Feche a conexão.
sock.close()
