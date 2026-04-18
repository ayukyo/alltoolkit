// Package trie_utils provides a generic Trie (prefix tree) implementation.
// Trie is efficient for prefix-based operations like autocomplete, spell checking,
// and dictionary lookups.
//
// Features:
//   - Generic key type support (using runes for Unicode)
//   - Insert, Search, Delete operations
//   - Prefix search (autocomplete)
//   - Pattern matching with wildcards
//   - Word frequency tracking
//   - Longest common prefix finding
//   - Zero external dependencies
//
// Example:
//
//	trie := trie_utils.NewTrie()
//	trie.Insert("hello", 1)
//	trie.Insert("help", 2)
//	words := trie.WordsWithPrefix("hel") // ["hello", "help"]
package trie_utils

import (
	"sort"
	"sync"
)

// TrieNode represents a single node in the trie
type TrieNode struct {
	children map[rune]*TrieNode
	isEnd    bool
	value    interface{}
	count    int // Frequency/count of words ending at this node
}

// Trie is the main trie structure
type Trie struct {
	root  *TrieNode
	size  int // Total number of words
	mutex sync.RWMutex
}

// NewTrie creates and returns a new empty trie
func NewTrie() *Trie {
	return &Trie{
		root: &TrieNode{
			children: make(map[rune]*TrieNode),
		},
		size: 0,
	}
}

// Insert adds a word to the trie with an optional value
// Returns true if the word was newly inserted, false if it already existed
func (t *Trie) Insert(word string, value interface{}) bool {
	t.mutex.Lock()
	defer t.mutex.Unlock()

	if word == "" {
		return false
	}

	node := t.root
	for _, ch := range word {
		if node.children[ch] == nil {
			node.children[ch] = &TrieNode{
				children: make(map[rune]*TrieNode),
			}
		}
		node = node.children[ch]
	}

	isNew := !node.isEnd
	if isNew {
		t.size++
	}
	node.isEnd = true
	node.value = value
	node.count++
	return isNew
}

// InsertWord adds a word without a value
func (t *Trie) InsertWord(word string) bool {
	return t.Insert(word, nil)
}

// Search checks if a word exists in the trie
func (t *Trie) Search(word string) bool {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	node := t.findNode(word)
	return node != nil && node.isEnd
}

// SearchWithValue checks if a word exists and returns its value
func (t *Trie) SearchWithValue(word string) (interface{}, bool) {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	node := t.findNode(word)
	if node != nil && node.isEnd {
		return node.value, true
	}
	return nil, false
}

// GetCount returns the count/frequency of a word
func (t *Trie) GetCount(word string) int {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	node := t.findNode(word)
	if node != nil && node.isEnd {
		return node.count
	}
	return 0
}

// StartsWith checks if there is any word in the trie that starts with the prefix
func (t *Trie) StartsWith(prefix string) bool {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	return t.findNode(prefix) != nil
}

// Delete removes a word from the trie
// Returns true if the word was found and deleted
func (t *Trie) Delete(word string) bool {
	t.mutex.Lock()
	defer t.mutex.Unlock()

	if word == "" {
		return false
	}

	path := make([]*TrieNode, 0, len(word)+1)
	path = append(path, t.root)

	node := t.root
	for _, ch := range word {
		if node.children[ch] == nil {
			return false
		}
		node = node.children[ch]
		path = append(path, node)
	}

	if !node.isEnd {
		return false
	}

	node.isEnd = false
	node.value = nil
	node.count = 0
	t.size--

	// Clean up unused nodes
	for i := len(path) - 1; i > 0; i-- {
		currentNode := path[i]
		if currentNode.isEnd || len(currentNode.children) > 0 {
			break
		}
		parentNode := path[i-1]
		ch := []rune(word)[i-1]
		delete(parentNode.children, ch)
	}

	return true
}

// WordsWithPrefix returns all words that start with the given prefix
func (t *Trie) WordsWithPrefix(prefix string) []string {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	var results []string
	startNode := t.findNode(prefix)
	if startNode == nil {
		return results
	}

	t.collectWords(startNode, prefix, &results)
	return results
}

// WordsWithPrefixLimit returns at most n words that start with the given prefix
func (t *Trie) WordsWithPrefixLimit(prefix string, limit int) []string {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	var results []string
	startNode := t.findNode(prefix)
	if startNode == nil {
		return results
	}

	t.collectWordsLimit(startNode, prefix, &results, limit)
	return results
}

// AutoComplete provides autocomplete suggestions for a prefix
// Returns up to 'limit' suggestions
func (t *Trie) AutoComplete(prefix string, limit int) []string {
	if limit <= 0 {
		limit = 10
	}
	return t.WordsWithPrefixLimit(prefix, limit)
}

// LongestCommonPrefix finds the longest common prefix among all words in the trie
func (t *Trie) LongestCommonPrefix() string {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	if t.size == 0 {
		return ""
	}

	var prefix []rune
	node := t.root

	for len(node.children) == 1 && !node.isEnd {
		for ch, child := range node.children {
			prefix = append(prefix, ch)
			node = child
			break
		}
	}

	return string(prefix)
}

// AllWords returns all words in the trie
func (t *Trie) AllWords() []string {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	var results []string
	t.collectWords(t.root, "", &results)
	return results
}

// Size returns the number of words in the trie
func (t *Trie) Size() int {
	t.mutex.RLock()
	defer t.mutex.RUnlock()
	return t.size
}

