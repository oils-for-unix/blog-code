TODO
====

- I think you can have a netstring dict format
  - 3:key,4:value,
  - and then you can search for the key value

- capture feed are probably useful for that

- Check signatures more tightly
- Check syntax?

- errors
  - syscall errors
  - arg conversion errors
  - op errors
- control flow without exceptions  

- Consider LINEAR TIME
  - DATA ORIENTED - for argv and env
  - abandon 'loop break' for something LESS GENERAL

  - EOF condition, empty stack condition, etc.
    - eof is a flag set by r-line?

- Consider NESTED structure
  - `{ }` in code can mirror data

  - I guess you can push the DATA stack
  - `frame { }`

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

## Naming

- By default it doesn't need bf
  - nullbrain can have it, but catbrain shouldn't

- Abbreviations:
  - cabr
  - nubr - since it can't read data, it can do arbitrary computation?
  - shbr
  - bad-brain - make this stand out
