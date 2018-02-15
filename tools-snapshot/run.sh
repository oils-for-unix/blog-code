#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

new-post() {
  local name=$1
  local day=${2:-$(date '+%d')}

  # pick the last one alphabetiaclly
  for month_dir in blog/201?/??; do
    true
  done
  local path=$month_dir/${name}.md
  echo $path

  cat >$path <<EOF
---
title: TODO
date: $(date '+%Y/%m/%d')
comments_url: TODO
---

Test body
EOF

  pushd $month_dir 
  ln -s --verbose ${name}.md ${day}.md || true
  popd

  local symlink_path=$month_dir/${day}.md
  echo "Wrote $path"

  #ls -l $path $symlink_path

  git add $path $symlink_path
  wc -l $path $symlink_path
}

copy-snapshot() {
  local dest=../blog-code/tools-snapshot

  # A separate tool
  cp -v ~/hg/zoo/bin/snip.py Snip $dest

  mkdir -p $dest
  cp -v Makefile *.py {build,deps,files,latch,run}.sh $dest

  mkdir -p $dest/css
  cp -v css/*.css $dest/css

  cp -v blog/*.md $dest/blog  # index and tags

  local post_dir=$dest/blog/2018/02
  mkdir -p $post_dir
  cp -v blog/2018/02/commonmark.md $post_dir
  ln -s -v commonmark.md $post_dir/14.md
}

"$@"