// Clear removes all words from the trie
func (t *Trie) Clear() {
	t.mutex.Lock()
	defer t.mutex.Unlock()

	t.root = &TrieNode{
		children: make(map[rune]*TrieNode),
	}
	t.size = 0
}

// PatternMatch finds all words matching a pattern
// '?' matches any single character
// '*' matches zero or more characters
func (t *Trie) PatternMatch(pattern string) []string {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	var results []string
	t.matchPattern(t.root, "", pattern, &results)
	return results
}

// MinPrefix finds the shortest unique prefix for a given word
// Returns the word itself if it's not in the trie
func (t *Trie) MinPrefix(word string) string {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	node := t.root
	for i, ch := range word {
		if len(node.children) > 1 || node.isEnd {
			return word[:i+1]
		}
		if node.children[ch] == nil {
			return word
		}
		node = node.children[ch]
	}
	return word
}

// GetWordsByFrequency returns words sorted by frequency (descending)
func (t *Trie) GetWordsByFrequency() []WordFrequency {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	var wf []WordFrequency
	t.collectWordsWithFrequency(t.root, "", &wf)
	sort.Slice(wf, func(i, j int) bool {
		return wf[i].Count > wf[j].Count
	})
	return wf
}

// WordFrequency represents a word and its frequency
type WordFrequency struct {
	Word  string
	Count int
}

// ContainsAny checks if the trie contains any word that is a prefix of the given string
func (t *Trie) ContainsAnyPrefixOf(s string) bool {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	node := t.root
	for _, ch := range s {
		if node.isEnd {
			return true
		}
		if node.children[ch] == nil {
			return false
		}
		node = node.children[ch]
	}
	return node.isEnd
}

// LongestPrefixOf finds the longest word in the trie that is a prefix of s
func (t *Trie) LongestPrefixOf(s string) string {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	var longest string
	node := t.root

	for i, ch := range s {
		if node.children[ch] == nil {
			break
		}
		node = node.children[ch]
		if node.isEnd {
			longest = s[:i+1]
		}
	}

	return longest
}

// Helper functions

// findNode navigates to the node at the end of the given prefix
func (t *Trie) findNode(prefix string) *TrieNode {
	node := t.root
	for _, ch := range prefix {
		if node.children[ch] == nil {
			return nil
		}
		node = node.children[ch]
	}
	return node
}

// collectWords collects all words from a node recursively
func (t *Trie) collectWords(node *TrieNode, prefix string, results *[]string) {
	if node.isEnd {
		*results = append(*results, prefix)
	}
	for ch, child := range node.children {
		t.collectWords(child, prefix+string(ch), results)
	}
}

// collectWordsLimit collects words up to a limit
func (t *Trie) collectWordsLimit(node *TrieNode, prefix string, results *[]string, limit int) {
	if len(*results) >= limit {
		return
	}
	if node.isEnd {
		*results = append(*results, prefix)
	}
	for ch, child := range node.children {
		if len(*results) >= limit {
			return
		}
		t.collectWordsLimit(child, prefix+string(ch), results, limit)
	}
}

// collectWordsWithFrequency collects words with their frequencies
func (t *Trie) collectWordsWithFrequency(node *TrieNode, prefix string, wf *[]WordFrequency) {
	if node.isEnd {
		*wf = append(*wf, WordFrequency{Word: prefix, Count: node.count})
	}
	for ch, child := range node.children {
		t.collectWordsWithFrequency(child, prefix+string(ch), wf)
	}
}

// matchPattern implements pattern matching with wildcards
func (t *Trie) matchPattern(node *TrieNode, current string, pattern string, results *[]string) {
	if len(pattern) == 0 {
		if node.isEnd {
			*results = append(*results, current)
		}
		return
	}

	ch := rune(pattern[0])
	remaining := pattern[1:]

	switch ch {
	case '?':
		// Match any single character
		for c, child := range node.children {
			t.matchPattern(child, current+string(c), remaining, results)
		}
	case '*':
		// Match zero characters
		t.matchPattern(node, current, remaining, results)
		// Match one or more characters
		for c, child := range node.children {
			t.matchPattern(child, current+string(c), pattern, results)
		}
	default:
		if child, ok := node.children[ch]; ok {
			t.matchPattern(child, current+string(ch), remaining, results)
		}
	}
}

// BatchInsert inserts multiple words at once
func (t *Trie) BatchInsert(words []string) int {
	count := 0
	for _, word := range words {
		if t.InsertWord(word) {
			count++
		}
	}
	return count
}

// BatchInsertWithValues inserts multiple words with values
func (t *Trie) BatchInsertWithValues(pairs map[string]interface{}) int {
	count := 0
	for word, value := range pairs {
		if t.Insert(word, value) {
			count++
		}
	}
	return count
}

// ToMap converts the trie to a map of words to values
func (t *Trie) ToMap() map[string]interface{} {
	t.mutex.RLock()
	defer t.mutex.RUnlock()

	result := make(map[string]interface{})
	t.collectWordsToMap(t.root, "", result)
	return result
}

func (t *Trie) collectWordsToMap(node *TrieNode, prefix string, result map[string]interface{}) {
	if node.isEnd {
		result[prefix] = node.value
	}
	for ch, child := range node.children {
		t.collectWordsToMap(child, prefix+string(ch), result)
	}
}