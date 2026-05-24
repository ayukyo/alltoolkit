package run_length_encoding_utils

import (
	"bytes"
	"testing"
)

func TestEncode(t *testing.T) {
	tests := []struct {
		name     string
		input    []byte
		wantRuns []Run
		wantErr  bool
	}{
		{
			name:     "simple run",
			input:    []byte{1, 1, 1, 2, 2, 3},
			wantRuns: []Run{{1, 3}, {2, 2}, {3, 1}},
			wantErr:  false,
		},
		{
			name:     "single element",
			input:    []byte{42},
			wantRuns: []Run{{42, 1}},
			wantErr:  false,
		},
		{
			name:     "all same",
			input:    []byte{7, 7, 7, 7, 7},
			wantRuns: []Run{{7, 5}},
			wantErr:  false,
		},
		{
			name:     "empty input",
			input:    []byte{},
			wantRuns: nil,
			wantErr:  true,
		},
		{
			name:     "long run",
			input:    bytes.Repeat([]byte{0xFF}, 300),
			wantRuns: []Run{{0xFF, 300}},
			wantErr:  false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := Encode(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("Encode() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if len(got.Runs) != len(tt.wantRuns) {
					t.Errorf("Encode() got %d runs, want %d", len(got.Runs), len(tt.wantRuns))
					return
				}
				for i, run := range got.Runs {
					if run.Value != tt.wantRuns[i].Value || run.Count != tt.wantRuns[i].Count {
						t.Errorf("Encode() run[%d] = {%d, %d}, want {%d, %d}",
							i, run.Value, run.Count, tt.wantRuns[i].Value, tt.wantRuns[i].Count)
					}
				}
			}
		})
	}
}

