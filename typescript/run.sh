#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

download() {
  wget https://deno.land/x/install/install.sh
  chmod +x install.sh
}

# Puts it in $HOME/.deno/
# I prefer ~/install, but OK

deno() {
  ~/.deno/bin/deno "$@"
}

hi() {
  time deno run hi.ts
}

readonly NERD_FILES='header.ts lex.ts parse.ts transform.ts'

fmt() {
  deno fmt --single-quote $NERD_FILES tests.ts
}

lint() {
  deno lint \
    --rules-exclude='prefer-const,no-unreachable,no-unused-vars' \
    $NERD_FILES tests.ts
}

check-run() {
  local name=$1

  time deno check $name.ts

  echo --

  time deno run $name.ts
}

# https://matklad.github.io/2023/08/17/typescript-is-surprisingly-ok-for-compilers.html
matklad-test() {
  check-run matklad-test
}

bool-int-andy-test() {
  check-run bool-int-andy-test
}

tests() {
  check-run tests
}

count() {
  wc -l *.ts
  echo

  # The production code
  wc -l $NERD_FILES
}

"$@"
