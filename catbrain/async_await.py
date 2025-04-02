#!/usr/bin/env python3
#
# Demo from Claude AI

import asyncio

async def counter(start=0):
    count = start
    while True:
        # With async generators, we use yield directly
        reset_to = yield count
        
        # If we receive a value via send(), reset the counter
        if reset_to is not None:
            count = reset_to
        else:
            count += 1

# Usage with an async function:
async def main():
    # Create and initialize the async generator
    gen = counter(10)
    
    # We use __anext__ directly or the 'async for' syntax
    print(await gen.__anext__())  # Get first value: 10
    print(await gen.asend(None))  # Get next value: 11
    print(await gen.asend(None))  # Get next value: 12
    print(await gen.asend(5))     # Reset counter to 5
    print(await gen.asend(None))  # Get next value: 6

asyncio.run(main())
