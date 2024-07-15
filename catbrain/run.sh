#!/usr/bin/env bash
#
# catbrain tests
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

OILS_REPO=~/git/oilshell/oil

: ${LIB_OSH=$OILS_REPO/stdlib/osh}

source $LIB_OSH/task-five.sh
source $LIB_OSH/no-quotes.sh

test-hello() {
  ./catbrain.py -c 'w-line hi'
}

test-seq() {
  # Note: should this be allowed though?
  # It's not data dependent?
  # We shouldn't do anything proportional to integer size?
  # I think we can only GENERATE fixed sizes from seq!

  ./catbrain.py -c '
  load argv
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

  break  # disabled
}
'
}

test-argv-env() {
  # TODO: how to print json and commas?
  ./catbrain.py -c '
def json-lines {
  loop {
    encode json
    w-line
    if empty-stack {
      break
    }
  }
}

def sep {
  ch newline
  w
}

load argv
json-lines

sep
w-line --
sep

load env
json-lines

' 'foo bar' baz $(seq 9)
}

test-join() {
  ./catbrain.py -c '
array {
  const foo
  ch tab
  const bar
}
join

array {
  const 42
  ch tab
  const 43
}
join

pp stack

w-line
w-line
'
}

test-gen-tsv() {
  ./catbrain.py -c '
const size; ch tab; const path; join; w-line
loop {
  array { load counter; w; ch tab; const foo }
  join; w-line
  msleep 400
  array { load pid; w; ch tab; load now; }
  join; w-line
  msleep 200

  # For testing
  break
}
w-line done
'
}

test-log() {
  seq 3 | ./catbrain.py -c '
loop {
  log x
  r-line 
  if empty-string { break }
  w
}
'
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

test-capture-bad() {
  local status stdout

  nq-capture status stdout \
    ./catbrain.py -c 'capture foo'

  nq-assert 1 = $status

  nq-capture status stdout \
    ./catbrain.py -c 'capture { echo } a'

  nq-assert 1 = $status
}

test-capture() {
  ./catbrain.py -c '
#const foo
capture {
  w foo
  w bar
  const c
}
w-line
w-line
'
}

test-feed() {
  ./catbrain.py -c '
const foo
const stdin
feed {
  r 1
  r 1
}
# Same stack
w-line  # t
w-line  # s
w-line  # this is foo, because we dilost the rest of "stdin"
'
}

test-def() {
  ./catbrain.py -c '
def my-write {
  w-line
}

my-write foo
my-write bar
'

  ./catbrain.py -c '
def write2 {
  # This needs nested stacks
  #const 1; ch space; join;
  #const 2; ch space

  w 1
  ch space
  w  # write the space
  w-line

  w 2
  ch space
  w  # write space
  w-line
}

write2 eggs spam
'
}

test-eval() {
  ./catbrain.py -c '
eval {
  w-line a
  w-line b
}
'
}

test-pp() {
  # I'm not sure if pp $1 is valid
  ./catbrain.py -c '
const foo
const bar

pp top
pp top
'
}

test-nesting() {
  ./catbrain.py -c '
const extern
const-array ls /tmp

pp stack

gather
pp stack

const-array aa bb
pp stack

spread
pp stack

pop 2

spread
pp stack

encode json
pp top
'

}

test-array() {
  ./catbrain.py -c '
const mystr
array {
  const foo
  const bar
}
# pretty print the top value, no matter what it is
pp top

pp top

# error, because there is no way to pass array
#pp mystr
'

# there is no syntax to pass an array IMMEDIATE?   You have to build it on the
# stack first and then pass it/

# each "def" takes an array of args, each of which is EITHER a string or array?
# yeah it is a nested heap

# extern ls /tmp  # This one interprets it as an array though!
# extern

}

test-bad-args() {
  local status stdout

  nq-capture status stdout \
    ./catbrain.py -c 'eval foo'
  nq-assert 1 = "$status"

  return
  nq-capture status stdout \
    ./catbrain.py -c 'extern { w-line hi } '
  nq-assert 1 = "$status"

}

test-extern() {
  ./catbrain.py -c '
  array {
    const ls
    const /
  }
  pp top
  extern 
  '

  ./catbrain.py -c 'extern ls /'

  ./catbrain.py -c '
const-array ls /
extern
'

  ./catbrain.py -c '
array {
  const ls  
  ch space
  const _tmp
}
join  
sh
'
}

test-async() {
  # TODO: make this work with an EVENT LOOP, not a waitpid(-1) ?
  #
  # SIGCHLD will send a byte to a pipe, to wake up the loop

  # TODO: look at "waker" in Python

  # Lib/asyncio/unix_events.py has signal.set_wakeup_fd

  return

  ./catbrain.py -c '
fork { sleep 0.1 }
fork { sleep 0.2 }
wait
wait
'
}

all() {
  ~/git/oilshell/oil/bin/osh \
    ~/git/oilshell/oil/devtools/byo.sh test ./run.sh
}

task-five "$@"  
