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

change-header() {
  echo '#include "newdep.h"' >> defs.h

  # Override it
  echo '#define EXIT_CODE 100' > newdep.h
}

run-main() {
  set +o errexit
  ./main
  echo "status: $?"
  echo
}

show-file() {
  local path=$1
  echo "--- $path ---"
  cat $path
  echo
}

demo() {
  clean

  git checkout defs.h newdep.h  # revert it
  show-file defs.h
  show-file newdep.h

  make "$@"
  run-main

  show-file main.d.mm
  show-file main.d

  change-header
  show-file defs.h
  show-file newdep.h

  make "$@"
  run-main

  show-file main.d.mm
  show-file main.d

  #clean
}

# Trying without the %.d rule.  This seems wrong on two counts:
# https://news.ycombinator.com/item?id=15061615
#
# Hm but it works?  

demo-short() {
  demo -f short.mk
}

"$@"
