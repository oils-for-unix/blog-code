#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

readonly BASH_DIR=~/src/languages/bash-4.4

bash-files() {
  find $BASH_DIR \
    \( -name 'y.tab.c' -a -prune \) -o \
    \( -name 'readline' -a -prune \) -o \
    \( -name parse.y -a -print \) -o \
    \( -name '*.[ch]' -a -print \)
}

readline-files() {
  find $BASH_DIR/lib/readline \
    \( -name '*.[ch]' -a -print \)
}

significant() {
  # 87K sloccount
  # 88K cloc
  bash-files | xargs cloc
  echo

  # 24K sloccount and cloc
  readline-files | xargs cloc
  echo
}

physical() {
  # 124K raw lines
  bash-files | xargs wc -l | sort -n | tail -n 20
  echo

  # 35K raw lines
  readline-files | xargs wc -l | sort -n | tail
  echo
}

"$@"
