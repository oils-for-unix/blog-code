#!/usr/bin/env python3
"""
typed.py
"""
from __future__ import print_function

import sys

from dataclasses import dataclass
from typing import Union, List


# Example from
# https://www.pyret.org/index.html

# tree =
# | Leaf()
# | Node(value int,  a tree, b tree)
#

@dataclass(frozen=True)
class Leaf:
  pass


# The dataclass adds a constructor
@dataclass(frozen=True)
class Node:
  value: int
  # I think Python 3.11 will have delayed evaluation of annotations
  a: 'tree'
  b: 'tree'


tree = Union[Leaf, Node]


def TreeSum(t: tree) -> int:
  match t:
    case Leaf():
      return 0
    case Node(value, left, right):
      return value + TreeSum(left) + TreeSum(right)


def main(argv: List[str]) -> None:
  print('Hello from typed.py')

  leaf = Leaf()
  print(TreeSum(leaf))
  node4 = Node(4, leaf, leaf)
  t = Node(5, node4, leaf)
  print(TreeSum(t))


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
