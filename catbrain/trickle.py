#!/usr/bin/env python3

import sys
import time

chunk_size = int(sys.argv[1])
iters = int(sys.argv[2])
secs = float(sys.argv[3])

for i in range(iters):
    chunk = sys.stdin.read(chunk_size)
    if not chunk:  # EOF
        break
    time.sleep(secs)
    sys.stdout.write(chunk)
    sys.stdout.flush()

# Cut off the input
