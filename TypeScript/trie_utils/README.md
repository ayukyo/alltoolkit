# Trie Utilities - TypeScript

A comprehensive Trie (Prefix Tree) data structure utility module providing efficient string storage, prefix searching, and autocomplete functionality.

**Zero external dependencies.**

## Features

- **Trie Implementation**: Full-featured prefix tree with insert, search, delete operations
- **RadixTree**: Space-optimized compressed trie (Radix Tree)
- **Autocomplete**: Prefix-based word suggestions with frequency sorting
- **Pattern Matching**: Wildcard search support (`.` matches any character)
- **Longest Prefix Match**: Find longest word matching a string prefix
- **Frequency Tracking**: Track word usage frequency
- **Edit Distance Search**: Find words within specified edit distance
- **Serialization**: JSON export/import for persistence

## Installation

No external dependencies required. Simply import the module:

```typescript
import { Trie, RadixTree, TrieUtils } from './trie_utils/mod';
```

## Quick Start

### Basic Trie Operations

```typescript
import { Trie } from './trie_utils/mod';

const trie = new Trie();

// Insert words
trie.insert('apple');
trie.insert('app');
trie.insert('application');

// Search
trie.search('apple');     // true
trie.search('appl');      // false (partial word)
trie.startsWith('app');   // true

// Delete
trie.delete('apple');     // true
trie.search('apple');     // false
trie.search('app');       // true (still exists)
```

### Autocomplete

```typescript
import { Trie } from './trie_utils/mod';

const trie = Trie.fromArray(['apple', 'app', 'application', 'apply', 'apt']);

// Get all words starting with prefix
trie.autocomplete('app');  // ['app', 'apple', 'application', 'apply']

// Limit results
trie.autocomplete('app', 2);  // ['app', 'apple']

// Sort by frequency
trie.insert('apple', 10);  // insert with frequency
trie.insert('app', 1);
trie.autocompleteByFrequency('app');  // [{word: 'apple', frequency: 10}, ...]
```

### Pattern Matching

```typescript
import { Trie } from './trie_utils/mod';

const trie = Trie.fromArray(['cat', 'car', 'can', 'bat', 'bar']);

// Wildcard search (. matches any character)
trie.searchPattern('ca.');  // ['cat', 'car', 'can']
trie.searchPattern('.at');  // ['cat', 'bat']
```

### Longest Prefix Match

```typescript
import { Trie } from './trie_utils/mod';

const trie = Trie.fromArray(['www', 'www.example', 'www.example.com']);

trie.longestPrefixMatch('www.example.com/page');  // 'www.example.com'
trie.longestPrefixMatch('www.test.org');           // 'www'
```

### RadixTree (Compressed Trie)

```typescript
import { RadixTree } from './trie_utils/mod';

const radix = new RadixTree();
radix.insert('apple');
radix.insert('app');
radix.insert('application');

radix.search('apple');        // true
radix.autocomplete('app');    // ['app', 'apple', 'application']
```

## API Reference

### Trie Class

| Method | Description | Time Complexity |
|--------|-------------|-----------------|
| `insert(word, frequency)` | Insert a word | O(m) |
| `insertAll(words)` | Insert multiple words | O(n·m) |
| `search(word)` | Check if exact word exists | O(m) |
| `startsWith(prefix)` | Check if prefix exists | O(m) |
| `delete(word)` | Delete a word | O(m) |
| `autocomplete(prefix, limit)` | Get words with prefix | O(m + k) |
| `autocompleteByFrequency(prefix, limit)` | Autocomplete sorted by frequency | O(m + k) |
| `searchPattern(pattern, limit)` | Pattern match with wildcards | O(26^w·m) |
| `longestPrefixMatch(str)` | Find longest prefix word | O(m) |
| `getFrequency(word)` | Get word frequency | O(m) |
| `getAllWords()` | Get all words | O(n·m) |
| `size()` | Word count | O(1) |
| `nodeCount()` | Node count | O(1) |
| `clear()` | Clear all words | O(1) |

### TrieUtils Class

| Method | Description |
|--------|-------------|
| `fromArray(words)` | Create trie from array |
| `fromText(text)` | Create trie from text |
| `findWithinEditDistance(trie, word, maxDistance)` | Find words within edit distance |
| `merge(trie1, trie2)` | Merge two tries |
| `longestCommonPrefix(trie)` | Find longest common prefix |
| `totalCharacters(trie)` | Count total characters stored |
| `compressionRatio(trie)` | Calculate space efficiency |

## Use Cases

- **Autocomplete Systems**: Build efficient suggestion engines
- **Spell Checkers**: Find similar words using edit distance
- **Search Engines**: Prefix-based document indexing
- **URL Routing**: Path matching for web servers
- **Word Games**: Scrabble, Boggle, crossword helpers
- **Code Completion**: IDE autocomplete functionality

## Testing

```bash
npx ts-node mod_test.ts
```

## Performance

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Insert | O(m) | O(m) |
| Search | O(m) | O(1) |
| Delete | O(m) | O(1) |
| Prefix Search | O(m) | O(1) |
| Autocomplete | O(m + k) | O(k) |

Where:
- m = word length
- k = total characters in results
- n = number of words

## License

MIT