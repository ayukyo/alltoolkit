"""
usage_examples.py - Practical examples for slug_utils

Demonstrates real-world use cases for slug generation.
"""

from mod import (
    slugify,
    slugify_unique,
    deslugify,
    is_valid_slug,
    slug_range,
    url_slug,
    file_slug,
)


def example_blog_post_urls():
    """Example: Generate URL-friendly slugs for blog posts."""
    print("=" * 50)
    print("Example 1: Blog Post URLs")
    print("=" * 50)
    
    titles = [
        "My First Blog Post!",
        "How to Build a REST API with Python",
        "10 Tips for Better Code Quality",
        "Café & Restaurant Reviews 2024",
        "What's New in JavaScript ES2024?",
    ]
    
    print("\nGenerating URL slugs for blog titles:\n")
    for title in titles:
        slug = url_slug(title)
        print(f"  Title: {title!r}")
        print(f"    URL: /blog/{slug}")
        print()


def example_unique_slugs():
    """Example: Generate unique slugs for existing content."""
    print("=" * 50)
    print("Example 2: Unique Slugs for Duplicate Titles")
    print("=" * 50)
    
    # Existing slugs in database
    existing_slugs = {
        "my-first-post",
        "my-first-post-2",
        "hello-world",
    }
    
    new_titles = [
        "My First Post",  # Duplicate!
        "My First Post",  # Another duplicate!
        "Hello World",    # Duplicate!
        "Brand New Post", # New
    ]
    
    print("\nGenerating unique slugs (avoiding duplicates):\n")
    print(f"  Existing: {existing_slugs}")
    print()
    
    for title in new_titles:
        unique_slug = slugify_unique(title, existing_slugs)
        existing_slugs.add(unique_slug)
        print(f"  Title: {title!r}")
        print(f"    → Unique slug: {unique_slug}")
        print()


def example_file_names():
    """Example: Generate filesystem-friendly filenames."""
    print("=" * 50)
    print("Example 3: File-Friendly Names")
    print("=" * 50)
    
    document_names = [
        "Annual Report 2024.pdf",
        "Project Proposal - Draft #2.docx",
        "Meeting Notes (January).txt",
        "Data Export - Final Version.csv",
    ]
    
    print("\nConverting document names to safe filenames:\n")
    for doc in document_names:
        filename = file_slug(doc)
        print(f"  Original: {doc!r}")
        print(f"    Safe: {filename}")
        print()


def example_slug_validation():
    """Example: Validate user-provided slugs."""
    print("=" * 50)
    print("Example 4: Slug Validation")
    print("=" * 50)
    
    test_slugs = [
        "valid-slug",
        "Invalid Slug",      # Has spaces
        "another-valid-123",
        "Invalid!",          # Has special char
        "also-valid_underscore",
        "-starts-with-dash", # Invalid start
        "ends-with-dash-",   # Invalid end
    ]
    
    print("\nValidating slugs:\n")
    for test_slug in test_slugs:
        valid = is_valid_slug(test_slug)
        status = "✓ Valid" if valid else "✗ Invalid"
        print(f"  {test_slug!r}: {status}")


def example_truncated_slugs():
    """Example: Generate slugs with length limits."""
    print("\n" + "=" * 50)
    print("Example 5: Smart Truncation")
    print("=" * 50)
    
    long_titles = [
        "The Complete Guide to Building Scalable Web Applications",
        "A Comprehensive Introduction to Machine Learning and Artificial Intelligence",
        "Understanding the Fundamentals of Cloud Computing Architecture",
    ]
    
    print("\nGenerating slugs with maximum length of 30:\n")
    for title in long_titles:
        slug = slug_range(title, max_length=30)
        print(f"  Title: {title!r}")
        print(f"    Slug ({len(slug)} chars): {slug}")
        print()


def example_multilingual():
    """Example: Handle multilingual content."""
    print("=" * 50)
    print("Example 6: Multilingual Support")
    print("=" * 50)
    
    titles = [
        "Café au Lait Recipe",          # French accent
        "München Travel Guide",          # German umlaut
        "Moscow: Москва Guide",          # Russian
        "Tokyo Sushi 東京寿司",           # Japanese (partial support)
        "Beijing 北京 Tour",              # Chinese (partial support)
        "Naïve Implementation",          # Diaeresis
    ]
    
    print("\nTransliterating multilingual titles:\n")
    for title in titles:
        slug = url_slug(title)
        print(f"  {title!r}")
        print(f"    → {slug}")
        print()


def example_ecommerce():
    """Example: E-commerce product slugs."""
    print("=" * 50)
    print("Example 7: E-commerce Product URLs")
    print("=" * 50)
    
    products = [
        "iPhone 15 Pro Max 256GB - Space Black",
        "Samsung Galaxy S24 Ultra 512GB",
        "Sony WH-1000XM5 Wireless Headphones",
        "Apple MacBook Pro 14\" M3 Pro",
        "Nintendo Switch OLED Model - White",
    ]
    
    print("\nGenerating product page slugs:\n")
    for product in products:
        slug = url_slug(product)
        print(f"  Product: {product}")
        print(f"    URL: /products/{slug}")
        print()


def example_deslugify():
    """Example: Convert slugs back to readable text."""
    print("=" * 50)
    print("Example 8: Converting Slugs Back to Text")
    print("=" * 50)
    
    slugs = [
        "hello-world",
        "my-blog-post",
        "product-review-2024",
        "user_guide",
    ]
    
    print("\nConverting slugs to readable text:\n")
    for slug in slugs:
        separator = '_' if '_' in slug else '-'
        text = deslugify(slug, separator=separator)
        print(f"  Slug: {slug!r}")
        print(f"    Text: {text!r}")
        print()


def main():
    """Run all examples."""
    example_blog_post_urls()
    example_unique_slugs()
    example_file_names()
    example_slug_validation()
    example_truncated_slugs()
    example_multilingual()
    example_ecommerce()
    example_deslugify()
    
    print("=" * 50)
    print("All examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()