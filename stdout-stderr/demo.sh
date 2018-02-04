#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

prog() {
  seq 3 
  seq 4 6 >&2
  seq 7 9
}

filter() {
  $0 prog 2> >(awk '{print "e " $0 >> "/dev/stderr"; fflush(); }') > >(awk '{print "o " $0; fflush(); }') 
}

"$@"
