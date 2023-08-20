Type Checking in TypeScript
===========================

- `matklad.ts` - Transcription of
  <https://matklad.github.io/2023/08/17/typescript-is-surprisingly-ok-for-compilers.html>

- `bool-int-andy.ts` - Remove visitor, and report multiple errors with 'errors'
  out param.

## Components

- Syntax in the style of Scheme, more specifically Norvig's lis.py (begin,
  set!), with Clojure [] sugar

- Lexer in the style of Oils
  - TODO: Lexer modes!

- Parser and error messages in the style of Oils 
  - Errors: unbalanced ()

- "Transformer" in the style of CPython
  - Errors: Arity of `if` and `+`

- Type Inference (and checking) from matklad 
  - errors:
    - binary operands must have same type
    - if condition is boolean
    - then else must have same type

- Type system: Str, Bool, Num, List (heterogeneous)
  - this makes it homoiconic?  for NON

  - Num is floating point, so we can do something arguably non-boring:
    mandelbort (not just fibonacci)

- Evaluator from lis.py
  - scoping

- Compiler!
  - translator to C++
  - begin, set! should be OK I think ?

- Runtime
  - Garbage collector for List?
  - Tagged pointers?
  - Small string?

Later components:

- Explicit typing
  - casting?

- Data language with proper string literals, and maybe float literals:  NON,
  Nerd Object Notation
  - See "Shape of Data" from Jamie Brandon

- Comptime evaluation?  And then bundle the whole thing into a single text file
  program?

## Terminology and Core Types

- Id -- for tokens
- Tag -- for nodes

- Node - homogeneous -- rename to PNode?

- Expr

- Type

- Value

## TODO

- DONE Add a better syntax for testing
  - S-expressions with any type of thing
  - `(== (+ 1 2) (+ 3 4))`

- Print nice parse errors

- read() vs. parse()
  - if and binary operators need to be parsed to an AST

- Add lexer modes for "\u{123456} \n \\"

- then port the type checker

- then write an evaluator!

- Add enough to run statically typed Fibonacci!
  - bools and ints / conditions and arithmetic
  - `(define ...)` to avoid confusing lambda binding
  - `(begin ...)` so we define, then apply, more like JavaScript
  - `(print ...)` since it's a side effect

https://stackoverflow.com/questions/15057786/scheme-fibonacci-series-with-nested-lambda

You would have to use the Y combinator, but maybe we can do without it:

```lisp
(begin
  # Using syntax from book ?
  (deftype fib (-> [number] number)

  (define fib
    (lambda [n]
      (if (== n 0)
        1
        (+ (fib (- n 1)) (fib (- n 2))))))

  # Is print polymorphic
  (print (fib 10))
```

In JS 

```javascript
var fib = function(n: number): number {
  if (n === 0) {
    return 1
  } else {
    return fib(n - 1) + fib(n - 2)
  }
}

print((fib(10))
```

- Turn it into simply typed lambda calculus
  - "Abstraction" and "Application", aka Function Defs and Calls
  - With var binding!

- Turn it into a type CHECKED language, not type inferred

- Port to Python 3 with pattern matching and MyPy, and see how long it is.

## Comparable Projects

Title: A Statically Typed Language in 500 lines of TypeScript (or Python)

"Simplest code that's not a toy" -- Has a good parser with exhaustive
reasoning, and gives precise error emssages.  Based on Oils.

- Similar to "500 lines or less" book (which doesn't have this)

NONE of these are statically typed.

- Make-a-Lisp: Much bigger codebase to read
- Norvig's Lispy -- both languages dynamically typed, s.split('(') etc.
- ocamlscheme -- Uses ML lex and yacc

But the reader is worth comparing.

- Types and Programming Languages, e.g. Chapter 11 Lambda Calculus
  - Doesn't have examples!
  - No parser!  Hard to write tests!

- Dragon Book: Shockingly, doesn't have code for a type checker!
  - Somehow I didn't realize this for awhile

- TODO: look at Essentials of Programming Languages?
  - Does not have parser?

 
## Fiddly Things I learned from Oils

- Representing Tokens, location info
- Lexer modes for ""
- Writing down the grammar first, then writing the recursive descent parser
  - errors should "fall out" cleanly

General them is "exhaustive reasoning" -- languages have many conditionals, and
it's important to tame them.


## List of Errors

- Lexing -- there are no errors
- Reading -- matching `() []`, EOF, etc.
- Transforming -- `if` and `+` have right arity
- Inference / Type checking -- `+` has right args, etc.
- Runtime -- 1/0

## Notes on Stages

- Lexing: use regex for exhaustive reasoning.
  - Weird JavaScript API, "sticky bit"
- Reading: important to write out the grammar!
  - Added [] synonym for (), allowing Clojure-like sugar
- Why separate reading and parsing?
  - CPython has parser and transformer
    - homogeneous -> heterogeneous tree (untyped or "tagged" with dynamic type,
      to TYPED)
  - Matklad's type inference code operated on a heterogeneous
  - "Reader" will be useful for JSON

## Notes on TypeScript

- Printing JSON is really underated!
  - I can see the tokens and the trees!
  - color from Deno is nice
  - Oils is going to be like this !!!

- Inference of types from JSON-like object literals is fairly pleasant
  - reminds me of Zig's type inference of anonymous struct literals

- Minor: 'export' makes code very noisy

- Structural types, and a string '(' or 'Bool' or '+' as a type is very
  interesting

- Dict punning {dict} is good
  - Oils has it!

## Work Log

- Friday:
  - install Deno, copy code and fix typos, get it to run
  - got help on inference,
  - remove visitor, report multiple type errors.
  - add test cases
- Saturday:
  - Write lexer and "reader", with precise location information.  Many tests.


## Naming Ideas

- Statick
- Licks
- Lycks
- Slicks
- Statyck
- Yack
- Yaks
  - YDN -- Yaks Data Notation
  - I want to illustrate the principle of a data notation
- Nerd: because I was nerd-sniped!


