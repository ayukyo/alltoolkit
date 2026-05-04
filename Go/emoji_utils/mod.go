// Package emoji_utils provides emoji-related utilities without external dependencies.
// It offers encoding, decoding, extraction, classification, and validation for emoji.
package emoji_utils

import (
	"unicode"
	"unicode/utf8"
)

// EmojiCategory represents the category of an emoji
type EmojiCategory string

const (
	CategoryFaces        EmojiCategory = "Faces"
	CategoryPeople       EmojiCategory = "People"
	CategoryAnimals      EmojiCategory = "Animals"
	CategoryFood         EmojiCategory = "Food"
	CategoryTravel       EmojiCategory = "Travel"
	CategoryActivities    EmojiCategory = "Activities"
	CategoryObjects      EmojiCategory = "Objects"
	CategorySymbols      EmojiCategory = "Symbols"
	CategoryFlags        EmojiCategory = "Flags"
	CategoryUnknown      EmojiCategory = "Unknown"
)

// EmojiInfo contains detailed information about an emoji
type EmojiInfo struct {
	Emoji       string        // The emoji character
	Name        string        // Human-readable name
	Category    EmojiCategory // Category classification
	CodePoints  []rune        // Unicode code points
	IsComposite bool          // True if made of multiple code points
}

// EmojiRange defines a range of emoji code points
type EmojiRange struct {
	Start rune
	End   rune
	Name  string
}

// Common emoji ranges for detection
var emojiRanges = []EmojiRange{
	{0x1F600, 0x1F64F, "Emoticons"},       // 😀-🙏
	{0x1F300, 0x1F5FF, "Misc Symbols"},    // 🌀-🗿
	{0x1F680, 0x1F6FF, "Transport"},       // 🚀-🛿
	{0x1F900, 0x1F9FF, "Supplemental"},   // 🤀-🧿
	{0x1FA00, 0x1FA6F, "Chess"},          // 🨀-🩿
	{0x1FA70, 0x1FAFF, "Symbols-Pict"},   // 🩰-🫿
	{0x2600, 0x27BF, "Misc Symbols & Dingbats"}, // ☀-➿ (includes watch ⌚, keyboard ⌨)
	{0x1F000, 0x1F02F, "Mahjong"},        // 🀀-🀿
	{0x1F0A0, 0x1F0FF, "Playing Cards"},  // 🂠-🃿
	{0xFE00, 0xFE0F, "Variation Selectors"},
	{0x1F1E6, 0x1F1FF, "Regional Indicators"}, // 🇦-🇿
	{0x231A, 0x231B, "Watch"},            // ⌚ ⌛
	{0x23E9, 0x23F3, "Media Controls"},   // ⏩-⏳
	{0x23F8, 0x23FA, "Media Controls"},   // ⏸-⏺
	{0x25AA, 0x25AB, "Shapes"},           // ▪ ▫
	{0x25B6, 0x25C0, "Shapes"},           // ▶ ◀
	{0x25FB, 0x25FE, "Shapes"},           // ◻-◾
	{0x2614, 0x2615, "Weather"},          // ☔ ☕
	{0x2648, 0x2653, "Zodiac"},           // ♈-♓
	{0x267F, 0x267F, "Accessibility"},   // ♿
	{0x2693, 0x2693, "Objects"},          // ⚓
	{0x26A1, 0x26A1, "Weather"},          // ⚡
	{0x26AA, 0x26AB, "Shapes"},           // ⚪ ⚫
	{0x26BD, 0x26BE, "Sports"},           // ⚽ ⚾
	{0x26C4, 0x26C5, "Weather"},          // ⛄ ⛅
	{0x26CE, 0x26CE, "Zodiac"},           // ⛎
	{0x26D4, 0x26D4, "Signs"},            // ⛔
	{0x26EA, 0x26EA, "Buildings"},        // ⛪
	{0x26F2, 0x26F3, "Places"},           // ⛲ ⛳
	{0x26F5, 0x26F5, "Transport"},        // ⛵
	{0x26FA, 0x26FA, "Places"},           // ⛺
	{0x26FD, 0x26FD, "Transport"},        // ⛽
	{0x2702, 0x2702, "Objects"},          // ✂
	{0x2705, 0x2705, "Symbols"},          // ✅
	{0x2708, 0x270D, "Transport/Objects"}, // ✈-✍
	{0x270F, 0x270F, "Objects"},          // ✏
	{0x2712, 0x2712, "Objects"},          // ✒
	{0x2714, 0x2714, "Symbols"},          // ✔
	{0x2716, 0x2716, "Symbols"},          // ✖
	{0x271D, 0x271D, "Symbols"},          // ✝
	{0x2721, 0x2721, "Symbols"},          // ✡
	{0x2728, 0x2728, "Symbols"},          // ✨
	{0x2733, 0x2734, "Symbols"},          // ✳ ✴
	{0x2744, 0x2744, "Weather"},          // ❄
	{0x2747, 0x2747, "Symbols"},          // ❇
	{0x274C, 0x274C, "Symbols"},          // ❌
	{0x274E, 0x274E, "Symbols"},          // ❎
	{0x2753, 0x2755, "Symbols"},          // ❓-❕
	{0x2757, 0x2757, "Symbols"},          // ❗
	{0x2763, 0x2764, "Symbols"},          // ❣ ❤
	{0x2795, 0x2797, "Math"},             // ➕-➗
	{0x27A1, 0x27A1, "Arrows"},           // ➡
	{0x27B0, 0x27B0, "Symbols"},          // ➰
	{0x27BF, 0x27BF, "Symbols"},          // ➿
	{0x2934, 0x2935, "Arrows"},           // ⤴ ⤵
	{0x2B05, 0x2B07, "Arrows"},           // ⬅-⬇
	{0x2B1B, 0x2B1C, "Shapes"},           // ⬛ ⬜
	{0x2B50, 0x2B50, "Symbols"},          // ⭐
	{0x2B55, 0x2B55, "Symbols"},          // ⭕
	{0x3030, 0x3030, "Symbols"},          // 〰
	{0x3297, 0x3297, "Symbols"},          // ㊗
	{0x3299, 0x3299, "Symbols"},          // ㊙
}

