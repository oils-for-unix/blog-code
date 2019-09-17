#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# Naive solution
mult-inherit() {
  g++ -o mult-inherit mult-inherit.cc
  ./mult-inherit
}

# Tried to fix it but I don't understand what went wrong
virtual() {
  g++ -o virtual virtual.cc
  ./virtual
}

# After doing Python code gen
simple-mi() {
  g++ -o simple-mi simple-mi.cc
  ./simple-mi
}

# StackOverflow
so1() {
  g++ -std=c++11 -o so1 so1.cc
  ./so1
}

"$@"
