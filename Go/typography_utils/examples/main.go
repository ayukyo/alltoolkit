// Example usage of typography_utils package
package main

import (
	"fmt"
	"strings"

	typography_utils "github.com/yourusername/alltoolkit/Go/typography_utils"
)

func main() {
	fmt.Println("=== Typography Utils Demo ===")
	fmt.Println()

	// === Smart Quotes ===
	fmt.Println("--- Smart Quotes ---")
	original := "He said \"Hello World\"... wait -- I mean \"Hi\"."
	smart := typography_utils.Smartify(original)
	fmt.Println("Original:", original)
	fmt.Println("Smartified:", smart)
	fmt.Println()

	// === Dash Normalization ===
	fmt.Println("--- Dash Normalization ---")
	rangeText := "pages 10--20, chapters 1--5"
	enDash := typography_utils.EnDash(rangeText)
	emDash := typography_utils.EmDash("thought -- or idea")
	fmt.Println("En dash for ranges:", enDash)
	fmt.Println("Em dash for breaks:", emDash)
	fmt.Println()

	// === Ellipsis ===
	fmt.Println("--- Ellipsis Normalization ---")
	ellipsisText := "Wait...... then go"
	normalized := typography_utils.NormalizeEllipsis(ellipsisText, true)
	fmt.Println("Original:", ellipsisText)
	fmt.Println("Normalized:", normalized)
	fmt.Println()

	// === Text Statistics ===
	fmt.Println("--- Text Statistics ---")
	statsText := "Hello world. How are you today? I am fine!"
	stats := typography_utils.GetTextStatistics(statsText)
	fmt.Println("Text:", statsText)
	fmt.Printf("Characters: %d\n", stats.Chars)
	fmt.Printf("Words: %d\n", stats.Words)
	fmt.Printf("Sentences: %d\n", stats.Sentences)
	fmt.Println()

	// === Chinese Text ===
	fmt.Println("--- Chinese Typography ---")
	chineseText := "你好,世界!这是一个测试."
	chineseNormalized := typography_utils.NormalizeChinesePunctuation(chineseText)
	fmt.Println("Original:", chineseText)
	fmt.Println("Normalized:", chineseNormalized)

	chinesePara := "第一段内容\n\n第二段内容"
	indented := typography_utils.ChineseParagraphIndent(chinesePara, "　　")
	fmt.Println("Paragraph indent:")
	fmt.Println(indented)
	fmt.Println()

	// === Title Case ===
	fmt.Println("--- Title Case ---")
	title := typography_utils.TitleCase("the lord of the rings")
	fmt.Println("Title:", title)
	fmt.Println()

	// === Slugify ===
	fmt.Println("--- Slugify ---")
	slug := typography_utils.Slugify("Hello World! How are you?", "-", true)
	fmt.Println("Slug:", slug)
	fmt.Println()

	// === Text Wrapping ===
	fmt.Println("--- Text Wrapping ---")
	longText := "This is a very long text that needs to be wrapped at a specific width for better readability."
	wrapped := typography_utils.WrapText(longText, 30)
	fmt.Println("Wrapped at 30 chars:")
	fmt.Println(wrapped)
	fmt.Println()

	// === Alignment ===
	fmt.Println("--- Text Alignment ---")
	alignText := "Hello"
	fmt.Println("Left aligned:", typography_utils.AlignLeft(alignText, 10, " "))
	fmt.Println("Right aligned:", typography_utils.AlignRight(alignText, 10, " "))
	fmt.Println("Center aligned:", typography_utils.AlignCenter(alignText, 10, " "))
	fmt.Println()

	// === Line Numbers ===
	fmt.Println("--- Line Numbers ---")
	codeText := "line one\nline two\nline three"
	withNumbers := typography_utils.AddLineNumbers(codeText, 1, 4)
	fmt.Println("With line numbers:")
	fmt.Println(withNumbers)
	fmt.Println()

	// === HTML Escaping ===
	fmt.Println("--- HTML Escaping ---")
	htmlText := "<div>Hello & Goodbye</div>"
	escaped := typography_utils.EscapeHTML(htmlText)
	fmt.Println("Original:", htmlText)
	fmt.Println("Escaped:", escaped)
	fmt.Println("Unescaped:", typography_utils.UnescapeHTML(escaped))
	fmt.Println()

	// === Markdown Escaping ===
	fmt.Println("--- Markdown Escaping ---")
	mdText := "# Hello **World**"
	mdEscaped := typography_utils.EscapeMarkdown(mdText)
	fmt.Println("Original:", mdText)
	fmt.Println("Escaped:", mdEscaped)
	fmt.Println()

	// === Whitespace Normalization ===
	fmt.Println("--- Whitespace Normalization ---")
	messyText := "  hello   world  \n\n\n\n  extra  spaces  "
	clean := typography_utils.NormalizeSpaces(messyText)
	fmt.Println("Original:", messyText)
	fmt.Println("Cleaned:", clean)
	fmt.Println()

	// === Combined Processing ===
	fmt.Println("--- Combined Processing Example ---")
	rawText := `  He said "Hello"... wait -- let me think...
This is a test.  How are you?  
`
	processed := typography_utils.Smartify(rawText)
	processed = typography_utils.NormalizeSpaces(processed)
	processed = typography_utils.WrapText(processed, 40)
	fmt.Println("Raw input:")
	fmt.Println(rawText)
	fmt.Println("Processed output:")
	fmt.Println(processed)

	// === Statistics on processed text ===
	fmt.Println()
	fmt.Println("--- Statistics on Mixed Content ---")
	mixedText := "Hello 世界. This is 测试 text. 你好吗?"
	mixedStats := typography_utils.GetTextStatistics(mixedText)
	fmt.Println("Mixed text:", mixedText)
	fmt.Printf("Total words: %d\n", mixedStats.Words)
	fmt.Printf("Chinese chars: %d\n", mixedStats.ChineseChars)
	fmt.Printf("English words: %d\n", mixedStats.EnglishWords)
	fmt.Printf("Sentences: %d\n", mixedStats.Sentences)
}