#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# TODO:
# - find example
# - chroot example


parallel-each() {
  xargs -P 4 -n 1 -- $0 "$@"
}

# Some expensive thing
sleep-hello() {
  local seconds=$1
  echo "hello for $seconds"
  sleep $seconds
}

peach-demo() {
  time echo '0.1 0.2 0.3' | parallel-each sleep-hello
}

"$@"
