#!/usr/bin/python
"""
words.py
"""
from __future__ import print_function

import sys


def main(argv):
  action = argv[1]
  words = [line.strip() for line in sys.stdin]

  if action in ('ripgrep', 're2', 'egrep'):  # | is alternation
    print('|'.join(words))

  elif action == 'fgrep':
    print('\n'.join(words))  # newline seprated file

  elif action == 'grep':  #\| is alternation
    print('\\|'.join(words))

  elif action == 're2c':
    quoted = ['"%s"' % w for w in words]
    print(" | ".join(quoted))

  else:
    raise RuntimeError('Invalid action %r' % action)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
