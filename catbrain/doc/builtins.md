catbrain Builtins
====

## Core Language

- fn
- for while
  - break continue
- if case
- try error
  - error is equivalent to const [:error [status 1 message "failed"]]

- =
  - without args, it just prints the stack
  - = array 0 .field  # prints this expression
    - this is a bit like jq I guess

## Traditional Stack Manipulation

    dup    # duplicate top element
    dup 2  # TODO: could do this

    pop    # throw away 1
    pop 2  # throw away 2

I think there is "swap" an dall that

## Async Runtime - there is an io module

    io extern ls /tmp  # shortcut for typing is 'x ls /tmp'

    io forkwait { echo hi; x ls /tmp }

    io read; assign buf
    io write foo bar

    # problem: this is global process state.  Other
    io redir {
      echo
    }

    io read %fd; assign buf
    io write %fd %value

And the `io` module is an Obj!   Just like in YSH

### Catbrain is more explicit


    fn add -- x y -- result {
      # leave this on the stack
      stdout {
        extern expr %x + %y
      }
    }


    const 3
    const 5

    add  # does not work, missing args

    add ^ ^  # pop each one off, so it's add 5 3

Then

    stdout { date '+%D' }
    echo ^

is like

    const %{ date '+%D' }
    echo ^

You can also do

    echo %

To leave it on the stack

## More

### Control Flow / Compound Commands

- arbitrary loop may be disallowed in catbrain, allowed in shbrain, etc.
  - `loop` - 
- limited to data
  - `for` - loop that is limited to data
- `break`
- `if`
- `capture feed`

Question: `def` is like a macro?

### Stack

- `const'
- `getvar'
- 'dup`
- TODO: `pop`, `clear`
- `empty-stack`
  - extensions: is-zero, empty-string
- `ch`
  - `ch tab space newline sq` - or `apos` is HTML name?

### I/O

- `w; r 3`
- `w-line r-line`
- `log`
- `flush`

### Compute

- `op`
  - `fib` - to generate work without writing `bf`
  -  rotate` - trivial string function

### Process

- exit
- msleep
- load
  - argv
  - now
  - pid
  - env
  - counter - TODO: fix counter

### Transform

- decode
  - json string
  - j8 string
  - netstr
- encode
  - json string
  - j8 string
  - netstr

### Protocols

- FANOS
  - todo: hook up py_fanos?