// Emoticon to emoji mapping
var emoticonMap = map[string]string{
	":)":  "😊",
	":-)": "😊",
	":(":  "😢",
	":-(": "😢",
	":D":  "😀",
	":-D": "😀",
	";)":  "😉",
	";-)": "😉",
	":P":  "😛",
	":-P": "😛",
	":p":  "😛",
	":-p": "😛",
	":O":  "😮",
	":-O": "😮",
	":o":  "😮",
	":-o": "😮",
	"<3":  "❤️",
	"</3": "💔",
	":*":  "😘",
	":-*": "😘",
	":|":  "😐",
	":-|": "😐",
	":/":  "😕",
	":-/": "😕",
	":'(": "😢",
	":')": "😂",
	":3":  "🐱",
	"^_^": "😊",
	"^__^": "😊",
	"^^":  "😊",
	">_<": "😣",
	"T_T": "😭",
	"TT":  "😭",
	"xD":  "😂",
	"XD":  "😂",
}

// Emoji name mapping for common emojis
var emojiNames = map[rune]string{
	0x1F600: "Grinning Face",
	0x1F601: "Beaming Face",
	0x1F602: "Face with Tears of Joy",
	0x1F603: "Smiling Face",
	0x1F604: "Grinning Face Smiling Eyes",
	0x1F605: "Grinning Face Sweat",
	0x1F606: "Grinning Squinting Face",
	0x1F607: "Smiling Face Halo",
	0x1F608: "Smiling Face Horns",
	0x1F609: "Winking Face",
	0x1F60A: "Smiling Face Smiling Eyes",
	0x1F60B: "Face Savoring Food",
	0x1F60C: "Relieved Face",
	0x1F60D: "Smiling Face Heart-Eyes",
	0x1F60E: "Smiling Face Sunglasses",
	0x1F60F: "Smirking Face",
	0x1F610: "Neutral Face",
	0x1F611: "Expressionless Face",
	0x1F612: "Unamused Face",
	0x1F613: "Downcast Face Sweat",
	0x1F614: "Pensive Face",
	0x1F615: "Confused Face",
	0x1F616: "Confounded Face",
	0x1F617: "Kissing Face",
	0x1F618: "Face Blowing Kiss",
	0x1F619: "Kissing Face Smiling Eyes",
	0x1F61A: "Kissing Face Closed Eyes",
	0x1F61B: "Face with Tongue",
	0x1F61C: "Winking Face Tongue",
	0x1F61D: "Squinting Face Tongue",
	0x1F61E: "Disappointed Face",
	0x1F61F: "Worried Face",
	0x1F620: "Angry Face",
	0x1F621: "Pouting Face",
	0x1F622: "Crying Face",
	0x1F623: "Persevering Face",
	0x1F624: "Face with Steam",
	0x1F625: "Sad but Relieved Face",
	0x1F626: "Frowning Open Mouth",
	0x1F627: "Anguished Face",
	0x1F628: "Fearful Face",
	0x1F629: "Weary Face",
	0x1F62A: "Sleepy Face",
	0x1F62B: "Tired Face",
	0x1F62C: "Grimacing Face",
	0x1F62D: "Loudly Crying Face",
	0x1F62E: "Mouth Open Face",
	0x1F62F: "Hushed Face",
	0x1F630: "Anxious Face Sweat",
	0x1F631: "Screaming in Fear",
	0x1F632: "Astonished Face",
	0x1F633: "Flushed Face",
	0x1F634: "Sleeping Face",
	0x1F635: "Dizzy Face",
	0x1F636: "Face Without Mouth",
	0x1F637: "Face with Medical Mask",
	0x2764:  "Red Heart",
	0x1F494: "Broken Heart",
	0x1F495: "Two Hearts",
	0x1F496: "Sparkling Heart",
	0x1F497: "Growing Heart",
	0x1F498: "Heart with Arrow",
	0x1F499: "Blue Heart",
	0x1F49A: "Green Heart",
	0x1F49B: "Yellow Heart",
	0x1F49C: "Purple Heart",
	0x1F49D: "Heart with Ribbon",
	0x1F49E: "Revolving Hearts",
	0x1F49F: "Heart Decoration",
	0x2665:  "Heart Suit",
	0x2661:  "White Heart Suit",
	0x1F44D: "Thumbs Up",
	0x1F44E: "Thumbs Down",
	0x1F44F: "Clapping Hands",
	0x1F44A: "Punch",
	0x1F44B: "Waving Hand",
	0x270C:  "Victory Hand",
	0x1F44C: "OK Hand",
}

