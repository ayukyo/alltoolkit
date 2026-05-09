package pluralize_utils

import (
	"testing"
)

func TestSingularToPlural_RegularNouns(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"cat", "cats"},
		{"dog", "dogs"},
		{"book", "books"},
		{"pen", "pens"},
		{"table", "tables"},
		{"car", "cars"},
		{"house", "houses"},
		{"tree", "trees"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_EndingWithSXZCHSH(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"bus", "buses"},
		{"box", "boxes"},
		{"quiz", "quizzes"},
		{"church", "churches"},
		{"brush", "brushes"},
		{"class", "classes"},
		{"glass", "glasses"},
		{"match", "matches"},
		{"dish", "dishes"},
		{"fix", "fixes"},
		{"buzz", "buzzes"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_EndingWithY(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		// Consonant + y -> ies
		{"city", "cities"},
		{"story", "stories"},
		{"baby", "babies"},
		{"party", "parties"},
		{"lady", "ladies"},
		{"country", "countries"},
		{"fly", "flies"},
		{"try", "tries"},
		// Vowel + y -> s
		{"day", "days"},
		{"boy", "boys"},
		{"toy", "toys"},
		{"key", "keys"},
		{"guy", "guys"},
		{"valley", "valleys"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_EndingWithO(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		// -oes ending
		{"potato", "potatoes"},
		{"tomato", "tomatoes"},
		{"hero", "heroes"},
		{"echo", "echoes"},
		{"torpedo", "torpedoes"},
		{"veto", "vetoes"},
		{"mosquito", "mosquitoes"},
		// -os ending
		{"photo", "photos"},
		{"piano", "pianos"},
		{"radio", "radios"},
		{"video", "videos"},
		{"logo", "logos"},
		{"taco", "tacos"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_EndingWithF(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"knife", "knives"},
		{"wife", "wives"},
		{"life", "lives"},
		{"leaf", "leaves"},
		{"wolf", "wolves"},
		{"shelf", "shelves"},
		{"thief", "thieves"},
		{"half", "halves"},
		{"calf", "calves"},
		{"loaf", "loaves"},
		// Exceptions (don't change)
		{"roof", "roofs"},
		{"chief", "chiefs"},
		{"belief", "beliefs"},
		{"chef", "chefs"},
		{"cliff", "cliffs"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_IrregularNouns(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"man", "men"},
		{"woman", "women"},
		{"child", "children"},
		{"person", "people"},
		{"foot", "feet"},
		{"tooth", "teeth"},
		{"goose", "geese"},
		{"mouse", "mice"},
		{"ox", "oxen"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_LatinGreekNouns(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"analysis", "analyses"},
		{"basis", "bases"},
		{"crisis", "crises"},
		{"phenomenon", "phenomena"},
		{"criterion", "criteria"},
		{"datum", "data"},
		{"medium", "media"},
		{"curriculum", "curricula"},
		{"focus", "foci"},
		{"fungus", "fungi"},
		{"nucleus", "nuclei"},
		{"stimulus", "stimuli"},
		{"syllabus", "syllabi"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_UncountableNouns(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"sheep", "sheep"},
		{"deer", "deer"},
		{"fish", "fish"},
		{"species", "species"},
		{"series", "series"},
		{"moose", "moose"},
		{"information", "information"},
		{"news", "news"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_CasePreservation(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Cat", "Cats"},
		{"CAT", "CATS"},
		{"Child", "Children"},
		{"MAN", "MEN"},
		{"Woman", "Women"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_WithCount(t *testing.T) {
	if result := SingularToPlural("cat", 1); result != "cat" {
		t.Errorf("SingularToPlural(\"cat\", 1) = %q, want \"cat\"", result)
	}
	if result := SingularToPlural("cat", 2); result != "cats" {
		t.Errorf("SingularToPlural(\"cat\", 2) = %q, want \"cats\"", result)
	}
	if result := SingularToPlural("cat", 0); result != "cats" {
		t.Errorf("SingularToPlural(\"cat\", 0) = %q, want \"cats\"", result)
	}
}

func TestSingularToPlural_EmptyString(t *testing.T) {
	if result := SingularToPlural(""); result != "" {
		t.Errorf("SingularToPlural(\"\") = %q, want \"\"", result)
	}
}

func TestSingularToPlural_HyphenatedWords(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"brother-in-law", "brothers-in-law"},
		{"mother-in-law", "mothers-in-law"},
		{"passer-by", "passers-by"},
		{"father-in-law", "fathers-in-law"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_Pronouns(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"he", "they"},
		{"she", "they"},
		{"it", "they"},
		{"this", "these"},
		{"that", "those"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

// Tests for PluralToSingular

func TestPluralToSingular_RegularNouns(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"cats", "cat"},
		{"dogs", "dog"},
		{"books", "book"},
		{"pens", "pen"},
		{"tables", "table"},
	}

	for _, tt := range tests {
		result := PluralToSingular(tt.input)
		if result != tt.expected {
			t.Errorf("PluralToSingular(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestPluralToSingular_EndingWithEs(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"boxes", "box"},
		{"buses", "bus"},
		{"churches", "church"},
		{"brushes", "brush"},
		{"classes", "class"},
		{"matches", "match"},
		{"dishes", "dish"},
	}

	for _, tt := range tests {
		result := PluralToSingular(tt.input)
		if result != tt.expected {
			t.Errorf("PluralToSingular(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestPluralToSingular_EndingWithIes(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"cities", "city"},
		{"stories", "story"},
		{"babies", "baby"},
		{"parties", "party"},
		{"ladies", "lady"},
		{"countries", "country"},
	}

	for _, tt := range tests {
		result := PluralToSingular(tt.input)
		if result != tt.expected {
			t.Errorf("PluralToSingular(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestPluralToSingular_EndingWithVes(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"knives", "knife"},
		{"wives", "wife"},
		{"lives", "life"},
		{"leaves", "leaf"},
		{"wolves", "wolf"},
		{"shelves", "shelf"},
		{"thieves", "thief"},
		{"halves", "half"},
	}

	for _, tt := range tests {
		result := PluralToSingular(tt.input)
		if result != tt.expected {
			t.Errorf("PluralToSingular(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestPluralToSingular_IrregularNouns(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"men", "man"},
		{"women", "woman"},
		{"children", "child"},
		{"people", "person"},
		{"feet", "foot"},
		{"teeth", "tooth"},
		{"geese", "goose"},
		{"mice", "mouse"},
	}

	for _, tt := range tests {
		result := PluralToSingular(tt.input)
		if result != tt.expected {
			t.Errorf("PluralToSingular(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestPluralToSingular_LatinGreekNouns(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"analyses", "analysis"},
		{"bases", "basis"},
		{"crises", "crisis"},
		{"phenomena", "phenomenon"},
		{"criteria", "criterion"},
		{"data", "datum"},
		{"media", "medium"},
		{"curricula", "curriculum"},
		{"foci", "focus"},
		{"fungi", "fungus"},
		{"nuclei", "nucleus"},
		{"stimuli", "stimulus"},
	}

	for _, tt := range tests {
		result := PluralToSingular(tt.input)
		if result != tt.expected {
			t.Errorf("PluralToSingular(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestPluralToSingular_CasePreservation(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Cats", "Cat"},
		{"CATS", "CAT"},
		{"Children", "Child"},
		{"MEN", "MAN"},
	}

	for _, tt := range tests {
		result := PluralToSingular(tt.input)
		if result != tt.expected {
			t.Errorf("PluralToSingular(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestPluralToSingular_EmptyString(t *testing.T) {
	if result := PluralToSingular(""); result != "" {
		t.Errorf("PluralToSingular(\"\") = %q, want \"\"", result)
	}
}

// Tests for IsPlural

func TestIsPlural_RegularPlurals(t *testing.T) {
	plurals := []string{"cats", "dogs", "boxes", "cities"}
	for _, word := range plurals {
		if !IsPlural(word) {
			t.Errorf("IsPlural(%q) = false, want true", word)
		}
	}
}

func TestIsPlural_SingularNouns(t *testing.T) {
	singulars := []string{"cat", "dog", "box", "city"}
	for _, word := range singulars {
		if IsPlural(word) {
			t.Errorf("IsPlural(%q) = true, want false", word)
		}
	}
}

func TestIsPlural_IrregularPlurals(t *testing.T) {
	plurals := []string{"men", "women", "children", "people", "feet", "teeth"}
	for _, word := range plurals {
		if !IsPlural(word) {
			t.Errorf("IsPlural(%q) = false, want true", word)
		}
	}
}

func TestIsPlural_UncountableNouns(t *testing.T) {
	uncountable := []string{"sheep", "deer", "fish", "information"}
	for _, word := range uncountable {
		if IsPlural(word) {
			t.Errorf("IsPlural(%q) = true, want false", word)
		}
	}
}

func TestIsPlural_SingularOnlyWords(t *testing.T) {
	singularOnly := []string{"news", "politics", "mathematics", "physics", "series", "species"}
	for _, word := range singularOnly {
		if IsPlural(word) {
			t.Errorf("IsPlural(%q) = true, want false", word)
		}
	}
}

// Tests for GetPluralForm

func TestGetPluralForm_CountOne(t *testing.T) {
	tests := []struct {
		word     string
		count    int
		expected string
	}{
		{"cat", 1, "cat"},
		{"cats", 1, "cat"},
		{"box", 1, "box"},
		{"child", 1, "child"},
	}

	for _, tt := range tests {
		result := GetPluralForm(tt.word, tt.count)
		if result != tt.expected {
			t.Errorf("GetPluralForm(%q, %d) = %q, want %q", tt.word, tt.count, result, tt.expected)
		}
	}
}

func TestGetPluralForm_CountOther(t *testing.T) {
	tests := []struct {
		word     string
		count    int
		expected string
	}{
		{"cat", 0, "cats"},
		{"cat", 2, "cats"},
		{"cat", 100, "cats"},
		{"box", 2, "boxes"},
		{"child", 3, "children"},
	}

	for _, tt := range tests {
		result := GetPluralForm(tt.word, tt.count)
		if result != tt.expected {
			t.Errorf("GetPluralForm(%q, %d) = %q, want %q", tt.word, tt.count, result, tt.expected)
		}
	}
}

// Tests for BatchPluralize

func TestBatchPluralize(t *testing.T) {
	input := []string{"cat", "dog", "box", "city"}
	expected := []string{"cats", "dogs", "boxes", "cities"}
	result := BatchPluralize(input)

	for i, word := range result {
		if word != expected[i] {
			t.Errorf("BatchPluralize[%d] = %q, want %q", i, word, expected[i])
		}
	}
}

func TestBatchPluralize_EmptyList(t *testing.T) {
	result := BatchPluralize([]string{})
	if len(result) != 0 {
		t.Errorf("BatchPluralize([]) = %v, want []", result)
	}
}

// Tests for BatchSingularize

func TestBatchSingularize(t *testing.T) {
	input := []string{"cats", "dogs", "boxes", "cities"}
	expected := []string{"cat", "dog", "box", "city"}
	result := BatchSingularize(input)

	for i, word := range result {
		if word != expected[i] {
			t.Errorf("BatchSingularize[%d] = %q, want %q", i, word, expected[i])
		}
	}
}

func TestBatchSingularize_EmptyList(t *testing.T) {
	result := BatchSingularize([]string{})
	if len(result) != 0 {
		t.Errorf("BatchSingularize([]) = %v, want []", result)
	}
}

// Tests for GetArticle

func TestGetArticle_ConsonantStart(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"cat", "a"},
		{"dog", "a"},
		{"book", "a"},
		{"pen", "a"},
	}

	for _, tt := range tests {
		result := GetArticle(tt.input)
		if result != tt.expected {
			t.Errorf("GetArticle(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestGetArticle_VowelStart(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"apple", "an"},
		{"orange", "an"},
		{"elephant", "an"},
		{"umbrella", "an"},
		{"ice", "an"},
	}

	for _, tt := range tests {
		result := GetArticle(tt.input)
		if result != tt.expected {
			t.Errorf("GetArticle(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestGetArticle_WithCount(t *testing.T) {
	if result := GetArticle("cat", 1); result != "a" {
		t.Errorf("GetArticle(\"cat\", 1) = %q, want \"a\"", result)
	}
	if result := GetArticle("apple", 1); result != "an" {
		t.Errorf("GetArticle(\"apple\", 1) = %q, want \"an\"", result)
	}
	if result := GetArticle("cat", 2); result != "" {
		t.Errorf("GetArticle(\"cat\", 2) = %q, want \"\"", result)
	}
	if result := GetArticle("cat", 0); result != "" {
		t.Errorf("GetArticle(\"cat\", 0) = %q, want \"\"", result)
	}
}

func TestGetArticle_CaseInsensitive(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Apple", "an"},
		{"ORANGE", "an"},
		{"Cat", "a"},
		{"DOG", "a"},
	}

	for _, tt := range tests {
		result := GetArticle(tt.input)
		if result != tt.expected {
			t.Errorf("GetArticle(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

// Tests for FormatCount

func TestFormatCount_SingleItem(t *testing.T) {
	tests := []struct {
		word     string
		count    int
		expected string
	}{
		{"cat", 1, "a cat"},
		{"apple", 1, "an apple"},
		{"dog", 1, "a dog"},
	}

	for _, tt := range tests {
		result := FormatCount(tt.word, tt.count)
		if result != tt.expected {
			t.Errorf("FormatCount(%q, %d) = %q, want %q", tt.word, tt.count, result, tt.expected)
		}
	}
}

func TestFormatCount_MultipleItems(t *testing.T) {
	tests := []struct {
		word     string
		count    int
		expected string
	}{
		{"cat", 0, "0 cats"},
		{"cat", 2, "2 cats"},
		{"box", 5, "5 boxes"},
		{"city", 10, "10 cities"},
	}

	for _, tt := range tests {
		result := FormatCount(tt.word, tt.count)
		if result != tt.expected {
			t.Errorf("FormatCount(%q, %d) = %q, want %q", tt.word, tt.count, result, tt.expected)
		}
	}
}

func TestFormatCount_WithoutArticle(t *testing.T) {
	if result := FormatCount("cat", 1, false); result != "cat" {
		t.Errorf("FormatCount(\"cat\", 1, false) = %q, want \"cat\"", result)
	}
	if result := FormatCount("apple", 1, false); result != "apple" {
		t.Errorf("FormatCount(\"apple\", 1, false) = %q, want \"apple\"", result)
	}
}

func TestFormatCount_IrregularNouns(t *testing.T) {
	tests := []struct {
		word     string
		count    int
		expected string
	}{
		{"child", 2, "2 children"},
		{"person", 5, "5 people"},
		{"man", 3, "3 men"},
	}

	for _, tt := range tests {
		result := FormatCount(tt.word, tt.count)
		if result != tt.expected {
			t.Errorf("FormatCount(%q, %d) = %q, want %q", tt.word, tt.count, result, tt.expected)
		}
	}
}

// Test round-trip conversion

func TestRoundTrip_SingularPluralSingular(t *testing.T) {
	words := []string{"cat", "dog", "box", "city", "knife", "child", "man", "person"}
	for _, word := range words {
		plural := SingularToPlural(word)
		singular := PluralToSingular(plural)
		if singular != word {
			t.Errorf("Round trip failed: %q -> %q -> %q", word, plural, singular)
		}
	}
}

func TestRoundTrip_PluralSingularPlural(t *testing.T) {
	words := []string{"cats", "dogs", "boxes", "cities", "knives", "children", "men", "people"}
	for _, word := range words {
		singular := PluralToSingular(word)
		plural := SingularToPlural(singular)
		if plural != word {
			t.Errorf("Round trip failed: %q -> %q -> %q", word, singular, plural)
		}
	}
}

// Edge case tests

func TestSingularToPlural_SingleLetter(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"a", "as"},
		{"x", "xes"},
		{"X", "XES"},
	}

	for _, tt := range tests {
		result := SingularToPlural(tt.input)
		if result != tt.expected {
			t.Errorf("SingularToPlural(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSingularToPlural_AlreadyPlural(t *testing.T) {
	// singular_to_plural assumes input is singular
	// "cats" ends with 's' so it gets 'es' added
	if result := SingularToPlural("cats"); result != "catses" {
		t.Errorf("SingularToPlural(\"cats\") = %q, want \"catses\"", result)
	}
}