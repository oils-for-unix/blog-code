#!/usr/bin/env bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

readonly SOCKET='control.socket'

serve() {
  ./server.py $SOCKET
}

to-stdout() {
  ./headless_client.py $SOCKET
}

to-new-pty() {
  ./headless_client.py $SOCKET pty
}

to-disk() {
  local file=_tmp/disk.txt

  mkdir -p _tmp

  ./headless_client.py $SOCKET $file
  echo --
  head $file
  echo --
}

"$@"
