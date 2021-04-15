#!/usr/bin/env bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

readonly SOCKET='osh.c5po-socket'

serve() {
  ./server.py --socket-path $SOCKET
}

to-my-stdout() {
  ./headless_client.py --socket-path $SOCKET --to-file /dev/stdout "$@"
}

to-new-pty() {
  ./headless_client.py --socket-path $SOCKET --to-new-pty
}

to-disk() {
  local file=_tmp/disk.txt

  mkdir -p _tmp

  ./headless_client.py --socket-path $SOCKET --to-file $file
  echo --
  head $file
  echo --
}

# Doesn't work, we get EINVAL on sock.listen() or sock.accept(), after
# socket.fromfd()
socket-pair() {
  ./headless_client.py UNUSED
}

"$@"
