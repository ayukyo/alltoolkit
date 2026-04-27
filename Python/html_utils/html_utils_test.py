#!/usr/bin/env python3
"""
AllToolkit - HTML Utilities Test Suite

Comprehensive tests for HTML parsing, manipulation, and generation utilities.
Zero dependencies - uses only Python standard library.
"""

import os
import sys
import unittest
from typing import List, Dict, Any

# Import the module under test

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    parse_html, find_elements, find_by_id, find_by_class,
    extract_links, extract_images, sanitize_html, html_to_text,
    generate_tag, generate_link, generate_image, generate_table, generate_form,
    minify_html, prettify_html, extract_title, extract_meta,
    count_tags, get_dom_depth, validate_html_structure,
    HTMLElement, HTMLElementType, HTMLTreeBuilder
)


class TestHTMLElement(unittest.TestCase):
    """Tests for HTMLElement dataclass."""
    
    def test_create_element(self):
        """Test creating a basic element."""
        elem = HTMLElement(tag="div")
        self.assertEqual(elem.tag, "div")
        self.assertEqual(elem.attributes, {})
        self.assertEqual(elem.children, [])
        self.assertEqual(elem.text, "")
    
    def test_create_element_with_attributes(self):
        """Test creating an element with attributes."""
        elem = HTMLElement(tag="a", attributes={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(elem.get_attribute("href"), "https://example.com")
        self.assertEqual(elem.get_attribute("target"), "_blank")
        self.assertEqual(elem.get_attribute("missing", "default"), "default")
    
    def test_set_remove_attribute(self):
        """Test setting and removing attributes."""
        elem = HTMLElement(tag="div")
        elem.set_attribute("class", "container")
        self.assertEqual(elem.get_attribute("class"), "container")
        
        self.assertTrue(elem.remove_attribute("class"))
        self.assertIsNone(elem.get_attribute("class"))
        self.assertFalse(elem.remove_attribute("class"))
    
    def test_class_manipulation(self):
        """Test adding and removing CSS classes."""
        elem = HTMLElement(tag="div", attributes={"class": "foo bar"})
        
        self.assertTrue(elem.has_class("foo"))
        self.assertTrue(elem.has_class("bar"))
        self.assertFalse(elem.has_class("baz"))
        
        elem.add_class("baz")
        self.assertTrue(elem.has_class("baz"))
        
        elem.remove_class("foo")
        self.assertFalse(elem.has_class("foo"))
    
    def test_get_text(self):
        """Test getting text content."""
        root = HTMLElement(tag="div")
        text1 = HTMLElement(tag="#text", text="Hello ", element_type=HTMLElementType.TEXT)
        text2 = HTMLElement(tag="#text", text="World", element_type=HTMLElementType.TEXT)
        root.children = [text1, text2]
        
        self.assertEqual(root.get_text(), "Hello World")
    
    def test_to_html_simple(self):
        """Test converting simple element to HTML."""
        elem = HTMLElement(tag="p", text="Hello World")
        self.assertEqual(elem.to_html(), "<p>Hello World</p>")
    
    def test_to_html_with_attributes(self):
        """Test converting element with attributes to HTML."""
        elem = HTMLElement(tag="a", attributes={"href": "https://example.com"}, text="Link")
        self.assertEqual(elem.to_html(), '<a href="https://example.com">Link</a>')
    
    def test_to_html_self_closing(self):
        """Test self-closing tags."""
        elem = HTMLElement(tag="img", attributes={"src": "test.png"})
        self.assertEqual(elem.to_html(), '<img src="test.png">')
    
    def test_to_html_nested(self):
        """Test nested elements."""
        parent = HTMLElement(tag="div")
        child = HTMLElement(tag="span", text="content")
        parent.children = [child]
        html = parent.to_html()
        self.assertIn("<span>content</span>", html)
    
    def test_repr_text_element(self):
        """Test repr for text element."""
        elem = HTMLElement(tag="#text", text="Hello", element_type=HTMLElementType.TEXT)
        self.assertIn("Text", repr(elem))
    
    def test_repr_comment_element(self):
        """Test repr for comment element."""
        elem = HTMLElement(tag="#comment", text="A comment", element_type=HTMLElementType.COMMENT)
        self.assertIn("Comment", repr(elem))


class TestHTMLParser(unittest.TestCase):
    """Tests for HTML parsing."""
    
    def test_parse_simple_html(self):
        """Test parsing simple HTML."""
        html = "<div><p>Hello</p></div>"
        root = parse_html(html)
        self.assertEqual(root.tag, "root")
        self.assertEqual(len(root.children), 1)
    
    def test_parse_with_attributes(self):
        """Test parsing HTML with attributes."""
        html = '<a href="https://example.com" target="_blank">Link</a>'
        root = parse_html(html)
        links = find_elements(root, tag="a")
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].get_attribute("href"), "https://example.com")
        self.assertEqual(links[0].get_attribute("target"), "_blank")
    
    def test_parse_nested_elements(self):
        """Test parsing nested elements."""
        html = "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        root = parse_html(html)
        lis = find_elements(root, tag="li")
        self.assertEqual(len(lis), 2)
    
    def test_parse_comments(self):
        """Test parsing HTML comments."""
        html = "<div><!-- This is a comment --><p>Content</p></div>"
        root = parse_html(html)
        comments = find_elements(root, tag="#comment")
        self.assertEqual(len(comments), 1)
        self.assertIn("This is a comment", comments[0].text)
    
    def test_parse_doctype(self):
        """Test parsing DOCTYPE declaration."""
        html = "<!DOCTYPE html><html><body>Test</body></html>"
        root = parse_html(html)
        doctypes = find_elements(root, tag="!DOCTYPE")
        self.assertEqual(len(doctypes), 1)
    
    def test_parse_with_text_nodes(self):
        """Test parsing text nodes."""
        html = "<p>Hello <strong>World</strong>!</p>"
        root = parse_html(html)
        text = root.get_text()
        self.assertIn("Hello", text)
        self.assertIn("World", text)


