Type Checking in TypeScript
===========================

- `matklad.ts` - Transcription of
  <https://matklad.github.io/2023/08/17/typescript-is-surprisingly-ok-for-compilers.html>

- `bool-int-andy.ts` - Remove visitor, and report multiple errors with 'errors'
  out param.

## Slogans

- Oils lexing/parsing/errors , TAPL Typed Arithmetic (by way of matklad),
  Norvig's Lispy (syntax and evaluator)

## Tiers to the Language

- Nerd TAPL -- the arithmetic language 
  - forms: if, unary and binary ops
  - types: Bool, Int

- Nerd Mandelbrot -- 
  - forms: lambda, apply, set!, begin, deftype
  - types: Bool, Float, Str
    - do you need List?  Well it might be good

- Nerd Oils -- 
  - Write a dynamically typed shell language ??
    - Shnerd ?  Sherd?
    - read(), eval(), apply()
    - Can you write Sherd with Nerd mandelbrot?
      - Depends if you need List or not?

  - Data Language with NON -- Nerd Object Notation
    - I guess this is in Sherd, because Nerd is statically typed.

  - Explicit function level typing, with inference in the middle?

## Components

- Syntax in the style of Scheme, more specifically Norvig's lis.py (begin,
  set!), with Clojure [] sugar

- Lexer in the style of Oils
  - TODO: Lexer modes!  for \n \u{123456} \\ 
  - then even `\(fib 10)` string interpolation

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

- Control flow dependent null checking (MyPy and Dart have this)

## Terminology and Core Types

- Id -- for tokens
- Tag -- for nodes

- Node - homogeneous -- rename to PNode?

- Expr

- Type

- Value
 
## Fiddly Things I learned from Oils

- Representing Tokens, location info
- Lexer modes for ""
- Writing down the grammar first, then writing the recursive descent parser
  - errors should "fall out" cleanly

General them is "exhaustive reasoning" -- languages have many conditionals, and
it's important to tame them.

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

### List of Errors

- Lexing -- there are no errors - but BAD uses
- Reading -- matching `() []`, EOF, etc.
- Transforming -- `if` and `+` have right arity
- Inference / Type checking -- `+` has right args, etc.
- Runtime -- 1/0

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