// IsEmoji checks if a rune is an emoji
func IsEmoji(r rune) bool {
	// Check variation selectors
	if r >= 0xFE00 && r <= 0xFE0F {
		return true
	}
	if r >= 0x1F3FB && r <= 0x1F3FF {
		return true // Skin tone modifiers
	}
	if r >= 0x1F1E6 && r <= 0x1F1FF {
		return true // Regional indicators (flags)
	}

	// Check emoji ranges
	for _, er := range emojiRanges {
		if r >= er.Start && r <= er.End {
			return true
		}
	}

	// Zero-width joiner used in composite emojis
	if r == 0x200D {
		return true
	}

	return false
}

// ContainsEmoji checks if a string contains any emoji
func ContainsEmoji(s string) bool {
	for _, r := range s {
		if IsEmoji(r) {
			return true
		}
	}
	return false
}

// CountEmoji counts the number of emoji characters in a string
// Each individual emoji (even when consecutive) is counted separately
// Variation selectors and skin tone modifiers don't count as separate emojis
func CountEmoji(s string) int {
	count := 0
	prevWasZWJ := false

	for _, r := range s {
		// Skip variation selectors - they're part of the previous emoji
		if r >= 0xFE00 && r <= 0xFE0F {
			continue
		}
		// Skip skin tone modifiers - they're part of the previous emoji
		if r >= 0x1F3FB && r <= 0x1F3FF {
			continue
		}

		if r == 0x200D { // Zero-width joiner
			prevWasZWJ = true
			continue
		}

		if IsEmoji(r) {
			// If previous char was ZWJ, this is part of a composite emoji
			// so we don't count it as a new emoji
			if !prevWasZWJ {
				count++
			}
		}
		prevWasZWJ = false
	}

	return count
}

