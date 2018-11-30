#!/usr/bin/python3
"""
without_data_frames.py
"""

import collections
import csv


def log(msg, *args):
  print()
  if args:
    msg = msg % args
  print('  ' + msg)


def main():
  # Load data
  with open('traffic.csv') as f:
    reader = csv.reader(f)

    # Skip the title
    date, url, num_hits = reader.__next__()
    assert date == 'date' and url == 'url' and num_hits == 'num_hits', 'Invalid header row'

    # Compute two "group by" dictionaries, and the total number of hits.
    by_url = collections.defaultdict(int)
    by_date = collections.defaultdict(int)
    total_hits = 0

    for date, url, num_hits in reader:
      num_hits = int(num_hits)
      by_date[date] += num_hits
      by_url[url] += num_hits
      total_hits += num_hits

  log('Daily Traffic:')
  print('%20s %s' % ('date', 'num_hits'))
  daily = sorted(by_date.items())  # sort by date
  for date, num_hits in daily:
    print('%20s %d' % (date, num_hits))

  log('Popular Pages:')
  print('%20s %s' % ('url', 'percentage'))
  popular = sorted(by_url.items(), key=lambda x: x[1], reverse=True)
  for url, num_hits in popular:
    print('%20s %.2f' % (url, float(num_hits) / total_hits * 100.0))


if __name__ == '__main__':
  main()
