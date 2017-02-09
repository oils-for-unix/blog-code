#!/bin/bash
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

compare() {
  diff -u "$@" && echo 'PASSED'
}

pipe-both() {
  mkdir -p _tmp/
  local out=_tmp/stdout-stderr.txt

  # POSIX way
  ./stdout_stderr.py 2>&1 | tr A-Z a-z > $out

  compare $out - <<EOF
stderr
stdout
EOF

  # Special bash |& operator
  ./stdout_stderr.py |& tr A-Z a-z > $out
  compare $out - <<EOF
stderr
stdout
EOF
}
# oil:
# ./stdout_stderr.py |- tr A-Z a-z > $out

pipe-stderr() {
  mkdir -p _tmp/
  local out=_tmp/stderr.txt

  # must dup stderr to stdout first, and then stdout to /dev/null
  ./stdout_stderr.py 2>&1 >/dev/null | tr A-Z a-z > $out

  compare $out - <<EOF
stderr
EOF
}
#oil:
# ./stdout_stderr.py !2 > !1  >/dev/null | tr A-Z a-z > $out
# ./stdout_stderr.py !2 > !1  !1 > /dev/null | tr A-Z a-z > $out

"$@"
