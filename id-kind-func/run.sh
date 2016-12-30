#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

export() {
  mkdir -p _tmp
  ./func_search.py print ik7 > _tmp/ik7.txt
  ./func_search.py print ik6 > _tmp/ik6.txt
}

readonly CLANG=${CLANG:-~/install/clang+llvm-3.8.0-x86_64-linux-gnu-ubuntu-14.04/bin/clang++}
readonly GCC=${GCC:-c++}

build-run() {
  local cxx=$1
  local name=$2
  local out=${3:-_tmp/$name}

  mkdir -p _tmp
  $cxx -std=c++11 -O3 -o $out $name.cc
  #chmod +x _tmp/ik7
  $out
}

ik7() {
  set -o xtrace
  build-run $GCC ik7
}

# http://blog.reverberate.org/2009/07/giving-up-on-at-style-assembler-syntax.html
# Using Intel syntax so I can google instruction names.
dump-func() {
  local bin=${1:-_tmp/ik7}
  objdump -M intel -d $bin | grep --after-context 12 LookupKind
}

compare-gcc-clang() {
  set -o xtrace
  build-run $GCC ik7 _tmp/ik7-gcc
  build-run $CLANG ik7 _tmp/ik7-clang
  set +o xtrace

  echo ---
  echo GCC
  echo
  dump-func _tmp/ik7-gcc
  echo

  echo ---
  echo Clang
  echo
  dump-func _tmp/ik7-clang
}

show-versions() {
  $GCC --version
  $CLANG --version
}


"$@"
