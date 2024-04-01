Shell Injection Demo in Rust
============================

## What's wrong with this code?

    rustc main.rs
    ./main.rs

Why does the file `PWNED` appear in the current directory?

## Context

- Discussion of blog post with shell injection in Rust:
  <https://lobste.rs/s/hru0ib/how_lose_control_your_shell#c_jamktx>
- Discussion of `xz` backdoor a bit later:
  <https://lobste.rs/s/uihyvs/backdoor_upstream_xz_liblzma_leading_ssh#c_h3urdz>

The shell injection in Rust was not technically related to the `xz` backdoor.
I was making an analogy.

The point was that both of these snippets should be suspicious from looking at
just **one line**, and nothing else:

- `xz -d | /bin/bash` 
  - Because it’s a sign of compressed code in the repo or tarball. Executable
    source code shouldn’t be compressed because that’s a form of obfuscation.
    There’s no other reason for it.
- `if let command = format!("cd {:?}; /usr/bin/env -0;", dir);`
  - Because it’s string concatenation of code, without proper escaping. (This
    example has the wrong form of escaping, which is equivalent to no escaping)

I was being a bit of a dick there, to make a point.  There's a consistent
pattern of shell and HTML injections in blog posts:

- <https://oilshell.zulipchat.com/#narrow/stream/266575-blog-ideas/topic/Shell.20Injection.20in.20Rust>

Not only do people not notice the bugs, but when I explicitly point them out,
they argue that there's no problem.

We've lost knowledge.

So this Rust program is a demo of one such problem.

---

There does seem to be confusion between memory safety and string safety.  Rust
doesn't really do anything about the latter.

Another example from the thread:

- <https://lobste.rs/s/njfvjb/rustdesk_with_tailscale_on_arch_linux>




