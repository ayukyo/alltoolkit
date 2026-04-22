/**
 * Trie Utilities - TypeScript
 * 
 * A comprehensive Trie (Prefix Tree) data structure utility module providing
 * efficient string storage, prefix searching, and autocomplete functionality.
 * Zero external dependencies.
 * 
 * Features:
 * - Insert, search, and delete operations
 * - Prefix-based search and autocomplete
 * - Pattern matching with wildcards
 * - Longest prefix matching
 * - Word frequency tracking
 * - Memory-efficient implementation
 * 
 * @module trie_utils
 * @version 1.0.0
 * @license MIT
 */

/**
 * Trie node structure
 */
class TrieNode {
    children: Map<string, TrieNode>;
    isEndOfWord: boolean;
    frequency: number;

    constructor() {
        this.children = new Map<string, TrieNode>();
        this.isEndOfWord = false;
        this.frequency = 0;
    }
}

/**
 * Search result with word and frequency
 */
export interface TrieSearchResult {
    word: string;
    frequency: number;
}

/**
 * Trie (Prefix Tree) implementation
 * 
 * A tree-like data structure used for efficient retrieval of keys in a dataset.
 * Optimized for prefix-based searches and autocomplete systems.
 * 
 * Time Complexity:
 * - Insert: O(m) where m is the length of the word
 * - Search: O(m)
 * - Delete: O(m)
 * - Prefix Search: O(m + k) where k is total characters in results
 * 
 * Space Complexity: O(n * m) where n is number of words, m is average length
 * 
 * @example
 * ```typescript
 * const trie = new Trie();
 * trie.insert("apple");
 * trie.insert("app");
 * trie.insert("application");
 * 
 * console.log(trie.search("apple")); // true
 * console.log(trie.startsWith("app")); // true
 * console.log(trie.autocomplete("app")); // ["app", "apple", "application"]
 * ```
 */
export class Trie {
    private root: TrieNode;
    private _size: number;
    private _totalNodes: number;

    constructor() {
        this.root = new TrieNode();
        this._size = 0;
        this._totalNodes = 1; // root node
    }

    /**
     * Insert a word into the trie
     * @param word - The word to insert
     * @param frequency - Optional frequency count (default: 1, increments if exists)
     * @returns The trie instance for chaining
     * @timeComplexity O(m) where m is word length
     */
    insert(word: string, frequency: number = 1): Trie {
        if (!word) return this;

        let node = this.root;
        for (const char of word) {
            if (!node.children.has(char)) {
                node.children.set(char, new TrieNode());
                this._totalNodes++;
            }
            node = node.children.get(char)!;
        }

        if (!node.isEndOfWord) {
            this._size++;
        }
        node.isEndOfWord = true;
        node.frequency += frequency;

        return this;
    }

    /**
     * Insert multiple words into the trie
     * @param words - Array of words to insert
     * @returns The trie instance for chaining
     * @timeComplexity O(n * m) where n is number of words
     */
    insertAll(words: string[]): Trie {
        for (const word of words) {
            this.insert(word);
        }
        return this;
    }

    /**
     * Search for exact word in the trie
     * @param word - The word to search for
     * @returns true if the word exists
     * @timeComplexity O(m)
     */
    search(word: string): boolean {
        if (!word) return false;

        const node = this.findNode(word);
        return node !== null && node.isEndOfWord;
    }

    /**
     * Check if any word in the trie starts with the given prefix
     * @param prefix - The prefix to check
     * @returns true if prefix exists
     * @timeComplexity O(m)
     */
    startsWith(prefix: string): boolean {
        if (!prefix) return true;

        return this.findNode(prefix) !== null;
    }

    /**
     * Delete a word from the trie
     * @param word - The word to delete
     * @returns true if the word was found and deleted
     * @timeComplexity O(m)
     */
    delete(word: string): boolean {
        if (!word) return false;
        const result = this.deleteHelper(this.root, word, 0);
        return result !== false; // Return true if word was found
    }

