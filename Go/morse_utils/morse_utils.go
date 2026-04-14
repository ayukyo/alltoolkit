// Package morse_utils provides Morse code encoding and decoding utilities.
// Zero external dependencies - pure Go standard library implementation.
package morse_utils

import (
	"errors"
	"strings"
	"time"
)

// MorseCode represents a single Morse code element
type MorseCode string

// Morse code constants
const (
	Dot       MorseCode = "."
	Dash      MorseCode = "-"
	Space     MorseCode = " "
	CharSpace MorseCode = "   " // 3 units between characters
	WordSpace MorseCode = "       " // 7 units between words
)

// Errors
var (
	ErrInvalidCharacter = errors.New("invalid character for Morse encoding")
	ErrInvalidMorseCode = errors.New("invalid Morse code sequence")
	ErrEmptyInput        = errors.New("empty input")
)

// International Morse Code mapping
var letterToMorse = map[rune]string{
	// Letters
	'A': ".-",
	'B': "-...",
	'C': "-.-.",
	'D': "-..",
	'E': ".",
	'F': "..-.",
	'G': "--.",
	'H': "....",
	'I': "..",
	'J': ".---",
	'K': "-.-",
	'L': ".-..",
	'M': "--",
	'N': "-.",
	'O': "---",
	'P': ".--.",
	'Q': "--.-",
	'R': ".-.",
	'S': "...",
	'T': "-",
	'U': "..-",
	'V': "...-",
	'W': ".--",
	'X': "-..-",
	'Y': "-.--",
	'Z': "--..",
	// Numbers
	'0': "-----",
	'1': ".----",
	'2': "..---",
	'3': "...--",
	'4': "....-",
	'5': ".....",
	'6': "-....",
	'7': "--...",
	'8': "---..",
	'9': "----.",
	// Punctuation
	'.': ".-.-.-",
	',': "--..--",
	'?': "..--..",
	'\'': ".----.",
	'!': "-.-.--",
	'/': "-..-.",
	'(': "-.--.",
	')': "-.--.-",
	'&': ".-...",
	':': "---...",
	';': "-.-.-.",
	'=': "-...-",
	'+': ".-.-.",
	'-': "-....-",
	'_': "..--.-",
	'"': ".-..-.",
	'$': "...-..-",
	'@': ".--.-.",
	// Prosigns (special symbols)
	'×': "-..-.", // Same as /
}

// Reverse mapping for decoding
var morseToLetter map[string]rune

func init() {
	morseToLetter = make(map[string]rune)
	for char, code := range letterToMorse {
		morseToLetter[code] = char
	}
}

// TimingConfig holds timing configuration for Morse code audio/signals
type TimingConfig struct {
	DotDuration   time.Duration // Duration of a dot (1 unit)
	DashDuration  time.Duration // Duration of a dash (3 units)
	IntraCharGap  time.Duration // Gap within a character (1 unit)
	InterCharGap  time.Duration // Gap between characters (3 units)
	WordGap       time.Duration // Gap between words (7 units)
	Frequency     int           // Audio frequency in Hz
}

// DefaultTiming returns standard timing configuration
// Based on standard Morse code timing (dot = 1 unit)
func DefaultTiming() *TimingConfig {
	dotDuration := 100 * time.Millisecond
	return &TimingConfig{
		DotDuration:  dotDuration,
		DashDuration: 3 * dotDuration,
		IntraCharGap: dotDuration,
		InterCharGap: 3 * dotDuration,
		WordGap:      7 * dotDuration,
		Frequency:    700, // Standard Morse tone frequency
	}
}

// FastTiming returns a faster timing configuration for quick transmission
func FastTiming() *TimingConfig {
	dotDuration := 50 * time.Millisecond
	return &TimingConfig{
		DotDuration:  dotDuration,
		DashDuration: 3 * dotDuration,
		IntraCharGap: dotDuration,
		InterCharGap: 3 * dotDuration,
		WordGap:      7 * dotDuration,
		Frequency:    700,
	}
}

// SlowTiming returns a slower timing configuration for learning/beginners
func SlowTiming() *TimingConfig {
	dotDuration := 200 * time.Millisecond
	return &TimingConfig{
		DotDuration:  dotDuration,
		DashDuration: 3 * dotDuration,
		IntraCharGap: dotDuration,
		InterCharGap: 3 * dotDuration,
		WordGap:      7 * dotDuration,
		Frequency:    600,
	}
}

