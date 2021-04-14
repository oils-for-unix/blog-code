#!/usr/bin/env python3
"""
headless_client.py

Python 3 supports descriptor passing.
"""
from __future__ import print_function

import array
import socket
import os
import sys

import netstring
from netstring import log


def main(argv):
  sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

  print(sys.version)
  print('Hello from headless_client.py')
  print(sock.sendmsg)

  server_address = './uds_socket'
  log('Connecting to %s', server_address)
  try:
    sock.connect(server_address)
  except socket.error as e:
    log('error: %s', e)
    sys.exit(1)

  try:
    where = argv[1]  # could be 'file'
  except IndexError:
    mode = 'stdout'

  try:
    # NUL terminator
    msg = b'MAIN\0'

    if where == 'stdout':
      stdout_fd = sys.stdout.fileno()
    else:
      stdout_fd = os.open(where, os.O_RDWR | os.O_CREAT)

    log('stdout_fd = %d', stdout_fd)

    sock.send(b'%d:' % len(msg))  # netstring prefix

    # Send the FILE DESCRIPTOR with the NETSTRING PAYLOAD
    result = sock.sendmsg([msg], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", [stdout_fd]))])
    log('sendmsg returned %s', result)

    sock.send(b',')  # trailing netstring thing

    msg, _ = netstring.Receive(sock)

  finally:
    log('closing socket')
    sock.close()


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
