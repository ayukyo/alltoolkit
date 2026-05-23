package typography_utils

import (
	"strings"
	"testing"
)

// ==================== Smart Quotes Tests ====================

func TestSmartQuotes(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"He said \"hello\".", "He said \"hello\"."},
		{"\"Hello\" and \"World\"", "\"Hello\" and \"World\""},
		{"It's a test.", "It's a test."},
		{"Don't worry.", "Don't worry."},
		{"'Tis the season.", "'Tis the season."},
	}

	for _, test := range tests {
		result := SmartQuotes(test.input)
		if result != test.expected {
			t.Errorf("SmartQuotes(%s) = %s, expected %s", test.input, result, test.expected)
		}
	}
}

func TestStraightenQuotes(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"He said \"hello\".", "He said \"hello\"."},
		{"It's a test.", "It's a test."},
		{"«quoted»", "\"quoted\""},
		{"『quoted』", "\"quoted\""},
	}

	for _, test := range tests {
		result := StraightenQuotes(test.input)
		if result != test.expected {
			t.Errorf("StraightenQuotes(%s) = %s, expected %s", test.input, result, test.expected)
		}
	}
}

// ==================== Dash Normalization Tests ====================

func TestNormalizeDashes(t *testing.T) {
	tests := []struct {
		input    string
		style    DashStyle
		expected string
	}{
		{"pages 10--20", DashStyleAuto, "pages 10–20"},
		{"pages 10--20", DashStyleEn, "pages 10–20"},
		{"pages 10--20", DashStyleEm, "pages 10—20"},
		{"pages 10--20", DashStyleHyphen, "pages 10-20"},
		{"thought -- or idea", DashStyleAuto, "thought — or idea"},
		{"thought -- or idea", DashStyleEm, "thought — or idea"},
	}

	for _, test := range tests {
		result := NormalizeDashes(test.input, test.style)
		if result != test.expected {
			t.Errorf("NormalizeDashes(%s, %v) = %s, expected %s", test.input, test.style, result, test.expected)
		}
	}
}

func TestEmDash(t *testing.T) {
	input := "thought -- or idea"
	expected := "thought — or idea"
	result := EmDash(input)
	if result != expected {
		t.Errorf("EmDash(%s) = %s, expected %s", input, result, expected)
	}
}

func TestEnDash(t *testing.T) {
	input := "pages 10--20"
	expected := "pages 10–20"
	result := EnDash(input)
	if result != expected {
		t.Errorf("EnDash(%s) = %s, expected %s", input, result, expected)
	}
}

// ==================== Ellipsis Normalization Tests ====================

func TestNormalizeEllipsis(t *testing.T) {
	tests := []struct {
		input    string
		useChar  bool
		expected string
	}{
		{"Wait...", true, "Wait…"},
		{"Wait...", false, "Wait..."},
		{"Wait....", true, "Wait…"},
		{"Wait. . .", true, "Wait…"},
		{"Wait……", true, "Wait…"},
	}

	for _, test := range tests {
		result := NormalizeEllipsis(test.input, test.useChar)
		if result != test.expected {
			t.Errorf("NormalizeEllipsis(%s, %v) = %s, expected %s", test.input, test.useChar, result, test.expected)
		}
	}
}

// ==================== Smartify Tests ====================

func TestSmartify(t *testing.T) {
	input := "He said \"Hello World\"... this is a test -- really!"
	expected := "He said \"Hello World\"… this is a test — really!"
	result := Smartify(input)
	if result != expected {
		t.Errorf("Smartify(%s) = %s, expected %s", input, result, expected)
	}
}

// ==================== Text Wrapping Tests ====================

func TestWrapText(t *testing.T) {
	tests := []struct {
		input    string
		width    int
		expected string
	}{
		{"Short line", 20, "Short line"},
		{"This is a long text that needs wrapping", 20, "This is a long text\nthat needs wrapping"},
		{"Line1\nLine2\nLine3", 10, "Line1\nLine2\nLine3"},
	}

	for _, test := range tests {
		result := WrapText(test.input, test.width)
		if result != test.expected {
			t.Errorf("WrapText(%s, %d) = %s, expected %s", test.input, test.width, result, test.expected)
		}
	}
}

func TestWrapParagraphs(t *testing.T) {
	input := "First paragraph with some text.\n\nSecond paragraph here."
	width := 20
	result := WrapParagraphs(input, width)
	
	// Should have two paragraphs separated by double newline
	if strings.Count(result, "\n\n") != 1 {
		t.Errorf("WrapParagraphs should preserve paragraph breaks")
	}
}

// ==================== Whitespace Normalization Tests ====================

