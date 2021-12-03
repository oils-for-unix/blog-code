#!/usr/bin/env bash
#
# Usage:
#   ./docker-as-proc.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

demo() {
  # why do I need -i in addition to -a stdin?
  echo mystdin | sudo docker run -a stdin -a stdout -a stderr -i alpine \
    sh -c 'read x; echo stdin=$x; echo stderr >&2'
}

terminal-demo() {
  # busybox ls has --color=auto
  sudo docker run -a stdin -a stdout -a stderr -i -t alpine \
    ls --color=auto
}

startup-time() {
  time sh -c 'echo hi'
  # ~570 ms on a very fast machine!  (lenny.local)
  time sudo docker run alpine sh -c 'echo hi'
}

"$@"
