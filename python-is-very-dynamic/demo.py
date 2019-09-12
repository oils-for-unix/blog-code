#!/usr/bin/env python3
"""
dyn.py
"""
from __future__ import print_function

import sys


class Unrelated(object):
  def m1(self):
    return "m1 unrelated"

  def m2(self):
    return "m2 unrelated"


class C(object):
  def m1(self):
    return "m1 C"

  def m2(self):
    return "m2 C"


class Sub(C):
  def m1(self):
    return "m1 Sub"


def main(argv):
  obj = Sub()
  print(obj.m1())
  print(obj.m2())
  print('---')

  print('Changed type of object:')
  obj.__class__ = C
  print(obj.m1())
  print(obj.m2())
  print('---')

  obj2 = Sub()
  print(obj2.m1())
  print(obj2.m2())
  print('---')

  print('Changed superclass of type:')
  Sub.__bases__ = (Unrelated,)
  print(obj2.m1())
  print(obj2.m2())


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