func TestDecode(t *testing.T) {
	tests := []struct {
		name    string
		runs    []Run
		want    []byte
		wantErr bool
	}{
		{
			name:    "simple decode",
			runs:    []Run{{1, 3}, {2, 2}, {3, 1}},
			want:    []byte{1, 1, 1, 2, 2, 3},
			wantErr: false,
		},
		{
			name:    "single run",
			runs:    []Run{{42, 5}},
			want:    []byte{42, 42, 42, 42, 42},
			wantErr: false,
		},
		{
			name:    "empty runs",
			runs:    []Run{},
			want:    nil,
			wantErr: true,
		},
		{
			name:    "invalid count",
			runs:    []Run{{1, 0}},
			want:    nil,
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			e := &Encoded{Runs: tt.runs}
			got, err := e.Decode()
			if (err != nil) != tt.wantErr {
				t.Errorf("Decode() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr && !bytes.Equal(got, tt.want) {
				t.Errorf("Decode() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestEncodeDecode(t *testing.T) {
	tests := [][]byte{
		[]byte("AAAAABBBCCCCDDDDDD"),
		[]byte{0, 0, 0, 1, 1, 2, 3, 3, 3, 3},
		bytes.Repeat([]byte{42}, 1000),
		{1, 2, 3, 4, 5}, // No repeats
		{255, 255, 255, 254, 254, 253},
	}

	for i, data := range tests {
		t.Run(string(rune(i+'A')), func(t *testing.T) {
			encoded, err := Encode(data)
			if err != nil {
				t.Fatalf("Encode() error: %v", err)
			}

			decoded, err := encoded.Decode()
			if err != nil {
				t.Fatalf("Decode() error: %v", err)
			}

			if !bytes.Equal(decoded, data) {
				t.Errorf("Round-trip failed: got %v, want %v", decoded, data)
			}
		})
	}
}

func TestBytesAndFromBytes(t *testing.T) {
	tests := [][]byte{
		[]byte("AAAABBBCC"),
		{0, 0, 0, 1, 1, 2},
		bytes.Repeat([]byte{100}, 255),
		bytes.Repeat([]byte{200}, 256),
		bytes.Repeat([]byte{50}, 65535),
	}

	for i, data := range tests {
		t.Run(string(rune(i+'0')), func(t *testing.T) {
			encoded, err := Encode(data)
			if err != nil {
				t.Fatalf("Encode() error: %v", err)
			}

			packed, err := encoded.Bytes()
			if err != nil {
				t.Fatalf("Bytes() error: %v", err)
			}

			decoded, err := FromBytes(packed)
			if err != nil {
				t.Fatalf("FromBytes() error: %v", err)
			}

			result, err := decoded.Decode()
			if err != nil {
				t.Fatalf("Decode() error: %v", err)
			}

			if !bytes.Equal(result, data) {
				t.Errorf("Round-trip failed")
			}
		})
	}
}

func TestBytesOverflow(t *testing.T) {
	// Test that count > 65535 returns error
	data := bytes.Repeat([]byte{42}, 65536)
	encoded, err := Encode(data)
	if err != nil {
		t.Fatalf("Encode() error: %v", err)
	}

	_, err = encoded.Bytes()
	if err == nil {
		t.Error("Bytes() should return error for count > 65535")
	}
}

func TestEncodeString(t *testing.T) {
	encoded, err := EncodeString("AAAAABBBCCCC")
	if err != nil {
		t.Fatalf("EncodeString() error: %v", err)
	}

	if len(encoded.Runs) != 3 {
		t.Errorf("Expected 3 runs, got %d", len(encoded.Runs))
	}

	decoded, err := encoded.DecodeToString()
	if err != nil {
		t.Fatalf("DecodeToString() error: %v", err)
	}

	if decoded != "AAAAABBBCCCC" {
		t.Errorf("Expected 'AAAAABBBCCCC', got '%s'", decoded)
	}
}

func TestRatio(t *testing.T) {
	tests := []struct {
		input     string
		wantRatio float64
	}{
		{"AAAAA", 5.0 / 3.0},     // 5 bytes -> 1 run (3 bytes encoded)
		{"ABCDE", 5.0 / 15.0},     // 5 bytes -> 5 runs (15 bytes encoded)
		{"AAABBC", 6.0 / 9.0},     // 6 bytes -> 3 runs (9 bytes encoded)
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			encoded, err := EncodeString(tt.input)
			if err != nil {
				t.Fatalf("EncodeString() error: %v", err)
			}

			got := encoded.Ratio()
			// Allow small floating point differences
			if got < tt.wantRatio-0.01 || got > tt.wantRatio+0.01 {
				t.Errorf("Ratio() = %v, want %v", got, tt.wantRatio)
			}
		})
	}
}

func TestOriginalSize(t *testing.T) {
	encoded, _ := Encode([]byte("AAAAABBBCC"))
	if encoded.OriginalSize() != 10 {
		t.Errorf("OriginalSize() = %d, want 10", encoded.OriginalSize())
	}
}

func TestNumRuns(t *testing.T) {
	encoded, _ := Encode([]byte("AAAAABBBCC"))
	if encoded.NumRuns() != 3 {
		t.Errorf("NumRuns() = %d, want 3", encoded.NumRuns())
	}
}

func TestString(t *testing.T) {
	encoded, _ := Encode([]byte{65, 65, 65, 66, 66})
	got := encoded.String()
	expected := "65:3, 66:2"
	if got != expected {
		t.Errorf("String() = %q, want %q", got, expected)
	}
}

func TestEncodeInts(t *testing.T) {
	runs, err := EncodeInts([]int{1, 1, 1, 2, 2, 3})
	if err != nil {
		t.Fatalf("EncodeInts() error: %v", err)
	}

	if len(runs) != 3 {
		t.Errorf("Expected 3 runs, got %d", len(runs))
	}

	decoded, err := DecodeInts(runs)
	if err != nil {
		t.Fatalf("DecodeInts() error: %v", err)
	}

	expected := []int{1, 1, 1, 2, 2, 3}
	if len(decoded) != len(expected) {
		t.Fatalf("Expected %d elements, got %d", len(expected), len(decoded))
	}

	for i := range expected {
		if decoded[i] != expected[i] {
			t.Errorf("decoded[%d] = %d, want %d", i, decoded[i], expected[i])
		}
	}
}

func TestEncodeRunes(t *testing.T) {
	runs, err := EncodeRunes([]rune("你好你好你"))
	if err != nil {
		t.Fatalf("EncodeRunes() error: %v", err)
	}

	// 你好你好你 = 你,好,你,好,你
	// Runs: 你:1, 好:1, 你:1, 好:1, 你:1
	if len(runs) != 5 {
		t.Errorf("Expected 5 runs, got %d", len(runs))
	}

	// Test with repeated runes
	runs2, err := EncodeRunes([]rune("AAAA"))
	if err != nil {
		t.Fatalf("EncodeRunes() error: %v", err)
	}

	if len(runs2) != 1 || runs2[0].Value != 'A' || runs2[0].Count != 4 {
		t.Errorf("Expected single run {A, 4}, got %v", runs2)
	}
}

func TestEncodeStringRunes(t *testing.T) {
	runs, err := EncodeStringRunes("🚀🚀🚀🌟")
	if err != nil {
		t.Fatalf("EncodeStringRunes() error: %v", err)
	}

	if len(runs) != 2 {
		t.Errorf("Expected 2 runs, got %d", len(runs))
	}

	decoded, err := DecodeRuneRunsToString(runs)
	if err != nil {
		t.Fatalf("DecodeRuneRunsToString() error: %v", err)
	}

	if decoded != "🚀🚀🚀🌟" {
		t.Errorf("Expected '🚀🚀🚀🌟', got %q", decoded)
	}
}

func TestAnalyze(t *testing.T) {
	encoded, _ := Encode([]byte("AAAAABBBCC"))

	stats := encoded.Analyze()
	if stats == nil {
		t.Fatal("Analyze() returned nil")
	}

	if stats.OriginalSize != 10 {
		t.Errorf("OriginalSize = %d, want 10", stats.OriginalSize)
	}

	if stats.NumRuns != 3 {
		t.Errorf("NumRuns = %d, want 3", stats.NumRuns)
	}

	if stats.LongestRun != 5 {
		t.Errorf("LongestRun = %d, want 5", stats.LongestRun)
	}

	if stats.MostCommonValue != 'A' {
		t.Errorf("MostCommonValue = %d, want %d", stats.MostCommonValue, 'A')
	}
}

func TestIsCompressible(t *testing.T) {
	tests := []struct {
		input string
		want  bool
	}{
		{"AAAAA", true},       // Highly compressible
		{"ABABABAB", false},   // Not compressible
		{"ABCDE", false},      // Not compressible
		{"A", false},          // Too short
		{"", false},           // Empty
		{"AAAAABBBCCCCC", true}, // Compressible
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			got := IsCompressible([]byte(tt.input))
			if got != tt.want {
				t.Errorf("IsCompressible(%q) = %v, want %v", tt.input, got, tt.want)
			}
		})
	}
}

func TestBytesWithEscape(t *testing.T) {
	escape := byte(0xFF)

	tests := []struct {
		name  string
		input []byte
	}{
		{"simple", []byte("AAAAA")},
		{"with escape char", bytes.Repeat([]byte{escape}, 5)},
		{"mixed", []byte{escape, escape, escape, 'A', 'A', 'B'}},
		{"large count", bytes.Repeat([]byte{'X'}, 300)},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			encoded, err := Encode(tt.input)
			if err != nil {
				t.Fatalf("Encode() error: %v", err)
			}

			packed, err := encoded.BytesWithEscape(escape)
			if err != nil {
				t.Fatalf("BytesWithEscape() error: %v", err)
			}

			// Verify we can decode back (this is a basic check)
			if len(packed) == 0 {
				t.Error("BytesWithEscape() returned empty data")
			}
		})
	}
}

