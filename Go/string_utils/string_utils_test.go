package string_utils

import (
	"testing"
)

// ==================== Case Conversion Tests ====================

func TestToCamelCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello_world", "helloWorld"},
		{"hello-world", "helloWorld"},
		{"hello world", "helloWorld"},
		{"HelloWorld", "helloWorld"},
		{"HELLO_WORLD", "helloWorld"},
		{"already_camel_case", "alreadyCamelCase"},
		{"XMLHttpRequest", "xmlHttpRequest"},
		{"", ""},
		{"a", "a"},
		{"ABC", "abc"},
	}

	for _, test := range tests {
		result := ToCamelCase(test.input)
		if result != test.expected {
			t.Errorf("ToCamelCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToPascalCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello_world", "HelloWorld"},
		{"hello-world", "HelloWorld"},
		{"hello world", "HelloWorld"},
		{"helloWorld", "HelloWorld"},
		{"HELLO_WORLD", "HelloWorld"},
		{"", ""},
		{"a", "A"},
	}

	for _, test := range tests {
		result := ToPascalCase(test.input)
		if result != test.expected {
			t.Errorf("ToPascalCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToSnakeCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"helloWorld", "hello_world"},
		{"HelloWorld", "hello_world"},
		{"hello world", "hello_world"},
		{"hello-world", "hello_world"},
		{"XMLHttpRequest", "xml_http_request"},
		{"", ""},
		{"a", "a"},
	}

	for _, test := range tests {
		result := ToSnakeCase(test.input)
		if result != test.expected {
			t.Errorf("ToSnakeCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToKebabCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"helloWorld", "hello-world"},
		{"HelloWorld", "hello-world"},
		{"hello world", "hello-world"},
		{"hello_world", "hello-world"},
		{"", ""},
		{"a", "a"},
	}

	for _, test := range tests {
		result := ToKebabCase(test.input)
		if result != test.expected {
			t.Errorf("ToKebabCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToScreamingSnakeCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"helloWorld", "HELLO_WORLD"},
		{"hello world", "HELLO_WORLD"},
		{"hello-world", "HELLO_WORLD"},
		{"", ""},
		{"a", "A"},
	}

	for _, test := range tests {
		result := ToScreamingSnakeCase(test.input)
		if result != test.expected {
			t.Errorf("ToScreamingSnakeCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToTitleCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello world", "Hello World"},
		{"HELLO WORLD", "Hello World"},
		{"hello-world", "Hello World"},
		{"", ""},
		{"a", "A"},
	}

	for _, test := range tests {
		result := ToTitleCase(test.input)
		if result != test.expected {
			t.Errorf("ToTitleCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

// ==================== String Manipulation Tests ====================

func TestReverse(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "olleh"},
		{"", ""},
		{"a", "a"},
		{"你好世界", "界世好你"}, // Unicode test
		{"A man a plan a canal Panama", "amanaP lanac a nalp a nam A"},
	}

	for _, test := range tests {
		result := Reverse(test.input)
		if result != test.expected {
			t.Errorf("Reverse(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestTruncate(t *testing.T) {
	tests := []struct {
		input    string
		maxLen   int
		suffix   string
		expected string
	}{
		{"hello world", 8, "...", "hello..."},
		{"short", 10, "...", "short"},
		{"hello world", 11, "...", "hello world"},
		{"", 5, "...", ""},
		{"hello", 5, "...", "hello"},
	}

	for _, test := range tests {
		result := Truncate(test.input, test.maxLen, test.suffix)
		if result != test.expected {
			t.Errorf("Truncate(%q, %d, %q) = %q, expected %q", test.input, test.maxLen, test.suffix, result, test.expected)
		}
	}
}

func TestPadLeft(t *testing.T) {
	tests := []struct {
		input    string
		length   int
		padChar  rune
		expected string
	}{
		{"hello", 10, '-', "-----hello"},
		{"hello", 5, '-', "hello"},
		{"hello", 3, '-', "hello"},
		{"", 5, '*', "*****"},
	}

	for _, test := range tests {
		result := PadLeft(test.input, test.length, test.padChar)
		if result != test.expected {
			t.Errorf("PadLeft(%q, %d, %q) = %q, expected %q", test.input, test.length, test.padChar, result, test.expected)
		}
	}
}

func TestPadRight(t *testing.T) {
	tests := []struct {
		input    string
		length   int
		padChar  rune
		expected string
	}{
		{"hello", 10, '-', "hello-----"},
		{"hello", 5, '-', "hello"},
		{"", 5, '*', "*****"},
	}

	for _, test := range tests {
		result := PadRight(test.input, test.length, test.padChar)
		if result != test.expected {
			t.Errorf("PadRight(%q, %d, %q) = %q, expected %q", test.input, test.length, test.padChar, result, test.expected)
		}
	}
}

func TestPadCenter(t *testing.T) {
	tests := []struct {
		input    string
		length   int
		padChar  rune
		expected string
	}{
		{"hi", 6, '-', "--hi--"},
		{"hello", 5, '-', "hello"},
		{"ab", 5, '-', "-ab--"},
	}

	for _, test := range tests {
		result := PadCenter(test.input, test.length, test.padChar)
		if result != test.expected {
			t.Errorf("PadCenter(%q, %d, %q) = %q, expected %q", test.input, test.length, test.padChar, result, test.expected)
		}
	}
}

// ==================== String Validation Tests ====================

func TestIsEmail(t *testing.T) {
	valid := []string{
		"test@example.com",
		"user.name@example.com",
		"user+tag@example.co.uk",
		"user123@subdomain.example.com",
	}

	invalid := []string{
		"invalid",
		"@example.com",
		"user@",
		"user @example.com",
		"user@example",
		"",
	}

	for _, email := range valid {
		if !IsEmail(email) {
			t.Errorf("IsEmail(%q) should be true", email)
		}
	}

	for _, email := range invalid {
		if IsEmail(email) {
			t.Errorf("IsEmail(%q) should be false", email)
		}
	}
}

func TestIsURL(t *testing.T) {
	valid := []string{
		"http://example.com",
		"https://example.com/path",
		"http://subdomain.example.com:8080/path?query=value",
	}

	invalid := []string{
		"example.com",
		"ftp://example.com",
		"",
		"not a url",
	}

	for _, url := range valid {
		if !IsURL(url) {
			t.Errorf("IsURL(%q) should be true", url)
		}
	}

	for _, url := range invalid {
		if IsURL(url) {
			t.Errorf("IsURL(%q) should be false", url)
		}
	}
}

func TestIsUUID(t *testing.T) {
	valid := []string{
		"550e8400-e29b-41d4-a716-446655440000",
		"6ba7b810-9dad-11d1-80b4-00c04fd430c8",
	}

	invalid := []string{
		"not-a-uuid",
		"550e8400-e29b-41d4-a716",
		"",
		"550e8400e29b41d4a716446655440000",
	}

	for _, uuid := range valid {
		if !IsUUID(uuid) {
			t.Errorf("IsUUID(%q) should be true", uuid)
		}
	}

	for _, uuid := range invalid {
		if IsUUID(uuid) {
			t.Errorf("IsUUID(%q) should be false", uuid)
		}
	}
}

func TestIsIPv4(t *testing.T) {
	valid := []string{
		"192.168.1.1",
		"0.0.0.0",
		"255.255.255.255",
		"127.0.0.1",
	}

	invalid := []string{
		"256.1.1.1",
		"192.168.1",
		"192.168.1.1.1",
		"not.an.ip",
		"",
	}

	for _, ip := range valid {
		if !IsIPv4(ip) {
			t.Errorf("IsIPv4(%q) should be true", ip)
		}
	}

	for _, ip := range invalid {
		if IsIPv4(ip) {
			t.Errorf("IsIPv4(%q) should be false", ip)
		}
	}
}

func TestIsEmpty(t *testing.T) {
	if !IsEmpty("") {
		t.Error("IsEmpty('') should be true")
	}
	if !IsEmpty("   ") {
		t.Error("IsEmpty('   ') should be true")
	}
	if !IsEmpty("\t\n") {
		t.Error("IsEmpty('\\t\\n') should be true")
	}
	if IsEmpty("hello") {
		t.Error("IsEmpty('hello') should be false")
	}
}

func TestIsAlpha(t *testing.T) {
	if !IsAlpha("hello") {
		t.Error("IsAlpha('hello') should be true")
	}
	if !IsAlpha("HelloWorld") {
		t.Error("IsAlpha('HelloWorld') should be true")
	}
	if IsAlpha("hello123") {
		t.Error("IsAlpha('hello123') should be false")
	}
	if IsAlpha("") {
		t.Error("IsAlpha('') should be false")
	}
}

func TestIsAlphanumeric(t *testing.T) {
	if !IsAlphanumeric("hello123") {
		t.Error("IsAlphanumeric('hello123') should be true")
	}
	if !IsAlphanumeric("HelloWorld") {
		t.Error("IsAlphanumeric('HelloWorld') should be true")
	}
	if IsAlphanumeric("hello world") {
		t.Error("IsAlphanumeric('hello world') should be false")
	}
	if IsAlphanumeric("") {
		t.Error("IsAlphanumeric('') should be false")
	}
}

func TestIsNumeric(t *testing.T) {
	if !IsNumeric("12345") {
		t.Error("IsNumeric('12345') should be true")
	}
	if !IsNumeric("0") {
		t.Error("IsNumeric('0') should be true")
	}
	if IsNumeric("123.45") {
		t.Error("IsNumeric('123.45') should be false")
	}
	if IsNumeric("") {
		t.Error("IsNumeric('') should be false")
	}
}

func TestIsLower(t *testing.T) {
	if !IsLower("hello") {
		t.Error("IsLower('hello') should be true")
	}
	if IsLower("Hello") {
		t.Error("IsLower('Hello') should be false")
	}
	if IsLower("HELLO") {
		t.Error("IsLower('HELLO') should be false")
	}
	if IsLower("") {
		t.Error("IsLower('') should be false")
	}
}

func TestIsUpper(t *testing.T) {
	if !IsUpper("HELLO") {
		t.Error("IsUpper('HELLO') should be true")
	}
	if IsUpper("Hello") {
		t.Error("IsUpper('Hello') should be false")
	}
	if IsUpper("hello") {
		t.Error("IsUpper('hello') should be false")
	}
	if IsUpper("") {
		t.Error("IsUpper('') should be false")
	}
}

// ==================== String Analysis Tests ====================

func TestWordCount(t *testing.T) {
	tests := []struct {
		input    string
		expected int
	}{
		{"hello world", 2},
		{"one two three four", 4},
		{"", 0},
		{"   ", 0},
		{"single", 1},
		{"multiple   spaces", 2},
	}

	for _, test := range tests {
		result := WordCount(test.input)
		if result != test.expected {
			t.Errorf("WordCount(%q) = %d, expected %d", test.input, result, test.expected)
		}
	}
}

func TestCharCount(t *testing.T) {
	if CharCount("hello") != 5 {
		t.Error("CharCount('hello') should be 5")
	}
	if CharCount("你好") != 2 {
		t.Error("CharCount('你好') should be 2")
	}
	if CharCount("") != 0 {
		t.Error("CharCount('') should be 0")
	}
}

func TestLineCount(t *testing.T) {
	tests := []struct {
		input    string
		expected int
	}{
		{"one\ntwo\nthree", 3},
		{"single line", 1},
		{"", 0},
		{"line1\n", 2},
	}

	for _, test := range tests {
		result := LineCount(test.input)
		if result != test.expected {
			t.Errorf("LineCount(%q) = %d, expected %d", test.input, result, test.expected)
		}
	}
}

func TestCount(t *testing.T) {
	if Count("hello hello hello", "hello") != 3 {
		t.Error("Count should find 3 'hello'")
	}
	if Count("hello", "x") != 0 {
		t.Error("Count should find 0 'x'")
	}
	if Count("hello", "") != 0 {
		t.Error("Count with empty substring should be 0")
	}
}

func TestFrequency(t *testing.T) {
	freq := Frequency("aabbc")
	if freq['a'] != 2 {
		t.Error("Frequency of 'a' should be 2")
	}
	if freq['b'] != 2 {
		t.Error("Frequency of 'b' should be 2")
	}
	if freq['c'] != 1 {
		t.Error("Frequency of 'c' should be 1")
	}
}

func TestWordFrequency(t *testing.T) {
	freq := WordFrequency("hello world hello")
	if freq["hello"] != 2 {
		t.Error("WordFrequency of 'hello' should be 2")
	}
	if freq["world"] != 1 {
		t.Error("WordFrequency of 'world' should be 1")
	}
}

func TestLongestWord(t *testing.T) {
	if LongestWord("hi hello world") != "hello" {
		t.Error("LongestWord should be 'hello'")
	}
	if LongestWord("") != "" {
		t.Error("LongestWord('') should be ''")
	}
}

func TestShortestWord(t *testing.T) {
	if ShortestWord("hello world hi") != "hi" {
		t.Error("ShortestWord should be 'hi'")
	}
	if ShortestWord("") != "" {
		t.Error("ShortestWord('') should be ''")
	}
}

// ==================== String Similarity Tests ====================

func TestLevenshteinDistance(t *testing.T) {
	tests := []struct {
		s1       string
		s2       string
		expected int
	}{
		{"kitten", "sitting", 3},
		{"hello", "hello", 0},
		{"", "hello", 5},
		{"hello", "", 5},
		{"", "", 0},
		{"abc", "xyz", 3},
		{"你好世界", "你好", 2}, // Unicode test
	}

	for _, test := range tests {
		result := LevenshteinDistance(test.s1, test.s2)
		if result != test.expected {
			t.Errorf("LevenshteinDistance(%q, %q) = %d, expected %d", test.s1, test.s2, result, test.expected)
		}
	}
}

func TestSimilarity(t *testing.T) {
	tests := []struct {
		s1       string
		s2       string
		minimum  float64
		maximum  float64
	}{
		{"hello", "hello", 1.0, 1.0},
		{"hello", "", 0.0, 0.0},
		{"", "", 1.0, 1.0},
		{"kitten", "sitting", 0.5, 0.6},
	}

	for _, test := range tests {
		result := Similarity(test.s1, test.s2)
		if result < test.minimum-0.01 || result > test.maximum+0.01 {
			t.Errorf("Similarity(%q, %q) = %f, expected between %f and %f", test.s1, test.s2, result, test.minimum, test.maximum)
		}
	}
}

func TestHammingDistance(t *testing.T) {
	dist, ok := HammingDistance("karolin", "kathrin")
	if !ok || dist != 3 {
		t.Errorf("HammingDistance('karolin', 'kathrin') = %d, expected 3", dist)
	}

	_, ok = HammingDistance("abc", "abcd")
	if ok {
		t.Error("HammingDistance should return false for different length strings")
	}
}

func TestJaroSimilarity(t *testing.T) {
	// Same strings should have similarity of 1
	if JaroSimilarity("hello", "hello") != 1.0 {
		t.Error("JaroSimilarity of same strings should be 1.0")
	}

	// Empty strings
	if JaroSimilarity("", "") != 1.0 {
		t.Error("JaroSimilarity('', '') should be 1.0")
	}

	// One empty string
	if JaroSimilarity("hello", "") != 0.0 {
		t.Error("JaroSimilarity('hello', '') should be 0.0")
	}
}

func TestJaroWinklerSimilarity(t *testing.T) {
	// Same strings should have similarity of 1
	if JaroWinklerSimilarity("hello", "hello") != 1.0 {
		t.Error("JaroWinklerSimilarity of same strings should be 1.0")
	}

	// Jaro-Winkler should be >= Jaro for strings with common prefix
	jaro := JaroSimilarity("hello", "hella")
	jw := JaroWinklerSimilarity("hello", "hella")
	if jw < jaro {
		t.Error("JaroWinklerSimilarity should be >= JaroSimilarity for strings with common prefix")
	}
}

// ==================== String Checks Tests ====================

func TestContains(t *testing.T) {
	if !Contains("Hello World", "world", false) {
		t.Error("Contains with caseSensitive=false should be true")
	}
	if Contains("Hello World", "world", true) {
		t.Error("Contains with caseSensitive=true should be false")
	}
	if !Contains("Hello World", "Hello", true) {
		t.Error("Contains should find 'Hello'")
	}
}

func TestContainsAll(t *testing.T) {
	if !ContainsAll("hello world foo bar", []string{"hello", "world", "foo"}, false) {
		t.Error("ContainsAll should be true")
	}
	if ContainsAll("hello world", []string{"hello", "missing"}, false) {
		t.Error("ContainsAll should be false when substring missing")
	}
}

func TestContainsAny(t *testing.T) {
	if !ContainsAny("hello world", []string{"foo", "world"}, false) {
		t.Error("ContainsAny should be true when at least one substring found")
	}
	if ContainsAny("hello world", []string{"foo", "bar"}, false) {
		t.Error("ContainsAny should be false when no substrings found")
	}
}

func TestStartsWith(t *testing.T) {
	if !StartsWith("Hello World", "hello", false) {
		t.Error("StartsWith with caseSensitive=false should be true")
	}
	if StartsWith("Hello World", "hello", true) {
		t.Error("StartsWith with caseSensitive=true should be false")
	}
}

func TestEndsWith(t *testing.T) {
	if !EndsWith("Hello World", "world", false) {
		t.Error("EndsWith with caseSensitive=false should be true")
	}
	if EndsWith("Hello World", "world", true) {
		t.Error("EndsWith with caseSensitive=true should be false")
	}
}

func TestIsPalindrome(t *testing.T) {
	palindromes := []string{
		"racecar",
		"A man a plan a canal Panama",
		"Was it a car or a cat I saw",
		"12321",
		"a",
		"",
	}

	for _, p := range palindromes {
		if !IsPalindrome(p) {
			t.Errorf("IsPalindrome(%q) should be true", p)
		}
	}

	notPalindromes := []string{
		"hello",
		"world",
		"palindrome",
	}

	for _, p := range notPalindromes {
		if IsPalindrome(p) {
			t.Errorf("IsPalindrome(%q) should be false", p)
		}
	}
}

func TestIsAnagram(t *testing.T) {
	if !IsAnagram("listen", "silent") {
		t.Error("IsAnagram('listen', 'silent') should be true")
	}
	if !IsAnagram("Anagram", "Nag a ram") {
		t.Error("IsAnagram('Anagram', 'Nag a ram') should be true")
	}
	if IsAnagram("hello", "world") {
		t.Error("IsAnagram('hello', 'world') should be false")
	}
}

func TestIsPangram(t *testing.T) {
	pangrams := []string{
		"The quick brown fox jumps over the lazy dog",
		"Pack my box with five dozen liquor jugs",
	}

	for _, p := range pangrams {
		if !IsPangram(p) {
			t.Errorf("IsPangram(%q) should be true", p)
		}
	}

	notPangrams := []string{
		"hello world",
		"not a pangram",
	}

	for _, p := range notPangrams {
		if IsPangram(p) {
			t.Errorf("IsPangram(%q) should be false", p)
		}
	}
}

// ==================== String Transformation Tests ====================

func TestRemoveWhitespace(t *testing.T) {
	if RemoveWhitespace("hello world") != "helloworld" {
		t.Error("RemoveWhitespace should remove spaces")
	}
	if RemoveWhitespace("  hello  ") != "hello" {
		t.Error("RemoveWhitespace should remove leading/trailing spaces")
	}
	if RemoveWhitespace("h\te\nl\tl\to") != "hello" {
		t.Error("RemoveWhitespace should remove tabs and newlines")
	}
}

func TestRemoveAccents(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"café", "cafe"},
		{"naïve", "naive"},
		{"résumé", "resume"},
		{"über", "uber"},
		{"hello", "hello"},
	}

	for _, test := range tests {
		result := RemoveAccents(test.input)
		if result != test.expected {
			t.Errorf("RemoveAccents(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestMask(t *testing.T) {
	result := Mask("1234567890", 2, 2, '*')
	if result != "12******90" {
		t.Errorf("Mask('1234567890', 2, 2, '*') = %q, expected '12******90'", result)
	}

	result = Mask("abc", 1, 1, '*')
	if result != "a*c" {
		t.Errorf("Mask('abc', 1, 1, '*') = %q, expected 'a*c'", result)
	}

	// Test fully masked case
	result = Mask("ab", 1, 1, '*')
	if result != "**" {
		t.Errorf("Mask('ab', 1, 1, '*') = %q, expected '**'", result)
	}
}

func TestMaskEmail(t *testing.T) {
	result := MaskEmail("test@example.com", '*')
	if result[0] != 't' || result[len(result)-1] != 'm' {
		t.Errorf("MaskEmail should preserve first and last char of local part, got %q", result)
	}
}

func TestMaskPhone(t *testing.T) {
	result := MaskPhone("+1 (234) 567-8901", '*')
	// Should show last 4 digits
	if result[len(result)-4:] != "8901" {
		t.Errorf("MaskPhone should show last 4 digits, got %q", result)
	}
}

func TestSwapCase(t *testing.T) {
	if SwapCase("Hello World") != "hELLO wORLD" {
		t.Error("SwapCase('Hello World') should be 'hELLO wORLD'")
	}
	if SwapCase("ABC123xyz") != "abc123XYZ" {
		t.Error("SwapCase should only swap letter case")
	}
}

// ==================== String Utilities Tests ====================

func TestSubstring(t *testing.T) {
	if Substring("hello world", 0, 5) != "hello" {
		t.Error("Substring('hello world', 0, 5) should be 'hello'")
	}
	if Substring("你好世界", 0, 2) != "你好" {
		t.Error("Substring should handle Unicode correctly")
	}
	if Substring("hello", -1, 10) != "hello" {
		t.Error("Substring should handle out of bounds")
	}
}

func TestLeft(t *testing.T) {
	if Left("hello world", 5) != "hello" {
		t.Error("Left('hello world', 5) should be 'hello'")
	}
	if Left("你好世界", 2) != "你好" {
		t.Error("Left should handle Unicode correctly")
	}
	if Left("hi", 5) != "hi" {
		t.Error("Left should return full string if n > length")
	}
}

func TestRight(t *testing.T) {
	if Right("hello world", 5) != "world" {
		t.Error("Right('hello world', 5) should be 'world'")
	}
	if Right("你好世界", 2) != "世界" {
		t.Error("Right should handle Unicode correctly")
	}
}

func TestSplitLines(t *testing.T) {
	lines := SplitLines("one\ntwo\nthree")
	if len(lines) != 3 {
		t.Errorf("SplitLines should return 3 lines, got %d", len(lines))
	}
	if lines[0] != "one" || lines[1] != "two" || lines[2] != "three" {
		t.Error("SplitLines returned wrong lines")
	}
}

func TestChunk(t *testing.T) {
	tests := []struct {
		input    string
		size     int
		expected []string
	}{
		{"hello", 2, []string{"he", "ll", "o"}},
		{"abcdef", 3, []string{"abc", "def"}},
		{"", 2, nil},
		{"a", 2, []string{"a"}},
	}

	for _, test := range tests {
		result := Chunk(test.input, test.size)
		if len(result) != len(test.expected) {
			t.Errorf("Chunk(%q, %d) returned %d chunks, expected %d", test.input, test.size, len(result), len(test.expected))
			continue
		}
		for i, chunk := range result {
			if chunk != test.expected[i] {
				t.Errorf("Chunk(%q, %d)[%d] = %q, expected %q", test.input, test.size, i, chunk, test.expected[i])
			}
		}
	}
}

func TestTemplate(t *testing.T) {
	template := "Hello ${name}, welcome to ${place}!"
	values := map[string]string{
		"name":  "World",
		"place": "Earth",
	}
	expected := "Hello World, welcome to Earth!"
	result := Template(template, values)
	if result != expected {
		t.Errorf("Template() = %q, expected %q", result, expected)
	}
}

// ==================== Fuzzy Matching Tests ====================

func TestFuzzyMatch(t *testing.T) {
	if !FuzzyMatch("hello world", "hlo") {
		t.Error("FuzzyMatch('hello world', 'hlo') should be true")
	}
	if !FuzzyMatch("Hello World", "hlo") {
		t.Error("FuzzyMatch should be case-insensitive")
	}
	if FuzzyMatch("hello", "xyz") {
		t.Error("FuzzyMatch('hello', 'xyz') should be false")
	}
}

func TestFuzzyMatchScore(t *testing.T) {
	// Higher score for better matches
	score1 := FuzzyMatchScore("hello world", "hello")
	score2 := FuzzyMatchScore("hello world", "hlo")
	if score1 <= score2 {
		t.Error("FuzzyMatchScore should be higher for more precise match")
	}

	// Zero score for no match
	score3 := FuzzyMatchScore("hello world", "xyz")
	if score3 != 0 {
		t.Error("FuzzyMatchScore should be 0 for no match")
	}
}

func TestFindBestMatch(t *testing.T) {
	candidates := []string{"apple", "application", "apricot", "banana"}
	best, _ := FindBestMatch("app", candidates)
	if best != "apple" && best != "application" {
		t.Errorf("FindBestMatch('app', candidates) = %q, expected 'apple' or 'application'", best)
	}
}

// ==================== Edge Cases Tests ====================

func TestEmptyStrings(t *testing.T) {
	// All functions should handle empty strings gracefully
	if ToCamelCase("") != "" {
		t.Error("ToCamelCase('') should be ''")
	}
	if Reverse("") != "" {
		t.Error("Reverse('') should be ''")
	}
	if !IsPalindrome("") {
		t.Error("IsPalindrome('') should be true")
	}
	if !IsAnagram("", "") {
		t.Error("IsAnagram('', '') should be true")
	}
}

func TestUnicodeHandling(t *testing.T) {
	// Test with Chinese characters
	_ = ToCamelCase("你好_世界")
	_ = Reverse("你好世界")
	_ = CharCount("你好世界")
	_ = Left("你好世界", 2)

	// Test with emoji
	emoji := "hello🌍world"
	if CharCount(emoji) != 11 {
		t.Errorf("CharCount with emoji should be 11, got %d", CharCount(emoji))
	}
}

func TestLongStrings(t *testing.T) {
	// Test with long strings
	longStr := ""
	for i := 0; i < 10000; i++ {
		longStr += "a"
	}

	// Should not panic
	_ = Reverse(longStr)
	_ = CharCount(longStr)
	_ = IsPalindrome(longStr)
	_ = ToSnakeCase(longStr)
}

// Benchmark tests

func BenchmarkLevenshteinDistance(b *testing.B) {
	for i := 0; i < b.N; i++ {
		LevenshteinDistance("kitten", "sitting")
	}
}

func BenchmarkJaroSimilarity(b *testing.B) {
	for i := 0; i < b.N; i++ {
		JaroSimilarity("hello world", "hello earth")
	}
}

func BenchmarkReverse(b *testing.B) {
	str := "hello world this is a test string"
	for i := 0; i < b.N; i++ {
		Reverse(str)
	}
}

func BenchmarkToSnakeCase(b *testing.B) {
	str := "thisIsACamelCaseStringForTesting"
	for i := 0; i < b.N; i++ {
		ToSnakeCase(str)
	}
}

func BenchmarkFuzzyMatchScore(b *testing.B) {
	for i := 0; i < b.N; i++ {
		FuzzyMatchScore("hello world this is a test", "hello test")
	}
}

func BenchmarkWordCount(b *testing.B) {
	str := "The quick brown fox jumps over the lazy dog"
	for i := 0; i < b.N; i++ {
		WordCount(str)
	}
}