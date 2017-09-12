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


if __name__ == '__main__':
  main(sys.argv)
