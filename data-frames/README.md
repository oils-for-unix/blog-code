## What is a Data Frame?  Comparing R, Python, and SQL.

See the [companion article][blog-post] on the [Oil
blog](https://www.oilshell.org/blog/).

This directory has **five** different implementations of the same analysis on
[traffic.csv](traffic.csv):

- `without_data_frames.py` -- plain Python code.
- `with_dplyr.R` -- with the dplyr library in R.
- `with_base_R.R` -- with base R (no libraries).
- `with_pandas.py` -- with the Pandas library in Python.
- `run.sh` has a pure SQL solution with sqlite.

If you have all dependencies installed, you can run it like this:

    ./run.sh all

I tested it on an Ubuntu 16.04 machine.


### Dependencies

You may need to run some of these commands:

    ./run.sh install-r
    ./run.sh install-pandas
    ./run.sh install-dplyr  # This takes awhile

Look inside `run.sh` and adjust these functions for your OS, if necessary.

### TODO

- Julia?  Feel free to send me a patch to port this to DataFrames.jl.

[blog-post]: TODO
