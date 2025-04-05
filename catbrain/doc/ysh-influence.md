Catbrain influences YSH?
======

## Lessons

- procs and funcs aren't orthogonal
  - they can both take typed args, which aren't `extern`
  - they can both be pure - Hay
  - they can both use a fast bytecode runtime - again imagine huge Hay configurations
  - they can both use the async runtime

## "Accepted" Syntax Changes

- the `-` for appending to the stack
- the `^` for getting the top value 
  - in expression mode
  - in command mode
- the %error value, I think

Note: ^ sorta conflicts with ^(echo hi) and ^[x+y] and ^"echo hi"

If we really wanted, we could change that to

  %(echo hi)
  %[x+y]
  %"echo hi"

  %error  # special value
  %true %false %null are synonyms

Maybe we do a soft deprecation

Those are like "literals"?  Unevaluated?

Or maybe

- :(echo hi)
- :error  # the problem is that this looks ugly combined with `{k: v}`

## "Accepted" Runtime changes

- value stack
  - funcs and procs are still call / return, but you can control whether they
    are on the value stack or not
  - solves the "errors as exceptions" problem
  - enhances interactive experience
    - the "forth-like" words
    - but this is a forth-like stack
    - you can conctenate words, like 'sudo ls /etc` and `ssh myserver ls hi`
    - you can also concatenate COMMANDS, by using ^
      - add 0;
  - solves the Hay problem
  - List { - foo } is nice

- should be a bytecode interpreter
  - so break continue aren't exceptions

- HUGE: async runtime, or pluggable runtimes
  - xargs -P / ninja problem, etc.
  - how to show logs from parallel processes
  - distributed shell, more generally

Overall, we are reducing reliance on C++ exceptions

- the value stack
  - with nested, structured errors
- the %error value
- the bytecode change

Not sure:

- proc func unification

- proc block unification
  - I think this is OK, because you can do block.toProc() , and then invoke it
  - it's a literal piece of code

Punting on:

- embedding API, for now


- error OBJECTS - `__error__()` is true?
  - does this mask data?
- capability OBJECTS - `__cap__()` ?

### Any prior art for async shells?

- Only one I can think of is the Julia library
  - because Julia uses libuv!
  - and libuv uses Unix primitives or IOCP under the hood
  - TODO: maybe I should build a minimal libuv hello world

- Julia REPL is written in Julia too?
  - but it's not a shell ... TODO: try out  running multiple pipelines in Julia

## Justifications

Batch:

- Python speed (or more), instead of shell speed
  - Will C wanted to due Awk-like stuff, and Awk is fast
  - and there is also the C++ exception issue, where we are slower than other shells
  - this is "data plane" vs. "control plane"
- because I wanted to make YSH the language of process-based concurrency, for
  xargs -P/Ninja/process supervisors (the aurea project is basically a process
  supervisor with an RPC protocol)
  - and you need **coroutines** with async/await to control processes - this is
    the most natural way

Interactive:

- Koichi wrote shell in shell
  - ble.sh may be more driven by keyboard events
- Fish shell uses threads; that's why they ported to Rust
  - we can use coroutines
- Subhav and #shell-gui
  - a web shell might benefit from coroutines too?

Not for YSH, but for catbrain:

- intra process glue, not just inter-process glue
  - some things happen in the same process
  - we should make "glue" orthogonal from whether it's intra-process or inter-process
  - C ABI blog posts - C ABI is still the ultimate intra-process glue
- again Koichi wrote shell in shell
  - ble.sh may be more driven by keyboard events
  - we need a strict separation/reification of the VM !!
  - I want to make YSH VMs in YSH, and catbrain VMs in catbrain
    - YSH is close to that, but it's not easy.  We MAY be able to refactor to
      it

- Maybe: terminal click
  - they did not get rid of the shell; they wrote a shell inside a terminal
    emulator (globbing, etc.)
  - I think the **intra-process** glue might be better for some things
  - So yeah I want people to be able to put a shell inside the SAME PROCESS as
    a terminal
    - although dealing with the I/O is going to be very interesting
    - I'm not sure if it will need a global event loop
    - should look up GUI event loops ... Windows message  pump, etc.?  SDL?
- Look at what ghostty does -- does it **own** the main?

