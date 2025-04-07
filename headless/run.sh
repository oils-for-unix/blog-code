#!/usr/bin/env bash
#
# catbrain tests
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

OILS_REPO=~/git/oils-for-unix/oils

: ${LIB_OSH=$OILS_REPO/stdlib/osh}

source $LIB_OSH/task-five.sh
source $LIB_OSH/no-quotes.sh

make-venv() {
  python3 -m venv _tmp/venv
}

deps() {
  . _tmp/venv/bin/activate
  python3 -m pip install PyQt5
}

task-five "$@"  
