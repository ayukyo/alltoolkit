/**
 * Trie Utilities - Test Suite
 * 
 * Comprehensive tests for Trie and RadixTree implementations.
 * Run with: npx ts-node mod_test.ts
 */

import { Trie, RadixTree, TrieUtils, TrieSearchResult } from './mod.js';

// Test helper
function assert(condition: boolean, message: string): void {
    if (!condition) {
        throw new Error(`Assertion failed: ${message}`);
    }
}

function assertEqual<T>(actual: T, expected: T, message: string): void {
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
        throw new Error(`${message}\n  Expected: ${JSON.stringify(expected)}\n  Actual: ${JSON.stringify(actual)}`);
    }
}

function describe(name: string, fn: () => void): void {
    console.log(`\n📋 ${name}`);
    try {
        fn();
        console.log(`  ✅ All tests passed`);
    } catch (e: any) {
        console.log(`  ❌ Test failed: ${e.message}`);
        process.exit(1);
    }
}

function it(name: string, fn: () => void): void {
    try {
        fn();
        console.log(`  ✓ ${name}`);
    } catch (e: any) {
        console.log(`  ✗ ${name}`);
        throw e;
    }
}

// ==================== Trie Tests ====================

describe('Trie - Basic Operations', () => {
    it('should insert and search words', () => {
        const trie = new Trie();
        trie.insert('apple');
        assert(trie.search('apple'), 'Should find "apple"');
        assert(!trie.search('app'), 'Should not find "app"');
        assert(!trie.search('orange'), 'Should not find "orange"');
    });

    it('should handle empty string', () => {
        const trie = new Trie();
        assert(!trie.search(''), 'Empty string should not be found by default');
        trie.insert('');
        assert(trie.search(''), 'Empty string should be found after insert');
    });

    it('should handle startsWith', () => {
        const trie = new Trie();
        trie.insert('apple');
        trie.insert('app');
        trie.insert('application');
        
        assert(trie.startsWith('app'), 'Should find prefix "app"');
        assert(trie.startsWith('apple'), 'Should find prefix "apple"');
        assert(!trie.startsWith('orange'), 'Should not find prefix "orange"');
        assert(trie.startsWith(''), 'Empty prefix should return true');
    });

    it('should delete words correctly', () => {
        const trie = new Trie();
        trie.insert('apple');
        trie.insert('app');
        
        assert(trie.delete('apple'), 'Should delete "apple"');
        assert(!trie.search('apple'), 'Should not find "apple" after delete');
        assert(trie.search('app'), '"app" should still exist');
        assert(trie.startsWith('app'), 'Prefix "app" should still exist');
    });

    it('should handle deleting non-existent words', () => {
        const trie = new Trie();
        trie.insert('hello');
        assert(!trie.delete('world'), 'Should return false for non-existent word');
        assert(!trie.delete('hel'), 'Should return false for partial word');
    });

    it('should track size correctly', () => {
        const trie = new Trie();
        assertEqual(trie.size(), 0, 'Initial size should be 0');
        
        trie.insert('one');
        trie.insert('two');
        trie.insert('three');
        assertEqual(trie.size(), 3, 'Size should be 3');
        
        trie.insert('one'); // duplicate
        assertEqual(trie.size(), 3, 'Size should still be 3 after duplicate insert');
        
        trie.delete('one');
        assertEqual(trie.size(), 2, 'Size should be 2 after delete');
    });
});

describe('Trie - Autocomplete', () => {
    it('should autocomplete words', () => {
        const trie = new Trie();
        trie.insertAll(['apple', 'app', 'application', 'apply', 'apt', 'banana']);
        
        const results = trie.autocomplete('app');
        assertEqual(results.length, 4, 'Should find 4 words with prefix "app"');
        assert(results.includes('app'), 'Should include "app"');
        assert(results.includes('apple'), 'Should include "apple"');
    });

    it('should respect limit in autocomplete', () => {
        const trie = new Trie();
        trie.insertAll(['apple', 'app', 'application', 'apply', 'appliance']);
        
        const results = trie.autocomplete('app', 2);
        assertEqual(results.length, 2, 'Should return at most 2 results');
    });

    it('should return empty for non-existent prefix', () => {
        const trie = new Trie();
        trie.insert('hello');
        
        const results = trie.autocomplete('xyz');
        assertEqual(results.length, 0, 'Should return empty for non-existent prefix');
    });

    it('should autocomplete with frequency sorting', () => {
        const trie = new Trie();
        trie.insert('apple', 5);
        trie.insert('app', 1);
        trie.insert('application', 10);
        trie.insert('apply', 3);
        
        const results = trie.autocompleteByFrequency('app');
        assertEqual(results.length, 4, 'Should have 4 results');
        assertEqual(results[0].word, 'application', 'Most frequent should be first');
        assertEqual(results[0].frequency, 10, 'Should have correct frequency');
    });
});

