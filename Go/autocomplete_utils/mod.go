// Package autocomplete provides a Trie-based autocomplete engine.
//
// # Features
//
//   - Fast prefix-based word autocomplete using Trie data structure
//   - Case-sensitive and case-insensitive search modes
//   - Word frequency tracking for smarter suggestions
//   - Configurable suggestion limits
//   - Bulk word insertion
//   - Thread-unsafe, high-performance core implementation
//
// # Zero External Dependencies
//
// This package uses only Go standard library.
package autocomplete

import (
	"strings"
	"sort"
)

// TrieNode represents a node in the Trie.
type TrieNode struct {
	children  map[rune]*TrieNode
	isWordEnd bool
	frequency int
}

// NewTrieNode creates a new TrieNode.
func NewTrieNode() *TrieNode {
	return &TrieNode{
		children: make(map[rune]*TrieNode),
		isWordEnd: false,
		frequency: 0,
	}
}

// Trie is the core Trie data structure.
type Trie struct {
	root          *TrieNode
	caseSensitive bool
	totalWords    int
}

// New creates a new case-sensitive Trie.
func New() *Trie {
	return &Trie{
		root:          NewTrieNode(),
		caseSensitive: true,
		totalWords:    0,
	}
}

// NewCaseInsensitive creates a new case-insensitive Trie.
func NewCaseInsensitive() *Trie {
	return &Trie{
		root:          NewTrieNode(),
		caseSensitive: false,
		totalWords:    0,
	}
}

// Insert adds a word to the Trie.
func (t *Trie) Insert(word string) {
	key := word
	if !t.caseSensitive {
		key = strings.ToLower(key)
	}

	node := t.root
	for _, ch := range key {
		if _, exists := node.children[ch]; !exists {
			node.children[ch] = NewTrieNode()
		}
		node = node.children[ch]
	}
	if !node.isWordEnd {
		t.totalWords++
		node.isWordEnd = true
	}
	node.frequency++
}

// InsertBatch adds multiple words to the Trie.
func (t *Trie) InsertBatch(words []string) {
	for _, word := range words {
		t.Insert(word)
	}
}

// Contains checks if a word exists in the Trie.
func (t *Trie) Contains(word string) bool {
	key := word
	if !t.caseSensitive {
		key = strings.ToLower(key)
	}

	node := t.root
	for _, ch := range key {
		if _, exists := node.children[ch]; !exists {
			return false
		}
		node = node.children[ch]
	}
	return node.isWordEnd
}

// suggestionResult holds a suggestion with its score for ranking.
type suggestionResult struct {
	word      string
	frequency int
}

// Complete returns autocomplete suggestions for the given prefix.
// Results are sorted by frequency (most frequent first) and limited by limit.
func (t *Trie) Complete(prefix string, limit int) []string {
	if limit <= 0 {
		limit = 10
	}

	key := prefix
	if !t.caseSensitive {
		key = strings.ToLower(key)
	}

	// Navigate to the prefix node
	node := t.root
	for _, ch := range key {
		if _, exists := node.children[ch]; !exists {
			return []string{}
		}
		node = node.children[ch]
	}

	// Collect all words with this prefix
	var results []suggestionResult
	t.collectWords(node, prefix, &results)

	// Sort by frequency descending
	sort.Slice(results, func(i, j int) bool {
		if results[i].frequency != results[j].frequency {
			return results[i].frequency > results[j].frequency
		}
		return results[i].word < results[j].word
	})

	// Limit results
	if len(results) > limit {
		results = results[:limit]
	}

	// Extract words
	words := make([]string, len(results))
	for i, r := range results {
		words[i] = r.word
	}
	return words
}

// collectWords recursively collects all words from a node.
func (t *Trie) collectWords(node *TrieNode, prefix string, results *[]suggestionResult) {
	if node.isWordEnd {
		*results = append(*results, suggestionResult{
			word:      prefix,
			frequency: node.frequency,
		})
	}

	for ch, child := range node.children {
		t.collectWords(child, prefix+string(ch), results)
	}
}

// PrefixExists checks if any word with the given prefix exists.
func (t *Trie) PrefixExists(prefix string) bool {
	key := prefix
	if !t.caseSensitive {
		key = strings.ToLower(key)
	}

	node := t.root
	for _, ch := range key {
		if _, exists := node.children[ch]; !exists {
			return false
		}
		node = node.children[ch]
	}
	return true
}

// Remove deletes a word from the Trie.
func (t *Trie) Remove(word string) bool {
	key := word
	if !t.caseSensitive {
		key = strings.ToLower(key)
	}

	var path []*TrieNode
	node := t.root
	for _, ch := range key {
		if _, exists := node.children[ch]; !exists {
			return false
		}
		path = append(path, node)
		node = node.children[ch]
	}

	if !node.isWordEnd {
		return false
	}

	node.isWordEnd = false
	t.totalWords--

	// Optionally clean up unused branches (not strictly necessary)
	_ = path

	return true
}

// WordCount returns the number of unique words in the Trie.
func (t *Trie) WordCount() int {
	return t.totalWords
}

// Clear removes all words from the Trie.
func (t *Trie) Clear() {
	t.root = NewTrieNode()
	t.totalWords = 0
}

// GetFrequency returns the frequency of a word.
func (t *Trie) GetFrequency(word string) int {
	key := word
	if !t.caseSensitive {
		key = strings.ToLower(key)
	}

	node := t.root
	for _, ch := range key {
		if _, exists := node.children[ch]; !exists {
			return 0
		}
		node = node.children[ch]
	}
	if !node.isWordEnd {
		return 0
	}
	return node.frequency
}

// SuggestionItem represents a suggestion with metadata.
type SuggestionItem struct {
	Word      string
	Frequency int
}

// CompleteWithDetails returns suggestions with frequency information.
func (t *Trie) CompleteWithDetails(prefix string, limit int) []SuggestionItem {
	if limit <= 0 {
		limit = 10
	}

	key := prefix
	if !t.caseSensitive {
		key = strings.ToLower(key)
	}

	node := t.root
	for _, ch := range key {
		if _, exists := node.children[ch]; !exists {
			return []SuggestionItem{}
		}
		node = node.children[ch]
	}

	var results []SuggestionItem
	t.collectWordsWithDetails(node, prefix, &results)

	sort.Slice(results, func(i, j int) bool {
		if results[i].Frequency != results[j].Frequency {
			return results[i].Frequency > results[j].Frequency
		}
		return results[i].Word < results[j].Word
	})

	if len(results) > limit {
		results = results[:limit]
	}

	return results
}

func (t *Trie) collectWordsWithDetails(node *TrieNode, prefix string, results *[]SuggestionItem) {
	if node.isWordEnd {
		*results = append(*results, SuggestionItem{
			Word:      prefix,
			Frequency: node.frequency,
		})
	}

	for ch, child := range node.children {
		t.collectWordsWithDetails(child, prefix+string(ch), results)
	}
}