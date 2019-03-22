#!/bin/bash
#
# Usage:
#   ./deploy.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

compress() {
  for dir in _data/*; do
    local out="$PWD/$(basename $dir).wwz"
    pushd $dir
    zip -r -q $out .
    popd
  done
}

deploy() {
  local name=$1
  local host=$name.org
  local dest_dir=oilshell.org/grep-for-papers

  ssh $name@$host mkdir -p $dest_dir
  rsync --archive --verbose llvm.txt *.wwz $name@$host:$dest_dir/
}

"$@"
