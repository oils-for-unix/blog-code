#!/bin/bash
#
# From https://www.cs.dartmouth.edu/~doug/sieve/sieve.pdf
#
# Usage:
#   ./sieve.sh <function name>

#set -o nounset
#set -o pipefail
#set -o errexit

log() {
  echo "$@" >&2
}

download() {
  wget --no-clobber \
    http://www.cs.dartmouth.edu/~doug/sieve/sieve.bash \
    http://www.cs.dartmouth.edu/~doug/sieve/sieve.c \
    https://golang.org/doc/play/sieve.go
}

src() {
  local end=${1:-100}
  seq 2 $end
}

cull() {
  while true; do
    read n || exit
    (($n % $1 != 0)) && echo $n
  done
}

sink2() {
  read p
  test -n "$p" || die "done"
  #log "P $p"

  echo $p

  # Ah this is recursive!
  cull $p | sink2 &
}

prog2() {
  src | sink2

  return
  # Hm this doesn't help?
  while true; do
    wait -n
    echo "wait => $?"
  done
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
    # Hm this fixes a bug?  Only for pipefail
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
  # Why is there an extra 2 here?  Weird.
  { echo 2; src | sink3 {primes}<fifo; } | tee fifo
}

#
# Is a Go port possible?
# We need a way to make a pipe.
#

filter() {
  local in=$1
  local out=$2
  local prime=$3

  while read i; do
    if (( i % prime != 0 )); then
      echo $i >& $out
    fi
  done <& $in
}

test-filter() {
  seq 20 | filter 0 1 3
}

go-port() {
  # ah crap, fd is 10 in another process!  Not in this shell
  # we can't access it
  #src 10 {fd}>&1  &  # go generate(ch)

  local n=10

  # We need a way do express this
  # Really it should be 

  # Well anything you can do with pipe(), you can do with mkfifo?

  # pipe :r :w
  # src $n >& $w
  for (( i = 0; i < 10; i++ )); do
    read -u $r :prime
    echo $prime
    pipe :r2 :w2

    filter $r $w2 $prime

    r=r2
    #w=r2
  done

  src $n &

  for i in $(seq $n); do
    #echo $i
    :
  done

  wait
  echo 'done'
}


#
# Ideas for Oil APIs:
#
# High level:
#
# make-pipeline :p
# for i in {1..3}; do
#   add-process :p -- filter $i
#
#   # or maybe
#   add --pipeline :p -- filter $i
# done
#
# $ repr p
# [Pipeline with 3 components]
#
# $ p   # invoke it like this?
# $ $p  # or like this?  It's not a string
# $ run p
# $ fork run p; wait   
# $ run .p 
# run(p)

#
# Tangent: annoys me to start a process for a loop
#
# for i in @seq(n) {
#   echo $i
# }
# problems: these are strings
#
# special case:
# for (i in 1..n) {
# }

# push-dup
#


"$@"

