#!/bin/bash
#
# Problems:
# - Shell and awk should be combined
# - Shell needs escaping.  If they weren't combined, they BOTH would need
# escaping.
#
# Usage:
#   ./demo.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# Point-free function
hist() {
  sort | uniq -c | sort -r -n
}

hist-demo() {
  { echo foo; echo bar; echo foo; } | hist
}

# NOTE: not safe
awk-html-rows() {
  awk '
    BEGIN { print "<tr> <td>Count</td> <td>Name</td> </tr>"}
          { print "<tr> <td>" $1 "</td> <td>" $2 "</td> </tr>"}
  '
}

hist-pipeline-demo() {
  { echo foo; echo bar; echo foo; } | hist | awk-html-rows
}

shell-html-rows() {
  echo "<tr> <td>Count</td> <td>Name</td> </tr>"
  while read count name; do
    echo "<tr> <td>$count</td> <td>$name</td> </tr>"
  done
}

while-pipeline-demo() {
  { echo foo; echo bar; echo foo; } | hist | shell-html-rows
}

inline-demo() {
  { echo foo; echo bar; echo foo; } | 
  sort | uniq -c | sort -r -n       |
  { echo "<tr> <td>Count</td> <td>Name</td> </tr>";
    while read count name; do
      echo "<tr> <td>$count</td> <td>$name</td> </tr>"
    done
  }
}


"$@"
