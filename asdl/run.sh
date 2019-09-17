#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# Naive solution
mult-inherit() {
  cc -o mult-inherit mult-inherit.cc
  ./mult-inherit
}

# Tried to fix it but I don't understand what went wrong
virtual() {
  cc -o virtual virtual.cc
  ./virtual
}

# After doing Python code gen
simple-mi() {
  cc -std=c++11 -o simple-mi simple-mi.cc
  ./simple-mi
}

# StackOverflow
so1() {
  cc -std=c++11 -o so1 so1.cc
  ./so1
}

"$@"
