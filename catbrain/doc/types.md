catbrain Types
=====

- Error Str List Obj Fn 
  - Error type, in place of exceptions
  - no Null then?  try can turn %error into ''
    - yeah I think that is reasonable
- Str used as Int and Bool; List used as Dict with PList representation
  - List has optional "HASH PART" - this is lazily computed whenever you do
    "getvar", on anything that's more than say 10 properties
    - so you don't use extra GC space on non-lists
- Obj is a pair of List and Obj
- Fn is used for both proc and func
  - oh and it's also used for "block"?  It has no params
  - then you can call 'eval(vars=vars)' as long as there are no params?

Place is not necessary?  I think you just use the 'command ...; assign foo pattern

- Idea:
  - could Fn just be a invokable Obj?  with `__invoke__`?
  - then why not Error, Str, List objects too?

---

Minimal

- Str
  - this is the only thing that's not an object? for small string optimization
  - you can think of it as an "atom" too
  - you can simulate integers with it

- List
  - is exterior, untrusted, arbitary data
  - it's just a vector


- Obj
  - this is List and it has tail(obj)
  - it also has `__invoke__`
  - What about everything else?
    - I think

- Error
  - does this need to be separate?
  - it can it be a special kind of object?
  - with `__error__`

- I think if the first item of an obj is `%error`, it can be considered an error


Optional Unifications:

- Closures are just Obj?  i.e. a linked list of stack frames?


Implementation / GC Types  vs. Application Types
------------------------

- Atom (aka Str)
  - self-hosting note: must be bytes.  In JS this is buffer; in Python 3 it's bytes.
- Obj
  - this is a pair of (Vector, next)
  - List is expressed with this

now the question is: what about the error value?
  - is that NULL pointer?

I think that's fine.  But what about a function that returns nothing?  What
about the sentinel?

- (Vector, next) - next is a pointer.  So NULL might be bad


I think you only need two bits from each `uint64_t` value or `uint32_t`:

- 00 - Obj pointer
  - no masking
- 01 - this is a string
- 10 - this is the error value

The value `11` is not used.

Serialization of GC Heap
----

- j8 strings `b''` (or `u''`)
- [] syntax, without commas
- %error

Integers and Floats Built on Top
-------------------

They will be like

- `[] --> [__type__ f]`


PROBLEM: `__type__` is more than 6 chars.  So it should really be `_type`


- `[_data 123] --> [_type Int]`

Or is it like this:

- `[_data 123] --> [_type & { fn }]`



Maybe we have List -> Obj filtering?

List can't have any string keys?

List is pure untrusted code

Idea for Oils

- `Obj({}, null)`
  - this should actually VALIDATE the keys
  - none of them should begin with `_`? or `__`?
  - there is no private setate

- YES
  - this prevents spoofing of `__type__` and so forth
- TODO
  - `__type` and `__data` and `__call` fit in 6 chars, small string optimization
  - `__invoke` doesn't (and `__invoke__`)
    - maybe make it `__inv` or `__do` or `__cmd` or `__proc`

Tag Idiom?
--------

Maybe this is an idiom:

    ['' :error foo bar]

- Rather than methods?
- but you can't serialize that anyway?

I think YSH should have Obj

    [] --> {__error__: true}

    [] --> {__type__: 'Dict'}

    [] --> {__type__: 'Error'}

or maybe

    {} --> {__tag__: 'Dict'}
    {} --> {__tag__: 'Error'}

You can leave this on the stack ...

Why doesn't this work?  It's because `__tag__` data can introduce security problems

So it has to be

    {} --> {__type__: & { const 'Dict' } }
    {} --> {__type__: & { const 'Error' } }

const basically means "push"


### JSON Mapping

Wire types vs. application types

- `[_data null] --> [_type Null]`
- `[_data true] --> [_type Bool]`


- This part is good, because you can simulate JavaScript semantics too!
  - `[_data 123] --> [_type Int]`
  - `[_data 123.0] --> [_type Float]`

- `[any list 'data']` - don't really need `_type`
- `[k v k 2 but not __ keys] --> [_type Dict]`

And then you could do more types:

- date/time, etc.
- These are all application-specific

## Crazy idea: arithmetic and eggex self-hosted

I guess looke at Rhombus
