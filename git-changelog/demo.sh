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
  r"\x00(.*)\x01", 
  lambda match: cgi.escape(match.group(1)),
  sys.stdin.read())
'
}

git-log-html() {
  cat <<EOF
<!DOCTYPE html>
<html>
  <head>
    <title>Git Log</title>
  </head>
  <body>
    <h1>Git Log</h1>
    <table width="100%">
EOF

  # - a trick for HTML escaping (avoid XSS): surround %s with unlikely bytes,
  #   \x00 and \x01.  Then pipe Python to escape.
  local format='
  <tr>
    <td><a href="https://github.com/oilshell/blog-code/commit/%H">%h</a> </td>
    <td class="subject">%x00%s%x01</td>
  </tr>'
  git log -n 3 --pretty="format:$format" | escape-segments

  cat <<EOF
    </table>
  </body>
</html>
EOF
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
