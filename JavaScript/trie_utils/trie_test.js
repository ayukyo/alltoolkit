/**
 * Trie Utility Tests
 * Comprehensive test suite for Trie data structure
 * Run with: node trie_test.js
 */

const { Trie, TrieNode } = require('./trie.js');

// Test helper
let testCount = 0;
let passCount = 0;

function test(name, fn) {
    testCount++;
    try {
        fn();
        passCount++;
        console.log(`✓ ${name}`);
    } catch (e) {
        console.log(`✗ ${name}`);
        console.log(`  Error: ${e.message}`);
    }
}

function assertEqual(actual, expected, message = '') {
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
        throw new Error(`${message}\nExpected: ${JSON.stringify(expected)}\nActual: ${JSON.stringify(actual)}`);
    }
}

function assertTrue(value, message = '') {
    if (!value) {
        throw new Error(`${message}\nExpected truthy value, got: ${value}`);
    }
}

function assertFalse(value, message = '') {
    if (value) {
        throw new Error(`${message}\nExpected falsy value, got: ${value}`);
    }
}

console.log('=== Trie Utility Tests ===\n');

// Test 1: Basic insert and search
test('Insert and search basic words', () => {
    const trie = new Trie();
    trie.insert('hello');
    trie.insert('world');
    
    assertTrue(trie.search('hello'));
    assertTrue(trie.search('world'));
    assertFalse(trie.search('hell'));
    assertFalse(trie.search('helloo'));
});

// Test 2: Empty trie behavior
test('Empty trie behavior', () => {
    const trie = new Trie();
    
    assertTrue(trie.isEmpty());
    assertEqual(trie.size(), 0);
    assertFalse(trie.search('anything'));
    assertFalse(trie.startsWith('a'));
});

// Test 3: startsWith
test('Prefix search with startsWith', () => {
    const trie = new Trie();
    trie.insert('apple');
    trie.insert('application');
    trie.insert('app');
    trie.insert('banana');
    
    assertTrue(trie.startsWith('app'));
    assertTrue(trie.startsWith('apple'));
    assertTrue(trie.startsWith('ban'));
    assertFalse(trie.startsWith('band'));
    assertFalse(trie.startsWith('cat'));
});

// Test 4: Delete
test('Delete words from trie', () => {
    const trie = new Trie();
    trie.insert('apple');
    trie.insert('app');
    trie.insert('application');
    
    assertEqual(trie.size(), 3);
    
    assertTrue(trie.delete('app'));
    assertEqual(trie.size(), 2);
    assertFalse(trie.search('app'));
    assertTrue(trie.search('apple'));
    assertTrue(trie.search('application'));
    
    // Delete non-existent word
    assertFalse(trie.delete('apricot'));
    assertEqual(trie.size(), 2);
});

// Test 5: Autocomplete
test('Autocomplete functionality', () => {
    const trie = new Trie();
    trie.insert('apple');
    trie.insert('app');
    trie.insert('application');
    trie.insert('apricot');
    trie.insert('banana');
    trie.insert('bandana');
    
    const results = trie.autocomplete('app');
    assertEqual(results.length, 3);
    
    const words = results.map(r => r.word);
    assertTrue(words.includes('apple'));
    assertTrue(words.includes('app'));
    assertTrue(words.includes('application'));
    assertFalse(words.includes('apricot'));
});

// Test 6: Autocomplete with limit
test('Autocomplete with limit', () => {
    const trie = new Trie();
    for (let i = 0; i < 20; i++) {
        trie.insert(`word${i.toString().padStart(2, '0')}`);
    }
    
    const results = trie.autocomplete('word', 5);
    assertEqual(results.length, 5);
});

// Test 7: Frequency tracking
test('Word frequency tracking', () => {
    const trie = new Trie();
    trie.insert('hello');
    trie.insert('hello');
    trie.insert('hello');
    trie.insert('world');
    
    const helloResults = trie.autocomplete('hello');
    assertEqual(helloResults[0].frequency, 3);
    
    const worldResults = trie.autocomplete('world');
    assertEqual(worldResults[0].frequency, 1);
});

// Test 8: Associated data
test('Associated data storage', () => {
    const trie = new Trie();
    trie.insert('apple', { color: 'red', type: 'fruit' });
    trie.insert('car', { wheels: 4, type: 'vehicle' });
    
    assertEqual(trie.getWordData('apple'), { color: 'red', type: 'fruit' });
    assertEqual(trie.getWordData('car'), { wheels: 4, type: 'vehicle' });
    assertEqual(trie.getWordData('unknown'), null);
    
    assertTrue(trie.updateWordData('apple', { color: 'green', type: 'fruit' }));
    assertEqual(trie.getWordData('apple'), { color: 'green', type: 'fruit' });
});

// Test 9: Pattern search with wildcards
test('Pattern search with wildcards', () => {
    const trie = new Trie();
    trie.insert('cat');
    trie.insert('car');
    trie.insert('bat');
    trie.insert('bar');
    trie.insert('can');
    
    const results = trie.searchPattern('ca?');
    assertEqual(results.length, 3);
    
    const words = results.map(r => r.word);
    assertTrue(words.includes('cat'));
    assertTrue(words.includes('car'));
    assertTrue(words.includes('can'));
    assertFalse(words.includes('bat'));
});

// Test 10: Longest common prefix
test('Longest common prefix', () => {
    const trie1 = new Trie();
    trie1.insert('flower');
    trie1.insert('flow');
    trie1.insert('flight');
    assertEqual(trie1.longestCommonPrefix(), 'fl');
    
    const trie2 = new Trie();
    trie2.insert('dog');
    trie2.insert('cat');
    trie2.insert('bird');
    assertEqual(trie2.longestCommonPrefix(), '');
});

