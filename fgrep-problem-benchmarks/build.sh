#!/bin/bash
#
# Usage:
#   ./setup.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

source common.sh

download-re2() {
  mkdir -p _deps
  wget --directory _deps \
    https://github.com/google/re2/archive/2018-10-01.tar.gz
}

readonly RE2_DIR=_deps/re2-2018-10-01

# Easy to build.
# NOTE: Depends on C++ 11 atomic.
build-re2() {
  pushd $RE2_DIR
  make
  make test
  popd
}

link-re2() {
  ln -s -f --verbose $(basename $RE2_DIR) _deps/re2
}

# Why does it require threads?
re2-grep() {
  g++ $OPT_FLAGS \
    -o _tmp/re2_grep \
    re2_grep.cc \
    -I _deps/re2 \
    -L _deps/re2/obj -l re2 \
    -l pthread

  #_tmp/re2_grep
}



"$@"
