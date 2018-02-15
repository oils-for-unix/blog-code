#!/bin/bash
#
# Usage:
#   ./build.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

log() {
  echo "$@" >&2
}

snip-and-markdown() {
  local in=$1
  local out=$2

  #log "*** Building $in -> $out"

  < $in  \
    snip --script ./Snip - |
    ./cmark.py |
    sed -e 's|<pre><code>|<pre>|g' -e 's|</code></pre>|</pre>|g' \
    > $out
  echo "Wrote $out"
}

_link() {
  ln --verbose --no-target-directory -s -f "$@"
}

make-links() {
  # _site is already a symlink to oilshell.org
  _link ../oilshell.org__deploy _site 
  _link $PWD/analytics/static ../oilshell.org__deploy/analytics
  _link $PWD/analytics/_data ../oilshell.org__deploy/analytics-data
}

# TODO: This should probably go in the Makefile
make-dirs() {
  mkdir -v -p {_tmp/,_site/,}blog/2016/{10,11,12}
  mkdir -v -p {_tmp/,_site/,}blog/2017/{01,02,03,04,05,06,07,08,09,10,11,12}
  mkdir -v -p {_tmp/,_site/,}blog/2018/{01,02}
}

# One time thing: Create pygments CSS.
pygments-css() {
  #local style=vs  # vs is minimal.  doesn't have italics for comments.
  #local style=tango  # operators too noisy.

  #local style=colorful  # string has clashing background
  #local style=native  # doesn't work with grey
  #local style=murphy  # string has clashing background

  #local style=pastie  # char literals too strong, not bad?

  #local style=borland  # boring, too blue like links
  #local style=vim  # garish
  local style=friendly  # operators not emphasized enough.

  pygmentize -S $style -f html > css/code.css
}

"$@"
