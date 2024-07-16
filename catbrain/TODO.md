TODO
====

- error handling
  - leaving null on stack?
- try { }
  - bind to error codes from shell!

- syntax
  - this requires "Word parser"
  - `$[_]` `@[_]` - do we want `$_` too?  That's more grammar
    - top of stack
    - it's not a var name?
  - `$[array[0]]` `@[array]`

  - pipeline - ls | wc -l desugars to 'pipeline'

- runtime
  - var stack - named vars
  - dicts and mappings


Desugaring

    pipeline
 
`x=$x` could be desugared as:
 
    string {
      const 'x='
      getvar x
    }
 
    @a means
 
    getvar a
    assert is-array
 
 
    # also
    assert is-string

I guess that's word evaluation


    block { echo 1; echo 2; }
    eval  # run it!

    string 'echo 1; echo 2'
    eval-str

More:


    x ls /tmp  # leaves status on stack
    extern ls /tmp  # alias

    capture ls /tmp  # leaves status and then stdout

    try x ls tmp  # it tests for non-zero?

Then vars:

    nq-capture ls /tmp
    assign status stdout

    echo $status $stdout

I think we want this rule

    x env FOO=$x BAR=$x
    x my-server --port=$port

Capturing

    nq-capture {
      x printf hi
    }
    assign status stdout

    # hm yeah that's not bad

- async runtime!
  - think about pipeline { } { }

- serializing code from YSH
  catbrain { could be a keyword } or YSH reflection

- REPL for catbrain?
  - I think the lexer should support the REPL
  - now that I've figured out the word issue

- Refactor code for dialects?
  - nullcat - add BF interpreter?
  - kcat
  - ycat - I already have some of this

- I think you can have a netstring dict format
  - 3:key,4:value,
  - and then you can search for the key value
  - capture feed are probably useful for that
  - this can be a def

- Check signatures of commands more tightly
  - `_DataArg`, `_OneArg`, etc.

- errors
  - syscall errors
  - arg conversion errors
  - op errors

- control flow without exceptions  
  - break
  - early return from def

- location info for error messages

## async xargs -P in catbrain?

- expose self-pipe trick
- poll() loop I guess
  - poll for process exit
  - when you get that, start a new one

- poll line events?
  - I guess when you get a chunk, it's not too hard to split it up by lines
  - can have a splitlines primitive ...
  - but you preserve the boundaries, so you can join with other chunks
  - you can keep track of incomplete lines
  - do the last 5 lines

## Build

BUILD
- static linking
- dynamic linking
- fast enough for shell script!  No incremental build
  - should be at least 10x smaller than Oils

Testing:

- BYO protocol
  - ./catbrain-test.sh case-foo

## C Implementation

- Hm should have immediate string / small string optimization
  - everything is either Str or List[str] - following shell

- if you really wanted to be ambitious, you could do a Cheney collector
  - revive the old one
  - however I think it's better to start with the global vars

Notes:

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

### ERRORS in C implementation

- Out of stack space - well this is realy a heap
  - make it as long as argv?
- Code is too big - maybe make it 4096 bytes or something?
