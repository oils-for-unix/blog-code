Notes
=====

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
  - 

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
- O(1) list and dict
  - I think the array type could be a linked list, like bash?
  - then you don't have to worry about growing?
    - stack append is always just bumping pointers
- expressions and types

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
