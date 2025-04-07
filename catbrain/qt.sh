#!/usr/bin/env bash
#
# Testing the GUI with asyncio
#
# Usage:
#   ./qt.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

make-venv() {
  python3 -m venv _tmp/qt-venv
}

py-deps() {
  # I installed mypy
  . _tmp/qt-venv/bin/activate

  python3 -m pip install PyQT5 qasync
}

"$@"
