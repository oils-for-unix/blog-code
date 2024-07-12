#!/usr/bin/env bash
#
# catbrain tests
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

### testing

hello() {
  echo 'alice bob' | xargs -n 1 -- echo hi
}

gnu-demo() {
  seq 3 | xargs -I {} -- sh -c 'echo 0.$1; sleep 0.$1' dummy {}
  echo

  seq 5 | xargs -P 2 -I {} -- sh -c 'echo 0.$1; sleep 0.$1' dummy {}
  echo

  #return

  # This shows it calls wait4(-1, ...), which is waitpid(-1)
  # hm it also calls pipe2() every time, and fcntl?
  # why does it do that?  Yeah it reads from the pipe too

  # it reads(0, "1\n2\n3\n4\n5\n", ...) all at once
  # oh yes then I see the clone()
  # But every clone() has fnctl(4, F_SETFD, F_CLOEXEC) and pipe() and read()

  seq 5 | strace -- xargs -P 2 -I {} -- sh -c 'echo 0.$1; sleep 0.$1' dummy {}
}

my-demo() {
  seq 3 | ./xargs.py -I {} -- sh -c 'echo $1; sleep $1' dummy 0.{}
}

"$@"  
