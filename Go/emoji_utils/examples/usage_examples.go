// Example usage of emoji_utils package
package main

import (
	"fmt"
	"strings"

	emoji_utils "github.com/ayukyo/alltoolkit/Go/emoji_utils"
)

func main() {
	fmt.Println("=== Emoji Utils 示例 ===")
	fmt.Println()

	// 1. 检测Emoji
	fmt.Println("1. 检测 Emoji")
	fmt.Println("   IsEmoji('😀'):", emoji_utils.IsEmoji('😀'))
	fmt.Println("   IsEmoji('A'):", emoji_utils.IsEmoji('A'))
	fmt.Println()

	// 2. 检查字符串是否包含Emoji
	fmt.Println("2. 检查字符串是否包含 Emoji")
	texts := []string{
		"Hello World",
		"Hello 😀 World",
		"🎉 Party time!",
		"No emojis here",
	}
	for _, text := range texts {
		fmt.Printf("   ContainsEmoji(%q): %v\n", text, emoji_utils.ContainsEmoji(text))
	}
	fmt.Println()

	// 3. 统计Emoji数量
	fmt.Println("3. 统计 Emoji 数量")
	fmt.Printf("   CountEmoji('Hello 😀 World'): %d\n", emoji_utils.CountEmoji("Hello 😀 World"))
	fmt.Printf("   CountEmoji('😀😃😄'): %d\n", emoji_utils.CountEmoji("😀😃😄"))
	fmt.Printf("   CountEmoji('🎉🎉🎉 Party!'): %d\n", emoji_utils.CountEmoji("🎉🎉🎉 Party!"))
	fmt.Println()

	// 4. 提取Emoji
	fmt.Println("4. 提取 Emoji")
	text := "Hello 😀 World 🎉 Have a great day! ❤️"
	emojis := emoji_utils.ExtractEmoji(text)
	fmt.Printf("   Text: %q\n", text)
	fmt.Printf("   Emojis: %v\n", emojis)
	fmt.Println()

	// 5. 移除Emoji
	fmt.Println("5. 移除 Emoji")
	fmt.Printf("   RemoveEmoji('Hello 😀 World'): %q\n", emoji_utils.RemoveEmoji("Hello 😀 World"))
	fmt.Printf("   RemoveEmoji('🎉 Test 🎊 Here 🥳'): %q\n", emoji_utils.RemoveEmoji("🎉 Test 🎊 Here 🥳"))
	fmt.Println()

	// 6. 替换Emoji
	fmt.Println("6. 替换 Emoji")
	fmt.Printf("   ReplaceEmoji('Hello 😀', '[EMOJI]'): %q\n", emoji_utils.ReplaceEmoji("Hello 😀", "[EMOJI]"))
	fmt.Printf("   ReplaceEmoji('😀😃😄', '*'): %q\n", emoji_utils.ReplaceEmoji("😀😃😄", "*"))
	fmt.Println()

	// 7. 获取Emoji分类
	fmt.Println("7. 获取 Emoji 分类")
	categories := []struct {
		emoji string
		name  string
	}{
		{"😀", "笑脸"},
		{"👍", "点赞"},
		{"🐶", "动物"},
		{"🍎", "食物"},
		{"🚗", "旅行"},
		{"⚽", "运动"},
		{"📱", "物品"},
		{"❤", "符号"},
	}
	for _, item := range categories {
		cat := emoji_utils.GetEmojiCategory(item.emoji)
		fmt.Printf("   %s (%s): %s\n", item.emoji, item.name, cat)
	}
	fmt.Println()

	// 8. 获取Emoji详细信息
	fmt.Println("8. 获取 Emoji 详细信息")
	info := emoji_utils.GetEmojiInfo("😀")
	fmt.Printf("   Emoji: %s\n", info.Emoji)
	fmt.Printf("   Name: %s\n", info.Name)
	fmt.Printf("   Category: %s\n", info.Category)
	fmt.Printf("   CodePoints: %v\n", emoji_utils.EmojiToCodePoints(info.Emoji))
	fmt.Printf("   IsComposite: %v\n", info.IsComposite)
	fmt.Println()

	// 9. Emoticon 转 Emoji
	fmt.Println("9. Emoticon 转 Emoji")
	emoticonTexts := []string{
		"Hello :) How are you?",
		"I'm so happy :D",
		"Love you <3",
		"That's sad :(",
		";) Wink!",
	}
	for _, et := range emoticonTexts {
		converted := emoji_utils.EmoticonToEmoji(et)
		fmt.Printf("   %q -> %q\n", et, converted)
	}
	fmt.Println()

	// 10. Emoji 转 Unicode 码点
	fmt.Println("10. Emoji 转 Unicode 码点")
	codePoints := emoji_utils.EmojiToCodePoints("😀")
	fmt.Printf("   😀 -> %v\n", codePoints)
	codePoints = emoji_utils.EmojiToCodePoints("❤")
	fmt.Printf("   ❤ -> %v\n", codePoints)
	fmt.Println()

	// 11. Unicode 码点转 Emoji
	fmt.Println("11. Unicode 码点转 Emoji")
	emoji, err := emoji_utils.CodePointsToEmoji([]string{"U+1F600"})
	if err != nil {
		fmt.Printf("   Error: %v\n", err)
	} else {
		fmt.Printf("   U+1F600 -> %s\n", emoji)
	}
	emoji, err = emoji_utils.CodePointsToEmoji([]string{"0x2764"})
	if err != nil {
		fmt.Printf("   Error: %v\n", err)
	} else {
		fmt.Printf("   0x2764 -> %s\n", emoji)
	}
	fmt.Println()

	// 12. 计算Emoji显示长度
	fmt.Println("12. 计算 Emoji 显示长度")
	fmt.Printf("   EmojiLength('Hello'): %d (5 chars)\n", emoji_utils.EmojiLength("Hello"))
	fmt.Printf("   EmojiLength('Hello 😀'): %d (5 + space + emoji)\n", emoji_utils.EmojiLength("Hello 😀"))
	fmt.Printf("   EmojiLength('😀😃😄'): %d (3 emojis)\n", emoji_utils.EmojiLength("😀😃😄"))
	fmt.Println()

	// 13. 按Emoji分割文本
	fmt.Println("13. 按 Emoji 分割文本")
	segments := emoji_utils.SplitByEmoji("Hello 😀 World 🎉 Test")
	fmt.Println("   Segments:")
	for i, seg := range segments {
		emojiLabel := "Text"
		if seg.IsEmoji {
			emojiLabel = "Emoji"
		}
		fmt.Printf("      [%d] %s: %q\n", i, emojiLabel, seg.Text)
	}
	fmt.Println()

	// 14. 获取分类下的所有Emoji
	fmt.Println("14. 获取分类下的所有 Emoji")
	fmt.Println("   Faces:", strings.Join(emoji_utils.GetEmojisByCategory(emoji_utils.CategoryFaces)[:5], " "), "...")
	fmt.Println("   Animals:", strings.Join(emoji_utils.GetEmojisByCategory(emoji_utils.CategoryAnimals)[:5], " "), "...")
	fmt.Println("   Food:", strings.Join(emoji_utils.GetEmojisByCategory(emoji_utils.CategoryFood)[:5], " "), "...")
	fmt.Println()

	// 15. 验证Emoji
	fmt.Println("15. 验证 Emoji")
	validateTests := []string{"😀", "❤", "Hello", "", "🎉"}
	for _, vt := range validateTests {
		fmt.Printf("   ValidateEmoji(%q): %v\n", vt, emoji_utils.ValidateEmoji(vt))
	}
	fmt.Println()

	// 16. 检查是否仅包含Emoji
	fmt.Println("16. 检查是否仅包含 Emoji")
	onlyTests := []string{
		"😀😃😄",
		"😀 😃", // 带空格
		"Hello 😀",
		"   ", // 仅空格
	}
	for _, ot := range onlyTests {
		fmt.Printf("   IsEmojiOnly(%q): %v\n", ot, emoji_utils.IsEmojiOnly(ot))
	}
	fmt.Println()

	// 17. 移除修饰符
	fmt.Println("17. 移除修饰符")
	fmt.Printf("   StripSkinToneModifiers('👍'): %s\n", emoji_utils.StripSkinToneModifiers("👍"))
	fmt.Printf("   StripSkinToneModifiers('👍🏻'): %s\n", emoji_utils.StripSkinToneModifiers("👍🏻"))
	fmt.Printf("   StripVariationSelectors('❤️'): %s\n", emoji_utils.StripVariationSelectors("❤️"))
	fmt.Printf("   NormalizeEmoji('👍🏻'): %s\n", emoji_utils.NormalizeEmoji("👍🏻"))
	fmt.Println()

	// 18. 实际应用示例
	fmt.Println("18. 实际应用示例")
	fmt.Println("   --- 过滤用户评论中的 Emoji ---")
	comment := "This is an AMAZING product! 😍😍😍 I love it so much! ❤️👍🎉"
	cleanComment := emoji_utils.RemoveEmoji(comment)
	fmt.Printf("   Original: %s\n", comment)
	fmt.Printf("   Clean: %s\n", cleanComment)
	fmt.Println()

	fmt.Println("   --- 统计消息中的 Emoji 数量 ---")
	message := "Hello! 👋 How are you? 😊 I hope you're doing great! 🎉🌟✨"
	count := emoji_utils.CountEmoji(message)
	fmt.Printf("   Message: %s\n", message)
	fmt.Printf("   Emoji count: %d\n", count)
	fmt.Println()

	fmt.Println("   --- 分析 Emoji 分布 ---")
	text2 := "I love cats 🐱 dogs 🐶 and birds 🐦! My favorites are 😺 😻!"
	emojis2 := emoji_utils.ExtractEmoji(text2)
	categoryCount := make(map[emoji_utils.EmojiCategory]int)
	for _, e := range emojis2 {
		cat := emoji_utils.GetEmojiCategory(e)
		categoryCount[cat]++
	}
	fmt.Printf("   Text: %s\n", text2)
	fmt.Println("   Category distribution:")
	for cat, cnt := range categoryCount {
		fmt.Printf("      %s: %d\n", cat, cnt)
	}

	fmt.Println()
	fmt.Println("=== 示例完成 ===")
}