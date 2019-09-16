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

"$@"
