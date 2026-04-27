# Makefile for Bloom Filter
# Zero external dependencies - uses only C++ standard library

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

# Targets
all: test examples

test: bloom_filter_test.cpp
	$(CXX) $(CXXFLAGS) -o bloom_filter_test bloom_filter_test.cpp
	./bloom_filter_test

examples: usage_examples.cpp
	$(CXX) $(CXXFLAGS) -o usage_examples examples/usage_examples.cpp
	./usage_examples

clean:
	rm -f bloom_filter_test usage_examples bloom_filter.dat

.PHONY: all test examples clean