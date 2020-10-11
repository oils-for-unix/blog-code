#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

commandsub() {
  echo $(false)
  echo status=$?
}

assign() {
  local foo
  foo=$(false)
  echo status=$?
}

# subshell
# https://news.ycombinator.com/item?id=24738274

SH=${SH:-bash}

subshell-compare() {
  set +o errexit

  $SH -c 'set -e;  false && true ; echo hi'

  echo '--- subshell changes behavior --- '
  $SH -c 'set -e; (false && true); echo hi'
}

# function
# https://news.ycombinator.com/item?id=24740842

func-compare() {
  set +o errexit

  $SH -c 'set -e; false && true ; echo hi'

  echo '--- function changes behavior --- '

  $SH -c '
f() {
  false && true
}
set -e; f; echo hi
'

}

"$@"
