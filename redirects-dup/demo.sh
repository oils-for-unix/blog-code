#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

compare() {
  diff -u "$@" && echo 'PASSED'
}

pipe-both() {
  mkdir -p _tmp/
  local out=_tmp/stdout-stderr.txt

  # POSIX way
  ./stdout_stderr.py 2>&1 | tr A-Z a-z > $out

  compare $out - <<EOF
stderr
stdout
EOF

  # Special bash |& operator
  ./stdout_stderr.py |& tr A-Z a-z > $out
  compare $out - <<EOF
stderr
stdout
EOF
}
# oil:
# ./stdout_stderr.py |- tr A-Z a-z > $out

pipe-stderr() {
  mkdir -p _tmp/
  local out=_tmp/stderr.txt

  # must dup stderr to stdout first, and then stdout to /dev/null
  ./stdout_stderr.py 2>&1 >/dev/null | tr A-Z a-z > $out

  compare $out - <<EOF
stderr
EOF
}
#oil:
# ./stdout_stderr.py !2 > !1  >/dev/null | tr A-Z a-z > $out
# ./stdout_stderr.py !2 > !1  !1 > /dev/null | tr A-Z a-z > $out

# Maybe:
#
# ./stdout_stderr.py !2 | tr A-Z a-z > $out
# 
# But then what happens to stdout?

# http://stackoverflow.com/questions/2342826/how-to-pipe-stderr-and-not-stdout

pipe-stderr-keep-stdout() {
  mkdir -p _tmp/
  local out=_tmp/stderr.txt

  # must dup stderr to stdout first, and then stdout to /dev/null
  ./stdout_stderr.py 3>&1 1>&2 2>&3 | tr A-Z a-z > $out

  compare $out - <<EOF
stderr
EOF
}

process-subs() {
  mkdir -p _tmp/
  local out=_tmp/stdout.txt
  local err=_tmp/stderr.txt

  # must dup stderr to stdout first, and then stdout to /dev/null
  ./stdout_stderr.py > >(tr A-Z a-z > $out) 2> >(tr A-Z a-z > $err)

  compare $out - <<EOF
stdout
EOF
  compare $err - <<EOF
stderr
EOF
}

# oil:
# ./stdout_stderr.py !1 > $>[tr A-Z a-z > $out] !2 > $>[tr A-Z a-z > $err]

# TODO:
# - Make some graphviz diagrams of the descriptor table?

order-matters() {
  echo ---
  ./stdout_stderr.py >/dev/null 2>&1  # neither on console
  echo ---
  ./stdout_stderr.py 2>&1 >/dev/null  # STDERR on console
}

strace-order-matters() {
  echo ===
  strace -e open,dup2,fcntl sh -c './stdout_stderr.py >/dev/null 2>&1'
  echo ===
  strace -e open,dup2,fcntl sh -c './stdout_stderr.py 2>&1 >/dev/null'
}


"$@"
