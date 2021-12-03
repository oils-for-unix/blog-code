#!/usr/bin/env bash
#
# Usage:
#   ./runc.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

show() {
  # This was already installed as /usr/sbin/runc, maybe because I installed
  # docker?
  which runc
}

# Based on these instructions
# https://github.com/opencontainers/runc/#rootless-containers

rootless-export() {
  mkdir -p _container/
  cd _container/
  mkdir -p rootfs

  # gah root again!
  local id=$(sudo docker create busybox)


# [sudo] password for andy:
# Unable to find image 'busybox:latest' locally
# latest: Pulling from library/busybox
# 3aab638df1a9: Pulling fs layer
# 3aab638df1a9: Verifying Checksum
# 3aab638df1a9: Download complete
# 3aab638df1a9: Pull complete
# Digest: sha256:52817dece4cfe26f581c834d27a8e1bcc82194f914afe6d50afad5a101234ef1
# Status: Downloaded newer image for busybox:latest
# id=df605fb57bed3bed153964ac4fe3b740be94fbcc37097535526a9c61c50341e6

# andy@lenny:~/git/oilshell/blog-code/docker$ ./runc.sh rootless-export
# id=1d180be197597a030710c1b8d8a13d9b9a1f68bd1f548076c25fa0f65dd5609c

  echo id=$id

  sudo docker export $id | tar --directory rootfs -x -v -f -


  # Creates config.json
  # The --rootless parameter instructs runc spec to generate a configuration for a rootless container, which will allow you to run the container as a non-root user.
  runc spec --rootless
}

rootless-demo() {
  ls -l _container
  wc -l _container/config.json

  # This doesn't accept arguments!  It's in config.json
  # args: ["sh"]

  cd _container
  runc --root /tmp/runc run mycontainerid
}

"$@"
