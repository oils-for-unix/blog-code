#!/bin/bash

# symbols in OPT mode to see how bit it is
readonly CXXFLAGS='-std=c++11 -Wall -Wextra -g'
readonly DEBUG_FLAGS="$CXXFLAGS -fsanitize=address"
readonly OPT_FLAGS="$CXXFLAGS -O3"
