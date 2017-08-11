#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# from https://github.com/NixOS/nixpkgs/blob/master/pkgs/stdenv/generic/setup.sh#L318

# Return success if the specified file is an ELF object.
isELF() {
    local fn="$1"
    local fd
    local magic
    exec {fd}< "$fn"
    read -r -n 4 -u "$fd" magic
    exec {fd}<&-
    if [[ "$magic" =~ ELF ]]; then return 0; else return 1; fi
}

# My simpler rewrite.
isElfSimple() {
  local path=$1  # double quotes never necessary on RHS
  local magic

  # read 4 bytes from $path, without escaping, into $magic var
  read -r -n 4 magic < "$path"

  # Return the exit code of [[
  [[ "$magic" =~ ELF ]]
}

compareIsElf() {
  local path=$1
  isELF "$path" && echo "YES isELF $path" || echo "NO isELF $path"
  isElfSimple "$path" && echo "YES isElfSimple $path" || echo "NO isElfSimple $path"
}

testIsElf() {
  for path in /bin/sh /bin/true $0; do
    compareIsElf "$path"
    echo
  done
}

"$@"
