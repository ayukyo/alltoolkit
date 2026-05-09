// Package pluralize_utils provides English singular/plural word conversion utilities.
// Zero external dependencies, pure Go implementation.
//
// Features:
//   - Singular to plural conversion
//   - Plural to singular conversion
//   - Check if word is plural
//   - Get correct form based on count
//   - Batch operations
//   - Article handling
package pluralize_utils

import (
	"strconv"
	"strings"
	"unicode"
)

// irregularPlurals maps singular to plural for irregular words
var irregularPlurals = map[string]string{
	// Personal pronouns
	"i":    "we",
	"me":   "us",
	"my":   "our",
	"mine": "ours",
	"he":   "they",
	"him":  "them",
	"his":  "their",
	"she":  "they",
	"her":  "them",
	"hers": "theirs",
	"it":   "they",
	"its":  "their",
	"this": "these",
	"that": "those",

	// Common irregular nouns
	"man":     "men",
	"woman":   "women",
	"child":   "children",
	"person":  "people",
	"foot":    "feet",
	"tooth":   "teeth",
	"goose":   "geese",
	"mouse":   "mice",
	"louse":   "lice",
	"ox":      "oxen",
	"brother": "brothers",
	"die":     "dice",
	"penny":   "pence",

	// -f/-fe ending -> -ves
	"leaf":  "leaves",
	"loaf":  "loaves",
	"knife": "knives",
	"wife":  "wives",
	"life":  "lives",
	"wolf":  "wolves",
	"calf":  "calves",
	"half":  "halves",
	"self":  "selves",
	"shelf": "shelves",
	"thief": "thieves",

	// Latin/Greek origin words
	"analysis":    "analyses",
	"basis":       "bases",
	"crisis":      "crises",
	"diagnosis":   "diagnoses",
	"hypothesis":  "hypotheses",
	"oasis":       "oases",
	"parenthesis": "parentheses",
	"thesis":      "theses",
	"phenomenon":  "phenomena",
	"criterion":   "criteria",
	"datum":       "data",
	"medium":      "media",
	"bacterium":   "bacteria",
	"curriculum":  "curricula",
	"appendix":    "appendices",
	"index":       "indices",
	"matrix":      "matrices",
	"vertex":      "vertices",
	"axis":        "axes",
	"focus":       "foci",
	"fungus":      "fungi",
	"nucleus":     "nuclei",
	"radius":      "radii",
	"stimulus":    "stimuli",
	"syllabus":    "syllabi",
	"alumnus":     "alumni",
	"corpus":      "corpora",
	"genus":       "genera",
	"opus":        "opera",

	// French origin words
	"beau":    "beaux",
	"bureau":  "bureaux",
	"tableau": "tableaux",
	"chateau": "chateaux",

	// Same singular and plural form
	"sheep":      "sheep",
	"deer":       "deer",
	"fish":       "fish",
	"species":    "species",
	"series":     "series",
	"moose":      "moose",
	"swine":      "swine",
	"aircraft":   "aircraft",
	"spacecraft": "spacecraft",
	"salmon":     "salmon",
	"trout":      "trout",
	"bison":      "bison",
	"shrimp":     "shrimp",
	"means":      "means",
	"offspring":  "offspring",

	// Uncountable nouns
	"information": "information",
	"knowledge":   "knowledge",
	"advice":      "advice",
	"furniture":   "furniture",
	"equipment":   "equipment",
	"luggage":     "luggage",
	"traffic":     "traffic",
	"homework":    "homework",
	"news":        "news",
	"mathematics": "mathematics",
	"physics":     "physics",
	"economics":   "economics",
	"politics":    "politics",
	"measles":     "measles",
	"mumps":       "mumps",
	"billiards":   "billiards",
	"darts":       "darts",
}

// irregularSingulars maps plural to singular (reverse of irregularPlurals)
var irregularSingulars = make(map[string]string)

// uncountableWords contains words that don't change form
var uncountableWords = map[string]bool{
	"sheep":      true,
	"deer":       true,
	"fish":       true,
	"species":    true,
	"series":     true,
	"moose":      true,
	"swine":      true,
	"aircraft":   true,
	"spacecraft": true,
	"salmon":     true,
	"trout":      true,
	"bison":      true,
	"shrimp":     true,
	"means":      true,
	"offspring":  true,
	"information": true,
	"knowledge":   true,
	"advice":      true,
	"furniture":   true,
	"equipment":   true,
	"luggage":     true,
	"traffic":     true,
	"homework":    true,
	"news":        true,
	"mathematics": true,
	"physics":     true,
	"economics":   true,
	"politics":    true,
	"measles":     true,
	"mumps":       true,
	"billiards":   true,
	"darts":       true,
}

