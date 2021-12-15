#!/usr/bin/env python3
"""
dataclass_ast.py

Run with Python 3.10
"""
from __future__ import print_function

import sys

from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class BinOp:
  left: 'Expr'
  op: 'Op'
  right: 'Expr'

@dataclass(frozen=True)
class UnaryOp:
  op: 'Op'
  child: 'Expr'

@dataclass(frozen=True)
class Constant:
  value: int

@dataclass(frozen=True)
class Add:
  pass

@dataclass(frozen=True)
class Sub:
  pass

@dataclass(frozen=True)
class USub:
  pass

Expr = Union[BinOp, UnaryOp, Constant]

Op = Union[Add, Sub, USub]


# This one is superficially different than in the paper!
#
# Hm this depends on __match_args__ ?  Is it set in the ast module nodes?

def simplify(node):
  match node:
    case BinOp(Constant(left), Add(), Constant(right)):
      return Constant(left + right)
    case BinOp(left, Add() | Sub(), Constant(0)):
      return simplify(left)
    case UnaryOp(USub(), UnaryOp(USub(), item)):
      return simplify(item)
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
