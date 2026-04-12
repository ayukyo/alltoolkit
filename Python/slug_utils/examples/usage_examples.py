#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Slug Utils Usage Examples

Demonstration of various slug generation scenarios and best practices.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    slugify, unicode_to_ascii, slugify_cn, slugify_jp, slugify_kr,
    slugify_title, slugify_filename, slugify_username, slugify_url,
    slugify_batch, slugify_dict, is_valid_slug, suggest_slug,
    count_words_in_slug, truncate_slug
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def print_example(description, code, result):
    """Print an example with description, code, and result."""
    print(f"\n{description}")
    print(f"  Code: {code}")
    print(f"  Result: {result}")


# =============================================================================
# Basic Usage Examples
# =============================================================================

def basic_examples():
    """Demonstrate basic slug generation."""
    print_section("Basic Usage Examples")
    
    print_example(
        "Simple text slugification",
        'slugify("Hello World")',
        slugify("Hello World")
    )
    
    print_example(
        "Text with punctuation",
        'slugify("Hello, World!")',
        slugify("Hello, World!")
    )
    
    print_example(
        "Text with extra whitespace",
        'slugify("  Hello   World  ")',
        slugify("  Hello   World  ")
    )
    
    print_example(
        "Custom separator (underscore)",
        'slugify("Hello World", separator="_")',
        slugify("Hello World", separator="_")
    )
    
    print_example(
        "Preserve case",
        'slugify("Hello World", lowercase=False)',
        slugify("Hello World", lowercase=False)
    )


# =============================================================================
# Unicode and Accent Examples
# =============================================================================

def unicode_examples():
    """Demonstrate unicode and accent handling."""
    print_section("Unicode and Accent Examples")
    
    print_example(
        "French accents",
        'slugify("Café Résumé")',
        slugify("Café Résumé")
    )
    
    print_example(
        "German umlauts",
        'slugify("Über Größe")',
        slugify("Über Größe")
    )
    
    print_example(
        "Spanish tilde",
        'slugify("Niño España")',
        slugify("Niño España")
    )
    
    print_example(
        "Currency symbols",
        'slugify("Price: $100 €50 £30")',
        slugify("Price: $100 €50 £30")
    )
    
    print_example(
        "Ampersand replacement",
        'slugify("Tom & Jerry")',
        slugify("Tom & Jerry")
    )
    
    print_example(
        "Direct unicode to ASCII",
        'unicode_to_ascii("Naïve Café")',
        unicode_to_ascii("Naïve Café")
    )


# =============================================================================
# Stop Words and Replacements
# =============================================================================

def stop_words_examples():
    """Demonstrate stop word removal and word replacements."""
    print_section("Stop Words and Replacements")
    
    print_example(
        "Remove common stop words",
        'slugify("The Quick Brown Fox", remove_stop_words=True)',
        slugify("The Quick Brown Fox", remove_stop_words=True)
    )
    
    print_example(
        "Remove stops from article title",
        'slugify("The Lord of the Rings", remove_stop_words=True)',
        slugify("The Lord of the Rings", remove_stop_words=True)
    )
    
    print_example(
        "Custom stop words",
        'slugify("Hello World Foo Bar", remove_stop_words=True, stop_words={"foo", "bar"})',
        slugify("Hello World Foo Bar", remove_stop_words=True, stop_words={"foo", "bar"})
    )
    
    print_example(
        "Custom word replacements",
        'slugify("Python & JavaScript", word_replacements={"python": "py", "javascript": "js"})',
        slugify("Python & JavaScript", word_replacements={"python": "py", "javascript": "js"})
    )


# =============================================================================
# Length and Truncation
# =============================================================================

def length_examples():
    """Demonstrate max length and truncation."""
    print_section("Length and Truncation Examples")
    
    long_title = "A Very Long Title That Exceeds The Maximum Length We Want To Set"
    
    print_example(
        "Basic truncation",
        f'slugify("{long_title}", max_length=20)',
        slugify(long_title, max_length=20)
    )
    
    print_example(
        "Truncate at word boundary",
        f'slugify("{long_title}", max_length=20, truncate_words=True)',
        slugify(long_title, max_length=20, truncate_words=True)
    )
    
    print_example(
        "SEO-friendly title slug (max 60 chars)",
        'slugify_title("10 Best Practices for Python Development in 2024!", max_length=60)',
        slugify_title("10 Best Practices for Python Development in 2024!", max_length=60)
    )


# =============================================================================
# Specialized Functions
# =============================================================================

