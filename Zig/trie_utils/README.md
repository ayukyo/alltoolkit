# Trie Utils

A comprehensive Trie (Prefix Tree) implementation for Zig. Zero external dependencies - pure Zig standard library.

## Features

- **Trie**: Efficient string storage and prefix operations data structure
- **Basic operations**: insert, search, delete, batch insert
- **Prefix operations**: startsWith, countPrefix, longestCommonPrefix
- **Autocomplete**: getWordsWithPrefix, getAllWords (supports result limiting)
- **Pattern matching**: patternMatch with `?` (single char) and `*` (multiple chars) wildcards
- **Utilities**: count, isEmpty, nodeCount, memoryUsage, clear
- **Memory efficient**: Automatic cleanup of unused nodes

## Usage

```zig
const std = @import("std");
const Trie = @import("trie").Trie;

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    // Create a trie with max word size of 256 characters
    var trie = try Trie(256).init(allocator);
    defer trie.deinit();
    
    // Insert words
    _ = try trie.insert("apple");
    _ = try trie.insert("app");
    _ = try trie.insert("application");
    _ = try trie.insert("apply");
    
    // Search
    std.debug.print("Search 'apple': {}\n", .{trie.search("apple")});
    std.debug.print("Search 'appl': {}\n", .{trie.search("appl")});
    
    // Prefix operations
    std.debug.print("Starts with 'app': {}\n", .{trie.startsWith("app")});
    std.debug.print("Count prefix 'app': {}\n", .{trie.countPrefix("app")});
    
    // Autocomplete
    const words = try trie.getWordsWithPrefix(allocator, "app", 10);
    defer {
        for (words) |w| allocator.free(w);
        allocator.free(words);
    }
    std.debug.print("Words with prefix 'app':\n", .{});
    for (words) |word| {
        std.debug.print("  - {s}\n", .{word});
    }
}
```

## API Reference

### Initialization

```zig
var trie = try Trie(max_word_size).init(allocator);
defer trie.deinit();
```

### Basic Operations

| Method | Description |
|--------|-------------|
| `insert(word) !bool` | Insert a word, returns true if new |
| `insertBatch(words) !usize` | Insert multiple words |
| `search(word) bool` | Check if exact word exists |
| `delete(word) bool` | Remove a word, returns true if found |
| `count() usize` | Get total word count |
| `isEmpty() bool` | Check if trie is empty |
| `clear() !void` | Remove all words |

### Prefix Operations

| Method | Description |
|--------|-------------|
| `startsWith(prefix) bool` | Check if any word starts with prefix |
| `countPrefix(prefix) usize` | Count words with given prefix |
| `longestCommonPrefix() []const u8` | Find longest common prefix |

### Autocomplete

| Method | Description |
|--------|-------------|
| `getWordsWithPrefix(allocator, prefix, max) ![][]u8` | Get words starting with prefix |
| `getAllWords(allocator) ![][]u8` | Get all words in trie |

### Pattern Matching

```zig
// '?' matches any single character
// '*' matches zero or more characters
const matches = try trie.patternMatch(allocator, "ca?", 10);
```

### Utilities

| Method | Description |
|--------|-------------|
| `nodeCount() usize` | Count total nodes in trie |
| `memoryUsage() usize` | Estimate memory usage in bytes |

## Building

```bash
# Run tests
zig build test

# Run examples
zig build example-basic
zig build example-autocomplete
zig build example-spellcheck
zig build example-pattern
zig build example-frequency
```

## Examples

### Basic Usage
```bash
zig build example-basic
```
Demonstrates insert, search, delete, and prefix operations.

### Autocomplete
```bash
zig build example-autocomplete
```
Shows how to implement autocomplete functionality.

### Spell Checker
```bash
zig build example-spellcheck
```
Implements a simple spell checker using Trie.

### Pattern Matching
```bash
zig build example-pattern
```
Demonstrates wildcard pattern matching.

### Word Frequency
```bash
zig build example-frequency
```
Shows word frequency counting with Trie.

## Performance

- **Insert**: O(m) where m is word length
- **Search**: O(m)
- **Delete**: O(m)
- **Prefix operations**: O(m)
- **Autocomplete**: O(m + k×l) where k is number of results, l is average word length
- **Pattern matching**: O(m × 26^w) where w is number of wildcards

## Notes

- Characters are case-insensitive (both 'A' and 'a' map to the same node)
- Only alphabetic characters (a-z, A-Z) are supported
- Maximum word size is configurable at compile time
- Memory is automatically managed when using deinit()

## License

MIT