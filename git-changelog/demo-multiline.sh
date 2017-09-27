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

count-nul() {
  # -o puts every match on its own line.  grep -o -c doesn't work.
  od -A n -t x1 | grep -o '00' | wc -l
}

test-count-nul() {
  python -c "print '\0x\0\0'" | count-nul
  python -c "print '\1'" | count-nul
}

git-log-html() {
  echo '<table cellpadding=5>'

  local num_fields=2  # 2 fields contain arbitrary text
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

  local num_entries=5
  git log -n $num_entries --pretty="format:$format" > tmp.bin

  local nul_count expected
  nul_count=$(count-nul < tmp.bin)
  expected=$(( num_entries * num_fields * 2 ))  

  if test "$nul_count" -ne "$expected"; then
    echo 1>&2 "Expected $expected NUL characters, got $nul_count"
    return 1
  fi

  # Writes HTML to stdout.
  escape-segments < tmp.bin

  echo '</table>'
}

write-file() {
  # NOTE: with -n 5 there is a slight race condition.
  git-log-html > git-log-multiline.html
  echo "Wrote git-log-multiline.html"
}

"$@"
