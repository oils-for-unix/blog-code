#!/bin/bash
#
# Usage:
#   ./challenge2.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# Print a message to stderr
log() {
  echo "$@" >&2
}

escape-html() {
  sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'
}

git-log() {
  echo '<pre>'
  log "Running git"
  git log -n 1 | escape-html
  log "Done running git"
  echo '</pre>'
}

main() {
  log ""
  log "*** Count output lines"
  git-log | wc -l

  log ""
  log "*** Write output to file"
  git-log > out.html

  log ""
  log "*** Write output to file and log to file"
  git-log > out2.html 2> log.txt

  log ""
  log "*** Test"
  head -n 5 out.html out2.html log.txt
}

"$@"