describe('Trie - Pattern Matching', () => {
    it('should match patterns with wildcards', () => {
        const trie = new Trie();
        trie.insertAll(['cat', 'car', 'can', 'cap', 'bat', 'bar']);
        
        const results = trie.searchPattern('ca.');
        assertEqual(results.length, 4, 'Should find 4 words matching "ca."');
        assert(results.includes('cat'), 'Should include "cat"');
        assert(results.includes('car'), 'Should include "car"');
    });

    it('should match multiple wildcards', () => {
        const trie = new Trie();
        trie.insertAll(['test', 'text', 'best', 'rest']);
        
        const results = trie.searchPattern('.e.t');
        assertEqual(results.length, 4, 'Should find 4 words matching ".e.t"');
    });

    it('should handle patterns with no matches', () => {
        const trie = new Trie();
        trie.insertAll(['hello', 'world']);
        
        const results = trie.searchPattern('xyz.');
        assertEqual(results.length, 0, 'Should return empty for no matches');
    });
});

describe('Trie - Advanced Features', () => {
    it('should find longest prefix match', () => {
        const trie = new Trie();
        trie.insert('app');
        trie.insert('apple');
        trie.insert('application');
        
        assertEqual(trie.longestPrefixMatch('application'), 'application', 'Should find full match');
        assertEqual(trie.longestPrefixMatch('appetite'), 'app', 'Should find longest prefix');
        assertEqual(trie.longestPrefixMatch('xyz'), '', 'Should return empty for no match');
    });

    it('should track word frequency', () => {
        const trie = new Trie();
        trie.insert('hello');
        trie.insert('hello');
        trie.insert('hello');
        
        assertEqual(trie.getFrequency('hello'), 3, 'Should have frequency 3');
        assertEqual(trie.getFrequency('world'), 0, 'Non-existent word should have 0 frequency');
        
        trie.incrementFrequency('hello', 2);
        assertEqual(trie.getFrequency('hello'), 5, 'Should have frequency 5 after increment');
    });

    it('should count words with prefix', () => {
        const trie = new Trie();
        trie.insertAll(['apple', 'app', 'application', 'apply', 'apt']);
        
        assertEqual(trie.countWordsWithPrefix('app'), 4, 'Should count 4 words with "app"');
        assertEqual(trie.countWordsWithPrefix('ap'), 5, 'Should count 5 words with "ap"');
        assertEqual(trie.countWordsWithPrefix('xyz'), 0, 'Should count 0 for non-existent prefix');
    });

    it('should get all words', () => {
        const trie = new Trie();
        trie.insertAll(['apple', 'banana', 'cherry']);
        
        const words = trie.getAllWords();
        assertEqual(words.length, 3, 'Should have 3 words');
        assert(words.includes('apple'), 'Should include "apple"');
    });

    it('should find shortest and longest words', () => {
        const trie = new Trie();
        trie.insertAll(['a', 'apple', 'banana', 'cat', 'elephant']);
        
        assertEqual(trie.getShortestWord(), 'a', 'Should find "a" as shortest');
        assertEqual(trie.getLongestWord(), 'elephant', 'Should find "elephant" as longest');
    });

    it('should handle empty trie for shortest/longest', () => {
        const trie = new Trie();
        assertEqual(trie.getShortestWord(), '', 'Empty trie should return empty string');
        assertEqual(trie.getLongestWord(), '', 'Empty trie should return empty string');
    });
});

