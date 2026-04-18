# Trie Utils

A Trie (Prefix Tree) data structure implementation for Rust with zero external dependencies.

## Features

- **Zero Dependencies**: Pure Rust implementation, no external crates needed
- **Generic Key Support**: Works with any sequence of keys (strings, bytes, custom types)
- **Prefix Operations**: Efficient prefix search, autocomplete, and counting
- **Pattern Matching**: Wildcard search with `?` (single char) and `*` (multi char)
- **Memory Efficient**: Nodes share common prefixes, reducing memory usage

## Usage

### Basic Operations

```rust
use trie_utils::Trie;

// Create a trie for strings
let mut trie = Trie::new();

// Insert words with values
trie.insert_str("hello", 1);
trie.insert_str("world", 2);
trie.insert_str("help", 3);

// Check if words exist
assert!(trie.contains_str("hello"));
assert!(!trie.contains_str("hi"));

// Prefix search
assert!(trie.starts_with_str("hel"));

// Get all words with prefix
let words = trie.get_by_prefix_str("hel");
// Returns: [("hello", &1), ("help", &3)]

// Autocomplete
let suggestions = trie.autocomplete("hel", Some(5));
// Returns: ["hello", "help"]
```

### String Set

```rust
use trie_utils::Trie;

// Create a simple word set
let mut dictionary = Trie::string_set();

dictionary.insert_word("apple");
dictionary.insert_word("banana");

assert!(dictionary.contains_word("apple"));
assert!(!dictionary.contains_word("cherry"));
```

### Pattern Matching

```rust
use trie_utils::Trie;

let mut trie = Trie::new();
trie.insert_str("cat", 1);
trie.insert_str("car", 2);
trie.insert_str("cart", 3);
trie.insert_str("cast", 4);

// Single character wildcard (?)
let results = trie.search_pattern("?at");
// Matches: cat, bat, rat (if present)

// Multi-character wildcard (*)
let results = trie.search_pattern("ca*");
// Matches: car, cart, cast, cat
```

### Longest Prefix Match

Useful for URL routing, IP routing tables, etc.

```rust
use trie_utils::Trie;

let mut routes = Trie::new();
routes.insert_str("/api/users", "UserController");
routes.insert_str("/api/posts", "PostController");
routes.insert_str("/static", "StaticController");

// Find longest matching prefix
let match = routes.longest_prefix_str("/api/users/123");
// Returns: ("/api/users", "UserController")
```

### Byte Trie

```rust
use trie_utils::Trie;

let mut trie: Trie<u8, &str> = Trie::new();

trie.insert([0x01, 0x02, 0x03].into_iter(), "first");
trie.insert([0x01, 0x02, 0x04].into_iter(), "second");

let key: Vec<u8> = vec![0x01, 0x02, 0x03];
assert!(trie.contains(&key));
```

## API Summary

### Core Methods

| Method | Description |
|--------|-------------|
| `new()` | Create empty trie |
| `insert(key, value)` | Insert key-value pair |
| `get(key)` | Get value for key |
| `contains(key)` | Check if key exists |
| `remove(key)` | Remove key |
| `len()` | Number of entries |
| `clear()` | Clear all entries |

### Prefix Methods

| Method | Description |
|--------|-------------|
| `starts_with(prefix)` | Check if any key has prefix |
| `count_prefix(prefix)` | Count keys with prefix |
| `get_by_prefix(prefix)` | Get all entries with prefix |
| `longest_prefix(key)` | Find longest matching prefix |
| `shortest_unique_prefix(key)` | Find shortest unique prefix |

### String Convenience Methods

| Method | Description |
|--------|-------------|
| `insert_str(s, v)` | Insert string |
| `get_str(s)` | Get value for string |
| `contains_str(s)` | Check if string exists |
| `autocomplete(prefix, limit)` | Get autocomplete suggestions |
| `search_pattern(pattern)` | Wildcard search |

## Time Complexity

| Operation | Complexity |
|-----------|------------|
| Insert | O(k) |
| Search | O(k) |
| Delete | O(k) |
| Prefix Search | O(k + n) |
| Autocomplete | O(k + m) |

Where k = key length, n = number of matching entries, m = result limit.

## Use Cases

- **Autocomplete/Typeahead**: Efficient prefix-based suggestions
- **Spell Checking**: Quick dictionary lookup
- **URL Routing**: Longest prefix match for route resolution
- **IP Routing Tables**: Network prefix matching
- **Word Games**: Fast word validation (Scrabble, Boggle)
- **Search Engines**: Prefix-based indexing