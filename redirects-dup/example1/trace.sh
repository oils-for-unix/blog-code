#!/bin/bash

# -ff : follow forks
strace -ff -o r1trace -e dup2,fcntl,open,close,write -- ./r2.sh