describe('Trie - Serialization', () => {
    it('should export to JSON', () => {
        const trie = new Trie();
        trie.insertAll(['apple', 'banana']);
        
        const json = trie.toJSON() as any;
        assertEqual(json.size, 2, 'JSON should have size 2');
        assert(json.words.includes('apple'), 'JSON should include "apple"');
        assert(json.words.includes('banana'), 'JSON should include "banana"');
    });

    it('should create from JSON', () => {
        const trie = Trie.fromJSON({ words: ['hello', 'world'] });
        
        assert(trie.search('hello'), 'Should find "hello"');
        assert(trie.search('world'), 'Should find "world"');
        assertEqual(trie.size(), 2, 'Should have size 2');
    });

    it('should create from array', () => {
        const trie = Trie.fromArray(['one', 'two', 'three']);
        
        assert(trie.search('one'), 'Should find "one"');
        assert(trie.search('two'), 'Should find "two"');
        assertEqual(trie.size(), 3, 'Should have size 3');
    });
});

// ==================== RadixTree Tests ====================

describe('RadixTree - Basic Operations', () => {
    it('should insert and search words', () => {
        const radix = new RadixTree();
        radix.insert('apple');
        radix.insert('app');
        radix.insert('application');
        
        assert(radix.search('apple'), 'Should find "apple"');
        assert(radix.search('app'), 'Should find "app"');
        assert(radix.search('application'), 'Should find "application"');
        assert(!radix.search('appx'), 'Should not find "appx"');
    });

    it('should handle startsWith', () => {
        const radix = new RadixTree();
        radix.insert('apple');
        
        assert(radix.startsWith('app'), 'Should find prefix "app"');
        assert(radix.startsWith('apple'), 'Should find prefix "apple"');
        assert(!radix.startsWith('orange'), 'Should not find prefix "orange"');
    });

    it('should autocomplete words', () => {
        const radix = new RadixTree();
        radix.insert('apple');
        radix.insert('app');
        radix.insert('application');
        radix.insert('banana');
        
        const results = radix.autocomplete('app');
        assertEqual(results.length, 3, 'Should find 3 words with prefix "app"');
    });

    it('should track size correctly', () => {
        const radix = new RadixTree();
        assertEqual(radix.size(), 0, 'Initial size should be 0');
        
        radix.insert('one');
        radix.insert('two');
        radix.insert('three');
        assertEqual(radix.size(), 3, 'Size should be 3');
    });
});

// ==================== TrieUtils Tests ====================

describe('TrieUtils - Helper Functions', () => {
    it('should create trie from text', () => {
        const text = 'hello world hello universe';
        const trie = TrieUtils.fromText(text);
        
        assert(trie.search('hello'), 'Should find "hello"');
        assert(trie.search('world'), 'Should find "world"');
        assertEqual(trie.getFrequency('hello'), 2, 'Should count "hello" frequency');
    });

    it('should find words within edit distance', () => {
        const trie = new Trie();
        trie.insertAll(['hello', 'hallo', 'help', 'held', 'cat']);
        
        const results = TrieUtils.findWithinEditDistance(trie, 'hello', 1);
        assert(results.includes('hello'), 'Should include "hello"');
        assert(results.includes('hallo'), 'Should include "hallo"');
        assert(results.includes('help'), 'Should include "help"');
        assert(!results.includes('cat'), 'Should not include "cat"');
    });

    it('should find longest common prefix', () => {
        const trie = new Trie();
        trie.insertAll(['apple', 'app', 'application', 'apply']);
        
        const lcp = TrieUtils.longestCommonPrefix(trie);
        assertEqual(lcp, 'app', 'Longest common prefix should be "app"');
    });

    it('should merge tries', () => {
        const trie1 = new Trie();
        trie1.insertAll(['apple', 'banana']);
        
        const trie2 = new Trie();
        trie2.insertAll(['cherry', 'date']);
        
        const merged = TrieUtils.merge(trie1, trie2);
        assert(merged.search('apple'), 'Should find "apple"');
        assert(merged.search('cherry'), 'Should find "cherry"');
        assertEqual(merged.size(), 4, 'Merged size should be 4');
    });

    it('should calculate total characters', () => {
        const trie = new Trie();
        trie.insertAll(['a', 'ab', 'abc']);
        
        const total = TrieUtils.totalCharacters(trie);
        assertEqual(total, 6, 'Total characters should be 1+2+3=6');
    });

    it('should calculate compression ratio', () => {
        const trie = new Trie();
        trie.insertAll(['apple', 'app', 'application']);
        
        const ratio = TrieUtils.compressionRatio(trie);
        assert(ratio > 1, 'Compression ratio should be greater than 1 for shared prefixes');
    });
});

