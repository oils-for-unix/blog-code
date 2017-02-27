#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

f() {
  local x='local to f'
  g
}

g() {
  local y='local to g'
  h
}

h() {
  local z='local to h'
  echo $x - $y - $z
}

f
