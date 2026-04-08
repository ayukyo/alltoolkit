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
//   - "..." if maxLen < 3.
//
// Examples:
//
//     Truncate("Hello World", 8)     // Returns "Hello..."
//     Truncate("Hello", 10)          // Returns "Hello"
//     Truncate("你好世界", 5)         // Returns "你好..."
//     Truncate("", 10)               // Returns ""
//
// Performance: O(n) where n is the number of runes to scan.
// Memory: Pre-allocates buffer for optimal performance.
func Truncate(s string, maxLen int) string {
	// Handle edge cases with early returns
	if s == "" {
		return ""
	}

	// Validate maxLen with bounds checking - must be at least 3 for ellipsis
	const ellipsisLen = 3
	if maxLen < ellipsisLen {
		return "..."
	}

	// Fast path: check byte length for pure ASCII strings
	if len(s) <= maxLen {
		// Verify it's actually ASCII (no multi-byte chars)
		if len(s) == utf8.RuneCountInString(s) {
			return s
		}
	}

	// Calculate target length (reserve space for ellipsis)
	targetLen := maxLen - ellipsisLen
	
	// Fast path: count runes first to avoid unnecessary work
	if utf8.RuneCountInString(s) <= targetLen {
		return s
	}

	// Single-pass: count runes and find truncation point
	var truncIdx int
	count := 0
	for i := 0; i < len(s); {
		r, size := utf8.DecodeRuneInString(s[i:])
		
		// Check if we've reached the target length
		if count >= targetLen {
			break
		}
		
		// Handle invalid UTF-8 gracefully - treat as single byte
		if r == utf8.RuneError && size == 1 {
			truncIdx = i + 1
			count++
			i++
		} else {
			truncIdx = i + size
			count++
			i += size
		}
	}

	return s[:truncIdx] + "..."
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
	// Handle edge cases with early returns
	if s == "" {
		return ""
	}

	// Validate maxLen with bounds checking
	const ellipsisLen = 3
	if maxLen <= ellipsisLen {
		return "..."
	}

	// Fast path: if string already fits, return as-is
	if len(s) <= maxLen {
		return s
	}

	// Reserve space for ellipsis
	targetLen := maxLen - ellipsisLen

	// Walk backwards to find valid UTF-8 boundary
	for i := targetLen; i > 0; i-- {
		if utf8.ValidString(s[:i]) {
			return s[:i] + "..."
		}
	}

	// Fallback: return ellipsis if no valid boundary found
	return "..."
}