    /**
     * Helper method for recursive deletion
     * Returns 'cleanup' if node can be removed, 'found' if word found but stop cleanup, false if not found
     */
    private deleteHelper(node: TrieNode, word: string, index: number): string | false {
        if (index === word.length) {
            if (!node.isEndOfWord) {
                return false; // Word not found
            }
            node.isEndOfWord = false;
            node.frequency = 0;
            this._size--;
            return node.children.size === 0 ? 'cleanup' : 'found';
        }

        const char = word[index];
        const childNode = node.children.get(char);
        if (!childNode) {
            return false; // Word not found
        }

        const childResult = this.deleteHelper(childNode, word, index + 1);

        if (childResult === false) {
            return false; // Word not found
        }

        if (childResult === 'cleanup') {
            // Child can be removed
            node.children.delete(char);
            this._totalNodes--;
            // Check if this node can also be cleaned up
            if (!node.isEndOfWord && node.children.size === 0) {
                return 'cleanup';
            }
        }

        return 'found'; // Word was found, stop cleanup
    }

    /**
     * Find the node at the end of a prefix
     * @param prefix - The prefix to find
     * @returns The node or null if not found
     */
    private findNode(prefix: string): TrieNode | null {
        let node = this.root;
        for (const char of prefix) {
            if (!node.children.has(char)) {
                return null;
            }
            node = node.children.get(char)!;
        }
        return node;
    }

    /**
     * Get all words with the given prefix (autocomplete)
     * @param prefix - The prefix to search for
     * @param limit - Maximum number of results (default: 10)
     * @returns Array of words with the prefix
     * @timeComplexity O(m + k) where k is total characters in results
     */
    autocomplete(prefix: string, limit: number = 10): string[] {
        const results: string[] = [];
        const startNode = prefix ? this.findNode(prefix) : this.root;

        if (!startNode) return results;

        this.collectWords(startNode, prefix, results, limit);
        return results;
    }

    /**
     * Get all words with the given prefix, sorted by frequency
     * @param prefix - The prefix to search for
     * @param limit - Maximum number of results
     * @returns Array of search results with frequency
     */
    autocompleteByFrequency(prefix: string, limit: number = 10): TrieSearchResult[] {
        const results: TrieSearchResult[] = [];
        const startNode = prefix ? this.findNode(prefix) : this.root;

        if (!startNode) return results;

        this.collectWordsWithFrequency(startNode, prefix, results);
        results.sort((a, b) => b.frequency - a.frequency);

        return results.slice(0, limit);
    }

    /**
     * Recursively collect all words from a node
     */
    private collectWords(
        node: TrieNode,
        prefix: string,
        results: string[],
        limit: number
    ): void {
        if (results.length >= limit) return;

        if (node.isEndOfWord) {
            results.push(prefix);
        }

        for (const [char, child] of node.children) {
            this.collectWords(child, prefix + char, results, limit);
        }
    }

    /**
     * Recursively collect all words with frequency from a node
     */
    private collectWordsWithFrequency(
        node: TrieNode,
        prefix: string,
        results: TrieSearchResult[]
    ): void {
        if (node.isEndOfWord) {
            results.push({ word: prefix, frequency: node.frequency });
        }

        for (const [char, child] of node.children) {
            this.collectWordsWithFrequency(child, prefix + char, results);
        }
    }

    /**
     * Get all words in the trie
     * @returns Array of all words
     * @timeComplexity O(n * m) where n is number of words
     */
    getAllWords(): string[] {
        const results: string[] = [];
        this.collectWords(this.root, '', results, Infinity);
        return results;
    }

    /**
     * Search for words matching a pattern with wildcards
     * @param pattern - Pattern with '.' as wildcard
     * @param limit - Maximum results
     * @returns Array of matching words
     * @timeComplexity O(26^w * m) where w is number of wildcards
     * @example
     * ```typescript
     * trie.insert("cat");
     * trie.insert("car");
     * trie.insert("can");
     * trie.searchPattern("ca."); // ["cat", "car", "can"]
     * ```
     */
    searchPattern(pattern: string, limit: number = 10): string[] {
        const results: string[] = [];
        this.searchPatternHelper(this.root, pattern, 0, '', results, limit);
        return results;
    }

