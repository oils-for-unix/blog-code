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
  r"\x01([^\x02]*)\x02", 
  lambda match: cgi.escape(match.group(1)),
  sys.stdin.read())
'
}

git-log-html() {
  echo '<table cellpadding=5>'

  # - a trick for HTML escaping (avoid XSS): surround %s with unlikely bytes,
  #   0x01 and 0x02.  Then pipe Python to escape.
  local format=$'
  <tr>
    <td> <a href="https://github.com/oilshell/blog-code/commit/%H">%h</a> </td>
    <td> %ad </td>
    <td> \x01%an\x02 </td>
  </tr>
  <tr>
    <td></td>
    <td colspan=2><pre>\x01%B\x02</pre></td>
  </tr>
  '
  git log -n 5 --pretty="format:$format" | escape-segments

  echo '</table>'
}

write-file() {
  git-log-html > git-log-multiline.html
  echo "Wrote git-log-multiline.html"
}

"$@"