// ExtractEmoji extracts all emojis from a string
// Handles composite emojis (with ZWJ) and skin tone modifiers
func ExtractEmoji(s string) []string {
	var emojis []string
	var currentEmoji []rune
	prevWasZWJ := false

	for _, r := range s {
		if r == 0x200D { // Zero-width joiner
			if len(currentEmoji) > 0 {
				currentEmoji = append(currentEmoji, r)
			}
			prevWasZWJ = true
			continue
		}

		if IsEmoji(r) {
			if len(currentEmoji) > 0 && !prevWasZWJ {
				// End previous emoji and start new one
				emojis = append(emojis, string(currentEmoji))
				currentEmoji = []rune{r}
			} else {
				currentEmoji = append(currentEmoji, r)
			}
		} else {
			if len(currentEmoji) > 0 {
				emojis = append(emojis, string(currentEmoji))
				currentEmoji = nil
			}
		}
		prevWasZWJ = false
	}

	// Don't forget the last emoji
	if len(currentEmoji) > 0 {
		emojis = append(emojis, string(currentEmoji))
	}

	return emojis
}

// RemoveEmoji removes all emojis from a string
func RemoveEmoji(s string) string {
	var result []rune

	for _, r := range s {
		if !IsEmoji(r) {
			result = append(result, r)
		}
	}

	return string(result)
}

// ReplaceEmoji replaces all emojis with a replacement string
// Each emoji (including consecutive ones) is replaced separately
func ReplaceEmoji(s, replacement string) string {
	var result []rune
	prevWasZWJ := false

	for _, r := range s {
		if r == 0x200D { // Zero-width joiner
			prevWasZWJ = true
			continue
		}

		if IsEmoji(r) {
			if !prevWasZWJ {
				// Start of new emoji
				result = append(result, []rune(replacement)...)
			}
			// If prevWasZWJ, this is continuation of composite emoji, skip
		} else {
			result = append(result, r)
		}
		prevWasZWJ = false
	}

	return string(result)
}

// GetEmojiInfo returns detailed information about an emoji
func GetEmojiInfo(emoji string) EmojiInfo {
	info := EmojiInfo{
		Emoji: emoji,
	}

	runes := []rune(emoji)
	info.CodePoints = runes
	info.IsComposite = len(runes) > 1

	// Get name
	if len(runes) > 0 {
		if name, ok := emojiNames[runes[0]]; ok {
			info.Name = name
		} else {
			info.Name = "Unknown Emoji"
		}
	}

	// Determine category
	info.Category = GetEmojiCategory(emoji)

	return info
}

// GetEmojiCategory determines the category of an emoji
func GetEmojiCategory(emoji string) EmojiCategory {
	if len(emoji) == 0 {
		return CategoryUnknown
	}

	r := []rune(emoji)[0]

	// Faces and emoticons
	if r >= 0x1F600 && r <= 0x1F64F {
		return CategoryFaces
	}

	// People and body parts
	if (r >= 0x1F466 && r <= 0x1F469) || (r >= 0x1F476 && r <= 0x1F487) {
		return CategoryPeople
	}
	if r >= 0x1F9B0 && r <= 0x1F9B3 {
		return CategoryPeople
	}
	if r >= 0x1F440 && r <= 0x1F44F {
		return CategoryPeople
	}

	// Animals
	if r >= 0x1F400 && r <= 0x1F43F {
		return CategoryAnimals
	}
	if r >= 0x1F980 && r <= 0x1F9AE {
		return CategoryAnimals
	}

	// Food
	if r >= 0x1F32D && r <= 0x1F37F {
		return CategoryFood
	}
	if r >= 0x1F950 && r <= 0x1F96F {
		return CategoryFood
	}

	// Travel
	if r >= 0x1F680 && r <= 0x1F6FF {
		return CategoryTravel
	}
	if r >= 0x1F681 && r <= 0x1F68C {
		return CategoryTravel
	}

	// Activities/Sports
	if r >= 0x1F380 && r <= 0x1F39F {
		return CategoryActivities
	}
	if r >= 0x26BD && r <= 0x26F3 {
		return CategoryActivities
	}

	// Objects
	if r >= 0x1F4A0 && r <= 0x1F4FF {
		return CategoryObjects
	}
	if r >= 0x1F500 && r <= 0x1F5FF {
		return CategoryObjects
	}

	// Symbols
	if r >= 0x2600 && r <= 0x27BF {
		return CategorySymbols
	}
	if r >= 0x1F300 && r <= 0x1F37F {
		return CategorySymbols
	}

	// Flags (Regional indicators)
	if r >= 0x1F1E6 && r <= 0x1F1FF {
		return CategoryFlags
	}

	return CategoryUnknown
}

