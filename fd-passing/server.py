#!/usr/bin/env python3
"""
server.py

https://pymotw.com/2/socket/uds.html
"""
from __future__ import print_function

import os
import socket
import sys
import subprocess

import netstring
from netstring import log


def main(argv):
  server_address = argv[1]
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
      msg, descriptors = netstring.Receive(connection)

      #log('ancdata %s', type(ancdata))
      #os.write(ancdata, 'TESTING')

      # Why isn't 'ls' enough?
      p = subprocess.Popen(['ls', '--color=auto'], stdout=descriptors[0])
      status = p.wait()
      log('status = %d', status)

      reply = netstring.Encode(b'OK')
      connection.sendall(reply)
      log('')
            
    finally:
      #os.close(descriptors[0])
      # Clean up the connection
      connection.close()


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
