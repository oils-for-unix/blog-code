#!/usr/bin/python
from __future__ import print_function
"""
blog.py

Generate web pages, blog posts, and indices from metadata / rendered HTML.
"""

import collections
import json
import re
import sys


def log(msg, *args):
  if args:
    msg = msg % args
  print('[blog.py] ' + msg, file=sys.stderr)


DEFAULT_META = {
   'css_file': 'bundle.css',
   'js_file': 'bundle.js',
   'body_css_class': 'skinny',
   'home_url': '/',
}


# Mixing HTML in markdown is sensitive to whitespace, need trailing \n on
# </table>.
TABLE_BEGIN = '<table>\n'
TABLE_END = '</table>\n'

# TODO: Proper escaping
INDEX_ROW = """\
<tr>
  <td class="date"> %(year)s-%(month)02d-%(day)02d </td>
  <td> <a href="%(year)s/%(month)02d/%(day)02d.html">%(title)s</a> </td>
</tr>
"""

SPACE_ROW = """\
<tr>
  <td class="date"> &nbsp; </td>
  <td> &nbsp; </td>
</tr>
"""

# TODO: Escape everything

HEADER = """\
<!DOCTYPE html>
<html lang=en>

<head>
  <meta charset=utf-8>

  <title>%(title)s</title>

  <!-- NOTE: has to be /css unless the docs know their depth -->
  <link rel="stylesheet" type="text/css" href="/css/%(css_file)s" />
  <script type="text/javascript" src="/js/%(js_file)s"></script>

  <!-- INSERT LATCH JS -->
</head>

<body onload="" class="%(body_css_class)s">
  <!-- INSERT LATCH HTML -->
"""

# TODO: Should use JSON Template for these variants.
PAGE_TITLE = """\
<h1>%(title)s</h1>
"""

POST_TITLE = """\
<h2>%(title)s</h2>
<div class="date">
  %(year)s-%(month)02d-%(day)02d
</div>
"""

UPDATED_POST_TITLE = """\
<h2>%(title)s</h2>
<div> 
  <span class="date">
    %(year)s-%(month)02d-%(day)02d
  </span>
  <span style="float: right; font-size: medium;">
  (Last updated %(updated_year)s-%(updated_month)02d-%(updated_day)02d)
  </span>
</div>
"""

# Go to https://analytics.google.com/
# To see the tracking code.

GOOGLE_ANALYTICS = """\
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-91166618-1', 'auto');
  ga('send', 'pageview');
</script>
"""

FOOTER = GOOGLE_ANALYTICS + """\
</body>
</html>
"""

def MaybeHeader(meta, out_f):
  if meta.get('home_url') == '-':
    return

  out_f.write('<p style="text-align: right">')

  if _IsBlog(meta):
    out_f.write('<a href="/blog/">blog</a> | ' % meta)

  # NOTE: home_url is always /, or - to disable.  For example, index.md
  # explicit disables home_url.
  out_f.write('<a href="/">oilshell.org</a>' % meta)
  #out_f.write('<a href="%(home_url)s">oilshell.org</a>' % meta)

  out_f.write('</p>\n')


def WritePostFooter(meta, f):
  comments_url = meta.get('comments_url', '')
  if comments_url:
    f.write("""
[comments-url]: %s

""" % comments_url)

  f.write("""
<div id="post-footer">
<ul>
""" % meta)

  if comments_url:
    f.write('<li><a href="%(comments_url)s">Discuss This Post on Reddit</a>' % meta)

  f.write("""
  <li>Get notified about new posts via
  <a href="https://twitter.com/oilshellblog">@oilshellblog on Twitter</a>
""")

  # Also write tags here
  tags = _GetTags(meta)
  if tags:
    f.write('<li>Read Posts Tagged: ')
    for tag in tags:
      f.write('&nbsp;&nbsp;<span class="blog-tag"><a href="/blog/tags.html?tag=%s#%s">%s</a></span> '
          % (tag, tag, tag))
    f.write('</li>')

  f.write("""
  <li><a href="../..">Back to the Blog Index</a>
</ul>
</div>
""")


# TODO:
# - How does meta['title'] go in the end HTML?
# - Import html.sh to html.py.  Doesn't have to be markdown.

def ByDate(m):
  return (m['year'], m['month'], m['day'])


def CaseInsensitive(s):
  return s.lower()


