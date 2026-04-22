/**
 * Trie Utilities - Basic Usage Examples
 * 
 * Demonstrates core functionality of Trie and RadixTree.
 */

import { Trie, RadixTree, TrieUtils } from '../mod';

console.log('=== Trie Utilities Examples ===\n');

// Example 1: Basic Trie Operations
console.log('📝 Example 1: Basic Trie Operations');
console.log('-'.repeat(40));

const trie = new Trie();

// Insert words
trie.insert('apple');
trie.insert('app');
trie.insert('application');
trie.insert('apply');
trie.insert('aptitude');
trie.insert('banana');

console.log('Inserted words: apple, app, application, apply, aptitude, banana');
console.log(`Total words: ${trie.size()}`);
console.log(`Total nodes: ${trie.nodeCount()}`);

// Search for words
console.log('\nSearch results:');
console.log(`  search('apple'): ${trie.search('apple')}`);
console.log(`  search('app'): ${trie.search('app')}`);
console.log(`  search('appl'): ${trie.search('appl')} (partial word)`);
console.log(`  search('orange'): ${trie.search('orange')} (not in trie)`);

// Prefix search
console.log('\nPrefix search:');
console.log(`  startsWith('app'): ${trie.startsWith('app')}`);
console.log(`  startsWith('ban'): ${trie.startsWith('ban')}`);
console.log(`  startsWith('xyz'): ${trie.startsWith('xyz')}`);

// Example 2: Autocomplete
console.log('\n📝 Example 2: Autocomplete');
console.log('-'.repeat(40));

const autocompleteResults = trie.autocomplete('app', 5);
console.log(`Autocomplete for 'app': ${autocompleteResults.join(', ')}`);

// Build a dictionary trie
const dictionary = Trie.fromArray([
    'algorithm', 'array', 'binary', 'branch', 'buffer',
    'cache', 'class', 'code', 'compiler', 'computer',
    'data', 'debug', 'developer', 'display', 'driver',
    'editor', 'encode', 'error', 'event', 'exception',
    'file', 'float', 'function', 'framework', 'frontend'
]);

console.log('\nAutocomplete from dictionary:');
console.log(`  'de' → ${dictionary.autocomplete('de').join(', ')}`);
console.log(`  'co' → ${dictionary.autocomplete('co').join(', ')}`);
console.log(`  'fu' → ${dictionary.autocomplete('fu').join(', ')}`);

// Example 3: Frequency Tracking
console.log('\n📝 Example 3: Word Frequency Tracking');
console.log('-'.repeat(40));

const freqTrie = new Trie();

// Simulate search history
const searches = ['javascript', 'python', 'javascript', 'python', 'javascript', 'rust', 'python', 'python'];
for (const term of searches) {
    freqTrie.insert(term);
}

console.log('Search history frequencies:');
const results = freqTrie.autocompleteByFrequency('');
for (const r of results) {
    console.log(`  ${r.word}: ${r.frequency} searches`);
}

// Example 4: Pattern Matching
console.log('\n📝 Example 4: Pattern Matching with Wildcards');
console.log('-'.repeat(40));

const wordsTrie = Trie.fromArray([
    'cat', 'car', 'can', 'cap', 'cab',
    'bat', 'bar', 'ban', 'bag',
    'rat', 'ran', 'rap'
]);

console.log('Pattern matching:');
console.log(`  'ca.' → ${wordsTrie.searchPattern('ca.').join(', ')}`);
console.log(`  '.at' → ${wordsTrie.searchPattern('.at').join(', ')}`);
console.log(`  'b..' → ${wordsTrie.searchPattern('b..').join(', ')}`);

// Example 5: Longest Prefix Match
console.log('\n📝 Example 5: Longest Prefix Match');
console.log('-'.repeat(40));

const prefixTrie = Trie.fromArray(['www', 'www.example', 'www.example.com', 'api']);
const urls = [
    'www.example.com/page',
    'www.test.org',
    'api/v1/users',
    'unknown.site'
];

console.log('URL prefix matching:');
for (const url of urls) {
    const match = prefixTrie.longestPrefixMatch(url);
    console.log(`  '${url}' → '${match}'`);
}

// Example 6: RadixTree (Compressed Trie)
console.log('\n📝 Example 6: RadixTree (Space-Efficient Trie)');
console.log('-'.repeat(40));

const radix = new RadixTree();
radix.insert('apple');
radix.insert('app');
radix.insert('application');
radix.insert('applepie');

console.log('RadixTree operations:');
console.log(`  search('apple'): ${radix.search('apple')}`);
console.log(`  search('app'): ${radix.search('app')}`);
console.log(`  autocomplete('app'): ${radix.autocomplete('app').join(', ')}`);

// Example 7: Trie Utilities
console.log('\n📝 Example 7: Trie Utilities');
console.log('-'.repeat(40));

const text = 'Hello world, hello universe, hello everyone!';
const textTrie = TrieUtils.fromText(text);

console.log('Text analysis:');
console.log(`  Words found: ${textTrie.getAllWords().join(', ')}`);
console.log(`  'hello' frequency: ${textTrie.getFrequency('hello')}`);

// Merge two tries
const trie1 = Trie.fromArray(['apple', 'banana']);
const trie2 = Trie.fromArray(['cherry', 'date']);
const merged = TrieUtils.merge(trie1, trie2);

console.log('\nMerged trie:');
console.log(`  Words: ${merged.getAllWords().join(', ')}`);
console.log(`  Size: ${merged.size()}`);

// Longest common prefix
const lcpTrie = Trie.fromArray(['programming', 'programmer', 'program', 'programmable']);
const lcp = TrieUtils.longestCommonPrefix(lcpTrie);
console.log(`\nLongest common prefix of ${lcpTrie.getAllWords().join(', ')}: '${lcp}'`);

// Compression analysis
console.log('\nCompression analysis:');
console.log(`  Total characters: ${TrieUtils.totalCharacters(lcpTrie)}`);
console.log(`  Compression ratio: ${TrieUtils.compressionRatio(lcpTrie).toFixed(2)}`);

// Example 8: Edit Distance Search
console.log('\n📝 Example 8: Spell Check with Edit Distance');
console.log('-'.repeat(40));

const spellTrie = Trie.fromArray([
    'hello', 'help', 'held', 'hero', 'hallo', 'hello',
    'world', 'word', 'work', 'would', 'worn'
]);

const misspelled = 'helo';
const suggestions = TrieUtils.findWithinEditDistance(spellTrie, misspelled, 1);
console.log(`Suggestions for '${misspelled}' (edit distance ≤ 1):`);
console.log(`  ${suggestions.join(', ')}`);

console.log('\n✅ All examples completed successfully!');