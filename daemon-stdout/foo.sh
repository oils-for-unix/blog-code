#!/bin/bash

exec ./foo.js "$@" >stdout_and_stderr.txt 2>&1