def WriteAllEntries(meta_list, all_f):
  by_month = collections.defaultdict(list)
  for meta in meta_list:
    year = meta['year']
    month = meta['month']
    by_month[year, month].append(meta)

  css_flag = False

  all_f.write('<table id="all-posts">')
  for year, month in sorted(by_month):
    month_meta = by_month[year, month]

    css_class = 'alt-month' if css_flag else ''
    all_f.write('<tbody class="%s">' % css_class)
    css_flag = not css_flag

    n = len(month_meta)
    for i, meta in enumerate(month_meta):
      all_f.write(INDEX_ROW % meta)
      if i % 5 == 4 and i != n - 1:  # don't do the last one
        all_f.write(SPACE_ROW)

    all_f.write(SPACE_ROW)
    all_f.write('</tbody>')

  all_f.write('</table>')


def _ReadMetaList(meta_paths):
  meta_list = []
  for i, path in enumerate(meta_paths):
    with open(path) as f:
      meta = json.load(f)
      # TODO: How to space it out?
      meta_list.append(meta)
  return meta_list


def _IsBlog(meta):
  return 'year' in meta


def _IsPublished(meta):
  return meta.get('published') != 'no'


def MakeBlogIndex(meta_list, latest_f, all_f):
  # Filter out posts that don't have a date.
  # Allow disabling with "published: no".
  meta_list = [m for m in meta_list if _IsBlog(m) and _IsPublished(m)]
  meta_list.sort(key=ByDate)

  # Write LATEST
  latest_f.write(TABLE_BEGIN)
  for meta in reversed(meta_list[-5:]):
    latest_f.write(INDEX_ROW % meta)
  latest_f.write(TABLE_END)

  # Write ALL
  WriteAllEntries(meta_list, all_f)

  log('Wrote index of %d blog entries', len(meta_list))


def HeaderFooter(in_f, meta, out_f):
  out_f.write(HEADER % meta)
  MaybeHeader(meta, out_f)

  contents = in_f.read()
  out_f.write(contents)

  out_f.write(FOOTER)


TITLE_RE = re.compile(
    r'(\d\d\d\d) / (\d\d) / (\d\d): [ ]* (.*)', re.VERBOSE)

DATE_RE = re.compile(
    r'(\d\d\d\d) / (\d\d) / (\d\d)', re.VERBOSE)

META_RE = re.compile(
    r'(\S+): [ ]* (.*)', re.VERBOSE)


def SplitDocument(entry_f, meta_f, content_f):
  """Split a document into metadata JSON and content Markdown.

  Used for blog posts and index.md / cross-ref.md.
  """
  first_line = entry_f.readline().strip()

  # TODO: if first_line is ---, then read metadata in key: value format.
  has_date = False
  has_updated = False

  if first_line == '---':
    meta = {}
    while True:
      line = entry_f.readline().strip()
      if line == '---':
        break
      m = META_RE.match(line)
      if not m:
        raise RuntimeError('Invalid metadata line %r' % line)
      name, value = m.groups()

      if name == 'date':
        m2 = DATE_RE.match(value)
        if not m2:
          raise RuntimeError('Invalid date %r' % value)
        year, month, day = m2.groups()
        meta['year'] = int(year)
        meta['month'] = int(month)
        meta['day'] = int(day)
        has_date = True

      elif name == 'updated_date':
        m2 = DATE_RE.match(value)
        if not m2:
          raise RuntimeError('Invalid date %r' % value)
        year, month, day = m2.groups()
        meta['updated_year'] = int(year)
        meta['updated_month'] = int(month)
        meta['updated_day'] = int(day)
        has_updated = True

      else:
        meta[name] = value

  else:
    raise AssertionError('Every blog post should now begin with ---')

    unused_dashes = entry_f.readline()

    m = TITLE_RE.match(first_line)
    if m:
      year, month, day, title = m.groups()

      #print(year, month, day, title)
      meta = {
          'title': title,
          'year': int(year),
          'month': int(month),
          'day': int(day),
          }
      has_date = True
    else:
      meta = {'title': first_line}

  json.dump(meta, meta_f)

  # Read the rest of the file
  contents = entry_f.read()

  if has_updated and has_date:
    content_f.write(UPDATED_POST_TITLE % meta)
  elif has_date:
    # Write blog post title and year/month/day
    content_f.write(POST_TITLE % meta)
  else:
    # Just write the title of the page (e.g. cross ref)
    content_f.write(PAGE_TITLE % meta)

  content_f.write(contents)

  # TODO: Write footer after appendix somehow?
  if _IsBlog(meta):
    WritePostFooter(meta, content_f)


