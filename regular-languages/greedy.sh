#!/bin/bash
#
# Experiment: When is .*? necessary?
#
# Conjecture: almost nowhere in regular languages.  It's a performance
# optimization for backtracking engines.  You can trivially rewrite most
# regexes without it.
#
# By definition .* vs. .*? doesn't affect matching.  It only affects submatch
# extraction.  (e.g. the "recognition problem" vs. the "parse problem")
#
# Usage:
#   ./greedy.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

csv() {
  cat <<EOF
foo,bar
spam,eggs
EOF
}

html() {
  cat <<EOF
<div foo="bar>
</div>
EOF
}


demo() {
  csv | gawk 'match($0, "(.*),(.*)", a) { print "0=" a[0] "\t1=" a[1] "\t2=" a[2] }'

  echo ---

  html | gawk 'match($0, "<(.*)>", a) { print "0=" a[0] "\t1=" a[1] }'

  html | python2 -c '
import re, sys

pat = re.compile("<(.*)>")

for line in sys.stdin:
  m = pat.match(line)
  if m:
    print(m.groups())
'
}

survey() {
  local out=$PWD/survey.txt
  cd ~/git/oilshell/oil
  fgrep '.*?' */*.py | tee $out
}

"$@"
