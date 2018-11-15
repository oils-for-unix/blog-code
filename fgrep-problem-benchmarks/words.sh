#!/bin/bash
#
# Usage:
#   ./words.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

readonly WORDS=/usr/share/dict/words
readonly FILTERED=_tmp/filtered.txt

export LC_ALL=C

many-words-pipe-pat() {
  readarray SAMPLED < _tmp/sampled.txt

  words-pipe-pat "${SAMPLED[@]}"
}

many-words-re2c-pat() {
  readarray SAMPLED < _tmp/sampled.txt
  re2c-pat "${SAMPLED[@]}"
}

# pipe-pat defined in common.sh

egrep-dash-e-argv() {
  # NOTE: only supports argv without spaces.  readarray could help
  python -c '
import sys
for arg in sys.argv[1:]:
  print("-e")
  print(arg)
' "${KEYWORDS[@]}"
}

# Use a special marker in the code
update-re2c-keywords() {
  local file=$1
  local pat="$(./make_pat.py re2c < $file)"
  sed -i "s;.*__TO_REPLACE__.*;      $pat  // __TO_REPLACE__ ;g" fixed-strings.re2c.cc
}

prune() {
  wc -l $WORDS

  # Select words of at least length 4, because I think 1 length patterns cause
  # too much short-circuiting in the benchmarks.

  egrep '^[a-zA-Z0-9-]{4,}$' $WORDS | wc -l

  egrep '^[a-zA-Z0-9-]{4,}$' $WORDS > $FILTERED
}

# Run this many times to get _tmp/sampled.txt.  Then it's reused in big-pipe-pat.
write-sample() {
  # adjust until we no longer get "arglist too long!
  # But this is random because of 'shuf'
  #local n=14436

  # egrep starts to have a lot of problems between 300 and 400.  It starts
  # taking 8.7 seconds!
  # Maybe it is building a DFA that is too big!

  #local n=14200
  local n=${1:-2000}

  local file=_tmp/sampled-$n.txt
  shuf -n $n $FILTERED > $file

  readarray SAMPLED < $file
  echo "Sampled ${#SAMPLED[@]} items"

  # Check that it's not too big for an argument!
  pat="$(./make_pat.py re2 < $file)"
  argv "$pat" > /dev/null
}

readonly NUM_WORDS=(10 100 1000 2000 3000 4000 5000 6000)

write-n() {
  for n in "${NUM_WORDS[@]}"; do
    write-sample $n
  done 
  wc -l _tmp/sampled-*.txt
}

write-keywords() {
  for k in "${KEYWORDS[@]}"; do
    echo $k 
  done > _tmp/keywords.txt
  wc -l _tmp/keywords.txt
}

if test $(basename $0) = words.sh; then
  "$@"
fi
