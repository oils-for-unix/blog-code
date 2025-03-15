#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

null-sql() {
  echo '
CREATE TABLE test (
  id INTEGER PRIMARY KEY,
  val1 INTEGER,
  val2 INTEGER
);

INSERT INTO test VALUES (1, NULL, 0);

-- This is to test that there is actually output
SELECT * FROM test;
SELECT "---";

SELECT * FROM test WHERE val1 = val2;
'
}

string-case-sql() {
  echo "
CREATE TABLE items (
  id INTEGER PRIMARY KEY,
  name TEXT,
  status TEXT
);

INSERT INTO items VALUES
  (1, 'Apple', 'active'),
  (2, 'Banana', 'ACTIVE'),
  (3, 'Cherry', 'Active');

SELECT * FROM items WHERE status = 'active';
"
}

compat() {
  for test in null string-case; do
    echo "*** $test"

    echo '    sqlite3'
    ${test}-sql | sqlite3
  done

  # TODO: Test on mysql and postgres
  #
  # Claude AI says sqlite and postgres agree, where mysql disagrees because of its NULL handling.
  #
  # I guess I can use an SSH tunnnel?  Or run it directly on the machine
}

"$@"
