#!/usr/bin/python
"""
demo.py
"""

import os
import subprocess
import sys
import timeit
import time


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


def Compute(points):
  total = 0
  # Test attribute access speed
  for p in points:
    total += p.x + p.y
  return total


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

  print 'Creating %d points...' % n
  points = []
  for i in xrange(n):
    o = cls(i, i)
    points.append(o)

  start_time = time.time()
  total = Compute(points)
  elapsed = time.time() - start_time
  print 'Computed %d from %d points in %.1f ms' % (total, n, elapsed * 1000)

  # Both 64?  getsizeof() isn't recursive
  #print sys.getsizeof(p)
  #print sys.getsizeof(ps)

  if os.getenv('SHOW_MEM'):
    pat = '^VmPeak'
    argv = ['grep', pat, '/proc/%d/status' % os.getpid()]
    subprocess.call(argv)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print >>sys.stderr, 'FATAL: %s' % e
    sys.exit(1)
