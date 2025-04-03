TODO
====

### in Python Impl

- add process API with self-pipe trick
  - maybe I should try Claude Code

- Check signatures of commands more tightly
  - `_DataArg`, `_OneArg`, etc.

- Tests should be in YSH?
  - then we need YSH test framework - yblocks

### Self hosting TODO

- provide parser in Python
  - that provides some kind of "TERM" format
  - I think this is a binary format you can load in memory
  - is it netstring based?


Is it tagged?

Well I guess everything is an Obj almost

Error Str List Obj  FN


## Notes

- async runtime!
  - think about pipeline { } { }

- serializing code from YSH
  catbrain { could be a keyword } or YSH reflection

- REPL for catbrain?
  - I think the lexer should support the REPL
  - now that I've figured out the word issue

- I think you can have a netstring dict format
  - 3:key,4:value,
  - and then you can search for the key value
  - capture feed are probably useful for that
  - this can be a def

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
