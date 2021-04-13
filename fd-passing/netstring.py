#!/usr/bin/env python2
"""
netstring.py
"""
from __future__ import print_function

import sys


def log(msg, *args):
  if args:
    msg = msg % args
  print(msg, file=sys.stderr)


def Encode(s):
  return b'%d:%s,' % (len(s), s)


def Receive(connection):
  len_buf = []
  while True:
    byte = connection.recv(1)
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
  #log('num_bytes = %d', num_bytes)

  data, ancdata, msg_flags, address = connection.recvmsg(16)
  log("recvmsg = %r %r %r %r", data, ancdata, msg_flags, address)

  return data, ancdata
