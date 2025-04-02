Shell vs. Catbrain
==================

## Comparisons

<!-- TODO: render this table with ul-table

- maybe build it into oils-for-unix?
  - might need to remove comments and so forth

-->

<table>
<caption> Shell vs. YSH vs. Catbrain</caption>

- thead
  - Aspect
  - POSIX Shell
  - YSH
  - Catbrain
- tr
  - Syntax
  - Odd, but Standard
  - Like Python or JavaScript - a language that your teammates will find familiar
  - Minimal / esoteric shell / forth / Tcl (but arguably more familiar than
    Forth and Tcl, and even Lisp)
- tr
  - Primitive Data Types
  - Strings
  - Strings, Bool, Int, Float, ...
  - Strings
- tr
  - Compound Data Types
  - A single array `"$@"`
  - `List` and `Dict`
  - `List` - values can be string or List, List of pairs can be treated like a
    Dict
- tr
  - Runtime model / syscalls
  - waitpid(-1)
  - waitpid(-1)
  - Idea: make it fully general?  Can express fork() poll()?
- tr
  - Serialization
  - very limited
  - JSON / J8 Notation
  - Lisp-like printer/reader?  But we can express graphs like Pickle?

</table>


<table>

<caption>
Oils vs. catbrain VM
</caption>

- thead
  - Aspect
  - Oils
  - Catbrain
- tr
  - C++ exceptions
  - Yes
  - No (Eval() should return an integer code Break, Continue, Return?)
- tr
  - Stackless?
  - No, uses call stack for function calls
  - Needed for Lua-like coroutines
- tr
  - C API
  - Not yet - needs to integrate with GC
  - Not yet - but could involve coroutines?
- tr
  - Garbage Collected?
  - Yes
  - Could be?  We could cheat with a single mutable `$_line` register?
    Better idea: we can COPY arbitrary values from one VM to another!  You
    spawn a whole catbrain VM for each line!  And copy it!
- tr
  - Subinterpreters
  - No (or not yet)
  - Yes, we should have it!
- tr
  - Shared Library Interface
  - No (or not yet)
  - Yes, we should have it!

</table>

## vs. Ribbit Scheme 

Maybe all of these things can be represented by the same structure:

- data
- code
  - problem: line number info.  Look at what Clojure and Racket do.
- stack (stack frames, and maybe closures)

## Catbrain Language Intro

### Syntax

- commands are made of words and blocks
- blocks are made of commmands
- pipelines desugar to commands

    # expresssion has value.  But is this different thana list?
    my-command --foo=%[a 1]

    # does this make sense?
    echo %{x | html}

    echo $[a[0] => html()]   # proc vs. func distinction?

### Runtime

- a value is a string or an array of values (recursive)
- **Stack** model, like Forth
  - `jq` has a similar "point-free" style

- data
  - `value.Str`
  - `value.Array` - sequence of strs or arrays
    - note there is no value.Dict - it is an array of length-2-arrays (pairs)
- code:
  - `value.Command` - first word, then args are words or blocks
    - do you even need this, if you have block?
  - `value.Block` - sequence of commands

What about:

- `value.Word`?  That's an unevaluated expression
  - a word can be reduced to blocks

  - so maybe it is?  Maybe it is a value.Command that produces output?
    - a wrapper?

  - maybe there is no reflection on words?

## Motivating Examples

See forth-style.md


    cb$  w-line zz  # immediate arg, stack not used
    zz

    cb$  const foo            # push
    cb$  const bar            # push

    cb$  pp
        $_  bar   # top of stack
        $1  foo   # bottom

    cb$  const-array ls /tmp  # push array

    cb$  pp
        $_  ['ls', '/tmp']
        $1  bar 
        $2  foo 

    cb$  x          # take args from top of stack, not whole stack?
    file-in-tmp.txt
    file-in-tmp.jpg

    cb$  w-line     # pop arg and write line
    bar

    cb$  w-line     # pop arg and write line
    foo

Note: generally you don't do things in this "reverse" order.

Generally you use 1 or 2 things on the stack.

## Simple Commands

These are designed to be identical to shell.

### Builtin Commands

    sh$  echo hi 'quoted'
    hi quoted

    cb$  echo hi 'quoted'  # same thing
    hi quoted

### External Commands

    sh$  ls --color /tmp

    cb$  x ls --color /tmp
         extern ls  # long way of writing it
         

### User-defined Commands (procs)

    sh$  my-ls /tmp

    ysh$ runproc my-ls /tmp  # defined with proc

    cb$  runproc my-ls /tmp  # defined with 'def'

## Assignment

    sh$    s=mystr
    bash$  a=(x y z)

    ysh$   var s = 'mystr'
    ysh$   var a = :| x y z |
    ysh$   var a = ['x', 'y', 'z']

    cb$    assign s mystr

