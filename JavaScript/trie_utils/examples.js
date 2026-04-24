/**
 * Trie Utility Examples
 * Demonstrates common use cases for the Trie data structure
 * Run with: node examples.js
 */

const { Trie } = require('./trie.js');

console.log('=== Trie Utility Examples ===\n');

// Example 1: Autocomplete System
console.log('1. Autocomplete System');
console.log('----------------------');

const autocompleteTrie = new Trie();

// Common programming terms
const programmingTerms = [
    'function', 'functional', 'functional programming',
    'variable', 'var', 'value',
    'class', 'classy', 'classical', 'class inheritance',
    'array', 'arraylist', 'array methods',
    'object', 'object-oriented', 'object destructuring',
    'string', 'string interpolation', 'string methods',
    'map', 'map function', 'map data structure',
    'filter', 'filter array', 'find', 'findIndex',
    'reduce', 'reduce array',
    'promise', 'promise all', 'promise chaining',
    'async', 'async await', 'asynchronous',
    'callback', 'callback hell',
    'closure', 'closures in javascript',
    'prototype', 'prototypal inheritance',
    'module', 'modules', 'modular design'
];

programmingTerms.forEach(term => autocompleteTrie.insert(term));

console.log('Search "fun":');
autocompleteTrie.autocomplete('fun', 5).forEach(r => {
    console.log(`  - ${r.word}`);
});

console.log('\nSearch "arr":');
autocompleteTrie.autocomplete('arr', 5).forEach(r => {
    console.log(`  - ${r.word}`);
});

console.log('\nSearch "pro":');
autocompleteTrie.autocomplete('pro', 5).forEach(r => {
    console.log(`  - ${r.word}`);
});

// Example 2: Spell Checker
console.log('\n\n2. Spell Checker');
console.log('----------------');

const dictionary = new Trie();
const words = [
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
    'hello', 'world', 'javascript', 'programming', 'computer', 'algorithm',
    'data', 'structure', 'trie', 'tree', 'node', 'search', 'insert', 'delete'
];

words.forEach(word => dictionary.insert(word));

function spellCheck(word, trie) {
    if (trie.search(word)) {
        return { correct: true, word };
    }
    
    // Try to find similar words
    const suggestions = trie.searchPattern(word.slice(0, -1) + '?', 3);
    return { correct: false, word, suggestions };
}

const testWords = ['hello', 'hallo', 'javascript', 'javascrit', 'trie', 'trei', 'xyz'];
testWords.forEach(word => {
    const result = spellCheck(word, dictionary);
    if (result.correct) {
        console.log(`✓ "${word}" is correct`);
    } else {
        console.log(`✗ "${word}" not found. Suggestions: ${result.suggestions.map(s => s.word).join(', ') || 'none'}`);
    }
});

// Example 3: Word Frequency Counter
console.log('\n\n3. Word Frequency Counter');
console.log('-------------------------');

const frequencyTrie = new Trie();
const text = 'the quick brown fox jumps over the lazy dog the fox was quick';
const wordList = text.toLowerCase().split(/\s+/);

wordList.forEach(word => frequencyTrie.insert(word));

console.log('Word frequencies in: "the quick brown fox jumps over the lazy dog the fox was quick"');
frequencyTrie.getAllWords()
    .sort((a, b) => b.frequency - a.frequency)
    .forEach(r => {
        console.log(`  ${r.word}: ${r.frequency}`);
    });

// Example 4: Contact Search
console.log('\n\n4. Contact Search (with associated data)');
console.log('---------------------------------------');

const contacts = new Trie();

const contactList = [
    { name: 'Alice Johnson', phone: '555-0101', email: 'alice@example.com' },
    { name: 'Alice Smith', phone: '555-0102', email: 'alice.smith@example.com' },
    { name: 'Bob Brown', phone: '555-0201', email: 'bob@example.com' },
    { name: 'Charlie Davis', phone: '555-0301', email: 'charlie@example.com' },
    { name: 'David Wilson', phone: '555-0401', email: 'david@example.com' },
    { name: 'Eve Miller', phone: '555-0501', email: 'eve@example.com' },
    { name: 'Alice Cooper', phone: '555-0103', email: 'alice.cooper@example.com' }
];

contactList.forEach(contact => {
    contacts.insert(contact.name.toLowerCase(), contact);
});

console.log('Search contacts starting with "alice":');
contacts.autocomplete('alice', 5).forEach(r => {
    console.log(`  ${r.data.name}`);
    console.log(`    Phone: ${r.data.phone}`);
    console.log(`    Email: ${r.data.email}`);
});

// Example 5: Longest Common Prefix
console.log('\n\n5. Longest Common Prefix');
console.log('------------------------');

const prefixTrie1 = new Trie();
['flower', 'flow', 'flight'].forEach(w => prefixTrie1.insert(w));
console.log(`LCP of ["flower", "flow", "flight"]: "${prefixTrie1.longestCommonPrefix()}"`);