// CustomTiming creates a custom timing configuration
func CustomTiming(dotDuration time.Duration, frequency int) *TimingConfig {
	return &TimingConfig{
		DotDuration:  dotDuration,
		DashDuration: 3 * dotDuration,
		IntraCharGap: dotDuration,
		InterCharGap: 3 * dotDuration,
		WordGap:      7 * dotDuration,
		Frequency:    frequency,
	}
}

// Signal represents a signal element (on/off with duration)
type Signal struct {
	On       bool          // true = signal on, false = signal off
	Duration time.Duration // Duration of this signal
}

// Encode converts a string to Morse code
func Encode(text string) (string, error) {
	if text == "" {
		return "", nil
	}

	var result []string
	words := strings.Fields(text)

	for wordIdx, word := range words {
		if wordIdx > 0 {
			result = append(result, string(WordSpace))
		}

		for charIdx, char := range word {
			morse, ok := letterToMorse[char]
			if !ok {
				// Try lowercase
				morse, ok = letterToMorse[char-'a'+'A']
				if !ok {
					return "", ErrInvalidCharacter
				}
			}

			if charIdx > 0 {
				result = append(result, string(CharSpace))
			}
			result = append(result, morse)
		}
	}

	return strings.Join(result, ""), nil
}

// MustEncode converts a string to Morse code, panics on error
func MustEncode(text string) string {
	result, err := Encode(text)
	if err != nil {
		panic(err)
	}
	return result
}

// EncodeWithSeparator encodes text with a custom separator between characters
func EncodeWithSeparator(text, separator string) (string, error) {
	if text == "" {
		return "", nil
	}

	var result []string
	words := strings.Fields(text)

	for wordIdx, word := range words {
		if wordIdx > 0 {
			result = append(result, " / ") // Standard word separator
		}

		for charIdx, char := range word {
			morse, ok := letterToMorse[char]
			if !ok {
				morse, ok = letterToMorse[char-'a'+'A']
				if !ok {
					return "", ErrInvalidCharacter
				}
			}

			if charIdx > 0 {
				result = append(result, separator)
			}
			result = append(result, morse)
		}
	}

	return strings.Join(result, ""), nil
}

// Decode converts Morse code to a string
func Decode(morse string) (string, error) {
	if morse == "" {
		return "", nil
	}

	// Normalize: replace multiple spaces with single space for word detection
	// Then split by word boundaries (7 spaces) and character boundaries (3 spaces)

	var result strings.Builder
	words := strings.Split(morse, "       ") // 7 spaces = word boundary

	for wordIdx, word := range words {
		if wordIdx > 0 {
			result.WriteRune(' ')
		}

		// Handle 3-space character boundaries
		chars := strings.Split(strings.TrimSpace(word), "   ")
		for _, charMorse := range chars {
			charMorse = strings.TrimSpace(charMorse)
			if charMorse == "" {
				continue
			}

			// Decode each dot/dash sequence
			letter, ok := morseToLetter[charMorse]
			if !ok {
				return "", ErrInvalidMorseCode
			}
			result.WriteRune(letter)
		}
	}

	return result.String(), nil
}

// MustDecode converts Morse code to a string, panics on error
func MustDecode(morse string) string {
	result, err := Decode(morse)
	if err != nil {
		panic(err)
	}
	return result
}

// DecodeWithSeparator decodes Morse code with custom separator
func DecodeWithSeparator(morse, separator string) (string, error) {
	if morse == "" {
		return "", nil
	}

	var result strings.Builder
	words := strings.Split(morse, " / ")

	for wordIdx, word := range words {
		if wordIdx > 0 {
			result.WriteRune(' ')
		}

		chars := strings.Split(strings.TrimSpace(word), separator)
		for _, charMorse := range chars {
			charMorse = strings.TrimSpace(charMorse)
			if charMorse == "" {
				continue
			}

			letter, ok := morseToLetter[charMorse]
			if !ok {
				return "", ErrInvalidMorseCode
			}
			result.WriteRune(letter)
		}
	}

	return result.String(), nil
}

