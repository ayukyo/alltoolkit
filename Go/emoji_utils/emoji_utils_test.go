package emoji_utils

import (
	"testing"
)

func TestIsEmoji(t *testing.T) {
	tests := []struct {
		r      rune
		expect bool
	}{
		{'😀', true},
		{'❤', true},
		{'A', false},
		{'z', false},
		{'0', false},
		{' ', false},
		{'🇦', true}, // Regional indicator
		{0x1F600, true}, // Grinning face
		{0xFE0F, true},  // Variation selector
	}

	for _, tt := range tests {
		result := IsEmoji(tt.r)
		if result != tt.expect {
			t.Errorf("IsEmoji(%U) = %v, want %v", tt.r, result, tt.expect)
		}
	}
}

func TestContainsEmoji(t *testing.T) {
	tests := []struct {
		s      string
		expect bool
	}{
		{"Hello World", false},
		{"Hello 😀 World", true},
		{"❤️", true},
		{"", false},
		{"12345", false},
		{"Test 🎉🎉🎉", true},
		{"   ", false},
		{"🇺🇸", true},
	}

	for _, tt := range tests {
		result := ContainsEmoji(tt.s)
		if result != tt.expect {
			t.Errorf("ContainsEmoji(%q) = %v, want %v", tt.s, result, tt.expect)
		}
	}
}

func TestCountEmoji(t *testing.T) {
	tests := []struct {
		s      string
		expect int
	}{
		{"Hello World", 0},
		{"Hello 😀 World", 1},
		{"😀😃😄", 3},
		{"Test 🎉🎉🎉 here", 3},
		{"No emojis here", 0},
		{"", 0},
		{"❤️💙💚", 3},
	}

	for _, tt := range tests {
		result := CountEmoji(tt.s)
		if result != tt.expect {
			t.Errorf("CountEmoji(%q) = %d, want %d", tt.s, result, tt.expect)
		}
	}
}

func TestExtractEmoji(t *testing.T) {
	tests := []struct {
		s      string
		expect []string
	}{
		{"Hello 😀 World", []string{"😀"}},
		{"😀😃😄", []string{"😀", "😃", "😄"}},
		{"No emojis", nil},
		{"🎉 Test 🎊 Here 🥳", []string{"🎉", "🎊", "🥳"}},
	}

	for _, tt := range tests {
		result := ExtractEmoji(tt.s)
		if len(result) != len(tt.expect) {
			t.Errorf("ExtractEmoji(%q) = %v, want %v", tt.s, result, tt.expect)
			continue
		}
		for i, e := range result {
			if e != tt.expect[i] {
				t.Errorf("ExtractEmoji(%q)[%d] = %q, want %q", tt.s, i, e, tt.expect[i])
			}
		}
	}
}

func TestRemoveEmoji(t *testing.T) {
	tests := []struct {
		s      string
		expect string
	}{
		{"Hello 😀 World", "Hello  World"},
		{"😀😃😄", ""},
		{"No emojis here", "No emojis here"},
		{"🎉 Test 🎊 Here 🥳", " Test  Here "},
		{"", ""},
	}

	for _, tt := range tests {
		result := RemoveEmoji(tt.s)
		if result != tt.expect {
			t.Errorf("RemoveEmoji(%q) = %q, want %q", tt.s, result, tt.expect)
		}
	}
}

func TestReplaceEmoji(t *testing.T) {
	tests := []struct {
		s          string
		repl       string
		expect     string
	}{
		{"Hello 😀 World", "[EMOJI]", "Hello [EMOJI] World"},
		{"😀😃😄", "X", "XXX"},
		{"No emojis", "*", "No emojis"},
		{"🎉 Test 🎊 Here", "😊", "😊 Test 😊 Here"},
	}

	for _, tt := range tests {
		result := ReplaceEmoji(tt.s, tt.repl)
		if result != tt.expect {
			t.Errorf("ReplaceEmoji(%q, %q) = %q, want %q", tt.s, tt.repl, result, tt.expect)
		}
	}
}

