#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Markdown Utilities Test Suite
==========================================
Comprehensive test suite for the markdown_utils module.

Run: python markdown_utils_test.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # HTML entity functions
    escape_html, unescape_html,
    
    # Conversion functions
    markdown_to_html, html_to_markdown,
    
    # Extraction functions
    extract_headings, extract_links, extract_code_blocks, extract_tables,
    
    # Generation functions
    create_table, create_link, create_image, create_code_block,
    create_inline_code, create_list, create_blockquote,
    create_horizontal_rule, create_heading,
    
    # Validation
    validate_markdown,
    
    # Transformation
    transform_headings, remove_formatting, word_count,
    
    # Utility functions
    join_markdown, split_by_heading, strip_comments,
    
    # Data classes
    HeadingInfo, LinkInfo, CodeBlockInfo, TableInfo,
)


# ============================================================================
# Test Results Tracking
# ============================================================================

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def record(self, name: str, passed: bool, error: str = None):
        if passed:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            self.errors.append((name, error))
            print(f"  ✗ {name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")
        print(f"{'='*60}")
        return self.failed == 0


results = TestResults()


# ============================================================================
# Helper Functions
# ============================================================================

def assert_equal(actual, expected, tolerance: float = 0):
    """Assert equality with optional tolerance for floats."""
    if tolerance > 0:
        if isinstance(actual, tuple):
            return all(abs(a - e) <= tolerance for a, e in zip(actual, expected))
        return abs(actual - expected) <= tolerance
    
    return actual == expected


def test_section(name: str):
    """Print test section header."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")


def test(name: str, condition: bool, error_msg: str = None):
    """Record a test result."""
    if not condition:
        error_msg = error_msg or f"Expected True, got {condition}"
    results.record(name, condition, error_msg if not condition else None)


# ============================================================================
# HTML Entity Tests
# ============================================================================

def test_html_entities():
    """Test HTML escaping and unescaping."""
    test_section("HTML Entity Functions")
    
    # escape_html
    test("escape_html: basic", 
         escape_html("<script>") == "&lt;script&gt;")
    test("escape_html: quotes",
         escape_html('"hello"') == "&quot;hello&quot;")
    test("escape_html: ampersand",
         escape_html("A & B") == "A &amp; B")
    
    # unescape_html
    test("unescape_html: basic",
         unescape_html("&lt;div&gt;") == "<div>")
    test("unescape_html: roundtrip",
         unescape_html(escape_html("<test>")) == "<test>")


# ============================================================================
# Markdown to HTML Tests
# ============================================================================

def test_markdown_to_html():
    """Test Markdown to HTML conversion."""
    test_section("Markdown to HTML Conversion")
    
    # Headers
    test("md2html: h1",
         "<h1>Hello</h1>" in markdown_to_html("# Hello"))
    test("md2html: h2",
         "<h2>World</h2>" in markdown_to_html("## World"))
    test("md2html: h6",
         "<h6>Small</h6>" in markdown_to_html("###### Small"))
    
    # Bold and Italic
    test("md2html: bold",
         "<strong>bold</strong>" in markdown_to_html("**bold**"))
    test("md2html: italic",
         "<em>italic</em>" in markdown_to_html("*italic*"))
    test("md2html: bold-italic",
         "<strong><em>both</em></strong>" in markdown_to_html("***both***"))
    
    # Links
    html = markdown_to_html("[Google](https://google.com)")
    test("md2html: link",
         '<a href="https://google.com"' in html and "Google" in html)
    
    # Images
    html = markdown_to_html("![Alt](image.png)")
    test("md2html: image",
         '<img' in html and 'src="image.png"' in html)
    
    # Code blocks
    html = markdown_to_html("```python\nprint(1)\n```")
    test("md2html: code block",
         "<pre>" in html and "<code" in html)
    
    # Inline code
    html = markdown_to_html("`code`")
    test("md2html: inline code",
         "<code>code</code>" in html)
    
    # Lists
    html = markdown_to_html("- Item 1\n- Item 2")
    test("md2html: unordered list",
         "<ul>" in html and "<li>" in html)
    
    # Blockquotes
    html = markdown_to_html("> Quote")
    test("md2html: blockquote",
         "<blockquote>" in html)
    
    # Horizontal rule
    html = markdown_to_html("---")
    test("md2html: horizontal rule",
         "<hr" in html)


# ============================================================================
# HTML to Markdown Tests
# ============================================================================

def test_html_to_markdown():
    """Test HTML to Markdown conversion."""
    test_section("HTML to Markdown Conversion")
    
    # Headers
    test("html2md: h1",
         html_to_markdown("<h1>Hello</h1>") == "# Hello")
    test("html2md: h2",
         html_to_markdown("<h2>World</h2>") == "## World")
    
    # Bold and Italic
    test("html2md: bold",
         "**text**" in html_to_markdown("<strong>text</strong>"))
    test("html2md: italic",
         "*text*" in html_to_markdown("<em>text</em>"))
    
    # Links
    md = html_to_markdown('<a href="https://example.com">Link</a>')
    test("html2md: link",
         "[Link]" in md and "https://example.com" in md)
    
    # Code
    test("html2md: inline code",
         "`code`" in html_to_markdown("<code>code</code>"))
    
    # Lists
    md = html_to_markdown("<ul><li>Item</li></ul>")
    test("html2md: list",
         "- Item" in md)


# ============================================================================
# Heading Extraction Tests
# ============================================================================

def test_extract_headings():
    """Test heading extraction."""
    test_section("Heading Extraction")
    
    md = "# Heading 1\n## Heading 2\n### Heading 3"
    headings = extract_headings(md)
    
    test("extract_headings: count", len(headings) == 3)
    test("extract_headings: level 1", headings[0].level == 1)
    test("extract_headings: level 2", headings[1].level == 2)
    test("extract_headings: text", headings[0].text == "Heading 1")
    test("extract_headings: anchor", headings[0].anchor == "heading-1")
    test("extract_headings: line number", headings[0].line_number == 1)
    
    # Test to_markdown method
    test("extract_headings: to_markdown",
         headings[0].to_markdown() == "# Heading 1")


# ============================================================================
# Link Extraction Tests
# ============================================================================

def test_extract_links():
    """Test link extraction."""
    test_section("Link Extraction")
    
    md = """