def _GetTags(m):
  tags_str = m.get('tags')
  return tags_str.split() if tags_str else []


def ReadAndCollectTags(meta_list):
  """Use this for both tag-index and posts-by-tag. """
  unique_tags = set()
  posts_by_tag = collections.defaultdict(list)

  for m in meta_list:
    if not _IsPublished(m):
      continue

    #print(m, file=sys.stderr)
    tags = _GetTags(m)

    for t in tags:
      unique_tags.add(t)
      posts_by_tag[t].append(m)

  # Sort in reverse chronological order
  for tag, posts in posts_by_tag.iteritems():
    posts.sort(key=ByDate)

  return posts_by_tag


def TagIndex(posts_by_tag, f):
  f.write('<p>')
  for tag in sorted(posts_by_tag, key=CaseInsensitive):
    f.write('<span class="blog-tag"><a href="tags.html?tag=%s#%s">%s</a> (%d)&nbsp;&nbsp;&nbsp;</span> ' % (
      tag, tag, tag, len(posts_by_tag[tag])))
  f.write('</p>')


def PostsByTag(posts_by_tag, f):
  for tag in sorted(posts_by_tag, key=CaseInsensitive):
    f.write('<a name="%s"></a>' % tag)
    f.write('<p style="color: blue;" class="blog-tag">#%s</p>' % tag)
    f.write(TABLE_BEGIN)

    meta_list = posts_by_tag[tag]

    for meta in meta_list:
      # A list of posts
      f.write(INDEX_ROW % meta)

    f.write(TABLE_END)


def main(argv):
  # NOTE: We can't do split-entry and header-footer in the same step, because
  # the snip and markdown tools have to be invoked in between.  Markdown would
  # ignore stuff in <body></body>.
  try:
    action = argv[1]
  except IndexError:
    raise RuntimeError('Usage: ./blog.py ACTION [ARG]...')

  if action == 'index':
    latest_out = argv[2]
    all_out = argv[3]
    meta_paths = argv[4:]
    meta_list = _ReadMetaList(meta_paths)
    with open(latest_out, 'w') as latest_f, open(all_out, 'w') as all_f:
      MakeBlogIndex(meta_list, latest_f, all_f)

  elif action == 'split-entry':
    entry_path = argv[2]  # e.g. blog/2016/11/01.md
    out_prefix = argv[3]  # e.g _site/blog/2016/11/01

    meta_path = out_prefix + '_meta.json'
    content_path = out_prefix + '_content.md'

    with \
        open(entry_path) as entry_f, \
        open(meta_path, 'w') as meta_f, \
        open(content_path, 'w') as content_f:
      SplitDocument(entry_f, meta_f, content_f)

  elif action == 'header-footer':
    # Used for both blog posts and /index.html, etc.

    meta_path = argv[2]
    in_path = argv[3]

    meta = dict(DEFAULT_META)
    with open(meta_path) as f:
      doc_meta = json.load(f)

    meta.update(doc_meta)  # override

    with open(in_path) as in_f:
      HeaderFooter(in_f, meta, sys.stdout)

  elif action == 'tag-index':
    # For the /blog/ page, list all unique tags.
    meta_paths = argv[2:]
    meta_list = _ReadMetaList(meta_paths)
    posts_by_tag = ReadAndCollectTags(meta_list)
    TagIndex(posts_by_tag, sys.stdout)

  elif action == 'posts-by-tag':
    # Output a single HTML page of posts sorted by tag
    meta_paths = argv[2:]
    meta_list = _ReadMetaList(meta_paths)
    posts_by_tag = ReadAndCollectTags(meta_list)
    PostsByTag(posts_by_tag, sys.stdout)
    #print('TAGS %s ' % (meta_paths,))

  else:
    raise RuntimeError('Invalid action %r' % action)


# TODO: This should be moved into Snip
#
# It transforms the piece on stdin.  And it can also have a side effect of
# writing a file.
#
# --> metadata 
# title: Status Update
# date: 2016/10/11
# tags: foo-bar   bar-baz
# style: post
# <--
#
# Possibly even "snip" should be moved to oil/pulp.  It's like <?php -- mixing
# code with data.  Well sorta -- snip is just dialects of data.  Not really
# code.


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print(e, file=sys.stderr)
    sys.exit(1)
