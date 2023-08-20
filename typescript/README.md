Type Checking in TypeScript
===========================

- `matklad.ts` - Transcription of
  <https://matklad.github.io/2023/08/17/typescript-is-surprisingly-ok-for-compilers.html>

- `bool-int-andy.ts` - Remove visitor, and report multiple errors with 'errors'
  out param.

## Slogans

- Oils parsing, TAPL Typed Arithmetic (by way of matklad), Norvig's Lispy
  (syntax and evaluator)

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

- String interpolation!
  - (echo "hello \(var) \(fib 10)")

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

Types could be attached to set

```lisp

(set x 42)  # untyped

(set (x Int) 42)  # typed

(set IdType (-> [Int] Int))

# -> is a specal form like lambda, since first arg isn't evaluated
(set PlusType (-> [Int Int] Int))
(set EqType (-> [Int Int] Bool))
(set AndTYpe (-> [Bool Bool] Bool))

(set
  (x IdType) 
  (lambda [x] x)
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

## Notes on Deno

Used all the tools:

- deno check && deno run
  - ended up with @ts-nocheck on evaluator, but it's very useful in general
- deno fmt -- helpful 
  - just 2 few deno-fmt-ignore, on the lexer Regex, and evaluator switch statement
- Deno lint
  - fairly useful, although I silence some warnings
  - also @ts-nocheck lint rule conflicts with deno check
- deno bundle -- says it's deprecated?
  - didn't deploy it, but it seems useful
- deno test -- good enough test framework!
  - just Deno.test() -- that's it!
  - assert, assertEquals
    - List and map equality in Oils

## Work Log

- Friday:
  - install Deno, copy code and fix typos, get it to run
  - got help on inference,
  - remove visitor, report multiple type errors.
  - add test cases
- Saturday:
  - Write lexer and "reader", with precise location information.  Many tests.
  - Wrote transformer -- straightforward.  Decided to let errors pass through
  - Hooked up check.ts -- Map<> decision and undefined is a little awkward.
    - code is shorter
  - implemented evaluator with @ts-ignore
- Sunday:
  - evaluator uses dynamic JavaScript -- easier to read
  - polish and test

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


