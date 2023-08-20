## Syntax Notes

```lisp
(begin
  # Using syntax from book ?
  (deftype fib (-> [number] number)

  (define fib
    (lambda [n]
      (if (== n 0)
        1
        (+ (fib (- n 1)) (fib (- n 2))))))

  # Is print polymorphic
  (print (fib 10))
```

Types could be attached to set

```lisp

(set x 42)  # untyped

(set [x Int] 42)  # typed

# deftype might be better than set?
# or just type
(type IdType (-> [Int] Int))

(set IdType (-> [Int] Int))

# -> is a specal form like lambda, since first arg isn't evaluated
(set PlusType (-> [Int Int] Int))
(set EqType (-> [Int Int] Bool))
(set AndType (-> [Bool Bool] Bool))

(set
  (x IdType) 
  (lambda [x] x))

(set
  (x AndType) 
  (lambda [x y] (and x y)))
```

In JS 

```javascript
var fib = function(n: number): number {
  if (n === 0) {
    return 1
  } else {
    return fib(n - 1) + fib(n - 2)
  }
}

print((fib(10))
```

## WebAssembly Syntax

- <https://developer.mozilla.org/en-US/docs/WebAssembly/Understanding_the_text_format>

Has `$p1` instead of indices

```
(func (param $p1 i32) (param $p2 f32) (local $loc f64) ...)
```

- Has `(param ...)`
- `(result ...)`

We could do that

```lisp
(set x
  (lambda
    [(param x Int) (param y Int) (result Int)]
    (begin
      (set x y)
      z)))
```

Untyped:

```lisp
(set x
  (lambda [x y]
    (begin
      (set x y)
      z)))
```

### Grammar

Official:

- <https://webassembly.github.io/spec/core/text/values.html>
  - this has semantics with => , which is a little confusing

More readable referenec impl, with some differences

- <https://github.com/WebAssembly/spec/blob/master/interpreter/README.md#s-expression-syntax>

```
num:    <digit>(_? <digit>)*
hexnum: <hexdigit>(_? <hexdigit>)*
nat:    <num> | 0x<hexnum>
int:    <nat> | +<nat> | -<nat>
float:  <num>.<num>?(e|E <num>)? | 0x<hexnum>.<hexnum>?(p|P <num>)?
name:   $(<letter> | <digit> | _ | . | + | - | * | / | \ | ^ | ~ | = | < | > | ! | ? | @ | # | $ | % | & | | | : | ' | `)+
string: "(<char> | \n | \t | \\ | \' | \" | \<hex><hex> | \u{<hex>+})*"
```

- We can use their int and float syntax
  - leave out hex
- string syntax is pretty much what we want, it's double quoted and has \u{1234}
  - is hex really "\ff" ?  Not \xff

