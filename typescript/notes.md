## Fiddly Things I learned from Oils

- Representing Tokens, location info
  - quoting errors 
- Lexer modes for ""
- Writing down the grammar first, then writing the recursive descent parser
  - errors should "fall out" cleanly

General them is "exhaustive reasoning" -- languages have many conditionals, and
it's important to tame them.

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

- Interesting fact in eval.ts:
  - when we add  if (...) throw typeError()
  - then TypeScript is smart enough to narrow the type
  - when we added DYNAMIC type checks to the evaluator, for yaks values
    - the TYPESCRIPT code become statically typed (valid), and we didn't have
      to use @ts-nocheck

- Typescript `interface Bool {}` vs `type Bool = ` is a confusing -- they are
  ALMOST interchangeable, and it has changed between versions
  - The language certainly works well, and is sophisticated, but it seems like
    it was a bit cobbled together

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

### Lessons

- static check + run at once is a good workflow!  Very fast and easy
  - wish we could do that with Oils
  - Haiving a fast checker will help
- Now I'm interested in structural types
  - though it's unclear if you can apply that

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
  - added op signatures to fix bug
  - switched to Deno test framework -- seems good enough
  - made type checking optional by adding dynamic checks to evaluator
    - so it's like Python / mycpp

## Lessons Learned

- S-expressions are the same thing as Concrete syntax trees, like Python's pgen
  / pgen2!!
  - It's ID and then a variable list of children!
  - I don't know why I didn't realize this before.  I haven't worked with
    s-expressions in 20 years, although I certainly read them in blog posts and so forth.

- Honestly this clarified macros and special forms
  - especially the transformer stage, separate PNode and Expr types
  - TODO: I'm curious about implementing macros, quoting, quasi-quoting

- Tested out accumulator style for reporting multiple errors: it's
  straightforward
  - flatten a tree, so it's natural

- Structural types are useful

- Deno check/run is a good workflow

- Type checking can be very simple - ignoring difficulties like ambiguous
  literals (is 42 signed/unsigned?) is a good idea


## Thoughts / Ideas

- Now I want to look at Julia macros
  - quoting, quasi-quoting, and substitution
- Ditto Elixir
- Look at Lispy part 2

- I wonder if we can make the statically typed language compile to the mycpp runtime
  - `(var [x (List int)] \(1 2 3))` etc.

## Oils

- procs have unevaluated args, which are kind of like macros
  - should funcs too?



