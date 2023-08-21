Tea
===

A language that's like our use of Python and mycpp:

- Dynamic semantics, and an interpreter with REPL
- If it's 100% statically typed, then it can be compiled to fast C++, on our runtime
  - Not sure if we want gradual typing, you might be forced to go from leaves
- Extra
  - Dynamic semantics produce either JSON, or ASDL-like "pickles" (squeeze and freeze?)
  - These can be frozen into a C++ binary as static data (zero runtime cost)
  - So it's like a comptime

## Language of Types

    Bool  Int  Float   Str
    (List T) e.g. (List Int), (List Str)
    (Dict K V) e.g. (Dict Str Int)

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

## Comptime / Freezing

- Dynamic semantics can give you JSON-like data literals?  That you include in
  your SCRIPT!
- Static semantics give you structs and arrays, using C++ literals syntax?

