## Comparable Projects

Title: A Statically Typed Language in 500 lines of TypeScript (or Python)

"Simplest code that's not a toy" -- Has a good parser with exhaustive
reasoning, and gives precise error emssages.  Based on Oils.

- Similar to "500 lines or less" book (which doesn't have this)

NONE of these are statically typed.

- https://mukulrathi.com/create-your-own-programming-language/intro-to-type-checking/
  - best one, it's in OCaml and longer.
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

## Table

MOTIVATIONS: static TYPES make code go fast!!  mycpp leverages the C++
compiler.

I would like to write something like mycpp -- "Pea".  MyPy's type system is
incredibly useful and complex, but we arguably want something simpler.

Meta: TypeScript's type system is awesome, but it's unclear how to translate it
to fast code !!!
  Maybe something like AssemblyScript



Interpreter involves 2 languages:

- Language being interpreted (e.g. Python)
- Language that implements the interpreter (C)

Compiler involves 3 languaegs:

- Language being compiled (e.g. C++)
- Language that implements the compiler (C++)
- Language being translated to (Assembly)

Resources

BOOKS

- Crafting Interpreters pt 1: Java (static) interpreting Lox (dynamic)
- Crafting Interpreters pt 2: C (static) compiling Lox (dynamic) to bytecode (dynamic)

- Dragon book ?

- Appel Tiger
  - ML/Java/C -- procedural tiger?

- Essentials of Programming Languages
  - Lisp based

- TAPL
  - OCaml (Static) and static languages, but no real parser or scaffolding required
  - link to course material

- Terrence Parr
  - Java/ANTLR (more like a DSL) - Not sure there is a complete one

- https://compilerbook.com/
  - bytecode


COURSE

- Coursera?
  - Standard ML (static)  ???

WEB 


- ocamlscheme
  - OCaml (static) interpreting Lisp (dynamic)
    - or was there a compiler too?
    - I hacked on this codebase to learn OCaml

- OPy
  - Python compiling Python to Bytecode (dynamic)
- byterun
  - Python interpreting bytecode

- Mukul Rathi's
  - OCaml static / Java-like static

- plzoo 
  - OCaml (static) implementing static

- Let's build a compiler
  - https://compilers.iecc.com/crenshaw/
  - PASCAL compiling ???

REAL

- C interpreting femtolisp 
- femtolisp front end for Julia


LISP Section

- SICP chapters
  - Lisp interpreting Lisp -- metacircular

- Norvig Lispy:
  - Python interpreting Lisp

- Make-a-lisp
  - Lisp and X  -- are they all interpreters?