// Test 11: Count with prefix
test('Count words with prefix', () => {
    const trie = new Trie();
    trie.insert('apple');
    trie.insert('application');
    trie.insert('app');
    trie.insert('apricot');
    trie.insert('banana');
    trie.insert('bandana');
    
    assertEqual(trie.countWithPrefix('app'), 3);
    assertEqual(trie.countWithPrefix('ap'), 4);
    assertEqual(trie.countWithPrefix('ban'), 2);
    assertEqual(trie.countWithPrefix('zebra'), 0);
});

// Test 12: Clear
test('Clear trie', () => {
    const trie = new Trie();
    trie.insert('one');
    trie.insert('two');
    trie.insert('three');
    
    assertEqual(trie.size(), 3);
    
    trie.clear();
    
    assertEqual(trie.size(), 0);
    assertTrue(trie.isEmpty());
    assertFalse(trie.search('one'));
});

// Test 13: Get all words
test('Get all words', () => {
    const trie = new Trie();
    trie.insert('banana');
    trie.insert('apple');
    trie.insert('cherry');
    trie.insert('date');
    
    const words = trie.getAllWords();
    assertEqual(words.length, 4);
    
    const wordList = words.map(w => w.word);
    assertTrue(wordList.includes('apple'));
    assertTrue(wordList.includes('banana'));
    assertTrue(wordList.includes('cherry'));
    assertTrue(wordList.includes('date'));
});

// Test 14: Unicode support
test('Unicode character support', () => {
    const trie = new Trie();
    trie.insert('你好');
    trie.insert('世界');
    trie.insert('こんにちは');
    trie.insert(' مرحبا');
    
    assertTrue(trie.search('你好'));
    assertTrue(trie.search('世界'));
    assertTrue(trie.search('こんにちは'));
    assertTrue(trie.startsWith('你'));
    assertFalse(trie.search('hello'));
});

// Test 15: Export/Import JSON
test('Export and import to/from JSON', () => {
    const trie1 = new Trie();
    trie1.insert('apple', { type: 'fruit' });
    trie1.insert('banana', { type: 'fruit' });
    trie1.insert('car', { type: 'vehicle' });
    
    const json = trie1.toJSON();
    
    const trie2 = new Trie();
    trie2.fromJSON(json);
    
    assertEqual(trie2.size(), 3);
    assertTrue(trie2.search('apple'));
    assertTrue(trie2.search('banana'));
    assertTrue(trie2.search('car'));
    assertEqual(trie2.getWordData('apple'), { type: 'fruit' });
});

// Test 16: Chaining
test('Method chaining', () => {
    const trie = new Trie()
        .insert('one')
        .insert('two')
        .insert('three');
    
    assertEqual(trie.size(), 3);
});

// Test 17: Error handling
test('Error handling for invalid input', () => {
    const trie = new Trie();
    
    let errorCaught = false;
    try {
        trie.insert('');
    } catch (e) {
        errorCaught = true;
    }
    assertTrue(errorCaught, 'Should throw on empty string');
    
    errorCaught = false;
    try {
        trie.insert(123);
    } catch (e) {
        errorCaught = true;
    }
    assertTrue(errorCaught, 'Should throw on non-string');
    
    // Search should handle gracefully (return false)
    assertFalse(trie.search(''));
    assertFalse(trie.search(null));
    assertFalse(trie.search(123));
});

// Test 18: Large dataset performance
test('Large dataset performance', () => {
    const trie = new Trie();
    const wordCount = 1000;
    
    // Insert many words
    const startInsert = Date.now();
    for (let i = 0; i < wordCount; i++) {
        trie.insert(`word${i}`);
    }
    const insertTime = Date.now() - startInsert;
    
    assertEqual(trie.size(), wordCount);
    console.log(`  Insert ${wordCount} words: ${insertTime}ms`);
    
    // Search performance
    const startSearch = Date.now();
    for (let i = 0; i < wordCount; i++) {
        trie.search(`word${i}`);
    }
    const searchTime = Date.now() - startSearch;
    console.log(`  Search ${wordCount} words: ${searchTime}ms`);
    
    // Autocomplete performance
    const startAuto = Date.now();
    trie.autocomplete('word', 10);
    const autoTime = Date.now() - startAuto;
    console.log(`  Autocomplete: ${autoTime}ms`);
    
    // Should be fast (< 100ms for each operation)
    assertTrue(insertTime < 500, 'Insert should be fast');
    assertTrue(searchTime < 500, 'Search should be fast');
    assertTrue(autoTime < 100, 'Autocomplete should be fast');
});

// Test 19: Edge cases
test('Edge cases', () => {
    const trie = new Trie();
    
    // Single character word
    trie.insert('a');
    assertTrue(trie.search('a'));
    assertTrue(trie.startsWith('a'));
    
    // Very long word
    const longWord = 'a'.repeat(1000);
    trie.insert(longWord);
    assertTrue(trie.search(longWord));
    assertEqual(trie.autocomplete('a', 5).length, 2);
    
    // Delete single char word
    assertTrue(trie.delete('a'));
    assertFalse(trie.search('a'));
    assertTrue(trie.search(longWord));
});

// Test 20: TrieNode class
test('TrieNode class', () => {
    const node = new TrieNode();
    
    assertEqual(node.children, {});
    assertFalse(node.isEndOfWord);
    assertEqual(node.frequency, 0);
    assertEqual(node.data, null);
});

// Print summary
console.log('\n=== Test Summary ===');
console.log(`Passed: ${passCount}/${testCount}`);
console.log(`Failed: ${testCount - passCount}/${testCount}`);

if (passCount === testCount) {
    console.log('\n✓ All tests passed!');
    process.exit(0);
} else {
    console.log('\n✗ Some tests failed.');
    process.exit(1);
}