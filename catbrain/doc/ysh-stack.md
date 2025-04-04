YSH Stack Manipulation
=====

## Summary

We have

    $^ and @^ in command mode (need to train people to use right pinky, not left one)
    ^ in expression mode

    - operator to append to stack


### New verbs

- `pop` command
  - maybe: `var x = _pop()`
  - though that's the same as: var x = ^; pop;

- `smash` - clear the stack
  - because `clear` is taken
  - could be `wipe` too
  - forth uses `clear`

- could also be its own builtin:

```
stack pop
stack clear
stack show  # same as =
```

Yeah that's not bad

### More

## Notes

In command mode, I might want:

- echo $$ and @@
  - but `$$` is the PID - I don't want to clobber that
  - maybe `$[]` and `@[]`
  - empty expressions mean `_top` implicitly
  - yes these are allowed

- there is also ! and !!
  - maybe I can fold history in, and repurpose those
  - `!!` already means last command
  - ^foo^bar works on the first word
  - I think we could take it in other words - `parse_caret`

- and then

```
echo $[^]
echo @[^]
```

```
# These are not taken!
echo $^
echo @^
```

That is good!

So yeah history is another thing to add

Then is it

- `$[]` `@[]` - top
  - expression is `_top` or `_top()`
  - I guess `_error` becomes the `_top` then, and then there is a `:fatal` or `:error` value?
  - similar to `null`
- `$^` `@^` - pop?
  - expression is `_pop()`

    = 1 + 2  # pretty printing
    =   # print the top !  Yes!

    - 1 + 2  # append to the stack - this works like a list item

List {
  - 'hi'
  - 'there'
  - 'f'
}

Yeah this is cool!

It's an implicit stack

- Then you can splice with @[] 

I am not sure if you need `$^` and `$*` and `_pop()`

- I think probaly you just need


What do errors look like?  I think we want a dict?

    {:error: true, ...}

    {'0': ERROR}   # this is an idiom for tagged/"TYPED" dicts?  Use the 0 key?
    {'0': ERR}
    {'0': error}

Maybe we also have:

    %true
    %false
    %null

In addition to `true false null`.    And there is just %error, not plain error.

They become SYMBOLS?

But maybe it's value.Error

## Nested and Structured Errors

- simple commands
- pipelines
- process sub
- from failglob
- from redirects - can't open file, e


Example:


    ysh$ - {k: 42}
    ysh$ =              # prints the entire stack
    (Dict)  {k: "42"}

    ysh$ json write (_top)

    ysh$ json write (^)  # maybe ^ is an expression?

I think it could be

    $^ @^ and ^ as expression

That's always the top of stack.

And there is a `pop` command too



### Moving back to stack

    var x = ^

    builtin var x $^

Yes this is the way!

## What you can do with an expression

- pretty print it with `=`
- append it to stack with `-`
- throw it away with `call`

