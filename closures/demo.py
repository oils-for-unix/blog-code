#!/usr/bin/python3
"""
demo.py
"""

import sys


x = 1
def UseLocalBeforeAssigned():
  print(x)
  x = 2
  print(x)


# Using y from closing scope, but not mutating it.
# "Add" outlives MakeAdder.
def MakeAdder(y):
  def Add(x):
    return x + y
  return Add


# Mutating enclosing scope.
def MakeCounter():
  count = 0
  def Inc(x):
    # UnboundLocalError if this isn't here
    nonlocal count
    count += x
    return count
  return Inc


# Using x from enclosing scope.  But inner function doesn't outlive the outer.
def FilterDemo():
  x = 3
  mylist = range(5)

  f = filter(lambda item: item != x, mylist)
  return list(f)


def main(argv):
  try:
    UseLocalBeforeAssigned()
  except UnboundLocalError as e:
    print(e)

  print()

  add5 = MakeAdder(5)
  print(add5(1))  # 6
  print(add5(2))  # 7

  print()

  inc = MakeCounter()
  print(inc(3))
  print(inc(5))

  print()

  print(FilterDemo())


if __name__ == '__main__':
  main(sys.argv)