// EmoticonToEmoji converts a text emoticon to emoji
func EmoticonToEmoji(text string) string {
	result := text
	for emoticon, emoji := range emoticonMap {
		result = replaceAll(result, emoticon, emoji)
	}
	return result
}

// Replace all occurrences (case-insensitive for some emoticons)
func replaceAll(s, old, new string) string {
	result := ""
	i := 0
	oldRunes := []rune(old)
	sRunes := []rune(s)

	for i < len(sRunes) {
		if i+len(oldRunes) <= len(sRunes) {
			match := true
			for j, or := range oldRunes {
				if unicode.ToLower(sRunes[i+j]) != unicode.ToLower(or) {
					match = false
					break
				}
			}
			if match {
				result += new
				i += len(oldRunes)
				continue
			}
		}
		result += string(sRunes[i])
		i++
	}

	return result
}

// EmojiToCodePoints converts an emoji to its Unicode code point representation
func EmojiToCodePoints(emoji string) []string {
	var codePoints []string
	for _, r := range emoji {
		codePoints = append(codePoints, "U+"+formatHex(r))
	}
	return codePoints
}

// CodePointsToEmoji converts code points back to emoji
func CodePointsToEmoji(codePoints []string) (string, error) {
	var runes []rune
	for _, cp := range codePoints {
		var r rune
		_, err := parseCodePoint(cp, &r)
		if err != nil {
			return "", err
		}
		runes = append(runes, r)
	}
	return string(runes), nil
}

// formatHex formats a rune as uppercase hex
func formatHex(r rune) string {
	return formatHexUpper(uint32(r))
}

func formatHexUpper(v uint32) string {
	const digits = "0123456789ABCDEF"
	var buf [8]byte
	i := 8
	for v > 0 {
		i--
		buf[i] = digits[v%16]
		v /= 16
	}
	if i == 8 {
		return "0"
	}
	return string(buf[i:])
}

// parseCodePoint parses a code point string like "U+1F600" or "0x1F600"
func parseCodePoint(s string, r *rune) (int, error) {
	s = trimPrefix(s, "U+")
	s = trimPrefix(s, "u+")
	s = trimPrefix(s, "0X")
	s = trimPrefix(s, "0x")

	var result rune
	for _, c := range s {
		result *= 16
		if c >= '0' && c <= '9' {
			result += rune(c - '0')
		} else if c >= 'A' && c <= 'F' {
			result += rune(c - 'A' + 10)
		} else if c >= 'a' && c <= 'f' {
			result += rune(c - 'a' + 10)
		} else {
			return 0, errInvalidCodePoint
		}
	}
	*r = result
	return len(s), nil
}

func trimPrefix(s, prefix string) string {
	if len(s) >= len(prefix) && s[:len(prefix)] == prefix {
		return s[len(prefix):]
	}
	return s
}

type parseError string

func (e parseError) Error() string { return string(e) }

var errInvalidCodePoint = parseError("invalid code point")

// EmojiLength returns the display length of a string, counting emojis as 1
// Each individual emoji is counted as 1 character
// Variation selectors and skin tone modifiers don't add to the length
func EmojiLength(s string) int {
	length := 0
	prevWasZWJ := false

	for _, r := range s {
		// Skip variation selectors - they don't add display length
		if r >= 0xFE00 && r <= 0xFE0F {
			continue
		}
		// Skip skin tone modifiers - they don't add display length
		if r >= 0x1F3FB && r <= 0x1F3FF {
			continue
		}

		if r == 0x200D { // Zero-width joiner
			prevWasZWJ = true
			continue
		}

		if IsEmoji(r) {
			if !prevWasZWJ {
				length++
			}
		} else {
			if utf8.RuneLen(r) > 0 {
				length++
			}
		}
		prevWasZWJ = false
	}

	return length
}

// SplitByEmoji splits a string into emoji and non-emoji segments
func SplitByEmoji(s string) []EmojiSegment {
	var segments []EmojiSegment
	var currentText []rune
	var currentEmoji []rune

	for _, r := range s {
		if IsEmoji(r) {
			if len(currentText) > 0 {
				segments = append(segments, EmojiSegment{
					Text:  string(currentText),
					IsEmoji: false,
				})
				currentText = nil
			}
			currentEmoji = append(currentEmoji, r)
		} else {
			if len(currentEmoji) > 0 {
				segments = append(segments, EmojiSegment{
					Text:  string(currentEmoji),
					IsEmoji: true,
				})
				currentEmoji = nil
			}
			currentText = append(currentText, r)
		}
	}

	// Handle remaining segments
	if len(currentText) > 0 {
		segments = append(segments, EmojiSegment{
			Text:  string(currentText),
			IsEmoji: false,
		})
	}
	if len(currentEmoji) > 0 {
		segments = append(segments, EmojiSegment{
			Text:  string(currentEmoji),
			IsEmoji: true,
		})
	}

	return segments
}

