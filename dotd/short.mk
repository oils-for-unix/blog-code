default: main

CFLAGS = -MD

SOURCES = main.c

OBJS = $(SOURCES:.c=.o)

# NOTE: Adding -include removes error message
-include $(SOURCES:.c=.d)

main: $(OBJS)
	cc -o $@ $(OBJS)

