# Yaks: A Typed Language From Scratch, With All the Bells and Whistles (Blog)

## Language

- Traditional front end: Lexer, Parser to CST, Transformer to AST
  - Concrete vs. Abstract Syntax Tree is Important (see below)
- Type Checker
- Compiler (to WASM) That Relies on Types (+)
- Interpreter that does dynamic checks (for quick prototyping)

- Data Types:
  - Bool Num (is a float for mandelbrot)
  - Str List `Vector[T]` (+)
    - with UTF-8 support?  At least count the length

### Advanced features later (+)

- String Interpolation `(echo "hello \(name)")`
- Comptime like Zig,  (C++ constexpr/consteval), D has this too I think
  - `(constexpr x (+ 2 3)`
  - `(constexpr [x Int] (+ 2 3)`

- Serialization with YON: Yaks Object Notation
  - TODO: static vs. dynamic variant?

- Reader macros?
  - Quasi-quote with `\\(foo $unquote @splice)`
  - Not sure if we need `$(a b) @(c d)`, maybe not
    - I think those are just variables

  - for shell `$(echo hi)` => `(cmd echo hi)` ?
  - `$(echo "hello \(name)")` => `(cmd echo hi)` ?

  - There's a conflict between string substitution $var $(echo hi) and macro 
  - use case: `and` macro

- Julia uses $
- Elixir just uses unquote(x) and unquote do end?
  - <https://elixir-lang.org/getting-started/meta/quote-and-unquote.html>
  - just

## Runtimes

### node.js interpreter

- just use process.stdout and process.stdin?
  - for reading and writing YON

### WebAssembly

- console.log() binding I guess
- maybe the `<canvas></canvas>` binding for Mandelbrot
  - https://github.com/andychu/javascript-vs-c
  - file:///home/andy/git/oilshell/javascript-vs-c/mandelbrot.html
  - How do you do Math.log?

- Exchange YON with browser?
  - "" string literal syntax should be easy
  - I guess you can send UTF-8 strings, but not everything

### Unix - Plain C?

- File I/O with `Int` FD
- (fork) and (wait) concurreency?

- What about garbage collection and signals?

## Tools

- Formatter
  - indentation and whitespace
  - maybe comments -- we don't have that right now -- I think Lisps
    traditionally have some problems with this

- Linter
  - unused variables

- Test framework?  Probably need it, could use macros for assert?

- Bundler?  Probably not, we don't have modules?

### "IDE" from Scratch

- textarea and input box
- reprint the whole text with `<span class="error"></span>` when there's an
  error

- IDE server with completion
  - look at matklad posts
  - the three loops?
  - complete keywords/functions first
    - but really you need objects like (obj.method 1 2 3)

## Applications

- Mandelbrot (graphics)
  - Num and `Vector[Num]`
- Shak: Shell implemented in Yaks?
  - can probably use Deno/node.js stdout, and possibly
  - $(echo hi)

