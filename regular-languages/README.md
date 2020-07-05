Engine Support For Regular Languages
====================================

This is some research for Eggex.

    ./compare.sh regex-bracktrack

Result: As you would expect, Perl and Python backtrack, but
bash/zsh/egrep/awk/sed don't.  (bash and osh use libc's `regexec()`.
Not sure what zsh uses.)

    ./compare.sh glob-bracktrack
    ./compare.sh fnmatch-backtrack

Result: Perl, Python, and bash/mksh internal glob backtrack.
dash/ash/osh don't.  (osh uses libc's `glob()` and `fnmatch()`, but
bash doesn't).

    ./compare.sh greedy

Result: They're all greedy.  (sed has some issues related to the
semantics of `s` and implicit `.*` at the front.

Only Perl and Python have the nongreedy `.*?` operator.

    ./compare.sh submatch

Result: they all have the same behavior.  Is there a better test?

## Interpretation

- `osh` doesn't backtrack anywhere!  That's just because it uses libc.
- None of the GNU tools tested backtrack.
- `bash` backtracks on glob and fnmatch, but not regex.  That is, its
  internal implementations backtrack, but the ones delegated to libc
  don't.

## TODO

- Test musl libc in addition to GNU libc.
- Test on BSDs and OS X.  Apparently globs are exponential time:
  - https://research.swtch.com/glob
- What other divergences can we find?  Among:
  - Perl/Python
  - shells / libc / grep / sed / awk

## Operations

Regex:

- `op-line` prints a line if it matches a regex
  - egrep, sed, mawk and gawk, libc (via bash), python, perl
- `op-match` prints the matching portion
  - egrep, sed, gawk, libc (via bash), python, perl
- `op-submatch` prints the first submatch
  -  sed, gawk, libc (via bash), python, perl

Other:

- `op-glob`: `glob()` and `fnmatch()` via shell

