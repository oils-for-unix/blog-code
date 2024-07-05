CC=gcc
CFLAGS=-Wall

all: example

include syscall-reporter.mk

example: example.o syscall-reporter.o

.PHONY: clean
clean:
	rm -f example example.o
