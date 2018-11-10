# fgrep-problem-benchmarks

The "fgrep problem" is to match a set of fixed strings in a corpus.  The
matching can be done "in parallel" by a DFA.

There are various methods to generate the DFA.

See the top of `fixed-strings.sh` for instructions on running these benchmarks.

[Lobste.rs Discussion about Aho-Corasick Algorithm](https://lobste.rs/s/fq8uil/aho_corasick)

## DFA Visualizations

[DFA for Benchmark Problem](https://raw.githubusercontent.com/oilshell/blog-code/master/fgrep-problem-benchmarks/_gen/fixed-strings.png)

Simpler DFA for `"do" | "done" | "break"`

![Simpler DFA](https://raw.githubusercontent.com/oilshell/blog-code/master/fgrep-problem-benchmarks/_gen/trie.png)

## Code Size

[GrepFixedStrings() has 791 bytes of code](https://raw.githubusercontent.com/oilshell/blog-code/master/fgrep-problem-benchmarks/_gen/code-size.txt).  It has one or two variables, so all of them should fix in registers.

