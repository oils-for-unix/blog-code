#!/usr/bin/env python2
"""
partition.py

Copy of

https://stackoverflow.com/questions/7938809/how-to-understand-the-dynamic-programming-solution-in-linear-partitioning
"""
from __future__ import print_function

import sys

from operator import itemgetter


def linear_partition(seq, k):
    if k <= 0:
        return []
    n = len(seq) - 1
    if k > n:
        return map(lambda x: [x], seq)
    table, solution = linear_partition_table(seq, k)
    k, ans = k-2, []
    while k >= 0:
        ans = [[seq[i] for i in xrange(solution[n-1][k]+1, n+1)]] + ans
        n, k = solution[n-1][k], k-1
    return [[seq[i] for i in xrange(0, n+1)]] + ans

def linear_partition_table(seq, k):
    n = len(seq)
    table = [[0] * k for x in xrange(n)]
    solution = [[0] * (k-1) for x in xrange(n-1)]
    for i in xrange(n):
        table[i][0] = seq[i] + (table[i-1][0] if i else 0)
    for j in xrange(k):
        table[0][j] = seq[0]
    for i in xrange(1, n):
        for j in xrange(1, k):
            table[i][j], solution[i-1][j-1] = min(
                ((max(table[x][j-1], table[i][0]-table[x][0]), x) for x in xrange(i)),
                key=itemgetter(0))
    return (table, solution)


def main(argv):
  k = int(argv[1])
  seq = [int(s) for s in argv[2:]]
  p = linear_partition(seq, k)
  print(p)
  print([sum(part) for part in p])
  print()


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
