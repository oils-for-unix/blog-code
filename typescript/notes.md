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

Lessons

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
