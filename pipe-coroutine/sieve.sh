#!/bin/bash
#
# From https://www.cs.dartmouth.edu/~doug/sieve/sieve.pdf
#
# Usage:
#   ./sieve.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

src () {
  seq 2 100
}

cull() {
  while true; do
    read n
    (($n % $1 != 0)) && echo $n
  done
}

sink() {
  read p
  echo $p
  cull $p | sink &
}

main() {
  src | sink
}

"$@"
