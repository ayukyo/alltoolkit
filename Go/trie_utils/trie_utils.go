// Package trie_utils implements a Trie (prefix tree) data structure.
//
// A Trie is an ordered tree data structure used to store a dynamic set
// or associative array where the keys are usually strings. It's particularly
// efficient for prefix-based operations like autocomplete and spell checking.
//
// Features:
//   - Insert, search, and delete operations
//   - Prefix search and autocomplete suggestions
//   - Case-sensitive and case-insensitive modes
//   - Word frequency tracking
//   - Memory-efficient node structure
package trie_utils

import (
	"sort"
	"strings"
)

// TrieNode represents a single node in the Trie.
type TrieNode struct {
	children map[rune]*TrieNode
	isEnd    bool
	count    int // Frequency count for this word
}

// Trie represents the Trie data structure.
type Trie struct {
	root       *TrieNode
	size       int // Number of words
	caseSensitive bool
}

// Stats holds statistics about a Trie.
type Stats struct {
	TotalWords     int // Total number of words stored
	TotalNodes     int // Total number of nodes
	AverageDepth   float64 // Average depth of words
	MaxDepth       int // Maximum depth
	BranchingFactor float64 // Average branching factor
}

// NewTrie creates a new empty Trie with case-sensitive matching.
func NewTrie() *Trie {
	return &Trie{
		root: &TrieNode{
			children: make(map[rune]*TrieNode),
		},
		caseSensitive: true,
	}
}

// NewTrieCaseInsensitive creates a new Trie with case-insensitive matching.
func NewTrieCaseInsensitive() *Trie {
	return &Trie{
		root: &TrieNode{
			children: make(map[rune]*TrieNode),
		},
		caseSensitive: false,
	}
}

// normalizeWord normalizes a word based on case sensitivity setting.
func (t *Trie) normalizeWord(word string) string {
	if !t.caseSensitive {
		return strings.ToLower(word)
	}
	return word
}

// Insert adds a word to the Trie.
// Returns true if the word was newly added, false if it already existed.
// Increments the count if the word already exists.
func (t *Trie) Insert(word string) bool {
	word = t.normalizeWord(word)
	if word == "" {
		return false
	}

	node := t.root
	newWord := true

	for _, ch := range word {
		if node.children == nil {
			node.children = make(map[rune]*TrieNode)
		}
		if _, exists := node.children[ch]; !exists {
			node.children[ch] = &TrieNode{children: make(map[rune]*TrieNode)}
		}
		node = node.children[ch]
	}

	if node.isEnd {
		newWord = false
	} else {
		node.isEnd = true
		t.size++
	}
	node.count++

	return newWord
}

// InsertBatch adds multiple words to the Trie.
// Returns the count of newly inserted words.
func (t *Trie) InsertBatch(words []string) int {
	inserted := 0
	for _, word := range words {
		if t.Insert(word) {
			inserted++
		}
	}
	return inserted
}

// Search checks if a word exists in the Trie.
func (t *Trie) Search(word string) bool {
	word = t.normalizeWord(word)
	node := t.findNode(word)
	return node != nil && node.isEnd
}

// GetCount returns the frequency count of a word.
// Returns 0 if the word doesn't exist.
func (t *Trie) GetCount(word string) int {
	word = t.normalizeWord(word)
	node := t.findNode(word)
	if node != nil && node.isEnd {
		return node.count
	}
	return 0
}

// findNode finds the node corresponding to the given prefix.
func (t *Trie) findNode(prefix string) *TrieNode {
	node := t.root
	for _, ch := range prefix {
		if node.children == nil {
			return nil
		}
		if child, exists := node.children[ch]; exists {
			node = child
		} else {
			return nil
		}
	}
	return node
}

// StartsWith checks if there is any word in the Trie that starts with the given prefix.
func (t *Trie) StartsWith(prefix string) bool {
	prefix = t.normalizeWord(prefix)
	return t.findNode(prefix) != nil
}

// Delete removes a word from the Trie.
// Returns true if the word was found and removed, false otherwise.
func (t *Trie) Delete(word string) bool {
	word = t.normalizeWord(word)
	if word == "" {
		return false
	}

	// Find the node and all its ancestors
	path := make([]*TrieNode, 0, len(word)+1)
	path = append(path, t.root)

	node := t.root
	for _, ch := range word {
		if node.children == nil {
			return false
		}
		if child, exists := node.children[ch]; exists {
			node = child
			path = append(path, node)
		} else {
			return false
		}
	}

	if !node.isEnd {
		return false
	}

	node.isEnd = false
	node.count = 0
	t.size--

	// Clean up unused nodes (back to front)
	runes := []rune(word)
	for i := len(path) - 2; i >= 0; i-- {
		currentNode := path[i+1]
		// Only delete if this node has no children and is not an end of another word
		if len(currentNode.children) == 0 && !currentNode.isEnd {
			delete(path[i].children, runes[i])
		} else {
			break
		}
	}

	return true
}

