// Package slug_utils provides utilities for generating URL-friendly slug strings.
// Slugs are commonly used for blog posts, product URLs, and SEO-friendly links.
package slug_utils

import (
	"regexp"
	"strings"
	"unicode"
)

// Config holds configuration options for slug generation.
type Config struct {
	// Separator is the character used to separate words (default: "-")
	Separator string
	// MaxLength limits the slug length (0 = no limit)
	MaxLength int
	// Lowercase converts the slug to lowercase (default: true)
	Lowercase bool
	// TrimSeparator removes leading/trailing separators (default: true)
	TrimSeparator bool
}

// DefaultConfig returns the default configuration.
func DefaultConfig() Config {
	return Config{
		Separator:     "-",
		MaxLength:     0,
		Lowercase:     true,
		TrimSeparator: true,
	}
}

// Slugger provides slug generation methods.
type Slugger struct {
	config Config
	// transliteration map for common characters
	translit map[rune]string
}

// New creates a new Slugger with default configuration.
func New() *Slugger {
	return NewWithConfig(DefaultConfig())
}

// NewWithConfig creates a new Slugger with custom configuration.
func NewWithConfig(config Config) *Slugger {
	// Ensure separator is valid
	if config.Separator == "" {
		config.Separator = "-"
	}

	s := &Slugger{
		config:   config,
		translit: getTransliterationMap(),
	}
	return s
}

// getTransliterationMap returns a map for transliterating common unicode characters.
func getTransliterationMap() map[rune]string {
	return map[rune]string{
		// Latin extended
		'À': "A", 'Á': "A", 'Â': "A", 'Ã': "A", 'Ä': "A", 'Å': "A",
		'Æ': "AE", 'Ç': "C",
		'È': "E", 'É': "E", 'Ê': "E", 'Ë': "E",
		'Ì': "I", 'Í': "I", 'Î': "I", 'Ï': "I",
		'Ð': "D", 'Ñ': "N",
		'Ò': "O", 'Ó': "O", 'Ô': "O", 'Õ': "O", 'Ö': "O", 'Ø': "O",
		'Ù': "U", 'Ú': "U", 'Û': "U", 'Ü': "U",
		'Ý': "Y", 'Þ': "TH", 'ß': "ss",
		'à': "a", 'á': "a", 'â': "a", 'ã': "a", 'ä': "a", 'å': "a",
		'æ': "ae", 'ç': "c",
		'è': "e", 'é': "e", 'ê': "e", 'ë': "e",
		'ì': "i", 'í': "i", 'î': "i", 'ï': "i",
		'ð': "d", 'ñ': "n",
		'ò': "o", 'ó': "o", 'ô': "o", 'õ': "o", 'ö': "o", 'ø': "o",
		'ù': "u", 'ú': "u", 'û': "u", "ü": "u",
		'ý': "y", 'þ': "th", 'ÿ': "y",
		// Cyrillic (basic transliteration)
		'а': "a", 'б': "b", 'в': "v", 'г': "g", 'д': "d",
		'е': "e", 'ё': "yo", 'ж': "zh", 'з': "z", 'и': "i",
		'й': "y", 'к': "k", 'л': "l", 'м': "m", 'н': "n",
		'о': "o", 'п': "p", 'р': "r", 'с': "s", 'т': "t",
		'у': "u", 'ф': "f", 'х': "kh", 'ц': "ts", 'ч': "ch",
		'ш': "sh", 'щ': "sch", 'ъ': "", 'ы': "y", 'ь': "",
		'э': "e", 'ю': "yu", 'я': "ya",
		'А': "A", 'Б': "B", 'В': "V", 'Г': "G", 'Д': "D",
		'Е': "E", 'Ё': "Yo", 'Ж': "Zh", 'З': "Z", 'И': "I",
		'Й': "Y", 'К': "K", 'Л': "L", 'М': "M", 'Н': "N",
		'О': "O", 'П': "P", 'Р': "R", 'С': "S", 'Т': "T",
		'У': "U", 'Ф': "F", 'Х': "Kh", 'Ц': "Ts", 'Ч': "Ch",
		'Ш': "Sh", 'Щ': "Sch", 'Ъ': "", 'Ы': "Y", 'Ь': "",
		'Э': "E", 'Ю': "Yu", 'Я': "Ya",
		// Greek
		'α': "a", 'β': "b", 'γ': "g", 'δ': "d", 'ε': "e",
		'ζ': "z", 'η': "h", 'θ': "th", 'ι': "i", 'κ': "k",
		'λ': "l", 'μ': "m", 'ν': "n", 'ξ': "x", 'ο': "o",
		'π': "p", 'ρ': "r", 'σ': "s", 'τ': "t", 'υ': "y",
		'φ': "f", 'χ': "ch", 'ψ': "ps", 'ω': "o",
		// German special characters
		'Ü': "Ue", 'Ö': "Oe", 'Ä': "Ae",
		'ü': "ue", 'ö': "oe", 'ä': "ae",
		// Currency symbols
		'€': "eur", '£': "gbp", '¥': "yen", '$': "usd", '₹': "inr",
		// Common symbols
		'©': "c", '®': "r", '™': "tm", '°': "deg", '±': "plusminus",
		'×': "x", '÷': "div",
	}
}

