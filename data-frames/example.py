#!/usr/bin/python3
"""
example.py
"""
import sys

import pandas as pd


def main(argv):
  d = {
      'date': pd.to_datetime(['2018-11-30', '2018-11-30', '2018-12-01', '2018-12-01']),
      'url':  ['/releases.html', '/blog/', '/releases.html', '/blog/'],
      'hits': [42, 1000, 84, 2000],
  }
  traffic = pd.DataFrame(data=d)
  print(traffic)
  print()
  books = traffic[traffic.url == '/blog/']
  print(books)
  print()

  print('Total traffic to /blog/ = %d' % sum(books.hits))


if __name__ == '__main__':
  main(sys.argv)