Forth style:

    cb$    const mystr
    cb$    assign s     # pops top value and assigns to it

Array in forth:

    cb$    list {
             const x
             const y
             const z
           }
    cb$    setvar a

Lisp style:

    cb$    setvar a array { const x; const y; }

(This is bernstein chaining with block vars!)

### Destructured Assignment

    ysh$ var x, y = foo()

    cb$  foo
    cb$  assign x y

## Words

### Var Interpolation

    sh$  echo $x
    sh$  echo "hi $x"

    cb$  echo $x

Forth style:

    # I guess %{} runs all the commands, and then concatenates the stack?
    # It makes a marker for the stack?

    cb$ echo %{c 'hi '; getvar x}

    cb$  getvar x   
    cb$  echo

Forth style string interpolation:

    const 'hi '

    # doesn't exist
    echo $x

Array

    bash$  echo "${a[@]}" 

    ysh$   echo @a

    cb$    echo %%a 

### Backslash Escapes

    sh$    echo -e 'one\ttwo'

    bash$  echo $'one\ttwo'

    cb$    string { const 'one'; ch tab; echo two }
    cb$    w-line

    cb$    w-line %{ c 'one'; ch tab; c 'two' }

    cb$    make-list { c 'one'; ch tab; c 'two' };
    cb$    join
    cb$    w-line

### Unquoted and Quoted Words - Forth-Style Stack

Forth style equvalent of above:

    cb$  const hi  # push constant on the stack
    cb$  w-line    # pop stack and print it
    hi

    cb$ const 'quoted'
    cb$ w-line
    quoted

Array on the stack

    cb$ const foo

    cb$ array { const hi; ch space; const 'quoted' }
    cb$ join       # join top of stack
    cb$ w-line
    hi quoted

    cb$ w-line
    foo

### Brace Expansion

    sh$ echo {alice,bob}@example.com

    cb$ var names [alice bob]
    cb$ echo %[names]@example.com   # this can automatically do cartesian product?

    # Or does this make more sense?  Slicing an array can do it
    cb$ echo %%[names]@example.com 

I guess you can have a uniform PARSING rule for %[] and %%[] ?

Do you need %{}

## Interlude: Stack Manipulation

    dup    # duplicate top element
    dup 2  # TODO: could do this

    pop    # throw away 1
    pop 2  # throw away 2

### Command Sub

    sh$   x=$(echo hi)
    ysh$  var x = $(echo hi)

    cb$   capture-stdout { w-line hi }
    $cb   setvar x   


### Mappings / Dicts

    bash$ declare -A A=([key1]=value1 [key2]=value2)

    ysh$  var mydict = {key1: 'value1', key2: 'value2'}

    cb$   map {  # no first class dict type?
            pair key1 value1
            pair key2 value2
          }
          assign mydict

## Redirects

    sh$  echo hi > out.txt
    sh$  sort < in.txt

    ysh$ redir >out.txt { echo hi }
    ysh$ redir <in.txt { sort }

    cb$  redir '>' out.txt { echo hi }
    cb$  redir '<' in.txt { sort }

## Compound Commands

### Sequence

    sh$ echo one; echo 2

    cb$ echo one; echo 2

### Braced Groups

    sh$ { echo one; echo 2; }  # can be redirected at once

    cb$ group { echo one; echo 2; }
    # { echo one } isn't a command; it's a block, so it's not at the top level
    # we have commands only

### Pipelines

    sh$ ls | grep foo | wc -l

    cb$ ls | grep foo | wc -l  # TODO

    cb$ pipeline { ls } { grep foo } { wc -l }

    cb$ { echo 1; echo 2 } | wc -l

Desugars to:

    cb$ pipeline { echo 1; echo 2 } { wc -l } 

Shelling Out:

    # sh -c 'ls | wc -l'

    sh 'ls | wc -l'

    # Hm I wonder if we also have
    capture-stdout 'ls | wc -l'

    ysh 'ls | wc -l'


## Structured Programming (ALGOL-like)

## Loops

    while {
      w-line  # stack empty
    }

    for {
      w
    }

    for-line {
      w
    }


## If

    if empty {
      break
    }

TODO:

    if boolstatus test $x = foo {
      echo foo
    } elif boolstatus test $x = bar {
      echo bar
    } else {
      echo other
    }

Important: `boolstatus` is different than `x`  !  It does something different
with the exit code of the process.

- `boolstatus`
  - `0` is on the stack if the command exited 0
  - `1` is on the stack if the command exited 1
  - else it leaves `null` on the stack with the  status!

- `x` leaves nothing on the stack if the command succeeds (code 0)
  - if the command fails, it leaves `null` on the stack, AND the exit code

- `try x ls` leaves the exit code no matter what, so you can test it


