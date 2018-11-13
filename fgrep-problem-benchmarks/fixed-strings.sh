#!/bin/bash
#
# Usage:
#   ./fixed-strings.sh <function name>
#
# Demo:
#   ./fixed-strings.sh fetch-data
#   ./fixed-strings.sh make-ten  # ten copies of the data
#   ./fixed-strings.sh all-benchmarks
#
# Also useful:
#   viz, vis-trie

source common.sh
source words.sh  # for many-words-pipe-pat

set -o nounset
set -o pipefail
set -o errexit

readonly ONE=_tmp/all-1.txt
readonly TWO=_tmp/all-2.txt
readonly TEN=_tmp/all-10.txt

# ESSENTIAL BUG FIX FOR GREP
export LC_ALL=C

banner() {
  echo
  echo ----- "$@"
  echo
}

re2c() {
  ~/git/oilshell/oil/_deps/re2c-1.0.3/re2c "$@"
}

publish-data() {
  local name=$1
  scp $ONE $name@$name.org:oilshell.org/share
}

fetch-data() {
  mkdir -p _tmp
  wget --directory _tmp https://www.oilshell.org/share/all-1.txt
}

# Compare re2c with fgrep.

# Is fgrep using Aho-Corsick?
# I suspect that fgrep does GNU grep-like tricks to be fast.  Maybe we have to
# mmap() the whole file and then use re2c?  assume it has a NUL terminator.