func TestNormalizeSpaces(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"  hello   world  ", "hello world"},
		{"line1  \n  line2  ", "line1\nline2"},
		{"text\n\n\n\nmore", "text\n\nmore"},
	}

	for _, test := range tests {
		result := NormalizeSpaces(test.input)
		if result != test.expected {
			t.Errorf("NormalizeSpaces(%s) = %s, expected %s", test.input, result, test.expected)
		}
	}
}

func TestRemoveExtraBlankLines(t *testing.T) {
	input := "line1\n\n\n\n\n\nline2"
	expected := "line1\n\n\nline2"
	result := RemoveExtraBlankLines(input, 2)
	if result != expected {
		t.Errorf("RemoveExtraBlankLines(%s, 2) = %s, expected %s", input, result, expected)
	}
}

// ==================== Character Statistics Tests ====================

func TestGetTextStatistics(t *testing.T) {
	text := "Hello world. How are you today? I am fine!"
	stats := GetTextStatistics(text)

	if stats.Words != 9 {
		t.Errorf("Expected 9 words, got %d", stats.Words)
	}

	if stats.Sentences != 3 {
		t.Errorf("Expected 3 sentences, got %d", stats.Sentences)
	}

	if stats.Lines != 1 {
		t.Errorf("Expected 1 line, got %d", stats.Lines)
	}
}

func TestGetTextStatisticsWithChinese(t *testing.T) {
	text := "Hello 世界. This is 测试."
	stats := GetTextStatistics(text)

	if stats.ChineseChars != 4 {
		t.Errorf("Expected 4 Chinese chars (世界+测试), got %d", stats.ChineseChars)
	}

	if stats.EnglishWords < 3 {
		t.Errorf("Expected at least 3 English words, got %d", stats.EnglishWords)
	}
}

func TestCountWords(t *testing.T) {
	tests := []struct {
		input    string
		expected int
	}{
		{"Hello world", 2},
		{"你好世界", 4},
		{"Hello 世界 test", 4},
		{"", 0},
	}

	for _, test := range tests {
		result := CountWords(test.input)
		if result != test.expected {
			t.Errorf("CountWords(%s) = %d, expected %d", test.input, result, test.expected)
		}
	}
}

func TestCountSentences(t *testing.T) {
	tests := []struct {
		input    string
		expected int
	}{
		{"Hello world.", 1},
		{"Hello! How are you?", 2},
		{"你好。世界！", 2},
		{"", 0},
	}

	for _, test := range tests {
		result := CountSentences(test.input)
		if result != test.expected {
			t.Errorf("CountSentences(%s) = %d, expected %d", test.input, result, test.expected)
		}
	}
}

// ==================== HTML Escaping Tests ====================

func TestEscapeHTML(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"<div>Hello</div>", "&lt;div&gt;Hello&lt;/div&gt;"},
		{"Hello & Goodbye", "Hello &amp; Goodbye"},
		{"\"quoted\"", "&quot;quoted&quot;"},
	}

	for _, test := range tests {
		result := EscapeHTML(test.input)
		if result != test.expected {
			t.Errorf("EscapeHTML(%s) = %s, expected %s", test.input, result, test.expected)
		}
	}
}

func TestUnescapeHTML(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"&lt;div&gt;Hello&lt;/div&gt;", "<div>Hello</div>"},
		{"Hello &amp; Goodbye", "Hello & Goodbye"},
		{"&copy; 2024", "© 2024"},
	}

	for _, test := range tests {
		result := UnescapeHTML(test.input)
		if result != test.expected {
			t.Errorf("UnescapeHTML(%s) = %s, expected %s", test.input, result, test.expected)
		}
	}
}

// ==================== Markdown Escaping Tests ====================

func TestEscapeMarkdown(t *testing.T) {
	input := "# Hello **World**"
	expected := "\\# Hello \\*\\*World\\*\\*"
	result := EscapeMarkdown(input)
	if result != expected {
		t.Errorf("EscapeMarkdown(%s) = %s, expected %s", input, result, expected)
	}
}

// ==================== Title Case Tests ====================

func TestTitleCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"the quick brown fox", "The Quick Brown Fox"},
		{"the lord of the rings", "The Lord of the Rings"},
		{"HELLO WORLD", "Hello World"},
	}

	for _, test := range tests {
		result := TitleCase(test.input)
		if result != test.expected {
			t.Errorf("TitleCase(%s) = %s, expected %s", test.input, result, test.expected)
		}
	}
}

// ==================== Slugify Tests ====================

