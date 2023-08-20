## TODO

- Fix typing bug, e.g. (+ true ture)
  - Make sure Symbol is disallowed

- can we get rid of Error as a valid Expr?
  - that's because of the transformer

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
  - `(define ...)` to avoid confusing lambda binding
  - `(begin ...)` so we define, then apply, more like JavaScript
  - `(print ...)` since it's a side effect

https://stackoverflow.com/questions/15057786/scheme-fibonacci-series-with-nested-lambda

You would have to use the Y combinator, but maybe we can do without it:

- Turn it into simply typed lambda calculus
  - "Abstraction" and "Application", aka Function Defs and Calls
  - With var binding!

- Turn it into a type CHECKED language, not type inferred

- Port to Python 3 with pattern matching and MyPy, and see how long it is.

