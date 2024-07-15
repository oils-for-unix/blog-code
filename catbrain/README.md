catbrain
========

Slogans:

- A {Tcl, Lisp, Forth } that can express
    { Shell, Awk, Make, find, xargs } and
    { Python, JavaScript and node.js event loop, R data frames } and
    { YAML, Dockerfiles, HTML Templates, ...}  and
    {JSON, TSV, S-expressions, ...} ?

    All with Ruby-like blocks
  
  - "A shell you can't use at work"
  - But derived from existing practice

- A mix of **practicality** and **purity**, honed over 8+ years
- A readable language that must be driven by data
- A language for STREAMING j8 notation!
  - and working with pure text
  - Oils table.ysh is row-wise or column-wise
  - although stream.ysh does work column-wise, with more computation!
- A Language for Generating Workloads, With 4 Runtimes
  - heating up the CPU, forknig threads, switching, etc.

This language has some reminders of Hay too

    foo { echo hi }   

v Oils:
    - no types
    - no expressions
    - no string interpolation
    - no variables

Features:

- Restricted language
  - Output size is limited to a constant function of (input size, program size)
  - No variables
  - no infinite loops
- Syntax is a subset of YSH
  - Well specified grammar
- Embeddable - can safetly execute it within your programs
  - it does zero memory allocation
- Extendable
  - provide your own functions - you can provide the user with arbitrary
    computation and I/O
- TODO: comes with 4 runtimes

Flavors of:

- POSIX shell - words
- YSH for the { } syntax
- Tcl - shell + Lisp
  - also has [] and {} evaluation model
- jq 
  - because it has  an implicit "this" or satck
  - it has not variables!  (jq has variables, but you do most things without
    them)
- Forth because it has a stack
- node.js - if we have an event loop with the self-pipe trick for process
  completion?
- Brainfuck - do we still need this?

Comparisons:

- Forth: catbrain has a stack, but it's block-structured like ALGOL
- Shell: looks similar - based on "words", but it has a stack like forth
- YSH: has block args, but uses them for EVRYTHING, including control flow
- Tcl: it's based more on arrays of strings rather than strings
- jq: it's command-based, rather than expression based (and doesn't have cross
  product / "PEG semantics")
- brainfuck: it's also minimal, with a "basic input and output" model `. ,`
  - but catbrain programs are not "obfuscated"
  - it's designed to be very readable, within the constraints model

## Where did catbrain come from?

- protobuf tools - I always wanted to have something you could "append code to"
- "shell has a forth-like quality"
  - can we preserve "bernstein chaining" in an actual stack-based language?
- jq in jq thread - streaming language with no vars
- generating testdata for xargs -P
- realizing that shell could have an async-style runtime (event loop), not a
  synchronous style
  - need that for the "Ninja problem" (which make -j doesn't do)

## Runtimes

- `nullcat` - a language with no input or output
  - WASM runtime 
  - no memory allocation - globals

- `kcat` - stdin/stdout/argv/env/status - Unix filter like awk
  - basic Unix cat/tac/echo
  - pid
  - no memory allocation - fixed

- `ycat` - everything a shell has?
  - arbitrary I/O and syscalls
  - exec
  - wait

  - unfortunately we can't share the runtime?  Because we have SmallStr?
  - it would be nice

- `workcat` - workloads
  - can start threads, e.g. so you can inspect them
  - fork
  - malloc

- `badcat`
  - I don't know all of these
  - seg faults
    - dereference null
    - divide by zero
  - ubsan - integer behavior
  - asan - overflow
  - syscalls?
  - blowing the C call stack
    - how?
    - I think you just create a malicious stack

## Syntax

### Lexer

Tokens:

    # includes { } because we want spaces, like YSH
    UNQUOTED = / [a-z A-Z 0-9 '_{}']+ /
    LBRACE = / '{' /
    RBRACE = / '}' /
    
    SQ = / \' [^ \']* \' /
    SEMI = / ';' /
    NEWLINE = / \n /
    
    # These are ignored by the lexer
    SPACE = / ' '+ /
    COMMENT = / '#' ![\n]* /

### Grammar

    program = Eof | seq Eof

    terminator = semi | newline+

    seq = NEWLINE* cmd (terminator cmd)* terminator?

    block = '{' seq '}'

    arg = word | block

    # Flexible, uniform syntax:
    cmd = word arg*  

YSH RULES
    cmd = word+ block?  # like YSH, one optional block

Enforce these OUTSIDE the grammar:

    0 args                      - msleep
    1 word arg                  - w-line hi
    1 block arg                 - loop { w-line hi }
    1 word arg and 1 block arg: - if eof { break }

Slogans;

### YSH Subset Issue

This is valid catbrain, but not YSH

    foo { echo arg1 } arg1
    foo { echo arg1 } {
        echo arg2
    }

We can disallow it statically in catbrain if there is always a rewrite

### Keyword/Builtin Conflicts

- Get rid of YSH keywords
  - .if .for .try
  - x or .extern
  - const -> .const or val, lit
  - fork forkwait builtin
    - TBH I like using the same name
    - as long as they do SIMILAR things, not identical, it could be OK
    - I think the YSH convention could be to add it

   if empty-stack {
     break
   }

YSH

   .if empty-stack {
     .break
   }

## Help Wanted

- I know how to implement cat-brain and sh-brain
- I don't know how to implement null-brain and (all of) bad-brain!

## Programs It can Run

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

- arbitrary loop may be disallowed in catbrain, allowed in shbrain, etc.
  - `loop` - 

- limited to data
  - `for` - loop that is limited to data

- `break`
- `if`
- `capture feed`

Question: `def` is like a macro?

### Stack

- `const'
- `getvar'
- 'dup`
- TODO: `pop`, `clear`
- `empty-stack`
  - extensions: is-zero, empty-string
- `ch`
  - `ch tab space newline sq` - or `apos` is HTML name?

### I/O

- `w; r 3`
- `w-line r-line`
- `log`
- `flush`

### Compute

- `bf`
- `op`
  - `fib` - to generate work without writing `bf`
  -  rotate` - trivial string function

### Process

- exit
- msleep
- load
  - argv
  - now
  - pid
  - env
  - counter - TODO: fix counter

### Transform

- decode
  - json string
  - j8 string
  - netstr
- encode
  - json string
  - j8 string
  - netstr

### Protocols

- FANOS
  - todo: hook up py_fanos?
