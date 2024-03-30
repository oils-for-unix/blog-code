#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

what-is-wrong-with-this-rust-code() {
  rm -v -f PWNED

  #rm -r -f -v hidden/
  #./setup.sh make-dir

  ~/.cargo/bin/rustc main.rs

  # Run the program on a subtree
  ./main hidden/
}

reveal() {
  find hidden/
}

"$@"
