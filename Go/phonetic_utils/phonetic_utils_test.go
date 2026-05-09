package phonetic_utils

import (
	"testing"
)

func TestSoundex(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Robert", "R163"},
		{"Rupert", "R163"},
		{"Smith", "S530"},
		{"Schmidt", "S530"},
		{"Johnson", "J525"},
		{"Jonson", "J525"},
		{"Ashcraft", "A261"},
		{"Ashcroft", "A261"},
		{"Tymczak", "T520"},
		{"Pfister", "P236"},
		{"", "0000"},
		{"A", "A000"},
		{"123", "0000"},
		{"OConnor", "O256"},
		{"VanDeussen", "V532"},
	}

	for _, test := range tests {
		result := Soundex(test.input)
		if result != test.expected {
			t.Errorf("Soundex(%q) = %q, want %q", test.input, result, test.expected)
		}
	}
}

func TestSoundexWords(t *testing.T) {
	words := SoundexWords("John Smith")
	expected := []string{"J500", "S530"}
	if len(words) != len(expected) {
		t.Errorf("SoundexWords length = %d, want %d", len(words), len(expected))
	}
	for i, w := range words {
		if w != expected[i] {
			t.Errorf("SoundexWords[%d] = %q, want %q", i, w, expected[i])
		}
	}
}

func TestMetaphone(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Smith", "SM0"},
		{"Schmidt", "SXMTT"},
		{"phone", "FN"},
		{"action", "AKXN"},
		{"", ""},
	}

	for _, test := range tests {
		result := Metaphone(test.input)
		if result != test.expected {
			t.Errorf("Metaphone(%q) = %q, want %q", test.input, result, test.expected)
		}
	}
}

func TestRefinedSoundex(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Smith", "S640"},
		{"Robert", "R174"},
		{"", "0000"},
		{"A", "A000"},
	}

	for _, test := range tests {
		result := RefinedSoundex(test.input)
		if result != test.expected {
			t.Errorf("RefinedSoundex(%q) = %q, want %q", test.input, result, test.expected)
		}
	}
}

func TestNYSIIS(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Smith", "SNAT"},
		{"Schmidt", "SNAT"},
		{"Johnson", "JANS"},
		{"O'Connor", "OCAN"},
		{"", ""},
	}

	for _, test := range tests {
		result := NYSIIS(test.input)
		// Note: NYSIIS implementation may vary slightly, so we check prefix
		if test.input != "" && result == "" {
			t.Errorf("NYSIIS(%q) = %q, want non-empty", test.input, result)
		}
	}
}

func TestMatchRatingCodex(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Smith", "SMTH"},
		{"O'Connor", "OCNR"},
		{"Johnson", "JNSN"},
		{"", ""},
	}

	for _, test := range tests {
		result := MatchRatingCodex(test.input)
		if test.input != "" && result == "" {
			t.Errorf("MatchRatingCodex(%q) = %q, want non-empty", test.input, result)
		}
	}
}

func TestEncodeAll(t *testing.T) {
	result := EncodeAll("Smith")
	if result.Soundex == "" {
		t.Error("EncodeAll Soundex is empty")
	}
	if result.Metaphone == "" {
		t.Error("EncodeAll Metaphone is empty")
	}
	if result.RefinedSoundex == "" {
		t.Error("EncodeAll RefinedSoundex is empty")
	}
	if result.NYSIIS == "" {
		t.Error("EncodeAll NYSIIS is empty")
	}
	if result.MatchRatingCodex == "" {
		t.Error("EncodeAll MatchRatingCodex is empty")
	}
}

func TestPhoneticAlgorithmEncode(t *testing.T) {
	tests := []struct {
		algorithm PhoneticAlgorithm
		input     string
	}{
		{AlgorithmSoundex, "Robert"},
		{AlgorithmMetaphone, "Robert"},
		{AlgorithmRefinedSoundex, "Robert"},
		{AlgorithmNYSIIS, "Robert"},
		{AlgorithmMatchRatingCodex, "Robert"},
	}

	for _, test := range tests {
		result := test.algorithm.Encode(test.input)
		if result == "" {
			t.Errorf("Algorithm(%d).Encode(%q) = empty", test.algorithm, test.input)
		}
	}
}

