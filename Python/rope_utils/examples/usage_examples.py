#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Rope Utilities Usage Examples
===========================================
Practical examples demonstrating the Rope data structure for efficient
string manipulation.

The Rope data structure is ideal for:
- Text editors and IDEs
- Large file manipulation
- String processing pipelines
- Undo/redo implementations
"""

import sys
sys.path.insert(0, '..')

from mod import Rope, BatchEditor, from_lines, concat_ropes


def example_basic_operations():
    """Basic rope operations."""
    print("=" * 60)
    print("Example 1: Basic Operations")
    print("=" * 60)
    
    # Create a rope
    r = Rope("Hello, World!")
    print(f"Created rope: {r}")
    print(f"Length: {len(r)}")
    print(f"Depth: {r.depth()}")
    
    # Access characters
    print(f"\nCharacter at index 0: {r[0]}")
    print(f"Character at index 7: {r[7]}")
    print(f"Last character: {r[-1]}")
    
    # Slicing
    print(f"\nSlice [0:5]: {r[0:5]}")
    print(f"Slice [7:12]: {r[7:12]}")
    print(f"Reverse: {r.reverse()}")
    
    print()


def example_text_editing():
    """Text editing operations."""
    print("=" * 60)
    print("Example 2: Text Editing (Simulating a Text Editor)")
    print("=" * 60)
    
    # Start with a document
    doc = Rope("The quick brown fox jumps over the lazy dog.")
    print(f"Original: {doc}")
    
    # Insert text at position 4
    doc = doc.insert(4, "very ")
    print(f"After insert: {doc}")
    
    # Replace "brown" with "red"
    pos = doc.find("brown")
    if pos != -1:
        doc = doc.delete(pos, pos + 5)
        doc = doc.insert(pos, "red")
    print(f"After replace: {doc}")
    
    # Delete a word
    pos = doc.find("lazy ")
    if pos != -1:
        doc = doc.delete(pos, pos + 5)
    print(f"After delete: {doc}")
    
    # Add at end
    doc = doc.insert(len(doc), " Amazing!")
    print(f"After append: {doc}")
    
    print()


def example_batch_operations():
    """Batch editing operations."""
    print("=" * 60)
    print("Example 3: Batch Operations")
    print("=" * 60)
    
    doc = Rope("function hello() { return 'world'; }")
    print(f"Original: {doc}")
    
    # Batch multiple edits
    editor = BatchEditor(doc)
    editor.insert(9, "greet")      # function greet...
    editor.replace(24, 29, "hi")   # 'world' -> 'hi'
    editor.insert(len(doc), " // greeting function")
    
    result = editor.apply()
    print(f"After batch: {result}")
    
    print()


def example_large_file_simulation():
    """Simulate large file operations."""
    print("=" * 60)
    print("Example 4: Large File Simulation")
    print("=" * 60)
    
    # Create a "large" document (simulating a file)
    lines = [f"Line {i}: This is line number {i} with some content." for i in range(1000)]
    doc = from_lines(lines)
    
    print(f"Created document with {len(doc)} characters")
    print(f"Tree depth: {doc.depth()}")
    print(f"Stats: {doc.stats()}")
    
    # Efficient insertions at beginning
    doc = doc.insert(0, "// Header comment\n")
    print(f"\nAfter header insertion: {len(doc)} characters")
    
    # Efficient insertions at end
    doc = doc.insert(len(doc), "\n// Footer comment")
    print(f"After footer insertion: {len(doc)} characters")
    
    # Find and count
    count = doc.count("Line")
    print(f"Occurrences of 'Line': {count}")
    
    # Extract substring
    first_line = doc[0:50]
    print(f"First 50 chars: {first_line}...")
    
    print()


def example_document_manipulation():
    """Document manipulation example."""
    print("=" * 60)
    print("Example 5: Document Manipulation")
    print("=" * 60)
    
    # Create a markdown document
    doc = Rope("""# Title

This is a paragraph with some text.

## Section 1

More content here.

## Section 2

