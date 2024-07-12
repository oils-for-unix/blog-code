TODO
====

- try { }
  - bind to error codes from shell!

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


## Build

BUILD
- static linking
- dynamic linking

Testing:

- BYO protocol
  - ./catbrain-test.sh case-foo

## Functions / macros

argv and env can be printed the same way

   # does it take an argument?  There are no vars, so that doesn't make sense?
   # Or you could create one var $x
   # $_ - just that single var, hm
   # Or maybe just $1 $2 $3

   def dump { 
     w-line yo
   }
   state argv
   dump
   state env
   dump

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

## Naming

- By default it doesn't need bf
  - nullbrain can have it, but catbrain shouldn't

- Abbreviations:
  - cabr
  - nubr - since it can't read data, it can do arbitrary computation?
  - shbr
  - bad-brain - make this stand out
