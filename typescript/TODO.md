## TODO

- 'name' lexer rule should be all printable chars but NOT
  - `# ( ) [ ] { }`
  - TODO: look at ascii table

- Bundle it, embed in a web page
  - text box with button
  - dropdown for examples
    - it would be nice if we can show ALL errors?
    - maybe the test runner should register the case

  - maybe ui.ts with template literal
    - actually you can bundle it all
    - or put it in a shell script

  - call run() I guess
    - show the output in another textarea
    - run() should take two functions:
      - puts(), log() 

    - run(puts, console.log)
    - Those could be node.innerText or something
    - out.log(), out.write()

- Compile to WASM
  - Num -> f32 or f64
  - Bool -> i32

## Nerd Fibonacci / Tea

See [tea.md](tea.md)

- Add enough to run statically typed Fibonacci!
  - bools and ints / conditions and arithmetic
  - `(def ...)` to avoid confusing lambda binding
    - it can overwrite variables, but later `(set ...)`
  - `(do ...)` so we have side effects
  - `(fn [x] x)`
    - `(fn [(param x Int) (result Int)] x)`
    - syntax inspired by WASM tex format
  - `(print ...)` since it's a side effect
  - macro `defn`
    - how to implement macros?
    - `macro` and `defmacro` ?

https://stackoverflow.com/questions/15057786/scheme-fibonacci-series-with-nested-lambda

You would have to use the Y combinator, but maybe we can do without it:

- Turn it into simply typed lambda calculus
  - "Abstraction" and "Application", aka Function Defs and Calls
  - With var binding!

- Turn it into a type CHECKED language, not type inferred

- Port to Python 3 with pattern matching and MyPy, and see how long it is.

## Research

Need to figure out how to implement macros.

- Lispy.py shows how to do it with 
  - quasi-quote
  - unquote
  - unquote-splicing
