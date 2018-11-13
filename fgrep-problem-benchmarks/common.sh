#!/bin/bash

if test -n "$__INCLUDE__"; then
  return
fi
__INCLUDE__=1

# symbols in OPT mode to see how bit it is
readonly CXXFLAGS='-std=c++11 -Wall -Wextra -g'
readonly DEBUG_FLAGS="$CXXFLAGS -fsanitize=address"
readonly OPT_FLAGS="$CXXFLAGS -O3"

# For smaller benchmark
readonly KEYWORDS=(for while continue break if fi then else elif case esac do done)

