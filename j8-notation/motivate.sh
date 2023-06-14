#!/usr/bin/env bash
#
# Usage:
#   ./motivate.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# TODO: need a unicode / UTF-16 surrogate pair / UTF-8 playground
#
# https://jvns.ca/blog/2023/04/17/a-list-of-programming-playgrounds/
# 
# We can write one in Python?  Since it deals with bytes better than JavaScript

py-json-ls() {
  python3 -c '
import json, os, sys

def log(*args):
  #print("\t", *args, file=sys.stderr)
  pass

# utf-8
log("default encoding:", sys.getdefaultencoding())
log("FS encoding:", sys.getfilesystemencoding())

# surrogateescape
log("FS errors:", sys.getfilesystemencodeerrors())

log(os.listdir())

# encode error actually does make sense here
#log([f.encode("utf-8") for f in os.listdir()])

# Problem: Python uses surrogateescape handler to move \xff to \udcff
print(json.dumps(os.listdir(".")))
'

# Is the surrogate pair encoding correct?
#
# No, the error should be on os.listdir() !!!
}

node-json-ls() {
  nodejs -e '
const fs = require("fs");
var listing = fs.readdirSync(".");
process.stdout.write(JSON.stringify(listing));
'
}

ls-demo() {
  cd _tmp
  set +o errexit

  py-json-ls

  LC_CTYPE=C py-json-ls
}

py-decode-first() {
  python3 -c \
    'import sys, json; sys.stdout.write(json.loads(sys.stdin.read())[0])'
}

node-decode-first() {
  nodejs -e '
process.stdin.on("data", data => {
  process.stdout.write(JSON.parse(data)[0]);
})
'
}

view-bytes() {
  # hex in groups of 1
  od -t x1 "$@"
}

node-encode-surrogate() {
  # ef bf bd
  #
  # Aha, it's the unicode replacement character
  # https://www.compart.com/en/unicode/U+FFFD

  nodejs -e 'process.stdout.write(JSON.stringify("\udcff") + "\n")'
}

node-write-surrogate() {
  # WHY is node.js doing this
  # ef bf bd
  nodejs -e 'process.stdout.write("\udcff\n")'
}

round-trip() {
  local s=$1
  mkdir -p _tmp
  pushd _tmp

  rm -v -f *

  touch "$s"

  echo 'python JSON'
  py-json-ls
  echo

  # Node gives invalid character
  # JSON8 will fix this
  echo 'node JSON'
  node-json-ls
  echo

  echo 'python -> python'
  py-json-ls | py-decode-first
  echo
  py-json-ls | py-decode-first | view-bytes
  echo

  echo 'node -> python'
  node-json-ls | py-decode-first
  echo
  node-json-ls | py-decode-first | view-bytes
  echo

  # Why does node.js output 3 bytes?
  echo 'python -> node'
  py-json-ls | node-decode-first
  echo
  py-json-ls | node-decode-first | view-bytes
  echo

  popd
}

demo() {
  round-trip $'\xce\xbc' 

  # surrogateescape allows invalid utf-8 in memory, and it can't be encoded

  set +o errexit
  round-trip $'\xff'
}


"$@"