def specialized_examples():
    """Demonstrate specialized slug functions."""
    print_section("Specialized Function Examples")
    
    # Title slugs
    print("\n--- Title Slugs ---")
    print_example(
        "Blog post title",
        'slugify_title("How to Build a REST API with Python")',
        slugify_title("How to Build a REST API with Python")
    )
    
    print_example(
        "Article with special chars",
        'slugify_title("What is C++? A Beginner\'s Guide!")',
        slugify_title("What is C++? A Beginner's Guide!")
    )
    
    # Filename slugs
    print("\n--- Filename Slugs ---")
    print_example(
        "Document with version",
        'slugify_filename("Quarterly Report Q4 2024 (Final v2).pdf")',
        slugify_filename("Quarterly Report Q4 2024 (Final v2).pdf")
    )
    
    print_example(
        "Image file",
        'slugify_filename("IMG_20240115_143022.jpg")',
        slugify_filename("IMG_20240115_143022.jpg")
    )
    
    # Username slugs
    print("\n--- Username Slugs ---")
    print_example(
        "Email-style username",
        'slugify_username("john.doe@example.com")',
        slugify_username("john.doe@example.com")
    )
    
    print_example(
        "Username with special chars",
        'slugify_username("User_2024!")',
        slugify_username("User_2024!")
    )
    
    # URL slugs
    print("\n--- URL Slugs ---")
    print_example(
        "Blog post URL",
        'slugify_url("https://example.com/blog/my-awesome-post")',
        slugify_url("https://example.com/blog/my-awesome-post")
    )
    
    print_example(
        "URL with query params",
        'slugify_url("https://example.com/products?category=electronics&sort=price")',
        slugify_url("https://example.com/products?category=electronics&sort=price")
    )
    
    print_example(
        "URL with domain",
        'slugify_url("https://medium.com/article", keep_domain=True)',
        slugify_url("https://medium.com/article", keep_domain=True)
    )


# =============================================================================
# Multi-language Examples
# =============================================================================

def multilingual_examples():
    """Demonstrate multi-language slug generation."""
    print_section("Multi-language Examples")
    
    # Chinese
    print("\n--- Chinese (拼音) ---")
    print_example(
        "Beijing",
        'slugify_cn("北京")',
        slugify_cn("北京")
    )
    
    print_example(
        "Shanghai",
        'slugify_cn("上海")',
        slugify_cn("上海")
    )
    
    print_example(
        "Mixed Chinese and English",
        'slugify_cn("北京 Beijing")',
        slugify_cn("北京 Beijing")
    )
    
    # Japanese
    print("\n--- Japanese (ローマ字) ---")
    print_example(
        "Vowels",
        'slugify_jp("あいうえお")',
        slugify_jp("あいうえお")
    )
    
    print_example(
        "Greeting",
        'slugify_jp("こんにちは")',
        slugify_jp("こんにちは")
    )
    
    # Korean
    print("\n--- Korean (로마자) ---")
    print_example(
        "Greeting",
        'slugify_kr("안녕하세요")',
        slugify_kr("안녕하세요")
    )
    
    print_example(
        "Korea",
        'slugify_kr("한국")',
        slugify_kr("한국")
    )


# =============================================================================
# Batch Processing Examples
# =============================================================================

def batch_examples():
    """Demonstrate batch processing."""
    print_section("Batch Processing Examples")
    
    # Batch slugify
    print("\n--- Batch Slugify ---")
    texts = ["Hello World", "Hello World", "Foo Bar", "Foo Bar", "Test"]
    slugs = slugify_batch(texts, ensure_unique=True)
    
    print("Input texts:", texts)
    print("Output slugs (unique):", slugs)
    
    # Batch without uniqueness
    slugs_no_unique = slugify_batch(texts, ensure_unique=False)
    print("Output slugs (not unique):", slugs_no_unique)
    
    # Dict slugify
    print("\n--- Dict Slugify ---")
    data = {
        "title": "My Blog Post",
        "author": "John Doe",
        "category": "Technology",
        "views": 1000  # Non-string value preserved
    }
    
    result = slugify_dict(data)
    print(f"Input: {data}")
    print(f"Output: {result}")
    
    # Dict with specific keys
    result_keys = slugify_dict(data, keys=["title", "author"])
    print(f"Output (keys=title,author): {result_keys}")


# =============================================================================
# Validation Examples
# =============================================================================

