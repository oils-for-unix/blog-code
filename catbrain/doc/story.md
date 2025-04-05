Story of Catbrain
====

Where did catbrain come from?

## July 2024

Thinking about the xargs -P problem

- I think it was the Ninja thread, and the zig build system thread
  - Ninja buffers the output
- There I started researching an async runtime 
  - but that doesn't fit with shell's waitpid(-1) model
  - TODO: link to 2022 blog post

- Also generating testdata for xargs -P
  - I wanted to do it with a "brainfuck"-like langauge

- jq in jq thread - streaming language with no vars
  - it sort of has an implicit operator, with .  -- this is a function and not
    a value?  It's a bit confusing
  - brainfuck also has `. ,` for input and output
- I said "Shell, Awk, and Make should be combined"
  - Koichi also agreed that jq should be combined
  - jq has all these string, list, time/date functions, similar to Awk
  - it basically exposes a binding to libc, which I don't think is great
    - all these "weak languages" use libc as their stdlib

## March 2025

- Confetti config language popped up on Reddit
  - it's untyped - everything is a string
  - similar to Tcl - except it's code, not data
  - similar to kdl, which I had seen before
  - I was working on Hay at the same time
- Hay version 1 the `_hay()` "register" - but how about turning it into the VALUE STACK?

## Past Experiences

- protobuf tools - I always wanted to have something you could "append code to"
  - I had this "Cpp stack" idea
  - there I wanted to bind to lots of proprietary C++ code
  - (also that would been perfect for the GFS/CFS shell thing I forked/worked on)
- "shell has a forth-like quality"
  - can we preserve "bernstein chaining" in an actual stack-based language?
  - realization: we can concatenate WORDS
    - but the stack model also lets concatenate COMMANDS
  - I've also been looking at various notebooks, like Jupyter, Quarto, etc.


## Other Notes

What comes after crafting interpreters?  It has objects and closures, but it doesn't have

- A module system
  - YSH treats modules as objects

- Data structures
  - UTF-8
  - big num - though catbrain won't have that

- A REPL!
  - parsing issues - the $PS2 problem
  - embedding in a GUI, which uses an event loop?
  - writing a REPL in Lox, or in catbrain
  - and also asynchrony, e.g. select()

## Something that bugs me about shell, that could use async

    sleep 3 &

I only get a notification when I hit enter.

I should get a notification immediately - and the notification could be in GUI

There is no place in the UI for notification!

It also makes the shell hard to test!

