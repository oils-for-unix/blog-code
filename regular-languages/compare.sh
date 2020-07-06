#!/bin/bash
#
# Demo for EggEx.  Do any of these common engines backtrack?
#
# Related: https://research.swtch.com/glob
#
# "Perhaps the most interesting fact evident in the graph is that GNU glibc,
# the C library used on Linux systems, has a linear-time glob implementation,
# but BSD libc, the C library used on BSD and macOS systems, has an
# exponential-time implementation."
#
# Usage:
#   ./regex-backtrack.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

source op-line.sh
source op-match.sh
source op-submatch.sh
source op-glob.sh

TIMEFORMAT='%U'  # CPU seconds spent in user mode

# https://swtch.com/~rsc/regexp/regexp1.html

pattern() {
  local n=$1

  # a?^n a^n
  repeat 'a?' $n
  repeat 'a' $n
  echo
}

text() {
  local n=$1
  repeat a $n
  echo
}

demo() {
  pattern 1
  pattern 2
  pattern 3

  text 1
  text 2
  text 3
}

regex-backtrack() {
  local max=${1:-22}

  for i in $(seq $max); do
    local pattern=$(pattern $i)
    local text=$(text $i)

    time egrep-task "$text" "$pattern"
    time sed-task "$text" "$pattern"

    # Does zsh use libc?  Not sure
    time libc-task "$text" "$pattern"
    time zsh-task "$text" "$pattern"

    time gawk-task "$text" "$pattern"
    time mawk-task "$text" "$pattern"
    time python-task "$text" "$pattern"
    time perl-task "$text" "$pattern"

    # This backtracks, but it's harder to tell than Perl/Python due to
    # startup overhead
    time js-task "$text" "$pattern"
    echo
  done
}

#
# glob
#

glob-setup() {
  mkdir -p $GLOB_TMP
  cd $GLOB_TMP
  touch $(repeat a 100)
  ls -l 
}

readonly OIL_REPO=../../oil

readonly -a SHELLS=(dash bash mksh $OIL_REPO/_deps/spec-bin/ash osh)

glob-backtrack() {
  # bash and mksh both backtrack
  # dash and ash are OK.  osh is good too!  with GNU libc.

  # - zsh doesn't source it?
  # - yash doesn't like 'local'.

  for sh in ${SHELLS[@]}; do
    echo === $sh
    $sh -c '. ./op-glob.sh; glob_bench'
  done

}

fnmatch-backtrack() {
  # Same for fnmatch(): bash and mksh backtrack
  # osh doesn't
  # but dash and ash somehow don't like 'time shellfunc'?

  for sh in ${SHELLS[@]}; do
    echo === $sh
    $sh -c '. ./op-glob.sh; fnmatch_bench'
  done
}

#
# Greedy vs. non-greedy
#
# sed, python, perl, gawk have captures
#

greedy() {
  local text='<p>hello</p> foo'

  for pat in '<.*>' '<.*>h'; do
    echo
    echo "=== matching against $pat"
    echo

    time egrep-match "$text" "$pat"

    #local pat2='\<.*\>h'
    time sed-match "$text" "$pat"

    time libc-match "$text" "$pat"
    time gawk-match "$text" "$pat"
    time python-match "$text" "$pat"
    time perl-match "$text" "$pat"
    time js-match "$text" "$pat"
  done

  echo
  echo '== nongreedy'
  echo

  # Only backtracking engines support this non-greedy behavior
  pat='<.*?>'
  time python-match "$text" "$pat"
  time perl-match "$text" "$pat"
}

#
# Capture Semantics -- the "parse problem"
#

# Digression: POSIX submatching
# https://swtch.com/~rsc/regexp/regexp2.html

submatch() {
  local text='abcdefg'
  local pat='(a|bcdef|g|ab|c|d|e|efg|fg)*'

  # Simpler version
  local text='abc'
  local pat='(a|bc|ab|c)*'

  # they all print 'g' ?
  # So there's no difference?

  # These are POSIX conformance bugs?
  # 2010: http://hackage.haskell.org/package/regex-posix-unittest
  # https://wiki.haskell.org/Regex_Posix

  libc-submatch "$text" "$pat"
  gawk-submatch "$text" "$pat"
  sed-submatch "$text" "$pat"

  python-submatch "$text" "$pat"
  perl-submatch "$text" "$pat"
  js-submatch "$text" "$pat"
}

# From Table 4
# https://www3.cs.stonybrook.edu/~dongyoon/papers/FSE-19-LinguaFranca.pdf
submatch-case() {
  local text=$1
  local pat=$2

  local submatch=${3:-1}

  echo
  echo "Matching pattern  $pat  on  $text, submatch $submatch"

  # they all print 'g' ?
  # So there's no difference?

  # These are POSIX conformance bugs?
  # 2010: http://hackage.haskell.org/package/regex-posix-unittest
  # https://wiki.haskell.org/Regex_Posix

  libc-submatch "$text" "$pat" "$submatch"
  gawk-submatch "$text" "$pat" "$submatch"
  sed-submatch "$text" "$pat" "$submatch"

  python-submatch "$text" "$pat" "$submatch"
  perl-submatch "$text" "$pat" "$submatch"
  js-submatch "$text" "$pat" "$submatch"
}

submatch2() {
  submatch-case 'aa' '(a*)+' 1
  submatch-case 'aa' '(a*)+' 2

  submatch-case 'ab' '((a)|(b))+' 1
  submatch-case 'ab' '((a)|(b))+' 2

  # v8 is different!
  submatch-case ']' '([]])' 1
}

"$@"
