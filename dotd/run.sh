#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# https://www.gnu.org/software/make/manual/html_node/Automatic-Prerequisites.html

clean() {
  rm -v -f main.d main.d.mm main.o main
}

edit-files() {
  #echo '#include "newdep.h"' >> defs.h

  # Override it
  #echo '#define EXIT_CODE 100' > newdep.h

  sed -i 's|/\*HERE\*/|#include "defs.h"|g' main.c
}

run-main() {
  set +o errexit
  ./main
  echo "status: $?"
  echo
}

show-file() {
  local path=$1
  echo "--- $path ---"
  cat $path
  echo
}

demo() {
  clean

  git checkout main.c defs.h newdep.h  # revert it
  show-file main.c
  #show-file defs.h
  #show-file newdep.h

  make "$@"
  run-main

  show-file main.d.mm
  show-file main.d

  edit-files
  show-file main.c
  #show-file defs.h
  #show-file newdep.h

  make "$@"
  run-main

  show-file main.d.mm
  show-file main.d

  #clean
}

# Trying without the %.d rule.  This seems wrong on two counts:
# https://news.ycombinator.com/item?id=15061615
#
# Hm but it works?  

demo-short() {
  demo -f short.mk
}

show-flag() {
  local flag=$1
  rm -f main.d
  # -M writes to stdout
  echo "... $flag ..."
  gcc $flag main.c
  echo
}

flags() {
  show-flag -M
  test -f main.d && { echo "Should not exist"; exit 1; }

  # -MD is equivalent to -M -MF file, except that -E is not implied.  -E means
  show-flag -MD
  show-file main.d

  show-flag -MMD
  show-file main.d
}

# Hm this doesn't seem to output a .d file if there's a compile error.  But it's a simple case.
compile-error() {
  rm -f compile-error.d
  set +o errexit
  gcc -MD compile-error.c
  ls -l
}

# Invoke the preprocessor directly
preprocessor-deps() {
  # How to write it to a file, but not preprocess?
  cpp main.c -M -MF my_custom_name.d
  show-file my_custom_name.d

  # Doesn't generate .o file
  gcc -c main.c -M -MF my_custom_name2.d
  show-file my_custom_name2.d
  #ls -l main.o

  # TODO: I don't think there's way to compile and generate .d to a custom name?  Two outputs?
}

trace-procs() {
  local prefix=$1
  shift

  rm -f $prefix.*
  strace -ff -e 'execve' -o $prefix -- "$@"
  ls -l $prefix.*
  head $prefix.*
}

# TODO: Does Clang work the same way?
trace-gcc() {
  # /usr/lib/gcc/x86_64-linux-gnu/5/cc1
  # Hm -MD invokes cc1 with -MD main.d?  It takes an arg?
  # Forks assembler0
  mkdir -p _tmp
  local prefix=_tmp/gcc
  trace-procs $prefix gcc -c main.c -MD

  rm -f $prefix.*

  # How many processes?  FOUR.
  # 1. cc1 main.d main.c -> tmp file with assembly
  # 2. as -o main.o /tmp/ccoPSa4.s.  (Also it does 4 execve() calls, instead of using evecvpe?)
  # 3. cc1 foo.d foo.c -> tmp file with assembly
  # 4. as -o  foo.o /tmp/ccoPS5a4.s (same name?)
  #
  # Hm yes that is a lot of format juggling!

  touch foo.c
  trace-procs $prefix gcc -c main.c foo.c -MD
}

# Both of these invoke cc1.  That is odd.  They just pass flags straight
# through.  -MD takes and argument though.
trace-cpp() {
  trace-procs _tmp/cpp cpp main.c -M -MF my_custom_name3.d

  rm _tmp/cpp*

  trace-procs _tmp/cpp cpp main.c -MD my_custom_name4.d
}

# NOTES:
# - This feels wrong because we couldn't set up a sandbox with just deps.  Deps
# should be known, even in a full build?
# - Is it specific to the C preprocessor?  The logic is that if a new
# dependency was added, then an #include must have been added, so the timestamp
# must have changed.
# - It's focused on .c files and not .h files.  .c files are translation units.

# Questions:
# - How should OPy 'import' integrate witih Makefile?  How does Go do it?
# Their object format is different.

# Page from 2000, updated 4/2017.
# http://make.mad-scientist.net/papers/advanced-auto-dependency-generation/

# - They're using the "Combined method" that's different than the GNU Make Manual
# - Lots of other flags, not just -MD
# - They use "mv" for .Td to to .d ?  Why?
#   because gcc is incapable of generating two outputs!  What a horrible
#   syntax!
#
# I think this is for out of tree builds:
#
# -MT $@ set the name of the target in the generated dependency file
# -MD or -MMD : generate as a side effect of compilation, not INSTEAD of compilation
# -MP: adds a target for each prequisite, to avoid errors when deleting files
# -MF: write location to temporary file
#
# POSTCOMPILE:
# mv - so we don't have corrupted half-files (but doesn't this happen for all
# build rules?  The build system should take care of it)  But it says that
#   compilation failures can leave a half-formed dependency file.  Geez.  gcc
#   should fail to generate a dependency file if compilation fails, but maybe
#   it doesn't.  Could you check its exit code too?
# touch - so that the .o file  and .d file are newer?
#
# This scheme is full of hacks to get around Make!  mv is definitely one.  This
# is "naive style vs. pedantic style".
#
# You can also just flags to CFLAGS instead of having DEPFLAGS


# Critiques:
# - gcc flags are horrible  -- lots of gymnastics to to out of tree builds instead of -MD
# - gcc semantics are bad -- if it truly leaves a broken file (not able to reproduce this)
# - the protocol is bad: makefile snippets





"$@"