class TestFindElements(unittest.TestCase):
    """Tests for element finding functions."""
    
    def setUp(self):
        """Set up test HTML."""
        self.html = """
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <div id="main" class="container">
                    <h1 class="title">Hello World</h1>
                    <p class="intro">Introduction text</p>
                    <a href="https://example.com" class="link">Example</a>
                    <a href="https://test.com" class="link">Test</a>
                </div>
            </body>
        </html>
        """
        self.root = parse_html(self.html)
    
    def test_find_by_tag(self):
        """Test finding elements by tag name."""
        links = find_elements(self.root, tag="a")
        self.assertEqual(len(links), 2)
        
        headings = find_elements(self.root, tag="h1")
        self.assertEqual(len(headings), 1)
    
    def test_find_by_id(self):
        """Test finding element by ID."""
        main = find_by_id(self.root, "main")
        self.assertIsNotNone(main)
        self.assertEqual(main.tag, "div")
        
        missing = find_by_id(self.root, "nonexistent")
        self.assertIsNone(missing)
    
    def test_find_by_class(self):
        """Test finding elements by class name."""
        links = find_by_class(self.root, "link")
        self.assertEqual(len(links), 2)
        
        containers = find_by_class(self.root, "container")
        self.assertEqual(len(containers), 1)
    
    def test_find_by_attributes(self):
        """Test finding elements by attributes."""
        links = find_elements(self.root, tag="a", attributes={"href": "https://example.com"})
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].get_text().strip(), "Example")
    
    def test_find_by_text(self):
        """Test finding elements by text content."""
        elements = find_elements(self.root, text="Hello")
        self.assertGreater(len(elements), 0)


