#!/usr/bin/env bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

make-files() {
  mkdir -p _tmp
  echo foo > _tmp/foo.txt
  echo bar > _tmp/bar.txt
}

test-post() {
  curl -X POST -F "files=@_tmp/foo.txt" -F "files=@_tmp/bar.txt" http://localhost:8080/upload
}

serve() {
  # from Claude AI
  ~/install/go/bin/go run file-upload-handler.go
}


"$@"
