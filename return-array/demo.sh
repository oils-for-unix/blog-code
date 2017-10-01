#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

argv() {
  python -c 'import sys;print sys.argv[1:]' "$@"
}

set-myarray() {
  myarray=('a b' $'c\nd')
}

set-array-var() {
  local name=$1
  # I think you need eval here
  name=('a b' $'c\nd')
}

main() {
  declare -a myarray
  declare -a otherarray
  set-myarray

  argv "${myarray[@]}"

  # Not sure how to do this:
  return
  set-array-var otherarray
  argv "${otherarray[@]}"
}

"$@"
