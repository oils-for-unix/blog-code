Type Checking in TypeScript
===========================

- `matklad.ts` - Transcription of
  <https://matklad.github.io/2023/08/17/typescript-is-surprisingly-ok-for-compilers.html>

- `bool-int-andy.ts` - Remove visitor, and report multiple errors with 'errors'
  out param.

## Slogans

- Oils lexing/parsing/errors , TAPL Typed Arithmetic (by way of matklad),
  Norvig's Lispy (syntax and evaluator)

## Docs

- [TODO.md](TODO.md) - my working stuff
- [yaks.md](yaks.md) - design
  - [data-types.md](design.md) - Bool Num Vec Func, then List
  - [syntax.md](syntax.md) - Ideas for Yaks syntax
  - [blog.md](blog.md) - What I might want to put on the blog
- Blog
  - [lang-table.md](lang-table.md) - Related Work
  - [notes.md](notes.md) - Experiences with TypeScript etc.

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

- Nerd: because I was nerd-sniped!
  - NON: Nerd Object Notation is s-expressions, maybe with a more C-like accent

- Yaks: Was also OK

- Tydy -- Dynamically typed, and statically typed
  - interpreted AND compiled
  - Coudl be a

- Shapes: Dyad, Knot, Coil

