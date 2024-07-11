Cat-Brain: A Small Language for Generating Unix Process Workloads, With 4 Runtimes
=====

## Runtimes

- `null-brain` - a language with no input or output
  - WASM runtime 
  - no memory allocation - globals

- `cat-brain` - stdin/stdout/argv/env/status - Unix filter
  - basic Unix cat/echo
  - pid
  - no memory allocation - fixed

- `sh-brain` - arbitrary I/O and syscalls
  - regcomp()
  - regexec()
  - fork
  - exec
  - malloc

- `bad-brain`
  - I don't know all of these

## Flavors

- POSIX shell
- Brainfuck
- YSH, Tcl
- Lisp, Forth
- jq, awk

## Syntax

### Lexer

    # includes { } because we want spaces, like YSH
    UNQUOTED = / [a-z A-Z 0-9 '_{}']+ /
    
    SQ = / \' [^ \']* \' /
    
    SPACE = / ' '+ /

    END = / [';' \n] /

    # These are ignored by the lexer
    COMMENT = / SPACE '#' ![\n]* /

### Grammar

    program = cmd (END cmd)* END?

    block = '{' program '}'

    word = UNQUOTED | SQ

    arg = word | block

    cmd = SPACE? word (SPACE arg)*  # Flexible, uniform syntax:

YSH RULES
    cmd = SPACE? word (SPACE word)* block?  # like YSH, one optional block

Enforce these OUTSIDE the grammar:

    0 args                      - msleep
    1 word arg                  - w-line hi
    1 block arg                 - loop { w-line hi }
    1 word arg and 1 block arg: - if eof { break }

Slogans;

## C Implementation

    struct VM {
      Pair* stack;
      Pair* top;
      int counter;
      bool eof;
    };

    struct Str {
      int len;
      char* data;
    };

    struct Pair {
      // remember in Yaks this wasn't a string?  You could could have ((f 42) 43)
      Str* head;
      Pair* next;
    };


## Help Wanted

- I know how to implement cat-brain and sh-brain
- I don't know how to implement null-brain and (all of) bad-brain!


## Programs I want to run

- cat
- CGI hello
  - print env as J8 notation
  - print argv as J8 Notation
- spec/bin
  argv - definitely - tnet equivalent
  printenv
- write arbitrary TSV8

## Builtins

### Control Flow / Compound Commands

- `loop break`
- `if`
- `capture feed`

Question: `def` is like a macro?

### Stack

- `push pop dup`
- `push`
- `empty` predicate
- `ch`
  - `ch tab space newline sq` - or `apos` is HTML name?

### I/O

- `w; r 3`
- `w-line r-line`
- `log`
- `eof` predicate
- `flush`

### Compute

- `bf`
- `fib` - to generate work without writing `bf`
- `rotate` - trivial string function

### Process

- push-argv
- push-env
- exit
- msleep
- now
- pid

### Transform

- `from-netstr to-netstr`
- `from-j8 to-j8`
- `from-json to-json`
  - this signals an error
  - are errors recoverable?  For now, no

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
