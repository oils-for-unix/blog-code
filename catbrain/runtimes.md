Catbrain Runtimes and Commands
-------------


## Intro

- `cb-pure` - a language with no input or output
  - WASM runtime 
  - no memory allocation - globals

- `cb-filter` - stdin/stdout/argv/env/status - Unix filter like awk
  - basic Unix cat/tac/echo
  - pid
  - no memory allocation - fixed

- `cb-sh` - everything a shell has?  synchronous runtime?
  - arbitrary I/O and syscalls
  - exec
  - wait

  - unfortunately we can't share the runtime?  Because we have SmallStr?
  - it would be nice
  - async runtime

- `cb-ev` - shell event loop?
  - node.js style runtime

- `cb-busy` - workloads
  - can start threads, e.g. so you can inspect them
  - fork
  - malloc

- `cb-bad`
  - I don't know all of these
  - seg faults
    - dereference null
    - divide by zero
  - ubsan - integer behavior
  - asan - overflow
  - syscalls?
  - blowing the C call stack
    - how?
    - I think you just create a malicious stack


## Details

### cb-pure

    c const  - load a string

    const 'foo'
    const [my list]

Control flow

    for while
    if case

Abstraction

    fn

### cb-sh

    x ls
    extern ls

    redir

### cb-event, cb-async, cb-ev

need a name for this

### cb-sed

    
### cb-worker

- threaded runtime

### cb-evil

- seg fault, etc.

## Naming

- cat-pure
  - this is definitely a different binary
- cat-sed
  - this can't open any files?  It has POSIX regex bindings?
- cat-sh
- cat-ev
- cat-worker
  - not sure if pthreads really needs to be separate?  Is it different than the event loop?
- cat-evil
  - this is definitely a different binary



