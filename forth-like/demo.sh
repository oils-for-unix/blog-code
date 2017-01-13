#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

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

hello-sleep() {
  echo hello
  sleep $1
}

retry-demo() {
  retry 5 hello-sleep 0.1
}

timeout-retry-demo() {
  timeout 0.3 $0 retry 5 hello-sleep 0.1
}

"$@"
