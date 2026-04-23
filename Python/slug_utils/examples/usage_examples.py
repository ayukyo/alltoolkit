#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Slug Utilities Examples
=====================================
Practical examples for using the slug_utils module.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from slug_utils.mod import (
    generate_slug,
    generate_unique_slug,
    generate_sequential_slug,
    generate_date_slug,
    generate_category_slug,
    generate_hierarchical_slug,
    generate_slug_batch,
    slug_from_filename,
    is_valid_slug,
    fix_slug,
    slug_to_text,
    SlugGenerator,
)


def example_basic_slugs():
    """Basic slug generation examples."""
    print("\n" + "=" * 50)
    print("Basic Slug Generation")
    print("=" * 50)
    
    titles = [
        "Hello World",
        "This is a Blog Post!",
        "Héllo Wörld Café",
        "2024 Annual Report",
        "Price: $99.99 Only",
        "Tech & Innovation Summit",
    ]
    
    for title in titles:
        slug = generate_slug(title)
        print(f"  '{title}' → '{slug}'")


def example_custom_separator():
    """Custom separator examples."""
    print("\n" + "=" * 50)
    print("Custom Separators")
    print("=" * 50)
    
    title = "My Awesome Blog Post"
    
    print(f"  Default (-): '{generate_slug(title)}'")
    print(f"  Underscore (_): '{generate_slug(title, separator='_')}'")
    print(f"  Dot (.): '{generate_slug(title, separator='.')}'")
    print(f"  None: '{generate_slug(title, separator='')}'")


def example_max_length():
    """Maximum length examples."""
    print("\n" + "=" * 50)
    print("Maximum Length Constraints")
    print("=" * 50)
    
    title = "This is a very long title that needs to be shortened"
    
    for max_len in [10, 20, 30, 50]:
        slug = generate_slug(title, max_length=max_len)
        print(f"  Max {max_len}: '{slug}' (len={len(slug)})")


def example_unique_slugs():
    """Unique slug generation examples."""
    print("\n" + "=" * 50)
    print("Unique Slug Generation")
    print("=" * 50)
    
    existing = ["hello-world", "hello-world-2", "my-post"]
    
    new_titles = ["Hello World", "My Post", "Hello World"]
    
    for title in new_titles:
        slug = generate_unique_slug(title, existing)
        existing.append(slug)
        print(f"  '{title}' → '{slug}'")


def example_sequential_slugs():
    """Sequential slug examples."""
    print("\n" + "=" * 50)
    print("Sequential Slug Generation")
    print("=" * 50)
    
    base = "Chapter"
    
    print("  Without padding:")
    for i in [1, 2, 3, 10, 100]:
        slug = generate_sequential_slug(base, i)
        print(f"    Index {i}: '{slug}'")
    
    print("\n  With zero-padding (3 digits):")
    for i in [1, 2, 3, 10, 100]:
        slug = generate_sequential_slug(base, i, index_width=3)
        print(f"    Index {i}: '{slug}'")


def example_date_slugs():
    """Date-prefixed slug examples."""
    print("\n" + "=" * 50)
    print("Date-Prefixed Slugs")
    print("=" * 50)
    
    title = "Daily Update"
    
    dates = ["2024-01-15", "2024-06-20", "2024-12-31"]
    
    for date in dates:
        slug = generate_date_slug(title, date)
        print(f"  '{title}' + {date} → '{slug}'")
    
    print(f"\n  Today's date: '{generate_date_slug(title)}'")


def example_hierarchical_slugs():
    """Hierarchical slug examples."""
    print("\n" + "=" * 50)
    print("Hierarchical Slugs")
    print("=" * 50)
    
    paths = [
        ["Blog", "Tech", "Python"],
        ["Products", "Electronics", "Phones"],
        ["Docs", "API", "v2", "Endpoints"],
    ]
    
    for path in paths:
        slug = generate_hierarchical_slug(path)
        print(f"  {path} → '{slug}'")


def example_category_slugs():
    """Category-prefixed slug examples."""
    print("\n" + "=" * 50)
    print("Category-Prefixed Slugs")
    print("=" * 50)
    
    categories = ["Tech", "Lifestyle", "Business"]
    title = "How to Succeed"
    
    for cat in categories:
        slug = generate_category_slug(title, cat)
        print(f"  '{cat}' + '{title}' → '{slug}'")


def example_batch_generation():
    """Batch generation examples."""
    print("\n" + "=" * 50)
    print("Batch Generation")
    print("=" * 50)
    
    titles = [
        "First Post",
        "Second Post",
        "First Post",  # Duplicate
        "Tech News",
        "Tech News",  # Duplicate
    ]
    
    print("  Input titles:", titles)
    
    print("\n  With unique enforcement:")
    slugs = generate_slug_batch(titles, ensure_unique=True)
    print(f"  Output: {slugs}")
    
    print("\n  Without unique enforcement:")
    slugs = generate_slug_batch(titles, ensure_unique=False)
    print(f"  Output: {slugs}")