func TestSlugify(t *testing.T) {
	tests := []struct {
		input      string
		separator  string
		lowercase  bool
		expected   string
	}{
		{"Hello World!", "-", true, "hello-world"},
		{"This is a Test", "_", true, "this_is_a_test"},
		{"你好世界", "-", true, "你好世界"},
		{"Hello  World", "-", true, "hello-world"},
	}

	for _, test := range tests {
		result := Slugify(test.input, test.separator, test.lowercase)
		if result != test.expected {
			t.Errorf("Slugify(%s, %s, %v) = %s, expected %s", test.input, test.separator, test.lowercase, result, test.expected)
		}
	}
}

// ==================== Alignment Tests ====================

func TestAlignLeft(t *testing.T) {
	input := "Hello"
	width := 10
	expected := "Hello     "
	result := AlignLeft(input, width, " ")
	if result != expected {
		t.Errorf("AlignLeft(%s, %d) = %s, expected %s", input, width, result, expected)
	}
}

func TestAlignRight(t *testing.T) {
	input := "Hello"
	width := 10
	expected := "     Hello"
	result := AlignRight(input, width, " ")
	if result != expected {
		t.Errorf("AlignRight(%s, %d) = %s, expected %s", input, width, result, expected)
	}
}

func TestAlignCenter(t *testing.T) {
	input := "Hello"
	width := 10
	expected := "  Hello   "
	result := AlignCenter(input, width, " ")
	if result != expected {
		t.Errorf("AlignCenter(%s, %d) = %s, expected %s", input, width, result, expected)
	}
}

func TestAlignJustify(t *testing.T) {
	input := "Hello world this is"
	width := 20
	result := AlignJustify(input, width)
	
	// Should be exactly width characters
	if len(result) != width {
		t.Errorf("AlignJustify result length should be %d, got %d", width, len(result))
	}
}

// ==================== Line Numbers Tests ====================

func TestAddLineNumbers(t *testing.T) {
	input := "Hello\nWorld"
	start := 1
	width := 4
	result := AddLineNumbers(input, start, width)

	// Should have line numbers
	if !strings.Contains(result, "   1") {
		t.Errorf("AddLineNumbers should include line number 1")
	}
	if !strings.Contains(result, "   2") {
		t.Errorf("AddLineNumbers should include line number 2")
	}
}

// ==================== Chinese Typography Tests ====================

func TestNormalizeChinesePunctuation(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"你好,世界!", "你好，世界！"},
		{"This is (test)", "This is （test）"},
	}

	for _, test := range tests {
		result := NormalizeChinesePunctuation(test.input)
		if result != test.expected {
			t.Errorf("NormalizeChinesePunctuation(%s) = %s, expected %s", test.input, result, test.expected)
		}
	}
}

func TestChineseParagraphIndent(t *testing.T) {
	input := "第一段\n\n第二段"
	indent := "　　"
	result := ChineseParagraphIndent(input, indent)

	// Should have indent at start of each paragraph
	if !strings.HasPrefix(result, indent) {
		t.Errorf("ChineseParagraphIndent should add indent at start")
	}
	if !strings.Contains(result, "\n\n"+indent) {
		t.Errorf("ChineseParagraphIndent should add indent to second paragraph")
	}
}

// ==================== Quote Style Tests ====================

func TestQuoteStyles(t *testing.T) {
	defaultStyle := DefaultQuoteStyle()
	if defaultStyle.LeftDouble != "\"" {
		t.Errorf("DefaultQuoteStyle LeftDouble should be \"")
	}

	chineseStyle := ChineseQuoteStyle()
	if chineseStyle.LeftDouble != "\"" {
		t.Errorf("ChineseQuoteStyle LeftDouble should be \"")
	}

	straightStyle := StraightQuoteStyle()
	if straightStyle.LeftDouble != "\"" {
		t.Errorf("StraightQuoteStyle LeftDouble should be \"")
	}
}

// ==================== Benchmarks ====================

func BenchmarkSmartQuotes(b *testing.B) {
	text := "He said \"hello\" and she said \"world\"... it's a test -- really!"
	for i := 0; i < b.N; i++ {
		SmartQuotes(text)
	}
}

func BenchmarkSmartify(b *testing.B) {
	text := "He said \"Hello World\"... this is a test -- really!"
	for i := 0; i < b.N; i++ {
		Smartify(text)
	}
}

func BenchmarkNormalizeSpaces(b *testing.B) {
	text := "  hello   world  \n  line2  "
	for i := 0; i < b.N; i++ {
		NormalizeSpaces(text)
	}
}

func BenchmarkGetTextStatistics(b *testing.B) {
	text := "Hello world. How are you today? I am fine! This is a longer text with more sentences."
	for i := 0; i < b.N; i++ {
		GetTextStatistics(text)
	}
}