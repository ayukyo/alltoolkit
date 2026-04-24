# Trie Utility (JavaScript)

A high-performance **Trie (Prefix Tree)** data structure implementation with zero external dependencies.

## Features

- ✅ **Core Operations**: Insert, search, delete words
- ✅ **Prefix Search**: Autocomplete suggestions
- ✅ **Pattern Matching**: Search with wildcards (`?` matches any single character)
- ✅ **Frequency Tracking**: Track word occurrence counts
- ✅ **Data Association**: Store custom data with each word
- ✅ **Serialization**: Export/import to JSON format
- ✅ **Unicode Support**: Works with any Unicode characters
- ✅ **Zero Dependencies**: Pure JavaScript, works everywhere

## Time Complexity

| Operation | Complexity |
|-----------|------------|
| Insert | O(m) |
| Search | O(m) |
| Delete | O(m) |
| Prefix Search | O(m + n) |

Where `m` is the word length and `n` is the total characters in results.

## Quick Start

```javascript
const { Trie } = require('./trie.js');

// Create a trie
const trie = new Trie();

// Insert words
trie.insert('apple');
trie.insert('application');
trie.insert('app');
trie.insert('apricot');

// Search
console.log(trie.search('apple'));     // true
console.log(trie.search('app'));       // true
console.log(trie.search('ap'));        // false (prefix only)

// Prefix check
console.log(trie.startsWith('app'));   // true

// Autocomplete
trie.autocomplete('app').forEach(r => {
    console.log(r.word, r.frequency);
});
// Output: app, apple, application (sorted by frequency)
```

## API Reference

### Constructor

```javascript
const trie = new Trie();
```

### Methods

#### `insert(word, data?)`
Insert a word into the trie. Optionally associate data with it.
```javascript
trie.insert('hello');
trie.insert('world', { importance: 'high' });
```

#### `search(word) → boolean`
Check if a word exists in the trie.
```javascript
trie.search('hello'); // true or false
```

#### `startsWith(prefix) → boolean`
Check if any word starts with the given prefix.
```javascript
trie.startsWith('hel'); // true if any word begins with 'hel'
```

#### `delete(word) → boolean`
Remove a word from the trie. Returns `true` if word was deleted.
```javascript
trie.delete('hello'); // true if found and deleted
```

#### `autocomplete(prefix, limit?) → Array`
Get all words with the given prefix, sorted by frequency.
```javascript
trie.autocomplete('app', 5); // [{word: 'apple', frequency: 1, data: null}, ...]
```

#### `searchPattern(pattern, limit?) → Array`
Search for words matching a pattern. Use `?` as wildcard.
```javascript
trie.searchPattern('a?ple'); // Matches 'apple', 'ample', etc.
```

#### `getWordData(word) → * | null`
Get data associated with a word.
```javascript
trie.getWordData('world'); // { importance: 'high' }
```

#### `updateWordData(word, data) → boolean`
Update data associated with a word.
```javascript
trie.updateWordData('world', { importance: 'low' });
```

#### `countWithPrefix(prefix) → number`
Count all words with the given prefix.
```javascript
trie.countWithPrefix('app'); // 3 (app, apple, application)
```

#### `longestCommonPrefix() → string`
Get the longest common prefix of all words.
```javascript
trie.insert('flower');
trie.insert('flow');
trie.insert('flight');
trie.longestCommonPrefix(); // 'fl'
```

#### `getAllWords(limit?) → Array`
Get all words in the trie.
```javascript
trie.getAllWords(); // [{word: 'apple', frequency: 1, data: null}, ...]
```

#### `size() → number`
Get the total number of words.
```javascript
trie.size(); // 5
```

#### `isEmpty() → boolean`
Check if trie is empty.
```javascript
trie.isEmpty(); // false
```

#### `clear()`
Remove all words from the trie.
```javascript
trie.clear();
```

#### `toJSON() → Object`
Export trie to JSON format.
```javascript
const json = trie.toJSON();
localStorage.setItem('trie', JSON.stringify(json));
```

#### `fromJSON(json) → Trie`
Import trie from JSON format.
```javascript
const trie = new Trie();
trie.fromJSON(JSON.parse(localStorage.getItem('trie')));
```

## Use Cases

### 1. Autocomplete System
```javascript
const autocomplete = new Trie();
dictionary.forEach(word => autocomplete.insert(word));

// Get suggestions as user types
input.addEventListener('input', (e) => {
    const suggestions = autocomplete.autocomplete(e.target.value, 10);
    showSuggestions(suggestions);
});
```

### 2. Spell Checker
```javascript
const dictionary = new Trie();
words.forEach(w => dictionary.insert(w));

function spellCheck(word) {
    if (dictionary.search(word)) return { correct: true };
    
    // Suggest similar words
    const suggestions = dictionary.searchPattern(
        word.slice(0, -1) + '?', 5
    );
    return { correct: false, suggestions };
}
```

### 3. Contact Search
```javascript
const contacts = new Trie();
contacts.insert('alice', { phone: '555-0101', email: 'alice@example.com' });
contacts.insert('alice smith', { phone: '555-0102' });

const results = contacts.autocomplete('ali');
results.forEach(r => console.log(r.data));
```

### 4. Word Frequency Counter
```javascript
const counter = new Trie();
text.split(/\s+/).forEach(word => counter.insert(word.toLowerCase()));

counter.getAllWords()
    .sort((a, b) => b.frequency - a.frequency)
    .forEach(w => console.log(`${w.word}: ${w.frequency}`));
```

### 5. IP Routing Table
```javascript
const routes = new Trie();
routes.insert('192.168.1', { gateway: '10.0.0.1' });
routes.insert('192.168.2', { gateway: '10.0.0.2' });

// Find route for IP
const route = routes.autocomplete('192.168.1.100', 1)[0];
```

## Running Tests

```bash
node trie_test.js
```

## Running Examples

```bash
node examples.js
```

## License

MIT License - Free for personal and commercial use.