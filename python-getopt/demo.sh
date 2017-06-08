#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

main() {
  for i in 5000 10000 15000 20000; do
    time ./getopt_quadratic.py $i
  done
}

main "$@"
