package slug_utils

import (
	"testing"
)

func TestGenerate(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"simple", "Hello World", "hello-world"},
		{"with numbers", "Hello World 123", "hello-world-123"},
		{"special chars", "Hello!@#World", "hello-world"},
		{"multiple spaces", "Hello    World", "hello-world"},
		{"leading trailing spaces", "  Hello World  ", "hello-world"},
		{"underscores", "hello_world", "hello-world"},
		{"mixed case", "HeLLo WoRLD", "hello-world"},
		{"empty string", "", ""},
		{"only special chars", "!@#$%^", ""},
		{"with dots", "hello.world", "hello-world"},
		{"with plus", "hello+world", "hello-world"},
		{"consecutive dashes", "hello---world", "hello-world"},
		{"unicode letters", "café", "cafe"},
		{"german umlaut", "grüße", "gruesse"},
		{"cyrillic", "привет мир", "privet-mir"},
		{"greek", "γεια σου", "geia-sou"},
		{"currency", "price €100", "price-eur-100"},
		{"copyright", "© 2024 Company", "c-2024-company"},
		{"trademark", "Product™", "product-tm"},
		{"chinese", "你好世界", "ni-hao-shi-jie"},
		{"japanese", "こんにちは", "konnichiha"},
		{"korean", "안녕하세요", "annyeonghaseyo"},
		{"arabic", "مرحبا", "mrhba"},
	}

	slugger := New()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := slugger.Generate(tt.input)
			if result != tt.expected {
				t.Errorf("Generate(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestGenerateWithConfig(t *testing.T) {
	t.Run("custom separator underscore", func(t *testing.T) {
		slugger := NewWithConfig(Config{
			Separator: "_",
			Lowercase: true,
		})
		result := slugger.Generate("Hello World")
		expected := "hello_world"
		if result != expected {
			t.Errorf("Generate with underscore = %q, want %q", result, expected)
		}
	})

	t.Run("no lowercase", func(t *testing.T) {
		slugger := NewWithConfig(Config{
			Separator: "-",
			Lowercase: false,
		})
		result := slugger.Generate("Hello World")
		expected := "Hello-World"
		if result != expected {
			t.Errorf("Generate without lowercase = %q, want %q", result, expected)
		}
	})

	t.Run("max length", func(t *testing.T) {
		slugger := NewWithConfig(Config{
			Separator: "-",
			MaxLength: 10,
			Lowercase: true,
		})
		result := slugger.Generate("Hello Beautiful World")
		// Should truncate at word boundary
		if len(result) > 10 {
			t.Errorf("Generate with max length = %q (len=%d), want len <= 10", result, len(result))
		}
	})

	t.Run("max length exact", func(t *testing.T) {
		slugger := NewWithConfig(Config{
			Separator:     "-",
			MaxLength:     5,
			Lowercase:     true,
			TrimSeparator: true,
		})
		result := slugger.Generate("Hello World")
		if len(result) > 5 {
			t.Errorf("Generate with max length 5 = %q (len=%d)", result, len(result))
		}
	})
}

func TestGenerateUnique(t *testing.T) {
	existing := make(map[string]bool)

	// Simulate existing slugs
	existing["hello-world"] = true
	existing["hello-world-1"] = true

	slugger := New()

	t.Run("first unique slug", func(t *testing.T) {
		result := slugger.GenerateUnique("My New Post", existing)
		expected := "my-new-post"
		if result != expected {
			t.Errorf("GenerateUnique = %q, want %q", result, expected)
		}
	})

	t.Run("duplicate base slug", func(t *testing.T) {
		result := slugger.GenerateUnique("Hello World", existing)
		expected := "hello-world-2"
		if result != expected {
			t.Errorf("GenerateUnique = %q, want %q", result, expected)
		}
	})

	t.Run("another duplicate", func(t *testing.T) {
		existing["hello-world-2"] = true
		result := slugger.GenerateUnique("Hello World", existing)
		expected := "hello-world-3"
		if result != expected {
			t.Errorf("GenerateUnique = %q, want %q", result, expected)
		}
	})
}

func TestGenerateMultiple(t *testing.T) {
	slugger := New()

	result := slugger.GenerateMultiple("Hello", "World", "2024")
	expected := "hello-world-2024"
	if result != expected {
		t.Errorf("GenerateMultiple = %q, want %q", result, expected)
	}
}

func TestIsValidSlug(t *testing.T) {
	tests := []struct {
		slug     string
		expected bool
	}{
		{"hello-world", true},
		{"hello_world", true},
		{"hello123", true},
		{"hello-world-123", true},
		{"Hello-World", true},
		{"", false},
		{"hello world", false},
		{"hello@world", false},
		{"hello.world", false},
		{"hello/world", false},
		{"hello world!", false},
	}

	for _, tt := range tests {
		t.Run(tt.slug, func(t *testing.T) {
			result := IsValidSlug(tt.slug)
			if result != tt.expected {
				t.Errorf("IsValidSlug(%q) = %v, want %v", tt.slug, result, tt.expected)
			}
		})
	}
}

func TestParseSlug(t *testing.T) {
	tests := []struct {
		slug      string
		separator string
		expected  []string
	}{
		{"hello-world", "-", []string{"hello", "world"}},
		{"hello_world_123", "_", []string{"hello", "world", "123"}},
		{"single", "-", []string{"single"}},
		{"", "-", []string{""}},
	}

	for _, tt := range tests {
		t.Run(tt.slug, func(t *testing.T) {
			result := ParseSlug(tt.slug, tt.separator)
			if len(result) != len(tt.expected) {
				t.Errorf("ParseSlug length = %d, want %d", len(result), len(tt.expected))
				return
			}
			for i, v := range result {
				if v != tt.expected[i] {
					t.Errorf("ParseSlug[%d] = %q, want %q", i, v, tt.expected[i])
				}
			}
		})
	}
}

func TestTruncate(t *testing.T) {
	tests := []struct {
		name      string
		slug      string
		maxLength int
		separator string
		expected  string
	}{
		{"no truncation needed", "hello", 10, "-", "hello"},
		{"exact length", "hello", 5, "-", "hello"},
		{"truncate at separator", "hello-world-test", 11, "-", "hello-world"},
		{"truncate short", "hello-world", 5, "-", "hello"},
		{"empty separator", "hello-world", 11, "", "hello-world"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Truncate(tt.slug, tt.maxLength, tt.separator)
			if result != tt.expected {
				t.Errorf("Truncate = %q, want %q", result, tt.expected)
			}
		})
	}
}

