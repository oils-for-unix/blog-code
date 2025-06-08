#!/usr/bin/env bash
#
# Usage:
#   ./git.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

merge-to-main() {
  local do_push=${1:-T}  # pass F to disable

  local branch=$(git rev-parse --abbrev-ref HEAD)

  if test "$do_push" = T; then
    git checkout main
    git merge $branch

    time git push origin
    echo
    time git push codeberg
    echo

    git checkout $branch
  else
    git checkout main
    git merge $branch
    git checkout $branch
  fi
}

rebase-main() {
  git rebase -i main
}

diff-main() {
  git diff main..
}

log-main() {
  git log main..
}

"$@"