    /**
     * Helper for pattern matching with wildcards
     */
    private searchPatternHelper(
        node: TrieNode,
        pattern: string,
        index: number,
        current: string,
        results: string[],
        limit: number
    ): void {
        if (results.length >= limit) return;

        if (index === pattern.length) {
            if (node.isEndOfWord) {
                results.push(current);
            }
            return;
        }

        const char = pattern[index];

        if (char === '.') {
            // Wildcard: try all children
            for (const [childChar, childNode] of node.children) {
                this.searchPatternHelper(
                    childNode,
                    pattern,
                    index + 1,
                    current + childChar,
                    results,
                    limit
                );
            }
        } else {
            const childNode = node.children.get(char);
            if (childNode) {
                this.searchPatternHelper(
                    childNode,
                    pattern,
                    index + 1,
                    current + char,
                    results,
                    limit
                );
            }
        }
    }

    /**
     * Find the longest word in the trie that is a prefix of the given string
     * @param str - The string to match
     * @returns The longest matching prefix word, or empty string
     * @timeComplexity O(m)
     * @example
     * ```typescript
     * trie.insert("app");
     * trie.insert("apple");
     * trie.longestPrefixMatch("application"); // "apple"
     * ```
     */
    longestPrefixMatch(str: string): string {
        let node = this.root;
        let longestMatch = '';
        let currentPrefix = '';

        for (const char of str) {
            if (!node.children.has(char)) {
                break;
            }
            node = node.children.get(char)!;
            currentPrefix += char;
            if (node.isEndOfWord) {
                longestMatch = currentPrefix;
            }
        }

        return longestMatch;
    }

    /**
     * Get the frequency of a word
     * @param word - The word to check
     * @returns The frequency, or 0 if not found
     * @timeComplexity O(m)
     */
    getFrequency(word: string): number {
        const node = this.findNode(word);
        return node?.isEndOfWord ? node.frequency : 0;
    }

    /**
     * Increment the frequency of a word
     * @param word - The word to increment
     * @param amount - Amount to increment (default: 1)
     * @returns true if word exists
     * @timeComplexity O(m)
     */
    incrementFrequency(word: string, amount: number = 1): boolean {
        const node = this.findNode(word);
        if (node && node.isEndOfWord) {
            node.frequency += amount;
            return true;
        }
        return false;
    }

    /**
     * Count the number of words with the given prefix
     * @param prefix - The prefix to count
     * @returns Number of words with this prefix
     * @timeComplexity O(m + n) where n is number of words under prefix
     */
    countWordsWithPrefix(prefix: string): number {
        const startNode = prefix ? this.findNode(prefix) : this.root;
        if (!startNode) return 0;

        let count = 0;
        this.countWords(startNode, (c) => { count = c; });
        return count;
    }

    /**
     * Helper to count words from a node
     */
    private countWords(node: TrieNode, callback: (count: number) => void): void {
        let count = 0;
        const stack: TrieNode[] = [node];
        while (stack.length > 0) {
            const current = stack.pop()!;
            if (current.isEndOfWord) {
                count++;
            }
            for (const child of current.children.values()) {
                stack.push(child);
            }
        }
        callback(count);
    }

    /**
     * Get the number of words in the trie
     * @returns The word count
     * @timeComplexity O(1)
     */
    size(): number {
        return this._size;
    }

    /**
     * Get the total number of nodes in the trie
     * @returns The node count
     * @timeComplexity O(1)
     */
    nodeCount(): number {
        return this._totalNodes;
    }

    /**
     * Check if the trie is empty
     * @returns true if no words
     * @timeComplexity O(1)
     */
    isEmpty(): boolean {
        return this._size === 0;
    }