// EmojiSegment represents a segment of text that is either emoji or regular text
type EmojiSegment struct {
	Text    string
	IsEmoji bool
}

// GetEmojisByCategory returns all known emojis of a specific category
func GetEmojisByCategory(category EmojiCategory) []string {
	// Return sample emojis for each category
	switch category {
	case CategoryFaces:
		return []string{"😀", "😃", "😄", "😁", "😅", "😂", "🤣", "😊", "😇", "🙂", "😉", "😍", "🥰", "😘", "😗", "😙", "😚", "😋", "😛", "😜"}
	case CategoryPeople:
		return []string{"👋", "🤚", "🖐", "✋", "🖖", "👌", "🤌", "🤏", "✌", "🤞", "🤟", "🤘", "🤙", "👍", "👎", "👏", "🙌", "🤲", "🙏"}
	case CategoryAnimals:
		return []string{"🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐧", "🐦"}
	case CategoryFood:
		return []string{"🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑"}
	case CategoryTravel:
		return []string{"🚗", "🚕", "🚙", "🚌", "🚎", "🏎", "🚓", "🚑", "🚒", "🚐", "🛻", "🚚", "🚛", "🚜", "🦯", "🦽", "🦼", "🛴"}
	case CategoryActivities:
		return []string{"⚽", "🏀", "🏈", "⚾", "🥎", "🎾", "🏐", "🏉", "🥏", "🎱", "🪀", "🏓", "🏸", "🏒", "🏑", "🥍", "🏏", "🪃"}
	case CategoryObjects:
		return []string{"⌚️", "📱", "💻", "⌨️", "🖥️", "🖨️", "🖱️", "🖲️", "🕹️", "🗜️", "💽", "💾", "💿", "📀", "📼", "📷", "📸"}
	case CategorySymbols:
		return []string{"❤", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", "❣", "💕", "💞", "💓", "💗", "💖", "💘", "💝"}
	case CategoryFlags:
		return []string{"🇺🇸", "🇬🇧", "🇨🇳", "🇯🇵", "🇫🇷", "🇩🇪", "🇮🇹", "🇪🇸", "🇷🇺", "🇧🇷", "🇨🇦", "🇦🇺", "🇰🇷", "🇲🇽", "🇮🇳"}
	default:
		return []string{}
	}
}

// ValidateEmoji checks if a string is a valid emoji sequence
func ValidateEmoji(s string) bool {
	if len(s) == 0 {
		return false
	}

	runes := []rune(s)
	if len(runes) == 0 {
		return false
	}

	// At least one rune should be an emoji
	hasEmoji := false
	for _, r := range runes {
		if IsEmoji(r) {
			hasEmoji = true
			break
		}
	}

	return hasEmoji
}

// IsEmojiOnly checks if a string contains only emojis (and optional whitespace)
func IsEmojiOnly(s string) bool {
	for _, r := range s {
		if !IsEmoji(r) && !unicode.IsSpace(r) {
			return false
		}
	}
	return true
}

// StripSkinToneModifiers removes skin tone modifiers from an emoji
func StripSkinToneModifiers(emoji string) string {
	var result []rune
	for _, r := range emoji {
		// Remove skin tone modifiers (1F3FB-1F3FF)
		if r < 0x1F3FB || r > 0x1F3FF {
			result = append(result, r)
		}
	}
	return string(result)
}

// StripVariationSelectors removes variation selectors from an emoji
func StripVariationSelectors(emoji string) string {
	var result []rune
	for _, r := range emoji {
		// Remove variation selectors (FE00-FE0F)
		if r < 0xFE00 || r > 0xFE0F {
			result = append(result, r)
		}
	}
	return string(result)
}

// NormalizeEmoji normalizes an emoji by removing modifiers and selectors
func NormalizeEmoji(emoji string) string {
	return StripVariationSelectors(StripSkinToneModifiers(emoji))
}