#!/usr/bin/env bash
#
# Sample code for xargs blog post.

# https://www.oilshell.org/blog/2021/08/xargs.html
#
# Usage:
#   ./demo.sh <function name>
#
# Example:
#   ./demo.sh do_one
#   ./demo.sh do_all
#   ./demo.sh do_all_parallel

set -o nounset
set -o pipefail
set -o errexit

hello() {
  echo 'alice bob' | xargs -n 1 -- echo hi
}

do_one() {
   # Rather than xargs -I {}, it's more flexible to
   # use a function with $1
   echo "Do something with $1"  
   cp --verbose $1 /tmp

   sleep 0.5  # to show parallelization
}

do_all() {
  # Call the do_one function for each item.
  # Also add -P to make it parallel
  cat tasks.txt | xargs -n 1 -d $'\n' -- $0 do_one
}

preview() {
  # Add echo to preview the tasks
  cat tasks.txt | xargs -n 1 -d $'\n' -- echo $0 do_one
}

do_all_parallel() {
  cat tasks.txt | xargs -n 1 -d $'\n' -P 2 -- $0 do_one
}

"$@"  # dispatch on $0; or use 'runproc' in Oil
