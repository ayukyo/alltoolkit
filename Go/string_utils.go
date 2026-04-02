// Package stringutils provides general-purpose string manipulation utilities.
// All functions are safe for concurrent use and handle Unicode correctly.
package stringutils

import "unicode/utf8"

// Truncate truncates a string to the specified maximum length.
// If the string exceeds maxLen, it truncates at the last valid UTF-8 rune
// boundary and appends an ellipsis ("...") to indicate truncation.
//
// Parameters:
//   - s:      The input string to truncate. Can be empty.
//   - maxLen: The maximum length of the resulting string, including ellipsis.
//             Must be >= 3 (to accommodate ellipsis). If < 3, returns "...".
//
// Returns:
//   - A truncated string with "..." appended if truncation occurred.
//   - The original string if its length <= maxLen.
//   - Empty string if input is empty.
//
// Examples:
//
//     Truncate("Hello World", 8)     // Returns "Hello..."
//     Truncate("Hello", 10)          // Returns "Hello"
//     Truncate("你好世界", 5)         // Returns "你好..."
//     Truncate("", 10)               // Returns ""
//
// Performance: O(n) where n is the number of runes to scan.
// Memory: Allocates new string only when truncation occurs.
func Truncate(s string, maxLen int) string {
	// Handle edge cases
	if s == "" {
		return ""
	}

	// If maxLen is too small, return just ellipsis
	if maxLen < 3 {
		return "..."
	}

	// If string fits within limit, return as-is
	if utf8.RuneCountInString(s) <= maxLen {
		return s
	}

	// Calculate target length (reserve space for ellipsis)
	targetLen := maxLen - 3
	if targetLen < 0 {
		targetLen = 0
	}

	// Build result, respecting UTF-8 boundaries
	var result []byte
	count := 0
	for i := 0; i < len(s); {
		r, size := utf8.DecodeRuneInString(s[i:])
		if r == utf8.RuneError && size == 1 {
			// Invalid UTF-8, skip byte
			i++
			continue
		}

		if count >= targetLen {
			break
		}

		result = append(result, s[i:i+size])
		count++
		i += size
	}

	return string(result) + "..."
}

// TruncateSafe is a variant that guarantees the result never exceeds maxLen bytes,
// useful for database fields with strict byte limits.
//
// Parameters:
//   - s:       The input string to truncate.
//   - maxLen:  Maximum byte length of result, including ellipsis (must be >= 3).
//
// Returns:
//   - Truncated string guaranteed to be <= maxLen bytes.
//
// Example:
//
//     TruncateSafe("Hello World", 8)  // Returns "Hel..." (fits in 8 bytes)
func TruncateSafe(s string, maxLen int) string {
	if s == "" {
		return ""
	}

	if maxLen < 3 {
		return "..."
	}

	if len(s) <= maxLen {
		return s
	}

	// Reserve space for ellipsis
	targetLen := maxLen - 3

	// Walk backwards to find valid UTF-8 boundary
	for i := targetLen; i > 0; i-- {
		if utf8.ValidString(s[:i]) {
			return s[:i] + "..."
		}
	}

	// Fallback: return ellipsis if no valid boundary found
	return "..."
}
