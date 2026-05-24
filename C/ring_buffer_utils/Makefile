# Ring Buffer Utility Makefile

CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c99 -O2
LDFLAGS =

# Source files
SRCS = ring_buffer.c
TEST_SRC = test_ring_buffer.c
EXAMPLE_SRC = example.c

# Object files
OBJS = $(SRCS:.c=.o)

# Targets
TEST_BIN = test_ring_buffer
EXAMPLE_BIN = ring_buffer_example

.PHONY: all clean test example

all: test example

# Build test binary
$(TEST_BIN): $(OBJS) $(TEST_SRC)
	$(CC) $(CFLAGS) -o $@ $(TEST_SRC) $(OBJS) $(LDFLAGS)

# Build example binary
$(EXAMPLE_BIN): $(OBJS) $(EXAMPLE_SRC)
	$(CC) $(CFLAGS) -o $@ $(EXAMPLE_SRC) $(OBJS) $(LDFLAGS)

# Compile object files
%.o: %.c ring_buffer.h
	$(CC) $(CFLAGS) -c -o $@ $<

# Build and run tests
test: $(TEST_BIN)
	./$(TEST_BIN)

# Build examples
example: $(EXAMPLE_BIN)
	./$(EXAMPLE_BIN)

# Clean build artifacts
clean:
	rm -f $(OBJS) $(TEST_BIN) $(EXAMPLE_BIN)

# Memory check with valgrind (if available)
memcheck: $(TEST_BIN)
	valgrind --leak-check=full --error-exitcode=1 ./$(TEST_BIN)