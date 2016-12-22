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

readonly CLANG=~/install/clang+llvm-3.8.0-x86_64-linux-gnu-ubuntu-14.04/bin/clang++

build-run() {
  local name=$1
  CXX=c++ 
  CXX=$CLANG

  $CXX -std=c++11 -O3 -o _tmp/$name $name.cc
  #chmod +x _tmp/ik7
  _tmp/ik7
}

ik7() {
  build-run ik7
}

dump() {
  objdump -d _tmp/ik7
}


"$@"
