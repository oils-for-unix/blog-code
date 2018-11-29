#!/usr/bin/python3
"""
example.py
"""
import sys

import pandas as pd


def log(msg, *args):
  print()
  if args:
    msg = msg % args
  print('  ' + msg)


def main(argv):
  traffic = pd.read_csv('traffic.csv')
  log('Loaded:')
  print(traffic)

  total_hits = sum(traffic.num_hits)
  log('Total hits = %d', total_hits)

  daily = traffic.groupby('date').apply(lambda x: sum(x.num_hits))
  log('Daily Traffic:')
  print(daily)

  popular = traffic.groupby('url').apply(lambda x: sum(x.num_hits) / total_hits * 100.0)
  log('Popular Pages:')
  print(popular)


if __name__ == '__main__':
  main(sys.argv)
