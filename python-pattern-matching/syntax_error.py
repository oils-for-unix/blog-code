#!/usr/bin/env python2
"""
syntax_error.py
"""
from __future__ import print_function

import sys


def main(argv):
  # type: OOPS -> None

  # Hm Python 3.10's AST module doesn't validate this syntax.  It just returns
  # it as an opaque string.

  print('Hello from syntax_error.py')



if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
