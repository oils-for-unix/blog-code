# Print the whole match (usually $0)

egrep-match() {
  local text=$1
  local pat=$2

  echo -n 'egrep '
  # -o for only matching portion
  echo "$text" | egrep -o "$pat"
}

sed-match() {
  local text=$1
  local pat=$2

  echo -n 'sed   '
  #echo "$text" | sed -r -n 's/'"$pat"'/&/p'

  # you need these extra .* in sed.  Because of the way the 's' command works.
  # But that breaks some stuff

  # https://stackoverflow.com/questions/2777579/how-to-output-only-captured-groups-with-sed/43997253

  echo "$text" | sed -r -n 's/.*('"$pat"').*/\1/p'

  #echo "$text" | sed "/$pat/p"
}

gawk-match() {
  local text=$1
  local pat=$2

  echo -n 'gawk  '
  echo "$text" | gawk 'match($0, /'"$pat"'/, m) { print m[0] }'
}

libc-match() {
  local text=$1
  local pat=$2

  echo -n 'libc  '
  [[ "$text" =~ $pat ]]
  echo ${BASH_REMATCH[0]}
}

python-match() {
  local text=$1
  local pattern=$2

  echo -n 'py    '
  python -c '
import re, sys

pattern, text = sys.argv[1:]
#print(pattern)
#print(text)

# Assumed to match
print(re.match(pattern, text).group(0))
' "$pattern" "$text"
}

perl-match() {
  local text=$1
  local pat=$2

  # I can't figure out how to do the equivalent of $0 in Perl?
  echo -n 'perl  '
  echo "$text" | perl -n -e '$_ = /('"$pat"')/; print $1'
  echo
}

js-match() {
  local text=$1
  local pattern=$2

  echo -n 'js    '
  nodejs -e '
//console.log(process.argv)
argv = process.argv
var text = argv[1];
var pattern  = argv[2];
var m = text.match(pattern);
console.log(m[0]);

' "$text" "$pattern"
}

