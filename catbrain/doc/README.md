catbrain
========

## Slogans

    A { Tcl, Lisp, Forth } that can express
      { Shell, Awk, Make, find, xargs } and
      { Python, JavaScript and node.js event loop, R data frames } and
      { YAML, Dockerfiles, HTML Templates, ...}  and
      {JSON, TSV, S-expressions, ...} ?

Shell is the Language of

- Process-based Concurrency
- the Control Plane - also xargs -P, make
- Inter-Process Communication - Byte and Text streams over Pipes

But catbrain is also:

- Coroutines-based concurrency
  - because coroutines are good for controlling concurrent Unix processes
- MAYBE Data Plane 
  - Awk and R need to be fast
  - we will have a fast GC and interpreter ... but we might need static types
    too, not sure
- Intra-process communication
  - embeddable/extensable in C - like Lua, Tcl, Wren, ...
  - We might also be able to memcpy() heaps between threads?
    - threads trust each other - processes don't

Slogan for async features:

  Processes, Pipes, and Robust "forward" parsing
  Queues/Backpressure
  Timeouts/Cancellation

- The future of shell is "asynchronous / event-based"
  - e.g. for embedding in a GUI

- Closer to the metal than most small Lisps/schemes!
  - designed to talk to operating system kernels
  - it's designed around an efficient GC
  - Lisps aren't great for parsing!  catbrain has more locality
    - we will have a special `[_type Token]` field I believe
- Closer to the user than Lisp!
  - easy to type syntax, that can be used directly

## Influences

Flavors of:

- POSIX shell - words
- YSH/Tcl/Ruby for the { } blocks
- Tcl (which is shell + Lisp)
  - also has [] and {} evaluation model
- jq 
  - because it has an implicit "this" or satck
  - it has not variables!  (jq has variables, but you do most things without
    them)
- Forth because it has a stack

For the runtimes:

- node.js - event loop/async runtime, with the self-pipe trick for process
  completion?
  - also works on Windows

### es shell Influence

    Tcl      =               shell + Lisp
    es shell =         Tcl + shell + Lisp
    catbrain = Forth + Tcl + shell + Lisp

### Comparisons

- [Shell vs. Catbrain](shell-vs-catbrain.md)
  - similar syntax, has "words", meant for typing
  - oriented around ARGV and ENV interface, but we add Lisp-like recursive data structures
- YSH vs. Catbrain
  - also has block args, but uses them for EVERYTHING, including control flow, fn, etc.
  - catbrain is intended to be faster, for the data plane too
  - catbrain is an embeddable / extendable / sandboxed / pure language; YSH is
    a shell language
- [Tcl vs. Catbrain](tcl-vs-catbrain.md)
  - In Tcl, everything is a string.  There are special dynamic parsing rules
    for splitting and command blocks.
  - catbrain is statically parsed, and it has `Error Str List Obj Fn` types
- YSH vs. Catbrain
  - YSH is for "using at work" (familiar to Python and JS programmers)
  - Catbrain is a bit esoteric - for Forth, Tcl, Lisp users
- vs. Forth
  - catbrain has a stack, but it's block-structured like ALGOL
- vs. jq: it's command-based, rather than expression based (and doesn't have cross
  product aka "PEG backtracking semantics")
- brainfuck: it's also minimal, with a "basic input and output" model `. ,`
  - but catbrain programs are not "obfuscated"
  - it's designed to be very readable, within the constraints model

## Features

- Extendable
  - provide your own functions - you can provide the user with arbitrary
    computation and I/O
- Well specified grammar 
  - PUNTING ON THIS: Syntax is a subset of YSH

## Where did catbrain come from?

See [story.md](story.md)


## 4 Runtimes

See [Runtimes][runtimes.md]

## Help Wanted

- TODO: Python prototype with test cases
- Example programs should work

## Programs It can Run

- cat
- CGI hello
  - print env as J8 notation
  - print argv as J8 Notation
  - can it parse HTTP post?
- spec/bin
  argv - definitely - tnet equivalent
  printenv
- write arbitrary TSV8
