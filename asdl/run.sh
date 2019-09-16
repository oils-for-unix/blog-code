#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

mult-inherit() {
  cc -o mult-inherit mult-inherit.cc
  ./mult-inherit
}

"$@"