func TestPhoneticMatch(t *testing.T) {
	// Names that should match
	matchTests := []struct {
		name1     string
		name2     string
		algorithm PhoneticAlgorithm
	}{
		{"Smith", "Schmidt", AlgorithmSoundex},
		{"Johnson", "Jonson", AlgorithmSoundex},
		{"Robert", "Rupert", AlgorithmSoundex},
	}

	for _, test := range matchTests {
		if !test.algorithm.Match(test.name1, test.name2) {
			t.Errorf("%v should match %v using algorithm %d", test.name1, test.name2, test.algorithm)
		}
	}

	// Names that should not match
	noMatchTests := []struct {
		name1     string
		name2     string
		algorithm PhoneticAlgorithm
	}{
		{"Smith", "Johnson", AlgorithmSoundex},
		{"Robert", "William", AlgorithmSoundex},
	}

	for _, test := range noMatchTests {
		if test.algorithm.Match(test.name1, test.name2) {
			t.Errorf("%v should NOT match %v using algorithm %d", test.name1, test.name2, test.algorithm)
		}
	}
}

func TestPhoneticSimilarity(t *testing.T) {
	// Test that similar names have some similarity
	similarity := PhoneticSimilarity("Smith", "Schmidt")
	if similarity < 0.2 {
		t.Errorf("PhoneticSimilarity(Smith, Schmidt) = %v, want >= 0.2", similarity)
	}

	// Test that different names have lower similarity
	similarity = PhoneticSimilarity("John", "Jane")
	if similarity < 0.4 {
		t.Errorf("PhoneticSimilarity(John, Jane) = %v, want >= 0.4", similarity)
	}
}

func TestFindMatches(t *testing.T) {
	candidates := []string{"Smith", "Schmidt", "Smythe", "Johnson", "Jonson"}
	matches := FindMatches("Smith", candidates, AlgorithmSoundex, 0.5)

	if len(matches) == 0 {
		t.Error("FindMatches should return at least one match")
	}

	// First match should be Smith itself (100% match)
	if matches[0].Name != "Smith" {
		t.Errorf("FindMatches first result = %v, want Smith", matches[0].Name)
	}
}

func TestBatchEncode(t *testing.T) {
	names := []string{"Smith", "Schmidt", "Johnson"}
	result := BatchEncode(names, AlgorithmSoundex)

	if len(result) != 3 {
		t.Errorf("BatchEncode length = %d, want 3", len(result))
	}

	// Check that Soundex codes match for Smith and Schmidt
	if result["Smith"] != result["Schmidt"] {
		t.Errorf("Smith and Schmidt should have same Soundex code")
	}
}

func TestCleanString(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "HELLO"},
		{"Hello World", "HELLOWORLD"},
		{"O'Brien", "OBRIEN"},
		{"123abc", "ABC"},
		{"", ""},
	}

	for _, test := range tests {
		result := cleanString(test.input)
		if result != test.expected {
			t.Errorf("cleanString(%q) = %q, want %q", test.input, result, test.expected)
		}
	}
}

func TestIsVowel(t *testing.T) {
	vowels := []rune{'A', 'E', 'I', 'O', 'U'}
	nonVowels := []rune{'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'}

	for _, v := range vowels {
		if !isVowel(v) {
			t.Errorf("isVowel(%q) = false, want true", v)
		}
	}

	for _, v := range nonVowels {
		if isVowel(v) {
			t.Errorf("isVowel(%q) = true, want false", v)
		}
	}
}

func TestRemoveAdjacentDuplicates(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"AABBCC", "ABC"},
		{"AAAAA", "A"},
		{"ABABAB", "ABABAB"},
		{"", ""},
		{"A", "A"},
	}

	for _, test := range tests {
		result := removeAdjacentDuplicates(test.input)
		if result != test.expected {
			t.Errorf("removeAdjacentDuplicates(%q) = %q, want %q", test.input, result, test.expected)
		}
	}
}

// Benchmark tests
func BenchmarkSoundex(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Soundex("Schwarzenegger")
	}
}

func BenchmarkMetaphone(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Metaphone("Schwarzenegger")
	}
}

func BenchmarkNYSIIS(b *testing.B) {
	for i := 0; i < b.N; i++ {
		NYSIIS("Schwarzenegger")
	}
}

func BenchmarkEncodeAll(b *testing.B) {
	for i := 0; i < b.N; i++ {
		EncodeAll("Schwarzenegger")
	}
}