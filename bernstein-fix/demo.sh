#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

argv() {
  python -c 'import sys; print sys.argv[1:]' "$@"
}

local() {
  # Test out some hard characters
  argv begin \' \" ' ' \\ end
}

argv-to-sh-demo() {
  ./argv_to_sh.py begin \' \" ' ' \\ end
}

ssh-demo() {
  ssh localhost $(./argv_to_sh.py echo begin \' \" ' ' \\ end)
  ssh localhost $(./argv_to_sh.py $PWD/$0 argv begin \' \" ' ' \\ end)
}


"$@"
