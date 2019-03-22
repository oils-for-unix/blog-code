#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

readonly LLVM_DIR=~/src/languages/llvm-7.0.1.src
readonly CLANG_DIR=~/src/languages/cfe-3.8.0.src
readonly PYTHON_DIR=~/src/languages/Python-3.6.7

readonly BASH_DIR=~/src/languages/bash-5.0
readonly DASH_DIR=~/src/languages/dash-0.5.8
readonly ZSH_DIR=~/src/languages/zsh-5.1.1


extensions() {
  find $LLVM_DIR -type f | exthist
}

# TODO: Python could use a different filter, e.g. getting rid of
# unicodename_db.h.

files() {
  local dir=$1
  find $dir \
    -name _pubs -a -prune -o \
    '(' -name '*.cpp' -o -name '*.cc' -o -name '*.c' -o -name '*.h' -o -name '*.py' ')' -a -print0
}

grep-pubs() {
  # Common flags
  # CPython has .py files that looks binary to grep.  Without this, we get
  # 'Binary file matches' and it messes up the output.
  local flags='--binary-files=text'

  # This does NOT suppress the bad output, as you would think.  GNU grep only
  # looks at the first part of the file and suppresses it.
  #local flags='--binary-files=without-match'

  # get rid of common non-pub reasons for years: Copyright 2013, MSVC 2013,
  # Visual Studio 2013, etc.

  # Not an error if no results
  set +o errexit

  egrep $flags -n 'https?://|\.pdf|\.PDF' -- "$@" | egrep $flags -v 'gnu.org/licenses'

  # This year check unfortunately brings in a lot of in-source changelogs too.
  egrep $flags -n -w '19[0-9][0-9]|20[0-1][0-9]' -- "$@" | egrep $flags -v 'copyright|Copyright|Studio|MSVC|_MSC_VER'

  set -o errexit
}

unique-sources() {
  egrep -o '^[^:]+' | sort | uniq
}

# Assume files are UTF-8 (which is NOT the HTML default.)
html-header() {
  cat <<EOF
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
  </head>
EOF
}

# The UI would be better with a bit of JavaScript, but OK.
number-lines() {
  html-header

  cat <<EOF
    <pre>
EOF
  
  awk '
  { 
    # really terrible way of escaping HTML.  \\& is a literal ampersand!
    gsub("&", "\\&amp;");
    gsub("<", "\\&lt;");
    gsub(">", "\\&gt;");

    # 1-based line number
    line_num = sprintf("%5d", NR)
    print "<a name=L" NR "></a>" line_num " " $0
  }
  '

  cat <<EOF
    </pre>
  </body>
</html>
EOF
}

pretty-sources() {
  local dir=$1
  mkdir -p $dir
  while read rel_path; do
    # number all lines
    local out=$dir/$rel_path.html  # add .html extension so browser will open it
    mkdir -p $(dirname $out)
    number-lines < $rel_path > $out
  done
}

html-pubs() {
  local dir=$1
  local this_script=$PWD/$0

  # Make it in the current directory
  local out_dir=$PWD/_data/$(basename $dir)
  mkdir -p $out_dir

  pushd $dir  # for prettier output from grep

  # TODO: handle the case where nothing is found!
  local manifest=$out_dir/manifest.bin
  files . > $manifest
  
  local results=$out_dir/results.txt

  # remove stupid grep messages.  Why doesn't grep -I work?
  cat $manifest | xargs -0 -- $this_script grep-pubs > $results

  # Sanity check for bad unicode, etc.
  file $results

  # avoid xargs because it can mess up the total
  wc -l --files0-from $manifest > $out_dir/wc.txt

  local num_results=$(wc -l < $results)
  # last line is the total, I think
  local num_lines=$(tail -n 1 $out_dir/wc.txt | awk '{print $1}')
  local num_files=$(cat $manifest | xargs -0 -n 1 -- echo | wc -l)

  # make index
  cat $results | to-html $(basename $dir) $num_results $num_lines $num_files > $out_dir/index.html

  # make pages the index links to
  cat $results | $this_script unique-sources | $this_script pretty-sources $out_dir

  popd

  echo "$num_results results"
  echo "file://$out_dir/index.html"
}

llvm-pubs() { html-pubs $LLVM_DIR; }
clang-pubs() { html-pubs $CLANG_DIR; }
python-pubs() { html-pubs $PYTHON_DIR; }

bash-pubs() { html-pubs $BASH_DIR; }
dash-pubs() { html-pubs $DASH_DIR; }
zsh-pubs() { html-pubs $ZSH_DIR; }

re2c-pubs() { html-pubs ~/src/re2c-0.16; }
sqlite-pubs() { html-pubs ~/src/sqlite-src-3110100; }
make-pubs() { html-pubs ~/src/make-4.1; }
mawk-pubs() { html-pubs ~/src/languages/mawk-1.3.4-20150503; }

lua-pubs() { html-pubs ~/src/languages/lua-5.3.3; }
ocaml-pubs() { html-pubs ~/src/languages/ocaml-4.06.0; }

# This needs to search .ts files
typescript-pubs() { html-pubs ~/git/languages/TypeScript; }
v8-pubs() { html-pubs ~/git/languages/v8; }
linux-pubs() { html-pubs ~/src/linux-5.0.3; }

to-html() {
  local dir=$1
  local num_results=$2
  local num_lines=$3
  local num_files=$4

  html-header

  cat <<EOF
  <body>

    <h2>URLs and dates in <code>$dir</code></h2>

    <p style="">
      $num_results results (searched $num_lines lines in $num_files source files)
    </p>
    <p>
      This page was
      <a href="https://github.com/oilshell/blog-code/tree/master/grep-for-papers">generated
      with shell scripts.</a>
    </p>
    <pre>
EOF

  # TODO: HTML escaping would be better
  awk '
  match($0, "([^:]+):([0-9]+):(.*)", m) {
    filename = m[1]
    line_num = m[2]
    snippet = m[3]

    # Horrible HTML escaping.
    gsub("&", "\\&amp;", snippet);
    gsub("<", "\\&lt;", snippet);
    gsub(">", "\\&gt;", snippet);

    # Make URLs into links
    # Some source has URLS <http://like-this> or (http://like-this)
    # The former is hard to detect because we would need to not match &gt;
    gsub("(https?://[^)[:space:]]+)", "<a href=\"&\">&</a>", snippet);

    print "<a href=\"" filename ".html#L" line_num "\">" filename ":" line_num "</a> " snippet "<br/>"
  }
  '

  cat <<EOF
    </pre>

    <hr/>
    <p style="text-align: right; font-style: italic;">Generated on $(date)<p>

  </body>
</html>
EOF
}

"$@"