func TestIntToString(t *testing.T) {
	tests := []struct {
		input    int
		expected string
	}{
		{0, "0"},
		{1, "1"},
		{123, "123"},
		{-1, "-1"},
		{-123, "-123"},
		{999999, "999999"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			result := intToString(tt.input)
			if result != tt.expected {
				t.Errorf("intToString(%d) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestTransliteration(t *testing.T) {
	slugger := New()

	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"french accents", "à la carte", "a-la-carte"},
		{"spanish tilde", "año nuevo", "ano-nuevo"},
		{"german umlaut", "München", "muenchen"},
		{"german sharp s", "straße", "strasse"},
		{"scandinavian", "Öland åker", "oelandaaker"},
		{"portuguese", "coração", "coracao"},
		{"russian", "Москва", "moskva"},
		{"greek", "Αθήνα", "athina"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := slugger.Generate(tt.input)
			if result != tt.expected {
				t.Errorf("Transliteration %q = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestPackageLevelFunctions(t *testing.T) {
	t.Run("Generate", func(t *testing.T) {
		result := Generate("Hello World")
		expected := "hello-world"
		if result != expected {
			t.Errorf("Generate = %q, want %q", result, expected)
		}
	})

	t.Run("GenerateMultiple", func(t *testing.T) {
		result := GenerateMultiple("Hello", "World")
		expected := "hello-world"
		if result != expected {
			t.Errorf("GenerateMultiple = %q, want %q", result, expected)
		}
	})

	t.Run("GenerateUnique", func(t *testing.T) {
		existing := make(map[string]bool)
		result := GenerateUnique("Hello World", existing)
		expected := "hello-world"
		if result != expected {
			t.Errorf("GenerateUnique = %q, want %q", result, expected)
		}
	})
}

// Benchmark tests
func BenchmarkGenerate(b *testing.B) {
	slugger := New()
	input := "Hello Beautiful World! This is a test @#$ string with some special characters."

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		slugger.Generate(input)
	}
}

func BenchmarkGenerateShort(b *testing.B) {
	slugger := New()
	input := "hello-world"

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		slugger.Generate(input)
	}
}

func BenchmarkGenerateUnique(b *testing.B) {
	slugger := New()
	existing := make(map[string]bool)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		slugger.GenerateUnique("Hello World", existing)
	}
}

func BenchmarkTransliteration(b *testing.B) {
	slugger := New()
	input := "Привет мир! Grüße aus München 你好世界"

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		slugger.Generate(input)
	}
}