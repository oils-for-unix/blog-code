#!/bin/bash
#
# Usage:
#   ./words.sh <function name>

source common.sh

set -o nounset
set -o pipefail
set -o errexit

readonly WORDS=/usr/share/dict/words
readonly FILTERED=_tmp/filtered.txt

export LC_ALL=C

prune() {
  wc -l $WORDS

  # Select words of at least length 4, because I think 1 length patterns cause
  # too much short-circuiting in the benchmarks.

  egrep '^[a-zA-Z0-9-]{4,}$' $WORDS | wc -l

  egrep '^[a-zA-Z0-9-]{4,}$' $WORDS > $FILTERED
}

# Run this many times to get _tmp/sampled.txt.  Then it's reused in big-pipe-pat.
sample() {
  # adjust until we no longer get "arglist too long!
  # But this is random because of 'shuf'
  #local n=14436

  local n=14200

  shuf -n $n $FILTERED > _tmp/sampled.txt

  readarray SAMPLED < _tmp/sampled.txt
  echo "Sampled ${#SAMPLED[@]} items"

  pat="$(words-pipe-pat "${SAMPLED[@]}")"
  argv "$pat"
}

many-words-pipe-pat() {
  readarray SAMPLED < _tmp/sampled.txt

  pat="$(words-pipe-pat "${SAMPLED[@]}")"
  argv "$pat"
}

if test $(basename $0) = words.sh; then
  "$@"
fi
