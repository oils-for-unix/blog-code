#!/usr/bin/python
"""
getopt_bug.py
"""
from __future__ import print_function

import getopt
import sys


def main(argv):
  n = int(argv[1])
  long_argv = ['-o', 'FOO'] * n
  opts, long_argv = getopt.getopt(long_argv, 'o:')
  print(len(opts))


if __name__ == '__main__':
  main(sys.argv)
