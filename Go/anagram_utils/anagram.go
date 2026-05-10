// Package anagram_utils provides utilities for generating and checking anagrams.
// An anagram is a word or phrase formed by rearranging the letters of another.
// 包 anagram_utils 提供生成和检查字谜的工具。
// 字谜是通过重新排列另一个单词或短语的字母而形成的单词或短语。
package anagram_utils

import (
	"sort"
	"strings"
	"unicode"
)

// IsAnagram checks if two strings are anagrams of each other.
// It ignores case and non-letter characters by default.
// IsAnagram 检查两个字符串是否互为字谜。
// 默认情况下忽略大小写和非字母字符。
func IsAnagram(s1, s2 string) bool {
	// Normalize both strings: lowercase and filter letters only
	norm1 := normalize(s1)
	norm2 := normalize(s2)

	if len(norm1) != len(norm2) {
		return false
	}

	// Sort and compare
	return sortString(norm1) == sortString(norm2)
}

// IsAnagramStrict checks if two strings are exact anagrams (case-sensitive, includes all characters).
// IsAnagramStrict 检查两个字符串是否为精确字谜（区分大小写，包含所有字符）。
func IsAnagramStrict(s1, s2 string) bool {
	if len(s1) != len(s2) {
		return false
	}
	return sortString(s1) == sortString(s2)
}

// normalize converts string to lowercase and removes non-letter characters.
// normalize 将字符串转换为小写并移除非字母字符。
func normalize(s string) string {
	var result strings.Builder
	result.Grow(len(s))
	for _, r := range s {
		if unicode.IsLetter(r) {
			result.WriteRune(unicode.ToLower(r))
		}
	}
	return result.String()
}

// sortString returns a sorted version of the string.
// sortString 返回字符串的排序版本。
func sortString(s string) string {
	runes := []rune(s)
	sort.Slice(runes, func(i, j int) bool {
		return runes[i] < runes[j]
	})
	return string(runes)
}

// GetSignature returns the letter signature of a string (sorted letters).
// Useful for grouping anagrams together.
// GetSignature 返回字符串的字母签名（排序后的字母）。
// 对于将字谜分组非常有用。
func GetSignature(s string) string {
	return sortString(normalize(s))
}

// GetSignatureStrict returns the strict letter signature (case-sensitive, all chars).
// GetSignatureStrict 返回严格的字母签名（区分大小写，包含所有字符）。
func GetSignatureStrict(s string) string {
	return sortString(s)
}

// FindAnagrams finds all anagrams of a word in a given word list.
// Returns a slice of matching words (excluding the original word itself).
// FindAnagrams 在给定的单词列表中查找单词的所有字谜。
// 返回匹配单词的切片（排除原始单词本身）。
func FindAnagrams(word string, wordList []string) []string {
	signature := GetSignature(word)
	var result []string
	normalizedWord := normalize(word)

	for _, w := range wordList {
		if normalize(w) == normalizedWord {
			continue // Skip the same word
		}
		if GetSignature(w) == signature {
			result = append(result, w)
		}
	}
	return result
}

// FindAnagramsStrict finds exact anagrams (case-sensitive) in a word list.
// FindAnagramsStrict 在单词列表中查找精确字谜（区分大小写）。
func FindAnagramsStrict(word string, wordList []string) []string {
	signature := GetSignatureStrict(word)
	var result []string

	for _, w := range wordList {
		if w == word {
			continue
		}
		if GetSignatureStrict(w) == signature {
			result = append(result, w)
		}
	}
	return result
}

// GroupAnagrams groups words by their anagram signature.
// Returns a map where keys are signatures and values are lists of anagrams.
// GroupAnagrams 按字谜签名对单词进行分组。
// 返回一个映射，其中键是签名，值是字谜列表。
func GroupAnagrams(words []string) map[string][]string {
	groups := make(map[string][]string)
	for _, word := range words {
		sig := GetSignature(word)
		groups[sig] = append(groups[sig], word)
	}
	return groups
}

// GroupAnagramsStrict groups words by their strict anagram signature.
// GroupAnagramsStrict 按严格字谜签名对单词进行分组。
func GroupAnagramsStrict(words []string) map[string][]string {
	groups := make(map[string][]string)
	for _, word := range words {
		sig := GetSignatureStrict(word)
		groups[sig] = append(groups[sig], word)
	}
	return groups
}

// GenerateAnagrams generates all possible anagrams of a string.
// Warning: This can be very slow for long strings (O(n!)).
// Warning: For strings longer than 10 characters, consider using limited generation.
// GenerateAnagrams 生成字符串的所有可能字谜。
// 警告：对于长字符串，这可能非常慢（O(n!)）。
// 警告：对于超过 10 个字符的字符串，请考虑使用受限生成。
func GenerateAnagrams(s string) []string {
	runes := []rune(normalize(s))
	if len(runes) == 0 {
		return []string{}
	}

	// Use a map to deduplicate
	seen := make(map[string]bool)
	var result []string

	permute(runes, 0, seen)
	for anagram := range seen {
		result = append(result, anagram)
	}

	sort.Strings(result)
	return result
}

// permute generates all permutations recursively.
func permute(runes []rune, start int, seen map[string]bool) {
	if start == len(runes)-1 {
		seen[string(runes)] = true
		return
	}

	for i := start; i < len(runes); i++ {
		// Swap
		runes[start], runes[i] = runes[i], runes[start]
		permute(runes, start+1, seen)
		// Swap back
		runes[start], runes[i] = runes[i], runes[start]
	}
}

