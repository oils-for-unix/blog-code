#!/usr/bin/env bash
#
# Adapting https://fly.io/blog/docker-without-docker/
#
# Usage:
#   ./without-docker.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

download() {
  wget 'https://gist.githubusercontent.com/tqbf/10006fae0b81d7c7c93513890ff0cf08/raw/2b774ecf3b8cb8042fa87ab0d86a41175873201a/docker-pull.sh'
}

"$@"
