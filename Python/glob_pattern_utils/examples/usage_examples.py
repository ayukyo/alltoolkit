"""
Glob Pattern Utils - Usage Examples

This file demonstrates various use cases for the glob_pattern_utils module.
Run with: python usage_examples.py
"""

import sys
import os

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    GlobPattern,
    match,
    filter_strings,
    expand_braces,
    translate,
    is_glob,
    escape,
    GlobMatcher,
    fnmatch_translate,
    glob_to_regex,
)


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def example_basic_matching():
    """Demonstrate basic pattern matching."""
    print_section("Basic Pattern Matching")
    
    # Using the match function
    print("Using match() function:")
    print(f"  match('*.txt', 'file.txt') -> {match('*.txt', 'file.txt')}")
    print(f"  match('*.txt', 'file.py') -> {match('*.txt', 'file.py')}")
    print(f"  match('test?.py', 'test1.py') -> {match('test?.py', 'test1.py')}")
    print(f"  match('test?.py', 'test12.py') -> {match('test?.py', 'test12.py')}")
    
    # Using GlobPattern class (more efficient for repeated matching)
    print("\nUsing GlobPattern class:")
    pattern = GlobPattern("*.py")
    files = ["main.py", "test.py", "readme.md", "config.json"]
    for f in files:
        print(f"  {f}: {pattern.match(f)}")


def example_character_classes():
    """Demonstrate character class patterns."""
    print_section("Character Classes")
    
    # Basic character class
    print("Basic character class [abc]:")
    pattern = GlobPattern("[abc].txt")
    for name in ["a.txt", "b.txt", "c.txt", "d.txt"]:
        print(f"  {name}: {pattern.match(name)}")
    
    # Range character class
    print("\nRange character class [a-z]:")
    pattern = GlobPattern("[a-z].txt")
    for name in ["a.txt", "m.txt", "z.txt", "A.txt", "1.txt"]:
        print(f"  {name}: {pattern.match(name)}")
    
    # Negated character class
    print("\nNegated character class [!abc]:")
    pattern = GlobPattern("[!abc].txt")
    for name in ["a.txt", "b.txt", "d.txt", "x.txt"]:
        print(f"  {name}: {pattern.match(name)}")
    
    # Digit class
    print("\nDigit class [0-9]:")
    pattern = GlobPattern("file[0-9].txt")
    for name in ["file1.txt", "file5.txt", "file9.txt", "fileA.txt"]:
        print(f"  {name}: {pattern.match(name)}")


def example_brace_expansion():
    """Demonstrate brace expansion."""
    print_section("Brace Expansion")
    
    # Match patterns with brace expansion
    print("Matching with braces:")
    pattern = GlobPattern("file.{txt,py,md}")
    for name in ["file.txt", "file.py", "file.md", "file.js"]:
        print(f"  {name}: {pattern.match(name)}")
    
    # Expand braces to get all patterns
    print("\nExpanding braces:")
    expanded = expand_braces("file.{txt,py,md}")
    print(f"  file.{{txt,py,md}} -> {expanded}")
    
    # Multiple braces
    print("\nMultiple brace expansions:")
    expanded = expand_braces("{src,dist}/*.{js,ts}")
    print(f"  {{src,dist}}/*.{{js,ts}} -> {expanded}")


def example_escape_characters():
    """Demonstrate escaping special characters."""
    print_section("Escape Characters")
    
    # Match literal asterisk
    print("Matching literal special characters:")
    pattern = GlobPattern("file\\*.txt")
    print(f"  Pattern: 'file\\*.txt'")
    for name in ["file*.txt", "file_test.txt", "file.txt"]:
        print(f"    {name}: {pattern.match(name)}")
    
    # Escape function
    print("\nUsing escape() function:")
    escaped = escape("file*.txt")
    print(f"  escape('file*.txt') -> '{escaped}'")
    pattern = GlobPattern(escaped)
    print(f"  match('{escaped}', 'file*.txt') -> {pattern.match('file*.txt')}")


def example_case_sensitivity():
    """Demonstrate case-sensitive and case-insensitive matching."""
    print_section("Case Sensitivity")
    
    # Case-sensitive (default)
    print("Case-sensitive matching (default):")
    pattern = GlobPattern("FILE.txt", case_sensitive=True)
    for name in ["FILE.txt", "file.txt", "File.Txt"]:
        print(f"  {name}: {pattern.match(name)}")
    
    # Case-insensitive
    print("\nCase-insensitive matching:")
    pattern = GlobPattern("FILE.txt", case_sensitive=False)
    for name in ["FILE.txt", "file.txt", "File.Txt"]:
        print(f"  {name}: {pattern.match(name)}")


def example_filter_strings():
    """Demonstrate filtering strings."""
    print_section("Filtering Strings")
    
    files = [
        "main.py",
        "test.py",
        "utils.py",
        "readme.md",
        "config.json",
        "data.txt",
        "log.txt",
    ]
    
    # Filter by extension
    print("Filter *.py:")
    py_files = filter_strings("*.py", files)
    print(f"  {py_files}")
    
    print("\nFilter *.txt:")
    txt_files = filter_strings("*.txt", files)
    print(f"  {txt_files}")
    
    print("\nFilter test*:")
    test_files = filter_strings("test*", files)
    print(f"  {test_files}")


