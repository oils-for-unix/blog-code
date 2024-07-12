Notes
=====

## Links    

- https://learnxinyminutes.com/docs/factor/
  - loops hard to read?
- https://learnxinyminutes.com/docs/forth/

I think Tcl is closer to what we want - it's shell and Lisp like.

    
## DraftS

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
