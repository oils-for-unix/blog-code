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

edit-files() {
  #echo '#include "newdep.h"' >> defs.h

  # Override it
  #echo '#define EXIT_CODE 100' > newdep.h

  sed -i 's|/\*HERE\*/|#include "defs.h"|g' main.c
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

  git checkout main.c defs.h newdep.h  # revert it
  show-file main.c
  #show-file defs.h
  #show-file newdep.h

  make "$@"
  run-main

  show-file main.d.mm
  show-file main.d

  edit-files
  show-file main.c
  #show-file defs.h
  #show-file newdep.h

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

show-flag() {
  local flag=$1
  rm -f main.d
  # -M writes to stdout
  echo "... $flag ..."
  gcc $flag main.c
  echo
}

flags() {
  show-flag -M
  test -f main.d && { echo "Should not exist"; exit 1; }

  # -MD is equivalent to -M -MF file, except that -E is not implied.  -E means
  show-flag -MD
  show-file main.d

  show-flag -MMD
  show-file main.d
}

# Invoke the preprocessor directly
preprocessor-deps() {
  # How to write it to a file, but not preprocess?
  cpp main.c -M -MF my_custom_name.d
  show-file my_custom_name.d

  # Doesn't generate .o file
  gcc -c main.c -M -MF my_custom_name2.d
  show-file my_custom_name2.d
  #ls -l main.o

  # TODO: I don't think there's way to compile and generate .d to a custom name?  Two outputs?
}


"$@"