func TestGetEmojiCategory(t *testing.T) {
	tests := []struct {
		emoji  string
		expect EmojiCategory
	}{
		{"😀", CategoryFaces},
		{"👍", CategoryPeople},
		{"🐶", CategoryAnimals},
		{"🍎", CategoryFood},
		{"🚗", CategoryTravel},
		{"⚽", CategoryActivities},
		{"📱", CategoryObjects},
		{"❤", CategorySymbols},
		{"🇺🇸", CategoryFlags},
	}

	for _, tt := range tests {
		result := GetEmojiCategory(tt.emoji)
		if result != tt.expect {
			t.Errorf("GetEmojiCategory(%q) = %v, want %v", tt.emoji, result, tt.expect)
		}
	}
}

func TestGetEmojiInfo(t *testing.T) {
	tests := []struct {
		emoji     string
		wantName  string
		wantCat   EmojiCategory
	}{
		{"😀", "Grinning Face", CategoryFaces},
		{"😊", "Smiling Face Smiling Eyes", CategoryFaces},
		{"❤", "Red Heart", CategorySymbols},
	}

	for _, tt := range tests {
		info := GetEmojiInfo(tt.emoji)
		if info.Emoji != tt.emoji {
			t.Errorf("GetEmojiInfo(%q).Emoji = %q, want %q", tt.emoji, info.Emoji, tt.emoji)
		}
		if info.Name != tt.wantName {
			t.Errorf("GetEmojiInfo(%q).Name = %q, want %q", tt.emoji, info.Name, tt.wantName)
		}
		if info.Category != tt.wantCat {
			t.Errorf("GetEmojiInfo(%q).Category = %v, want %v", tt.emoji, info.Category, tt.wantCat)
		}
	}
}

func TestEmoticonToEmoji(t *testing.T) {
	tests := []struct {
		input  string
		expect string
	}{
		{":)", "😊"},
		{":(", "😢"},
		{":D", "😀"},
		{"Hello :) World", "Hello 😊 World"},
		{"<3 you!", "❤️ you!"},
		{"No emoticons here", "No emoticons here"},
		{":) :D :P", "😊 😀 😛"},
	}

	for _, tt := range tests {
		result := EmoticonToEmoji(tt.input)
		if result != tt.expect {
			t.Errorf("EmoticonToEmoji(%q) = %q, want %q", tt.input, result, tt.expect)
		}
	}
}

func TestEmojiToCodePoints(t *testing.T) {
	tests := []struct {
		emoji  string
		expect []string
	}{
		{"😀", []string{"U+1F600"}},
		{"❤", []string{"U+2764"}},
	}

	for _, tt := range tests {
		result := EmojiToCodePoints(tt.emoji)
		if len(result) != len(tt.expect) {
			t.Errorf("EmojiToCodePoints(%q) = %v, want %v", tt.emoji, result, tt.expect)
			continue
		}
		for i, cp := range result {
			if cp != tt.expect[i] {
				t.Errorf("EmojiToCodePoints(%q)[%d] = %q, want %q", tt.emoji, i, cp, tt.expect[i])
			}
		}
	}
}

func TestCodePointsToEmoji(t *testing.T) {
	tests := []struct {
		codePoints []string
		expect     string
	}{
		{[]string{"U+1F600"}, "😀"},
		{[]string{"U+2764"}, "❤"},
		{[]string{"1F600"}, "😀"},
		{[]string{"0x1F600"}, "😀"},
	}

	for _, tt := range tests {
		result, err := CodePointsToEmoji(tt.codePoints)
		if err != nil {
			t.Errorf("CodePointsToEmoji(%v) error: %v", tt.codePoints, err)
			continue
		}
		if result != tt.expect {
			t.Errorf("CodePointsToEmoji(%v) = %q, want %q", tt.codePoints, result, tt.expect)
		}
	}
}

func TestEmojiLength(t *testing.T) {
	tests := []struct {
		s      string
		expect int
	}{
		{"Hello", 5},
		{"Hello 😀", 7},  // Hello (5) + space (1) + emoji (1) = 7
		{"😀😃😄", 3},
		{"Test 🎉🎉🎉", 8}, // Test (4) + space (1) + 3 emojis = 8
		{"", 0},
	}

	for _, tt := range tests {
		result := EmojiLength(tt.s)
		if result != tt.expect {
			t.Errorf("EmojiLength(%q) = %d, want %d", tt.s, result, tt.expect)
		}
	}
}

