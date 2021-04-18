#!/usr/bin/env python2
"""
netstring.py
"""
from __future__ import print_function

import array
import socket
import sys


def log(msg, *args):
  if args:
    msg = msg % args
  print(msg, file=sys.stderr)


def Encode(s):
  return b'%d:%s,' % (len(s), s)


def send(sock, msg, fds=None):
  fds = fds or []

  sock.send(b'%d:' % len(msg))  # netstring prefix

  # Send the FILE DESCRIPTOR with the NETSTRING PAYLOAD
  ancillary = (
    socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", fds)
  )
  result = sock.sendmsg([msg], [ancillary])
  log('sendmsg returned %s', result)

  sock.send(b',')  # trailing netstring thing


def recv_fds_once(sock, msglen, maxfds):
  """From Python docs"""

  fds = array.array("i")   # Array of ints
  msg, ancdata, flags, addr = sock.recvmsg(
     msglen, socket.CMSG_LEN(maxfds * fds.itemsize))
  for cmsg_level, cmsg_type, cmsg_data in ancdata:
    if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
      # Append data, ignoring any truncated integers at the end.
      fds.frombytes(cmsg_data[:len(cmsg_data) - (len(cmsg_data) % fds.itemsize)])
  return msg, list(fds)


def recv(sock):
  len_buf = []
  while True:
    byte = sock.recv(1)
    #log('byte = %r', byte)

    if len(byte) == 0:
      raise RuntimeError('Expected a netstring length byte')

    if byte == b':':
      break

    if b'0' <= byte and byte <= b'9':
      len_buf.append(byte)
    else:
      raise RuntimeError('Invalid netstring length byte %r' % byte)

  num_bytes = int(b''.join(len_buf))
  log('num_bytes = %d', num_bytes)

  # +1 for the comma
  n = num_bytes + 1

  msg = b''
  fd_list = []

  while True:
    chunk, fds = recv_fds_once(sock, n, 3)
    log("chunk %r  FDs %s", chunk, fds)

    fd_list.extend(fds)
    msg += chunk
    if len(msg) == n:
      break

  return msg, fd_list
