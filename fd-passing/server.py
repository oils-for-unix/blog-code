#!/usr/bin/env python3
"""
server.py

https://pymotw.com/2/socket/uds.html
"""
from __future__ import print_function

import errno
import os
import socket
import sys
import subprocess

import netstring
from netstring import log


def main(argv):
  server_address = argv[1]

  # Make sure the socket does not already exist
  # If we don't do this, we get 'address already in use'
  try:
    os.unlink(server_address)
  except OSError as e:
    if e.errno != errno.ENOENT:  # some error deleting it
      raise

  sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

  log('Binding to %s', server_address)
  sock.bind(server_address)

  # Listen for incoming connections

  # TODO: Should we MAINTAIN the connections?
  #
  # We don't need netstrings if the client opens and closes
  # every time?  But that's slower for coprocesses.
  #
  # A typical entry requires 3 commands: prompt, execute, and dump-state
  #   ECMD echo ${PS1@P}
  #   ECMD cd / 
  #   ECMD dump-state

  sock.listen(1)

  while True:
    # Wait for a connection
    log('accept()')
    conn, client_address = sock.accept()
    try:
      log('Connection from %r', client_address)

      # Note: This can raise various exceptions
      msg, descriptors = netstring.Receive(conn)

      # Why isn't 'ls' enough?
      p = subprocess.Popen(['ls', '--color=auto'], stdout=descriptors[0])
      status = p.wait()

      p = subprocess.Popen(['sleep', '1'])
      status = p.wait()

      # Close so we don't leak
      os.close(descriptors[0])
      log('status = %d', status)

      reply = netstring.Encode(b'OK')
      conn.sendall(reply)
      log('')
            
    finally:
      conn.close()


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
