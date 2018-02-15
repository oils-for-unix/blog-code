---
title: CommonMark is a Useful, High-Quality Project
date: 2018/02/14
comments_url: https://www.reddit.com/r/oilshell/comments/7xl82q/commonmark_is_a_useful_highquality_project/
tags: escaping-quoting usage-tips utf8
---

I write every page on this site in [Markdown][] syntax.  At first, I used the
original `markdown.pl` to generate HTML.

But I've just switched to [cmark][], the C implementation of [CommonMark][].  I
had a **great** experience, which I document here.

We need more projects like this: ones that fix existing, widely-deployed
technology rather than create new technology.

<div id="toc">
</div> 

### What is CommonMark?

The [home page][CommonMark] says:

<p style="margin-left: 1em;"><i>We propose a standard, unambiguous syntax
specification for Markdown, along with a suite of comprehensive tests
...</i></p>

Much like Unix shell, Markdown is a complex language with many implementations.
I happened to use `markdown.pl`, but another popular implementation is
[pandoc][].  Sites like [Reddit][reddit-markdown], [Github][github-markdown],
and [StackOverflow][stackoverflow-markdown] have their own variants as well.

However, shell has a [POSIX spec][posix-shell-spec].  It specifies many
non-obvious parts of the language, and shells widely agree on these cases.
(Caveat: there are many things that POSIX doesn't specify, as mentioned in the
[FAQ on POSIX][faq-posix]).

But CommonMark goes further.  In addition to a [detailed written
specification][commonmark-spec], the project provides:

1. An executable test suite, embedded in the [source for the spec][spec.txt].
1. [cmark][], a high-quality C implementation that I'm now using.
1. [commonmark.js][], an implementation in JavaScript.

[spec.txt]: https://github.com/commonmark/CommonMark/blob/master/spec.txt
[cmark]: https://github.com/commonmark/cmark
[commonmark.js]: https://github.com/commonmark/commonmark.js

Perfect!