// singularOnlyWords are words ending in 's' but are singular
var singularOnlyWords = map[string]bool{
	"news":        true,
	"politics":    true,
	"mathematics": true,
	"physics":     true,
	"economics":   true,
	"athletics":   true,
	"measles":     true,
	"mumps":       true,
	"billiards":   true,
	"darts":       true,
	"tactics":     true,
	"series":      true,
	"species":     true,
}

// oEndingOesWords are words ending in 'o' that add 'es'
var oEndingOesWords = map[string]bool{
	"potato":  true,
	"tomato":  true,
	"hero":    true,
	"echo":    true,
	"torpedo": true,
	"veto":    true,
	"mosquito": true,
}

// fFeEndingExceptions are words ending in 'f' that don't follow the ves rule
// (these words just add 's' instead of changing f to ves)
var fFeEndingExceptions = map[string]bool{
	"roof":   true,
	"chief":  true,
	"belief": true,
	"chef":   true,
	"cliff":  true,
	"sheriff": true,
	"proof":  true,
	"hoof":   true,
}

func init() {
	// Build reverse mapping
	for singular, plural := range irregularPlurals {
		irregularSingulars[plural] = singular
	}
}

// SingularToPlural converts a singular word to its plural form.
// If count is provided and equals 1, the singular form is returned.
func SingularToPlural(word string, count ...int) string {
	if word == "" {
		return ""
	}

	// If count is provided and equals 1, return singular
	if len(count) > 0 && count[0] == 1 {
		return word
	}

	lowerWord := strings.ToLower(word)

	// Check if uncountable
	if uncountableWords[lowerWord] {
		return word
	}

	// Check irregular plurals
	if plural, ok := irregularPlurals[lowerWord]; ok {
		return preserveCase(word, plural)
	}

	// Apply rules
	return applyPluralRules(word)
}

// PluralToSingular converts a plural word to its singular form.
func PluralToSingular(word string) string {
	if word == "" {
		return ""
	}

	lowerWord := strings.ToLower(word)

	// Check if uncountable
	if uncountableWords[lowerWord] {
		return word
	}

	// Check irregular singulars
	if singular, ok := irregularSingulars[lowerWord]; ok {
		return preserveCase(word, singular)
	}

	// Apply rules
	return applySingularRules(word)
}

// IsPlural checks if a word is in plural form.
func IsPlural(word string) bool {
	if word == "" {
		return false
	}

	lowerWord := strings.ToLower(word)

	// Singular-only words ending in 's'
	if singularOnlyWords[lowerWord] {
		return false
	}

	// Uncountable words
	if uncountableWords[lowerWord] {
		return false
	}

	// Check if it's in the plural form of irregular words
	if _, ok := irregularSingulars[lowerWord]; ok {
		return true
	}

	// Check if it's a singular form in irregular plurals
	if _, ok := irregularPlurals[lowerWord]; ok {
		// For words that are same in singular and plural
		if irregularPlurals[lowerWord] == lowerWord {
			return false
		}
		return false
	}

	// Common plural endings
	if strings.HasSuffix(lowerWord, "s") && !strings.HasSuffix(lowerWord, "ss") {
		return true
	}

	return false
}

// GetPluralForm returns the correct singular or plural form based on count.
func GetPluralForm(word string, count int) string {
	if count == 1 {
		return PluralToSingular(word)
	}
	return SingularToPlural(word)
}

// BatchPluralize converts multiple words to plural form.
func BatchPluralize(words []string) []string {
	result := make([]string, len(words))
	for i, word := range words {
		result[i] = SingularToPlural(word)
	}
	return result
}

// BatchSingularize converts multiple words to singular form.
func BatchSingularize(words []string) []string {
	result := make([]string, len(words))
	for i, word := range words {
		result[i] = PluralToSingular(word)
	}
	return result
}

