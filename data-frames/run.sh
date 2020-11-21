#!/bin/bash
#
# Run the same analysis in 5 languages/libraries.
#
# Usage:
#   ./run.sh <function name>
#
# See README.md for instructions.

set -o nounset
set -o pipefail
set -o errexit

install-r() {
  sudo apt install r-base
}

# NOTE: This takes awhile to download and compile!  But it's worth it.
install-dplyr() {
  sudo Rscript -e 'install.packages(c("dplyr"), repos="https://cran.us.r-project.org")'
}

install-pandas() {
  pip3 install pandas
}

all() {
  echo
  echo '--- With dplyr in R ---'
  echo

  ./with_dplyr.R

  echo
  echo '--- With base R ---'
  echo

  ./with_base_R.R

  echo
  echo '--- With Pandas in Python ---'
  echo

  ./with_pandas.py

  echo
  echo '--- Python without Data Frames ---'
  echo

  ./without_data_frames.py

  echo
  echo '--- With SQL (in shell!) ---'
  echo

  rm -f $DB
  csv2sqlite
  with-sql
}

readonly DB='traffic.sqlite3 '

csv2sqlite() {
  sqlite3 $DB <<EOF
.mode csv
.import traffic.csv traffic
EOF
}

with-sql() {
  sqlite3 $DB <<EOF
SELECT 'Rows:';
SELECT date, url, num_hits FROM traffic;

SELECT '';
SELECT 'Daily Traffic:';  -- silly way to print
SELECT date, SUM(num_hits) FROM traffic GROUP BY date;

SELECT '';
SELECT 'Popular Pages:';

-- Style from blog post
SELECT url,
       SUM(num_hits) * 100.0 / (SELECT SUM(num_hits) FROM traffic)
       AS percentage
FROM traffic
GROUP BY url
ORDER BY percentage DESC;

EOF
}

# This selects from two tables.
# credit to jeb and terminus-est on lobste.rs
# https://lobste.rs/s/hnfc6a/what_is_data_frame_python_r_sql
with-cte() {
  sqlite3 $DB <<EOF
-- Use common table expression.  This table has a single column: the total
-- number of hits in the data set.
WITH     total (num_hits) AS (SELECT SUM(num_hits) FROM traffic)
SELECT   url,
         traffic.num_hits * 100.0 / total.num_hits AS percentage
FROM     traffic, total
GROUP BY url
ORDER BY percentage DESC;
EOF
}

# Window functions use the "OVER" keyword.
# https://sqlite.org/windowfunctions.html

# Doesn't work?  Syntax error on line 1.  sqlite supports the WINDOW keyword
# for intermediate definitions.

with-window() {
  sqlite3 $DB <<EOF
SELECT date, url, num_hits FROM traffic;
EOF

  sqlite3 $DB <<EOF
WITH total_hits_per_url AS (
  SELECT url, sum(hits) AS hits
  FROM traffic
  GROUP BY url
)
SELECT url, hits * 100.0 / sum(hits) OVER () AS percentage
FROM total_hits_per_url
ORDER BY percentage desc;
EOF
}

"$@"
