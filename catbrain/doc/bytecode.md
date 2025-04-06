Bytecode
--------


BICAMERAL syntax idea

We parse and get the CST - the token tree

And then we can either:

- transform to AST
- transform to bytecode

OR

- maybe directly translate to bytecode
  - with jump


## Compound

### Conditional

    if test %[x] -lt 1 {
       echo hi
    } elif test $[x] -lt 2 {
        echo hi
    }

    match

### Loop

    while test %[x] {
    }

    const [a b c]; for x {
       echo %[x]
    }

    const [[name bob] [age value]]; for key value {
       echo $key $value
    }

    break
    continue

### Errors

    try {
      ls %[x]
    }
    if failed { echo hi }

    catch ls %[x] & {
        echo hi
    }

## Functions

    # what about things that might return nothing, or an error?

    fn foo -- x y -- result {
    }

    # %% is like ...
    # but it might not return a result
    # maybe | error

    # I guess if | is a token, we can parse this ahead of time

    fn extern -- %% -- |%error {
    }

### Bytecode

- control flow
  - `jump 1`
  - 'jump-if-false'

- functions
  - `invoke` - for invokable object
  - define?   Is this a special bytecode?  Probably
  - return?

- extern - external command?  Is it statically resolved?
- builtin - user-defined builtins

- stack
  - `pop`
  - `get-const 1`

- vars
  - `get-local 1` - variables are compiled AHEAD of time
  - `get-global 1` - variables are compiled AHEAD of time

- list bytecodes
  - `getattr`
  - `setattr`
  - `hasattr` ?

- string
  - equals

- integer (using string)
  - greater
  - less-than
  - inc  # I guess everything can be done with inc

- `make-list`?  # for the value stack?  I guess this is primitive

I guess we have to organize the VM a bit ..


