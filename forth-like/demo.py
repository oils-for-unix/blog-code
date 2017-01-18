#!/usr/bin/python
"""
demo.py -- Experimenting with expressing this forth-like pattern in Python.

It appears it can be done with varargs and splatting.
"""

import sys
import time


def retry(n, f, *args):
  for i in range(n):
    f(*args)


def hello_sleep(t):
  print 'hello'
  time.sleep(t)


def retry_demo():
  retry(5, hello_sleep, 0.1)


def timeout(seconds, f, *a):
  # TODO: Set SIGALARM or something
  print 'Running %s with args %s with timeout of %f' % (f, a, seconds)
  f(*a)


def timeout_retry_demo():
  timeout(0.3, retry, 5, hello_sleep, 0.1)


def main(_):
  hello_sleep(0.1)
  print('--')
  retry_demo()

  print('--')
  timeout_retry_demo()


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print >>sys.stderr, 'FATAL: %s' % e
    sys.exit(1)
