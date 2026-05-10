// Example usage of anagram_utils package
// anagram_utils 包使用示例
package main

import (
	"fmt"
	"sort"
	"strings"

	anagram "github.com/ayukyo/alltoolkit/Go/anagram_utils"
)

func main() {
	fmt.Println("=== Anagram Utils Examples ===")
	fmt.Println()

	// Example 1: Basic anagram check
	// 示例 1：基本字谜检查
	fmt.Println("1. Basic Anagram Check (基本字谜检查):")
	fmt.Printf("   IsAnagram(\"listen\", \"silent\"): %v\n", anagram.IsAnagram("listen", "silent"))
	fmt.Printf("   IsAnagram(\"dormitory\", \"dirty room\"): %v\n", anagram.IsAnagram("dormitory", "dirty room"))
	fmt.Printf("   IsAnagram(\"hello\", \"world\"): %v\n", anagram.IsAnagram("hello", "world"))
	fmt.Println()

	// Example 2: Strict anagram check (case-sensitive)
	// 示例 2：严格字谜检查（区分大小写）
	fmt.Println("2. Strict Anagram Check - Case Sensitive (严格字谜检查 - 区分大小写):")
	fmt.Printf("   IsAnagramStrict(\"Abc\", \"cba\"): %v\n", anagram.IsAnagramStrict("Abc", "cba"))
	fmt.Printf("   IsAnagramStrict(\"ABC\", \"CBA\"): %v\n", anagram.IsAnagramStrict("ABC", "CBA"))
	fmt.Println()

	// Example 3: Get letter signature
	// 示例 3：获取字母签名
	fmt.Println("3. Letter Signature (字母签名):")
	fmt.Printf("   GetSignature(\"listen\"): %s\n", anagram.GetSignature("listen"))
	fmt.Printf("   GetSignature(\"SILENT\"): %s\n", anagram.GetSignature("SILENT"))
	fmt.Println()

	// Example 4: Find anagrams in word list
	// 示例 4：在单词列表中查找字谜
	fmt.Println("4. Find Anagrams in Word List (在单词列表中查找字谜):")
	wordList := []string{"listen", "silent", "enlist", "inlets", "hello", "world", "tinsel", "earth", "heart"}
	anagrams := anagram.FindAnagrams("listen", wordList)
	fmt.Printf("   Anagrams of \"listen\": %v\n", anagrams)
	fmt.Println()

	// Example 5: Group anagrams
	// 示例 5：字谜分组
	fmt.Println("5. Group Anagrams (字谜分组):")
	words := []string{"listen", "silent", "enlist", "hello", "act", "cat", "tac", "earth", "heart"}
	groups := anagram.GroupAnagrams(words)
	for sig, group := range groups {
		if len(group) > 1 {
			fmt.Printf("   Signature \"%s\": %v\n", sig, group)
		}
	}
	fmt.Println()

	// Example 6: Generate all anagrams
	// 示例 6：生成所有字谜
	fmt.Println("6. Generate All Anagrams (生成所有字谜):")
	fmt.Printf("   Anagrams of \"abc\": %v\n", anagram.GenerateAnagrams("abc"))
	fmt.Printf("   Anagrams of \"aab\": %v\n", anagram.GenerateAnagrams("aab"))
	fmt.Println()

	// Example 7: Limited anagram generation
	// 示例 7：受限字谜生成
	fmt.Println("7. Limited Anagram Generation (受限字谜生成):")
	anagramsLimited := anagram.GenerateAnagramsLimit("abcd", 10)
	fmt.Printf("   First 10 anagrams of \"abcd\": %v\n", anagramsLimited)
	fmt.Printf("   Total possible: %d\n", anagram.CountAnagrams("abcd"))
	fmt.Println()

	// Example 8: Count unique anagrams
	// 示例 8：计算唯一字谜数量
	fmt.Println("8. Count Unique Anagrams (计算唯一字谜数量):")
	fmt.Printf("   CountAnagrams(\"abc\"): %d (3! = 6)\n", anagram.CountAnagrams("abc"))
	fmt.Printf("   CountAnagrams(\"aab\"): %d (3!/2! = 3)\n", anagram.CountAnagrams("aab"))
	fmt.Printf("   CountAnagrams(\"aabb\"): %d (4!/(2!*2!) = 6)\n", anagram.CountAnagrams("aabb"))
	fmt.Println()

	// Example 9: Letter frequency
	// 示例 9：字母频率
	fmt.Println("9. Letter Frequency (字母频率):")
	freq := anagram.GetLetterFrequency("mississippi")
	fmt.Printf("   Frequency in \"mississippi\": %v\n", formatFreq(freq))
	fmt.Println()

	// Example 10: Valid anagram check (excluding same word)
	// 示例 10：有效字谜检查（排除相同单词）
	fmt.Println("10. Valid Anagram Check (有效字谜检查):")
	fmt.Printf("   IsValidAnagram(\"listen\", \"silent\"): %v\n", anagram.IsValidAnagram("listen", "silent"))
	fmt.Printf("   IsValidAnagram(\"test\", \"test\"): %v\n", anagram.IsValidAnagram("test", "test"))
	fmt.Println()

	// Example 11: Can form word from letters
	// 示例 11：能否用字母组成单词
	fmt.Println("11. Can Form Word (能否用字母组成单词):")
	fmt.Printf("   CanFormWord(\"abcdef\", \"bed\"): %v\n", anagram.CanFormWord("abcdef", "bed"))
	fmt.Printf("   CanFormWord(\"abcdef\", \"bedg\"): %v\n", anagram.CanFormWord("abcdef", "bedg"))
	fmt.Printf("   CanFormWord(\"aabbcc\", \"abc\"): %v\n", anagram.CanFormWord("aabbcc", "abc"))
	fmt.Println()

	// Example 12: Find possible words (word game helper)
	// 示例 12：查找可能的单词（文字游戏助手）
	fmt.Println("12. Find Possible Words - Word Game Helper (查找可能的单词 - 文字游戏助手):")
	available := "tacb"
	dictionary := []string{"cat", "act", "tac", "bat", "tab", "cab", "dog"}
	possible := anagram.FindPossibleWords(available, dictionary)
	sort.Strings(possible)
	fmt.Printf("   Letters: \"%s\"\n", available)
	fmt.Printf("   Possible words: %v\n", possible)
	fmt.Println()

	// Example 13: Scrabble scoring
	// 示例 13：Scrabble 分数
	fmt.Println("13. Scrabble Scoring (Scrabble 分数):")
	words_to_score := []string{"cat", "quiz", "jazz", "quick", "cabbage"}
	for _, w := range words_to_score {
		fmt.Printf("   ScrabbleScore(\"%s\"): %d\n", w, anagram.ScrabbleScore(w))
	}
	fmt.Println()

	// Example 14: Highest scoring word
	// 示例 14：最高分单词
	fmt.Println("14. Highest Scoring Word (最高分单词):")
	letters := "quizactopg"
	dict := []string{"cat", "dog", "quiz", "act", "zip"}
	best := anagram.HighestScoringWord(letters, dict)
	bestScore := anagram.ScrabbleScore(best)
	fmt.Printf("   Available letters: \"%s\"\n", letters)
	fmt.Printf("   Highest scoring word: \"%s\" (score: %d)\n", best, bestScore)
	fmt.Println()

	// Example 15: Longest anagram
	// 示例 15：最长字谜
	fmt.Println("15. Longest Anagram (最长字谜):")
	avail := "cttacti"
	dict2 := []string{"a", "at", "act", "cat", "tact", "tactic"}
	longest := anagram.LongestAnagram(avail, dict2)
	fmt.Printf("   Available letters: \"%s\"\n", avail)
	fmt.Printf("   Longest word: \"%s\" (length: %d)\n", longest, len(longest))
	fmt.Println()

	// Example 16: Classic anagram pairs
	// 示例 16：经典字谜对
	fmt.Println("16. Classic Anagram Pairs (经典字谜对):")
	classicPairs := [][2]string{
		{"listen", "silent"},
		{"dormitory", "dirty room"},
		{"eleven plus two", "twelve plus one"},
		{"astronomer", "moon starer"},
		{"the eyes", "they see"},
		{"funeral", "real fun"},
		{"slot machines", "cash lost in me"},
	}
	for _, pair := range classicPairs {
		result := anagram.IsAnagram(pair[0], pair[1])
		fmt.Printf("   %-20s ↔ %-20s: %v\n", "\""+pair[0]+"\"", "\""+pair[1]+"\"", result)
	}
	fmt.Println()

	// Example 17: Remove letter helper
	// 示例 17：移除字母助手
	fmt.Println("17. Remove Letter Helper (移除字母助手):")
	fmt.Printf("   RemoveLetter(\"hello\", 'l'): \"%s\"\n", anagram.RemoveLetter("hello", 'l'))
	fmt.Printf("   RemoveLetter(\"hello\", 'z'): \"%s\"\n", anagram.RemoveLetter("hello", 'z'))
	fmt.Println()

	fmt.Println("=== All Examples Complete ===")
}

func formatFreq(freq map[rune]int) string {
	var pairs []string
	for r, count := range freq {
		pairs = append(pairs, fmt.Sprintf("%c:%d", r, count))
	}
	sort.Strings(pairs)
	return "{" + strings.Join(pairs, ", ") + "}"
}