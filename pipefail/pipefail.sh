#!/bin/bash
set -e -o pipefail
printf '%65538s' | head -c 1
echo "this is not executed"
