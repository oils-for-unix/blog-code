Regex Derivatives Experiments
=============================

Previous experiments related to regular languages:

- <https://github.com/oilshell/blog-code/tree/master/fgrep-problem-benchmarks> (2018)
  (in this repo) - [re2c](https://re2c.org) is able to compile patterns like
  `aaa|bbb|ccc|...` in linear time, and match them in constant/sublinear time
  with respect to the number of alternations (N)

- <https://github.com/oilshell/blog-code/tree/master/regular-languages> (2021) - Perl
  and Python glob/fnmatch do exponential backtracking, but libc doesn't
  - Extended glob implementations (which give globs the power of regexes) backtrack

- <https://github.com/andychu/rsc-regexp/tree/master/py> (2023) - BurntSushi
  answered my question about Rust ownership.  
  - fork of <https://github.com/BurntSushi/rsc-regexp>
  - Tangent: I ported the the regex-to-NFA compiler and multi-state simulation
    to typed Python

- <https://github.com/andychu/epsilon/tree/master/refactor> (2023) - Somehow
  this got me back into regex derivatives, which I had long been interested in,
  but didn't understand.
  - fork of <https://github.com/MichaelPaddon/epsilon>
  - I refactored the code to a functional style, made it pass the tests from
    the BurntSushi repo.
  - Got non-linear blowup on the "Russ Cox regex", and "the fgrep problem".

## New Question

Computational complexity, "bad experiences" noted on from lobste.rs.

Use re2c as a baseline.

