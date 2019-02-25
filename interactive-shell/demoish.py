#!/usr/bin/python
"""
demoish.py

Let's think of the interactive shell prompt roughly as a state machine.

Inputs:
  - Enter a line that finishes a command
  - Enter a line that's incomplete.
  - Hitting TAB to complete
    - which display multiple candidates or fill in a single candidate
  - Ctrl-C to cancel a COMMAND in progress.
  - Ctrl-C to cancel a COMPLETION in progress, for slow completions.
    - NOTE: if there are blocking NFS calls, completion should go in a
      thread/process?
  - EOF: Ctrl-D on an EMPTY line.
    (Ctrl-D on a non-empty line behaves just like hitting enter)
  - SIGWINCH: Terminal width change.

Actions:
  - Display completions, which depends on the terminal width.
  - Display a 1-line message showing lack of completions ('no variables that
    begin with $')
  - Execute a command
  - Clear N lines below the prompt (must happen frequently)
  - Exit the shell

State:
  - The terminal width.  Changes dynamically.
  - The prompt: PS1 or PS2.  (Or could save/restore here?)
  - The number of lines to clear next.  EraseLines() uses this.
  - The completion that is in progress.  The 'compopt' builtin affects this.
  - The number of times you have requested the same completion (to show more
    lines)

UI:
  - Explanatory message when there's no completion
  - Progress when there's a slow completion (over 200 ms)
  - Empty input "moves" the prompt down a line
  - Flag help displayed in yellow
  - Line can be bold.  Although we might want syntax highlighting for $foo
    and so forth.  "$foo" vs. '$foo' is useful.

LATER:
  - Could have a caching decorator, because we recompute candidates every time.
    For $PATH entries?
  - experiment with ordering?  You would have to disable readline sorting:

Variable: int rl_sort_completion_matches
  If an application sets this variable to 0, Readline will not sort the list of
  completions (which implies that it cannot remove any duplicate completions).
  The default value is 1, which means that Readline will sort the completions
  and, depending on the value of rl_ignore_completion_duplicates, will attempt
  to remove duplicate matches.
"""
from __future__ import print_function

import optparse
import os
import readline
import signal
import sys
import time

# Only for prompt rendering.
import getpass
import pwd
import socket

import comp_ui

log = comp_ui.log
debug_log = comp_ui.debug_log


# Prompt style
_RIGHT = '_RIGHT'
_OSH = '_OSH'


def GetHomeDir():
  """Get the user's home directory from the /etc/passwd.

  Used by $HOME initialization in osh/state.py.  Tilde expansion and readline
  initialization use mem.GetVar('HOME').
  """
  uid = os.getuid()
  try:
    e = pwd.getpwuid(uid)
  except KeyError:
    return None
  else:
    return e.pw_dir


_HOME_DIR = GetHomeDir()


class WordsAction(object):
  """Yield a fixed list of completion candidates."""
  def __init__(self, words, delay=None):
    self.words = words
    self.delay = delay

  def Matches(self, prefix):
    for w in self.words:
      if w.startswith(prefix):
        if self.delay is not None:
          time.sleep(self.delay)

        yield w


class FileSystemAction(object):
  """Complete paths from the file system.

  Directories will have a / suffix.

  Copied from core/completion.py in Oil.
  """

  def __init__(self, dirs_only=False, exec_only=False, add_slash=False):
    self.dirs_only = dirs_only
    self.exec_only = exec_only

    # This is for redirects, not for UserSpec, which should respect compopt -o
    # filenames.
    self.add_slash = add_slash  # for directories

  def Matches(self, to_complete):
    #log('fs %r', to_complete)
    i = to_complete.rfind('/')
    if i == -1:  # it looks like 'foo'
      to_list = '.'
      base = ''
    elif i == 0:  # it's an absolute path to_complete like / or /b
      to_list = '/'
      base = '/'
    else:
      to_list = to_complete[:i]
      base = to_list
      #log('to_list %r', to_list)

    try:
      names = os.listdir(to_list)
    except OSError as e:
      return  # nothing

    for name in names:
      path = os.path.join(base, name)
      if path.startswith(to_complete):
        if self.exec_only:
          # TODO: Handle exception if file gets deleted in between listing and
          # check?
          if not os.access(path, os.X_OK):
            continue

        if self.add_slash and os.path.isdir(path):
          yield path + '/'
        else:
          yield path


