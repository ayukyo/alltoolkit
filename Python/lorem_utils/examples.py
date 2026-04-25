"""
Lorem Ipsum Generator Examples
==============================

Example usage of the lorem_utils module.

Run with: python examples.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lorem_utils import (
    LoremGenerator,
    words, sentence, sentences, paragraph, paragraphs,
    title, headline, html_paragraphs, list_items,
    buzzword, buzzwords, email, username, url, phone,
    address, name, company, generate
)


def print_section(title_str: str):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(title_str)
    print("=" * 60)


def demo_basic_usage():
    """Demonstrate basic usage."""
    print_section("📝 Basic Usage")
    
    # Generate words
    print("\n1. Generate 10 words:")
    print(words(10))
    
    # Generate a sentence
    print("\n2. Generate a sentence:")
    print(sentence())
    
    # Generate multiple sentences
    print("\n3. Generate 3 sentences:")
    print(sentences(3))
    
    # Generate a paragraph
    print("\n4. Generate a paragraph:")
    print(paragraph())
    
    # Generate multiple paragraphs
    print("\n5. Generate 2 paragraphs:")
    print(paragraphs(2))


def demo_class_usage():
    """Demonstrate class-based usage."""
    print_section("🔧 LoremGenerator Class")
    
    # Create generator with seed for reproducibility
    gen = LoremGenerator(seed=42)
    
    print("\n1. Words (with seed 42):")
    print(gen.words(8))
    
    print("\n2. Sentence (custom length 5-10 words):")
    print(gen.sentence(min_words=5, max_words=10))
    
    print("\n3. Paragraphs (custom length):")
    print(gen.paragraphs(2, min_sentences=3, max_sentences=5))
    
    print("\n4. Reset seed and generate again:")
    gen.reset_seed(42)
    print(gen.words(5))


def demo_titles_and_headlines():
    """Demonstrate title and headline generation."""
    print_section("📰 Titles & Headlines")
    
    print("\n1. Generate titles:")
    for i in range(3):
        print(f"   - {title()}")
    
    print("\n2. Generate headlines:")
    for i in range(3):
        print(f"   - {headline()}")


def demo_html_output():
    """Demonstrate HTML output."""
    print_section("🌐 HTML Output")
    
    print("\n1. HTML paragraphs:")
    print(html_paragraphs(2))
    
    print("\n2. HTML with custom tag:")
    print(html_paragraphs(2, wrap_tag='article'))


def demo_lists():
    """Demonstrate list generation."""
    print_section("📋 Lists")
    
    print("\n1. Unordered list:")
    print(list_items(5))
    
    print("\n2. Ordered list:")
    print(list_items(5, ordered=True))
    
    print("\n3. Short list items:")
    print(list_items(4, min_words=2, max_words=4))


def demo_fake_data():
    """Demonstrate fake data generation."""
    print_section("🎭 Fake Data")
    
    gen = LoremGenerator(seed=123)
    
    print("\n1. Fake personal info:")
    print(f"   Name: {gen.name()}")
    print(f"   Email: {gen.email()}")
    print(f"   Username: {gen.username()}")
    print(f"   Phone: {gen.phone()}")
    print(f"   Address: {gen.address()}")
    
    print("\n2. Fake company info:")
    print(f"   Company: {gen.company()}")
    print(f"   Website: {gen.url()}")
    
    print("\n3. Buzzwords:")
    print(f"   {gen.buzzwords(5)}")


def demo_generate_function():
    """Demonstrate the generate() function."""
    print_section("⚡ Generate Function")
    
    print("\n1. Generate by type:")
    print(f"   Words: {generate('words', 3, seed=42)}")
    print(f"   Sentence: {generate('sentence', seed=42)}")
    print(f"   Title: {generate('title', seed=42)}")
    print(f"   Email: {generate('email', seed=42)}")
    
    print("\n2. Generate paragraphs:")
    print(generate('paragraphs', 2, seed=42))


def demo_extended_pool():
    """Demonstrate extended word pool."""
    print_section("📚 Extended Word Pool")
    
    print("\n1. Standard word pool:")
    gen_standard = LoremGenerator(seed=42)
    print(gen_standard.words(15))
    
    print("\n2. Extended word pool:")
    gen_extended = LoremGenerator(seed=42, use_extended=True)
    print(gen_extended.words(15))


def demo_reproducibility():
    """Demonstrate reproducibility with seeds."""
    print_section("🔄 Reproducibility")
    
    print("\n1. Same seed = same output:")
    result1 = paragraphs(2, seed=999)
    result2 = paragraphs(2, seed=999)
    print(f"   Match: {result1 == result2}")
    
    print("\n2. Different seed = different output:")
    result3 = paragraphs(2, seed=1)
    result4 = paragraphs(2, seed=2)
    print(f"   Match: {result3 == result4}")


def demo_use_cases():
    """Demonstrate practical use cases."""
    print_section("💼 Practical Use Cases")
    
    # Use case 1: Mock data for development
    print("\n1. Mock User Data:")
    gen = LoremGenerator(seed=2024)
    print(f"   Name: {gen.name()}")
    print(f"   Email: {gen.email('company.com')}")
    print(f"   Phone: {gen.phone()}")
    
    # Use case 2: Placeholder content
    print("\n2. Placeholder Article:")
    print(f"   Title: {gen.headline()}")
    print(f"   Content: {gen.paragraph()[:100]}...")
    
    # Use case 3: UI Mockup
    print("\n3. UI Mockup Data:")
    print(f"   Button: {gen.buzzword()}")
    print(f"   Heading: {gen.title()}")
    print(f"   Description: {gen.sentences(1)}")
    
    # Use case 4: Form fields
    print("\n4. Form Field Data:")
    print(f"   Username: {gen.username()}")
    print(f"   Email: {gen.email()}")
    print(f"   Address: {gen.address()}")


def demo_content_generation():
    """Demonstrate content generation."""
    print_section("📝 Content Generation")
    
    gen = LoremGenerator(seed=42)
    
    # Blog post preview
    print("\n1. Blog Post Preview:")
    print(f"   Title: {gen.headline()}")
    print(f"   Author: {gen.name()}")
    print(f"   Date: 2024-01-15")
    print(f"   Preview: {gen.sentences(2)}")
    
    # Product description
    print("\n2. Product Description:")
    print(f"   Name: {gen.title()}")
    print(f"   Description: {gen.paragraph()}")
    print(f"   Price: $99.99")
    
    # Comment thread
    print("\n3. Comment Thread:")
    for i in range(3):
        print(f"   {gen.name()}: {gen.sentences(1)}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("🚀 Lorem Ipsum Generator Examples")
    print("=" * 60)
    
    demo_basic_usage()
    demo_class_usage()
    demo_titles_and_headlines()
    demo_html_output()
    demo_lists()
    demo_fake_data()
    demo_generate_function()
    demo_extended_pool()
    demo_reproducibility()
    demo_use_cases()
    demo_content_generation()
    
    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()