- https://claude.ai/chat/5cfbf712-0d41-45a1-accb-5cceb27c948e
  - Yes it's the message pump / event loop on windows
  - OS X - NSApplication run method
  - Linux: GTK and windows have signals and slots

## YSH vs. Catbrain

Main differences

- ad hoc registers vs.  implicit value stack - ACCEPT
  - `_error` and `_pipeline_status` and `_match()` etc. 
  - and `_hay()` register!  This doesn't have to be magic!!
  - it can just be a value stack

- error builtin throws "invisible" exception, versus explicit %error value
  - in other words, a value.Error, that can appear in a Dict
    - although actually I don't know how to make it appear in a dict key ...
    - maybe it can only appear in the value


- sync vs. async - ACCEPT, even though it's a lot of work

- intra-process (C linking) vs. inter-process

- Proc+Block vs. Fn only 

- Proc+Func vs. Fn only
  - honestly there are some Perlis-Thompson issues with proc vs. func
  - example: purity
  - `proc p [pure] (x, y) { echo hi }`

- commands+expressions vs. commands only
  - most users would want Python/JS expressions
  - and catbrain has no solution for eggex - ERE syntax sucks kinda
    - although I guess catbrain should be fast enough to implement string
      parsing, and you can do it yourself

- Single expression, single block arg - vs arbitrary arguments
  - this was bar-g feedback
  - () args, and {} args?

- implicit extern vs. explicit extern
  - `x ls` etc.
  - this can be controlled by a MODE?
  - or is it a feature of procs and funcs?

### Registers vs. Implicit value stack

- definitely `_pipeline_status` needs to change
- the stack seems RISKY, but potentially  nice

Right now shell has `$_` - the last argument

I kind of like the idea of the last VALUE

- %[top] or %%[top]]  # in catbrain
  - that can be `$[_top]` or maybe `$[_t]`
- what about `%[pop]` and `%%[pop]]`

See [ysh-stack.md](ysh-stack.md)

### Pipeline status

ls | grep | wc -l

[status: [0 1 0]]

[%error [pipeline [0 1 0]]]

### Implicit error builtin and try, or errors as values

Key issue:

- you can *return* an  error too
  - not just throw it

```
func f {
  return %error
  return { %error: {foo } }
  return { '0': %error }  # quotes required
}
```

- Or is it {0: %error}
  - a special value associated with the string [0]
  - sort of like NIL8

I liked the Zig idiom 

    var x = foo() catch |x| switch (err) { ... }

- it has the concept of an error
- so YSH can have a concept of an error value


Right now we have

   try { 
     foo
   }
   if failed {
     echo hi
   }

and then there is

   try { foo }
   if failed {
     echo hi
   }

How about

    foo !(err) {
      echo failure
    }
    foo !{
      echo failure
    }

    # problem is that  || already means something
    foo || {
      echo failure
    }

    # this is not horrible
    foo ||| {
      echo failure
    }

    if failed {
      echo hi
    }

Catbrain doesn't have an idiom for this, it only has `& x -- y` literals

It could be

    myproc &(func-sig) {
      echo func
    }
    myproc &&(proc-sig) {
      echo func
    }

    myproc || &(err) {
      echo func
    }

    myproc ||| {
      echo $[_error.code]   # I think ||| could still be OK
    }

    # actually this is probably the best
    # you're not passing -- you're handling errors
    #
    # I also wonder if we should get rid of ? as a glob char
    myproc ?? {
      echo $[_error.code]   # I think ||| could still be OK
    }

    # pipelines and process sub
    diff <(sort left) <(sort right) && {
        echo bad
    }

    ls | wc -l | hi && {

        = _error['0'] or _error.0 can be allowed
        = _error.code  - this is a summary of all the status?   not sure

        = _error.status

        = _error.pipe_codes
        = _error.psub_codes

        = _error.pipe_status  # not _pipeline_status
        = _error.psub_status  # no - _process_sub_status
    }

This is an idea for handling errors RIGHT when they happen

