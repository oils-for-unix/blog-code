#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# Note: MariaDB agrees with Postgres and sqlite
null-sql() {
  echo '
DROP TABLE IF EXISTS test_null;
CREATE TABLE test_null (
  id INTEGER PRIMARY KEY,
  val1 INTEGER,
  val2 INTEGER
);

INSERT INTO test_null VALUES (1, NULL, 0);

-- This is to test that there is actually output
-- SELECT * FROM test_null;
-- SELECT "---";

SELECT * FROM test_null WHERE val1 = val2;
'
}

# Note: MariaDB still disagrees
string-case-sql() {
  echo "
DROP TABLE IF EXISTS test_string_case;
CREATE TABLE test_string_case (
  id INTEGER PRIMARY KEY,
  name TEXT,
  status TEXT
);

INSERT INTO test_string_case VALUES
  (1, 'Apple', 'active'),
  (2, 'Banana', 'ACTIVE'),
  (3, 'Cherry', 'Active');

SELECT * FROM test_string_case WHERE status = 'active';
"
}

compat() {
  local user=$1
  local pass=$2
  local db_maria=$3
  local db_postgres=$4

  for test in null string-case; do
    echo "*** $test"

    echo '    sqlite3'
    ${test}-sql | sqlite3
    echo

    echo '    mysql'
    ${test}-sql | mysql -h localhost -u $user -p$pass $db_maria
    echo

    echo '    postgres'
    ${test}-sql | PGPASSWORD=$pass psql -h localhost -U $db_postgres
    echo
  done

  # TODO: Test on mysql and postgres
  #
  # Claude AI says sqlite and postgres agree, where mysql disagrees because of its NULL handling.
  #
  # I guess I can use an SSH tunnnel?  Or run it directly on the machine
}

"$@"
