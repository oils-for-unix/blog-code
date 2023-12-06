Regex Derivatives Experiments
=============================

## Older Experiments Related to Regexes and Computational Complexity

- <https://github.com/oilshell/blog-code/tree/master/fgrep-problem-benchmarks> (2018)
  (in this repo) - [re2c](https://re2c.org) is able to compile patterns like
  `aaa|bbb|ccc|...` in linear time, and match them in constant/sublinear time
  with respect to the number of alternations (N)

- <https://github.com/oilshell/blog-code/tree/master/regular-languages> (2021) - Perl
  and Python glob/fnmatch do exponential backtracking, but libc doesn't
  - Extended glob implementations (which give globs the power of regexes) backtrack

## Recent Experiments

- <https://github.com/andychu/rsc-regexp/tree/master/py> (2023) - BurntSushi
  answered my question about Rust ownership.  
  - fork of <https://github.com/BurntSushi/rsc-regexp>
  - Tangent: I ported the the regex-to-NFA compiler and multi-state simulation
    to typed Python

- <https://github.com/andychu/epsilon/tree/master/NOTES.md> (2023) - Somehow
  this got me back into regex derivatives, which I had long been interested in,
  but didn't understand.
  - fork of <https://github.com/MichaelPaddon/epsilon>
  - I refactored the code to a functional style, made it pass the tests from
    the BurntSushi repo.
    - See the `refactor/` directory
  - Got non-linear blowup on the "Russ Cox regex", and "the fgrep problem".
  - I referred to the links in my own 2020 blog post:
    <http://www.oilshell.org/blog/2020/07/ideas-questions.html#regular-expression-derivatives-papers-and-code>

## Related Threads

- <https://old.reddit.com/r/ProgrammingLanguages/comments/17tw4nc/which_languages_have_equality_hashing_and/>
  - I was excited about regex derivatives, and then I experienced the compile-time blowup in the epsilon implementation
  - Probably over-generalized the slowness from that implementation to the derivatives technique in general?
  - However it does appear there isn't a "single" agreed upon derivatives
    algorithm?  The canonicalization is non-trivial and affects the runtime and
    quality of the output?
  - How does the traditional PowerSet construction for NFA to DFA compare?  <https://old.reddit.com/r/ProgrammingLanguages/comments/17tw4nc/which_languages_have_equality_hashing_and/k96fdve/>

- <https://lobste.rs/s/pfigpn/neighborhood_infinity_three>
  - I mentioned the blowups I experienced, again may have over-generalized
  - good replies from Def / Frederic
  - and from Neel K -
    <https://semantic-domain.blogspot.com/2013/11/antimirov-derivatives-for-regular.html>

## Side Note: I believe Cloudflare Blog Post Explanation is Wrong

This blog post 

- <https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/>

is cited by the new .NET derivatives paper:

- <https://dl.acm.org/doi/abs/10.1145/3591262>

I think the problem is that they're using the Perl 5 regexp debugger to
demonstrated a bug.

But they are actually using PCRE, which is MUCH more sophisticated.

- I tried the pattern that caused an outage with `pcregrep`, and it didn't blow
  up.
- My guess is that you need to do submatch extraction to trigger the blowup.
  - But the blog post didn't mention submatch extraction.  It was only about
    matching.
  - This could be investigated a bit more by writing some C code against the
    PCRE API.  Can their pattern be matched in linear time, and does it blow up
    when submatches are requested?

## New Question

Computational complexity, "bad experiences" noted on from lobste.rs.

Use re2c as a baseline.

## Demos of Blowups in Epsilon

Commands to run in the `andychu/epsilon` repo, which tests the `refactor/` dir:

    ./run.sh fgrep-problem-blowup              # aaa|bbb|ccc|...

    ./backtrack.sh compare-synthetic-rsc-all   # a?a? ... aaa ...

## TODO:

- Create test harness for the two problems
  - a?a?a? ... aaa ...
  - aaa|bbb|ccc|...
    - move this one out of unit tests

- Do these tests against NFA implementation
- Do these tests against re2c?
- Then ask to plug in in say OCaml impls
  - add start and end params
