package main

import (
	"fmt"
	"strings"

	su "github.com/openclaw/alltoolkit/Go/string_utils"
)

func main() {
	fmt.Println("=== Go String Utils - 完整示例 ===")
	fmt.Println()

	// 1. 大小写转换
	fmt.Println("📐 大小写转换")
	fmt.Println(strings.Repeat("-", 40))

	original := "hello_world_example"
	fmt.Printf("原始字符串: %s\n", original)
	fmt.Printf("  → camelCase:    %s\n", su.ToCamelCase(original))
	fmt.Printf("  → PascalCase:   %s\n", su.ToPascalCase(original))
	fmt.Printf("  → snake_case:   %s\n", su.ToSnakeCase("HelloWorldExample"))
	fmt.Printf("  → kebab-case:   %s\n", su.ToKebabCase(original))
	fmt.Printf("  → SCREAMING:    %s\n", su.ToScreamingSnakeCase(original))
	fmt.Printf("  → Title Case:   %s\n", su.ToTitleCase(original))
	fmt.Println()

	// 2. 字符串验证
	fmt.Println("✅ 字符串验证")
	fmt.Println(strings.Repeat("-", 40))

	validations := []struct {
		name  string
		value string
		check func(string) bool
	}{
		{"邮箱", "test@example.com", su.IsEmail},
		{"电话", "+1-234-567-8901", su.IsPhone},
		{"URL", "https://example.com/path", su.IsURL},
		{"UUID", "550e8400-e29b-41d4-a716-446655440000", su.IsUUID},
		{"IPv4", "192.168.1.1", su.IsIPv4},
		{"十六进制颜色", "#FF5500", su.IsHexColor},
		{"URL Slug", "my-blog-post-title", su.IsSlug},
		{"纯字母", "HelloWorld", su.IsAlpha},
		{"字母数字", "Hello123", su.IsAlphanumeric},
		{"纯数字", "12345", su.IsNumeric},
		{"全大写", "HELLO", su.IsUpper},
		{"全小写", "hello", su.IsLower},
	}

	for _, v := range validations {
		status := "✗"
		if v.check(v.value) {
			status = "✓"
		}
		fmt.Printf("  %s %-15s %q\n", status, v.name+":", v.value)
	}
	fmt.Println()

	// 3. 字符串相似度
	fmt.Println("🔍 字符串相似度")
	fmt.Println(strings.Repeat("-", 40))

	pairs := []struct {
		s1 string
		s2 string
	}{
		{"kitten", "sitting"},
		{"hello", "hallo"},
		{"world", "word"},
		{"programming", "programmer"},
	}

	for _, p := range pairs {
		distance := su.LevenshteinDistance(p.s1, p.s2)
		similarity := su.Similarity(p.s1, p.s2)
		jaro := su.JaroSimilarity(p.s1, p.s2)
		jw := su.JaroWinklerSimilarity(p.s1, p.s2)

		fmt.Printf("  %q vs %q:\n", p.s1, p.s2)
		fmt.Printf("    Levenshtein 距离: %d\n", distance)
		fmt.Printf("    相似度:           %.2f%%\n", similarity*100)
		fmt.Printf("    Jaro 相似度:      %.2f%%\n", jaro*100)
		fmt.Printf("    Jaro-Winkler:     %.2f%%\n", jw*100)
	}
	fmt.Println()

	// 4. 字符串操作
	fmt.Println("🔧 字符串操作")
	fmt.Println(strings.Repeat("-", 40))

	str := "Hello World"
	fmt.Printf("原始: %q\n", str)
	fmt.Printf("  反转:           %q\n", su.Reverse(str))
	fmt.Printf("  截断(8,...):    %q\n", su.Truncate(str, 8, "..."))
	fmt.Printf("  左填充(15,-):   %q\n", su.PadLeft(str, 15, '-'))
	fmt.Printf("  右填充(15,-):   %q\n", su.PadRight(str, 15, '-'))
	fmt.Printf("  居中填充(15,*): %q\n", su.PadCenter(str, 15, '*'))
	fmt.Println()

	// 5. 字符串分析
	fmt.Println("📊 字符串分析")
	fmt.Println(strings.Repeat("-", 40))

	text := "The quick brown fox jumps over the lazy dog"
	fmt.Printf("文本: %q\n", text)
	fmt.Printf("  字符数:    %d\n", su.CharCount(text))
	fmt.Printf("  字节数:    %d\n", su.ByteCount(text))
	fmt.Printf("  单词数:    %d\n", su.WordCount(text))
	fmt.Printf("  最长单词:  %q\n", su.LongestWord(text))
	fmt.Printf("  最短单词:  %q\n", su.ShortestWord(text))

	// 字符频率
	freq := su.Frequency("hello world")
	fmt.Printf("  字符频率:   ")
	for char, count := range freq {
		fmt.Printf("%c:%d ", char, count)
	}
	fmt.Println()

	// 单词频率
	wordFreq := su.WordFrequency("hello world hello universe hello")
	fmt.Printf("  单词频率:   ")
	for word, count := range wordFreq {
		fmt.Printf("%s:%d ", word, count)
	}
	fmt.Println()
	fmt.Println()

	// 6. 特殊检查
	fmt.Println("🎯 特殊检查")
	fmt.Println(strings.Repeat("-", 40))

	palindromes := []string{
		"racecar",
		"A man a plan a canal Panama",
		"Was it a car or a cat I saw",
	}
	fmt.Println("回文检测:")
	for _, p := range palindromes {
		fmt.Printf("  %s %q\n", map[bool]string{true: "✓", false: "✗"}[su.IsPalindrome(p)], p)
	}

	anagrams := []struct {
		s1, s2 string
	}{
		{"listen", "silent"},
		{"anagram", "nag a ram"},
		{"hello", "world"},
	}
	fmt.Println("\n变位词检测:")
	for _, a := range anagrams {
		fmt.Printf("  %s %q ↔ %q\n", map[bool]string{true: "✓", false: "✗"}[su.IsAnagram(a.s1, a.s2)], a.s1, a.s2)
	}

	pangrams := []string{
		"The quick brown fox jumps over the lazy dog",
		"Pack my box with five dozen liquor jugs",
		"Hello world",
	}
	fmt.Println("\n全字母句检测 (包含所有26个字母):")
	for _, p := range pangrams {
		fmt.Printf("  %s %q\n", map[bool]string{true: "✓", false: "✗"}[su.IsPangram(p)], p)
	}
	fmt.Println()

	// 7. 字符串掩码
	fmt.Println("🔒 字符串掩码")
	fmt.Println(strings.Repeat("-", 40))

	email := "user@example.com"
	phone := "+1 (234) 567-8901"
	card := "1234567890123456"

	fmt.Printf("邮箱:   %q → %q\n", email, su.MaskEmail(email, '*'))
	fmt.Printf("电话:   %q → %q\n", phone, su.MaskPhone(phone, '*'))
	fmt.Printf("卡号:   %q → %q\n", card, su.Mask(card, 4, 4, '*'))
	fmt.Println()

	// 8. 模糊匹配
	fmt.Println("🔎 模糊匹配")
	fmt.Println(strings.Repeat("-", 40))

	pattern := "prg"
	candidates := []string{"programming", "programmer", "progress", "project", "pragmatic"}

	fmt.Printf("搜索模式: %q\n", pattern)
	fmt.Println("候选词:")
	for _, c := range candidates {
		score := su.FuzzyMatchScore(c, pattern)
		match := su.FuzzyMatch(c, pattern)
		fmt.Printf("  %s %-12s 分数: %3d\n", map[bool]string{true: "✓", false: "✗"}[match], c+":", score)
	}

	best, score := su.FindBestMatch(pattern, candidates)
	fmt.Printf("\n最佳匹配: %q (分数: %d)\n", best, score)
	fmt.Println()

	// 9. 其他实用功能
	fmt.Println("🛠️ 其他实用功能")
	fmt.Println(strings.Repeat("-", 40))

	// 子字符串
	text2 := "你好世界 Hello World"
	fmt.Printf("子字符串:\n")
	fmt.Printf("  原始:       %q\n", text2)
	fmt.Printf("  Left(6):    %q\n", su.Left(text2, 6))
	fmt.Printf("  Right(5):   %q\n", su.Right(text2, 5))
	fmt.Printf("  Substring:  %q\n", su.Substring(text2, 2, 6))

	// 分块
	chunks := su.Chunk("HelloWorld", 3)
	fmt.Printf("\n分块 (3字符): %v\n", chunks)

	// 模板替换
	template := "你好 ${name}，欢迎来到 ${place}！"
	values := map[string]string{"name": "世界", "place": "Go语言世界"}
	fmt.Printf("\n模板替换:\n")
	fmt.Printf("  模板: %q\n", template)
	fmt.Printf("  结果: %q\n", su.Template(template, values))

	// 移除重音
	fmt.Printf("\n移除重音:\n")
	accented := []string{"café", "naïve", "résumé", "über"}
	for _, a := range accented {
		fmt.Printf("  %q → %q\n", a, su.RemoveAccents(a))
	}

	fmt.Println()
	fmt.Println("=== 示例结束 ===")
}