fgrep-demo() {
  time fgrep $'main\nint' demo/* | wc -l
}

readonly MANIFEST=~/git/oilshell/oil/_tmp/wild/MANIFEST.txt
readonly ABS_PATHS=_tmp/wild-abs-paths.txt

make-manifest() {
  wc -l $MANIFEST

  mkdir -p _tmp
  awk '{ print "/home/andy/git/oilshell/oil/" $2 }' $MANIFEST >  $ABS_PATHS
}

make-big() {
  # 34 MB of shell scripts!
  time xargs cat < $ABS_PATHS > $ONE

  for i in $(seq 2); do
    echo _tmp/all-1.txt
  done | xargs cat > $TWO

  make-ten

  wc -l $ONE $TWO $TEN
  ls -l -h $ONE $TWO $TEN
}

make-ten() {
  # 338 MB now!
  for i in $(seq 10); do
    echo _tmp/all-1.txt
  done | xargs cat > $TEN

  ls -l -h $TEN
}

readonly KEYWORDS=(for while continue break if fi then else elif case esac do done)

fgrep-pat() {
  python -c 'import sys;sys.stdout.write("\n".join(sys.argv[1:]))' "${KEYWORDS[@]}"
}

grep-pat() {
  python -c 'import sys;sys.stdout.write("\\|".join(sys.argv[1:]))' "${KEYWORDS[@]}"
}

# pipe-pat defined in common.sh

# Same syntax!
ripgrep-pat() { pipe-pat "${KEYWORDS[@]}"; }
re2-pat() { pipe-pat "${KEYWORDS[@]}"; }
egrep-pat() { pipe-pat "${KEYWORDS[@]}"; }

egrep-dash-e-argv() {
  # NOTE: only supports argv without spaces.  readarray could help
  python -c '
import sys
for arg in sys.argv[1:]:
  print("-e")
  print(arg)
' "${KEYWORDS[@]}"
}

re2c-pat() {
  python -c '
import sys
quoted = ["\"%s\"" % w for w in sys.argv[1:]]
sys.stdout.write(" | ".join(quoted))
' "${KEYWORDS[@]}"
}

test-pat() {
  argv "$(fgrep-pat)"
  argv "$(grep-pat)"
  argv "$(re2c-pat)"
}

# Use a special marker in the code
update-re2c-keywords() {
  local pat="$(re2c-pat)"
  sed -i "s;.*__TO_REPLACE__.*;      $pat  // __TO_REPLACE__ ;g" fixed-strings.re2c.cc
}

describe-problem() {
  echo "Matching this file:"
  ls -l -h $TEN
  echo
  echo "Against ${#KEYWORDS[@]} keywords:"
  echo "   ${KEYWORDS[@]}"
  echo
}

# 9.3 seconds for "for line in f", but it has a loop.
# 5.7 seconds for findall on the whole thing.
python-re-benchmark() {

  banner 'Python re.findall()'

  time python -c '
from __future__ import print_function
import re, sys, time
path = sys.argv[1]
pat = re.compile("|".join(sys.argv[2:]))
with open(path) as f:
  contents = f.read() 

start_time = time.time()
pat.findall(contents)
elapsed = time.time() - start_time
print("findall() took %.f seconds" % elapsed, file=sys.stderr)
   
  #for line in f:
  #  m = pat.findall(line)
' $TEN "${KEYWORDS[@]}"
}

io-benchmark() {
  banner 'CAT'
  time cat $TEN > /dev/null

  banner 'WC'
  time wc -l $TEN
}

# Run with COUNT_RESULTS=1 ./fixed-strings.sh
COUNT_RESULTS=${COUNT_RESULTS:-}

grep-fixed-benchmark() {
  # fgrep is slowest!
  # what if I increase the number of strings?

  if test -n "$COUNT_RESULTS"; then
    echo
    echo 'FGREP number of results'
    fgrep "$(fgrep-pat)" $TEN | wc -l
  fi

  banner 'FGREP'
  time fgrep "$(fgrep-pat)" $TEN >/dev/null

  # Wow egrep is significantly slower than fgrep!

  if test -n "$COUNT_RESULTS"; then
    echo
    echo 'GREP number of results'
    grep "$(grep-pat)" $TEN | wc -l
  fi

  banner 'GREP'
  time grep "$(grep-pat)" $TEN >/dev/null

  if test -f $RG; then

    if test -n "$COUNT_RESULTS"; then
      echo
      echo 'RIPGREP number of results'
      $RG "$(ripgrep-pat)" $TEN | wc -l
    fi

    banner 'RIPGREP'
    time $RG "$(ripgrep-pat)" $TEN >/dev/null
  fi
}

# NOTE: egrep is faster with 14,300 strings than on 13 strings?  Probably
# because it is able to search LESS of the line.  A match is more likely to
# appear earlier in the line, even though there are fewer matches overall?
many-words-grep-benchmark() {

  # Always enable
  COUNT_RESULTS=1

  local pat="$(many-words-pipe-pat)"

  if test -n "$COUNT_RESULTS"; then
    echo
    echo 'EGREP number of results'
    egrep "$pat" $TEN > _tmp/many-egrep.txt
  fi

  banner 'EGREP'
  time egrep "$pat" $TEN >/dev/null

  if test -f $RG; then

    if test -n "$COUNT_RESULTS"; then
      echo
      echo 'RIPGREP number of results'
      $RG "$pat" $TEN > _tmp/many-ripgrep.txt
    fi

    banner 'RIPGREP'
    time $RG "$pat" $TEN >/dev/null
  fi

  wc -l _tmp/many-*
  md5sum _tmp/many-*
}

# Does this make a difference?  I'm not seeing it.  Could be related to
# locale.
egrep-syntax-comparison() {
  if true; then
    banner 'EGREP with | syntax'
    time egrep "$(egrep-pat)" $TEN >/dev/null

    banner 'EGREP with -e'
    time egrep $(egrep-dash-e-argv) $TEN >/dev/null
  fi
}

# I'm getting opposite results?  mmap() is a win?
# https://lemire.me/blog/2012/06/26/which-is-fastest-read-fread-ifstream-or-mmap/

re2c-fixed-benchmark() {
  local gen=_gen/fixed-strings.cc 
  local bin=_tmp/fixed-strings

  mkdir -p _gen

  re2c -o $gen fixed-strings.re2c.cc

  #g++ $DEBUG_FLAGS -o _tmp/fread _gen/fread.cc
  g++ $OPT_FLAGS -o $bin $gen

  # 800 ms to read line-by-line.  disabled because it's slow.  
  if false; then
    banner 'fgets'
    time $bin fgets $TEN >/dev/null
  fi

  # Without re2c: count the lines at memory bandwidth.  187 ms.
  banner 'read:count-lines'
  time $bin read:count-lines $TEN >/dev/null

  # 1214 ms.
  banner 'read:re2c-match'
  time $bin read:re2c-match $TEN >/dev/null

  # Hm the mmap() is the thing that is slow here?  Not re2c?
  banner 'mmap'
  time $bin mmap $TEN #>/dev/null
}

re2-fixed-benchmark() {
  ./build.sh re2-grep
  time _tmp/re2_grep "$(re2-pat)" $TEN >/dev/null
}

all-benchmarks() {
  io-benchmark
  grep-fixed-benchmark
  re2c-fixed-benchmark
  re2-fixed-benchmark
  python-re-benchmark
}

viz() {
  local name=${1:-fixed-strings}
  local dot=_gen/$name.dot
  re2c --emit-dot -o $dot $name.re2c.cc
  dot -T png -o _gen/$name.png $dot
}

viz-trie() {
  viz trie
}

# GrepFast() is 682 bytes only.
code-size() {
  ~/git/other/bloaty/bloaty -d symbols _tmp/fixed-strings | tee _gen/code-size.txt
}

readonly RG=~/install/ripgrep-0.10.0-x86_64-unknown-linux-musl/rg

download-ripgrep() {
  wget --directory ~/install \
    https://github.com/BurntSushi/ripgrep/releases/download/0.10.0/ripgrep-0.10.0-x86_64-unknown-linux-musl.tar.gz
}

# grep is faster than both fgrep and the "optimal" DFA in native code
# (generated by re2c).  I think grep is benefitting from SKIPPING bytes.

# TODO:
# - Compare 2 keywords vs 10-20

"$@"