// ToSignals converts Morse code to a sequence of on/off signals
func ToSignals(morse string, config *TimingConfig) []Signal {
	if config == nil {
		config = DefaultTiming()
	}

	var signals []Signal

	for i, char := range morse {
		switch char {
		case '.':
			signals = append(signals, Signal{On: true, Duration: config.DotDuration})
			signals = append(signals, Signal{On: false, Duration: config.IntraCharGap})
		case '-':
			signals = append(signals, Signal{On: true, Duration: config.DashDuration})
			signals = append(signals, Signal{On: false, Duration: config.IntraCharGap})
		case ' ':
			// Check how many consecutive spaces
			spaceCount := 0
			for j := i; j < len(morse) && rune(morse[j]) == ' '; j++ {
				spaceCount++
			}
			// Remove last intra-char gap (it will be replaced by word/char gap)
			if len(signals) > 0 {
				signals = signals[:len(signals)-1]
			}
			if spaceCount >= 7 {
				signals = append(signals, Signal{On: false, Duration: config.WordGap})
			} else {
				signals = append(signals, Signal{On: false, Duration: config.InterCharGap})
			}
		}
	}

	// Remove trailing off signal if present
	if len(signals) > 0 && !signals[len(signals)-1].On {
		signals = signals[:len(signals)-1]
	}

	return signals
}

// GetTotalDuration calculates the total duration of a Morse code transmission
func GetTotalDuration(morse string, config *TimingConfig) time.Duration {
	if config == nil {
		config = DefaultTiming()
	}

	signals := ToSignals(morse, config)
	var total time.Duration
	for _, signal := range signals {
		total += signal.Duration
	}
	return total
}

// ToBinary converts Morse code to a binary string (1 = signal on, 0 = signal off)
func ToBinary(morse string) string {
	var result strings.Builder
	for _, char := range morse {
		switch char {
		case '.':
			result.WriteString("1")
		case '-':
			result.WriteString("111")
		case ' ':
			result.WriteString("0")
		}
	}
	return result.String()
}

// FromBinary converts a binary string back to Morse code
func FromBinary(binary string) string {
	var result strings.Builder
	i := 0
	for i < len(binary) {
		if binary[i] == '1' {
			// Count consecutive 1s
			count := 0
			for i < len(binary) && binary[i] == '1' {
				count++
				i++
			}
			if count == 1 {
				result.WriteRune('.')
			} else if count == 3 {
				result.WriteRune('-')
			}
		} else {
			// Count consecutive 0s
			count := 0
			for i < len(binary) && binary[i] == '0' {
				count++
				i++
			}
			if count >= 3 {
				result.WriteString("   ")
			} else if count > 0 {
				result.WriteRune(' ')
			}
		}
	}
	return result.String()
}

// IsValidMorse checks if a string is valid Morse code
func IsValidMorse(morse string) bool {
	for _, char := range morse {
		if char != '.' && char != '-' && char != ' ' {
			return false
		}
	}
	return true
}

// IsValidText checks if a string can be encoded to Morse code
func IsValidText(text string) bool {
	for _, char := range text {
		if char == ' ' {
			continue
		}
		_, ok := letterToMorse[char]
		if !ok {
			_, ok = letterToMorse[char-'a'+'A']
			if !ok {
				return false
			}
		}
	}
	return true
}

// GetMorseCode returns the Morse code for a single character
func GetMorseCode(char rune) (string, bool) {
	morse, ok := letterToMorse[char]
	if !ok {
		morse, ok = letterToMorse[char-'a'+'A']
	}
	return morse, ok
}

// GetCharacter returns the character for a Morse code sequence
func GetCharacter(morse string) (rune, bool) {
	char, ok := morseToLetter[morse]
	return char, ok
}

// GetAllCodes returns all supported characters and their Morse codes
func GetAllCodes() map[rune]string {
	result := make(map[rune]string)
	for k, v := range letterToMorse {
		result[k] = v
	}
	return result
}

// Prosign represents a Morse code prosign (special operator signal)
type Prosign struct {
	Name        string
	Code        string
	Description string
}

