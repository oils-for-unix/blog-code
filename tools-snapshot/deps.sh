#!/bin/bash
#
# Usage:
#   ./deps.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# Dependencies:
# - inotify-tools: for latch
# - markdown
#
# My own dependencies:
#
# ~/git/webpipe/install.sh - latch
# ~/hg/zoo - for snip.
# ~/hg/json-template - latch.py depends on this.  Gah.
#
# Probably also: dust repository.

install() {
  sudo apt-get install inotify-tools markdown python-pygments
}

download-cmark() {
  wget --directory _tmp \
    https://github.com/commonmark/cmark/archive/0.28.3.tar.gz
}

readonly CMARK_DIR=_tmp/cmark-0.28.3

build-cmark() {
  pushd $CMARK_DIR
  # GNU make calls cmake?
  make
  popd

  # Binaries are in build/src
}

test-install() {
  pushd $CMARK_DIR
  make test
  sudo make install
  popd
}

demo-cmark() {
  echo '*hi*' | cmark
}

"$@"
