// Package main provides examples for morse_utils usage
package main

import (
	"fmt"
	"time"

	morse "github.com/ayukyo/alltoolkit/go/morse_utils"
)

func main() {
	fmt.Println("=== Morse Utils Examples ===\n")

	// 1. Basic Encoding
	exampleBasicEncoding()

	// 2. Basic Decoding
	exampleBasicDecoding()

	// 3. Round Trip
	exampleRoundTrip()

	// 4. Numbers and Punctuation
	exampleNumbersAndPunctuation()

	// 5. Timing Configuration
	exampleTimingConfig()

	// 6. Signal Conversion
	exampleSignalConversion()

	// 7. Binary Conversion
	exampleBinaryConversion()

	// 8. Prosigns
	exampleProsigns()

	// 9. WPM Conversion
	exampleWPMConversion()

	// 10. Statistics and Analysis
	exampleStatistics()

	// 11. Custom Separator
	exampleCustomSeparator()

	// 12. Validation
	exampleValidation()

	// 13. Single Character Lookup
	exampleLookup()

	// 14. Long Text
	exampleLongText()

	// 15. Transpose
	exampleTranspose()

	fmt.Println("\n=== Examples Complete ===")
}

// 1. Basic Encoding
func exampleBasicEncoding() {
	fmt.Println("1. Basic Encoding")
	fmt.Println("-----------------")

	// Encode simple text
	encoded, err := morse.Encode("SOS")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("SOS encoded:     %s\n", encoded)

	// Encode with lowercase (automatically converted)
	encoded, err = morse.Encode("hello")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("hello encoded:   %s\n", encoded)

	// Encode with spaces (word boundary)
	encoded, err = morse.Encode("HELLO WORLD")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("HELLO WORLD:     %s\n", encoded)

	// Quick encoding (panics on error)
	quick := morse.MustEncode("ABC")
	fmt.Printf("Quick encode:    %s\n", quick)

	fmt.Println()
}

// 2. Basic Decoding
func exampleBasicDecoding() {
	fmt.Println("2. Basic Decoding")
	fmt.Println("-----------------")

	// Decode Morse code
	decoded, err := morse.Decode("...   ---   ...")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("... --- ... decoded: %s\n", decoded)

	// Decode with word boundary
	decoded, err = morse.Decode("....   .   .-..   .-..   ---       .--   ---   .-.   .-..   -..")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("HELLO WORLD decoded: %s\n", decoded)

	// Quick decoding
	quick := morse.MustDecode(".-")
	fmt.Printf("Quick decode .-:     %s\n", quick)

	fmt.Println()
}

// 3. Round Trip
func exampleRoundTrip() {
	fmt.Println("3. Round Trip")
	fmt.Println("-------------")

	text := "MORSE CODE"
	encoded, _ := morse.Encode(text)
	decoded, _ := morse.Decode(encoded)

	fmt.Printf("Original:  %s\n", text)
	fmt.Printf("Encoded:   %s\n", encoded)
	fmt.Printf("Decoded:   %s\n", decoded)
	fmt.Printf("Match:     %v\n", text == decoded)

	fmt.Println()
}

// 4. Numbers and Punctuation
func exampleNumbersAndPunctuation() {
	fmt.Println("4. Numbers and Punctuation")
	fmt.Println("--------------------------")

	// Numbers
	numbers := "0123456789"
	encoded, _ := morse.Encode(numbers)
	fmt.Printf("%s encoded: %s\n", numbers, encoded)

	// Punctuation
	punctuation := "Hello, World!"
	encoded, _ = morse.Encode(punctuation)
	fmt.Printf("%s encoded: %s\n", punctuation, encoded)

	// Special characters
	special := "Email: test@example.com"
	encoded, _ = morse.Encode(special)
	fmt.Printf("%s encoded: %s\n", special, encoded)

	fmt.Println()
}

// 5. Timing Configuration
func exampleTimingConfig() {
	fmt.Println("5. Timing Configuration")
	fmt.Println("-----------------------")

	// Default timing (100ms dot)
	defaultTiming := morse.DefaultTiming()
	fmt.Printf("Default timing: dot=%v, dash=%v, frequency=%d Hz\n",
		defaultTiming.DotDuration, defaultTiming.DashDuration, defaultTiming.Frequency)

	// Fast timing (50ms dot)
	fastTiming := morse.FastTiming()
	fmt.Printf("Fast timing: dot=%v, dash=%v, frequency=%d Hz\n",
		fastTiming.DotDuration, fastTiming.DashDuration, fastTiming.Frequency)

	// Slow timing (200ms dot)
	slowTiming := morse.SlowTiming()
	fmt.Printf("Slow timing: dot=%v, dash=%v, frequency=%d Hz\n",
		slowTiming.DotDuration, slowTiming.DashDuration, slowTiming.Frequency)

	// Custom timing
	customTiming := morse.CustomTiming(150*time.Millisecond, 650)
	fmt.Printf("Custom timing: dot=%v, dash=%v, frequency=%d Hz\n",
		customTiming.DotDuration, customTiming.DashDuration, customTiming.Frequency)

	fmt.Println()
}

