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

  daily = traffic.groupby('date').sum()
  log('Daily Traffic:')
  print(daily)

  total_hits = sum(traffic.num_hits)
  log('Total hits = %d', total_hits)

  # https://stackoverflow.com/questions/29802034/set-column-name-for-apply-result-over-groupby
  popular = (
      traffic.groupby('url')
      .apply(lambda x: sum(x.num_hits) / total_hits * 100.0)
      .reset_index(name='percentage')
      .sort_values(by='percentage', ascending=False)
  )

  log('Popular Pages:')
  print(popular)


if __name__ == '__main__':
  main(sys.argv)