    /**
     * Clear all words from the trie
     * @returns The trie instance for chaining
     * @timeComplexity O(1)
     */
    clear(): Trie {
        this.root = new TrieNode();
        this._size = 0;
        this._totalNodes = 1;
        return this;
    }

    /**
     * Get the shortest word in the trie
     * @returns The shortest word, or empty string if trie is empty
     * @timeComplexity O(n * m)
     */
    getShortestWord(): string {
        if (this.isEmpty()) return '';

        const queue: Array<{ node: TrieNode; word: string }> = [
            { node: this.root, word: '' }
        ];

        while (queue.length > 0) {
            const { node, word } = queue.shift()!;
            if (node.isEndOfWord && word.length > 0) {
                return word;
            }
            for (const [char, child] of node.children) {
                queue.push({ node: child, word: word + char });
            }
        }

        return '';
    }

    /**
     * Get the longest word in the trie
     * @returns The longest word, or empty string if trie is empty
     * @timeComplexity O(n * m)
     */
    getLongestWord(): string {
        if (this.isEmpty()) return '';

        let longest = '';
        const stack: Array<{ node: TrieNode; word: string }> = [
            { node: this.root, word: '' }
        ];

        while (stack.length > 0) {
            const { node, word } = stack.pop()!;
            if (node.isEndOfWord && word.length > longest.length) {
                longest = word;
            }
            for (const [char, child] of node.children) {
                stack.push({ node: child, word: word + char });
            }
        }

        return longest;
    }

    /**
     * Export the trie to a JSON-serializable object
     * @returns A serializable representation
     */
    toJSON(): object {
        return {
            type: 'Trie',
            size: this._size,
            nodes: this._totalNodes,
            words: this.getAllWords()
        };
    }

    /**
     * Create a trie from a JSON object
     * @param data - The JSON data
     * @returns A new Trie instance
     */
    static fromJSON(data: { words?: string[] }): Trie {
        const trie = new Trie();
        if (data.words) {
            trie.insertAll(data.words);
        }
        return trie;
    }

    /**
     * Create a trie from an array of words
     * @param words - Array of words
     * @returns A new Trie instance
     */
    static fromArray(words: string[]): Trie {
        const trie = new Trie();
        trie.insertAll(words);
        return trie;
    }
}

/**
 * Compressed Trie (Radix Tree) implementation
 * 
 * A space-optimized version of the trie that compresses chains
 * of single-child nodes into single nodes.
 * 
 * @example
 * ```typescript
 * const radix = new RadixTree();
 * radix.insert("apple");
 * radix.insert("app");
 * radix.insert("application");
 * console.log(radix.autocomplete("app")); // ["app", "apple", "application"]
 * ```
 */
export class RadixTree {
    private root: RadixNode;
    private _size: number;

    constructor() {
        this.root = new RadixNode();
        this._size = 0;
    }

    /**
     * Insert a word into the radix tree
     * @param word - The word to insert
     * @returns The radix tree instance for chaining
     */
    insert(word: string): RadixTree {
        if (!word) return this;

        let node = this.root;
        let i = 0;

        while (i < word.length) {
            let found = false;
            const remaining = word.slice(i);

            for (const [prefix, child] of node.children) {
                const commonPrefix = this.getCommonPrefix(prefix, remaining);

                if (commonPrefix.length > 0) {
                    found = true;

                    if (commonPrefix === prefix) {
                        // Exact match, move to child
                        node = child;
                        i += prefix.length;
                    } else {
                        // Split the node
                        const splitNode = new RadixNode();
                        const suffix1 = prefix.slice(commonPrefix.length);
                        const suffix2 = remaining.slice(commonPrefix.length);

                        node.children.delete(prefix);
                        node.children.set(commonPrefix, splitNode);

                        splitNode.children.set(suffix1, child);
                        if (suffix2) {
                            const newChild = new RadixNode();
                            splitNode.children.set(suffix2, newChild);
                            newChild.isEndOfWord = true;
                            this._size++;
                        } else {
                            splitNode.isEndOfWord = true;
                            this._size++;
                        }

                        return this;
                    }
                    break;
                }
            }

            if (!found) {
                const newNode = new RadixNode();
                newNode.isEndOfWord = true;
                node.children.set(remaining, newNode);
                this._size++;
                return this;
            }
        }

        if (!node.isEndOfWord) {
            node.isEndOfWord = true;
            this._size++;
        }

        return this;
    }