// AutoComplete returns all words in the Trie that start with the given prefix.
// The returned words are sorted alphabetically.
func (t *Trie) AutoComplete(prefix string) []string {
	return t.AutoCompleteN(prefix, -1)
}

// AutoCompleteN returns up to n words in the Trie that start with the given prefix.
// If n is negative, returns all matching words.
// The returned words are sorted alphabetically.
func (t *Trie) AutoCompleteN(prefix string, n int) []string {
	prefix = t.normalizeWord(prefix)
	node := t.findNode(prefix)
	if node == nil {
		return []string{}
	}

	var results []string
	t.collectWords(node, prefix, &results)

	// Sort results
	sort.Strings(results)

	// Limit to n if specified
	if n > 0 && len(results) > n {
		results = results[:n]
	}

	return results
}

// AutoCompleteByFrequency returns words sorted by frequency (descending).
func (t *Trie) AutoCompleteByFrequency(prefix string, n int) []string {
	prefix = t.normalizeWord(prefix)
	node := t.findNode(prefix)
	if node == nil {
		return []string{}
	}

	type wordCount struct {
		word  string
		count int
	}

	var results []wordCount
	t.collectWordsWithCount(node, prefix, &results)

	// Sort by count (descending), then alphabetically
	sort.Slice(results, func(i, j int) bool {
		if results[i].count != results[j].count {
			return results[i].count > results[j].count
		}
		return results[i].word < results[j].word
	})

	words := make([]string, 0, len(results))
	for i, wc := range results {
		if n > 0 && i >= n {
			break
		}
		words = append(words, wc.word)
	}

	return words
}

// collectWords collects all words from a node recursively.
func (t *Trie) collectWords(node *TrieNode, prefix string, results *[]string) {
	if node.isEnd {
		*results = append(*results, prefix)
	}

	// Sort children for consistent ordering
	var keys []rune
	for k := range node.children {
		keys = append(keys, k)
	}
	sort.Slice(keys, func(i, j int) bool { return keys[i] < keys[j] })

	for _, ch := range keys {
		t.collectWords(node.children[ch], prefix+string(ch), results)
	}
}

// collectWordsWithCount collects all words with their counts.
func (t *Trie) collectWordsWithCount(node *TrieNode, prefix string, results *[]struct {
	word  string
	count int
}) {
	if node.isEnd {
		*results = append(*results, struct {
			word  string
			count int
		}{prefix, node.count})
	}

	for ch, child := range node.children {
		t.collectWordsWithCount(child, prefix+string(ch), results)
	}
}

// GetAllWords returns all words in the Trie, sorted alphabetically.
func (t *Trie) GetAllWords() []string {
	return t.AutoComplete("")
}

// Size returns the number of words in the Trie.
func (t *Trie) Size() int {
	return t.size
}

// IsEmpty checks if the Trie is empty.
func (t *Trie) IsEmpty() bool {
	return t.size == 0
}

// Clear removes all words from the Trie.
func (t *Trie) Clear() {
	t.root = &TrieNode{children: make(map[rune]*TrieNode)}
	t.size = 0
}

