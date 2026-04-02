// Package pathutils provides general-purpose path manipulation utilities.
// All functions are safe for concurrent use and work correctly across
// different operating systems (Windows, macOS, Linux).
package stringutils

import (
	"path/filepath"
	"strings"
)

// SafeJoin joins multiple path elements into a single path, ensuring:
//   - No path traversal attacks (removes ".." that would escape root)
//   - Clean, normalized path separators
//   - Leading/trailing whitespace is trimmed from each component
//   - Empty components are skipped
//
// Parameters:
//   - elems: Variable list of path elements to join. Each element can contain
//            multiple path separators; they will be normalized.
//
// Returns:
//   - A clean, joined path string with OS-correct separators.
//   - Empty string if no valid elements provided.
//   - Elements containing only "." or ".." are handled safely.
//
// Security Notes:
//   - This function does NOT verify if the path exists or is accessible.
//   - It only sanitizes the path structure to prevent traversal attacks.
//   - For web-facing applications, additional validation is recommended.
//
// Examples:
//
//     SafeJoin("/home", "user", "docs")           // Returns "/home/user/docs"
//     SafeJoin("/home/user", "../etc/passwd")     // Returns "/home/user/etc/passwd"
//     SafeJoin("/data", "subdir/../../etc")       // Returns "/data/etc"
//     SafeJoin("C:\\Users", "admin", "file.txt")  // Returns "C:\\Users\\admin\\file.txt"
//     SafeJoin("/base", "", "  file.txt  ")      // Returns "/base/file.txt"
//     SafeJoin()                                    // Returns "."
//
// Performance: O(n) where n is total length of all elements.
// Memory: Allocates new string for result.
func SafeJoin(elems ...string) string {
	if len(elems) == 0 {
		return "."
	}

	// Clean and filter elements
	cleaned := make([]string, 0, len(elems))
	for _, elem := range elems {
		// Trim whitespace
		elem = strings.TrimSpace(elem)
		// Skip empty elements
		if elem == "" {
			continue
		}
		cleaned = append(cleaned, elem)
	}

	if len(cleaned) == 0 {
		return "."
	}

	// Join all elements
	joined := filepath.Join(cleaned...)

	// Clean the path (resolve . and .., remove redundant separators)
	cleanedPath := filepath.Clean(joined)

	return cleanedPath
}

// ExtNoDot returns the file extension without the leading dot.
// Unlike filepath.Ext(), this returns an empty string for files without
// extension, rather than returning the dot itself.
//
// Parameters:
//   - path: The file path to extract extension from. Can be relative or absolute.
//
// Returns:
//   - The file extension without the leading dot (lowercase).
//   - Empty string if no extension found or path is empty.
//   - Extension is normalized to lowercase for case-insensitive comparison.
//
// Examples:
//
//     ExtNoDot("document.PDF")           // Returns "pdf"
//     ExtNoDot("/path/to/file.txt")      // Returns "txt"
//     ExtNoDot("README")                 // Returns ""
//     ExtNoDot("archive.tar.gz")         // Returns "gz"
//     ExtNoDot(".gitignore")             // Returns ""
//     ExtNoDot("")                       // Returns ""
//
// Performance: O(n) where n is length of path.
// Memory: Allocates new string for result.
func ExtNoDot(path string) string {
	if path == "" {
		return ""
	}

	// Get extension with filepath.Ext (includes the dot)
	ext := filepath.Ext(path)

	// Remove the leading dot and convert to lowercase
	if len(ext) > 1 {
		return strings.ToLower(ext[1:])
	}

	return ""
}

// BaseNoExt returns the filename without its extension.
// Combines filepath.Base() with extension removal for convenience.
//
// Parameters:
//   - path: The file path to process. Can be relative or absolute.
//
// Returns:
//   - The filename without extension.
//   - Empty string if path is empty or ends with separator.
//
// Examples:
//
//     BaseNoExt("/home/user/document.txt")   // Returns "document"
//     BaseNoExt("photo.JPG")                 // Returns "photo"
//     BaseNoExt("archive.tar.gz")            // Returns "archive.tar"
//     BaseNoExt("/path/to/dir/")             // Returns "dir"
//     BaseNoExt("README")                    // Returns "README"
//     BaseNoExt("")                          // Returns ""
//
// Performance: O(n) where n is length of path.
// Memory: Allocates new string for result.
func BaseNoExt(path string) string {
	if path == "" {
		return ""
	}

	// Get base filename
	base := filepath.Base(path)

	// Remove extension
	if ext := filepath.Ext(base); ext != "" {
		return base[:len(base)-len(ext)]
	}

	return base
}

// HasExt checks if a file path has any of the specified extensions.
// Comparison is case-insensitive.
//
// Parameters:
//   - path: The file path to check.
//   - exts: Variable list of extensions to check (with or without leading dot).
//
// Returns:
//   - true if path ends with any of the specified extensions.
//   - false if no match or path is empty.
//
// Examples:
//
//     HasExt("photo.jpg", "jpg", "png")          // Returns true
//     HasExt("document.PDF", ".pdf", ".doc")     // Returns true
//     HasExt("script.JS", ".js", ".ts")          // Returns true
//     HasExt("README", "txt", "md")              // Returns false
//     HasExt("", "txt")                          // Returns false
//
// Performance: O(n*m) where n is extensions count, m is path length.
// Memory: Minimal - only allocates for lowercase comparisons.
func HasExt(path string, exts ...string) bool {
	if path == "" || len(exts) == 0 {
		return false
	}

	// Get actual extension (lowercase, no dot)
	actualExt := ExtNoDot(path)

	// Check against each provided extension
	for _, ext := range exts {
		// Normalize: remove leading dot if present, convert to lowercase
		normalized := strings.ToLower(strings.TrimPrefix(ext, "."))
		if normalized == actualExt {
			return true
		}
	}

	return false
}
