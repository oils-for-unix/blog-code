#!/usr/bin/env bash

# CDX format
# https://commoncrawl.org/blog/announcing-the-common-crawl-index

index-paths() {
  # 302 different files
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
  local n=${1:-100}
  zcat cdx-00016.gz  | head -n $n
}

bench() {
  # 5.4 GB in 20 seconds
  time zcat cdx-00016.gz  | pv > /dev/null
}

count() {
  # 11.5 M lines?   1 URL per line
  #
  # So if there are all the same size, then that's 3.47 B URLs

  time zcat cdx-00016.gz | wc
}

json-to-url() {
  #jq -r '.offset .length .filename'
  jq -r '[.offset, .length, .filename] | @tsv' 
}

json() {
  # everything after the 3rd field
  shopt -s lastpipe
  preview 1 | cut -d ' ' -f 3- | json-to-url | read offset length filename

  # OK this works
  set -x
  curl -r "$offset-$((offset+length-1))" https://data.commoncrawl.org/$filename > page.gz
}

validate() {
  r=../../oils
  #echo $PWD/page.html | PYTHONPATH=$r:$r/vendor $r/data_lang/htm8_util.py  parse-htm8
  cat $PWD/page.html | PYTHONPATH=$r:$r/vendor $r/data_lang/htm8_util.py  tokens
}


"$@"
