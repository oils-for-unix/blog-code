Notes
=====

## 2025 Updates

### Rationale

- Coroutines and async runtime
- Powerful enough to parse arbitrary messages fast, quickly
  - it parses itself, so it's partly self-hosted
- embeddable and sandboxed

### Example program

- xargs -P
- ninja
- on Windows too


### Types

  - Error Str List Obj Fn 
    - Error type, in place of exceptions
    - no Null then?  try can turn %error into ''
      - yeah I think that is reasonable
  - Str used as Int and Bool; List used as Dict with PList representation
    - List has optional "HASH PART" - this is lazily computed whenever you do
      "getvar", on anything that's more than say 10 properties
      - so you don't use extra GC space on non-lists
  - Obj is a pair of List and Obj
  - fn is used for both proc and func

Place is not necessary?  I think you just use the 'command ...; assign foo pattern

### List literals

Since we don't have expressions, we should break YSH compat and add this

    echo [hi there]

    echo [hi %mystr %%mylist] {
      echo hi
    }

    make-dict {
      : key val
      : key %val
    }; assign foo

    const 's'; assign mystr
    const [a b [d e]]; assign mylist

    var mylist [a b [d e]]
    var mystr 's'

    var mymap [k v k2 v2]

    var mymap [k3 v3]

Consider different sigil, since it's not stringify

    echo %myvalue  # not just a string

    # what about interpolation

    ls --verbose=%val  # I think this should be allowed
                       # '--verbose=%val' is the way to quote a whole word?
                       # no backslashes

    echo @splice

    echo %%splice  # multiple, this is like * or **

    echo %[myvalue arg1 arg2]  # this is using a proc like a func, maybe call it fn
    echo @[myvalue arg1 arg2]  # splice it

    echo %%[myvalue arg1 arg2]  # splice it

    echo %[stdout { echo hi }]

    echo %[stdout {echo hi}]  # is it allowed?  could be

    # what about ()?  Reserved?

Maybe call it 'fn'.  since it's used for both


Yeah this is useful for breaking compaat

YSH uses [x > 3] as expressions

    stdout { expr 1 + 2 }; assign x

### external command, def, errors

- fn takes an array of values; external command only takes strings
  - extern ls foo
  - / ls foo

- fn can leave arbitrary value
  - external command leaves '0' to '255'
    - how to we avoid conflating the result, and failure?
  - or maybe it leaves a special error value - this is a map

```
[:error [status 255 msg 'foo']]  
```

### try turns :error into 'caught'

   cb$ false
   [:error [status 1]]
   [:error [status 1]]

   cb$ try { false }
   [caught [status 1]]  # now you can inspect it

### Scope

- lexical scope

### Mutation

   clear! mylist  # just use ! maybe

### Methods

    obj method a b c  # OK so this object is invokable

    make-object [x 3 y 4] [__invoke__ print-mag other]; assign my-vec

    my-vec # => 5

### Implementation

- Cheney collector
  - using C++ compile time reflection to generate field masks again
  - although do I really have a lot of field masks? 
    - if the parser is written in catbrain
    - TODO: look at tinypy GC

- 32-bit int as pointer?
  - because you want to memcpy() the whole heap
  - the parser is self-hosted in catbrain, so this is useful for sending code across the wire
    - but then again, it's not a trusted format
    - it can be invalid
    - so you'd need some kind of pickle thing
  - then smallstr is only 2 bytes?  If NUL terminated

- async only runtime?
  - no special async
  - this makes it like Tcl, Forth, node.js (except everything is async/await)

### Self Hosting

- The parser is definitely self-hosted
- Not sure if the call stack is a catbrain data structure
  - sort of like Ribbit Scheme

### Homoiconicity

I think it is pairs of (TAG VALUE) or (TAG LOCATION VALUE)

    [WORD 'foo']     foo or 'foo'
    [LIST [a b c]]   [a b c] 

    [COMMAND [echo hi]]     echo hi
    [BLOCK [COMMAND [echo 1]] [COMMAND [echo 2]]]   { echo 1; echo 2}
    [PIPELINE [COMMAND [echo 1]] [COMMAND [echo 2]]]  cat foo | grep | sed

    [GETVAR [EXPR foo]]     %foo
    [SPLICE [EXPR array]]   %%array

TODO:

- everything need location info
- maybe it is similar to the HASH PART of the List?


LOCATION is just a map

    [id Lit_Chars
     col 5
     length 3
     line [source [file [name x]] ]]

- TODO:
  - need pretty printing

### Data format

- tagged varint

### No Expressions

    [EXPR foo 0 bz]   # this is the syntax %[foo[0].baz] ??
                     # or maybe lists and maps are callable
                     # [foo 0 baz]
                     # Yeah that isn't bad
                     # Objects have specific methods
                     # mylist 0
                     # myobject method
                     #
                     # Yes I like that
                     # So it's just a command

