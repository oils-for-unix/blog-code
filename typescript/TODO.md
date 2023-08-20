## TODO

- Fix typing bug, e.g. (+ true ture)
  - Make sure Symbol is disallowed

- Maybe add dynamic checking to interpretr
  - so we can have real dynamic semantics, WITHOUT type checking
  - like mycpp / Tea

- Bundle it, embed in a web page
  - text box with button
  - dropdown for examples
  - maybe ui.ts with template literal
    - actually you can bundle it all

  - call run() I guess
    - show the output in another textarea
    - run() should take two functions:
      - puts(), log() 

    - run(puts, console.log)
    - Those could be node.innerText or something
    - out.log(), out.write()

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
