Notes
=====

## Missing in the Oils Runtime

- Embeddable pure interpreter
  - e.g. for Hay-like "remote evaluation"

- Small String Optimization - immediate values

- zero allocation

- Reflection on YSH source code within YSH
  - exporting tht AST

- Event loop!   ASYNC RUNTIME FOR SHELL!
  - Maybe this is where I prototype it?

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

## More Arrays

    extern ls /tmp
 
    const :| ls /tmp |  # array of words
    extern 

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

How to make a pipeline:

    array {
      const :| ls /tmp |
      const :| wc -l |
    }
    # array of arrays?
    pipeline


## Drafts

cat program:

    loop {
      r-line
      if eof { break }
      w
    }
    
capture:

    # This puts a var on the top of the stack!  Just like Tcl [] !!!  YES YES #
    OUTPUT
    capture {
      bf '<>+'
    }
    
    # capture output
    capture {
      w hi
      w 'hi'
    }
    
    # pop take of stack, and use it as input
    feed {
      capture {
        r-line
      }
    }
    
    capture {
      feed {
      }
    }
    
    # is this a meacro
    def f {
      r-line 
      w
    }
    
    KEY question:
    - are loop and break special forms?
    
    - or can you parse them?
    - I think you make it like TCL !!
      - you parse everything UNIFORMLY into a tree
    
    
      push-argv
      loop {    # loop over argv
        # now we operate on the top
        exit
    
        pop
        if empty { break }
      }
    
      push-env
      loop { 
        # now we operate on the top
        pop
        if empty { break }
      }
    
      loop {
        r-line; break-if-empty; w-line
      }
    
    # TSV filter
    
    - r-cell
    
    
    loop {  # over rows
      loop {  # over cells
    
       if newline {
         break
       }
      }
    }
    
    push a b;
    
    
    
    - loop -
    - cond - test if the top of stack is not empty?
    
    Stack oriented language
    
    
    Forever loop
    
    
    
    forever; r-line; w
    
    loop; r-line; w; end
    
    loop
      r-line; w
    end
    
    loop 
      loop
        r-line; w
      end
    end
    
    loop 
      cond
        r-line; w
      end
    end
    
    # repeat 3 times
    
    c-push 3  # push 3 on the stack
    loop
      r-line; w;
      c-dec
      cond; break; end;
    end
    
    repeat 3 {
      foo
    }
    
    test 0 {
      break
    }
    
    
    push foo
    c-push 3
    
    loop {
      w-line  # take it from the top of the stack
    
      c-dec
      cond { break }
    }
    
    def f x {  # only 1 arg?  Or multiple args?   Binding is allowed?
      p $x
    }
    f 'hi'
    
    def f
    
    
    How about no bindings?  Just a single arg $x
    
    w-line foo  # the arg stack
    
    def f x {
    }
    
    Is this like TCL?
    
    
    loop {
      r-line  # EOF is ''
    }
