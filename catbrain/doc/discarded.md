
## Layered Syntax

BAD IDEA - due to scope.  Too complex

- words '' and [ ] nesting { } are level 1
  - and probably ; for sequence
  - and & { } for function with args
    - not sure about def
  - this ensures easy syntax highlighting?

- Level two
  - all keywords - if case, for while, try error
  - | pipelines - because it's closures
    - does this get rewritten to dup or something?
  - anything involving word parts
    - glob *
    - tilde sub ~
    - cartesian product 
      - I think it has to be a string %%[words '{alice,bob}@example.com']
  - I'm not sure if you want
    %[] %%[]
    %{} %%{}

    I think you desguar them
    I think %[] is the value stack, and %{} is stdout

    and then splicing is derived
    Or other way around - splicing is more general of course - you would have to wrap it in a list 

- the problem is SCOPE
  - can you


### Do you need word_part?  No this is a separate layer

- because --verbose=%[val] is required, not just --verbose %[val] (with space)
  - this should be practial for typing
  - you don't want %[string { const --verbose; getvar val }

Other word language things

    ls ~/src               %{home-dir; const /src}
                          Maybe we need to rewrite ~ to something else

    ls *.py           # splicing  %%[glob '*.py']

    # Which one of these does cartesian product?
    ls %%[a]-%%[b]   # this can do cartesian product
    ls %[a]-%[b] 
    ls %[a]-[a b]

    ls {alice,bob}@example.com

    ls {alice,bob}@example.com

    # Hm is a list literal a word part?  I guess it could be
    ls [alice bob]'@example.com'

    My problem then is:

    b'fo\n'  # no J8 notation extension

Drop these features:

- ~andy
- ?.[a-z] - those can use glob ''

But yeah, these are word parts

- %[var]
- [my list]
- unquoted

Not sure about:

- 'quoted', because that has the j8 issue

Also, for elegance, I am resisting parsing ""

Although I suppose that can be desugared

Cheap hack:

    [alice bob]"@example.com"
    %[names]"example.com"
    b'hi'

Technically those don't conflict

So "double" can be a word part ... but 'double' is not

I wonder if we give in and do $x $y

- I guess $x is a string, but % is a value, and %% is splice
  - I suppose it doesn't cost that much more for either
  - the problem is that $x implies ${x}_foo, which I don't like

That can be solved with

    ls $x"_suffix"

Ugly:

    ls "foo"$x"_suffix"
    ls "foo"$[x]"_suffix"

    ls "foo${x}suffix"

    # Compatible with YSH
    # I guess we can allow  $name $[name] %name %[name] %%[splice]  %{echo hi}
    # then %error sorta makes sense
    # It's at least consistent
    ls "foo$[x]suffix"

    # actually this isn't bad
    ls "foo${ ch newline }suffix"
    ls "foo${ ch tab }suffix"

This is a general method of escaping

So that "" is a WORD, and it is not a word PART
