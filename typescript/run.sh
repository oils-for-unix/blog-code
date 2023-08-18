#!/bin/bash
#
# Usage:
#   ./deps.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

deno() {
  ~/.deno/bin/deno "$@"
}

hi() {
  time deno run hi.ts
}

# https://matklad.github.io/2023/08/17/typescript-is-surprisingly-ok-for-compilers.html
matklad() {
  time deno check matklad.ts

  echo --

  time deno run matklad.ts
}

"$@"
