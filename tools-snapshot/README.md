Oil Blog Tools Snapshot
=======================

A few people have asked how I make the oilshell.org site.

It uses the Unix philosophy; I describe some of the pieces at
[oilshell.org/site.html](//oilshell.org/site.html).

This directory has a snapshot of the source.  You probably won't be able to run
it, but it shows what the components are.

**Important**: this repo is unsupported.  I'm not accepting pull requests, and
I probably won't update it.  It's only to give a rough idea of how it works.

### Workflow

The workflow I use is:

    $ ./run.sh new-post  # quick and dirty Markdown template, plus a symlink
    $ ./latch.sh serve
    $ ./latch.sh notify-loop  # in another tmux pane, uses inotifywait

Then use vim to edit `blog/2018/02/commonmark.md`.

The latch server ensures that when I hit Ctrl-S, the page is rebuilt (quickly),
and the browser refreshes automatically.  I don't have even have to hit F5.  I
like having quick feedback.

Then when I'm done:

    $ make  # incremental builds help
    $ ./deploy.sh site  # incremental deploy with rsync

This repo is `~/git/oilshell/oilshell.org/`, and I have another repo
`~/git/oilshell/oilshell.org__deploy` for the generated HTML.

### External Tools

- `snip.py` and `Snip`: This is a simple shell macro system I developed.
  Sometimes you want to programmatically insert HTML into markdown, and I do
  this with a Python script that invokes shell snippets.
- The `latch` server mentioned is part of this repo:
  https://github.com/andychu/webpipe

(I wrote both of these tools prior to Oil.)

### Things I Want to Change

- `blog.py` should a real template language, e.g. JSON Template.  I use it to
  generate the "wild test" reports.  See [test/wild_report.py][] in the `oil`
  repo.
- I might want to start using some CommonMark extension points, rather than
  `snip.py`.  I'm not sure yet how these work.
- If you rename source files, the output directory is still polluted with the
  old names, and deployed.

[test/wild_report.py]: https://github.com/oilshell/oil/blob/master/test/wild_report.py

NOTE: `grep DOCTYPE */*.sh` in the `oilshell/oil` repo will also show sevearl
programmatically generated HTML pages.

### Comments

I would have been horrified by this code when I first started programming.
Superficially, it looks messy.

But I think it has a good architecture and has evolved well.  The pieces are
small and compose well.

The Knuth quote I mention in [this blog post][bespoke] about to re-editable or
"bespoke" code is relevant.

[bespoke]: http://www.oilshell.org/blog/2016/12/27.html

I've used static site generators before, and even tried to write my own.  But I
no longer believe in trying to reuse such a small amount of code.  It's better
to start with something simple, and grow it along with the content.

When you use templates, there's the implicit assumption that the content and
presentation are completely orthogonal.  With [oilshell.org][], I write the
content first, and then if I'm dissatisfied with the presentation, I write a
small amount of code to fix it.

The table of contents is a good example.  Not all blogs need it, but mine
benefits from it.  But it doesn't make sense to generalize before you know what
you need.

---

On another note, I would really like [combine shell, Awk, and Make][] rather
than have this cacophony of different langauges.  The [Oil
language][oil-language] should also be able to take the place of short Python
scripts.  (It won't be suitable for frameworks like Django.)

[shell-awk-make]: http://www.oilshell.org/blog/2016/11/13.html
[oilshell.org]: //www.oilshell.org
[oil-language]: //www.oilshell.org/blog/tags.html#oil-language

