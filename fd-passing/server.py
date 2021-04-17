#!/usr/bin/env python3
"""
server.py

https://pymotw.com/2/socket/uds.html
"""
from __future__ import print_function

import errno
import optparse
import os
import socket
import sys
import subprocess

import netstring
from netstring import log


def main(argv):
  p = optparse.OptionParser(__doc__)
  p.add_option(
      '--socket-path', dest='socket_path', default=None,
      help='Socket path to connect to')
  p.add_option(
      '--socket-fd', dest='socket_fd', type='int', default=None,
      help='File descriptor for our end of socketpair()')

  opts, _ = p.parse_args(argv[1:])

  if opts.socket_path:  # PATH like /tmp/c5po.socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Make sure the socket does not already exist
    # If we don't do this, we get 'address already in use'
    try:
      os.unlink(opts.socket_path)
    except OSError as e:
      if e.errno != errno.ENOENT:  # some error deleting it
        raise

    log('Binding to %s', opts.socket_path)
    sock.bind(opts.socket_path)

    # Listen for incoming connections
    try:
      sock.listen(1)
    except OSError as e:
      log('listen error: %s', e)

    # TODO: Should we MAINTAIN the connections?
    #
    # We don't need netstrings if the client opens and closes
    # every time?  But that's slower for coprocesses.
    #
    # A typical entry requires 3 commands: prompt, execute, and dump-state
    #   ECMD echo ${PS1@P}
    #   ECMD cd / 
    #   ECMD dump-state

    # Wait for a connection
    log('accept()')
    try:
      conn, client_address = sock.accept()
    except OSError as e:
      log("accept error: %s", e)
      # Uh what, you don't have to listen() here!  socketpair() is different?
      conn = sock
    else:
      log('Connection from %r', client_address)

  elif opts.socket_fd:
    fd = opts.socket_fd
    log('server.py got fd %d', fd)
    log('server.py descriptor state')
    os.system('ls -l /proc/%d/fd' % os.getpid())
    # This creates a NEW SOCKET, which is bad
    #sock = socket.fromfd(fd, socket.AF_UNIX, socket.SOCK_STREAM)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, fileno=fd)
    log('socket %s from FD %d', sock, fd)

    # Weird
    conn = sock

  else:
    raise AssertionError()


  try:
    while True:
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
