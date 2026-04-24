/**
 * Trie (Prefix Tree) Utility
 * A tree-like data structure for efficient string retrieval and prefix-based operations.
 * 
 * Features:
 * - Insert, search, delete operations
 * - Prefix search / autocomplete
 * - Word frequency tracking
 * - Pattern matching with wildcards
 * 
 * Time Complexity:
 * - Insert: O(m) where m is the length of the word
 * - Search: O(m)
 * - Delete: O(m)
 * - Prefix search: O(m + n) where n is total characters in results
 * 
 * Space Complexity: O(n * m) where n is number of words, m is average length
 * 
 * Zero external dependencies - pure JavaScript implementation
 */

/**
 * Trie node class
 */
class TrieNode {
    constructor() {
        this.children = {};      // Map of character to TrieNode
        this.isEndOfWord = false; // Marks the end of a complete word
        this.frequency = 0;       // Word frequency counter
        this.data = null;         // Optional associated data
    }
}

/**
 * Trie data structure implementation
 */
class Trie {
    constructor() {
        this.root = new TrieNode();
        this.wordCount = 0;
    }

    /**
     * Insert a word into the trie
     * @param {string} word - The word to insert
     * @param {*} data - Optional data to associate with the word
     * @returns {Trie} Returns this for chaining
     */
    insert(word, data = null) {
        if (!word || typeof word !== 'string') {
            throw new Error('Word must be a non-empty string');
        }

        let node = this.root;
        for (const char of word) {
            if (!node.children[char]) {
                node.children[char] = new TrieNode();
            }
            node = node.children[char];
        }
        
        if (!node.isEndOfWord) {
            this.wordCount++;
        }
        
        node.isEndOfWord = true;
        node.frequency++;
        if (data !== null) {
            node.data = data;
        }
        
        return this;
    }

    /**
     * Search for a word in the trie
     * @param {string} word - The word to search for
     * @returns {boolean} True if the word exists in the trie
     */
    search(word) {
        if (!word || typeof word !== 'string') {
            return false;
        }

        const node = this._findNode(word);
        return node !== null && node.isEndOfWord;
    }

    /**
     * Check if any word in the trie starts with the given prefix
     * @param {string} prefix - The prefix to check
     * @returns {boolean} True if any word has this prefix
     */
    startsWith(prefix) {
        if (!prefix || typeof prefix !== 'string') {
            return false;
        }

        return this._findNode(prefix) !== null;
    }

    /**
     * Delete a word from the trie
     * @param {string} word - The word to delete
     * @returns {boolean} True if the word was deleted
     */
    delete(word) {
        if (!word || typeof word !== 'string') {
            return false;
        }

        const result = { deleted: false };
        this._deleteHelper(this.root, word, 0, result);
        
        if (result.deleted) {
            this.wordCount--;
        }
        
        return result.deleted;
    }

    /**
     * Recursive helper for delete operation
     * @private
     */
    _deleteHelper(node, word, index, result) {
        if (index === word.length) {
            if (node.isEndOfWord) {
                node.isEndOfWord = false;
                node.frequency = 0;
                node.data = null;
                result.deleted = true;
                return Object.keys(node.children).length === 0;
            }
            return false;
        }

        const char = word[index];
        const childNode = node.children[char];
        
        if (!childNode) {
            return false;
        }

        const shouldDeleteChild = this._deleteHelper(childNode, word, index + 1, result);

        if (shouldDeleteChild && !childNode.isEndOfWord) {
            delete node.children[char];
            return Object.keys(node.children).length === 0;
        }

        return false;
    }

    /**
     * Get all words with a given prefix (autocomplete)
     * @param {string} prefix - The prefix to search for
     * @param {number} limit - Maximum number of results (default: 10)
     * @returns {Array<{word: string, frequency: number, data: *}>}
     */
    autocomplete(prefix, limit = 10) {
        if (!prefix || typeof prefix !== 'string') {
            return [];
        }

        const node = this._findNode(prefix);
        if (!node) {
            return [];
        }

        const results = [];
        this._collectWords(node, prefix, results, limit);
        
        // Sort by frequency (descending)
        results.sort((a, b) => b.frequency - a.frequency);
        
        return results.slice(0, limit);
    }

    /**
     * Collect all words from a given node
     * @private
     */
    _collectWords(node, prefix, results, limit) {
        if (results.length >= limit) {
            return;
        }

        if (node.isEndOfWord) {
            results.push({
                word: prefix,
                frequency: node.frequency,
                data: node.data
            });
        }

        for (const char of Object.keys(node.children).sort()) {
            this._collectWords(node.children[char], prefix + char, results, limit);
        }
    }

    /**
     * Find the node at the end of a given prefix
     * @private
     */
    _findNode(prefix) {
        let node = this.root;
        for (const char of prefix) {
            if (!node.children[char]) {
                return null;
            }
            node = node.children[char];
        }
        return node;
    }

    /**
     * Get all words in the trie
     * @param {number} limit - Maximum number of results
     * @returns {Array<{word: string, frequency: number, data: *}>}
     */
    getAllWords(limit = Infinity) {
        const results = [];
        this._collectWords(this.root, '', results, limit);
        return results;
    }

