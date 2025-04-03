Tcl vs. Catbrain
----------------

- Tcl
  - <https://wiki.tcl-lang.org/page/Dodekalogue>
  - <https://wiki.tcl-lang.org/page/Unix+shells> - vs shell

## Semantics

Data Model:

- Tcl has only `Str`
  - although there is a funky "dual" nature to the VM
- catbrain has `Error Str List Obj Fn`

Machine model:

- catbrain has a stack like Forth
  - this is mainly influenced by the shell idea of 'ls /tmp; echo status=$?'
  - you can think of the status `$?` as being pushed on the stack
  - but in catbrain, it can be any value
    - errors abort the interpreter, unless caught by `try`

## Syntax


Different:

- Tcl `$VAR` vs `{*}var` is our `%[var]` vs. %%[var]
- Tcl [command sub] is our %[expr sub] and %{command sub}
- Tcl $array(i) is our %[array i]

- we don't have backslash sub right now
  - although we would add it with b'\n' which is J8 notation
  - could be easy to do, especially if the parser is in catbrain itself

- catbrain has special syntax for pipelines: `ls | wc -l`

Similar

-  {} are usually command blocks, although we statically parse them