// GetArticle returns the appropriate article ("a" or "an") for a word.
// Returns empty string for count > 1.
func GetArticle(word string, count ...int) string {
	if len(count) > 0 && count[0] != 1 {
		return ""
	}

	if word == "" {
		return "a"
	}

	lowerWord := strings.ToLower(word)
	first := rune(lowerWord[0])

	switch first {
	case 'a', 'e', 'i', 'o', 'u':
		return "an"
	default:
		return "a"
	}
}

// FormatCount formats a count with the correct word form.
// Example: FormatCount("cat", 1) -> "a cat"
// Example: FormatCount("cat", 2) -> "2 cats"
// Example: FormatCount("cat", 1, false) -> "cat" (no article, no count)
func FormatCount(word string, count int, includeArticle ...bool) string {
	useArticle := true
	if len(includeArticle) > 0 {
		useArticle = includeArticle[0]
	}

	correctWord := GetPluralForm(word, count)

	if count == 1 {
		if useArticle {
			return GetArticle(word, count) + " " + correctWord
		}
		return correctWord
	}

	return strconv.Itoa(count) + " " + correctWord
}

// preserveCase preserves the original case pattern in the result.
func preserveCase(original, result string) string {
	if original == "" || result == "" {
		return result
	}

	// All uppercase
	if isAllUpper(original) {
		return strings.ToUpper(result)
	}

	// First letter uppercase, rest lowercase
	if unicode.IsUpper(rune(original[0])) {
		if len(result) > 0 {
			return strings.ToUpper(string(result[0])) + strings.ToLower(result[1:])
		}
	}

	return result
}

// isAllUpper checks if all letters in a string are uppercase.
func isAllUpper(s string) bool {
	hasLetter := false
	for _, r := range s {
		if unicode.IsLetter(r) {
			hasLetter = true
			if !unicode.IsUpper(r) {
				return false
			}
		}
	}
	return hasLetter
}

// addSuffixPreservingCase adds a suffix while preserving uppercase words
func addSuffixPreservingCase(word, suffix string) string {
	if isAllUpper(word) {
		return word + strings.ToUpper(suffix)
	}
	return word + suffix
}

// applyPluralRules applies standard pluralization rules.
func applyPluralRules(word string) string {
	lowerWord := strings.ToLower(word)

	// Handle hyphenated words
	if strings.Contains(word, "-") {
		return handleHyphenatedPlural(word)
	}

	// Words ending in 'z' -> add 'es' (buzz -> buzzes, quiz -> quizzes)
	// For single z ending words, we need to double the z (quiz -> quizzes)
	// But for double z ending words, just add es (buzz -> buzzes)
	if strings.HasSuffix(lowerWord, "z") {
		// Check if already ends with double z (buzz)
		if len(lowerWord) >= 2 && lowerWord[len(lowerWord)-2] == 'z' {
			// Double z, just add 'es'
			return addSuffixPreservingCase(word, "es")
		}
		// Single z, double it and add 'es'
		return word + "zes"
	}

	// Words ending in 's', 'x', 'ch', 'sh' -> add 'es'
	if strings.HasSuffix(lowerWord, "s") ||
		strings.HasSuffix(lowerWord, "x") ||
		strings.HasSuffix(lowerWord, "ch") ||
		strings.HasSuffix(lowerWord, "sh") {
		return addSuffixPreservingCase(word, "es")
	}

	// Words ending in 'y' preceded by consonant -> 'ies'
	if strings.HasSuffix(lowerWord, "y") && len(lowerWord) > 1 {
		prev := rune(lowerWord[len(lowerWord)-2])
		if !isVowel(prev) {
			return preserveCase(word, strings.ToLower(word[:len(word)-1]) + "ies")
		}
	}

	// Words ending in 'o'
	if strings.HasSuffix(lowerWord, "o") {
		// Some add 'es', others just 's'
		if oEndingOesWords[lowerWord] {
			return word + "es"
		}
		// Default: add 's' for most words ending in 'o'
		return word + "s"
	}

	// Words ending in 'fe' that should become 'ves'
	if strings.HasSuffix(lowerWord, "fe") {
		// Check if the whole word (without 'e') is an exception
		// e.g., "wife" is not an exception, "knife" is not an exception
		stemWithoutE := lowerWord[:len(lowerWord)-1] // "wif", "knif"
		if fFeEndingExceptions[stemWithoutE] {
			// Exception: just add 's'
			return addSuffixPreservingCase(word, "s")
		}
		return word[:len(word)-2] + "ves"
	}

	// Words ending in 'f' that should become 'ves'
	if strings.HasSuffix(lowerWord, "f") {
		// Check if the whole word is an exception
		if fFeEndingExceptions[lowerWord] {
			// Exception: just add 's'
			return addSuffixPreservingCase(word, "s")
		}
		return word[:len(word)-1] + "ves"
	}

	// Default: add 's'
	return addSuffixPreservingCase(word, "s")
}

