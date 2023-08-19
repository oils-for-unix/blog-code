Type Checking in TypeScript
===========================

- `matklad.ts` - Transcription of
  <https://matklad.github.io/2023/08/17/typescript-is-surprisingly-ok-for-compilers.html>

- `bool-int-andy.ts` - Remove visitor, and report multiple errors with 'errors'
  out param.

## TODO

- Add a better syntax for testing
  - S-expressions with any type of thing
  - `(== (+ 1 2) (+ 3 4))`

- Write an evaluator!

- Add enough to run statically typed Fibonacci!
  - bools and ints / conditions and arithmetic
  - `(define ...)` to avoid confusing lambda binding
  - `(begin ...)` so we define, then apply, more like JavaScript
  - `(print ...)` since it's a side effect

https://stackoverflow.com/questions/15057786/scheme-fibonacci-series-with-nested-lambda

You would have to use the Y combinator, but maybe we can do without it:

```lisp
(begin
  (define fib
    (lambda [n]
      (if (== n 0)
        1
        (+ (fib (- n 1)) (fib (- n 2))))))

  (print (fib 10))
```

In JS 

```javascript
var fib = function(n) {
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