    /**
     * Get common prefix of two strings
     */
    private getCommonPrefix(a: string, b: string): string {
        const minLen = Math.min(a.length, b.length);
        let i = 0;
        while (i < minLen && a[i] === b[i]) {
            i++;
        }
        return a.slice(0, i);
    }

    /**
     * Search for a word in the radix tree
     * @param word - The word to search
     * @returns true if found
     */
    search(word: string): boolean {
        let node = this.root;
        let i = 0;

        while (i < word.length) {
            const remaining = word.slice(i);
            let found = false;

            for (const [prefix, child] of node.children) {
                if (remaining.startsWith(prefix)) {
                    node = child;
                    i += prefix.length;
                    found = true;
                    break;
                }
            }

            if (!found) return false;
        }

        return node.isEndOfWord;
    }

    /**
     * Check if any word starts with prefix
     * @param prefix - The prefix to check
     * @returns true if prefix exists
     */
    startsWith(prefix: string): boolean {
        let node = this.root;
        let i = 0;

        while (i < prefix.length) {
            const remaining = prefix.slice(i);
            let found = false;

            for (const [edge, child] of node.children) {
                if (remaining.startsWith(edge) || edge.startsWith(remaining)) {
                    node = child;
                    i += Math.min(edge.length, remaining.length);
                    found = true;
                    break;
                }
            }

            if (!found) return false;
        }

        return true;
    }

    /**
     * Get all words with the given prefix
     * @param prefix - The prefix
     * @param limit - Maximum results
     * @returns Array of matching words
     */
    autocomplete(prefix: string, limit: number = 10): string[] {
        const results: string[] = [];
        let node = this.root;
        let i = 0;

        // Navigate to prefix node
        while (i < prefix.length) {
            const remaining = prefix.slice(i);
            let found = false;

            for (const [edge, child] of node.children) {
                if (remaining.startsWith(edge)) {
                    node = child;
                    i += edge.length;
                    found = true;
                    break;
                } else if (edge.startsWith(remaining)) {
                    node = child;
                    i = prefix.length;
                    found = true;
                    break;
                }
            }

            if (!found) return results;
        }

        this.collectRadixWords(node, prefix, results, limit);
        return results;
    }

    /**
     * Collect words from radix tree node
     */
    private collectRadixWords(
        node: RadixNode,
        prefix: string,
        results: string[],
        limit: number
    ): void {
        if (results.length >= limit) return;

        if (node.isEndOfWord) {
            results.push(prefix);
        }

        for (const [edge, child] of node.children) {
            this.collectRadixWords(child, prefix + edge, results, limit);
        }
    }

    /**
     * Get the number of words
     */
    size(): number {
        return this._size;
    }

    /**
     * Check if empty
     */
    isEmpty(): boolean {
        return this._size === 0;
    }
}

/**
 * Radix tree node
 */
class RadixNode {
    children: Map<string, RadixNode>;
    isEndOfWord: boolean;

    constructor() {
        this.children = new Map<string, RadixNode>();
        this.isEndOfWord = false;
    }
}

/**
 * Trie Utilities - Static helper functions
 */
export class TrieUtils {
    /**
     * Build a trie from an array of words
     * @param words - Array of words
     * @returns A new Trie instance
     */
    static fromArray(words: string[]): Trie {
        return Trie.fromArray(words);
    }

    /**
     * Build a trie from a text (splits on whitespace)
     * @param text - The text to process
     * @returns A new Trie instance
     */
    static fromText(text: string): Trie {
        const words = text.split(/\s+/).filter(w => w.length > 0);
        return Trie.fromArray(words);
    }