class TestExtractData(unittest.TestCase):
    """Tests for data extraction functions."""
    
    def test_extract_links(self):
        """Test extracting links from HTML."""
        html = """
        <html>
            <body>
                <a href="https://example.com" title="Example Site">Example</a>
                <a href="https://test.com">Test Link</a>
                <a href="/relative">Relative</a>
            </body>
        </html>
        """
        links = extract_links(html)
        self.assertEqual(len(links), 3)
        
        self.assertEqual(links[0]["href"], "https://example.com")
        self.assertEqual(links[0]["text"], "Example")
        self.assertEqual(links[0]["title"], "Example Site")
    
    def test_extract_images(self):
        """Test extracting images from HTML."""
        html = """
        <html>
            <body>
                <img src="image1.jpg" alt="First Image" title="Image 1">
                <img src="image2.png" alt="Second Image">
                <img src="image3.gif">
            </body>
        </html>
        """
        images = extract_images(html)
        self.assertEqual(len(images), 3)
        
        self.assertEqual(images[0]["src"], "image1.jpg")
        self.assertEqual(images[0]["alt"], "First Image")
        self.assertEqual(images[0]["title"], "Image 1")
    
    def test_extract_title(self):
        """Test extracting page title."""
        html = "<html><head><title>My Test Page</title></head><body></body></html>"
        title = extract_title(html)
        self.assertEqual(title, "My Test Page")
    
    def test_extract_title_missing(self):
        """Test extracting title when none exists."""
        html = "<html><body>No title</body></html>"
        title = extract_title(html)
        self.assertIsNone(title)
    
    def test_extract_meta(self):
        """Test extracting meta tags."""
        html = """
        <html>
            <head>
                <meta name="description" content="Page description">
                <meta property="og:title" content="Open Graph Title">
                <meta name="keywords" content="test, html, utils">
            </head>
        </html>
        """
        desc = extract_meta(html, name="description")
        self.assertEqual(desc, "Page description")
        
        og_title = extract_meta(html, property="og:title")
        self.assertEqual(og_title, "Open Graph Title")
    
    def test_count_tags(self):
        """Test counting tag occurrences."""
        html = "<div><p>Para 1</p><p>Para 2</p><span>Text</span></div>"
        counts = count_tags(html)
        self.assertEqual(counts.get("p", 0), 2)
        self.assertEqual(counts.get("div", 0), 1)
        self.assertEqual(counts.get("span", 0), 1)


class TestSanitizeHTML(unittest.TestCase):
    """Tests for HTML sanitization."""
    
    def test_remove_script_tags(self):
        """Test removing script tags."""
        html = "<p>Safe</p><script>alert('XSS')</script><p>Also safe</p>"
        sanitized = sanitize_html(html)
        self.assertNotIn("<script>", sanitized)
        self.assertNotIn("alert", sanitized)
        self.assertIn("Safe", sanitized)
    
    def test_remove_event_handlers(self):
        """Test removing event handler attributes."""
        html = '<button onclick="alert(1)" onmouseover="evil()">Click</button>'
        sanitized = sanitize_html(html)
        self.assertNotIn("onclick", sanitized)
        self.assertNotIn("onmouseover", sanitized)
    
    def test_remove_javascript_urls(self):
        """Test removing javascript: URLs."""
        html = '<a href="javascript:alert(1)">Click</a>'
        sanitized = sanitize_html(html)
        self.assertNotIn("javascript:", sanitized)
    
    def test_preserve_safe_tags(self):
        """Test preserving safe tags."""
        html = "<p><strong>Bold</strong> and <em>italic</em> text</p>"
        sanitized = sanitize_html(html)
        self.assertIn("<strong>", sanitized)
        self.assertIn("<em>", sanitized)
    
    def test_custom_allowed_tags(self):
        """Test with custom allowed tags."""
        html = "<div><script>bad</script><p>good</p></div>"
        sanitized = sanitize_html(html, allowed_tags={"p", "div"})
        self.assertNotIn("<script>", sanitized)
        self.assertIn("<p>", sanitized)
    
    def test_remove_style_tags(self):
        """Test removing style tags."""
        html = "<style>.bad { color: red; }</style><p>Content</p>"
        sanitized = sanitize_html(html)
        self.assertNotIn("<style>", sanitized)


class TestHTMLToText(unittest.TestCase):
    """Tests for HTML to text conversion."""
    
    def test_simple_conversion(self):
        """Test simple HTML to text conversion."""
        html = "<p>Hello World</p>"
        text = html_to_text(html)
        self.assertEqual(text, "Hello World")
    
    def test_nested_elements(self):
        """Test conversion with nested elements."""
        html = "<div><p>Paragraph 1</p><p>Paragraph 2</p></div>"
        text = html_to_text(html)
        self.assertIn("Paragraph 1", text)
        self.assertIn("Paragraph 2", text)
    
    def test_preserve_line_breaks(self):
        """Test that line breaks are preserved."""
        html = "<p>Line 1</p><p>Line 2</p>"
        text = html_to_text(html)
        self.assertIn("\n", text)
    
    def test_remove_comments(self):
        """Test that comments are removed."""
        html = "<p>Visible<!-- hidden comment -->text</p>"
        text = html_to_text(html)
        self.assertNotIn("comment", text)
        self.assertIn("Visible", text)
        self.assertIn("text", text)