- Problem: can there be map keys that look like numbres?

    var mylist [55 foo 55 bar]

    mylist 55  # what does this give you?

    So I think you need

    mylist .foo .0 .bar
    mylist foo .0 bar  # for string keys, it's optional

    mylist 0  # this is always indexing
    mylist .0  # this is always property lookup


### fn

    fn foo -- a b -- result {  # what's left on the stack is checked
      echo
    }

    fn closed -- {
    }

    fn open {
      write %%ARGV  # special var?  Or just leave it out
    }

## Missing in the Oils Runtime

- Embeddable pure interpreter
  - e.g. for Hay-like "remote evaluation"

- Small String Optimization - immediate values

- zero allocation

- Reflection on YSH source code within YSH
  - exporting tht AST

- **Event loop**!   ASYNC RUNTIME FOR SHELL!
  - Maybe this is where I prototype it?

- **type checker** - static subset
  - string args, array args, block args
  - command args

- **code pretty printer** with comment placement issue

- Compiling `return` to control flow, not exceptions!

Example:

    def f {
      const-array a b
      foreach {  # iterates over the container on TOS
        if x test $_ = b {  # $_ is the top
          return            # should be control flow
        }
        w-line
      }
    }

---

- OK I want to make a small C++ version
  - and test it

### Missing in catbrain

- Interactive parsing - TODO: I want to do this
  - this creates ownership issues?
  - Or does it?
  - I'm thinking of the "backing lines" problem
- GC
  - an idea is to allow copying between VMs, rather than GC
  - rooting is still annoying

### Bernstein chaining / composable blocks

NOPE

    setvar s string { const foo; ch newline }
    setvar a array { const foo; getvar a; const bar }


I think it would need to be:

    setvar s (string { const foo; ch newline })
    setvar a (array { const foo; getvar a; const bar })

() means run the thing and then pop the top value?

() could always be the top ...  or `(_)` or `$[_]`


It's

    string { const foo; ch newline }    
    assign s

    string { const foo; ch newline }    
    assign s

Therei s

    # immediate
    setvar mystr s  # only a string, not an array

    const-array a b
    assign myarr

    const foo
    const-array a b
    assign myarr mystr


I think it's

    cd /tmp

    block { echo hi }
    cd-with-block /tmp  # pops the stack if it doesn't get a literal


    block { echo hi }
    assign b
    pop

    getvar b           # puts the block on the stack
    cd-with-block /tmp

OK good!  Now we don't need special syntax

---

Tcl has `{*}` for splicing - weird syntax

### async

    fork sleep 0.1
    fork sleep 0.2
    time wait  # 200 ms, because it waits for all

    fork sleep 0.1
    fork sleep 0.2
    time wait -n  # 100 ms
    time wait -n  # another 100 ms

Now how do you implement call backs

    # Main issue: does it get a NEW STACK or not?
    # I think you copy it

    # This is the stack for the callback for fork?
    # It pops it and then saves it for later?

    const-array foo bar
    fork sleep 0.1 {
      echo done
    }

## Links    

- https://learnxinyminutes.com/docs/factor/
  - loops hard to read?
- https://learnxinyminutes.com/docs/forth/

I think Tcl is closer to what we want - it's shell and Lisp like.

## Using Stack for chaining programs

    const foo.o
    ex cc -o $1 foo.c
 
    const bar.o
    ex cc -o $2 foo.c
 
    # now link them?
    # the problem is that this isn't parallel
    ex ld

Maybe you can also do

    const a b c  # push all of these
    for {
      const $pop.o
      ex cc -o $pop foo.c
    }

Yeah you kind of need $pop and ${pop}
And I think $1 $2 $3 $4 makes sense

And also @1 @2 if it's an array?

This is useful for constructing command lines

## Reflecting on code - JSON Structure

    Command:
    ["w", ["arg1", "arg2"]]


    Block:
    [ ["w", []], ["w", []] ]

That is a bit ugly I guess

Another structure is

    ["w", "arg1", "arg2"]

    [["w"],
     ["w"]]

Or

    {"w": ["arg1", "arg2"]}
    {"w": []}

    [{"w": []},
     {"w": []}]

But dicts aren't native.

TODO:

- I want to reflect on source code
  - I want precise error info
  - So I wonder if you just get a tuple of (tree, tokens array)
  - and then you index into those positions

## NIL8

    (Command w (arg1 arg2))

    (Program (Command w) (Command w))

What about location info?

    (Command w (arg1 arg2) |48 49 50|)

    (Program (Command w |49 50|) (Command w |50 51|) |50 90|)

## Positional Args

    $1 $2 .. $9   #  are these right ot left?
                  # or maybe it's $_ is the top, and $1 $2 $3 are offsets from
                  # the top

    Not going to implement ${1} or $x or ${x}

    $-  # this can be POP?
    $!  # side effect

    $$  # pop, conflicts with PID?
    $_

    $<>  # not taken in shell?

    ${}


    const foo.c
    const bar.c
    const :| foo.c bar.c |
