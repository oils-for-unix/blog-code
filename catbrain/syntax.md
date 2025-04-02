Syntax
======

## Operator Chars

Words:

- '' single quotes
- space
- %[expression sub] %%[expression splice]
- %{command sub}
  - and %%{command splice}  (placeholder for this; requires j8 lines)
  - issue: catbrain doesn't have j8 strings?

(no double quotes)

Commands:

- ; sequence
- | pipeline
- { } blocks

Expressions

- [list literal [is nested]]
- %[expression .0 a foo] including %[var]
- %%[splice expression]

### Notes on Top Value

- and I think _ means the top value?
  - So you can do `%[_]` or `%%[_]`
  - or maybe `%` and `%%` ?  That is ambiguous
    - % can appear at the end, while %% can appear in a word
  - or maybe ^ and ^^
    - this is kind of like "history" , so it could work
    - this is the top value, but POPPED



```
fn open {  # any args are the top value?
  ls --verbose %%

  # This pops it off the stack?
  ls --verbose ^^

  # singular versions
  ls --verbose ^
  ls --verbose %
}
```

Does YSH need this?

   call f(x)
   ls --verbose ^^
   ^hi^bye is history - onl works as first word

Now I wonder if there is a "command sub" thing?

Like %{echo hi; echo 2}

That is very shell-like, so probably.  I guess it strips the trailing newline
too?

Consider:

    sh$ ls --flag=$(date +%D)

Otherwise it would be

    cb$ stdout { date +%D }

    cb$ ls --flag=%[_]  # top value
    cb$ ls --flag=^     # top value

- %%{echo 1; echo 2}  # are these the quoted lines or what?
  - do you have j8 lines?
  - it has to be, for YSH and catbrain to talk to each other
  - however I would like to implement the j8 string parser purely in catbrain
    - probably with regexes?  But in UTF-8 mode

### j8 idea

    echo u'hello'
    echo b'hello\n'

I suppose we can allow this?

Or at least we leave space for an extension?

Otherwise it's

    echo %{c hello; ch newline}

If we have YSH @(command; splice) as CB %%{command; splice}, then it makes
sense to have the string syntax too

Because catbrain can deal with arbitary strings

I suppose we could only have the rule for b'', and not u'', because it's a superset

And then even interpolation

    echo b'hello \$name' is technically valid

### netstring idea

Crazy idea is that

    write-lines %%{netstr one; netstr two}

This could be NETSTRING parsing

Arbitrary data is extremely unlikely to be netstrings

So this could be a way of communicating lists and maps with catbrain

    cat j8-lines.txt | j8-to-nets | cb-sh 'read-nets'

Yeah I kinda like this

So you use separate tools

And now you have lists and maps

    ls | lines-to-nets | read nets

Or maybe you can install a default hook, like

    shvar command-splice-hook=netstring {
    }

    shvar command-splice-hook=lines {
    }

Yeah that is probably more practical

Could do that in YSH too

### Lexer

Tokens:

    # includes { } because we want spaces, like YSH
    UNQUOTED = / [a-z A-Z 0-9 '_{}']+ /
    LBRACE = / '{' /
    RBRACE = / '}' /
    
    SQ = / \' [^ \']* \' /
    SEMI = / ';' /
    NEWLINE = / \n /
    
    # These are ignored by the lexer
    SPACE = / ' '+ /
    COMMENT = / '#' ![\n]* /

### Grammar

    program = Eof | seq Eof

    terminator = semi | newline+

    seq = NEWLINE* cmd (terminator cmd)* terminator?

    block = '{' seq '}'

    arg = word | block

    # Flexible, uniform syntax:
    cmd = word arg*  

YSH RULES
    cmd = word+ block?  # like YSH, one optional block

Enforce these OUTSIDE the grammar:

    0 args                      - msleep
    1 word arg                  - w-line hi
    1 block arg                 - loop { w-line hi }
    1 word arg and 1 block arg: - if eof { break }

Slogans;

### YSH Subset Issue

This is valid catbrain, but not YSH

    foo { echo arg1 } arg1
    foo { echo arg1 } {
        echo arg2
    }

We can disallow it statically in catbrain if there is always a rewrite

### Keyword/Builtin Conflicts

Get rid of YSH keywords?

- .if .for .try
  - x or .extern
  - const -> .const or val, lit
  - fork forkwait builtin
- TBH I like using the same name
  - as long as they do SIMILAR things, not identical, it could be OK
  - I think the YSH convention could be to add it

```
if empty-stack {
  break
}
```

YSH

```
.if empty-stack {
  .break
}
```

