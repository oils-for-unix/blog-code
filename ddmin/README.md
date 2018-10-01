ddmin Refactoring
=================

A comment in this [lobste.rs thread][thread] linked to the original Python
implementation of the **ddmin** "minimizing delta debugging algorithm", by
Andreas Zeller.

It's small piece of code, so I decided to rewrite it into modern Python
to understand the algorithm better.

Here are some things to try:

    ./ddmin.py  # Zeller's version

    ./my_ddmin.py  # my version

    ./run.sh count  # my version is now all contained inone file

And then read `ddmin.py` vs `my_ddmin.py`.

I still haven't applied it to a practical problem, but I suspect it will help
me with [Oil](https://www.oilshell.org) bugs.  I've been knee-deep in many
large shell scripts!

Links
-----

[Morning Paper on "Simplifying and Isolating Failure Inducing Input"][morning]

[thread]: https://lobste.rs/s/gone7a/celebration_code_6_pieces_code_had_impact

[morning]: https://blog.acolyer.org/2015/11/16/simplifying-and-isolating-failure-inducing-input/