// Common prosigns
var Prosigns = []Prosign{
	{"AR", ".-.-.", "End of message"},
	{"BT", "-...-", "Break / pause"},
	{"SK", "...-.-", "End of work"},
	{"SN", "...-.", "Understood"},
	{"KN", "-.--.", "Invite a specific station to transmit"},
	{"AS", ".-...", "Wait"},
	{"K", "-.-", "Invitation to transmit"},
	{"VE", "...-", "Verified"},
	{"HH", "........", "Error"},
	{"SOS", "...---...", "Distress signal"},
	{"CQ", "-.-.--.-", "Calling any station"},
}

// EncodeProsign encodes a prosign by its name
func EncodeProsign(name string) (string, bool) {
	for _, prosign := range Prosigns {
		if prosign.Name == name {
			return prosign.Code, true
		}
	}
	return "", false
}

// WPMToDotDuration converts words per minute to dot duration
// Standard word "PARIS" = 50 units = 1 word
// WPM = 60 / (total units per word * dot duration in seconds)
func WPMToDotDuration(wpm int) time.Duration {
	// Standard PARIS word: 50 units
	// At WPM words per minute, each word takes 60/WPM seconds
	// 50 units = 60/WPM seconds
	// 1 unit = 60/(WPM*50) seconds = 1.2/WPM seconds
	return time.Duration(float64(1200)/float64(wpm)) * time.Millisecond
}

// DotDurationToWPM converts dot duration to words per minute
func DotDurationToWPM(dotDuration time.Duration) int {
	// WPM = 1200 / (dot duration in ms)
	return int(1200 / float64(dotDuration.Milliseconds()))
}

// String returns the string representation of Morse code
func (m MorseCode) String() string {
	return string(m)
}

// ToAudio converts Morse code to audio timing information
type AudioInfo struct {
	Frequency    int
	SampleRate   int
	Duration     time.Duration
	SignalCount  int
	DotCount     int
	DashCount    int
	SpaceCount   int
}

// Analyze analyzes Morse code and returns statistics
func Analyze(morse string) *AudioInfo {
	info := &AudioInfo{
		Frequency:  700,
		SampleRate: 44100,
	}

	for _, char := range morse {
		switch char {
		case '.':
			info.DotCount++
			info.SignalCount++
		case '-':
			info.DashCount++
			info.SignalCount++
		case ' ':
			info.SpaceCount++
		}
	}

	return info
}

// Normalize normalizes Morse code (standardizes spacing)
func Normalize(morse string) string {
	var result strings.Builder
	words := strings.Split(morse, "       ")

	for wordIdx, word := range words {
		if wordIdx > 0 {
			result.WriteString("       ")
		}

		// Split by 3 spaces
		chars := strings.Split(strings.TrimSpace(word), "   ")
		for charIdx, char := range chars {
			if charIdx > 0 {
				result.WriteString("   ")
			}
			// Remove any single spaces within character codes
			code := strings.ReplaceAll(char, " ", "")
			result.WriteString(code)
		}
	}

	return result.String()
}

// IsProsign checks if a Morse code sequence is a prosign
func IsProsign(code string) bool {
	for _, prosign := range Prosigns {
		if prosign.Code == code {
			return true
		}
	}
	return false
}

// GetProsignInfo returns information about a prosign
func GetProsignInfo(code string) (Prosign, bool) {
	for _, prosign := range Prosigns {
		if prosign.Code == code {
			return prosign, true
		}
	}
	return Prosign{}, false
}

// Reverse reverses the text (useful for encoding in reverse order)
func Reverse(text string) string {
	runes := []rune(text)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// CountCharacters counts the number of characters in Morse code
func CountCharacters(morse string) int {
	count := 0
	words := strings.Split(morse, "       ")
	for _, word := range words {
		chars := strings.Split(strings.TrimSpace(word), "   ")
		count += len(chars)
	}
	return count
}

// CountWords counts the number of words in Morse code
func CountWords(morse string) int {
	if morse == "" {
		return 0
	}
	return len(strings.Split(morse, "       "))
}

// Transpose returns a transposed representation (dots and dashes swapped)
func Transpose(morse string) string {
	var result strings.Builder
	for _, char := range morse {
		switch char {
		case '.':
			result.WriteRune('-')
		case '-':
			result.WriteRune('.')
		default:
			result.WriteRune(char)
		}
	}
	return result.String()
}