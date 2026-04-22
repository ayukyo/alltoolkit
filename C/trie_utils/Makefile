# Makefile for Trie utils
# AllToolkit - C Trie Implementation

CC = gcc
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c11 -O2
TEST_FLAGS = -Wall -Wextra -std=c11 -g

# Source files
SRCS = trie.c
HDRS = trie.h
TEST_SRC = trie_test.c

# Example sources
EXAMPLE_SRC = basic_usage.c autocomplete.c spell_checker.c word_frequency.c iterator_demo.c
EXAMPLE_DIR = examples

# Output directories
BUILD_DIR = build
TEST_DIR = test_build

# Targets
.PHONY: all test clean examples run_examples

all: $(BUILD_DIR)/trie.o
	@echo "Build complete!"

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/trie.o: trie.c trie.h $(BUILD_DIR)
	$(CC) $(CFLAGS) -c trie.c -o $(BUILD_DIR)/trie.o

# Static library (optional)
$(BUILD_DIR)/trie.a: $(BUILD_DIR)/trie.o
	ar rcs $(BUILD_DIR)/trie.a $(BUILD_DIR)/trie.o

# Tests
test: $(TEST_DIR)/trie_test
	@echo "Running tests..."
	$(TEST_DIR)/trie_test

$(TEST_DIR):
	mkdir -p $(TEST_DIR)

$(TEST_DIR)/trie_test: $(TEST_SRC) trie.c trie.h $(TEST_DIR)
	$(CC) $(TEST_FLAGS) $(TEST_SRC) trie.c -o $(TEST_DIR)/trie_test

# Examples
examples: $(foreach ex, $(EXAMPLE_SRC), $(BUILD_DIR)/$(ex:.c=))

$(BUILD_DIR)/%: $(EXAMPLE_DIR)/%.c trie.c trie.h $(BUILD_DIR)
	$(CC) $(CFLAGS) -I. $(EXAMPLE_DIR)/$*.c trie.c -o $(BUILD_DIR)/$*

run_examples: examples
	@echo ""
	@echo "=== Running Basic Usage Example ==="
	$(BUILD_DIR)/basic_usage
	@echo ""
	@echo "=== Running Autocomplete Example ==="
	$(BUILD_DIR)/autocomplete
	@echo ""
	@echo "=== Running Iterator Demo ==="
	$(BUILD_DIR)/iterator_demo

# Clean
clean:
	rm -rf $(BUILD_DIR) $(TEST_DIR)
	@echo "Clean complete!"

# Install (copy to a location)
install: $(BUILD_DIR)/trie.a
	@echo "To use in your project, copy trie.h and trie.a"

# Help
help:
	@echo "Trie Utils Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  all          - Build trie.o object file"
	@echo "  test         - Build and run unit tests"
	@echo "  examples     - Build all example programs"
	@echo "  run_examples - Build and run selected examples"
	@echo "  clean        - Remove build artifacts"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "To use in your project:"
	@echo "  Include trie.h and compile with trie.c"