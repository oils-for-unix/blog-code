# Build the website.
#
# Hints:
# $<  first input
# $@  output

# http://blog.jgc.org/2015/04/the-one-line-you-should-add-to-every.html
print-%:
	@echo $*=$($*)

# NOTE: Because of the ??.md wildcard, (A) rebuilds a file but (B) doesn't.
#
# (A) 'touch blog/2016/10/XX.md && make'
# (B) 'touch blog/2016/10/XXX.md && make'

BLOG_SOURCES = $(shell find blog -name '??.md' -a -printf 'blog/%P\n')

META = $(addprefix _tmp/,$(BLOG_SOURCES:.md=_meta.json))

# crossref, etc.
SOURCES = $(wildcard *.md) $(wildcard blog/*.md) $(BLOG_SOURCES)

HTML = $(addprefix _site/,$(SOURCES:.md=.html))

all: $(HTML) _site/css/bundle.css _site/js/bundle.js _site/.htaccess

_site/css/bundle.css: css/base.css css/code.css css/toc.css
	cat $^ > $@

_site/js/bundle.js: js/toc.js
	cat $^ > $@

_site/.htaccess: wwz.htaccess deny.htaccess
	cat $^ > $@

# NOTE: two wildcards doesn't work: blog/2016/%/%.md.  But the wildcards work
# across directories.  The $(HTML) list is sufficient.

# Why does Make delete intermediate files?
# https://www.gnu.org/software/make/manual/html_node/Chained-Rules.html
# http://stackoverflow.com/questions/9638275/undo-intermediate-files-deletion-how-to
# http://stackoverflow.com/questions/3046117/gnu-makefile-multiple-outputs-from-single-rule-preventing-intermediate-files

# This is explicit:
#.PRECIOUS: _tmp/%_meta.json _tmp/%_body.html _tmp/%_content.md

# But this is easier:
.SECONDARY:

# Disable internal rules database
.SUFFIXES:

# Works for cross ref and index in addition to blog/????/??/??.md.  See 'make
# -d' output.
#
# $(patsubst %_meta.json,%,$@)
# #
# Perform replacement on the third output arg: _tmp/2016/10/10_meta.json 
#
# with pattern (.*)_meta.json and replacement \0 (in regex syntax)
#
# NOTE about combining the two rules:
# "The file name of the target of the rule. If the target is an archive member,
# then ‘$@’ is the name of the archive file. In a pattern rule that has
# multiple targets (see Introduction to Pattern Rules), ‘$@’ is the name of
# whichever target caused the rule’s recipe to be run."

_tmp/%_meta.json : %.md
	./blog.py split-entry $< $(patsubst %_meta.json,%,$@)
_tmp/%_content.md : %.md
	./blog.py split-entry $< $(patsubst %_content.md,%,$@)
_tmp/%_body.html: _tmp/%_content.md
	./build.sh snip-and-markdown $< $@
_site/%.html: _tmp/%_meta.json _tmp/%_body.html
	./blog.py header-footer $^ > $@

# For blog/index.html.  It has a blog/index.md "template", along with
# programatically generated content.
_tmp/blog/index_LATEST.html _tmp/blog/index_ALL.html: $(META)
	./blog.py index _tmp/blog/index_LATEST.html _tmp/blog/index_ALL.html $^
_tmp/blog/tag_index.html: $(META)
	./blog.py tag-index $^ > $@
_tmp/blog/index_body.html: _tmp/blog/index_content.md \
                           _tmp/blog/index_LATEST.html \
                           _tmp/blog/index_ALL.html \
                           _tmp/blog/tag_index.html
	./build.sh snip-and-markdown $< $@

_tmp/blog/posts_by_tag.html: $(META)
	./blog.py posts-by-tag $^ > $@
_tmp/blog/tags_body.html: _tmp/blog/tags_content.md \
                          _tmp/blog/posts_by_tag.html
	./build.sh snip-and-markdown $< $@
