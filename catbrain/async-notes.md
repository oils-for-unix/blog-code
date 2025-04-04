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

### More detailed History

There was the "Tulip" experiment, mentioned in the PEP.  I wonder if that was
influenced by Beazley's work

- Python 3.4 released asyncio library:
  - https://docs.python.org/3/whatsnew/3.4.html
  - asyncio: New provisional API for asynchronous IO (PEP 3156).
- Python 3.5 was released in 2015, with async/await syntax.  
  - https://docs.python.org/3/whatsnew/3.5.html
  - And the whole asyncio library relied on it.

- Python 3.6 (2016) and 3.7 (2018) added improvements

### Related stdlib features

- multiprocessing.Pool
  - process pool, uses Pickle
  - this module is fraught with problems
- concurrent.futures.ProcessPoolExecutor
  - I saw Beazley use this in a talk

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

### Some Lessons Learned on multiplexer

- type annotation: AsyncIterator[Event]
  - for 'yield' within 'async def'
  - AsyncGenerator[None,Event] - for type

- I am not sure we need that?   yield vs. await is interesting?
  - can you always simulate it with queues

- IncompleteReadError from readexactly()
  - I don't like this exceptions

- hm static types are nice to learn the API
  - Python does feel a bit unstructured


---

- there is `async wait_for(timeout)`
  - I wonder if Beazley goes over that implementation
  - I guess it would set a timer on the scheduler, and then cancel that task 
  - how do you cancel a task?

### TODO

- add timer to kill processes randomly
  - await sleep()
  - that is a feature

- add read() timeouts
  - or maybe you just have process timeouts?
  - that is more robust I think
  - but yeah you need to figure out how to cancel

- this example has pipes, processes, and queues
  - and it has user space protocol errors, and library errors
  - and now you need sleeping, and timeouts

## Notes on old experiments

- find your old fly/xmap code?
  - Surprisingly, I only found it on the google code archive!
  - I'm glad they did that
  - I archived the .zip files in git annex
- I don't have a complete list of other repos, but at least they all have wiki pages
  - (I also need to archive Zulip now)

---

What did each one do?

- xmap was like xargs
  - it used "torn", my fork of tornado
  - I was understanding async processes

- fly was basically PGI which is FANOS coprocesses
  - I added unix domain sockets and terminals later
  - I think they were both built on "torn"
  - surprisingly, it used threads and a mutex file?
  - maybe this led to the "Torn" experiment


### Found it

andy@hoover:~/hg/xmap$ hg log streams.py

changeset:   103:9186352c763b
user:        Andy Chu
date:        Mon Apr 30 16:51:47 2012 -0700
summary:     Factor out the streams library.


I didn't like writing the stateful TNET parser!

Tornado used EventEmitter, which may have been based on the node.js API?

Although of course Twisted was before that.  It was probably an abstraction
from Twisted.

---


 from torn import base
 import tnet
 from util import log

 # States for netstring parser
 _NEED_LENGTH = 0   # initial state, we don't know how many bytes we need
 _HAVE_LENGTH = 1   # we know how many bytes we need, but haven't gotten them yet


 class TnetValueStream(base.EventEmitter):
   """Wraps a readable file-like emitter.

   It registers itself as a listener for 'data', and then emits complete 'value'
   events.  The 'close' event is echoed.
   """