func TestSplitByEmoji(t *testing.T) {
	tests := []struct {
		s          string
		expectLen  int
	}{
		{"Hello 😀 World", 3},
		{"😀Hello", 2},
		{"Hello😀", 2},
		{"No emojis", 1},
		{"😀😃😄", 1},
	}

	for _, tt := range tests {
		result := SplitByEmoji(tt.s)
		if len(result) != tt.expectLen {
			t.Errorf("SplitByEmoji(%q) returned %d segments, want %d", tt.s, len(result), tt.expectLen)
		}
	}
}

func TestGetEmojisByCategory(t *testing.T) {
	categories := []EmojiCategory{
		CategoryFaces,
		CategoryPeople,
		CategoryAnimals,
		CategoryFood,
		CategoryTravel,
		CategoryActivities,
		CategoryObjects,
		CategorySymbols,
		CategoryFlags,
	}

	for _, cat := range categories {
		emojis := GetEmojisByCategory(cat)
		if len(emojis) == 0 {
			t.Errorf("GetEmojisByCategory(%v) returned empty list", cat)
		}
		for _, e := range emojis {
			if !ValidateEmoji(e) {
				t.Errorf("GetEmojisByCategory(%v) returned invalid emoji: %q", cat, e)
			}
		}
	}
}

func TestValidateEmoji(t *testing.T) {
	tests := []struct {
		s      string
		expect bool
	}{
		{"😀", true},
		{"❤", true},
		{"Hello", false},
		{"", false},
		{"A", false},
		{"🎉", true},
	}

	for _, tt := range tests {
		result := ValidateEmoji(tt.s)
		if result != tt.expect {
			t.Errorf("ValidateEmoji(%q) = %v, want %v", tt.s, result, tt.expect)
		}
	}
}

func TestIsEmojiOnly(t *testing.T) {
	tests := []struct {
		s      string
		expect bool
	}{
		{"😀", true},
		{"😀😃😄", true},
		{"😀 😃", true}, // With whitespace
		{"Hello 😀", false},
		{"", true}, // Empty string (no non-emoji)
		{"   ", true}, // Only whitespace
	}

	for _, tt := range tests {
		result := IsEmojiOnly(tt.s)
		if result != tt.expect {
			t.Errorf("IsEmojiOnly(%q) = %v, want %v", tt.s, result, tt.expect)
		}
	}
}

func TestStripSkinToneModifiers(t *testing.T) {
	tests := []struct {
		input  string
		expect string
	}{
		{"👍", "👍"},
		{"👍🏻", "👍"},
		{"👍🏼", "👍"},
		{"👍🏽", "👍"},
		{"👍🏾", "👍"},
		{"👍🏿", "👍"},
	}

	for _, tt := range tests {
		result := StripSkinToneModifiers(tt.input)
		if result != tt.expect {
			t.Errorf("StripSkinToneModifiers(%q) = %q, want %q", tt.input, result, tt.expect)
		}
	}
}

func TestNormalizeEmoji(t *testing.T) {
	tests := []struct {
		input  string
		expect string
	}{
		{"👍", "👍"},
		{"👍🏻", "👍"},
		{"❤️", "❤"},
	}

	for _, tt := range tests {
		result := NormalizeEmoji(tt.input)
		if result != tt.expect {
			t.Errorf("NormalizeEmoji(%q) = %q, want %q", tt.input, result, tt.expect)
		}
	}
}

// Benchmark tests
func BenchmarkContainsEmoji(b *testing.B) {
	s := "This is a test string with 😀 and ❤️ emojis"
	for i := 0; i < b.N; i++ {
		ContainsEmoji(s)
	}
}

func BenchmarkExtractEmoji(b *testing.B) {
	s := "Test 😀😃😄🎉🎊❤️ more text"
	for i := 0; i < b.N; i++ {
		ExtractEmoji(s)
	}
}

func BenchmarkEmojiLength(b *testing.B) {
	s := "Test string with 😀 and 🎉 emojis"
	for i := 0; i < b.N; i++ {
		EmojiLength(s)
	}
}