#!/usr/bin/python3
"""
without_data_frames.py
"""

import collections
import csv


def main():
  # Load it
  with open('traffic.csv') as f:
    reader = csv.reader(f)

    # Skip the title
    date, url, num_hits = reader.__next__()
    assert date == 'date' and url == 'url' and num_hits == 'num_hits', 'Invalid header row'

    # Sum hits by URL, and calculate the total number of hits.
    total_hits = 0
    by_url = collections.defaultdict(int)
    for date, url, num_hits in reader:
      num_hits = int(num_hits)
      by_url[url] += num_hits
      total_hits += num_hits

  # Print report.
  print('%20s %s' % ('url', 'percentage'))
  for url, num_hits in by_url.items():
    print('%20s %.2f' % (url, float(num_hits) / total_hits * 100.0))

  # TODO: Could sort these by percentage


if __name__ == '__main__':
  main()