But you still have

   try {
     myproc
     myproc-2
   }
   if failed {   # failed builtin now means "TOP Of STACK"[0] === %error
     echo `$[_error.code]
   }

### Synchronous/Blocking vs. Async 

Problems to solve:

- how to show logs from parallel processes
  - enhanced xargs -P
  - ninja
  - zig build system
- ble.sh also has a very state machine approach
  - oh yeah because the *interactive* loop is actually a select()!
  - `strace bash` shows that
  - although `strace dash/mksh` don't, and surprisingly `strace zsh` doesn't either?

Complexities in the shell runtime:

- job control
  - the Zed editor bug
- the "Starship bug"
  - DEBUG trap + job control + ... ?

### Proc+Block vs. Fn only 

catbrain has

   cd /tmp { echo hi }

   cd /tmp &(x, y) { echo hi }

So &() is basically a signature object.  OK.  You just pass it

TODO: I think we can reserve that syntax

But probably discourage it, don't use it that much?

The other problem is the arbitrary arg binding?

Maybe for `cd` it "downgrades" the zero-arg proc to its own binding

Samuel feedback:

- Command type can't be run in current scope

---

    var b = ^(echo hi)
    b

### Proc+Func vs. Fn only

What's the difference in Oils?

- procs have 4 kinds of args; funcs have 2
- procs return integers; funcs return rich values
- philosophical - guide to funcs and procs
  - procs may be exterior
  - funcs are interior
  - EXCEPT Hay is INTERIOR, and uses procs
- procs don't break - because they are exterior
  - except

----

- Non-orthogonality
  - PURITY
  - which runtime: async, or shell

I have that "annotation" idea

```
proc p [pure] (x) {
}
```

And there was:

- `extern` - this is for procs that are external entry points
  - I guess this one is OK
- runtime:async
- runtime:fast
- are funcs a different language?
  - but Hay is based around procs, and Hay is also **pure**


So proc and func could be structured like CPython

- a VERY rich language
- but each one compiles to specific BYTECODES


- should "rich" procs return values, and leave them on the stack?

```
ysh$ Package foo
ysh$ = 
(Dict)  {type: 'Package', name: 'foo'}
```

Leaves the value on the stack

Honestly I want

    proc p [extern] (a, b, c) {
      return 1
    }
    proc p [extern] {
      # or is this a VALUE stack for this CALL stack frame
      echo @ARGV
      return 2
    }

And that's just a func?

Change the BINDING?  This would be huge

POSITIONAL vs. named would have to go though

- foo= could be magical?

```
Package foo=bar

Package foo=bar x=(expr) y={echo hi}
```

I suppose that is all possible


### Literals in catbrain

- [a b c]

:| a b c |





### commands+expressions vs. commmands only

- in catbrain, I figured out that, like closure, you can have dicts and lists invokable

```
mylist 0   # leaves first item on the stack
mydict .foo .bar  # leaves property
myobj .foo
```

So yeah everything can be invokable

In YSH, that's

```
- mydict.foo  # push it on the stack
```


- Single expression, single block arg - vs arbitrary arguments
  - this was bar-g feedback
  - () args, and {} args?

## implicit extern vs. explicit extern

   func f(io) {
     var x = io.extern

     x ls /tmp
   }

   proc p {
     # allowed by default?
     ls /tmp

     x ls /tmp
   }

I still have to figure out the mechanism for getting rid of io

I think maybe there is a CAPABILITY flag?

- Obj has `__cap__() { return true }` method?
  - as long as `__cap__` exists, like `__invoke__`, then it can't be accessed
    as a global variable?

- So the capabilities are
  - io
    - this includes io.extern?
    - but maybe you can have a separate invokable object `x`
    - `x` just points to `io.extern`, which is an invokable object?  But does
      it wrap the BuiltinProc `extern`?
  - vm


## On the other hand - catbrain has naive scope?

- Closures for Command/Expr/Proc/Func solve a real problem
- The implicit value stack isn't explicit enough


## catbrain literals

- 'str'
- [my list]
- { echo fun }
- &(x, y) { echo fun }
  - or the more abstract & x -- result { x }
  - inspired by es shell, which uses @ i { echo hi }

## Older Ideas

- I wonder about this syntax:
  - filter [age > 1]

- instead, it could be
  - filter ^[age > 1]
  - synonym for filter (^[age > 1])

---

In catbrain, we have % and ^

- % is OK I guess
- Does ^ mean two things?  It means "pop", and it means Unevaluated
  - maybe it could be * or !

```
ls !
ls !!  # splice it

```

That char also has the "history" connotation

But it's the last VALUE, not the last command

