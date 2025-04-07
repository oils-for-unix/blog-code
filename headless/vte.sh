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

deb-deps() {
  # For Debian/Ubuntu:
  sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-vte-2.91
}

task-five "$@"  