## Case

TODO

    case $x {
      regex 'README(\.md)?' {
        echo README
      }
      glob '*.py' {
        echo python
      }
      glob '*.h' '*.cc' {
        echo 'C++'
      }
      default {
        echo 'other'
      }
    }

## Defining Fn

Not done:

    fn myfn {
      w-line foo
      w-line bar
    }

    fn myfn a b c {  # are these the things on the stack?
      w '['
      w $x
      w ']'
    }

So

    myfn foo

is short for

    const foo
    f

It's like passing args.  Hm.

## Pure Functions

TODO: leave VALUE on th estack, not just intergers

    def f {
      const 'foo'  # LEAVE It on the stack
      echo x  # FAIL: sandboxed
    }

But I guess procs can do that TOO?

PURITY though.

## try and error

Error handling:

    ysh$ try {
           sh -c false
         }
         if failed {
           echo 'failed'
         }
 
    cb$  try {
           x sh -c false
         }
         if failed {
           echo 'failed'
         }

Error code:

    cb$  try {
           x false
         }
         # _ is top value?
         # and maybe !_ pops it

         echo %[_ caught status]; pop  # discard t

## Hay

Declaring data:

    ysh$ hay define Package
    ysh$ Package cpython {
           version '3.12'
           url 'https://python.org/'
         }

    cb$
      # no integer literals, bool litearls, etc.
      Package cpython {
        version '3.12'
        url 'https://python.org/'
      }

## Expressions

Only in interpolation:

    cb$  echo foo=%[x]-%[a b .0]

    cb$  make-list {
           const 'foo='
           getvar x
           const '-'

           getvar a  # cool
           attr b
           index 0
         }
         join
         w-line


Arithmetic can use external commands:

    cb$  x expr 1 + 2 
    3

### Eggex

External?

    cb$  x expr $s : 'a(.*)b'

Could offer binding to regexec() regcomp().

### Unevaluated blocks (quotations)

    ysh$ cd /tmp { echo hi }
    ysh$ var b = ^(echo hi)


    cb$ cd /tmp { echo hi }
    cb$ block { echo hi }  # leave it on the stack
    cb$ cd /tmp $_         # does this make sense?
                           
Or maybe

    cb$ cd /tmp %_          # the current thing


Is there such thing as an unevaluated command?  Or just an array or block, like
YSH

### Unevaluated Expressions (quotations)

    ysh$  var ex = ^[2 + 3]
    ysh$  var result = evalExpr(ex)

    cb$   const [expr 2 '+' 3 ]
    cb$   capture { %%_ }  # splice the top value
    cb$   assign result

Problem: what if there is nested structure?  Does @_ still work?

## Libraries

### load

We explicitly load state into the VM:

    load argv
    load env
    load pid
    load counter

TODO:

    load rand

### Encoding and Decoding

    ysh$  echo $[toJ8('foo\n')]
    "foo\n"

    cb$   string { push foo; ch newline }
    cb$   encode json
    cb$   pp
    $_  '"foo\n"'

### JSON8 and TSV8

These are builtin pure catbrain?

## Useful External Commands

### `test` for booleans

    cb$  try { x test a = b }; echo $_
    1

    cb$  if x test a = a { echo yes }
    yes

### `expr` for expressions

    cb$  x expr 1 + 2
    3

### printf for formatting

    cb$  x printf '%03d\n' 42
    042
  

## Can catbrain help us with YSH features?

### Modules?

- source - reimplement it
- use

### Static Subset / Detecting Typos

- Type checker

### Tools

- pretty printer
- syntax highlighter
  - comment placement issue

Should be easy with such a uniform and small syntax

### Reflection on Source Code - "Lossless Syntax Tree"

- `declare -f`, etc.?

### Interactive Parsing

- PS2 problem

## C++ Implementation

- Lua-like embeddable pure interpreter
- Two runtimes?
  - Synchronous style `waitpid(-1)` - only waits on processes
  - Async style `poll()` - also waits on files
    - less pressing if we implement `pipecar` netstring scheme
- Small String Optimization
- Compile `break continue return` to control flow, without using C++ exceptions
  - like YSH, catbrain is a tree interpreter
  - what's the minimum way to do this

Probably:

- Fixed size global buffer instead of GC, i.e. zero allocation

## Features in Catbrain That Aren't in YSH

- `vm capture`, `vm feed`
  - this was 'builtin sub', which we don't have yet

Capture:

    cb$  vm capture {
           w foo
           w bar
         }  # output is pushed as value on top of stack
    cb$  echo
    foobar

Feed:

    cb$  const foobar
    cb$  vm feed {
           r 1     # read 1 byte 'f'
           echo
           r 2     # read 2 bytes 'oo'
           echo
         }  # output is pushed as value on top of stack
