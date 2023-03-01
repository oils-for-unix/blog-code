#!/usr/bin/env bash
#
# Adapting https://fly.io/blog/docker-without-docker/
#
# Usage:
#   ./without-docker.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

download() {
  wget 'https://gist.githubusercontent.com/tqbf/10006fae0b81d7c7c93513890ff0cf08/raw/2b774ecf3b8cb8042fa87ab0d86a41175873201a/docker-pull.sh'
}

pull-alpine() {
  ./my-docker.sh pull-all alpine
  #oilshell/soil-dummy
}

show-layers() {
  local dir=${1:-golang}

  wc -l $dir/config.json

  # pretty print
  jq . < $dir/config.json

  for layer in $dir/*.tar.gz; do
    ls -l $layer
    echo

    { tar --list -z < $layer || true; } | head
    echo
  done
}

# Naming Quirk: 
#
# https://hub.docker.com/_/golang
#
# is library/golang in the API

# TODO: We also need uncompressed sizes.  Is there a way to get that other than
# untarring?

my-images() {
  local out=$PWD/_tmp/my-images.txt
  pushd ~/git/oilshell/oil
  deps/images.sh list-images | tee $out
  popd
}

fetch-mine() {
  while read task; do
    ./registry.sh fetch-manifest oilshell/soil-$task
  done < _tmp/my-images.txt
}

# TODO:
# - Pick out "config" field of manifest.json
# - Fetch that
# - And then it has all the comments
# - Make a TSV file
#   - image_id, tag, layer digest, layer size, created_at, created_by ?
# - and then you can find:
#   - total size of each image
#   - total size of all layers

sum-first-col() {
  awk '
      { sum += $1 }
  END { printf("%.1f MB\n", sum / 1000000) }
  '
}

my-sizes() {
  local task=${1:-dummy}

  #./my-docker.sh sizes library/alpine

  while read task; do

    echo $task

    #./registry.sh sizes _tmp/oilshell/soil-$task/manifest.json | commas
    # sum it
    ./registry.sh sizes _tmp/oilshell/soil-$task/manifest.json | sum-first-col

    echo
  done < _tmp/my-images.txt

  # Compressed sizes from registry
  #
  # dummy: 125 MB
  # dev-minimal: 328 MB

  # Uncompressed from docker inspect:
  #
  # dummy: 324 MB
  # dev-minimal: 754 MB
}

"$@"
