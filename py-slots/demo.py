#!/usr/bin/python
"""
demo.py
"""

import dis
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
class PointSlots(object):
  __slots__ = ('x', 'y')

  def __init__(self, x, y):
    self.x = x
    self.y = y


def Compute(points):
  total = 0
  # Test attribute access speed
  for p in points:
    total += p.x 
    total += p.y
  return total


class LPoint(object):
  def __init__(self, x, y):
    self.x01234567890123456789 = x
    self.y01234567890123456789 = y


def LCompute(points):
  total = 0
  # Test attribute access speed
  for p in points:
    total += p.x01234567890123456789
    total += p.y01234567890123456789
  return total


# Are slots like a struct?
class LPointSlots(object):
  __slots__ = ('x01234567890123456789', 'y01234567890123456789')

  def __init__(self, x, y):
    self.x01234567890123456789 = x
    self.y01234567890123456789 = y


def main(argv):
  #p = Point(5, 10)
  #ps = PointSlots(5, 10)
  #p.z = 99
  #ps.z = 99  # not allowed

  if argv[1] == 'dis':
    dis.dis(Compute)
    return

  class_name = argv[1]
  n = int(argv[2])

  if class_name == 'Point':
    cls = Point
    compute_func = Compute
  elif class_name == 'PointSlots':
    cls = PointSlots
    compute_func = Compute
  elif class_name == 'LPoint':
    cls = LPoint
    compute_func = LCompute
  elif class_name == 'LPointSlots':
    cls = LPointSlots
    compute_func = LCompute
  else:
    raise AssertionError

  print 'Creating %d %s instances...' % (n, class_name)
  points = []
  for i in xrange(n):
    o = cls(i, i)
    points.append(o)

  start_time = time.time()
  total = compute_func(points)
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
