// Example: Path Utilities Demo
//
// This example demonstrates the usage of path utility functions.
// Run with: go run example/path_example.go
//
// Expected output:
//   SafeJoin Examples:
//   Joined: /home/user/docs
//   Cleaned: /home/user/etc/passwd
//   With spaces: /data/files/report.txt
//
//   Extension Examples:
//   ExtNoDot("document.PDF") = "pdf"
//   ExtNoDot("/path/to/file.txt") = "txt"
//   ExtNoDot("README") = ""
//   ExtNoDot("archive.tar.gz") = "gz"
//
//   Filename Examples:
//   BaseNoExt("/home/user/document.txt") = "document"
//   BaseNoExt("photo.JPG") = "photo"
//   BaseNoExt("archive.tar.gz") = "archive.tar"
//
//   Extension Check Examples:
//   HasExt("photo.jpg", "jpg", "png") = true
//   HasExt("script.JS", ".js", ".ts") = true
//   HasExt("README", "txt", "md") = false

package main

import (
	"fmt"
	"path/filepath"

	stringutils "alltoolkit/stringutils"
)

func main() {
	fmt.Println("=== Path Utilities Demo ===\n")

	// SafeJoin Examples
	fmt.Println("SafeJoin Examples:")
	fmt.Printf("Join paths: %s\n", stringutils.SafeJoin("/home", "user", "docs"))
	fmt.Printf("Handle traversal: %s\n", stringutils.SafeJoin("/home/user", "../etc/passwd"))
	fmt.Printf("Trim spaces: %s\n", stringutils.SafeJoin("/data", "  files  ", "report.txt"))
	fmt.Printf("Skip empty: %s\n", stringutils.SafeJoin("/base", "", "config.json"))
	fmt.Printf("No args: %s\n\n", stringutils.SafeJoin())

	// ExtNoDot Examples
	fmt.Println("ExtNoDot Examples:")
	fmt.Printf("ExtNoDot(\"document.PDF\") = %q\n", stringutils.ExtNoDot("document.PDF"))
	fmt.Printf("ExtNoDot(\"/path/to/file.txt\") = %q\n", stringutils.ExtNoDot("/path/to/file.txt"))
	fmt.Printf("ExtNoDot(\"README\") = %q\n", stringutils.ExtNoDot("README"))
	fmt.Printf("ExtNoDot(\"archive.tar.gz\") = %q\n", stringutils.ExtNoDot("archive.tar.gz"))
	fmt.Printf("ExtNoDot(\".gitignore\") = %q\n\n", stringutils.ExtNoDot(".gitignore"))

	// BaseNoExt Examples
	fmt.Println("BaseNoExt Examples:")
	fmt.Printf("BaseNoExt(\"/home/user/document.txt\") = %q\n", stringutils.BaseNoExt("/home/user/document.txt"))
	fmt.Printf("BaseNoExt(\"photo.JPG\") = %q\n", stringutils.BaseNoExt("photo.JPG"))
	fmt.Printf("BaseNoExt(\"archive.tar.gz\") = %q\n", stringutils.BaseNoExt("archive.tar.gz"))
	fmt.Printf("BaseNoExt(\"README\") = %q\n\n", stringutils.BaseNoExt("README"))

	// HasExt Examples
	fmt.Println("HasExt Examples:")
	fmt.Printf("HasExt(\"photo.jpg\", \"jpg\", \"png\") = %v\n", stringutils.HasExt("photo.jpg", "jpg", "png"))
	fmt.Printf("HasExt(\"script.JS\", \".js\", \".ts\") = %v\n", stringutils.HasExt("script.JS", ".js", ".ts"))
	fmt.Printf("HasExt(\"document.PDF\", \".pdf\", \".doc\") = %v\n", stringutils.HasExt("document.PDF", ".pdf", ".doc"))
	fmt.Printf("HasExt(\"README\", \"txt\", \"md\") = %v\n\n", stringutils.HasExt("README", "txt", "md"))

	// Practical Example: File processing
	fmt.Println("Practical Example - File Processing:")
	files := []string{
		"document.PDF",
		"photo.JPG",
		"data.json",
		"script.js",
		"README",
	}

	for _, file := range files {
		name := stringutils.BaseNoExt(file)
		ext := stringutils.ExtNoDot(file)
		isImage := stringutils.HasExt(file, "jpg", "jpeg", "png", "gif", "webp")
		isDoc := stringutils.HasExt(file, "pdf", "doc", "docx", "txt")

		fmt.Printf("  %s: name=%q, ext=%q, isImage=%v, isDoc=%v\n",
			filepath.Base(file), name, ext, isImage, isDoc)
	}
}
