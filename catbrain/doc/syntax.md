Syntax
======


## Syntax Design issues

- operator char issue
  b'hi'
  that's different than b 'hi'
  - I don't want a special rule for  this

- %error is not splicing?
  - maybe it's !error or &error
  - yeah I think & { echo }  and &error are good
    - you look one token ahead

- but what about
  - & x -- { echo hi }
  - & error -- { echo hi }  - this would be ambiguous

- so maybe
  - &&error 
  - !error
  - %%% - not readable
  - #error - this would be a comment?

## Tokens

- Space ''
- Newline '\n'
- Comment   # to end of line   - so then this does NOT need a space?
- Unquoted  `[a-z A-Z 0-9 / _ . - \]+~
  - \ is for Windows paths, and custom \n dialects - they may be different

  - TODO: do you need VarName?
  - because '/-foo-' is not a valid variable name.  For %var
- Quoted    'hi'
- Operator  ; |    % [ ]   & { }

- anything else: lexical error
  - that means ( ) is reserved, but not used

## Grammar

TODO: check this

           # note: there is no equivalent of "x$foo", that's %[join [x %[foo]]] or perhaps
           # %[join x %[foo]]
word        = Quoted | Unquoted | subst | splice

           # can expr-splice be empty?
           # was that the top, or is that %1 and %%1 ?
           # %%1 is the NUMBER of things
           # then %[] I think makes sense as the top value; is the same as %{ top } ?

expr_subst   =     '%' '[' cmd ']'      # %[mydict .field 0 .other_field]
expr_splice  = '%' '%' '[' cmd ']'
stack_splice = '%' '%' 1                # this is a little weird because there's no '1' $1 var, it's the NUMBER
                                        # I suppose that %1 could be top, and %2 could be second from top
                                        # and then %%2 could be them BOTH
error        = '%' 'error'              # is this OK?

             # maybe allow %var, and then %error is just special?  Sort of like 'null true false'
             # those could be added to certain dialects
             # then you need a "varname" token, which is different than WORD

cmd_subst    =     '%' '{' seq '}'      # example: %{ echo 1; echo 2 }
cmd_splice   = '%' '%' '{' seq '}'

             # a list is how you write long multi-line commands
sep          = Space | Newline
list         = '[' (sep? word)* ']'

cmd          = (Space? word) (Space word)*
end          = ';' | Newline
pipeline     = cmd ( '|' cmd )*
seq          = pipeline ( pipeline cmd )* end?

block_fn     = '{' cmd* '}'
fn           = '&' word* '{' cmd* '}'


push [ls -a -l]
%%[] or %%1   # splice the top 1


Difference betwen expr and command?

- expr are structured values you leave on the stack?
  - expr are INTERIOR values
- cmd are STREAMS
  - they are EXTERIOR values
  - so we have to capture stdout?

Most commands don't produce any external value though?

So these are exterior:

- pipelines
- cmd sub and splices %{} %%{}
- extern ls foo

Is everything  else interior?  We could have redirects later

I guess

## Operator Chars

Lexical:

- space
- # for comments

Literals:

- type Error
  - I think it's %error, because %[] is how you splice
  - %foo is invalid for now
    - well I might want %var ?  I think it's easy to type without
  - && ?  so we don't take any more chars?
  - ! - maybe just take this?    Or ?
  - or &!
  - I think %error is more readable than those

- type Str
  - '' single quotes
- type List
  - [list literal [is nested]]
- { } invokable Obj type
  - & { } - another invokable object
  - & -- { } - another invokable object
  - & x -- result { push %[x] } - another invokable object
    - or return x?

Commands:

- ; sequence
  - newline is a synonym
- | pipeline
  - this is arguably optional, but should be core I think
  - it is part of the shell runtime
  - redirects too, but those

Note that a sequence can be like an interior pipe:

    push [foo bar]; for x {  # bind each thing to $x
      echo %[x]
    }

    push [foo bar]; for {
      echo %[top]
    }

does %[top] actually work?  Should it be %[]?  This is a no-op

Because top evaluates to the top value?  But that's not a command?  

Is the concept of a "return value"  different than "leaving on the stack"?


Substitution and splicing:

- %[expression sub] %%[expression splice]
  - %%2 stack splice
  - %1 stack sub?  Is this the top?
    - this is useful in the data language

  - does %error make sense, or should we use a different symbol?
    - %error is not indexable, like a list or map is

- %{command sub}
  - and %%{command splice}  (placeholder for this; requires j8 lines)
  - issue: does catbrain have j8 strings?
    - yes, you can write j8 parser in catbrain itself

Expressions

- %[expression .0 a foo] including %[var]
- so then `.` is special?
  - I think this is an instance of RE-PARSING
  - so we want TOKENS
  - foo.c is not special
  - so we are doing RE-PARSING YES

### Reserved Chars / Allowed Chars

Allowed

- `.-_/` for foo/bar/baz.c
  - this means subtraction and division aren't operator characters
  - and also `%[mydict .field]` is allowed

Reserved

- and I guess `*.py` for globs?
  - what about `?`  It's debatable
- what about 
  ~ tilde sub

- I guess I don't know how to these language extensions should be parsed in the bicameral syntax
  - do you have the shell concept of delimiting chars?
  - so `**` and `~~` become 2 operators?
  - what about comments `#`?
    - I guess you could strip them until end of LINE?
    - or are they built in?