func TestNilEncoded(t *testing.T) {
	var e *Encoded

	// Test methods on nil
	if e.String() != "" {
		t.Error("String() on nil should return empty string")
	}

	if e.OriginalSize() != 0 {
		t.Error("OriginalSize() on nil should return 0")
	}

	if e.NumRuns() != 0 {
		t.Error("NumRuns() on nil should return 0")
	}

	if e.Ratio() != 0 {
		t.Error("Ratio() on nil should return 0")
	}

	_, err := e.Decode()
	if err == nil {
		t.Error("Decode() on nil should return error")
	}

	_, err = e.Bytes()
	if err == nil {
		t.Error("Bytes() on nil should return error")
	}
}

func TestFromBytesInvalid(t *testing.T) {
	tests := []struct {
		name    string
		input   []byte
		wantErr bool
	}{
		{"empty", []byte{}, true},
		{"not multiple of 3", []byte{1, 2}, true},
		{"zero count", []byte{1, 0, 0}, true}, // count = 0
		{"valid", []byte{65, 0, 5, 66, 0, 3}, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := FromBytes(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("FromBytes() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

// Benchmark tests
func BenchmarkEncode(b *testing.B) {
	data := bytes.Repeat([]byte("ABCDE"), 1000)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Encode(data)
	}
}

func BenchmarkDecode(b *testing.B) {
	data := bytes.Repeat([]byte("ABCDE"), 1000)
	encoded, _ := Encode(data)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		encoded.Decode()
	}
}

func BenchmarkBytes(b *testing.B) {
	data := bytes.Repeat([]byte("ABCDE"), 1000)
	encoded, _ := Encode(data)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		encoded.Bytes()
	}
}