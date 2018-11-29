#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

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
SELECT 'Daily Traffic:';  -- silly way to print
SELECT date, SUM(num_hits) FROM traffic GROUP BY date;

SELECT '';
SELECT 'Popular Pages:';
SELECT url,
       SUM(num_hits) * 100.0 / (SELECT SUM(num_hits) FROM traffic) AS percentage
FROM traffic
GROUP BY url
ORDER BY percentage DESC;
EOF
}

"$@"
