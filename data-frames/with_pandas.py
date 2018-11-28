#!/usr/bin/python3
"""
example.py
"""
import sys

import pandas as pd


def main(argv):
  traffic = pd.read_csv('traffic.csv')
  print(traffic)

  total_hits = sum(traffic.num_hits)
  print(total_hits)

  summary = traffic.groupby('url').apply(lambda x: sum(x.num_hits) / total_hits * 100.0)
  print(summary)


if __name__ == '__main__':
  main(sys.argv)
