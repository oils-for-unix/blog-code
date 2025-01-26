#!/usr/bin/env bash

# CDX format
# https://commoncrawl.org/blog/announcing-the-common-crawl-index

index-paths() {
  wget --no-clobber \
    'http://data.commoncrawl.org/crawl-data/CC-MAIN-2024-51/cc-index.paths.gz'
}

random-index() {
  # 759 MB
  wget --no-clobber \
    'data.commoncrawl.org/cc-index/collections/CC-MAIN-2024-51/indexes/cdx-00016.gz'
}

# OK these are CSV files or whatever?

preview() {
  gzip -d < cdx-00016.gz  | head -n 100
}

"$@"