_FS_ACTION = FileSystemAction(add_slash=True)


class FlagsHelpAction(object):
  """Yield flags and their help.

  Return a list of TODO: This API can't be expressed in shell itself.  How do
  zsh and fish do it?
  """

  def __init__(self, flags):
    self.flags = flags  # a list of tuples

  def Matches(self, prefix):
    for flag, desc in self.flags:
      if flag.startswith(prefix):
        yield flag, desc


class FlagsAndFileSystemAction(object):
  """Complete flags if the word starts with '-', otherwise files.

  This is basically what _longopt in bash-completion does.
  """
  def __init__(self, flags_action, fs_action):
    self.flags_action = flags_action
    self.fs_action = fs_action

  def Matches(self, prefix):
    if prefix.startswith('-'):
      for m in self.flags_action.Matches(prefix):
        yield m
    else:
      for m in self.fs_action.Matches(prefix):
        yield m


def JoinLinesOfCommand(pending_lines):
  last_line_pos = 0
  parts = []
  for line in pending_lines:
    if line.endswith('\\\n'):
      line = line[:-2]
      last_line_pos += len(line)
    parts.append(line)
  cmd = ''.join(parts)
  return cmd, last_line_pos


def MakeCompletionRequest(lines):
  """Returns a 4-tuple or an error code.

  Returns:
    first: The first word, or None if we're completing the first word itself
    to_complete: word to complete
    prefix: string
    prefix_pos: integer

  Cases we CAN complete:

    echo foo \
    f<TAB>

    echo foo \
    bar f<TAB>

  Cases we CAN'T complete:
    ec\
    h<TAB>    # complete 'o' ?

    echo f\
    o<TAB>    # complete 'o' ?
  """
  #log('pending_lines %s', pending_lines)

  # first word can't be split over multiple lines
  if len(lines) > 1 and ' ' not in lines[0]:
    return -1

  partial_cmd, last_line_pos = JoinLinesOfCommand(lines)

  # the first word if we're completing an arg, or None if we're completing the
  # first word itself
  first = None

  cmd_last_space_pos = partial_cmd.rfind(' ')
  if cmd_last_space_pos == -1:  # FIRST WORD state, no prefix
    prefix_pos = 0
    to_complete = partial_cmd
    prefix = ''

  else:  # Completing an argument, may be on any line
    # Find the first word with the left-most space.  (Not the right-most space
    # above).

    j = partial_cmd.find(' ')
    assert j != -1
    first = partial_cmd[:j]

    # The space has to be on the current line, or be the last char on the
    # previous line before the line continuation.  Otherwise we can't complete
    # anything.
    if cmd_last_space_pos < last_line_pos-1:
      return -2

    last_line = lines[-1]
    line_space_pos = last_line.rfind(' ')
    if line_space_pos == -1:  # space is on previous line
      prefix_pos = 0  # complete all of this line
    else:
      prefix_pos = line_space_pos + 1

    #log('space_pos = %d, last_line_pos = %d', line_space_pos, last_line_pos)

    to_complete = last_line[prefix_pos:]
    prefix = last_line[:prefix_pos]

  #log('X partial_cmd %r', partial_cmd, file=DEBUG_F)
  #log('X to_complete %r', to_complete, file=DEBUG_F)

  unquoted = ShellUnquote(to_complete)
  return first, unquoted, prefix, prefix_pos


def ShellUnquote(s):
  # This is an approximation.  In OSH we'll use the
  # CompletionWordEvaluator.

  result = []
  for ch in s:
    if ch != '\\':
      result.append(ch)
  return ''.join(result)


def ShellQuote(s):
  # TODO: Use regex replace.
  # & ; ( also need replacing.  And { in case you have a file
  # {foo,bar}
  # And ! for history.

  return s.replace(
      ' ', '\\ ').replace(
      '$', '\\$').replace(
      ';', '\\;').replace(
      '|', '\\|')


