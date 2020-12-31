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
source words.sh  # for constructing patterns

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

fgrep-pat() { ./make_pat.py fgrep; }
grep-pat() { ./make_pat.py grep; }
ripgrep-pat() { ./make_pat.py ripgrep; }
re2c-pat() { ./make_pat.py re2c; }
re2-pat() { ./make_pat.py re2; }

test-pat() {
  local k=_tmp/keywords.txt
  argv "$(fgrep-pat < $k)"
  argv "$(grep-pat < $k)"
  argv "$(ripgrep-pat < $k)"
  argv "$(re2c-pat < $k)"
}

grep-fixed-benchmark() {
  local words=_tmp/keywords.txt

  # fgrep is slowest!
  # what if I increase the number of strings?

  if test -n "$COUNT_RESULTS"; then
    echo
    echo 'FGREP number of results'
    fgrep "$(fgrep-pat < $words)" $TEN | wc -l
  fi

  banner 'FGREP'
  time fgrep "$(fgrep-pat < $words)" $TEN >/dev/null

  # Wow fgrep is significantly slower than grep!

  if test -n "$COUNT_RESULTS"; then
    echo
    echo 'GREP number of results'
    grep "$(grep-pat < $words)" $TEN | wc -l
  fi

  banner 'GREP'
  time grep "$(grep-pat < $words)" $TEN >/dev/null

  if test -f $RG; then

    if test -n "$COUNT_RESULTS"; then
      echo
      echo 'RIPGREP number of results'
      $RG "$(ripgrep-pat < $words)" $TEN | wc -l
    fi

    banner 'RIPGREP'
    time $RG "$(ripgrep-pat < $words)" $TEN >/dev/null
  fi
}

# NOTE: egrep is faster with 14,300 strings than on 13 strings?  Probably
# because it is able to search LESS of the line.  A match is more likely to
# appear earlier in the line, even though there are fewer matches overall?
many-words-grep-benchmark() {
  local file=$1
  local pat="$(./make_pat.py ripgrep < $file)"

  rm -f _tmp/many-*

  # Always enable
  COUNT_RESULTS=1

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


  return

  banner 'NOTE: egrep blows up on large input!  May want to Ctrl-C.'

  if test -n "$COUNT_RESULTS"; then
    echo
    echo 'EGREP number of results'
    egrep "$pat" $TEN > _tmp/many-egrep.txt
  fi

  banner 'EGREP'
  time egrep "$pat" $TEN >/dev/null

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

# TODO: Always update the words here?
re2c-fixed-benchmark() {
  local gen=_gen/fixed-strings.cc 
  local bin=_tmp/fixed-strings

  mkdir -p _gen

  banner 'Compiling with re2c'
  time re2c -o $gen fixed-strings.re2c.cc
  banner 'Done'
  return

  #g++ $DEBUG_FLAGS -o _tmp/fread _gen/fread.cc
  banner 'Compiling with g++ (GCC)'
  time g++ $OPT_FLAGS -o $bin $gen

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

  if false; then
    # Hm the mmap() is the thing that is slow here?  Not re2c?
    banner 'mmap'
    time $bin mmap $TEN #>/dev/null
  fi
}

re2-fixed-benchmark() {
  local words=${1:-_tmp/keywords.txt}

  banner "RE2 on $words"

  ./build.sh re2-grep
  time _tmp/re2_grep "$(re2-pat < $words)" $TEN >/dev/null
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

do-done-edited() {
  local name=do-done-edited
  local dot=$name.dot
  dot -T png -o _gen/$name.png $dot
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

# All times are 'user' time, which is most of the 'real' time.
#        re2c compile | re2c code size | re2c match time | ripgrep time | RE2
# n= 100         7 ms          11 KiB           1,566 ms         687 ms   1,398 ms
# n=1000        66 ms          57 KiB           2,311 ms       1,803 ms   1,874 ms
# n=2000       120 ms          93 KiB           2,499 ms       3,591 ms   2,681 ms
# n=3000       204 ms         125 KiB           2,574 ms       5,801 ms   3,471 ms
# n=4000       266 ms         159 KiB           2,563 ms       8,083 ms   4,323 ms
# n=5000       363 ms         186 KiB           2,638 ms      10,431 ms   5,294 ms
# n=6000       366 ms         213 KiB           2,659 ms      13,182 ms   6,397 ms
# n=47,000   2,814 ms
#
# NOTES:
# - egrep blows up around 400 strings!
# - RE2 says "DFA out of memory" at 2000 strings, because it exhausts its 8 MB
# budget.  We simply bump it up.
# - at 48,000 words, re2c segfaults!
# - At 10,000 words, GCC takes 36 seconds to compile re2c's output!  It's 74K
# lines in 1.2 MB of source.

compare-many-words() {
  local n=${1:-1000}

  local words=_tmp/sampled-$n.txt

  # ripgrep
  many-words-grep-benchmark $words

  # NOTE: blows up
  re2-fixed-benchmark $words

  update-re2c-keywords $words
  re2c-fixed-benchmark $words
  code-size
}

re2-many() {
  for n in 1000 2000 3000 4000 5000 6000; do
    local words=_tmp/sampled-$n.txt
    re2-fixed-benchmark $words
  done
}

re2c-huge() {
  local n=${1:-9000}
  write-sample $n
  local words=_tmp/sampled-$n.txt

  # Can't do this because the argument list is too long for sed!  Doh!
  update-re2c-keywords $words
  re2c-fixed-benchmark $words
}

max-re2c-state() {
  egrep -o 'yy[0-9]+' _gen/fixed-strings.cc | sort 
}

"$@"
