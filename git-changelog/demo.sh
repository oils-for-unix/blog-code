#!/bin/bash
#
# Demo of git changelog in HTML.
#
# Usage:
#   ./demo.sh <function name>

escape-segments() {
  python -c '
import cgi, re, sys

print re.sub(
  r"\x01(.*)\x02", 
  lambda match: cgi.escape(match.group(1)),
  sys.stdin.read())
'
}

git-log-html() {
  echo '<table>'

  # - a trick for HTML escaping (avoid XSS): surround %s with unlikely bytes,
  #   0x01 and 0x02.  Then pipe Python to escape.
  local format=$'
  <tr>
    <td> <a href="https://github.com/oilshell/blog-code/commit/%H">%h</a> </td>
    <td>\x01%s\x02</td>
  </tr>'
  git log -n 5 --pretty="format:$format" | escape-segments

  echo '</table>'
}

# Remember: http://www.oilshell.org/blog/2017/08/12.html
#
# Avoid Directly Manipulating File Descriptors in Shell Scripts.
# - git-log-html is a function, and functions have their own stdout.

write-file() {
  git-log-html > git-log.html
  echo "Wrote git-log.html"
}

"$@"
