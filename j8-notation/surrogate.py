#!/usr/bin/env python3
"""
surrogate.py

Using Python 3 API
"""
from __future__ import print_function

import json
import sys


def main(argv):
  ch = sys.argv[1]  # copy and paste Unicode emoji from browser to terminal
  print(ch)
  print(repr(ch))

  code_point = ord(ch[0])
  print(hex(code_point))

  u = code_point - 0x10000
  print(hex(u))

  w1 = u & 0b11111_11111
  w2 = (u & 0b11111_11111_00000_00000) >> 10

  print(w1)
  print(w2)

  first = 0xd800 + w2
  second = 0xdc00 + w1

  first_hex = hex(first)[2:]
  second_hex = hex(second)[2:]

  print(first_hex)
  print(second_hex)

  json_str = r'"\u%s\u%s"' % (first_hex, second_hex)
  print(json.loads(json_str))


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
