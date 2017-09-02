#!/usr/bin/python
"""
demo.py
"""

import os
import subprocess
import sys


class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y


# Are slots like a struct?
class PointStruct(object):
  __slots__ = ('x', 'y')

  def __init__(self, x, y):
    self.x = x
    self.y = y


def main(argv):
  p = Point(5, 10)
  ps = PointStruct(5, 10)

  #p.z = 99
  #ps.z = 99  # not allowed

  class_name = argv[1]
  n = int(argv[2])

  if class_name == 'Point':
    cls = Point
  elif class_name == 'PointStruct':
    cls = PointStruct
  else:
    raise AssertionError

  objs = []
  for i in xrange(n):
    o = cls(i, i*i)
    objs.append(o)

  print sys.getsizeof(p)
  print sys.getsizeof(ps)

  print len(objs)
  argv = ['grep', '^Vm', '/proc/%d/status' % os.getpid()]
  subprocess.call(argv)
  print 'DONE'


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print >>sys.stderr, 'FATAL: %s' % e
    sys.exit(1)
