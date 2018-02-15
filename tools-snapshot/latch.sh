#!/bin/bash
#
# Usage:
#   ./doc.sh <function name>
#
# How to serve docs:
#
# $ ./latch.sh notify-loop
# $ ./latch.sh serve
#
# NOTE: doc/index.md appears broken... I think there was some mapping logic in
# the server?

set -o nounset
set -o pipefail
set -o errexit

# Hook for latch to build
build-hook() {
  local in=$1
  local out=$2
  make $out
}

# Rebuild hook.  Assumes latch is installed.
notify-loop() {
  latch rebuild './latch.sh build-hook' *.md blog/2018/*/*.md
}

serve() {
  latch serve --root-dir _site
}

"$@"
