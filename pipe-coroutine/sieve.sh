#!/bin/bash
#
# From https://www.cs.dartmouth.edu/~doug/sieve/sieve.pdf
#
# Usage:
#   ./sieve.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

download() {
  wget http://www.cs.dartmouth.edu/~doug/sieve/sieve.bash
  wget http://www.cs.dartmouth.edu/~doug/sieve/sieve.c
}

src () {
  seq 2 100
}

cull() {
  while true; do
    read n
    (($n % $1 != 0)) && echo $n
  done
}

sink2() {
  read p
  echo $p

  # Ah this is recursive!
  cull $p | sink2 &
}

prog2() {
  src | sink2
}

#
# Program 3
#

die() {
  echo "$@" 1>&2
  exit 1
}

sink3() {
  read -u $primes pp
  while
    read p
    # Hm this fixes a bug?
    test -n "$p" || die "done"
    (($p < $pp * $pp))
  do
    echo $p
  done
  cull $pp | sink3 &
}

prog3() {
  rm -f fifo
  mkfifo fifo
  (echo 2; (src | sink3 {primes}<fifo)) | tee fifo
}

"$@"
