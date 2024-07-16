Shell vs. Catbrain
==================

## Catbrain Language Intro

### Syntax

- commands are made of words and blocks
- blocks are made of commmands
- pipelines desugar to commands

Lexer modes:

    my-command --foo=$[a[1]]

    echo ${x|html}

    echo $[a[0] => html()]   # proc vs. func distinction?

### Runtime

- a value is a string or an array of values (recursive)
- **Stack** model, like Forth
  - `jq` has a similar "point-free" style

Example:

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

    cb$    setvar s mystr

Forth style:

    cb$    const mystr
    cb$    setvar s     # pops top value and assigns to it

Array in forth:

    cb$    array {
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

    cb$  getvar x   
    cb$  echo

Forth style string interpolation:

    const 'hi '

    # doesn't exist
    echo $x

Array

    bash$  echo "${a[@]}" 

    ysh$   echo @a

    cb$    echo @a  # special syntax

### Backslash Escapes

    sh$    echo -e 'one\ttwo'

    bash$  echo $'one\ttwo'

    cb$    string { const 'one'; ch tab; echo two }
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

    cb$   array {  # no first class dict type?
            pair key1 value1
            pair key2 value2
          }
          assign mydict

## Redirects

    sh$  echo hi > out.txt
    sh$  sort < in.txt

    ysh$ fopen >out.txt { echo hi }
    ysh$ fopen <in.txt { sort }

    cb$  fopen '>' out.txt { echo hi }
    cb$  fopen '<' in.txt { sort }

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

    cb$ pipelne { echo 1; echo 2 } { wc -l } 

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

    if x test $x = foo {
      echo foo
    } elif x test $x = bar {
      echo bar
    } else {
      echo other
    }

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

## Defining Procs

Not done:

    def f {
      w-line foo
      w-line bar
    }

    def f a b c {  # are these the things on the stack?
      w '['
      w $x
      w ']'
    }

So

    f foo

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
         echo status=$_  # top?

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

    cb$  echo foo=$x-$[a.b[0]]

    cb$  array {
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

    cb cd /tmp %_          # the current thing


### Unevaluated Expressions (quotations)

    ysh$  var ex = ^[2 + 3]
    ysh$  var result = evalExpr(ex)


    cb$   const-array expr 2 '+' 3 
    cb$   command-sub { @_ }  
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
    f
    oo
