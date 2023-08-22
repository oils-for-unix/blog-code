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

## Three Dialects of Yaks

- Yaks TAPL -- the arithmetic language 
  - forms: if, unary and binary ops
  - types: Bool, Int

- Yaks Mandelbrot -- 
  - forms: fn, apply, def, do
  - types: Bool, Num, Vec/Array
  - Key point: it's NOT homoniconic
    - so no macros
    - no recursion / tail style!
    - doseq?

- Yaks to create Shak?
  - this one could have macros
  - And List is like a sum type?  It has a dynamic tag
    - Type = Bool | Num | (Vec T) | List
      - Use a [f32] representation

  - does this need anything else?

  - Write a dynamically typed shell language ??
    - Shnerd ?  Sherd?
    - read(), eval(), apply()
    - Can you write Sherd with Nerd mandelbrot?
      - Depends if you need List or not?

  - Data Language with NON -- Nerd Object Notation
    - I guess this is in Sherd, because Nerd is statically typed.

  - Explicit function level typing, with inference in the middle?

## Yaks like Oils C++

Code

- Top Level: class, func   (Class Fn Init Destroy)
- including methods, inheritance
- constructor and destructor for context manager
- modules: import

Within a function

- var set
  - not def?  Because (set [a i] 0) is different and useful
  - I guess Yaks TAPL can use def
- scope  : with - for scope { }
- looping: foreach, while
- cond   : if switch (tagswitch)
- errors : try catch throw

Data Types
 
- Bool Int Float Str
- (List T) (Dict K V)

Basically I want to make an interpreter with the same semantics as mycpp
We already have that -- it's Python

But this is a static interpreter I guess

## Bolt

- Follow Bolt, an OO language implemented in OCaml
  - TAPL doesn't seem to have an implementation
  - <https://mukulrathi.com/create-your-own-programming-language/intro-to-type-checking/>
  - Although he uses a repetitive AST style, not the map
  - Also typing environment is a list, not a Dict !
  - Dicts are missing from OCaml!

- <https://github.com/mukul-rathi/bolt/blob/master/src/frontend/typing/type_classes.ml>
  - 143 lines

- Does Bolt have function types?  I think we need those
  - or maybe we don't need first class ones?

- <https://mukulrathi.com/create-your-own-programming-language/inheritance-method-overriding-vtable/>
  - OK this is good, I want inheritance!
  - Copy all this in TypeScript

## PL Zoo

- <https://plzoo.andrej.com/>
  - "sub" language: eager, mutable records, statically typed, subtyping
  - but syntax?
  - examples don't have subtyping!!!  Bad

## Differences from Lisp

- We have the 'transform' stage
  - it does special forms, at PARSE time, not runtime

  - but does this make sense?
    - ((fn [x] (+ x 1)) 42) is the issue
    - you eval the first one

- TODO: rename parse to read?   I like parse though because it's creating
  recursive structure.  That's different than reading.
  - Also Lisp has a bunch of syntax!

## ocamlscheme

- https://github.com/schani/ocamlscheme

- "This is a very efficient interpreter for a small statically scoped subset of Scheme"
- "Most importantly, no symbol lookup needs to happen during execution"

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

