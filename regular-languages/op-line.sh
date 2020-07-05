# Filter lines

egrep-task() {
  local text=$1
  local pattern=$2

  echo -n 'egrep '
  echo "$text" | egrep "$pattern"
}

sed-task() {
  local text=$1
  local pattern=$2

  echo -n 'sed   '
  echo "$text" | sed "/$pattern/p"
}

awk-task() {
  local bin=$1
  local text=$2
  local pattern=$3

  echo -n "$bin  "
  echo "$text" | $bin "/$pattern/ { print }"
}

mawk-task() { awk-task mawk "$@"; }
gawk-task() { awk-task gawk "$@"; }

libc-task() {
  ### bash is linked against libc

  local text=$1
  local pattern=$2

  echo -n 'libc  '
  # note: pattern can't be quoted
  [[ "$text" =~ $pattern ]] && echo $text
}

zsh-task() {
  ### bash is linked against libc
  local text=$1
  local pattern=$2

  echo -n 'zsh   '
  # note: pattern can't be quoted
  zsh -c '[[ "$1" =~ $2 ]] && echo $1' dummy "$text" "$pattern"
}

python-task() {
  local text=$1
  local pattern=$2

  echo -n 'py    '
  python -c '
import re, sys

pattern, text = sys.argv[1:]
#print(pattern)
#print(text)

# Assumed to match
if re.match(pattern, text):
  print(text)
' "$pattern" "$text"
}

perl-task() {
  local text=$1
  local pattern=$2

  echo -n 'perl  '
  echo "$text" | perl -n -e "print if /$pattern/"

  # https://stackoverflow.com/questions/4794145/perl-one-liner-like-grep
}

