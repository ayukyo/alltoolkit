# Makefile for Stack Utils
# AllToolkit - 2026-04-22

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -pedantic
DEBUG_FLAGS = -g -O0 -DDEBUG

# Targets
all: test example

# Compile test suite
test: test_stack.c stack.c stack.h
	$(CC) $(CFLAGS) -o test_stack test_stack.c stack.c

# Compile with debug symbols
debug: test_stack.c stack.c stack.h
	$(CC) $(CFLAGS) $(DEBUG_FLAGS) -o test_stack_debug test_stack.c stack.c

# Compile examples
example: example_stack.c stack.c stack.h
	$(CC) $(CFLAGS) -o example_stack example_stack.c stack.c

# Run tests
run-test: test
	./test_stack

# Run examples
run-example: example
	./example_stack

# Clean build artifacts
clean:
	rm -f test_stack test_stack_debug example_stack *.o

# Full build and test
all-test: clean all run-test

.PHONY: all test debug example run-test run-example clean all-test