def validation_examples():
    """Demonstrate validation and utilities."""
    print_section("Validation and Utility Examples")
    
    # Validation
    print("\n--- Slug Validation ---")
    test_slugs = [
        "hello-world",
        "Hello_World",
        "hello_world",
        "-invalid-",
        "valid-123",
        "a",
        ""
    ]
    
    print("Testing various slugs:")
    for slug in test_slugs:
        is_valid = is_valid_slug(slug, allow_underscores=True)
        status = "✓" if is_valid else "✗"
        print(f"  {status} '{slug}' -> valid={is_valid}")
    
    # Suggest unique slug
    print("\n--- Suggest Unique Slug ---")
    existing = ["my-post", "my-post-1", "my-post-2"]
    suggestion = suggest_slug("My Post", existing)
    print(f"Existing: {existing}")
    print(f"Suggested for 'My Post': {suggestion}")
    
    # Count words
    print("\n--- Count Words in Slug ---")
    test_cases = [
        "hello-world-foo-bar",
        "a-b-c-d-e-f",
        "single",
        ""
    ]
    for slug in test_cases:
        count = count_words_in_slug(slug)
        print(f"  '{slug}' -> {count} words")
    
    # Truncate slug
    print("\n--- Truncate Slug ---")
    long_slug = "this-is-a-very-long-slug-with-many-words"
    print(f"Original: {long_slug}")
    print(f"Truncated to 15 (preserve words): {truncate_slug(long_slug, 15)}")
    print(f"Truncated to 15 (no preserve): {truncate_slug(long_slug, 15, preserve_words=False)}")


# =============================================================================
# Real-world Scenarios
# =============================================================================

def real_world_examples():
    """Demonstrate real-world usage scenarios."""
    print_section("Real-world Usage Scenarios")
    
    # Blog system
    print("\n--- Blog Post URL Generation ---")
    
    def create_post_url(title, base_path="/blog"):
        """Create SEO-friendly URL for a blog post."""
        slug = slugify_title(title, max_length=60)
        return f"{base_path}/{slug}"
    
    titles = [
        "10 Best Practices for Python Development in 2024",
        "How to Build a REST API: A Complete Guide",
        "What is Machine Learning? (Beginner's Guide)",
        "C++ vs Python: Which Should You Learn?"
    ]
    
    for title in titles:
        url = create_post_url(title)
        print(f"  {title[:40]}...")
        print(f"    → {url}")
    
    # File upload system
    print("\n--- Safe Filename Generation ---")
    
    def safe_upload_filename(original_name, user_id):
        """Generate safe filename for uploaded file."""
        slug = slugify_filename(original_name)
        name, ext = slug.rsplit('.', 1) if '.' in slug else (slug, '')
        timestamp = "20240412"  # In real app, use datetime
        return f"{name}_{user_id}_{timestamp}.{ext}" if ext else f"{name}_{user_id}_{timestamp}"
    
    uploads = [
        ("My Resume (Final).pdf", "user123"),
        ("Photo from Vacation 2024.jpg", "user456"),
        ("Project Proposal v3.2.docx", "user789"),
    ]
    
    for filename, user_id in uploads:
        safe_name = safe_upload_filename(filename, user_id)
        print(f"  {filename} → {safe_name}")
    
    # User registration
    print("\n--- Username Normalization ---")
    
    def normalize_username(desired, existing_users):
        """Suggest unique username for registration."""
        base = slugify_username(desired)
        return suggest_slug(base, existing_users)
    
    existing = ["john_doe", "john_doe_1", "admin", "test_user"]
    registrations = ["John.Doe", "john.doe", "Admin!", "New User"]
    
    for desired in registrations:
        suggested = normalize_username(desired, existing)
        print(f"  Desired: {desired:15} → Suggested: {suggested}")
    
    # Content management
    print("\n--- Content Management System ---")
    
    articles = [
        {"title": "Introduction to AI", "lang": "en"},
        {"title": "人工智能入门", "lang": "zh"},
        {"title": "AI 入門", "lang": "jp"},
        {"title": "AI 입문", "lang": "kr"},
    ]
    
    for article in articles:
        if article["lang"] == "zh":
            slug = slugify_cn(article["title"])
        elif article["lang"] == "jp":
            slug = slugify_jp(article["title"])
        elif article["lang"] == "kr":
            slug = slugify_kr(article["title"])
        else:
            slug = slugify_title(article["title"])
        
        print(f"  [{article['lang']}] {article['title']} → /articles/{slug}")


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("  AllToolkit - Slug Utils Usage Examples")
    print("  Comprehensive demonstrations of slug generation")
    print("="*70)
    
    basic_examples()
    unicode_examples()
    stop_words_examples()
    length_examples()
    specialized_examples()
    multilingual_examples()
    batch_examples()
    validation_examples()
    real_world_examples()
    
    print("\n" + "="*70)
    print("  Examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
