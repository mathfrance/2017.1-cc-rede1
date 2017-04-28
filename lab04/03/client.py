#!/usr/bin/python
# -*- coding: utf-8 -*-

# Socket Python Doc: https://docs.python.org/2.7/library/socket.html

# Importe o pacote do socket
import socket

# Cria um objeto socket UDP
ipv4 = socket.AF_INET
udp = socket.SOCK_DGRAM
sock = socket.socket(ipv4, udp)

# Defina a porta na qual você deseja se conectar
port = 12345

# Envia uma mensagem ao servidor
sock.sendto("Hi Server", ('127.0.0.1', port))

# Espera receber uma mensagem de resposta do servidor.
data, addr = sock.recvfrom(1024)
print data

# Feche a conexão
sock.close()