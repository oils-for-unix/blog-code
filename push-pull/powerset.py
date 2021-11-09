#!/usr/bin/env python3
"""
powerset.py
"""
from __future__ import print_function

import sys

# Transcribing Rust code from
# https://lobste.rs/s/khbbac/generate_all_things#c_xflsh6

def push_powerset(acc, n):
  if n == 0:
    print(acc)
  else:
    acc.append(True)
    push_powerset(acc, n-1)
    acc.pop()

    acc.append(False)
    push_powerset(acc, n-1)
    acc.pop()


def pull_powerset(n):
  if n == 0:
    yield []
  else:
    for x in pull_powerset(n-1):
      yield [True] + x

    for x in pull_powerset(n-1):
      yield [False] + x


def main(argv):
  print()
  print('PUSH STYLE')
  print()
  push_powerset([], 3)

  print()
  print('PULL STYLE')

  # FLATTENED API
  for t in pull_powerset(3):
    print(t)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
