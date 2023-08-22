## Pattern matching for List, like OCaml

I guess OCaml has polymorphism, but it doesn't have dynamic type tags

https://github.com/clojure/core.match

    (match (tag obj)
      [Bool (echo "bool")]
      [Num (echo "Num")]
      [Vec (echo "Vec")]
      [List (echo "List")])

Then you can recurse

The Num can be converted to strings I guess `<Vec Num>` type is a string

But how would you even declare this in a static language?

    (def x 3)
    (def [x Num] 3)

    (def [y Bool] true)

    (def [v (Vec Num)] [1 2 3])
    (def [v (Vec Num)] "abc")  # also a valid

    (def [v List] "abc")
    (def [v List] any)

A List is almost like an Any type?

Or it's really a pair?

- List Any Pair?
  - does it have efficient (tail) ?
- Once you have List, do you need Nil?
  - (rest x)

Or can you define your own sum types?  Union types?

    (Enum list
      Null
      [Boolean [b Bool]]
      [Number [n Num]]
      [Vector [v Vec]]
    )

Then you can instantiate it

    (def [x list] Null)
    (def [x list] Null)

So Yaks is a static language, and you can model a dynamic language in it?

Yaks-TAPL in Yaks-Shak:

    (Data Bool
      [tag 'Bool']
      [value Bool]
      [loc Num]
    )

    (Data Num
      [tag 'Num']
      [value Num]
      [loc Num]
    )

    # TODO: can we use these strings?
    (Enum op
      '+'
      '-'
      '/'
    )

    (Enum expr
      (ref Bool)  # shortcut for [Bool (ref Bool)]
      (ref Num)
      (ref Symbol)

      [If 
        [tag 'If']
        [loc Num]
        [cond expr]
        [then expr]
        [else expr]
      ]
      [Binary
        [tag 'Binary']  # is this assigned automatically?  Integer tag?
        [op op]
        [left expr]
        [right expr]
      ]
    )

    (Enum type
      Bool
      Int
    )

    (Enum value
      [Bool (ref Bool)]  # Zephyr ASDL Bool %Bool
      [Num (ref Num)]

      (codegen 'foo' 'bar')
    )

    (Fn identity [x] x)

## Macros

    (Data Token ...)
    (Enum list ...)
    (Fn parse ...)

    (def Token (data ...))
    (def list (enum ...))
    (def parse (fn [x]...))

## More Types for Eval Apply

CST

    Node = Bool | Int | Str | Symbol | List

TODO:

    List = ( Node[], location )

We have


   Expr = Bool | Num | Symbol
        | Binary | If | Error

TODO: add

        | List    # function call
        | Symbol  # name lookup (if it's not a special form!)

- "Inherited" from Node, no need for new data type
  - List -- 
  - Symbol -- 

- Will need to add
  - Def
  - Do
  - Fn
  - EmptyList -- this is a special value that evaluates to itself!

  - Call  - ((fn [x] (+ x 1)) 42) is a call
    - it just contains a List, that's it?
    - List is a valid Expr?  Ok probably

## Idea: No Str, it's a List[Num], can be static

- String literal syntax is compiled to a list of integers
  - could be unicode runes?

- This is just like WebAssembly!
- But you can have string output
  - You can do `(echo "hi")`
  - so `echo` a list and it prints it all as ASCII

- The language can still be homoiconic because of this
  - Bool, Num, List
  - It's a bit like fundamental computing: Bool is condition, List is iterative
    - Num is for doing graphics and stuff
  - It's a bit like C and web assembly too!
    - You can have a NUL terminator
    - Or you can make a length prefixed string
    - It's up to yo

- File descriptors are Num as well

## Language of Types

    Bool  Num  Float   Str
    (List T) e.g. (List Int), (List Str)
    (Dict K V) e.g. (Dict Str Int)

