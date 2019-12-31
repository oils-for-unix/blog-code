#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

LEFT='['
RIGHT=']'

gen() {
  echo BEGIN
  ls / | sort | head -n 3
  echo END
}

wrap() {
  while read line; do
    echo "$LEFT $line $RIGHT"
  done
}

gen | wrap | wrap