# Test
![Image](img.png)
[Google](https://google.com "Search")
[Link2](https://example.com)
"""
    links = extract_links(md)
    
    test("extract_links: count", len(links) == 3)
    test("extract_links: image detected", links[0].is_image == True)
    test("extract_links: link text", links[1].text == "Google")
    test("extract_links: link url", links[1].url == "https://google.com")
    test("extract_links: link title", links[1].title == "Search")
    test("extract_links: regular link", links[2].is_image == False)


# ============================================================================
# Code Block Extraction Tests
# ============================================================================

def test_extract_code_blocks():
    """Test code block extraction."""
    test_section("Code Block Extraction")
    
    md = """
```python
def hello():
    print("Hello")
```

Inline `code` here.
"""
    blocks = extract_code_blocks(md)
    
    test("extract_code_blocks: count", len(blocks) == 2)
    test("extract_code_blocks: language", blocks[0].language == "python")
    test("extract_code_blocks: code content", "def hello():" in blocks[0].code)
    test("extract_code_blocks: inline", blocks[1].is_inline == True)
    test("extract_code_blocks: inline code", blocks[1].code == "code")


# ============================================================================
# Table Extraction Tests
# ============================================================================

def test_extract_tables():
    """Test table extraction."""
    test_section("Table Extraction")
    
    md = """
| Name | Age | City |
|:---|:---:|---:|
| Alice | 30 | NYC |
| Bob | 25 | LA |
"""
    tables = extract_tables(md)
    
    test("extract_tables: count", len(tables) == 1)
    test("extract_tables: headers", tables[0].headers == ["Name", "Age", "City"])
    test("extract_tables: rows count", len(tables[0].rows) == 2)
    test("extract_tables: first row", tables[0].rows[0] == ["Alice", "30", "NYC"])
    test("extract_tables: alignments", len(tables[0].alignments) == 3)
    test("extract_tables: to_markdown", "| Name |" in tables[0].to_markdown())


# ============================================================================
# Table Generation Tests
# ============================================================================

def test_create_table():
    """Test table creation."""
    test_section("Table Generation")
    
    table = create_table(
        ["Name", "Age"],
        [["Alice", "30"], ["Bob", "25"]],
        ["left", "right"]
    )
    
    test("create_table: has header", "| Name | Age |" in table)
    test("create_table: has separator", "|:---|---:|" in table)
    test("create_table: has data", "| Alice | 30 |" in table)
    test("create_table: row count", table.count("|") == 12)  # 4 rows * 3 pipes


# ============================================================================
# Link Generation Tests
# ============================================================================

def test_create_link():
    """Test link creation."""
    test_section("Link Generation")
    
    test("create_link: basic",
         create_link("Google", "https://google.com") == "[Google](https://google.com)")
    test("create_link: with title",
         create_link("Google", "https://google.com", "Search") == 
         '[Google](https://google.com "Search")')


def test_create_image():
    """Test image creation."""
    test_section("Image Generation")
    
    test("create_image: basic",
         create_image("Logo", "logo.png") == "![Logo](logo.png)")
    test("create_image: with title",
         create_image("Logo", "logo.png", "Company Logo") == 
         '![Logo](logo.png "Company Logo")')


# ============================================================================
# Code Generation Tests
# ============================================================================

def test_create_code():
    """Test code block generation."""
    test_section("Code Generation")
    
    test("create_code_block: with language",
         create_code_block("print(1)", "python") == "```python\nprint(1)\n```")
    test("create_code_block: without language",
         create_code_block("code") == "```\ncode\n```")
    test("create_inline_code",
         create_inline_code("code") == "`code`")


# ============================================================================
# List Generation Tests
# ============================================================================

def test_create_list():
    """Test list generation."""
    test_section("List Generation")
    
    # Unordered list
    ul = create_list(["A", "B", "C"])
    test("create_list: unordered", "- A\n- B\n- C" == ul)
    
    # Ordered list
    ol = create_list(["A", "B", "C"], ordered=True)
    test("create_list: ordered", "1. A\n2. B\n3. C" == ol)
    
    # Ordered with start
    ol2 = create_list(["A", "B"], ordered=True, start=5)
    test("create_list: ordered start", "5. A\n6. B" == ol2)


# ============================================================================
# Other Generation Tests
# ============================================================================

def test_create_other():
    """Test other generation functions."""
    test_section("Other Generation Functions")
    
    test("create_blockquote",
         create_blockquote("Hello") == "> Hello")
    test("create_blockquote: multiline",
         "> Line1\n> Line2" in create_blockquote("Line1\nLine2"))
    
    test("create_horizontal_rule: dash",
         create_horizontal_rule("dash") == "---")
    test("create_horizontal_rule: asterisk",
         create_horizontal_rule("asterisk") == "***")
    
    test("create_heading: h1",
         create_heading("Test", 1) == "# Test")
    test("create_heading: h3",
         create_heading("Test", 3) == "### Test")
    test("create_heading: clamp max",
         create_heading("Test", 10) == "###### Test")
    test("create_heading: clamp min",
         create_heading("Test", 0) == "# Test")


# ============================================================================
# Validation Tests
# ============================================================================

def test_validate_markdown():
    """Test Markdown validation."""
    test_section("Markdown Validation")
    
    # Valid markdown
    valid, issues = validate_markdown("# Hello\n\nWorld")
    test("validate: valid md", valid == True)
    test("validate: no issues", len(issues) == 0)
    
    # Unclosed bold
    valid, issues = validate_markdown("**bold text")
    test("validate: unclosed bold", valid == False)
    test("validate: bold issue detected", any("bold" in i for i in issues))
    
    # Unclosed code block
    valid, issues = validate_markdown("```python\ncode")
    test("validate: unclosed code block", valid == False)
    test("validate: code block issue detected", any("code block" in i for i in issues))
    
    # Empty link
    valid, issues = validate_markdown("[text]()")
    test("validate: empty link", valid == False)
    test("validate: empty link detected", any("link URL" in i for i in issues))


# ============================================================================
# Transformation Tests
# ============================================================================

def test_transform_headings():
    """Test heading transformation."""
    test_section("Heading Transformation")
    
    md = "# H1\n## H2\n### H3"
    
    # Increase levels
    result = transform_headings(md, 1)
    test("transform: increase", "## H1\n### H2\n#### H3" == result)
    
    # Decrease levels
    result = transform_headings(md, -1)
    test("transform: decrease", "# H2\n## H3" in result)  # H1 can't go lower


def test_remove_formatting():
    """Test formatting removal."""
    test_section("Remove Formatting")
    
    md = "**bold** *italic* [link](url) `code`"
    result = remove_formatting(md)
    
    test("remove: bold", "**" not in result)
    test("remove: italic", "*" not in result)
    test("remove: links", "[" not in result)
    test("remove: code", "`" not in result)
    test("remove: keeps text", "bold" in result and "italic" in result)


def test_word_count():
    """Test word counting."""
    test_section("Word Count")
    
    md = "# Hello World\n\nThis is a **test**."
    counts = word_count(md)
    
    test("word_count: words", counts['word_count'] == 6)
    test("word_count: lines", counts['line_count'] == 3)
    test("word_count: chars", counts['char_count'] > 0)


# ============================================================================
# Utility Function Tests
# ============================================================================

def test_join_markdown():
    """Test joining Markdown documents."""
    test_section("Join Markdown")
    
    result = join_markdown("# Doc1", "# Doc2")
    test("join: has separator", "---" in result)
    test("join: has doc1", "# Doc1" in result)
    test("join: has doc2", "# Doc2" in result)
    
    # With custom separator
    result2 = join_markdown("A", "B", separator="\n\n")
    test("join: custom separator", "A\n\nB" == result2)


def test_split_by_heading():
    """Test splitting by heading."""
    test_section("Split by Heading")
    
    md = "# Section A\nContent A\n# Section B\nContent B"
    sections = split_by_heading(md)
    
    test("split: section count", len(sections) == 2)
    test("split: section A", "Section A" in sections)
    test("split: content A", "Content A" in sections["Section A"])
    test("split: section B", "Section B" in sections)


def test_strip_comments():
    """Test comment stripping."""
    test_section("Strip Comments")
    
    md = "Hello <!-- comment --> World"
    result = strip_comments(md)
    
    test("strip: removes comment", "<!--" not in result)
    test("strip: keeps text", "Hello" in result and "World" in result)
    
    # Multiline comment
    md2 = "Text <!-- multi\nline\ncomment --> More"
    result2 = strip_comments(md2)
    test("strip: multiline", "<!--" not in result2)


# ============================================================================
# Edge Case Tests
# ============================================================================

def test_edge_cases():
    """Test edge cases."""
    test_section("Edge Cases")
    
    # Empty input
    test("edge: empty md2html", markdown_to_html("") == "")
    test("edge: empty html2md", html_to_markdown("") == "")
    test("edge: empty headings", extract_headings("") == [])
    test("edge: empty links", extract_links("") == [])
    
    # Special characters
    md = "# Hello & Welcome <test>\n**Bold** text"
    html = markdown_to_html(md)
    test("edge: special chars", "&amp;" in html or "&" in html)
    
    # Nested formatting
    md = "**bold *italic* bold**"
    html = markdown_to_html(md)
    test("edge: nested formatting", "<strong>" in html and "<em>" in html)
    
    # Unicode
    md = "# 你好世界\nこんにちは"
    headings = extract_headings(md)
    test("edge: unicode", len(headings) == 1)
    test("edge: unicode text", headings[0].text == "你好世界")


# ============================================================================
# Main Test Runner
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "#"*60)
    print("# AllToolkit - Markdown Utilities Test Suite")
    print("#"*60)
    
    test_html_entities()
    test_markdown_to_html()
    test_html_to_markdown()
    test_extract_headings()
    test_extract_links()
    test_extract_code_blocks()
    test_extract_tables()
    test_create_table()
    test_create_link()
    test_create_image()
    test_create_code()
    test_create_list()
    test_create_other()
    test_validate_markdown()
    test_transform_headings()
    test_remove_formatting()
    test_word_count()
    test_join_markdown()
    test_split_by_heading()
    test_strip_comments()
    test_edge_cases()
    
    # Print summary
    success = results.summary()
    
    if success:
        print("\n✅ All tests passed!\n")
        return 0
    else:
        print(f"\n❌ {results.failed} test(s) failed\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