class TestHTMLGeneration(unittest.TestCase):
    """Tests for HTML generation functions."""
    
    def test_generate_tag_basic(self):
        """Test basic tag generation."""
        html = generate_tag("p", "Hello World")
        self.assertEqual(html, "<p>Hello World</p>")
    
    def test_generate_tag_with_attributes(self):
        """Test tag generation with attributes."""
        html = generate_tag("a", "Link", {"href": "https://example.com", "target": "_blank"})
        self.assertIn('href="https://example.com"', html)
        self.assertIn('target="_blank"', html)
    
    def test_generate_tag_self_closing(self):
        """Test self-closing tag generation."""
        html = generate_tag("br", self_closing=True)
        self.assertEqual(html, "<br>")
    
    def test_generate_link(self):
        """Test link generation."""
        html = generate_link("https://example.com", "Example", title="Example Site")
        self.assertIn('href="https://example.com"', html)
        self.assertIn("Example", html)
        self.assertIn('title="Example Site"', html)
    
    def test_generate_image(self):
        """Test image tag generation."""
        html = generate_image("test.jpg", alt="Test Image", width=100, height=200)
        self.assertIn('src="test.jpg"', html)
        self.assertIn('alt="Test Image"', html)
        self.assertIn('width="100"', html)
        self.assertIn('height="200"', html)
    
    def test_generate_table(self):
        """Test table generation."""
        headers = ["Name", "Age", "City"]
        rows = [
            ["Alice", "30", "New York"],
            ["Bob", "25", "London"]
        ]
        html = generate_table(headers, rows)
        self.assertIn("<table>", html)
        self.assertIn("<th>Name</th>", html)
        self.assertIn("<td>Alice</td>", html)
        self.assertIn("<td>London</td>", html)
    
    def test_generate_form_basic(self):
        """Test basic form generation."""
        html = generate_form("/submit", method="post")
        self.assertIn('<form action="/submit" method="post">', html)
    
    def test_generate_form_with_fields(self):
        """Test form generation with fields."""
        fields = [
            {"type": "text", "name": "username", "label": "Username"},
            {"type": "password", "name": "password", "label": "Password"},
            {"type": "submit", "name": "submit", "value": "Login"}
        ]
        html = generate_form("/login", method="post", fields=fields)
        self.assertIn('name="username"', html)
        self.assertIn('name="password"', html)
        self.assertIn('type="password"', html)


class TestHTMLFormatting(unittest.TestCase):
    """Tests for HTML formatting functions."""
    
    def test_minify_html(self):
        """Test HTML minification."""
        html = """
        <div>
            <p>Hello World</p>
        </div>
        """
        minified = minify_html(html)
        self.assertNotIn("\n", minified)
        self.assertIn("<div>", minified)
        self.assertIn("<p>Hello World</p>", minified)
    
    def test_minify_removes_comments(self):
        """Test that minification removes comments."""
        html = "<div><!-- comment --><p>Content</p></div>"
        minified = minify_html(html)
        self.assertNotIn("<!--", minified)
    
    def test_prettify_html(self):
        """Test HTML prettification."""
        html = "<div><p>Para 1</p><p>Para 2</p></div>"
        pretty = prettify_html(html)
        self.assertIn("\n", pretty)
        # Check indentation
        self.assertIn("  ", pretty)
    
    def test_prettify_nested(self):
        """Test prettifying nested elements."""
        html = "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        pretty = prettify_html(html)
        self.assertIn("<ul>", pretty)
        self.assertIn("<li>", pretty)


