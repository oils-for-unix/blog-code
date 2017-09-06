#!/bin/bash
#
# Demonstrate issue with empty array and set -u.
#
# Tested with GNU bash, version 4.3.48(1)-release (x86_64-pc-linux-gnu)
#
# Usage:
#   ./demo.sh <function name>

declare -a empty=()
declare -a single=('')
declare -a double=('' '')
declare -a myarray=('a b' c)

set -o nounset  # important!

empty() {
  echo 1 "${empty[@]:-empty_or_unset}"

  # This works fine as long as you have double quotes.
  echo 2 "${single[@]:-empty_or_unset}"

  echo 3 "${double[@]:-empty_or_unset}"

  echo 4 "${myarray[@]:-empty_or_unset}"
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


# 8 chars + 4 chars + name of at least 1 char = 13+ chars
#
# It takes 13+ punctuation characters to correctly interpolate arrays in
# "strict mode"

good-interpolate() {
  # NOTES:
  # - Outer $ is unquoted
  # - Use + , not :+
  # - Inner $ is quoted

  # This is similar in form to ${1+"$@"}, but it works around a different
  # problem.
  #
  # https://unix.stackexchange.com/questions/68484/what-does-1-mean-in-a-shell-script-and-how-does-it-differ-from

  argv ${single+"${single[@]}"}
  argv ${double+"${double[@]}"}
  argv ${myarray+"${myarray[@]}"}

  argv ${empty+"${empty[@]}"}
}

"$@"
