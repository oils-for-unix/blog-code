# Print a whole match (usually $1)

sed-submatch() {
  local text=$1
  local pat=$2
  local submatch=${3:-1}

  echo -n 'sed   '

  set +o errexit  # might not be there
  echo "$text" | sed -r -n 's/'"$pat"'/\'$submatch'/p'
}

gawk-submatch() {
  local text=$1
  local pat=$2
  local submatch=${3:-1}

  echo -n 'gawk  '
  echo "$text" | gawk 'match($0, /'"$pat"'/, m) { print m['$submatch'] }'
}

libc-submatch() {
  local text=$1
  local pat=$2
  local submatch=${3:-1}

  echo -n 'libc  '
  [[ "$text" =~ $pat ]]

  set +o nounset  # we might be asking for one that's not there
  echo ${BASH_REMATCH[$submatch]}
}

python-submatch() {
  local text=$1
  local pattern=$2
  local submatch=${3:-1}

  echo -n 'py    '
  python -c '
import re, sys

pattern, text, submatch = sys.argv[1:]
#print(pattern)
#print(text)

# Assumed to match
print(re.match(pattern, text).group(int(submatch)))
' "$pattern" "$text" "$submatch"
}

perl-submatch() {
  local text=$1
  local pat=$2
  local submatch=${3:-1}

  echo -n 'perl  '
  echo "$text" | perl -n -e '$_ = /'"$pat"'/; print $'$submatch
  echo
}

js-submatch() {
  local text=$1
  local pattern=$2
  local submatch=${3:-1}

  echo -n 'js    '
  nodejs -e '
//console.log(process.argv)
argv = process.argv
var text = argv[1];
var pattern  = argv[2];
var submatch = parseInt(argv[3]);
var m = text.match(pattern);
console.log(m[submatch]);

' "$text" "$pattern" "$submatch"
}

