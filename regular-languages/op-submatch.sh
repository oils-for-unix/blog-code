# Print a whole match (usually $1)

sed-submatch() {
  local text=$1
  local pat=$2

  echo -n 'sed   '
  echo "$text" | sed -r -n 's/'"$pat"'/\1/p'
}

gawk-submatch() {
  local text=$1
  local pat=$2

  echo -n 'gawk  '
  echo "$text" | gawk 'match($0, /'"$pat"'/, m) { print m[1] }'
}

libc-submatch() {
  local text=$1
  local pat=$2

  echo -n 'libc  '
  [[ "$text" =~ $pat ]]
  echo ${BASH_REMATCH[1]}
}

python-submatch() {
  local text=$1
  local pattern=$2

  echo -n 'py    '
  python -c '
import re, sys

pattern, text = sys.argv[1:]
#print(pattern)
#print(text)

# Assumed to match
print(re.match(pattern, text).group(1))
' "$pattern" "$text"
}

perl-submatch() {
  local text=$1
  local pat=$2

  echo -n 'perl  '
  echo "$text" | perl -n -e '$_ = /'"$pat"'/; print $1'
  echo
}