class RootCompleter(object):
  """Dispatch to multiple completers."""

  def __init__(self, reader, display, comp_lookup, comp_state):
    """
    Args:
      reader: for completing the entire command, not just one line
      comp_lookup: Dispatch to completion logic for different commands
      comp_state: fields are added here for Display
    """
    self.reader = reader
    self.display = display
    self.comp_lookup = comp_lookup
    self.comp_state = comp_state

  def Matches(self, comp):
    line = comp['line']
    self.comp_state['ORIG'] = line

    #log('lines %s', self.reader.pending_lines, file=DEBUG_F)
    lines = list(self.reader.pending_lines)
    lines.append(line)

    result = MakeCompletionRequest(lines)
    if result == -1:
      self.display.PrintOptional("(can't complete first word spanning lines)")
      return
    if result == -2:
      self.display.PrintOptional("(can't complete last word spanning lines)")
      return

    # We have to add on prefix before sending it completer.  And then
    first, to_complete, prefix, prefix_pos = result

    # For the Display callback to look at
    self.comp_state['prefix_pos'] = prefix_pos

    # Reset this at the beginning of each completion.
    # Is there any way to avoid creating a duplicate dictionary each time?
    # I think every completer could have an optional PAYLOAD.
    # Yes that is better.
    # And maybe you can yield the original 'c' too, without prefix and ' '.
    self.comp_state['DESC'] = {}

    if first:
      completer = self.comp_lookup.get(first, _FS_ACTION)
    else:
      completer = self.comp_lookup['__first']

    #log('to_complete: %r', to_complete, file=DEBUG_F)

    i = 0
    start_time = time.time()
    for match in completer.Matches(to_complete):
      if isinstance(match, tuple):
        flag, desc = match  # hack
        if flag.endswith('='):  # Hack for --color=auto
          rl_match = flag
        else:
          rl_match = flag + ' '
        self.comp_state['DESC'][rl_match] = desc  # save it for later
      else:
        match = ShellQuote(match)
        if match.endswith('/'):  # Hack for directories
          rl_match = match
        else:
          rl_match = match + ' '

      yield prefix + rl_match
      # TODO: avoid calling time() so much?
      elapsed_ms = (time.time() - start_time) * 1000

      # NOTES:
      # - Ctrl-C works here!  You only get the first 5 candidates.
      # - These progress messages will not help if the file system hangs!  We
      #   might want to run "adversarial completions" in a separate process?
      i += 1
      if elapsed_ms > 200:
        plural = '' if i == 1 else 'es'
        self.display.PrintOptional(
            '... %d match%s for %r in %d ms (Ctrl-C to cancel)', i,
            plural, line, elapsed_ms)

    if i == 0:
      self.display.PrintRequired('(no matches for %r)', line)


class CompletionCallback(object):
  """Registered with the readline library and called for completions."""

  def __init__(self, root_comp):
    self.root_comp = root_comp
    self.iter = None

  def Call(self, word_prefix, state):
    """Generate completions."""
    if state == 0:  # initial completion
      orig_line = readline.get_line_buffer()
      #begin = readline.get_begidx()
      end = readline.get_endidx()

      comp = {'line': orig_line[:end]}
      #debug_log('line %r', orig_line)
      #debug_log('begidx %d', begin)
      #debug_log('endidx %d', end)

      self.iter = self.root_comp.Matches(comp)

    try:
      c = self.iter.next()
    except StopIteration:
      c = None
    return c

  def __call__(self, word_prefix, state):
    try:
      return self.Call(word_prefix, state)
    except Exception as e:
      # Readline swallows exceptions!
      print(e)
      raise


def DoNothing(unused1, unused2):
  pass


class PromptEvaluator(object):
  """Evaluate the prompt and give it a certain style."""

  def __init__(self, style):
    """
    Args:
      style: _RIGHT, _BOLD, _UNDERLINE, _REVERSE or _OSH
    """
    self.style = style

  def Eval(self, template):
    p = template
    p = p.replace('\u', getpass.getuser())
    p = p.replace('\h', socket.gethostname())
    cwd = os.getcwd().replace(_HOME_DIR, '~')  # Hack
    p = p.replace('\w', cwd)
    prompt_len = len(p)

    right_prompt_str = None

    if self.style == _RIGHT:
      right_prompt_str = p
      p2 = comp_ui.PROMPT_BOLD + ': ' + comp_ui.PROMPT_RESET
      prompt_len = 2

    elif 0:
    #elif self.style == _BOLD:  # Make it bold and add '$ '
      p2 = comp_ui.PROMPT_BOLD + p + '$ ' + comp_ui.PROMPT_RESET
      prompt_len += 2

    elif 0:
    #elif self.style == _UNDERLINE:
      # Don't underline the space
      p2 = comp_ui.PROMPT_UNDERLINE + p + comp_ui.PROMPT_RESET + ' '
      prompt_len += 1

    elif 0:
    #elif self.style == _REVERSE:
      p2 = comp_ui.PROMPT_REVERSE + ' ' + p + ' ' + comp_ui.PROMPT_RESET + ' '
      prompt_len += 3

    elif self.style == _OSH:
      p2 = p + '$ '  # emulate bash style
      prompt_len += 2

    else:
      raise AssertionError

    return p2, prompt_len, right_prompt_str


