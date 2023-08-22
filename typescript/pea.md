Pea
===

A Python type checker that's itself statically typed.  Alternative to Yaks.
 
Static typing helpers the compiler.  Having ASDL and Python unified is nice.

## Architecture

- Use Python AST module to parse with type comments.

- Write ASDL Schema for typed Python
  - in particular the # type becomes "var" I think

- ASDL needs to grow a CST feature?
  - you can deserialize from CST?  But you have to make sure all the variant
    names are unique?

- Or I guess you manually write, in Python, the transform.ts equivalent for the `(Foo x y)`
  serialization?
  - You can also generate that I guess
  - Yeah you need some kind of code gen from ASDL -- it's a static vs. dynamic issue
  - It's exactly the same thing as asdl/format.py pretty-printing -- it
    requires code generation there


- Then the whole Python codebase compiler is statically typed, and can be
  translated to ASDL

- Files
  - pea/syntax.asdl ?
  - pea/pir.asdl ?   # mycpp IR
  - pea/PIR.asdl ?

- Then write a type checker with big Map like MyPy
  - I guess use the `with tagswitch` crap, it works OK

- How long does parsing, serializing, type checking, printing C++, take?
  - well you can make it incremental with Ninja?
  - <http://travis-ci.oilshell.org/github-jobs/4760/pea.wwz/_tmp/soil/logs/parse-all.txt>
  - 1.2 seconds on CI, but that's more than parsing
    - 0.58 seconds, Parsed 103 files and their type comments
  - 0.84 seconds on my hoover machine
    - 0.48 seconds on my machine
  - Well I hope it doesn't take another 1.2 seconds to serialize, etc.
    - But I don't want to rewrite a Python parser
- TODO:
  - batch it into 4 or 8 tasks
    - should get down to 0.2 seconds or less, even with Python interpreter startup?
  - Python interpreter takes 19ms, so you can do 100ms or more pieces of work

## More Performance Tests

- Test out raw pickle into another Python process?
  - also what if your batches aren't evenly sized, because modules aren't?
  - that messes with the parallelism a bit
- also can pickles be serialized over a pipe?

## Notes on OCaml

This was inspired by:

- Rust vs. OCaml post
- TypeScript post from matklad

(There was also a good post about Austral written in OCaml)

I just want algebraic data types in a fast language, that's not OCaml


Problems:

- Loops are annoying.  See Short-circuiting example from wiki: Why Not Write
  Oil in X?

- Destructuring algebraic data types repeats the names
  - it's like a tuple, not a real struct.  I want a real struct.

- Related: the location info pattern in TAPL is annoying

- Lexers and parsers require tools?  mll and mly
  - I like our regex style (Does OCaml have builtin regex)
  - Lexing and parsing are inherently stateful
  
- Syntax is confusing (ReasonML has good critique)
