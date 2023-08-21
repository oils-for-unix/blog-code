Yaks
====

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

## Example of Code that could work in both dynamic and static modes

Maybe all this can work?

I wrote it dynamically.  Seems like it can be static too.

Use of strings for tags everywhere is interesting.

```
function parseList(p: Parser, end_id: string): List {
  next(p); // eat (

  if (p.current.id !== 'name') {
    throw { message: 'Expected name after (', loc: p.pos };
  }
  let list: List = {
    tag: 'List',
    name: tokenValue(p.current),
    loc: p.pos,
    children: [],
  };
  next(p); // move past head

  while (p.current.id !== end_id) {
    list.children.push(parseNode(p));
  }
  next(p); // eat rparen / rbrack

  return list;
}
```