// 6. Signal Conversion
func exampleSignalConversion() {
	fmt.Println("6. Signal Conversion")
	fmt.Println("--------------------")

	morseCode := ".-" // A
	config := morse.DefaultTiming()

	signals := morse.ToSignals(morseCode, config)

	fmt.Printf("Morse: %s\n", morseCode)
	fmt.Printf("Signals (%d total):\n", len(signals))
	for i, signal := range signals {
		state := "OFF"
		if signal.On {
			state = "ON"
		}
		fmt.Printf("  Signal %d: %s for %v\n", i+1, state, signal.Duration)
	}

	// Calculate total duration
	total := morse.GetTotalDuration(morseCode, config)
	fmt.Printf("Total duration: %v\n", total)

	// More complex example
	morseCode = "...   ---   ..." // SOS
	total = morse.GetTotalDuration(morseCode, config)
	fmt.Printf("SOS duration: %v\n", total)

	fmt.Println()
}

// 7. Binary Conversion
func exampleBinaryConversion() {
	fmt.Println("7. Binary Conversion")
	fmt.Println("--------------------")

	// Convert Morse to binary
	morseCode := ".-.-."
	binary := morse.ToBinary(morseCode)
	fmt.Printf("Morse: %s -> Binary: %s\n", morseCode, binary)

	// Convert binary back to Morse
	morseCode = ".-"
	binary = morse.ToBinary(morseCode)
	back := morse.FromBinary(binary)
	fmt.Printf("Binary: %s -> Morse: %s\n", binary, back)

	// More examples
	examples := []string{"...", "---", ".-.-.-"}
	for _, m := range examples {
		b := morse.ToBinary(m)
		fmt.Printf("Morse: %s -> Binary: %s\n", m, b)
	}

	fmt.Println()
}

// 8. Prosigns
func exampleProsigns() {
	fmt.Println("8. Prosigns")
	fmt.Println("-----------")

	// List all prosigns
	fmt.Println("Available prosigns:")
	for _, prosign := range morse.Prosigns {
		fmt.Printf("  %s: %s - %s\n", prosign.Name, prosign.Code, prosign.Description)
	}

	// Encode specific prosign
	code, found := morse.EncodeProsign("AR")
	if found {
		fmt.Printf("\nAR (End of message): %s\n", code)
	}

	// SOS as prosign
	code, found = morse.EncodeProsign("SOS")
	if found {
		fmt.Printf("SOS (Distress): %s\n", code)
	}

	// Check if Morse code is a prosign
	isProsign := morse.IsProsign(".-.-.")
	fmt.Printf(".-.-. is prosign: %v\n", isProsign)

	// Get prosign info
	info, found := morse.GetProsignInfo(".-.-.")
	if found {
		fmt.Printf("Prosign info: %s - %s\n", info.Name, info.Description)
	}

	fmt.Println()
}

// 9. WPM Conversion
func exampleWPMConversion() {
	fmt.Println("9. WPM Conversion")
	fmt.Println("-----------------")

	// Convert WPM to dot duration
	wpmValues := []int{5, 10, 15, 20, 25, 30}
	for _, wpm := range wpmValues {
		dotDuration := morse.WPMToDotDuration(wpm)
		fmt.Printf("%d WPM -> dot duration: %v\n", wpm, dotDuration)
	}

	// Convert duration back to WPM
	dotDuration := 60 * time.Millisecond
	wpm := morse.DotDurationToWPM(dotDuration)
	fmt.Printf("\n%v dot duration -> %d WPM\n", dotDuration, wpm)

	// Create timing from WPM
	wpm := 15
	timing := morse.CustomTiming(morse.WPMToDotDuration(wpm), 700)
	fmt.Printf("\nTiming at %d WPM: dot=%v, dash=%v\n", wpm, timing.DotDuration, timing.DashDuration)

	fmt.Println()
}

// 10. Statistics and Analysis
func exampleStatistics() {
	fmt.Println("10. Statistics and Analysis")
	fmt.Println("---------------------------")

	morseCode := "...   ---   ..." // SOS

	// Analyze
	info := morse.Analyze(morseCode)
	fmt.Printf("Morse: %s\n", morseCode)
	fmt.Printf("Dot count: %d\n", info.DotCount)
	fmt.Printf("Dash count: %d\n", info.DashCount)
	fmt.Printf("Signal count: %d\n", info.SignalCount)
	fmt.Printf("Space count: %d\n", info.SpaceCount)

	// Count characters
	charCount := morse.CountCharacters(morseCode)
	fmt.Printf("Character count: %d\n", charCount)

	// Count words
	wordCount := morse.CountWords(morseCode)
	fmt.Printf("Word count: %d\n", wordCount)

	// Long text statistics
	encoded, _ := morse.Encode("HELLO WORLD")
	info = morse.Analyze(encoded)
	fmt.Printf("\nHELLO WORLD stats: dots=%d, dashes=%d, spaces=%d\n",
		info.DotCount, info.DashCount, info.SpaceCount)

	fmt.Println()
}

