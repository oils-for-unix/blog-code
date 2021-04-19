#!/usr/bin/env python3
"""
headless_client.py

We're using Python 3 because it supports descriptor passing.
"""
from __future__ import print_function

import pty
import optparse
import os
import socket
import sys

import py_fanos
from py_fanos import log


def main(argv):
  p = optparse.OptionParser(__doc__)
  p.add_option(
      '--socket-path', dest='socket_path', default=None,
      help='Socket path to connect to')
  p.add_option(
      '--socket-pair', dest='socket_pair', default=False, action='store_true',
      help='Create a new socket pair and fork the server')

  p.add_option(
      '--to-file', dest='to_file', default=None,
      help='Where the server should send child stdout')
  p.add_option(
      '--to-new-pty', dest='to_new_pty', default=False, action='store_true',
      help='Send the child stdout to a new PTY')

  opts, _ = p.parse_args(argv[1:])

  if opts.socket_pair:
    # Try to FORK THE SERVER and pass it a socket.
    # Doesn't work yet

    sock, sock2 = socket.socketpair()
    log('sock %s %d', sock, sock.fileno())
    log('sock2 %s %d', sock2, sock2.fileno())

    log('parent/client pid = %d', os.getpid())

    log('client descriptor state')
    os.system('ls -l /proc/%d/fd' % os.getpid())

    # This is necessary so that the child gets it
    os.set_inheritable(sock2.fileno(), True)

    # If we do this then we can't see descriptor 4 in the child
    import fcntl
    # fcntl.fcntl(sock2.fileno(), fcntl.F_SETFD, fcntl.FD_CLOEXEC)

    #fcntl.fcntl(sock.fileno(), fcntl.F_SETFD, fcntl.FD_CLOEXEC)

    child_argv = ['./server.py', '--socket-fd', str(sock2.fileno())]

    ret = os.fork()
    if ret == 0:
      os.close(sock.fileno())  # close parent end in child
      log('child/server pid = %d', os.getpid())
      os.execv(child_argv[0], child_argv)
    else:
      os.close(sock2.fileno())  # close child end in parent

      log('client descriptor state AFTER')
      os.system('ls -l /proc/%d/fd' % os.getpid())

  elif opts.socket_path:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    log('Connecting to %s', opts.socket_path)
    try:
      sock.connect(opts.socket_path)
    except socket.error as e:
      log('connect() error: %s', e)
      sys.exit(1)

  else:
    raise AssertionError()

  master_fd, slave_fd = -1, -1
  try:
    # NUL terminator
    msg = b'ECMD\0'

    if opts.to_file:
      stdout_fd = os.open(opts.to_file, os.O_RDWR | os.O_CREAT)

    elif opts.to_new_pty:
      master_fd, slave_fd = os.openpty()
      stdout_fd = slave_fd
      log('master %d slave %d', master_fd, slave_fd)

    else:
      raise AssertionError()

    log('stdout_fd = %d', stdout_fd)

    # Send 2 messages across one connection
    for i in range(2):
      py_fanos.send(sock, msg, [stdout_fd])

      msg, _ = py_fanos.recv(sock)

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
      log('from pty: %r', chunk)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