    /**
     * Find all words that are anagrams of the given letters
     * @param trie - The trie to search
     * @param letters - Available letters
     * @returns Array of anagram words
     */
    static findAnagrams(trie: Trie, letters: string): string[] {
        const results: string[] = [];
        const letterCount = new Map<string, number>();
        
        for (const char of letters.toLowerCase()) {
            letterCount.set(char, (letterCount.get(char) || 0) + 1);
        }

        this.anagramHelper(trie, '', letterCount, results);
        return results;
    }

    private static anagramHelper(
        trie: Trie,
        current: string,
        letterCount: Map<string, number>,
        results: string[]
    ): void {
        if (trie.search(current)) {
            results.push(current);
        }

        for (const [char, count] of letterCount) {
            if (count > 0) {
                letterCount.set(char, count - 1);
                this.anagramHelper(
                    trie as any,
                    current + char,
                    letterCount,
                    results
                );
                letterCount.set(char, count);
            }
        }
    }

    /**
     * Find words within edit distance
     * @param trie - The trie to search
     * @param word - The target word
     * @param maxDistance - Maximum edit distance
     * @returns Array of words within edit distance
     */
    static findWithinEditDistance(
        trie: Trie,
        word: string,
        maxDistance: number
    ): string[] {
        const results: string[] = [];
        const allWords = trie.getAllWords();

        for (const w of allWords) {
            if (this.editDistance(word, w) <= maxDistance) {
                results.push(w);
            }
        }

        return results;
    }

    /**
     * Calculate edit distance (Levenshtein distance)
     */
    private static editDistance(a: string, b: string): number {
        const dp: number[][] = Array(a.length + 1)
            .fill(null)
            .map(() => Array(b.length + 1).fill(0));

        for (let i = 0; i <= a.length; i++) dp[i][0] = i;
        for (let j = 0; j <= b.length; j++) dp[0][j] = j;

        for (let i = 1; i <= a.length; i++) {
            for (let j = 1; j <= b.length; j++) {
                if (a[i - 1] === b[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = Math.min(
                        dp[i - 1][j] + 1,      // deletion
                        dp[i][j - 1] + 1,      // insertion
                        dp[i - 1][j - 1] + 1   // substitution
                    );
                }
            }
        }

        return dp[a.length][b.length];
    }

    /**
     * Merge two tries into one
     * @param trie1 - First trie
     * @param trie2 - Second trie
     * @returns A new merged trie
     */
    static merge(trie1: Trie, trie2: Trie): Trie {
        const result = new Trie();
        const words1 = trie1.getAllWords();
        const words2 = trie2.getAllWords();

        result.insertAll(words1);
        result.insertAll(words2);

        return result;
    }

    /**
     * Find the longest common prefix of all words
     * @param trie - The trie to analyze
     * @returns The longest common prefix
     */
    static longestCommonPrefix(trie: Trie): string {
        let prefix = '';
        let node = (trie as any).root;

        while (node.children.size === 1 && !node.isEndOfWord) {
            const [char, child] = Array.from(node.children.entries())[0];
            prefix += char;
            node = child;
        }

        return prefix;
    }

    /**
     * Count total characters stored (sum of word lengths)
     * @param trie - The trie to analyze
     * @returns Total character count
     */
    static totalCharacters(trie: Trie): number {
        const words = trie.getAllWords();
        return words.reduce((sum, word) => sum + word.length, 0);
    }

    /**
     * Calculate compression ratio (characters stored / trie nodes)
     * @param trie - The trie to analyze
     * @returns Compression ratio
     */
    static compressionRatio(trie: Trie): number {
        const totalChars = this.totalCharacters(trie);
        const nodes = trie.nodeCount();
        return totalChars > 0 ? totalChars / nodes : 0;
    }
}

// Default exports
export default {
    Trie,
    RadixTree,
    TrieUtils
};