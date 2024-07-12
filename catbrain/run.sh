#!/usr/bin/env bash
#
# catbrain tests
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

test-hello() {
  ./catbrain.py -c 'w-line hi'
}

test-seq() {
  # Note: should this be allowed though?
  # It's not data dependent?
  # We shouldn't do anything proportional to integer size?
  # I think we can only GENERATE fixed sizes from seq!

  ./catbrain.py -c '
  state argv
  loop {
    dup
    w-line
    op dec
    if is-zero {
      break
    }
  }
  ' 5
}

test-cat() {
  seq 3 | ./catbrain.py -c '
loop {
  r-line
  if empty-string {
    break
  }
  w
} '
}

test-rotate() {
  ./catbrain.py -c '
 # does this push a new one?
loop {
  const abcdef

  # rotating based on counter is not that useful?
  # this is really a BINARY op of (string, number)
  op rotate

  w-line
  msleep 200
}
'
  
}

test-argv-env() {
  # TODO: how to print json and commas?
  ./catbrain.py -c '
state argv
loop {
  to-json
  w-line
  if empty-stack {
    break
  }
}

w-line --

state env

loop {
  to-json
  w-line
  if empty-stack {
    break
  }
}

' 'foo bar' baz 
}

test-gen-tsv() {
  ./catbrain.py -c '
const size; ch tab; const path; join; w-line
loop {
  state counter; w; ch tab; const foo; join; w-line
  msleep 400
  state pid; w; ch tab; state now; join; w-line
  msleep 200
}
w-line done
'
}

test-log() {
  seq 3 | ./catbrain.py -c 'loop { log x; r-line; w } '
}

test-exit() {
  set +o errexit
  ./catbrain.py -c 'w-line hi; exit 3'
  echo status=$?
}

test-cgi() {
  ./catbrain.py -c \
    "w-line 'Status: 200'
     w-line 'Content-Type: text/html; charset=utf-8'"
}

"$@"  