// LongestCommonPrefix returns the longest common prefix among all words in the Trie.
// Returns empty string if the Trie is empty.
func (t *Trie) LongestCommonPrefix() string {
	if t.IsEmpty() {
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

// LongestPrefixOf returns the longest word in the Trie that is a prefix of the given string.
func (t *Trie) LongestPrefixOf(word string) string {
	word = t.normalizeWord(word)
	var longest []rune
	var current []rune
	node := t.root

	for _, ch := range word {
		if node.children == nil {
			break
		}
		if child, exists := node.children[ch]; exists {
			current = append(current, ch)
			node = child
			if node.isEnd {
				longest = make([]rune, len(current))
				copy(longest, current)
			}
		} else {
			break
		}
	}

	return string(longest)
}

// CountPrefix returns the number of words that start with the given prefix.
func (t *Trie) CountPrefix(prefix string) int {
	prefix = t.normalizeWord(prefix)
	node := t.findNode(prefix)
	if node == nil {
		return 0
	}

	count := 0
	t.countWords(node, &count)
	return count
}

// countWords recursively counts all words under a node.
func (t *Trie) countWords(node *TrieNode, count *int) {
	if node.isEnd {
		*count++
	}
	for _, child := range node.children {
		t.countWords(child, count)
	}
}

// GetStats returns statistics about the Trie.
func (t *Trie) GetStats() Stats {
	stats := Stats{
		TotalWords: t.size,
	}

	if t.IsEmpty() {
		return stats
	}

	var totalDepth, maxDepth, totalBranches, nodeCount int
	t.calculateStats(t.root, 0, &totalDepth, &maxDepth, &totalBranches, &nodeCount)

	stats.TotalNodes = nodeCount
	stats.MaxDepth = maxDepth
	if t.size > 0 {
		stats.AverageDepth = float64(totalDepth) / float64(t.size)
	}
	if nodeCount > 1 {
		stats.BranchingFactor = float64(totalBranches) / float64(nodeCount-1)
	}

	return stats
}

// calculateStats recursively calculates Trie statistics.
func (t *Trie) calculateStats(node *TrieNode, depth int, totalDepth, maxDepth, totalBranches, nodeCount *int) {
	*nodeCount++
	
	if node.isEnd {
		*totalDepth += depth
	}
	if depth > *maxDepth {
		*maxDepth = depth
	}

	*totalBranches += len(node.children)

	for _, child := range node.children {
		t.calculateStats(child, depth+1, totalDepth, maxDepth, totalBranches, nodeCount)
	}
}

// MatchPattern returns all words that match the given pattern.
// Pattern supports:
//   - '?' for any single character
//   - '*' for any sequence of characters (including empty)
func (t *Trie) MatchPattern(pattern string) []string {
	var results []string
	t.matchPatternRecursive(t.root, "", pattern, &results)
	sort.Strings(results)
	return results
}

// matchPatternRecursive recursively matches pattern against Trie nodes.
func (t *Trie) matchPatternRecursive(node *TrieNode, current string, pattern string, results *[]string) {
	if len(pattern) == 0 {
		if node.isEnd {
			*results = append(*results, current)
		}
		return
	}

	ch := rune(pattern[0])
	rest := pattern[1:]

	switch ch {
	case '?':
		// Match any single character
		for childCh, child := range node.children {
			t.matchPatternRecursive(child, current+string(childCh), rest, results)
		}
	case '*':
		// Match zero or more characters
		// Zero characters: skip the *
		t.matchPatternRecursive(node, current, rest, results)
		// One or more characters: consume a character and stay on *
		for childCh, child := range node.children {
			t.matchPatternRecursive(child, current+string(childCh), pattern, results)
		}
	default:
		// Match exact character
		if child, exists := node.children[ch]; exists {
			t.matchPatternRecursive(child, current+string(ch), rest, results)
		}
	}
}

// FuzzySearch returns words that are within the given edit distance.
// Uses Levenshtein distance for fuzzy matching.
func (t *Trie) FuzzySearch(word string, maxDistance int) []string {
	word = t.normalizeWord(word)
	var results []string

	// Get all words and filter by edit distance
	t.collectWords(t.root, "", &results)

	var filtered []string
	for _, w := range results {
		if levenshteinDistance(word, w) <= maxDistance {
			filtered = append(filtered, w)
		}
	}

	sort.Strings(filtered)
	return filtered
}

// levenshteinDistance calculates the Levenshtein distance between two strings.
func levenshteinDistance(s1, s2 string) int {
	r1, r2 := []rune(s1), []rune(s2)
	len1, len2 := len(r1), len(r2)

	if len1 == 0 {
		return len2
	}
	if len2 == 0 {
		return len1
	}

	// Create matrix
	matrix := make([][]int, len1+1)
	for i := range matrix {
		matrix[i] = make([]int, len2+1)
	}

	// Initialize first column
	for i := 0; i <= len1; i++ {
		matrix[i][0] = i
	}

	// Initialize first row
	for j := 0; j <= len2; j++ {
		matrix[0][j] = j
	}

	// Fill in the rest
	for i := 1; i <= len1; i++ {
		for j := 1; j <= len2; j++ {
			cost := 1
			if r1[i-1] == r2[j-1] {
				cost = 0
			}

			matrix[i][j] = min(
				matrix[i-1][j]+1,      // deletion
				matrix[i][j-1]+1,      // insertion
				matrix[i-1][j-1]+cost, // substitution
			)
		}
	}

	return matrix[len1][len2]
}

func min(a, b, c int) int {
	if a < b {
		if a < c {
			return a
		}
		return c
	}
	if b < c {
		return b
	}
	return c
}