class InteractiveLineReader(object):
  """Simplified version of OSH prompt.

  Holds PS1 / PS2 state.
  """
  def __init__(self, ps1, ps2, prompt_eval, display, bold_line=False,
               erase_empty=0):
    self.ps1 = ps1
    self.ps2 = ps2
    self.prompt_eval = prompt_eval
    self.display = display
    self.bold_line = bold_line
    self.erase_empty = erase_empty

    self.prompt_str = ''
    self.right_prompt = ''

    self.pending_lines = []  # for completion to use
    self.Reset()  # initialize self.prompt_str

    # https://stackoverflow.com/questions/22916783/reset-python-sigint-to-default-signal-handler
    self.orig_handler = signal.getsignal(signal.SIGINT)
    self.last_prompt_len = 0
    #log('%s', self.orig_handler)

  def GetLine(self):
    signal.signal(signal.SIGINT, self.orig_handler)  # raise KeyboardInterrupt

    p = self.prompt_str
    if self.bold_line:
      p += comp_ui.PROMPT_BOLD

    if self.right_prompt_str:  # only for PS1
      self.display.ShowPromptOnRight(self.right_prompt_str)

    try:
      line = raw_input(p) + '\n'  # newline required
    except KeyboardInterrupt:
      print('^C')
      line = -1
    except EOFError:
      print('^D')  # bash prints 'exit'; mksh prints ^D.
      line = -2
    else:
      self.pending_lines.append(line)
    finally:
      # Ignore it usually, so we don't get KeyboardInterrupt in weird places.
      # NOTE: This can't be SIG_IGN, because that affects the child process.
      signal.signal(signal.SIGINT, DoNothing)

    # Nice trick to remove repeated prompts.
    if line == '\n':
      if self.erase_empty == 0:
        pass
      elif self.erase_empty == 1:
        # Go up one line and erase the whole line
        sys.stdout.write('\x1b[1A\x1b[2K\n')
        sys.stdout.flush()
      elif self.erase_empty == 2:
        sys.stdout.write('\x1b[1A\x1b[2K')
        sys.stdout.write('\x1b[1A\x1b[2K')
        sys.stdout.write('\n')  # go down one line
        sys.stdout.flush()
      else:
        raise AssertionError(self.erase_empty)

    self.prompt_str = self.ps2
    self.right_prompt_str = None

    self.display.SetPromptLength(len(self.ps2))
    return line

  def Reset(self):
    self.prompt_str, prompt_len, self.right_prompt_str = (
        self.prompt_eval.Eval(self.ps1))
    self.display.SetPromptLength(prompt_len)
    del self.pending_lines[:]

  def CurrentRenderedPrompt(self):
    """For BasicDisplay to reprint the prompt."""
    return self.prompt_str


def MainLoop(reader, display):
  while True:
    # TODO: Catch KeyboardInterrupt and EOFError here.
    line = reader.GetLine()

    # Erase lines before execution, displaying PS2, or exit!
    display.EraseLines()

    if line == -1:  # Ctrl-C
      display.Reset()
      reader.Reset()
      continue

    #log('got %r', line)
    if line == -2:  # EOF
      break

    if line.endswith('\\\n'):
      continue

    if line.startswith('cd '):
      try:
        dest = line.strip().split(None, 1)[1]
      except IndexError:
        log('cd: dir required')
      else:
        try:
          os.chdir(dest)
        except OSError as e:
          log('cd: %s', e)
      display.Reset()
      reader.Reset()
      continue

    # Take multiple lines from the reader, simulating the OSH parser.
    cmd, _ = JoinLinesOfCommand(reader.pending_lines)

    os.system(cmd)

    display.Reset()
    reader.Reset()


