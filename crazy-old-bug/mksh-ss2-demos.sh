#!/bin/mksh
# Author: Andy Chu (andy@oilshell.org)
#
# Demo of unexpected eval in mksh.
#
# Show all the contexts where this happens:
#
# ./mksh-ss2-demos.sh contexts

# TODO:
# - Come up with example vulnerability (CGI and other)
# - Test pre-shellshock shells to see what was changed

# I think this is less severe than ShellShock in one way, and more severe in
# another way:
#
# - Less severe because the script author must perform arithmetic (for a very loose definition of arithmetic)
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
  typeset -a myarray
  myarray=(7 8 9 10 11)

  mkdir -p out
  rm -f -v out/*

  local x

  # Arith substitution
  x='myarray[$(echo 0 | tee out/00-arith)]'
  echo $(( $x + 42 ))

  x='myarray[$(echo 1 | tee out/01-arith2)]'
  echo $(( x + 42 ))

  local varname

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

  # LHS assignment
  x='myarray[$(echo 12 | tee out/12-lhs)]'
  otherarray[x]=foo

  # Assoc array literal
  x='myarray[$(echo 13 | tee out/13-assoc)]'
  myassoc=([x]=foo)


  head out/*
  ls -l out/
}

# It has to be in an array index to work!
arith-compare() {
  typeset -a myarray
  myarray=(7 8 9)

  local code='myarray[1]'
  echo $(( $code + 42 ))

  local code='myarray[$(echo 1 | tee out/20-arith)]'

  echo $(( $code + 42 ))

  # NOT ALLOWED, because it's not an array
  local code='$(echo 3 | tee out/21-arith)'
  echo $(( $code + 42 ))

  ls -l out/
}

with-mksh-R56c() {
  local bin=~/src/languages/mksh-R56c/mksh

  # mksh doesn't have --version.  GAH!
  $bin $0 contexts
}

"$@"