// applySingularRules applies standard singularization rules.
func applySingularRules(word string) string {
	lowerWord := strings.ToLower(word)

	// Handle hyphenated words
	if strings.Contains(word, "-") {
		return handleHyphenatedSingular(word)
	}

	// Words ending in 'zes' (from quiz -> quizzes)
	if strings.HasSuffix(lowerWord, "zes") && len(lowerWord) > 4 {
		// Check if the word before 'zes' ends with 'z'
		stem := word[:len(word)-3]
		if strings.HasSuffix(strings.ToLower(stem), "z") {
			return stem
		}
	}

	// Words ending in 'ies' -> 'y' (consonant + y -> ies)
	if strings.HasSuffix(lowerWord, "ies") && len(lowerWord) > 3 {
		return word[:len(word)-3] + "y"
	}

	// Words ending in 'ves' -> 'f' or 'fe'
	if strings.HasSuffix(lowerWord, "ves") && len(lowerWord) > 3 {
		stem := word[:len(word)-3]
		lowerStem := strings.ToLower(stem)
		// Check which form is correct
		if irregularPlurals[lowerStem+"f"] != "" || fFeEndingExceptions[lowerStem] {
			return stem + "f"
		}
		if irregularPlurals[lowerStem+"fe"] != "" {
			return stem + "fe"
		}
		// Default to 'f' for unknown words ending in ves
		return stem + "f"
	}

	// Words ending in 'es'
	if strings.HasSuffix(lowerWord, "es") && len(lowerWord) > 2 {
		// -xes, -ses, -ches, -shes
		if strings.HasSuffix(lowerWord, "xes") ||
			strings.HasSuffix(lowerWord, "ses") ||
			strings.HasSuffix(lowerWord, "ches") ||
			strings.HasSuffix(lowerWord, "shes") {
			return word[:len(word)-2]
		}

		// -oes endings (potatoes -> potato)
		if strings.HasSuffix(lowerWord, "oes") && len(lowerWord) > 4 {
			stem := word[:len(word)-2]
			lowerStem := strings.ToLower(stem)
			if oEndingOesWords[lowerStem] {
				return stem
			}
		}

		// Otherwise, check if removing 'es' or 's' gives a valid word
		stemEs := word[:len(word)-2]
		stemS := word[:len(word)-1]

		// Prefer removing 'es' for words ending in consonant+es
		if len(stemEs) > 0 {
			last := rune(strings.ToLower(stemEs)[len(stemEs)-1])
			if last == 'x' || last == 's' || last == 'z' || last == 'h' {
				return stemEs
			}
		}

		// For regular words ending in 'es', just remove 's'
		return stemS
	}

	// Words ending in 's' (but not 'ss')
	if strings.HasSuffix(lowerWord, "s") && !strings.HasSuffix(lowerWord, "ss") {
		return word[:len(word)-1]
	}

	// Return as is if no rule applies
	return word
}

// handleHyphenatedPlural handles pluralization of hyphenated words.
// Only the main word is pluralized: brother-in-law -> brothers-in-law
func handleHyphenatedPlural(word string) string {
	parts := strings.Split(word, "-")
	if len(parts) < 2 {
		return word
	}

	// Pluralize the first word (the main noun)
	parts[0] = SingularToPlural(parts[0])
	return strings.Join(parts, "-")
}

// handleHyphenatedSingular handles singularization of hyphenated words.
func handleHyphenatedSingular(word string) string {
	parts := strings.Split(word, "-")
	if len(parts) < 2 {
		return word
	}

	// Singularize the first word
	parts[0] = PluralToSingular(parts[0])
	return strings.Join(parts, "-")
}

// isVowel checks if a rune is a vowel.
func isVowel(r rune) bool {
	switch unicode.ToLower(r) {
	case 'a', 'e', 'i', 'o', 'u':
		return true
	default:
		return false
	}
}