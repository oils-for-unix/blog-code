catbrain
=====

Slogans:

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

## Runtimes

- `null-brain` - a language with no input or output
  - WASM runtime 
  - no memory allocation - globals

- `cat-brain` - stdin/stdout/argv/env/status - Unix filter
  - basic Unix cat/tac/echo
  - pid
  - no memory allocation - fixed

- `sh-brain` - everything a shell has?
   - arbitrary I/O and syscalls
  - exec
  - wait

  - unfortunately we can't share the runtime?  Because we have SmallStr?
  - it would be nice

- workbrain - workloads
  - can start threads, e.g. so you can inspect them
  - fork
  - malloc

- `bad-brain`
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
- state
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
