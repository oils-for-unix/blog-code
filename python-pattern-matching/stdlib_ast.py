#!/usr/bin/env python3
"""
demo.py

Run with Python 3.10
"""
from __future__ import print_function

import sys
import ast
from ast import expr, Expr, BinOp, UnaryOp, Constant, Add, Sub, USub

from typing import cast

# https://gvanrossum.github.io/docs/PyPatternMatching.pdf

def fact(arg) -> int:
  match arg:
    case 0 | 1:
      f = 1
    case n:
      f = n * fact(n - 1)
  return f


def mysum(seq) -> int:
  match seq:
    case []:
      s: int = 0
    case [head, *tail]:
      s = head + mysum(tail)
  return s


# This one is superficially different than in the paper!
#
# Hm this depends on __match_args__ ?  Is it set in the ast module nodes?

def simplify(node) -> expr:
  match node:
    case BinOp(Constant(left), Add(), Constant(right)):
      return Constant(left + right)
    case BinOp(left, Add() | Sub(), Constant(0)):
      return simplify(left)
    case UnaryOp(USub(), UnaryOp(USub(), item)):
      return simplify(item)
    case _:
      return node


def main(argv) -> None:
  print('Hello from demo.py')

  print(fact(6))

  print(mysum([1, 2, 3]))

  # Test out all the optimizations
  for code_str in ['3 + 4', '3 - 0', '- - 5']:
    print('   %s' % code_str)

    module = ast.parse(code_str)
    print(ast.dump(module))

    # unwrap the expression
    stmt = module.body[0]
    e = cast(Expr, stmt).value

    print('   AST')
    print(ast.dump(e))

    opt = simplify(e)

    print()
    print(' => optimized')
    print(opt)
    print(ast.dump(opt))

    print('-----')


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
