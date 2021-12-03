#!/usr/bin/env bash
#
# Usage:
#   ./podman.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

download() {
  mkdir -p _deps
  wget --directory _deps --no-clobber \
    https://github.com/containers/podman/releases/download/v3.4.2/podman-remote-static.tar.gz
}

# Uh this isn't what I want?  It's management of a remote system.  I want
# something local.  I guess podman uses crun or runc or something.
#
# https://github.com/containers/podman/blob/main/docs/tutorials/remote_client.md

podman() {
  _deps/podman-remote-static "$@"
}

# Uh this tries to find qemu-system-x86_64
init() {
  podman machine init
}

"$@"
