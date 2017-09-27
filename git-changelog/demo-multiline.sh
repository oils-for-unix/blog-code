#!/bin/bash
#
# A harder variant.
#
# Usage:
#   ./demo-multiline.sh <function>

set -o nounset
set -o pipefail
set -o errexit

escape-segments() {
  python -c '
import cgi, re, sys

print re.sub(
  r"\x00([^\x00]*)\x00", 
  lambda match: cgi.escape(match.group(1)),
  sys.stdin.read())
'
}

# nul check with od.  Point-free style.
check-nul() {
  # -A n: no addresses
  # -t x1: 1 byte hex addresses
  od -A n -t x1 | grep 00 
}

test-check-nul() {
  python -c "print '\0'" | check-nul && echo YES
  python -c "print '\1'" | check-nul || echo NO
}

git-log-html() {
  echo '<table cellpadding=5>'

  # - a trick for HTML escaping (avoid XSS): surround %s with unlikely bytes,
  #   0x01 and 0x02.  Then pipe Python to escape.
  local format='
  <tr>
    <td> <a href="https://github.com/oilshell/blog-code/commit/%H">%h</a> </td>
    <td> %ad </td>
    <td> %x00%an%x00 </td>
  </tr>
  <tr>
    <td></td>
    <td colspan=2><pre>%x00%B%x00</pre></td>
  </tr>
  '

  local plain='%H %ad %an %B'
  if git log --pretty="format:$plain" "$@" | check-nul; then
    echo 1>&2 "FATAL: git log contains NUL characters"
    return 1
  fi
  git log "$@" --pretty="format:$format" | escape-segments

  echo '</table>'
}

write-file() {
  # NOTE: with -n 5 there is a slight race condition.
  git-log-html -n 5 > git-log-multiline.html
  echo "Wrote git-log-multiline.html"
}

"$@"
