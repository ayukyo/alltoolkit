package stringutils

import (
	"testing"
)

func TestTruncate(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		maxLen  int
		want    string
	}{
		{
			name:    "ASCII truncation",
			input:   "Hello World, this is a long message",
			maxLen:  20,
			want:    "Hello World, this...",
		},
		{
			name:    "No truncation needed",
			input:   "Hello",
			maxLen:  20,
			want:    "Hello",
		},
		{
			name:    "Chinese truncation",
			input:   "你好世界，这是一个很长的消息",
			maxLen:  10,
			want:    "你好世界，这...",
		},
		{
			name:    "Empty string",
			input:   "",
			maxLen:  10,
			want:    "",
		},
		{
			name:    "MaxLen less than 3",
			input:   "Hello",
			maxLen:  2,
			want:    "...",
		},
		{
			name:    "Exact fit",
			input:   "Hello",
			maxLen:  5,
			want:    "Hello",
		},
		{
			name:    "One over limit",
			input:   "Hello",
			maxLen:  4,
			want:    "...",
		},
		{
			name:    "Emoji handling",
			input:   "Hello 👋 World 🌍!",
			maxLen:  12,
			want:    "Hello 👋 Wo...",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := Truncate(tt.input, tt.maxLen)
			if got != tt.want {
				t.Errorf("Truncate(%q, %d) = %q, want %q",
					tt.input, tt.maxLen, got, tt.want)
			}
		})
	}
}

func TestTruncateSafe(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		maxLen  int
		want    string
		wantLen int
	}{
		{
			name:    "ASCII truncation",
			input:   "Hello World, this is a long message",
			maxLen:  20,
			want:    "Hel...",
			wantLen: 6,
		},
		{
			name:    "No truncation needed",
			input:   "Hello",
			maxLen:  20,
			want:    "Hello",
			wantLen: 5,
		},
		{
			name:    "Byte limit respected",
			input:   "Hello World",
			maxLen:  8,
			want:    "Hel...",
			wantLen: 6,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := TruncateSafe(tt.input, tt.maxLen)
			if got != tt.want {
				t.Errorf("TruncateSafe(%q, %d) = %q, want %q",
					tt.input, tt.maxLen, got, tt.want)
			}
			if len(got) > tt.maxLen {
				t.Errorf("TruncateSafe(%q, %d) result length %d exceeds maxLen %d",
					tt.input, tt.maxLen, len(got), tt.maxLen)
			}
		})
	}
}

// BenchmarkTruncate benchmarks the Truncate function
func BenchmarkTruncate(b *testing.B) {
	input := "Hello World, this is a long message with Unicode: 你好世界 🌍"
	for i := 0; i < b.N; i++ {
		Truncate(input, 30)
	}
}

// BenchmarkTruncateSafe benchmarks the TruncateSafe function
func BenchmarkTruncateSafe(b *testing.B) {
	input := "Hello World, this is a long message with Unicode: 你好世界 🌍"
	for i := 0; i < b.N; i++ {
		TruncateSafe(input, 30)
	}
}
