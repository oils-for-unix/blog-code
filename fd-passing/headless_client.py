#!/usr/bin/env python3
"""
headless_client.py

Python 3 supports descriptor passing.
"""
from __future__ import print_function

import array
import pty
import os
import socket
import sys

import netstring
from netstring import log


def main(argv):
  server_address = argv[1]

  # Where to write the response
  try:
    where = argv[2]  # could be 'file'
  except IndexError:
    where = 'my-stdout'

  sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

  log('Connecting to %s', server_address)
  try:
    sock.connect(server_address)
  except socket.error as e:
    log('error: %s', e)
    sys.exit(1)

  master_fd, slave_fd = -1, -1
  try:
    # NUL terminator
    msg = b'MAIN\0'

    if where == 'my-stdout':
      stdout_fd = sys.stdout.fileno()

    elif where == 'pty':
      master_fd, slave_fd = os.openpty()
      stdout_fd = slave_fd
      log('master %d slave %d', master_fd, slave_fd)

    else:
      stdout_fd = os.open(where, os.O_RDWR | os.O_CREAT)

    log('stdout_fd = %d', stdout_fd)

    sock.send(b'%d:' % len(msg))  # netstring prefix

    # Send the FILE DESCRIPTOR with the NETSTRING PAYLOAD
    ancillary = (
      socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", [stdout_fd])
    )
    result = sock.sendmsg([msg], [ancillary])
    log('sendmsg returned %s', result)

    sock.send(b',')  # trailing netstring thing

    msg, _ = netstring.Receive(sock)

  finally:
    log('closing socket')
    sock.close()

  #os.close(slave_fd)
  if master_fd != -1:
    # This hangs because the server still has the terminal open?  Not sure
    # where to close it.
    while True:
      chunk = os.read(master_fd, 1024)
      if not chunk:
        break
      log('pty %r', chunk)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
