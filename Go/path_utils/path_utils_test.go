package stringutils

import (
	"path/filepath"
	"testing"
)

func TestSafeJoin(t *testing.T) {
	tests := []struct {
		name     string
		elems    []string
		expected string
	}{
		{
			name:     "basic join",
			elems:    []string{"/home", "user", "docs"},
			expected: filepath.Join("/home", "user", "docs"),
		},
		{
			name:     "handles parent traversal",
			elems:    []string{"/home/user", "../etc/passwd"},
			expected: filepath.Join("/home", "etc", "passwd"),
		},
		{
			name:     "handles multiple parent traversal",
			elems:    []string{"/data", "subdir/../../etc"},
			expected: filepath.Join("/data", "etc"),
		},
		{
			name:     "skips empty elements",
			elems:    []string{"/base", "", "file.txt"},
			expected: filepath.Join("/base", "file.txt"),
		},
		{
			name:     "trims whitespace",
			elems:    []string{"/base", "  subdir  ", "file.txt"},
			expected: filepath.Join("/base", "subdir", "file.txt"),
		},
		{
			name:     "no elements returns dot",
			elems:    []string{},
			expected: ".",
		},
		{
			name:     "only empty elements returns dot",
			elems:    []string{"", "  ", ""},
			expected: ".",
		},
		{
			name:     "handles current directory",
			elems:    []string{".", "file.txt"},
			expected: "file.txt",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := SafeJoin(tt.elems...)
			if result != tt.expected {
				t.Errorf("SafeJoin(%v) = %q, want %q", tt.elems, result, tt.expected)
			}
		})
	}
}

func TestExtNoDot(t *testing.T) {
	tests := []struct {
		path     string
		expected string
	}{
		{"document.PDF", "pdf"},
		{"/path/to/file.txt", "txt"},
		{"README", ""},
		{"archive.tar.gz", "gz"},
		{".gitignore", ""},
		{"", ""},
		{"file.JPG", "jpg"},
		{"file.PNG", "png"},
		{"/home/user/data.CSV", "csv"},
	}

	for _, tt := range tests {
		t.Run(tt.path, func(t *testing.T) {
			result := ExtNoDot(tt.path)
			if result != tt.expected {
				t.Errorf("ExtNoDot(%q) = %q, want %q", tt.path, result, tt.expected)
			}
		})
	}
}

func TestBaseNoExt(t *testing.T) {
	tests := []struct {
		path     string
		expected string
	}{
		{"/home/user/document.txt", "document"},
		{"photo.JPG", "photo"},
		{"archive.tar.gz", "archive.tar"},
		{"README", "README"},
		{"", ""},
		{"/path/to/dir/", "dir"},
		{"file", "file"},
	}

	for _, tt := range tests {
		t.Run(tt.path, func(t *testing.T) {
			result := BaseNoExt(tt.path)
			if result != tt.expected {
				t.Errorf("BaseNoExt(%q) = %q, want %q", tt.path, result, tt.expected)
			}
		})
	}
}

func TestHasExt(t *testing.T) {
	tests := []struct {
		path     string
		exts      []string
		expected bool
	}{
		{"photo.jpg", []string{"jpg", "png"}, true},
		{"photo.JPG", []string{"jpg", "png"}, true},
		{"document.PDF", []string{".pdf", ".doc"}, true},
		{"script.JS", []string{".js", ".ts"}, true},
		{"README", []string{"txt", "md"}, false},
		{"", []string{"txt"}, false},
		{"file.txt", []string{}, false},
		{"image.PNG", []string{"png"}, true},
		{"data.json", []string{"json", "yaml", "yml"}, true},
	}

	for _, tt := range tests {
		t.Run(tt.path, func(t *testing.T) {
			result := HasExt(tt.path, tt.exts...)
			if result != tt.expected {
				t.Errorf("HasExt(%q, %v) = %v, want %v", tt.path, tt.exts, result, tt.expected)
			}
		})
	}
}

// Benchmark tests

func BenchmarkSafeJoin(b *testing.B) {
	elems := []string{"/home", "user", "documents", "projects", "myapp", "config", "settings.json"}
	for i := 0; i < b.N; i++ {
		SafeJoin(elems...)
	}
}

func BenchmarkExtNoDot(b *testing.B) {
	path := "/home/user/documents/archive.tar.gz"
	for i := 0; i < b.N; i++ {
		ExtNoDot(path)
	}
}

func BenchmarkBaseNoExt(b *testing.B) {
	path := "/home/user/documents/archive.tar.gz"
	for i := 0; i < b.N; i++ {
		BaseNoExt(path)
	}
}

func BenchmarkHasExt(b *testing.B) {
	path := "document.PDF"
	for i := 0; i < b.N; i++ {
		HasExt(path, ".pdf", ".doc", ".docx")
	}
}
