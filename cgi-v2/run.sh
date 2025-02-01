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

serve-go() {
  # from Claude AI
  ~/install/go/bin/go run file-upload-handler.go
}

# Wow, gccgo is super easy!

install() {
  # 42.6 MB of archives
  sudo apt-get install gccgo
}

compile() {
  # 106 KB binary
  gccgo -O2 -o file-upload-handler file-upload-handler.go
}

serve-gccgo() {
  # Hm this still has 4 threads?  Doesn't seem to respect GOMAXPROCS
  # Probably because I didn't actually start a goroutine

  #GOMAXPROCS=1 ./file-upload-handler
  GOMAXPROCS=10 ./file-upload-handler
}

#
# C++ extension
#

# does NOT work
build-c() {
	cc -c fib.c -o fib.o
	gccgo -o fibonacci main.go fib.o
}

# does NOT work
fib-gc() {
  ~/install/go/bin/go run main.go
}

"$@"
