"""
Tests for BBCode Utilities

Comprehensive tests for BBCode parsing, conversion, and validation.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bbcode_utils.bbcode_utils import (
    BBCodeParser, BBCodeNode, BBCodeNodeType,
    parse, to_html, to_text, validate,
    get_supported_tags, create_safe_parser, bbcode
)


def test_basic_formatting():
    """Test basic formatting tags"""
    print("Testing basic formatting tags...")
    
    # Bold
    html = to_html("[b]bold text[/b]")
    assert html == "<strong>bold text</strong>", f"Bold failed: {html}"
    
    # Italic
    html = to_html("[i]italic text[/i]")
    assert html == "<em>italic text</em>", f"Italic failed: {html}"
    
    # Underline
    html = to_html("[u]underlined[/u]")
    assert html == "<u>underlined</u>", f"Underline failed: {html}"
    
    # Strikethrough
    html = to_html("[s]strikethrough[/s]")
    assert html == "<del>strikethrough</del>", f"Strikethrough failed: {html}"
    
    print("  ✓ Basic formatting tags passed")


def test_nested_tags():
    """Test nested tag parsing"""
    print("Testing nested tags...")
    
    html = to_html("[b]Bold [i]and italic[/i][/b]")
    assert html == "<strong>Bold <em>and italic</em></strong>", f"Nested failed: {html}"
    
    html = to_html("[b][i][u]All three[/u][/i][/b]")
    assert html == "<strong><em><u>All three</u></em></strong>", f"Deep nested failed: {html}"
    
    print("  ✓ Nested tags passed")


def test_url_tag():
    """Test URL tag with attribute"""
    print("Testing URL tag...")
    
    html = to_html("[url=https://example.com]Click here[/url]")
    assert html == '<a href="https://example.com">Click here</a>', f"URL with attr failed: {html}"
    
    html = to_html("[url]https://example.com[/url]")
    assert "https://example.com" in html, f"URL without attr failed: {html}"
    
    print("  ✓ URL tag passed")


def test_img_tag():
    """Test image tag"""
    print("Testing image tag...")
    
    html = to_html("[img]https://example.com/image.png[/img]")
    assert "img" in html.lower(), f"Image tag failed: {html}"
    assert "example.com/image.png" in html, f"Image URL not in output: {html}"
    
    print("  ✓ Image tag passed")


def test_quote_tag():
    """Test quote tag"""
    print("Testing quote tag...")
    
    html = to_html("[quote]This is a quote[/quote]")
    assert "blockquote" in html, f"Quote failed: {html}"
    assert "This is a quote" in html, f"Quote content missing: {html}"
    
    print("  ✓ Quote tag passed")


def test_code_tag():
    """Test code tag"""
    print("Testing code tag...")
    
    html = to_html("[code]print('hello')[/code]")
    assert "pre" in html and "code" in html, f"Code failed: {html}"
    # Note: quotes are escaped to HTML entities
    assert "print" in html and "hello" in html, f"Code content missing: {html}"
    
    print("  ✓ Code tag passed")


def test_lists():
    """Test list tags"""
    print("Testing list tags...")
    
    html = to_html("[list][*]Item 1[*]Item 2[/list]")
    assert "<ul>" in html, f"UL list failed: {html}"
    assert "<li>Item 1</li>" in html, f"List items failed: {html}"
    
    html = to_html("[olist][*]First[*]Second[/olist]")
    assert "<ol>" in html, f"OL list failed: {html}"
    
    print("  ✓ List tags passed")


def test_color_and_size():
    """Test color and size tags"""
    print("Testing color and size tags...")
    
    html = to_html("[color=red]Red text[/color]")
    assert "color:red" in html or "color: red" in html, f"Color failed: {html}"
    assert "Red text" in html, f"Color content missing: {html}"
    
    html = to_html("[size=24]Large text[/size]")
    assert "font-size:24" in html, f"Size failed: {html}"
    
    print("  ✓ Color and size tags passed")


def test_tables():
    """Test table tags"""
    print("Testing table tags...")
    
    bbcode = "[table][tr][th]Header[/th][/tr][tr][td]Cell[/td][/tr][/table]"
    html = to_html(bbcode)
    assert "<table>" in html, f"Table failed: {html}"
    assert "<th>Header</th>" in html, f"Table header failed: {html}"
    assert "<td>Cell</td>" in html, f"Table cell failed: {html}"
    
    print("  ✓ Table tags passed")


def test_alignment():
    """Test alignment tags"""
    print("Testing alignment tags...")
    
    html = to_html("[center]Centered[/center]")
    assert "text-align:center" in html, f"Center failed: {html}"
    
    html = to_html("[left]Left aligned[/left]")
    assert "text-align:left" in html, f"Left align failed: {html}"
    
    html = to_html("[right]Right aligned[/right]")
    assert "text-align:right" in html, f"Right align failed: {html}"
    
    print("  ✓ Alignment tags passed")


def test_self_closing_tags():
    """Test self-closing tags"""
    print("Testing self-closing tags...")
    
    html = to_html("Line 1[br]Line 2")
    assert "<br>" in html, f"BR failed: {html}"
    
    html = to_html("Before[hr]After")
    assert "<hr>" in html, f"HR failed: {html}"
    
    print("  ✓ Self-closing tags passed")


def test_subscript_superscript():
    """Test subscript and superscript"""
    print("Testing subscript and superscript...")
    
    html = to_html("H[sub]2[/sub]O")
    assert "<sub>2</sub>" in html, f"Subscript failed: {html}"
    
    html = to_html("E=mc[sup]2[/sup]")
    assert "<sup>2</sup>" in html, f"Superscript failed: {html}"
    
    print("  ✓ Subscript and superscript passed")


def test_email_tag():
    """Test email tag"""
    print("Testing email tag...")
    
    html = to_html("[email=user@example.com]Send email[/email]")
    assert "mailto:user@example.com" in html, f"Email failed: {html}"
    assert "Send email" in html, f"Email text missing: {html}"
    
    print("  ✓ Email tag passed")


def test_to_text():
    """Test plain text extraction"""
    print("Testing plain text extraction...")
    
    text = to_text("[b]Bold[/b] and [i]italic[/i]")
    assert text == "Bold and italic", f"Plain text extraction failed: {text}"
    
    text = to_text("[url=https://example.com]Click here[/url]")
    assert text == "Click here", f"URL plain text failed: {text}"
    
    text = to_text("Line 1[br]Line 2")
    assert "\n" in text, f"BR plain text failed: {text}"
    
    print("  ✓ Plain text extraction passed")


def test_validation():
    """Test BBCode validation"""
    print("Testing BBCode validation...")
    
    # Valid BBCode
    valid, errors = validate("[b]Bold[/b]")
    assert valid, f"Validation failed for valid BBCode: {errors}"
    
    # Unclosed tag
    valid, errors = validate("[b]Unclosed")
    assert not valid, "Should detect unclosed tag"
    assert "Unclosed tag" in errors[0], f"Wrong error: {errors}"
    
    # Mismatched tags
    valid, errors = validate("[b][i]Mismatched[/b][/i]")
    assert not valid, "Should detect mismatched tags"
    
    print("  ✓ Validation passed")


def test_safe_parser():
    """Test safe parser (no URLs/images)"""
    print("Testing safe parser...")
    
    parser = create_safe_parser()
    
    # Safe tags should work
    html = parser.to_html(parser.parse("[b]Bold[/b]"))
    assert "<strong>" in html, f"Safe bold failed: {html}"
    
    # URL should be stripped
    html = parser.to_html(parser.parse("[url=https://evil.com]Click[/url]"))
    assert "<a" not in html, f"URL should be stripped: {html}"
    
    print("  ✓ Safe parser passed")


def test_unknown_tag_handling():
    """Test handling of unknown tags"""
    print("Testing unknown tag handling...")
    
    # Unknown tags should be stripped by default
    html = to_html("[unknowntag]Content[/unknowntag]")
    assert "Content" in html, f"Content should be preserved: {html}"
    assert "unknowntag" not in html.lower(), f"Unknown tag should be stripped: {html}"
    
    print("  ✓ Unknown tag handling passed")


def test_special_characters():
    """Test HTML special characters are escaped"""
    print("Testing special character escaping...")
    
    html = to_html("[b]<script>alert('xss')</script>[/b]")
    assert "&lt;script&gt;" in html, f"HTML not escaped: {html}"
    assert "<script>" not in html, f"Script tag not escaped: {html}"
    
    print("  ✓ Special character escaping passed")


def test_complex_document():
    """Test complex BBCode document"""
    print("Testing complex document...")
    
    bbcode = """
