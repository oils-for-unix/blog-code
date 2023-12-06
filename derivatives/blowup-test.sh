#!/bin/bash
#
# Test for computational complexity.
#
# Workloads:
#
# - fgrep-problem: aaa|bbb|ccc|...    (N is the number of fixed words)
# - synthetic-rsc: a?a?a? ... aaa ... (N is the number of a? and a repetitions)
#   - https://swtch.com/~rsc/regexp/regexp1.html
#
# Targets:
#
# - epsilon engine (original one, and my refactored one)
# - rsc-regexp repo I forked from BurntSushi
#   - C from rsc
#   - multiple Rust impls from Burntsushi
#   - my Python implementation

set -o nounset
set -o pipefail
set -o errexit

# CPU seconds spent in user mode
TIMEFORMAT='    *** process user mode secs = %U'

repeat() {
  local s=$1
  local n=$2

  for i in $(seq $n); do
    echo -n "$s"
  done
}

#
# synthetic-rsc workload
#

rsc-pat() {
  local n=$1

  # a?^n a^n
  repeat 'a?' $n
  repeat 'a' $n
  echo
}

rsc-yes() {
  local n=$1
  repeat a $n
  echo
}

rsc-no() {
  local n=$1
  repeat a $(( n - 1 ))
  echo
}

rsc-demo() {
  rsc-pat 1
  rsc-pat 2
  rsc-pat 3
  echo

  echo 'YES NO'
  rsc-yes 3
  rsc-no 3
}

#
# fgrep-problem workload
#

make-words() {
  local n=$1
  mkdir -p data
  cp -v /usr/share/dict/words data/

  # Omit words with apostrophes
  fgrep -v "'" words | shuf -n $n > data/words-$n.txt
}

make-all-words() {
  make-words 10
  make-words 20
  make-words 30

  wc -l data/*
}

fgrep-pat() {
  local num_words=$1
  local word_len=${2:-10}

  python3 -c '
import sys
num_words = int(sys.argv[1])
word_len = int(sys.argv[2])

words = []
for i in range(num_words):
  letter = chr(ord("a") + i)
  words.append(letter * word_len)

print("|".join(words))
' $num_words $word_len
}

fgrep-yes() {
  # j is in the middle
  repeat j 10
  echo
}

fgrep-no() {
  repeat % 10
  echo
}

fgrep-demo() {
  fgrep-pat 10
  fgrep-pat 11
  fgrep-pat 12
  echo

  echo YES NO
  fgrep-yes
  fgrep-no
}

#
# Tools to run it against
#
# Contract: print the text if it matches pat

# ~/git/oilshell
REPO_DIR=../..

epsilon() {
  local pat=$1
  local text=$2

  pushd $REPO_DIR/epsilon > /dev/null
  python3 -m refactor.tool match "$@"
  popd > /dev/null
}

py-nfa() {
  local pat=$1
  local text=$2

  pushd $REPO_DIR/rsc-regexp > /dev/null
  py/nfa.py match "$@"
  popd > /dev/null
}

# C NFA, and Rust NFA

with-re2c() {
  local pat=$1
  local text=$2
}

matchers-demo() {
  local cmd=$1

  echo
  echo "--- Testing with $cmd"
  echo

  time $cmd 'a?' a
  time $cmd 'a?' b
}

all-matchers-demo() {
  matchers-demo epsilon
  matchers-demo py-nfa
}

"$@"