CommonMark's tests and Oil's [spec tests][spec-test] follow the same
philosophy.  In order to specify the [OSH language][osh-language], I test over
a thousand shell snippets against [bash][], [dash][], [mksh][], [busybox][]
ash, and [zsh][].  (See blog posts tagged #[testing][].)

==> md-blog-tag testing

I'd like to see executable specs for more data formats and languages.  Of
course, POSIX has to specify not just the shell, but an entire operating
system, so it's perhaps understandable that they don't provide exhaustive
tests.  However, *some* tests would be better than *none*.

==> md-ref1 spec-test
==> md-ref1 osh-language
==> md-ref1 bash
==> md-ref1 dash
==> md-ref1 mksh
==> md-ref1 busybox
==> md-ref1 zsh

### Why Did I Switch?

I wanted to parse `<h1>`, `<h2>`, ... headers in the HTML output in order to
generate a **table of contents**, like the one at the top of this post.  That
is, the build process now starts like this:

1. Markdown &rarr; HTML.
1. HTML &rarr; HTML with an optional table of contents inserted.

The TOC used to be generated on the client side by traversing the DOM, using
JavaScript borrowed from [AsciiDoc][].  But it caused a noticable rendering
glitch.  Since switching to static HTML, my posts no longer "flash" at load
time.  

[AsciiDoc]: http://asciidoc.org/

I could have simply parsed the output of `markdown.pl`, but I didn't trust it.
I knew it was a Perl script that was last updated in 2004, and Perl and shell
share a similar [sloppiness with text](../../2016/10/20.html#perl).  They like
to confuse code and data.  This is one of the things I aim to fix with Oil.
(See blog posts tagged #[escaping-quoting].)

==> md-blog-tag escaping-quoting

This suspicion wasn't without evidence: I ran into a bug few months ago where
mysterious MD5 checksums in the HTML output!  I believe I "fixed" it by moving
whitespace around, but I still don't know what the cause was.  In
`markdown.pl`, you can see several calls to the Perl function `md5_hex()`, but
the code doesn't explain why they are there.

This [2009 reddit blog post][md5-bug] has a clue: it says that MD5 checksums
are used to prevent double-escaping.  But this makes no sense to me:
checksums seem irrelevant to that problem, precisely because you can't tell
apart checksums that the user wrote and checksums that the rendering process
inserted.  These bugs feel predictable &mdash; almost inevitable.

(However, I have some sympathy, because there are **multiple kinds** and
**multiple layers** of escaping in shell.  Most of these cases took more than
one try to get right.  The next post will list the different meanings of `\` in
shell.)

### How Did it Go?  

I changed the [oilshell.org](oilshell.org) `Makefile` to use `cmark` instead of
`markdown.pl`, and every blog post rendered the same way!  When I looked at the
underlying HTML, there were a few differences, which were either neutral
changes or improvements:

- `<p>"Oil"</p>` &rarr; `<p>&quot;Oil&quot;</p>`.  The former might be valid
  HTML, but the latter is better.  (The former is also not valid XML.)  Being
  explicit about `&quot;` and `&amp;` makes parsing simpler.  Remember, I'm not
  using the browser to parse HTML; I'm using a Python script at build time.

- Unicode characters are represented as themselves rather than HTML entities.
  For example, `&mdash;` turned into a literal "&mdash;".  I like this change,
  but it means that the output HTML is now UTF-8 rather than ASCII.  See the
  next section for a tip about `charset` declarations.

- Insignificant whitespace in the HTML output changed.

So every blog post rendered correctly.  But when I rendered the [blog
index](..), which includes generated HTML, I ran into a difference.  A markdown
heading between HTML tags was rendered literally, rather than with an `<h3>`
tag:

    <table>
      ...
    </table>
    ### Heading
    <table>
      ...
    </table>

I fixed it by adding whitespace.  I wouldn't write markdown like this anyway;
it was arguably an artifact of generating HTML inside markdown.

Still, I'm glad that I have a git repository for the **generated** HTML as well
as the source Markdown, so I can do a `git diff` after a build and eyeball
changes.

<h3 id="http-header-tip">Tip: Check your <code>charset</code> in both HTTP and
HTML</h3>

As noted above, the HTML output now has UTF-8 characters, rather than using
ASCII representations like `&mdash;`.

This could be a problem if your web server isn't properly configured.  I
checked and my web host is not sending a `charset` in the `Content-Type`
header:

<pre>
<span style="color: blue">$ curl --head http://www.oilshell.org/</span>
HTTP/1.1 200 OK
...
Content-Type: text/html
</pre>

But I remembered that the default charset for HTTP is ISO-8859-1, **not**
UTF-8.  Luckily, my HTML boilerplate already declared UTF-8.  If you "View
Source", you'll see this line in the `<head>` of this document:

--> syntax html
<meta charset=utf-8>
<--

So I didn't need to change anything.  When there's no encoding in the HTTP
`Content-Type` header, the browser will use the HTML encoding.

In summary, if you use `markdown.pl`, I recommend switching to [CommonMark][],
but be aware of the encoding you declare in **both** HTTP and HTML.

### `cmark` Uses `re2c`, AFL, and AddressSanitizer

I haven't yet looked deeply into the [cmark][] implementation, but I see three
things I like:

1. It uses [re2c][], a tool to generate state machines in the form of `switch`
   and `goto` statements from regular expressions.

   I also used this code generator to implement the OSH lexer.  For example,
   see [osh-lex.re2c.h][], which I describe in my (unfinished) [series of posts
   on lexing][lexing].

2. It uses [American Fuzzy Lop][afl], a relatively new fuzzer that has
   uncovered many old bugs.
   
   The first time I used it, I found a null pointer dereference in [toybox][]
   `sed` in less than a second.  Roughly speaking, it relies on compiler
   technology to know what `if` statements are in the code.  This means it can
   cover more code paths with less execution time than other fuzzers.

3. It uses [AddressSanitizer][asan], a compiler option that adds dynamic checks
   for memory errors to the generated code.
   
   I used it to find [at least one bug][bwk-bug] in Brian Kernighan's [awk
   implementation][bwk], as well as several bugs in [toybox][].  It's like
   [Valgrind](http://valgrind.org/), but it has less overhead.

In summary, these are **exactly the tools** you should use if you're writing a
parser in C that needs to be safe against adversarial input.

Fundamentally, parsers have a larger state space than most code you write.
It's impossible to reason about every case, so you need tools:

- Generating state machines from regular expressions is more reliable and
  readable than writing them by hand.
- [re2c][] also has **exhaustiveness checks** at compile time.  They're similar
  to the ones that languages like OCaml and Haskell provide for pattern
  matching constructs over [algebraic data types][adt].  These checks found
  bugs in my lexer **statically** &mdash; for example, what happens when an
  entire shell script ends with a single backslash?
- As mentioned, [American Fuzzy Lop][afl] finds novel code paths very quickly.
- [AddressSanitizer][asan] complements AFL, because it automatically makes
  assertions when exploring new code paths.  Something like a 1-byte buffer
  overflow may not cause your program to crash, so fuzzing alone won't detect
  it.

Another technique I've wanted to explore, but haven't yet, is [property-based
testing](http://hypothesis.works/articles/what-is-property-based-testing/).
As far as I understand, it's related to and complementary to fuzzing.

==> md-ref1 re2c
==> md-ref1 asan
==> md-ref1 afl
==> md-ref1 bwk
==> md-ref1 toybox
==> md-ref1 adt
==> md-blog-tag lexing

[osh-lex.re2c.h]: ../../2017/12/files/osh-lex.re2c.h.html

[bwk-bug]: https://github.com/andychu/bwk/blob/master/test-results/asan.log

### Conclusion

I had a great experience with [CommonMark][], and I'm impressed by its
thoroughness.  I created [oilshell.org/site.html](//oilshell.org/site.html) to
acknowledge it and all the other projects I depend on.

What other open source projects are fixing widely-deployed technology?  Let me
know [in the comments][comments-url].

<!--
What other languages needs fixing?  

- GNU Make.  Can't be statically parsed.  There is an Android version here, but
  they switched to a different version.
- TeX - dynamic parsing too.
- Wikipedia markup?
- R language?  -->

==> md-ref1 LST

[md5-bug]: https://redditblog.com/2009/09/28/we-had-some-bugs-and-it-hurt-us/

[Markdown]: https://en.wikipedia.org/wiki/Markdown
[CommonMark]: http://commonmark.org/

[pandoc]: https://pandoc.org/

[reddit-markdown]: https://www.reddit.com/r/reddit.com/comments/6ewgt/reddit_markdown_primer_or_how_do_you_do_all_that/c03nik6/

[github-markdown]: https://help.github.com/articles/basic-writing-and-formatting-syntax/

[stackoverflow-markdown]: https://stackoverflow.com/editing-help

==> md-ref1 posix-shell-spec

[faq-posix]: ../01/28.html#limit-to-posix

[commonmark-spec]: http://spec.commonmark.org/

[bash-manual]: https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html#Conditional-Constructs

