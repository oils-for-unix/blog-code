#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

utf-8() {
  echo _____
  echo "$@"
  ./demo 'en_US.UTF-8' "$@"
}

demo() {
  cc -o demo demo.c

  utf-8 'abc'

  utf-8 $'\xE2\x98\xA0'  # encoded version
  utf-8 $'\u2620'

  # encoded version
  utf-8 $'\u007a'
  utf-8 $'\u03bb'
  utf-8 $'\u4e09'
  utf-8 $'\U0001f618'
}

"$@"