- `()` - not doing anything with these now
- `<>` - not sure if we have redirects, can hardcode them I guess
  - 2>&1 - not sure

probably

    redir '>out.txt' { echo hi }

What about

- ^ ! history
- `* []` globbing


### Data Language

    [unquoted  'quoted']
    list {
      const foo
      ch \n
      const bar
      getvar x                             # is this better than %[x] or %x ?
    }; join; var mystring %1               # this means the top is x?

    list {
      list [_type Int]
      list [_data 123]
    }; make-obj; var myobj %1

Although really it should just be j8, without `''` rule

To be a GRAPH, you really need a STACK VM!  not JSON!
So actually it's easy to serialize this whole thing.

    push [_type Int]
    push [_data 123]    # data is on the TOP of the stack.  We splice from the TOP
    make-obj %%2   # this means you splice the last two values
                   # there is no such thing as %2

    # The algorithm for making a linked list is simple

    # This is where it's nice not to have any 'var'

    push %error
    push 'foo'
    push [1 2 3]  # app type
    push %[Obj [_data 123] > [_type Int]]

### Other Reserved Syntax

- `b''` is reserved, which means that a word is EITHER unquoted or has single quotes
  - there are no

- problem: then the operator char rule doesn't apply ...
  - Python has some lexing issues here too
  - hm couldn't find them

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


### Notes on Splicing

```
var expr [people 0 .name]
= expr

%%[expr]  # evaluates it, puts result on the stack

# Splice the expression, and then put the result into 'var'

var name %[%%expr]

```

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

### Lambda Syntax brainstorming

Es shell

    fn identity x { return x }

    fn identity = @ x { return x }

So you can pass stuff with

    apply @ i {cd $i; rm -f *} \
      /tmp /usr/tmp

So what is it in catbrain?

    apply { (i) cd $i; rm -f %%[io glob '*'] } /tmp /usr/tmp

    apply (i, j) { cd $i; rm -f %%[glob '*'] } /tmp /usr/tmp

This is SIGNATURE objects

    fn foo (i Str, j Str) {
      cd $i; rm -f %%[glob '*']
    } /tmp /usr/tmp


OR You can have a single "fn" keyword

    apply fn { cd $i; rm -f %%[glob '*'] } /tmp /usr/tmp

Or you can have a greedy rule?

The first { } goes with

    fn -- x y -- result

    fn ident -- x -- result {
      getvar x     
    }

Other symbols besides @ and (i)

It's like pipelines

    apply & x -- result { getvar x } \
      a b c d

That's not bad I think.  & is for function.

---

Open or closed

    # does nothing, doesn't affect the top of stack
    fn ident {
      pass
    }

    # does nothing EXPLICITLY
    fn ident -- x -- out {
      getvar x
    }

So then you also have

    # anon identity function!

    & { }

    # explicit anon identity function!

    & x -- out { getvar x }

I think this is equivalent to & { }

    & -- { }

But yeah I don't think this anonymous form should be used that often?

### Multi-line commands?

This makes it hard

   ... foo --verbose
       ;

     ls --hello \
     # can we allow this
   | other

     # I think we could change this empty lines rulwe
     ls -l \
       # can we allow this
       the directory

       ls -l \
       # comment
     | grep foo \
       # comment
     | sed foo \

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

## Survey of Lambda in Other Languages

- Haskell : `\x y -> x + y`
- Ruby: `->(x, y) x + y`
  lambda { |x, y| x + y }
  - why 2?
- Racket/Scheme uses lambda
- Clojure: `#(+ 1 2)` reader macro
- Wolfram: `Plus[#1, #2]&`
- Smalltalk: `[:x :y | x + y]`

Languages to  look at:

- Rebol
- Wolfram
- Elvish
- Rhombus Language (built on top of Racket)
- Cola object models?  Not sure these succeeded


So I think `&` is relatively good for function literals.

Could be 

- &|x, y| { echo $x }
- &(x, y) { echo $x } 

- & x y -- { echo $x } - might be better for syntax highlighting
  - later types could be
  - `& [x Int] [y [List Int]] -- result { echo hi; y }`

## Object Literal Syntax

What about object literal syntax?

- `[] --> []`   is what Oils uses

Meh I don't think we need it

I think it's just

    make-obj [__data x] [__type Int]

And then to assign it's

    var myobj %[make-obj [__data x] [__type Int]]

Splice the result 