Even more content.
""")
    
    print("Original document:")
    print(str(doc))
    print("-" * 40)
    
    # Add a new section
    section3 = "\n## Section 3\n\nNew section content.\n"
    doc = doc.insert(len(doc), section3)
    
    print("After adding section 3:")
    print(str(doc))
    print("-" * 40)
    
    # Extract all lines
    lines = doc.lines()
    print(f"Total lines: {len(lines)}")
    
    # Find section headers
    for i, line in enumerate(lines):
        if line.startswith("#"):
            print(f"  Header on line {i}: {line}")
    
    print()


def example_rope_concatenation():
    """Rope concatenation example."""
    print("=" * 60)
    print("Example 6: Rope Concatenation")
    print("=" * 60)
    
    # Create multiple ropes
    r1 = Rope("Hello, ")
    r2 = Rope("World!")
    r3 = Rope(" How are you?")
    
    # Concatenate using +
    combined = r1 + r2 + r3
    print(f"Combined: {combined}")
    
    # Repeat
    repeated = Rope("abc") * 3
    print(f"Repeated: {repeated}")
    
    # Join
    separator = Rope(" | ")
    items = ["Apple", "Banana", "Cherry"]
    joined = separator.join(items)
    print(f"Joined: {joined}")
    
    print()


def example_search_and_replace():
    """Search and replace example."""
    print("=" * 60)
    print("Example 7: Search and Replace")
    print("=" * 60)
    
    doc = Rope("The quick brown fox jumps over the lazy dog. The fox was very fast.")
    print(f"Original: {doc}")
    
    # Find
    pos = doc.find("fox")
    print(f"First 'fox' at position: {pos}")
    
    pos = doc.rfind("fox")
    print(f"Last 'fox' at position: {pos}")
    
    # Count
    count = doc.count("fox")
    print(f"Total 'fox' occurrences: {count}")
    
    # Replace all
    replaced = doc.replace("fox", "cat")
    print(f"After replace all: {replaced}")
    
    # Replace first occurrence only
    replaced_one = doc.replace("fox", "wolf", 1)
    print(f"After replace first: {replaced_one}")
    
    print()


def example_text_analysis():
    """Text analysis example."""
    print("=" * 60)
    print("Example 8: Text Analysis")
    print("=" * 60)
    
    text = Rope("""
    The quick brown fox jumps over the lazy dog.
    Pack my box with five dozen liquor jugs.
    How vexingly quick daft zebras jump!
    """)
    
    # Clean up
    text = text.strip()
    
    # Basic stats
    print(f"Text: {text}")
    print(f"Length: {len(text)} characters")
    print(f"Lines: {len(text.lines())}")
    print(f"Words: {len(text.words())}")
    
    # Case conversions
    print(f"\nUppercase: {text.upper()}")
    print(f"Lowercase: {text.lower()}")
    print(f"Title case: {text.title()}")
    
    # Check prefixes/suffixes
    print(f"\nStarts with 'The': {text.startswith('The')}")
    print(f"Ends with '!': {text.endswith('!')}")
    
    # Contains
    print(f"Contains 'fox': {'fox' in text}")
    print(f"Contains 'cat': {'cat' in text}")
    
    print()


def example_split_and_merge():
    """Split and merge example."""
    print("=" * 60)
    print("Example 9: Split and Merge")
    print("=" * 60)
    
    doc = Rope("First part | Second part | Third part")
    print(f"Original: {doc}")
    
    # Split at separator
    pos = doc.find(" | ")
    left, right = doc.split(pos)
    print(f"Split at first separator:")
    print(f"  Left: {left}")
    print(f"  Right: {right}")
    
    # Split again
    pos = right.find(" | ")
    middle, end = right.split(pos)
    print(f"Split right again:")
    print(f"  Middle: {middle}")
    print(f"  End: {end}")
    
    # Merge back
    merged = left + " | " + middle + " | " + end
    print(f"Merged back: {merged}")
    
    print()


def example_unicode_handling():
    """Unicode handling example."""
    print("=" * 60)
    print("Example 10: Unicode Handling")
    print("=" * 60)
    
    # Various Unicode text
    texts = [
        "Hello 你好 مرحبا",
        "Emoji: 🌍🎉🚀💡",
        "Math: α + β = γ",
        "Symbols: © ® ™ € £ ¥",
    ]
    
    for t in texts:
        r = Rope(t)
        print(f"Text: {r}")
        print(f"  Length: {len(r)} characters")
        print(f"  Reversed: {r.reverse()}")
        print()
    
    print()


def example_performance_comparison():
    """Performance comparison with string."""
    print("=" * 60)
    print("Example 11: Performance Comparison")
    print("=" * 60)
    
    import time
    
    n = 5000
    
    # String prepend (O(n²) overall)
    start = time.time()
    s = ""
    for i in range(n):
        s = "X" + s
    string_time = time.time() - start
    print(f"String prepend {n} times: {string_time:.4f}s")
    
    # Rope prepend (O(n log n) overall)
    start = time.time()
    r = Rope("")
    for i in range(n):
        r = r.insert(0, "X")
    rope_time = time.time() - start
    print(f"Rope prepend {n} times: {rope_time:.4f}s")
    print(f"Speedup: {string_time/rope_time:.1f}x faster")
    
    # Verify correctness
    assert str(r) == s, "Results don't match!"
    print("Results verified: ✓")
    
    print()


def main():
    """Run all examples."""
    example_basic_operations()
    example_text_editing()
    example_batch_operations()
    example_large_file_simulation()
    example_document_manipulation()
    example_rope_concatenation()
    example_search_and_replace()
    example_text_analysis()
    example_split_and_merge()
    example_unicode_handling()
    example_performance_comparison()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()