#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

demo() {
  for k in $(seq 5); do
    seq 10 | xargs ./partition.py $k
  done

  echo -----

  for k in $(seq 5); do
    seq 5 15 | xargs ./partition.py $k
  done
}

# Hm it doesn't seem to have a quadratic explosion?
n-scale() {
  for n in $(seq 1000 100 2000); do
    echo $n
    time seq $n | xargs ./partition.py 10
  done
}

# ditto, seems linear
k-scale() {
  for k in $(seq 10 10 100); do
    echo $k
    time seq 1000 | xargs ./partition.py $k
  done
}


"$@"