const prefixTrie2 = new Trie();
['interspecies', 'interstellar', 'interstate'].forEach(w => prefixTrie2.insert(w));
console.log(`LCP of ["interspecies", "interstellar", "interstate"]: "${prefixTrie2.longestCommonPrefix()}"`);

const prefixTrie3 = new Trie();
['dog', 'racecar', 'car'].forEach(w => prefixTrie3.insert(w));
console.log(`LCP of ["dog", "racecar", "car"]: "${prefixTrie3.longestCommonPrefix()}"`);

// Example 6: Word Games - Find words matching patterns
console.log('\n\n6. Word Games - Pattern Matching');
console.log('--------------------------------');

const wordGameTrie = new Trie();
const gameWords = [
    'cat', 'bat', 'rat', 'hat', 'mat', 'sat', 'pat', 'vat',
    'car', 'bar', 'far', 'jar', 'tar', 'war',
    'care', 'bare', 'fare', 'rare', 'ware',
    'cared', 'bared', 'fared', 'rared'
];

gameWords.forEach(word => wordGameTrie.insert(word));

console.log('Words matching "?at" (3-letter words ending in "at"):');
wordGameTrie.searchPattern('?at', 10).forEach(r => console.log(`  ${r.word}`));

console.log('\nWords matching "ca?" (3-letter words starting with "ca"):');
wordGameTrie.searchPattern('ca?', 10).forEach(r => console.log(`  ${r.word}`));

console.log('\nWords matching "???e" (4-letter words ending in "e"):');
wordGameTrie.searchPattern('???e', 10).forEach(r => console.log(`  ${r.word}`));

// Example 7: Serialization
console.log('\n\n7. Serialization (Export/Import)');
console.log('--------------------------------');

const originalTrie = new Trie();
originalTrie.insert('apple', { color: 'red' });
originalTrie.insert('banana', { color: 'yellow' });
originalTrie.insert('cherry', { color: 'red' });

console.log('Original trie:');
originalTrie.getAllWords().forEach(w => console.log(`  ${w.word}: ${JSON.stringify(w.data)}`));

const exported = JSON.stringify(originalTrie.toJSON(), null, 2);
console.log('\nExported JSON (truncated):');
console.log(exported.substring(0, 300) + '...');

const importedTrie = new Trie();
importedTrie.fromJSON(JSON.parse(exported));

console.log('\nImported trie:');
importedTrie.getAllWords().forEach(w => console.log(`  ${w.word}: ${JSON.stringify(w.data)}`));

// Example 8: IP Routing Table (simplified)
console.log('\n\n8. IP Routing Table (simplified)');
console.log('--------------------------------');

const routingTable = new Trie();

// Simplified IP prefixes with routing info
const routes = [
    { prefix: '192.168.1', gateway: '10.0.0.1', interface: 'eth0' },
    { prefix: '192.168.2', gateway: '10.0.0.2', interface: 'eth1' },
    { prefix: '10.0.0', gateway: 'direct', interface: 'lo' },
    { prefix: '172.16', gateway: '10.0.0.3', interface: 'eth2' }
];

routes.forEach(route => {
    routingTable.insert(route.prefix, route);
});

console.log('IP Routing Table:');
routingTable.getAllWords().forEach(r => {
    console.log(`  ${r.data.prefix}.x -> ${r.data.gateway} (${r.data.interface})`);
});

console.log('\nLookup "192.168.1":');
const route1 = routingTable.autocomplete('192.168.1', 1);
if (route1.length > 0) {
    const r = route1[0].data;
    console.log(`  Route via ${r.gateway} on ${r.interface}`);
}

// Example 9: Performance Benchmark
console.log('\n\n9. Performance Benchmark');
console.log('--------------------------');

const benchTrie = new Trie();
const benchWords = [];
const benchCount = 10000;

// Generate test words
for (let i = 0; i < benchCount; i++) {
    const word = `word${i.toString().padStart(5, '0')}`;
    benchWords.push(word);
}

// Insert benchmark
const insertStart = Date.now();
benchWords.forEach(word => benchTrie.insert(word));
const insertTime = Date.now() - insertStart;

// Search benchmark
const searchStart = Date.now();
benchWords.forEach(word => benchTrie.search(word));
const searchTime = Date.now() - searchStart;

// Autocomplete benchmark
const autoStart = Date.now();
for (let i = 0; i < 1000; i++) {
    benchTrie.autocomplete('word05', 10);
}
const autoTime = Date.now() - autoStart;

console.log(`${benchCount} words:`);
console.log(`  Insert: ${insertTime}ms`);
console.log(`  Search all: ${searchTime}ms`);
console.log(`  1000 autocompletes: ${autoTime}ms`);
console.log(`  Memory: ${benchTrie.size()} words in trie`);

console.log('\n=== End of Examples ===');