class TestValidation(unittest.TestCase):
    """Tests for HTML validation."""
    
    def test_validate_valid_html(self):
        """Test validating valid HTML."""
        html = "<html><head><title>Test</title></head><body><p>Content</p></body></html>"
        result = validate_html_structure(html)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["issues"]), 0)
    
    def test_validate_gets_depth(self):
        """Test that validation returns depth."""
        html = "<div><p><span>Text</span></p></div>"
        result = validate_html_structure(html)
        self.assertGreater(result["depth"], 0)
    
    def test_validate_counts_tags(self):
        """Test that validation counts tags."""
        html = "<div><p>1</p><p>2</p></div>"
        result = validate_html_structure(html)
        self.assertGreater(result["tag_count"], 0)
    
    def test_get_dom_depth(self):
        """Test DOM depth calculation."""
        html = "<div><p><span><a>Link</a></span></p></div>"
        root = parse_html(html)
        depth = get_dom_depth(root)
        self.assertGreaterEqual(depth, 4)  # div > p > span > a


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_empty_html(self):
        """Test parsing empty HTML."""
        root = parse_html("")
        self.assertIsNotNone(root)
        self.assertEqual(root.tag, "root")
    
    def test_whitespace_only(self):
        """Test parsing whitespace-only HTML."""
        root = parse_html("   \n\t  ")
        self.assertIsNotNone(root)
    
    def test_malformed_html(self):
        """Test parsing malformed HTML (parser should be forgiving)."""
        html = "<div><p>Unclosed"
        root = parse_html(html)
        self.assertIsNotNone(root)
    
    def test_unicode_content(self):
        """Test handling Unicode content."""
        html = "<p>Hello 世界 🌍 Привет</p>"
        root = parse_html(html)
        text = root.get_text()
        self.assertIn("世界", text)
        self.assertIn("🌍", text)
        self.assertIn("Привет", text)
    
    def test_special_characters(self):
        """Test handling special characters."""
        html = "<p>&lt;script&gt; &amp; &quot;quoted&quot;</p>"
        root = parse_html(html)
        text = root.get_text()
        self.assertIn("<", text)
        self.assertIn("&", text)
    
    def test_very_long_text(self):
        """Test handling very long text content."""
        long_text = "A" * 10000
        html = f"<p>{long_text}</p>"
        root = parse_html(html)
        text = root.get_text()
        self.assertEqual(len(text), 10000)
    
    def test_deeply_nested(self):
        """Test handling deeply nested elements."""
        html = "<div>" * 100 + "Content" + "</div>" * 100
        root = parse_html(html)
        depth = get_dom_depth(root)
        self.assertEqual(depth, 101)  # 100 divs + root element
    
    def test_many_attributes(self):
        """Test element with many attributes."""
        attrs = " ".join([f'data-{i}="value{i}"' for i in range(50)])
        html = f"<div {attrs}>Content</div>"
        root = parse_html(html)
        divs = find_elements(root, tag="div")
        self.assertEqual(len(divs), 1)
        self.assertEqual(len(divs[0].attributes), 50)


class TestRealWorldHTML(unittest.TestCase):
    """Tests with real-world HTML snippets."""
    
    def test_blog_post_html(self):
        """Test parsing blog post HTML."""
        html = """
        <article>
            <header>
                <h1>Blog Post Title</h1>
                <time datetime="2024-01-15">January 15, 2024</time>
            </header>
            <div class="content">
                <p>First paragraph of the blog post.</p>
                <p>Second paragraph with <a href="https://example.com">a link</a>.</p>
                <img src="image.jpg" alt="Blog image">
            </div>
            <footer>
                <span class="author">By Author Name</span>
            </footer>
        </article>
        """
        root = parse_html(html)
        
        # Extract title
        titles = find_elements(root, tag="h1")
        self.assertEqual(len(titles), 1)
        self.assertIn("Blog Post Title", titles[0].get_text())
        
        # Extract links
        links = extract_links(html)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["href"], "https://example.com")
        
        # Extract images
        images = extract_images(html)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]["src"], "image.jpg")
    
    def test_navigation_html(self):
        """Test parsing navigation HTML."""
        html = """
        <nav class="main-nav">
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
        </nav>
        """
        root = parse_html(html)
        
        navs = find_by_class(root, "main-nav")
        self.assertEqual(len(navs), 1)
        
        links = find_elements(root, tag="a")
        self.assertEqual(len(links), 3)
    
    def test_form_html(self):
        """Test parsing form HTML."""
        html = """
        <form action="/submit" method="post" class="contact-form">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
            
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
            
            <label for="message">Message:</label>
            <textarea id="message" name="message"></textarea>
            
            <button type="submit">Send</button>
        </form>
        """
        root = parse_html(html)
        
        forms = find_elements(root, tag="form")
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0].get_attribute("action"), "/submit")
        
        inputs = find_elements(root, tag="input")
        self.assertEqual(len(inputs), 2)


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestHTMLElement,
        TestHTMLParser,
        TestFindElements,
        TestExtractData,
        TestSanitizeHTML,
        TestHTMLToText,
        TestHTMLGeneration,
        TestHTMLFormatting,
        TestValidation,
        TestEdgeCases,
        TestRealWorldHTML
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("=" * 70)
    print("AllToolkit - HTML Utilities Test Suite")
    print("=" * 70)
    print()
    
    result = run_tests()
    
    print()
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
