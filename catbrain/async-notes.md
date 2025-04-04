Notes on async/await
----------------

## Python History

- generators were just 'yield' - I think Python 2.4
  - I guess this was similar to `__iter__`
  - next()
- Then you got yield and send() - maybe 2.5
- Then you got 'yield from'

And then you got async/await 

- with `asend()` and `gen.__anext__` or `async for`
- with `__await__`

key point: the FOR loop is no longer involved!

## User-Facing Features

- File descriptors
- Processes
- Queues
- Event Loops 


can you write your own scheduler and tasks?  seems like most people don't do
this.  Not sure if they will customize their event loop.

Key YSH/catbrain difference: you're not allowed to block!  In Python you can do
this.

Well the only way to block is with CPU.  I think that is OK.

We also have process pools to offload that work.  It's a coroutine + Unix
process architecture.

## Overall Archiecture and Mechanisms

From TOP to BOTTOM:
 
- library abstractions - Lib/asyncio
- Exceptions like StopAsyncIteration - part of Objects/
- magic methods like `__await__` - part of of Objects/
- Language keywords:
  - new is async/await
  - I don't think we need yield or yield from
- VM bytecodes
  - `YIELD_VALUE` and `RESUME`
  - `JUMP`

### Library Mechanisms

- Event Loop
- Scheduler - Tasks
  - calculate which tasks are ready to run -- which to call task.send(None)
    - is that like `__anext__`
    - file descriptors
    - queues
  - calculate deadlines for sleeping
- Future
- For processes
  - self-pipe trick

### Exceptions

- StopAsyncIteration
  - I want a sentinel value instead
- TimeoutError 
  - I want a sentinal value instead
- CancelledError - not sure

## Magic Methods / Protocols

- `__await__` I don't understand
  - makes an object "awaitable"
  - returns an iterator?  not coroutine - oh because it yields?
  - used to customize behavior when object is awaited.  Like the Awaitable

- `__aiter__` is like `__iter__`
- `__anext__` is like `__next__`
- `__aenter__` and `__aexit__` are like `__enter__ --exit__` - the `with`
  statement

YSH/catbrain - so do we have `__await__` magic methods then?

## Bytecodes

Python 3.12 is very different than the earlier byterun ones:

- 'await' and 'yield from'
  - `YIELD_VALUE` and `RESUME`
- `break` and `continue`
  - `JUMP`
- `return`
  - `RETURN_VALUE`
- what about calling a function?
  - `CALL`
  - `CALL_KW`
  - `PRECALL` - to prepare
  - `CALL_METHOD`
  - OK this kinda makes sense - it's optimized for speed.  Fewer conditionals

## TODO:

- netstring xmap example
  - and also we want to print when the process exits

- then port it to your own Lib/asyncio clone - using Beazley's notes

- then compile it to bytecode??  
  - Using compiler2?    That won't work
  - well you can use 'dis'

- and then implement that in your own pyvm2, without exceptions?

- then port the whole thing to catbrain/YSH!

## Claude AI

- first pass worked pretty well
  - need to test all sorts of errors
  - protocol errors
  - killing the process
  - maybe interleaved output and so forth
    - well you can write another filter to sleep between messages


