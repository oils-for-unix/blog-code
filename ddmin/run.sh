#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# The original code by Andreas Zeller (author of the paper) is mentioend here:
# https://lobste.rs/s/gone7a/celebration_code_6_pieces_code_had_impact

# (The shorter one inline didn't seem to run.)

download() {
  wget --no-clobber \
    https://www.st.cs.uni-saarland.de/whyprogramsfail/code/dd/ddmin.py \
    https://www.st.cs.uni-saarland.de/whyprogramsfail/code/dd/split.py \
    https://www.st.cs.uni-saarland.de/whyprogramsfail/code/dd/listsets.py
  chmod +x ddmin.py
}

count() {
  wc -l *.py
}

compare-output() {
  diff -u <(./ddmin.py) <(./my_ddmin.py) 
}

# Run with both Python 2 and Python 3.
smoke-test() {
  python2 my_ddmin.py
  python3 my_ddmin.py
}

"$@"