// ==================== Edge Cases ====================

describe('Edge Cases', () => {
    it('should handle special characters', () => {
        const trie = new Trie();
        trie.insert('hello-world');
        trie.insert('test_case');
        trie.insert('dot.separated');
        
        assert(trie.search('hello-world'), 'Should find "hello-world"');
        assert(trie.search('test_case'), 'Should find "test_case"');
        assert(trie.search('dot.separated'), 'Should find "dot.separated"');
    });

    it('should handle unicode characters', () => {
        const trie = new Trie();
        trie.insert('你好');
        trie.insert('世界');
        trie.insert('こんにちは');
        
        assert(trie.search('你好'), 'Should find Chinese characters');
        assert(trie.search('こんにちは'), 'Should find Japanese characters');
    });

    it('should handle very long words', () => {
        const trie = new Trie();
        const longWord = 'a'.repeat(1000);
        trie.insert(longWord);
        
        assert(trie.search(longWord), 'Should find very long word');
        assert(trie.startsWith('a'.repeat(500)), 'Should find prefix of long word');
    });

    it('should handle single character words', () => {
        const trie = new Trie();
        trie.insert('a');
        trie.insert('b');
        trie.insert('c');
        
        assertEqual(trie.size(), 3, 'Should have 3 single-character words');
        assert(trie.search('a'), 'Should find "a"');
        assert(trie.search('b'), 'Should find "b"');
        assert(trie.search('c'), 'Should find "c"');
    });

    it('should handle clear operation', () => {
        const trie = new Trie();
        trie.insertAll(['one', 'two', 'three']);
        trie.clear();
        
        assert(trie.isEmpty(), 'Should be empty after clear');
        assertEqual(trie.size(), 0, 'Size should be 0 after clear');
        assertEqual(trie.nodeCount(), 1, 'Should have only root node after clear');
    });

    it('should handle chaining', () => {
        const trie = new Trie()
            .insert('apple')
            .insert('banana')
            .insert('cherry');
        
        assertEqual(trie.size(), 3, 'Should have 3 words from chaining');
    });
});

// ==================== Performance Tests ====================

describe('Performance', () => {
    it('should handle large number of words efficiently', () => {
        const trie = new Trie();
        const wordCount = 10000;
        
        const startInsert = Date.now();
        for (let i = 0; i < wordCount; i++) {
            trie.insert(`word${i}`);
        }
        const insertTime = Date.now() - startInsert;
        
        assertEqual(trie.size(), wordCount, `Should have ${wordCount} words`);
        console.log(`    ⏱️  Insert ${wordCount} words: ${insertTime}ms`);
        
        const startSearch = Date.now();
        for (let i = 0; i < 1000; i++) {
            trie.search(`word${Math.floor(Math.random() * wordCount)}`);
        }
        const searchTime = Date.now() - startSearch;
        console.log(`    ⏱️  Search 1000 times: ${searchTime}ms`);
        
        const startAutocomplete = Date.now();
        trie.autocomplete('word1', 10);
        const autocompleteTime = Date.now() - startAutocomplete;
        console.log(`    ⏱️  Autocomplete: ${autocompleteTime}ms`);
    });

    it('should handle deep tries efficiently', () => {
        const trie = new Trie();
        const depth = 1000;
        const deepWord = 'a'.repeat(depth);
        
        const startInsert = Date.now();
        trie.insert(deepWord);
        const insertTime = Date.now() - startInsert;
        console.log(`    ⏱️  Insert word of depth ${depth}: ${insertTime}ms`);
        
        const startSearch = Date.now();
        trie.search(deepWord);
        const searchTime = Date.now() - startSearch;
        console.log(`    ⏱️  Search deep word: ${searchTime}ms`);
        
        assert(trie.search(deepWord), 'Should find deep word');
    });
});

// ==================== Summary ====================

console.log('\n' + '='.repeat(50));
console.log('📊 Test Summary');
console.log('='.repeat(50));
console.log('All tests passed! ✅');
console.log('\nTrie Utilities module is ready for use.');