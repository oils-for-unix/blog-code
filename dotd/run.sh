#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# https://www.gnu.org/software/make/manual/html_node/Automatic-Prerequisites.html

clean() {
  rm -v -f main.d main.d.mm main.o main
}

demo() {
  make 
  set +o errexit
  ./main
  echo "status: $?"
  echo

  echo "--- main.d.mm ---"
  cat main.d.mm
  echo

  echo "--- main.d ---"
  cat main.d
  echo

  clean
}

"$@"
