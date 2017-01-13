#!/bin/bash
#
# Usage:
#   ./t.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

retry() {
  local n=$1
  shift
  for i in $(seq $n); do
    "$@"
  done
}

sleep-echo() {
  echo hello
  sleep 0.1
}

retry-demo() {
  retry 5 sleep-echo
}

timeout-demo() {
  timeout 0.3 $0 retry 5 sleep-echo
}

"$@"
