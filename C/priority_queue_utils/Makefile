# Makefile for Priority Queue Utils
# AllToolkit - 2026-04-23

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -pedantic
DEBUG_FLAGS = -g -O0 -DDEBUG

# Targets
all: test example

# Compile test suite
test: test_priority_queue.c priority_queue.c priority_queue.h
	$(CC) $(CFLAGS) -o test_priority_queue test_priority_queue.c priority_queue.c

# Compile with debug symbols
debug: test_priority_queue.c priority_queue.c priority_queue.h
	$(CC) $(CFLAGS) $(DEBUG_FLAGS) -o test_priority_queue_debug test_priority_queue.c priority_queue.c

# Compile examples
example: example_priority_queue.c priority_queue.c priority_queue.h
	$(CC) $(CFLAGS) -o example_priority_queue example_priority_queue.c priority_queue.c

# Run tests
run-test: test
	./test_priority_queue

# Run examples
run-example: example
	./example_priority_queue

# Clean build artifacts
clean:
	rm -f test_priority_queue test_priority_queue_debug example_priority_queue *.o

# Full build and test
all-test: clean all run-test

.PHONY: all test debug example run-test run-example clean all-test