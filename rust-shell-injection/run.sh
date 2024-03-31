#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# Prepare the exploit:
#
#   ./setup.sh make-dir

what-is-wrong-with-this-rust-code() {
  rm -v -f PWNED

  ~/.cargo/bin/rustc main.rs

  ./main
}


reveal() {
  find hidden/
}

"$@"