[b]Title[/b]
[quote=Someone]
This is a [i]quote[/i] with [b]nested formatting[/b].
[/quote]
[list]
[*]Item 1
[*]Item 2 with [url=https://example.com]link[/url]
[/list]
[code]
def hello():
    print("Hello, World!")
[/code]
"""
    
    parser = BBCodeParser()
    ast = parser.parse(bbcode)
    html = parser.to_html(ast)
    text = parser.to_text(ast)
    
    assert "<strong>Title</strong>" in html, "Title not in HTML"
    assert "<blockquote>" in html, "Quote not in HTML"
    assert "<ul>" in html, "List not in HTML"
    assert "<pre><code>" in html, "Code not in HTML"
    assert "Title" in text, "Title not in plain text"
    
    print("  ✓ Complex document passed")


def test_ast_structure():
    """Test AST structure generation"""
    print("Testing AST structure...")
    
    ast = parse("[b]Test[/b]")
    
    assert ast.type == BBCodeNodeType.TAG, "Root should be a tag node"
    assert ast.tag_name == "root", "Root tag name should be 'root'"
    assert len(ast.children) == 1, "Root should have one child"
    
    bold_node = ast.children[0]
    assert bold_node.type == BBCodeNodeType.TAG, "Child should be a tag node"
    assert bold_node.tag_name == "b", "Child tag should be 'b'"
    assert len(bold_node.children) == 1, "Bold should have one child"
    
    text_node = bold_node.children[0]
    assert text_node.type == BBCodeNodeType.TEXT, "Should be a text node"
    assert text_node.content == "Test", f"Text content wrong: {text_node.content}"
    
    print("  ✓ AST structure passed")


def test_custom_handler():
    """Test custom tag handlers"""
    print("Testing custom tag handlers...")
    
    parser = BBCodeParser()
    
    def spoiler_handler(content, attrs, children):
        return f'<div class="spoiler" data-reveal="true">{content}</div>'
    
    parser.register_handler("spoiler", spoiler_handler)
    
    ast = parser.parse("[spoiler]Hidden content[/spoiler]")
    html = parser.to_html(ast)
    
    assert "spoiler" in html, f"Custom handler failed: {html}"
    assert "Hidden content" in html, f"Content missing: {html}"
    
    print("  ✓ Custom handler passed")


def test_convenience_function():
    """Test the bbcode() convenience function"""
    print("Testing convenience function...")
    
    result = bbcode("[b]test[/b]", "html")
    assert "<strong>test</strong>" in result, f"HTML output failed: {result}"
    
    result = bbcode("[b]test[/b]", "text")
    assert result == "test", f"Text output failed: {result}"
    
    result = bbcode("[b]test[/b]", "ast")
    assert '"type": "tag"' in result, f"AST output failed: {result}"
    
    print("  ✓ Convenience function passed")


def test_get_supported_tags():
    """Test get_supported_tags function"""
    print("Testing get_supported_tags...")
    
    tags = get_supported_tags()
    assert isinstance(tags, dict), "Should return a dictionary"
    assert "b" in tags, "Should include 'b' tag"
    assert "url" in tags, "Should include 'url' tag"
    assert "html" in tags["b"], "Tag config should include html template"
    
    print("  ✓ get_supported_tags passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("BBCode Utils Test Suite")
    print("="*50 + "\n")
    
    tests = [
        test_basic_formatting,
        test_nested_tags,
        test_url_tag,
        test_img_tag,
        test_quote_tag,
        test_code_tag,
        test_lists,
        test_color_and_size,
        test_tables,
        test_alignment,
        test_self_closing_tags,
        test_subscript_superscript,
        test_email_tag,
        test_to_text,
        test_validation,
        test_safe_parser,
        test_unknown_tag_handling,
        test_special_characters,
        test_complex_document,
        test_ast_structure,
        test_custom_handler,
        test_convenience_function,
        test_get_supported_tags,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*50 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)