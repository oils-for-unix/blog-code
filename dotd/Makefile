default: main

%.d: %.c
	@set -e; rm -f $@; cc_tmp=$@.mm; \
	$(CC) -M $(CPPFLAGS) $< > $$cc_tmp; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $$cc_tmp > $@;


SOURCES = main.c

OBJS = $(SOURCES:.c=.o)

# NOTE: Adding -include removes error message
include $(SOURCES:.c=.d)

main: $(OBJS)
	cc -o $@ $(OBJS)