def example_filename_slugs():
    """Filename-based slug examples."""
    print("\n" + "=" * 50)
    print("Filename-Based Slugs")
    print("=" * 50)
    
    filenames = [
        "My Document.pdf",
        "Report 2024.docx",
        "Presentation (Final).pptx",
        "data-analysis_v2.xlsx",
    ]
    
    for filename in filenames:
        slug = slug_from_filename(filename)
        print(f"  '{filename}' → '{slug}'")


def example_slug_generator_class():
    """SlugGenerator class examples."""
    print("\n" + "=" * 50)
    print("SlugGenerator Class")
    print("=" * 50)
    
    # Create generator with custom settings
    gen = SlugGenerator(separator="_", max_length=30)
    
    print("  Settings: separator='_', max_length=30")
    
    titles = ["Hello World", "Tech Blog Post", "A Very Very Long Title"]
    
    for title in titles:
        slug = gen.generate(title)
        print(f"    '{title}' → '{slug}'")
    
    print("\n  Unique generation:")
    gen2 = SlugGenerator()
    for title in ["Hello", "Hello", "Hello"]:
        slug = gen2.generate_unique(title)
        print(f"    '{title}' → '{slug}'")


def example_validation():
    """Slug validation examples."""
    print("\n" + "=" * 50)
    print("Slug Validation")
    print("=" * 50)
    
    test_slugs = [
        "hello-world",
        "Hello-World",
        "hello world",
        "hello_world",
        "",
        "test-123",
    ]
    
    for slug in test_slugs:
        is_valid = is_valid_slug(slug)
        print(f"  '{slug}' → Valid: {is_valid}")


def example_fixing():
    """Slug fixing examples."""
    print("\n" + "=" * 50)
    print("Fixing Invalid Slugs")
    print("=" * 50)
    
    bad_slugs = [
        "hello world",
        "Hello_World",
        "hello---world",
        "-hello-world-",
        "hello!@#world",
    ]
    
    for bad in bad_slugs:
        fixed = fix_slug(bad)
        print(f"  '{bad}' → '{fixed}'")


def example_slug_to_text():
    """Slug to text conversion examples."""
    print("\n" + "=" * 50)
    print("Slug to Text Conversion")
    print("=" * 50)
    
    slugs = [
        "hello-world",
        "my-blog-post-2024",
        "tech-news-today",
    ]
    
    for slug in slugs:
        text = slug_to_text(slug)
        print(f"  '{slug}' → '{text}'")


def example_real_world_scenario():
    """Real-world scenario: Blog system."""
    print("\n" + "=" * 50)
    print("Real-World Scenario: Blog System")
    print("=" * 50)
    
    # Simulate a blog post creation workflow
    print("\n  Creating blog posts:")
    
    posts = [
        ("Understanding Python Decorators", "Tech", "2024-01-15"),
        ("10 Tips for Better Sleep", "Lifestyle", "2024-01-16"),
        ("Python Decorators Deep Dive", "Tech", "2024-01-17"),
    ]
    
    existing_slugs = []
    
    for title, category, date in posts:
        # Generate base slug
        base = generate_slug(title)
        
        # Add category and date
        with_cat = generate_category_slug(title, category)
        with_date = generate_date_slug(title, date)
        
        # Ensure uniqueness
        unique = generate_unique_slug(title, existing_slugs)
        existing_slugs.append(unique)
        
        print(f"\n  Post: '{title}'")
        print(f"    Category: '{category}' → Slug: '{with_cat}'")
        print(f"    With date: '{with_date}'")
        print(f"    Unique: '{unique}'")


def example_international():
    """International character support."""
    print("\n" + "=" * 50)
    print("International Character Support")
    print("=" * 50)
    
    titles = [
        "Café de Paris",
        "Привет Мир",  # Russian
        "Γειά σου",  # Greek
        "東京の天気",  # Japanese (will be transliterated or stripped)
    ]
    
    for title in titles:
        slug = generate_slug(title)
        print(f"  '{title}' → '{slug}'")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - Slug Utilities Usage Examples")
    print("=" * 60)
    
    example_basic_slugs()
    example_custom_separator()
    example_max_length()
    example_unique_slugs()
    example_sequential_slugs()
    example_date_slugs()
    example_hierarchical_slugs()
    example_category_slugs()
    example_batch_generation()
    example_filename_slugs()
    example_slug_generator_class()
    example_validation()
    example_fixing()
    example_slug_to_text()
    example_real_world_scenario()
    example_international()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()