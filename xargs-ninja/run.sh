#!/usr/bin/env bash
#
# Sample code for xargs blog post.

# https://www.oilshell.org/blog/2021/08/xargs.html
#
# Usage:
#   ./demo.sh <function name>
#
# Example:
#   ./demo.sh do_one
#   ./demo.sh do_all
#   ./demo.sh do_all_parallel

set -o nounset
set -o pipefail
set -o errexit

hello() {
  echo 'alice bob' | xargs -n 1 -- echo hi
}

gnu-demo() {
  seq 3 | xargs -I {} -- sh -c 'echo 0.$1; sleep 0.$1' dummy {}
  echo

  seq 5 | xargs -P 2 -I {} -- sh -c 'echo 0.$1; sleep 0.$1' dummy {}
  echo

  #return

  # This shows it calls wait4(-1, ...), which is waitpid(-1)
  # hm it also calls pipe2() every time, and fcntl?
  # why does it do that?  Yeah it reads from the pipe too

  # it reads(0, "1\n2\n3\n4\n5\n", ...) all at once
  # oh yes then I see the clone()
  # But every clone() has fnctl(4, F_SETFD, F_CLOEXEC) and pipe() and read()

  seq 5 | strace -- xargs -P 2 -I {} -- sh -c 'echo 0.$1; sleep 0.$1' dummy {}
}

my-demo() {
  seq 3 | ./xargs.py -I {} -- sh -c 'echo $1; sleep $1' dummy 0.{}
}

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
