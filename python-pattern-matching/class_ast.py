#!/usr/bin/env python3
"""
dataclass_ast.py

Run with Python 3.10
"""
from __future__ import print_function

import sys

from dataclasses import dataclass
from typing import Union

class BinOp:
  # Without this, we get TypeError on 'case BinOp': BinOp accepts 0 positional subpatterns
  __match_args__ = ('left', 'op', 'right')

  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.right = right

  def __repr__(self):
    return 'BinOp(%s, %s, %s)' % (self.left, self.op, self.right)


class Constant:
  __match_args__ = ('value',)

  def __init__(self, value: int):
    self.value = value

  def __repr__(self):
    return 'Constant(%d)' % self.value


class Add:
  def __repr__(self):
    return 'Add()'


class Sub:
  def __repr__(self):
    return 'Sub()'


Expr = Union[BinOp, Constant]

Op = Union[Add, Sub]


# This one is superficially different than in the paper!
#
# Hm this depends on __match_args__ ?  Is it set in the ast module nodes?

def simplify(node):
  match node:
    case BinOp(Constant(left), Add(), Constant(right)):
      return Constant(left + right)
    case _:
      return node


def main(argv):
  expr = BinOp(Constant(3), Add(), Constant(4))
  print(expr)
  opt = simplify(expr)
  print('     => optimized')
  print(opt)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