def example_glob_matcher():
    """Demonstrate GlobMatcher for multiple patterns."""
    print_section("GlobMatcher - Multiple Patterns")
    
    # Create matcher with multiple patterns
    matcher = GlobMatcher()
    matcher.add_pattern("*.py")
    matcher.add_pattern("*.txt")
    matcher.add_pattern("*.md")
    
    files = [
        "main.py",
        "readme.md",
        "data.txt",
        "config.json",
        "test.py",
    ]
    
    print("Patterns: *.py, *.txt, *.md")
    print("\nmatch_any results:")
    for f in files:
        print(f"  {f}: {matcher.match_any(f)}")
    
    print("\nFiltered files (match any pattern):")
    filtered = matcher.filter(files)
    print(f"  {filtered}")
    
    # Clear and add new patterns
    matcher.clear()
    matcher.add_pattern("test*")
    matcher.add_pattern("*config*")
    
    print("\nNew patterns: test*, *config*")
    print(f"  Filtered: {matcher.filter(files)}")


def example_is_glob():
    """Demonstrate detecting glob patterns."""
    print_section("Detecting Glob Patterns")
    
    patterns = [
        "*.txt",
        "file?.py",
        "[abc].md",
        "{src,dist}/*.js",
        "file.txt",
        "file\\*.txt",  # Escaped asterisk
    ]
    
    for p in patterns:
        result = is_glob(p)
        print(f"  is_glob('{p}') -> {result}")


def example_translate():
    """Demonstrate converting glob to regex."""
    print_section("Translating Glob to Regex")
    
    patterns = [
        "*.txt",
        "file?.py",
        "[abc].md",
        "test_[0-9]*.json",
        "src/**/*.js",
    ]
    
    for p in patterns:
        regex = translate(p)
        print(f"  '{p}' -> '{regex}'")


def example_practical_use_cases():
    """Demonstrate practical use cases."""
    print_section("Practical Use Cases")
    
    # File type validation
    print("1. File type validation:")
    allowed_images = GlobMatcher()
    allowed_images.add_pattern("*.jpg")
    allowed_images.add_pattern("*.jpeg")
    allowed_images.add_pattern("*.png")
    allowed_images.add_pattern("*.gif")
    allowed_images.add_pattern("*.webp")
    
    uploads = ["photo.jpg", "document.pdf", "avatar.png", "script.js"]
    for f in uploads:
        valid = allowed_images.match_any(f)
        print(f"  {f}: {'✓ Valid image' if valid else '✗ Invalid'}")
    
    # Log file pattern matching
    print("\n2. Log file pattern matching:")
    log_pattern = GlobPattern("*-????-??-??.log")
    log_files = [
        "app-2024-01-15.log",
        "error-2024-01-15.log",
        "debug.log",
        "service-2024-01-16.log",
    ]
    for f in log_files:
        print(f"  {f}: {log_pattern.match(f)}")
    
    # Configuration file matching
    print("\n3. Configuration file matching:")
    config_matcher = GlobMatcher()
    config_matcher.add_pattern("*.config")
    config_matcher.add_pattern("*.conf")
    config_matcher.add_pattern("*.ini")
    config_matcher.add_pattern("*.yaml")
    config_matcher.add_pattern("*.yml")
    config_matcher.add_pattern("*.json")
    
    files = ["app.conf", "main.py", "config.json", "settings.yaml", "readme.md"]
    config_files = config_matcher.filter(files)
    print(f"  Config files: {config_files}")


def example_edge_cases():
    """Demonstrate edge cases."""
    print_section("Edge Cases")
    
    # Empty pattern
    print("Empty pattern:")
    pattern = GlobPattern("")
    print(f"  match('') -> {pattern.match('')}")
    print(f"  match('a') -> {pattern.match('a')}")
    
    # Star matches empty
    print("\nStar matches empty string:")
    print(f"  match('*', '') -> {match('*', '')}")
    
    # Question requires one char
    print("\nQuestion requires exactly one character:")
    print(f"  match('?', '') -> {match('?', '')}")
    print(f"  match('?', 'a') -> {match('?', 'a')}")
    print(f"  match('?', 'ab') -> {match('?', 'ab')}")
    
    # Unicode support
    print("\nUnicode support:")
    pattern = GlobPattern("文件*.txt")
    print(f"  match('文件*.txt', '文件1.txt') -> {pattern.match('文件1.txt')}")
    print(f"  match('文件*.txt', '文件测试.txt') -> {pattern.match('文件测试.txt')}")


def main():
    """Run all examples."""
    print("="*60)
    print(" Glob Pattern Utils - Usage Examples")
    print("="*60)
    
    example_basic_matching()
    example_character_classes()
    example_brace_expansion()
    example_escape_characters()
    example_case_sensitivity()
    example_filter_strings()
    example_glob_matcher()
    example_is_glob()
    example_translate()
    example_practical_use_cases()
    example_edge_cases()
    
    print("\n" + "="*60)
    print(" Examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()