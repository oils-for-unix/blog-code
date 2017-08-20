default: main

%.d: %.c
	@set -e; rm -f $@; \
	$(CC) -M $(CPPFLAGS) $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$


SOURCES = main.c

OBJS = $(SOURCES:.c=.o)

# NOTE: Adding -include removes error message
include $(SOURCES:.c=.d)

main: $(OBJS)
	cc -o $@ $(OBJS)