_MORE_COMMANDS = [
    'cd', 'echo', 'sleep', 'clear', 'slowc', 'many', 'toomany'
]

ECHO_WORDS = [
    'zz', 'foo', 'bar', 'baz', 'spam', 'eggs', 'python', 'perl', 'pearl',
    # To simulate filenames with spaces
    'two words', 'three words here',
]


def LoadFlags(path):
  flags = []
  with open(path) as f:
    for line in f:
      try:
        flag, desc = line.split(None, 1)
        desc = desc.strip()
      except ValueError:
        #log('Error: %r', line)
        #raise
        flag = line.strip()
        desc = None

      # TODO: do something with the description
      flags.append((flag, desc))
  return flags


_PS1 = '[demoish] \u@\h \w'


def main(argv):
  p = optparse.OptionParser(__doc__, version='snip 0.1')
  p.add_option(
      '--flag-dir', dest='flag_dir', default=None,
      help='Directory with flags definitions')
  p.add_option(
      '--style', dest='style', default='osh',
      help='Style of prompt')

  opts, _ = p.parse_args(argv[1:])

  _, term_width = comp_ui.GetTerminalSize()
  fmt = '%' + str(term_width) + 's'

  #msg = "[Oil 0.6.pre11] Type 'help' or visit https://oilshell.org/help/ "
  msg = "Type 'help' or visit https://oilshell.org/ for help"
  print(fmt % msg)
  print('')

  # Used to store the original line, flag descriptions, etc.
  comp_state = {}

  if opts.style == 'bare':
    display = comp_ui.BasicDisplay(comp_state)
    prompt = PromptEvaluator(_OSH)
    reader = InteractiveLineReader(_PS1, '> ', prompt, display,
                                   bold_line=False)
    display.SetReader(reader)  # needed to re-print prompt

  elif opts.style == 'osh':
    display = comp_ui.NiceDisplay(comp_state, bold_line=True)
    prompt = PromptEvaluator(_OSH)
    reader = InteractiveLineReader(_PS1, '> ', prompt, display,
                                   bold_line=True, erase_empty=1)
  elif opts.style == 'oil':
    display = comp_ui.NiceDisplay(comp_state, bold_line=True)
    # Oil has reverse video on the right.  It's also bold, and may be syntax
    # highlighted later.
    prompt = PromptEvaluator(_RIGHT)
    reader = InteractiveLineReader(_PS1, '| ', prompt, display,
                                   bold_line=True, erase_empty=2)

  else:
    raise RuntimeError('Invalid style %r' % opts.style)

  # Register a callback to receive terminal width changes.
  signal.signal(signal.SIGWINCH, lambda x, y: display.OnWindowChange())

  comp_lookup = {
      'echo': WordsAction(ECHO_WORDS),
      'slowc': WordsAction([str(i) for i in xrange(20)], delay=0.1),
      'many': WordsAction(['--flag%d' % i for i in xrange(50)]),
      'toomany': WordsAction(['--too%d' % i for i in xrange(1000)]),
  }

  commands = []
  if opts.flag_dir:
    for cmd in os.listdir(opts.flag_dir):
      path = os.path.join(opts.flag_dir, cmd)
      flags = LoadFlags(path)
      fl = FlagsHelpAction(flags)
      comp_lookup[cmd] = FlagsAndFileSystemAction(fl, _FS_ACTION)
      commands.append(cmd)

  comp_lookup['__first'] = WordsAction(commands + _MORE_COMMANDS)

  # Register a callback to generate completion candidates.
  root_comp = RootCompleter(reader, display, comp_lookup, comp_state)
  readline.set_completer(CompletionCallback(root_comp))

  # We want to parse the line ourselves, rather than use readline's naive
  # delimiter-based tokenization.
  readline.set_completer_delims('')

  # Register a callback to display completions.
  # NOTE: If we don't register a hook, readline will print the ENTIRE command
  # line completed, not just the word.

  # NOTE: Is this style hard to compile?  Maybe have to expand the args
  # literally.
  readline.set_completion_display_matches_hook(
      lambda *args: display.PrintCandidates(*args)
  )

  readline.parse_and_bind('tab: complete')

  MainLoop(reader, display)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
