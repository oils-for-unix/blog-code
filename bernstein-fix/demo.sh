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
  ./argv_to_sh.py begin \' \" 'a b' \\ end
}

quote-demo() {
  # Wrong because 'a b' gets split.
  argv $(./argv_to_sh.py echo begin \' \" 'a b' \\ end)

  # Quoting makes it correct.  SSH doesn't care, because it must join the rest
  # of the args, which is weird.
  #
  # I think the point of the weird SSH command syntax is to do remote
  # evaluation of vars?  Yes try ssh HOST 'echo' '$HOME'.
  #
  # What about su?  I guess it can also do evaluation of vars in the other
  # user's environment.
  #
  # Will there be a pattern in oil for this?

  argv "$(./argv_to_sh.py echo begin \' \" 'a b' \\ end)"
}

ssh-demo() {

  ssh localhost "$(./argv_to_sh.py echo begin \' \" 'a b' \\ end)"
  ssh localhost "$(./argv_to_sh.py $PWD/$0 argv begin \' \" 'a b' \\ end)"
}


"$@"