// 11. Custom Separator
func exampleCustomSeparator() {
	fmt.Println("11. Custom Separator")
	fmt.Println("--------------------")

	// Encode with slash separator
	encoded, _ := morse.EncodeWithSeparator("SOS", "/")
	fmt.Printf("SOS with / separator: %s\n", encoded)

	// Encode with pipe separator
	encoded, _ = morse.EncodeWithSeparator("ABC", "|")
	fmt.Printf("ABC with | separator: %s\n", encoded)

	// Decode with custom separator
	decoded, _ := morse.DecodeWithSeparator(".../---/...", "/")
	fmt.Printf("Decoded with / separator: %s\n", decoded)

	// Decode with pipe separator
	decoded, _ = morse.DecodeWithSeparator(".-|-...|-.-.", "|")
	fmt.Printf("Decoded with | separator: %s\n", decoded)

	fmt.Println()
}

// 12. Validation
func exampleValidation() {
	fmt.Println("12. Validation")
	fmt.Println("--------------")

	// Validate Morse code
	validMorse := []string{".-", "...   ---   ...", "---", ""}
	for _, m := range validMorse {
		fmt.Printf("IsValidMorse(%s): %v\n", m, morse.IsValidMorse(m))
	}

	invalidMorse := []string{".-x", "ABC", "..?"}
	for _, m := range invalidMorse {
		fmt.Printf("IsValidMorse(%s): %v\n", m, morse.IsValidMorse(m))
	}

	// Validate text
	validText := []string{"ABC", "Hello World", "123", "Test!"}
	fmt.Println("\nValid text for encoding:")
	for _, t := range validText {
		fmt.Printf("IsValidText(%s): %v\n", t, morse.IsValidText(t))
	}

	invalidText := []string{"你好", "テスト", "Test®"}
	for _, t := range invalidText {
		fmt.Printf("IsValidText(%s): %v\n", t, morse.IsValidText(t))
	}

	fmt.Println()
}

// 13. Single Character Lookup
func exampleLookup() {
	fmt.Println("13. Single Character Lookup")
	fmt.Println("---------------------------")

	// Get Morse code for a character
	chars := []rune{'A', 'S', 'O', '0', '.', '?'}
	for _, char := range chars {
		code, found := morse.GetMorseCode(char)
		fmt.Printf("GetMorseCode(%c): %s (found: %v)\n", char, code, found)
	}

	// Get character from Morse code
	codes := []string{".-", "...", "---", "-----", ".-.-.-"}
	for _, code := range codes {
		char, found := morse.GetCharacter(code)
		fmt.Printf("GetCharacter(%s): %c (found: %v)\n", code, char, found)
	}

	// Get all codes
	allCodes := morse.GetAllCodes()
	fmt.Printf("\nTotal supported characters: %d\n", len(allCodes))
	fmt.Println("Sample codes:")
	sampleChars := []rune{'A', 'B', 'C', '1', '2', '3', '.', ',', '!'}
	for _, char := range sampleChars {
		fmt.Printf("  %c: %s\n", char, allCodes[char])
	}

	fmt.Println()
}

// 14. Long Text
func exampleLongText() {
	fmt.Println("14. Long Text")
	fmt.Println("------------")

	// The famous pangram
	text := "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
	encoded, _ := morse.Encode(text)
	decoded, _ := morse.Decode(encoded)

	fmt.Printf("Original: %s\n", text)
	fmt.Printf("Encoded (first 50 chars): %s...\n", encoded[:50])
	fmt.Printf("Decoded: %s\n", decoded)
	fmt.Printf("Match: %v\n", text == decoded)

	// Statistics
	info := morse.Analyze(encoded)
	fmt.Printf("Stats: dots=%d, dashes=%d, signals=%d\n",
		info.DotCount, info.DashCount, info.SignalCount)

	// Duration at 20 WPM
	timing := morse.CustomTiming(morse.WPMToDotDuration(20), 700)
	duration := morse.GetTotalDuration(encoded, timing)
	fmt.Printf("Transmission time at 20 WPM: %v\n", duration)

	fmt.Println()
}

// 15. Transpose
func exampleTranspose() {
	fmt.Println("15. Transpose (Swap Dots/Dashes)")
	fmt.Println("--------------------------------")

	// Simple examples
	examples := []string{".", "-", ".-", "...", "---"}
	for _, m := range examples {
		transposed := morse.Transpose(m)
		fmt.Printf("Transpose(%s): %s\n", m, transposed)
	}

	// Transpose and encode comparison
	original := "SOS"
	encoded, _ := morse.Encode(original)
	transposed := morse.Transpose(encoded)
	fmt.Printf("\nOriginal %s: %s\n", original, encoded)
	fmt.Printf("Transposed: %s\n", transposed)

	// Decode transposed (will give different characters)
	decoded, _ := morse.Decode(transposed)
	fmt.Printf("Decoded transposed: %s\n", decoded)

	fmt.Println()
}