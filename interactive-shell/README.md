demoish: An interactive shell UI.
--------------------------------

Features:

- Sensitive to the terminal width.  Completions fill horizontally like in
  readline, and we update the width when we receive the `SIGWINCH`
  signal.
- Prints the first N candidates of a long list without an annoying y/n
  prompt.  You can hit TAB again to see more.
- Displays descriptions of flags
- Displays progress for slow completions
- Ctrl-C cancels a command
- Conserves vertical screen space.  Executing a command or hitting Ctrl-C
  removes the vertical space used by completion candidates.
- Respects PS2 when the line ends with `\`.

See the comments at the top of `demoish.py` for more technical details.
