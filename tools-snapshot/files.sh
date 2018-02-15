#!/bin/bash
#
# Usage:
#   ./files.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

readonly DEST_DIR=../oilshell.org__deploy/blog/2018/01/files

# Shared functions copied from oilshell.org__deploy/blog/2017/12/files.

# http://pygments.org/docs/changelog/
# Gah there is a regression in the packaged verison of the bash lexer.
#
# Installed via PIP.

install-pygments() {
  pip install pygments
}

format() {
  local path=$1
  local lang=${2:-bash}

  cat <<EOF
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="code.css" />
  </head>
  <body>
EOF
  pygmentize -f html -l $lang $path
  cat <<EOF
  </body>
</html>
EOF
}

2018-01-files() {
  # STUPID dreamhost!  lex.py.html is not an allowed filename.  Causes an
  # suexec error.
  format ../oil/testdata/osh-runtime/abuild sh > $DEST_DIR/abuild.html
  format ~/git/basis-build/_tmp/debootstrap/debootstrap > $DEST_DIR/debootstrap.html
  format ../distro-build/aboriginal/aboriginal-1.4.5/build.sh > $DEST_DIR/build.sh.html

  ls -l $DEST_DIR
}

css() {
  pygmentize -f html -S default > $DEST_DIR/code.css
  ls -l $DEST_DIR
}

"$@"
