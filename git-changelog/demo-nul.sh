#!/bin/bash
#
# Alternative solution using pairs of %x00, which is specific to git.
#
# Usage:
#   ./demo-nul.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

escape-segments0() {
  python -c '
import cgi, re, sys

print re.sub(
  r"\x00(.*)\x00", 
  lambda match: cgi.escape(match.group(1)),
  sys.stdin.read())
'
}

git-log-html0() {
  echo '<table>'

  # - a trick for HTML escaping (avoid XSS): surround %s with unlikely bytes,
  #   0x01 and 0x02.  Then pipe Python to escape.
  local format='
  <tr>
    <td> <a href="https://github.com/oilshell/blog-code/commit/%H">%h</a> </td>
    <td>%x00%s%x00</td>
  </tr>'
  git log -n 5 --pretty="format:$format" | escape-segments0

  echo '</table>'
}

write-file0() {
  git-log-html0 > git-log0.html
  echo "Wrote git-log0.html"
}

"$@"
