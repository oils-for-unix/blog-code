#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

declare -a empty=()
declare -a single=('')
declare -a double=('' '')
declare -a myarray=('a b' c)

set -o nounset  # important!

empty() {
  echo 1 ${empty[@]:-empty_or_unset}

  # This is considered empty or unset, but shouldn't be.
  # Confusion between unset value and empty array.
  # I guess this is because of the equivalence between a[0] and a.
  echo 2 ${single[@]:-empty_or_unset}

  echo 3 ${double[@]:-empty_or_unset}

  echo 4 ${myarray[@]:-empty_or_unset}
}

# Everything works
length() {
  echo ${#empty[@]}
  echo ${#single[@]}
  echo ${#double[@]}
  echo ${#myarray[@]}
}

argv() {
  python -c 'import sys;print sys.argv[1:]' "$@"
}

bad-interpolate() {
  argv "${single[@]}"
  argv "${double[@]}"
  argv "${myarray[@]}"

  # This one crashes, but shouldn't.
  argv "${empty[@]}"
}

# This is similar in form to ${1+"$@"}, but it works around something
# different.
#
# https://unix.stackexchange.com/questions/68484/what-does-1-mean-in-a-shell-script-and-how-does-it-differ-from

good-interpolate() {
  argv ${single+"${single[@]}"}
  argv ${double+"${double[@]}"}
  argv ${myarray+"${myarray[@]}"}

  argv ${empty+"${empty[@]}"}
}

"$@"
