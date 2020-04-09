#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

coroutine() {
  seq 40 |
  while read n; do 
    if (( n % 2 == 0 )); then
      echo $n;
    fi
  done |
  while read n; do 
    if (( n % 3 == 0 )); then
      echo $n;
    fi
  done |
  tac

}

"$@"
