#!/usr/bin/env bash
#
# Testing multiplexer
#
# Usage:
#   ./multi.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

make-venv() {
  python3 -m venv _tmp/multi-env
}

check-types() {
  # I installed mypy
  . _tmp/multi-env/bin/activate
  python3 -m mypy process-multiplexer.py
}

"$@"