Could also be

    <List T>
    <Dict K V>

    <Num>
    <Vec T>

    (def Person (data
      [name Str]
      [age Int]))

    (def word (enum
      [Operator (typeref Token)]
      [CompoundWord (typeref CompoundWord)]
      [BracedTree [parts (List word_part)]
      ))

    (def-data ...) (def-enum ...)

    or maybe capital letters for these macros

    (Data Person
      [name Str]
      [age Int])

    (Enum parse_result
      EmptyLine
      Eof
      [Node [cmd command]])

## List vs. Vector

- Clojure supports (rest [1 2 3]), but it gives you a List back
  - it uses ISeq I guess

- Mandelbrot wants the Vector type
- Shak wants the list data type
  - and anything homoiconic

  - List is inherently heterogeneous
    List = Foo | Bar

- Idea: Vec is homogeneous, flat, optimized type

- List is recursive type
  - maybe it's inherently dynamic, inherently ANY
  - in WebAssembly or C, how would you represent it?
    - pointer to a heap?

- `Vec<Num>` or `(Vec Num)` or `<Vec Num>`
  - can also have `<Vec List>` ?
  - `<List Vec>`

- I guess you could write a compiler that translates recursive
  - map()

- But I want to write an iterative style

- Common Lisp: <https://rosettacode.org/wiki/Mandelbrot_set#Common_Lisp>
  - uses imperative `do` loop, and `aref` for array reference

```
(deftype pixel () '(unsigned-byte 8))
(deftype image () '(array pixel))
```

- Clojure:
  - <https://rosettacode.org/wiki/Mandelbrot_set#Clojure>
  - uses `iterate`
  - uses `doseq`
- Actually you don't realy need data types?
  - you just print ASCII sequentially?
  - You could do that without a vector type
  - Just Bool Num If Func 
  - I guess just hard code doseq ?  It's a special form?
  - This is a static language



### Dynamic Pair type ?

- is it tagged?

- Key point is that it has to represent code

- How do you represent?

- Then do you need a string type?


### Int Float?

- If you think of it like WebAssembly, you might want these
  - could even have i32 i64 f32 f64
  - but probably just i64 and f64




## Three Dialects

- Yaks-TAPL, the toy language : Bool  Num
- Yaks-Mandelbrot :  add (Vec T) Func
- Yaks-Shak , also Yaks-Yaks
  - Str - length prefixed
  - Enum, Data -- to represent Node/Expr/Type
    - named fields

  - Do you need Dict (Map K V) like ASDL?
    - I guess this compiles to the mycpp runtime, so it's worthwhile
    - You would need a WASM vesrion too


- (foo.bar) infix?
- obj.method()

 
- Key point: Yaks is not a Lisp!  Because it's static
  - There is never a (head tail) etc.
  - I want macros, but I guess that means you write a Lisp in YAKS!


So that's Yaks -- a statically typed language implemented in TypeScript

And then Shak

Shak is the Lisp with shell features!  It uses the  same syntax!

  Same  lex.ts, same parse.ts


## Special Forms for Yaks vs Shak

- Yaks
  - (if true 1 2)
  - binary (+ 1 2)
  - (fn (-> [x Int] Int) x) - REQUIRED annotation?
  - (def x y)

- Shak - macros?
  - if
  - binary
  - fn but dynamic, not static
  - def but dynamic

  - $(echo hi) is (cmd 'echo' 'hi')
  - (quote echo hi)

  - (head tail)

## Shak Data Types -- Or call it Yasp?


Key point is that it can represent:

- Yaks code
- Shak code

And it can do macros.  Key point: Yaks can't represent its own code!
Shak can't re


    (Enum value
      Bool
      Num
      Str
      List  # single compound data structure
      Func
    )

Yisp


## Zephyr ASDL Metaprogramming

- Yaks could be `Data` and `Class`, like C++
  - or just Class

  - SUBTYPING with MULTIPLE inheritance!!!

- I guess you want Enum type?  for strongly typed tags?
  - then you can compile to C++ in a source fashion?


- And then write a Shac macro for ASDL enum and data!
  - Yes!!!




## Key Points / Relationships

- Yaks is a simple ML, used to implement Yaks efficiently

- Shac can represent and serialize BOTH Shac code, AND Yaks code!Y

- Shac can be used to metaprogram Yapk!!!!




## Summary

- Yaks-TAPL - Bool Num

- Yaks-Mandelbrot - Bool Num (Vec T) Func

- Yaks-ML- Bool Num Str (Vec T) (Map K V) Func (Enum ...) (Data ...)

  - Yaks-Meta
  - Yaks-ML

- Shac or Shec
  - Bool Num Str List (DYNAMIC) Func
  - Only ONE compound data structure
  - It uses SHAKON


Yaks could also be Maks?

## Names

- Shak
- Sheme

- Yeme
  - Yaks and Yeme
  - Scheme in Yaks, but with Shell

- Mesh, MON

- Schak  -- Scheme
- Schek

- Yaks and Shak or Shack

- Shack has letters from Scheme

- Shac

- Yaks and Shac
  - Shac: Scheme with Shell Features
  - Shec: Scheme with Shell Features
    - pronounced "Sheck" ?
