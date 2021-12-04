#!/usr/bin/env bash
#
# Usage:
#   ./bwrap.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

show() {
  # wow this is tiny, only 51K
  ls -l $(which bwrap)

  # links against libselinux
  ldd $(which bwrap)
}

deps() {
  # not mentioned in the README !!!
  # needed for ./configure from the tarball
  sudo apt install libcap-dev
}

bwrap() {
  _deps/bubblewrap-0.5.0/bwrap "$@"
}

demo() {
  #bwrap --ro-bind /usr /usr bash

  # hm this thing from the demo doesn't work
  bwrap --ro-bind /usr /usr --symlink usr/lib64 /lib64 --proc /proc --dev /dev --unshare-pid bash

  # also demos/bubblewrap-shell.sh in the repo doesn't work?
  # also where are the instructions to build?  I guess you need a tarbal
}

"$@"