// Generate creates a slug from the given input string.
func (s *Slugger) Generate(input string) string {
	if input == "" {
		return ""
	}

	var result strings.Builder
	lastWasSeparator := false

	for _, r := range input {
		// Check transliteration first
		if replacement, ok := s.translit[r]; ok {
			if replacement != "" {
				result.WriteString(replacement)
				lastWasSeparator = false
			}
			continue
		}

		// Handle alphanumeric characters
		if unicode.IsLetter(r) || unicode.IsDigit(r) {
			char := string(r)
			if s.config.Lowercase {
				char = strings.ToLower(char)
			}
			result.WriteString(char)
			lastWasSeparator = false
			continue
		}

		// Handle whitespace and separators
		if unicode.IsSpace(r) || r == '-' || r == '_' || r == '.' || r == '+' {
			if !lastWasSeparator && result.Len() > 0 {
				result.WriteString(s.config.Separator)
				lastWasSeparator = true
			}
			continue
		}

		// Skip other characters
	}

	output := result.String()

	// Trim separators
	if s.config.TrimSeparator {
		output = strings.Trim(output, s.config.Separator)
	}

	// Collapse multiple separators
	sepPattern := regexp.QuoteMeta(s.config.Separator)
	re := regexp.MustCompile(sepPattern + "+")
	output = re.ReplaceAllString(output, s.config.Separator)

	// Apply max length
	if s.config.MaxLength > 0 && len(output) > s.config.MaxLength {
		output = output[:s.config.MaxLength]
		// Trim to last separator to avoid cutting mid-word
		if idx := strings.LastIndex(output, s.config.Separator); idx > 0 {
			output = output[:idx]
		}
	}

	return output
}

// GenerateUnique creates a unique slug by appending a number if needed.
// The exists function should return true if the slug already exists.
func (s *Slugger) GenerateUnique(input string, exists func(string) bool) string {
	baseSlug := s.Generate(input)
	if baseSlug == "" {
		return ""
	}

	if !exists(baseSlug) {
		return baseSlug
	}

	counter := 1
	for {
		candidate := baseSlug + s.config.Separator + intToString(counter)
		if !exists(candidate) {
			return candidate
		}
		counter++
		if counter > 100000 { // Safety limit
			return candidate
		}
	}
}

// GenerateMultiple creates slugs from multiple input strings joined together.
func (s *Slugger) GenerateMultiple(inputs ...string) string {
	combined := strings.Join(inputs, " ")
	return s.Generate(combined)
}

// intToString converts an integer to string without importing strconv.
func intToString(n int) string {
	if n == 0 {
		return "0"
	}

	var negative bool
	if n < 0 {
		negative = true
		n = -n
	}

	var result []byte
	for n > 0 {
		result = append([]byte{byte('0' + n%10)}, result...)
		n /= 10
	}

	if negative {
		result = append([]byte{'-'}, result...)
	}

	return string(result)
}

// Package-level functions using default configuration

var defaultSlugger = New()

// Generate creates a slug from the given input string using default configuration.
func Generate(input string) string {
	return defaultSlugger.Generate(input)
}

// GenerateUnique creates a unique slug by appending a number if needed.
func GenerateUnique(input string, exists func(string) bool) string {
	return defaultSlugger.GenerateUnique(input, exists)
}

// GenerateMultiple creates slugs from multiple input strings joined together.
func GenerateMultiple(inputs ...string) string {
	return defaultSlugger.GenerateMultiple(inputs...)
}

// IsValidSlug checks if a string is a valid slug.
func IsValidSlug(slug string) bool {
	if slug == "" {
		return false
	}

	for _, r := range slug {
		if !unicode.IsLetter(r) && !unicode.IsDigit(r) && r != '-' && r != '_' {
			return false
		}
	}
	return true
}

// ParseSlug extracts words from a slug by splitting on the separator.
func ParseSlug(slug string, separator string) []string {
	if separator == "" {
		separator = "-"
	}
	return strings.Split(slug, separator)
}

// Truncate truncates a slug to the specified length, preserving word boundaries.
func Truncate(slug string, maxLength int, separator string) string {
	if len(slug) <= maxLength {
		return slug
	}

	if separator == "" {
		separator = "-"
	}

	// Try to break at a separator
	idx := strings.LastIndex(slug[:maxLength], separator)
	if idx > maxLength/2 {
		return slug[:idx]
	}
	return slug[:maxLength]
}