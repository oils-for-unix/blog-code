#!/usr/bin/env python3
"""
server.py

https://pymotw.com/2/socket/uds.html
"""
from __future__ import print_function

import socket
import sys
import os

import netstring
from netstring import log

server_address = './uds_socket'

# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the port
log('starting up on %s', server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
  # Wait for a connection
  log('waiting for a connection')
  connection, client_address = sock.accept()
  try:
    log('connection from %s', client_address)
    data, ancdata = netstring.Receive(connection)
    log('data %r, ancdata %r', data, ancdata)

    reply = netstring.Encode(b'OK')
    connection.sendall(reply)
    log('')
          
  finally:
    # Clean up the connection
    connection.close()