    /**
     * Search for words matching a pattern with wildcards
     * @param {string} pattern - Pattern with '?' as wildcard (matches any single char)
     * @param {number} limit - Maximum number of results
     * @returns {Array<{word: string, frequency: number, data: *}>}
     */
    searchPattern(pattern, limit = 10) {
        if (!pattern || typeof pattern !== 'string') {
            return [];
        }

        const results = [];
        this._searchPatternHelper(this.root, pattern, 0, '', results, limit);
        results.sort((a, b) => b.frequency - a.frequency);
        return results.slice(0, limit);
    }

    /**
     * Recursive helper for pattern search
     * @private
     */
    _searchPatternHelper(node, pattern, index, currentWord, results, limit) {
        if (results.length >= limit) {
            return;
        }

        if (index === pattern.length) {
            if (node.isEndOfWord) {
                results.push({
                    word: currentWord,
                    frequency: node.frequency,
                    data: node.data
                });
            }
            return;
        }

        const char = pattern[index];
        
        if (char === '?') {
            // Wildcard: try all children
            for (const childChar of Object.keys(node.children)) {
                this._searchPatternHelper(
                    node.children[childChar],
                    pattern,
                    index + 1,
                    currentWord + childChar,
                    results,
                    limit
                );
            }
        } else {
            // Exact match
            const childNode = node.children[char];
            if (childNode) {
                this._searchPatternHelper(
                    childNode,
                    pattern,
                    index + 1,
                    currentWord + char,
                    results,
                    limit
                );
            }
        }
    }

    /**
     * Get the longest common prefix of all words in the trie
     * @returns {string}
     */
    longestCommonPrefix() {
        let prefix = '';
        let node = this.root;

        while (node) {
            const children = Object.keys(node.children);
            if (children.length !== 1 || node.isEndOfWord) {
                break;
            }
            prefix += children[0];
            node = node.children[children[0]];
        }

        return prefix;
    }

    /**
     * Count words with a given prefix
     * @param {string} prefix - The prefix
     * @returns {number} Number of words with this prefix
     */
    countWithPrefix(prefix) {
        if (!prefix || typeof prefix !== 'string') {
            return 0;
        }

        const node = this._findNode(prefix);
        if (!node) {
            return 0;
        }

        return this._countWords(node);
    }

    /**
     * Count all words from a given node
     * @private
     */
    _countWords(node) {
        let count = node.isEndOfWord ? 1 : 0;
        for (const child of Object.values(node.children)) {
            count += this._countWords(child);
        }
        return count;
    }

    /**
     * Clear the trie
     */
    clear() {
        this.root = new TrieNode();
        this.wordCount = 0;
    }

    /**
     * Get the total number of words in the trie
     * @returns {number}
     */
    size() {
        return this.wordCount;
    }

    /**
     * Check if the trie is empty
     * @returns {boolean}
     */
    isEmpty() {
        return this.wordCount === 0;
    }

    /**
     * Get word data if it exists
     * @param {string} word - The word to look up
     * @returns {*|null} The associated data or null
     */
    getWordData(word) {
        if (!word || typeof word !== 'string') {
            return null;
        }

        const node = this._findNode(word);
        if (node && node.isEndOfWord) {
            return node.data;
        }
        return null;
    }

    /**
     * Update data associated with a word
     * @param {string} word - The word to update
     * @param {*} data - New data to associate
     * @returns {boolean} True if word was found and updated
     */
    updateWordData(word, data) {
        if (!word || typeof word !== 'string') {
            return false;
        }

        const node = this._findNode(word);
        if (node && node.isEndOfWord) {
            node.data = data;
            return true;
        }
        return false;
    }

    /**
     * Export trie to JSON format
     * @returns {Object}
     */
    toJSON() {
        return {
            wordCount: this.wordCount,
            root: this._nodeToJSON(this.root)
        };
    }

    /**
     * Convert node to JSON
     * @private
     */
    _nodeToJSON(node) {
        const json = {
            isEndOfWord: node.isEndOfWord,
            frequency: node.frequency
        };
        
        if (node.data !== null) {
            json.data = node.data;
        }
        
        if (Object.keys(node.children).length > 0) {
            json.children = {};
            for (const [char, child] of Object.entries(node.children)) {
                json.children[char] = this._nodeToJSON(child);
            }
        }
        
        return json;
    }

    /**
     * Import trie from JSON format
     * @param {Object} json - JSON representation of trie
     * @returns {Trie} Returns this for chaining
     */
    fromJSON(json) {
        this.clear();
        this.wordCount = json.wordCount;
        this._nodeFromJSON(this.root, json.root);
        return this;
    }

    /**
     * Convert JSON to node
     * @private
     */
    _nodeFromJSON(node, json) {
        node.isEndOfWord = json.isEndOfWord;
        node.frequency = json.frequency;
        node.data = json.data || null;
        
        if (json.children) {
            for (const [char, childJson] of Object.entries(json.children)) {
                node.children[char] = new TrieNode();
                this._nodeFromJSON(node.children[char], childJson);
            }
        }
    }
}

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Trie, TrieNode };
}

if (typeof window !== 'undefined') {
    window.Trie = Trie;
    window.TrieNode = TrieNode;
}