// GenerateAnagramsLimit generates up to n anagrams.
// Useful for avoiding explosion with long strings.
// GenerateAnagramsLimit 生成最多 n 个字谜。
// 对于避免长字符串的爆炸式增长非常有用。
func GenerateAnagramsLimit(s string, limit int) []string {
	runes := []rune(normalize(s))
	if len(runes) == 0 || limit <= 0 {
		return []string{}
	}

	seen := make(map[string]bool)
	result := make([]string, 0, limit)

	var generate func(int)
	generate = func(start int) {
		if len(result) >= limit {
			return
		}
		if start == len(runes)-1 {
			anagram := string(runes)
			if !seen[anagram] {
				seen[anagram] = true
				result = append(result, anagram)
			}
			return
		}

		for i := start; i < len(runes) && len(result) < limit; i++ {
			runes[start], runes[i] = runes[i], runes[start]
			generate(start + 1)
			runes[start], runes[i] = runes[i], runes[start]
		}
	}

	generate(0)
	return result
}

// IsValidAnagram checks if candidate is a valid anagram of source.
// Also checks that candidate is not identical to source.
// IsValidAnagram 检查 candidate 是否是 source 的有效字谜。
// 同时检查 candidate 是否与 source 相同。
func IsValidAnagram(source, candidate string) bool {
	normSource := normalize(source)
	normCandidate := normalize(candidate)

	// Must not be identical
	if normSource == normCandidate {
		return false
	}

	return IsAnagram(source, candidate)
}

// CountAnagrams returns the count of unique anagrams possible.
// For strings with duplicate characters, this is less than factorial.
// CountAnagrams 返回可能的唯一字谜数量。
// 对于有重复字符的字符串，这小于阶乘。
func CountAnagrams(s string) int {
	runes := []rune(normalize(s))
	n := len(runes)
	if n == 0 {
		return 0
	}

	// Count frequency of each character
	freq := make(map[rune]int)
	for _, r := range runes {
		freq[r]++
	}

	// Calculate factorial(n) / (factorial(count[each char]))
	result := factorial(n)
	for _, count := range freq {
		result /= factorial(count)
	}

	return result
}

// factorial calculates n!
func factorial(n int) int {
	if n <= 1 {
		return 1
	}
	result := 1
	for i := 2; i <= n; i++ {
		result *= i
	}
	return result
}

// GetLetterFrequency returns a map of letter frequencies.
// GetLetterFrequency 返回字母频率映射。
func GetLetterFrequency(s string) map[rune]int {
	freq := make(map[rune]int)
	for _, r := range normalize(s) {
		freq[r]++
	}
	return freq
}

// HasSameLetters checks if two strings have the same letter composition.
// HasSameLetters 检查两个字符串是否具有相同的字母组成。
func HasSameLetters(s1, s2 string) bool {
	return GetSignature(s1) == GetSignature(s2)
}

// RemoveLetter removes the first occurrence of a letter from a string.
// Useful for building anagrams step by step.
// RemoveLetter 从字符串中移除第一次出现的字母。
// 对于逐步构建字谜非常有用。
func RemoveLetter(s string, letter rune) string {
	runes := []rune(s)
	for i, r := range runes {
		if unicode.ToLower(r) == unicode.ToLower(letter) {
			return string(runes[:i]) + string(runes[i+1:])
		}
	}
	return s
}

// CanFormWord checks if word can be formed from the letters available.
// canFormWord 检查是否可以用可用的字母组成单词。
func CanFormWord(availableLetters, word string) bool {
	available := GetLetterFrequency(availableLetters)
	needed := GetLetterFrequency(word)

	for letter, count := range needed {
		if available[letter] < count {
			return false
		}
	}
	return true
}

// FindPossibleWords finds all words that can be formed from available letters.
// Each letter can only be used once.
// FindPossibleWords 查找所有可以用可用字母组成的单词。
// 每个字母只能使用一次。
func FindPossibleWords(availableLetters string, wordList []string) []string {
	var result []string
	for _, word := range wordList {
		if CanFormWord(availableLetters, word) {
			result = append(result, word)
		}
	}
	return result
}

// LongestAnagram finds the longest word that is an anagram of a subset of available letters.
// LongestAnagram 查找是可用字母子集字谜的最长单词。
func LongestAnagram(availableLetters string, wordList []string) string {
	longest := ""
	for _, word := range wordList {
		if CanFormWord(availableLetters, word) && len(word) > len(longest) {
			longest = word
		}
	}
	return longest
}

// ScrabbleScore calculates the Scrabble score for a word.
// ScrabbleScore 计算单词的 Scrabble 分数。
func ScrabbleScore(word string) int {
	// Standard Scrabble letter values
	values := map[rune]int{
		'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
		'd': 2, 'g': 2,
		'b': 3, 'c': 3, 'm': 3, 'p': 3,
		'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
		'k': 5,
		'j': 8, 'x': 8,
		'q': 10, 'z': 10,
	}

	score := 0
	for _, r := range normalize(word) {
		score += values[r]
	}
	return score
}

// HighestScoringWord finds the word with the highest Scrabble score from available letters.
// HighestScoringWord 从可用字母中查找 Scrabble 分数最高的单词。
func HighestScoringWord(availableLetters string, wordList []string) string {
	bestWord := ""
	bestScore := -1

	for _, word := range wordList {
		if CanFormWord(availableLetters, word) {
			score := ScrabbleScore(word)
			if score > bestScore {
				bestScore = score
				bestWord = word
			}
		}
	}
	return bestWord
}