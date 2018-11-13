#!/bin/bash

# symbols in OPT mode to see how bit it is
readonly CXXFLAGS='-std=c++11 -Wall -Wextra -g'
readonly DEBUG_FLAGS="$CXXFLAGS -fsanitize=address"
readonly OPT_FLAGS="$CXXFLAGS -O3"

pipe-pat() {
  python -c 'import sys;sys.stdout.write("|".join(sys.argv[1:]))' "$@"
}

words-pipe-pat() {
  python -c '
import sys
words = [ line.strip() for line in sys.argv[1:] ]
sys.stdout.write("|".join(words))
' "$@"
}

