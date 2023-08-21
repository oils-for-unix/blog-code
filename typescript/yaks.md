Yaks
====

A language that's like our use of Python and mycpp:

- Dynamic semantics, and an interpreter with REPL
- If it's 100% statically typed, then it can be compiled to fast C++, on our runtime
  - Not sure if we want gradual typing, you might be forced to go from leaves
- Extra
  - Dynamic semantics produce either JSON, or ASDL-like "pickles" (squeeze and freeze?)
  - These can be frozen into a C++ binary as static data (zero runtime cost)
  - So it's like a comptime

## Type Checker and Compiler for Yaks, in Yaks

This makes sense!

Port your damn type checker

Well then you need a dict type, but that's OK

    (set [d "key"] 42)
    (set [d name] 42)   # place is []

    (defn check [
      (, expr Expr)
      (, types (Dict Expr Type))
      (, errors (List Error))
      (-> (or Type null))
    ] 
      (def ok true)
      (def [result (or Type null)] null)

      (switch [expr.tag]  # reader macro (. expr tag)
        (case 'Name'
          (throw ShouldNotGetHere))

        (case (list 'Bool' 'Name')
          (throw ShouldNotGetHere))
    )

And then statically type it

You need Dict and switch

This is what I was doing with Python
  - turn Python into mycpp/Tea, by implementing a type checker in Python (MyPy)
  - and then they typed MyPy

- serialize the CST
  - Bool | Int | Str | List ? 
    - `(+ a b 42)` gives you a `[Str, Name, Name, Num]` ?
      - does `("+" a b)` make sense?
        - Clojure says "cannot call + as a function"
      - does `('+ a b)` 
      - does `((quote +) a b)`  ?

## Language of Types

    Bool  Int  Float   Str
    (List T) e.g. (List Int), (List Str)
    (Dict K V) e.g. (Dict Str Int)

    (def Person (data
      [name Str]
      [age Int]))

    (def word (enum
      [Operator (typeref Token)]
      [CompoundWord (typeref CompoundWord)]
      [BracedTree [parts (List word_part)]
      ))

    (def-data ...) (def-enum ...)

    or maybe capital letters for these macros

    (Data Person
      [name Str]
      [age Int])

    (Enum parse_result
      EmptyLine
      Eof
      [Node [cmd command]])

## Comptime / Freezing

- Dynamic semantics can give you JSON-like data literals?  That you include in
  your SCRIPT!
- Static semantics give you structs and arrays, using C++ literals syntax?

## Example of Code that could work in both dynamic and static modes

Maybe all this can work?

I wrote it dynamically.  Seems like it can be static too.

Use of strings for tags everywhere is interesting.

```
function parseList(p: Parser, end_id: string): List {
  next(p); // eat (

  if (p.current.id !== 'name') {
    throw { message: 'Expected name after (', loc: p.pos };
  }
  let list: List = {
    tag: 'List',
    name: tokenValue(p.current),
    loc: p.pos,
    children: [],
  };
  next(p); // move past head

  while (p.current.id !== end_id) {
    list.children.push(parseNode(p));
  }
  next(p); // eat rparen / rbrack

  return list;
}
```

### Shak - Shell Written in Yaks

HTML literals for lexer modes?

    (echo <p>hello</p>)

This is annoying to type

---

Maybe shell style literals in braces:

    (defn foo [x]
      (if true
        (do
          { ls /tmp/$mydir | sort | wc -l > out }
          { PYTHONPATH=. ./foo.py }))
      (def x $( ls /tmp )))

Are those reader macros?  For { } and $() arguably

    (pipe
      (cmd (list ls /tmp/$mydir))
      (cmd (list sort))
      (cmd (list wc -l) (redir > out))  # redirs are prefix ops
    )
    (cmd (list ./foo.py) (env PYTHONPATH .))

Shorter:

    (cmd (env PYTHONPATH .) foo.py)
    (cmd (redir > out) echo hi)

Probably shares the lexer?  So you have string interpolation

    (echo "hello \(name)")

    (echo "hello \(fn yo)")

    (echo "hello \$(hostname)")

So I guess you wite a recursive descent parser

I guess reuse the dynamic semantics of Yak for this?  Interpreted, without type checking

This is the same as unifying mycpp and YSH -- Tea/Oils

## Yaks: A Typed Language From Scratch, With All the Bells and Whistles (Blog)

### Language

- Traditional front end: Lexer, Parser to CST, Transformer to AST
  - Concrete vs. Abstract Syntax Tree is Important (see below)
- Type Checker
- Compiler (to WASM) That Relies on Types (+)
- Interpreter that does dynamic checks (for quick prototyping)

- Data Types:
  - Bool Num (is a float for mandelbrot)
  - Str List `Vector[T]` (+)
    - with UTF-8 support?  At least count the length

- Code Types
  - `(-> [Num Num] Bool)`

#### Advanced features later (+)

- String Interpolation `(echo "hello \(name)")`
- Comptime like Zig,  (C++ constexpr/consteval), D has this too I think
  - `(constexpr x (+ 2 3)`
  - `(constexpr [x Int] (+ 2 3)`

- Serialization with YON: Yaks Object Notation
  - TODO: static vs. dynamic variant?

- Reader macros?
  - Quasi-quote with `\\(foo $unquote @splice)`
  - Not sure if we need `$(a b) @(c d)`, maybe not
    - I think those are just variables

  - for shell `$(echo hi)` => `(cmd echo hi)` ?
  - `$(echo "hello \(name)")` => `(cmd echo hi)` ?

  - There's a conflict between string substitution $var $(echo hi) and macro 
  - use case: `and` macro

- Julia uses $
- Elixir just uses unquote(x) and unquote do end?
  - <https://elixir-lang.org/getting-started/meta/quote-and-unquote.html>
  - just

### Runtimes

### node.js interpreter

- just use process.stdout and process.stdin?
  - for reading and writing YON

### WebAssembly

- console.log() binding I guess
- maybe the `<canvas></canvas>` binding for Mandelbrot
  - https://github.com/andychu/javascript-vs-c
  - file:///home/andy/git/oilshell/javascript-vs-c/mandelbrot.html
  - How do you do Math.log?

- Exchange YON with browser?
  - "" string literal syntax should be easy
  - I guess you can send UTF-8 strings, but not everything

### Unix - Plain C?

- File I/O with `Int` FD
- (fork) and (wait) concurreency?

- What about garbage collection and signals?

### Tools

- Formatter
  - indentation and whitespace
  - maybe comments -- we don't have that right now -- I think Lisps
    traditionally have some problems with this

- Linter
  - unused variables

- Test framework?  Probably need it, could use macros for assert?

- Bundler?  Probably not, we don't have modules?

#### "IDE" from Scratch

- textarea and input box
- reprint the whole text with `<span class="error"></span>` when there's an
  error

### Applications

- Mandelbrot (graphics)
  - Num and `Vector[Num]`
- Shak: Shell implemented in Yaks?
  - can probably use Deno/node.js stdout, and possibly
  - $(echo hi)

