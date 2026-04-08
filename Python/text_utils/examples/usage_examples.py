#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit Text Utils - Usage Examples
=======================================
Demonstrates common use cases for the text utilities module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'text_utils'))

from mod import (
    clean_whitespace, clean_text, remove_html_tags, remove_urls, remove_emojis,
    truncate, pad_left, pad_right, pad_center, wrap_text, indent_text,
    to_camel_case, to_pascal_case, to_snake_case, to_kebab_case,
    replace_all, find_all,
    count_words, count_chars, word_frequency,
    escape_html, hash_text,
    levenshtein_distance, similarity_ratio, is_palindrome,
    reverse_string, extract_numbers, extract_emails, mask_text
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def example_cleaning():
    """Example: Text Cleaning"""
    print_section("Text Cleaning Examples")
    
    # Clean whitespace
    messy = "  Hello    World!  \n\n  How are you?  "
    cleaned = clean_whitespace(messy)
    print(f"Original: {repr(messy)}")
    print(f"Cleaned:  {repr(cleaned)}")
    
    # Remove HTML tags
    html = "<div><p>Hello <b>World</b></p><br/><img src='test.jpg'/></div>"
    plain = remove_html_tags(html)
    print(f"\nHTML:     {html}")
    print(f"Plain:    {plain}")
    
    # Remove URLs
    text_with_urls = "Visit https://example.com or www.test.org for more info"
    no_urls = remove_urls(text_with_urls)
    print(f"\nWith URLs:    {text_with_urls}")
    print(f"Without URLs: {no_urls}")
    
    # Clean text with multiple options
    dirty = "  Hello, World! 123  "
    cleaned_multi = clean_text(dirty, remove_punctuation=True, remove_digits=True, lowercase=True)
    print(f"\nOriginal: {repr(dirty)}")
    print(f"Cleaned:  {repr(cleaned_multi)}")


def example_formatting():
    """Example: Text Formatting"""
    print_section("Text Formatting Examples")
    
    # Truncate
    long_text = "This is a very long text that needs to be truncated"
    print(f"Original: {long_text}")
    print(f"Truncated (20 chars): {truncate(long_text, 20)}")
    
    # Padding
    print(f"\nPadding examples:")
    print(f"  Left pad:  '{pad_left('42', 8, '0')}'")
    print(f"  Right pad: '{pad_right('Hello', 10)}'")
    print(f"  Center:    '{pad_center('TITLE', 20, '=')}'")
    
    # Wrap text
    long_line = "This is a very long line that should be wrapped to fit within a specified width"
    wrapped = wrap_text(long_line, width=20)
    print(f"\nWrapped text (width=20):")
    print(wrapped)
    
    # Indent text
    code = "def hello():\n    print('Hello')\n    return True"
    indented = indent_text(code, spaces=4)
    print(f"\nIndented code:")
    print(indented)


def example_case_conversion():
    """Example: Case Conversion"""
    print_section("Case Conversion Examples")
    
    base = "hello_world_test"
    print(f"Original (snake_case): {base}")
    print(f"  camelCase:   {to_camel_case(base)}")
    print(f"  PascalCase:  {to_pascal_case(base)}")
    print(f"  kebab-case:  {to_kebab_case(base)}")
    
    camel = "helloWorldTest"
    print(f"\nOriginal (camelCase): {camel}")
    print(f"  snake_case:  {to_snake_case(camel)}")
    print(f"  kebab-case:  {to_kebab_case(camel)}")


def example_analysis():
    """Example: Text Analysis"""
    print_section("Text Analysis Examples")
    
    sample = "Python is great. Python is powerful. Python is easy to learn."
    
    print(f"Text: {sample}")
    print(f"\nAnalysis:")
    print(f"  Word count:   {count_words(sample)}")
    print(f"  Char count:   {count_chars(sample)}")
    print(f"  Line count:   {count_chars(sample.split('.')[0])}")  # Just demo
    
    freq = word_frequency(sample, lowercase=True)
    print(f"\nWord frequency:")
    for word, count in sorted(freq.items(), key=lambda x: -x[1])[:5]:
        print(f"  {word}: {count}")


def example_security():
    """Example: Security & Encoding"""
    print_section("Security & Encoding Examples")
    
    # HTML escaping (XSS prevention)
    user_input = "<script>alert('XSS')</script>"
    safe = escape_html(user_input)
    print(f"User input:  {user_input}")
    print(f"HTML escaped: {safe}")
    print(f"  (Safe to display in HTML)")
    
    # Hashing
    password = "my_secret_password"
    print(f"\nPassword hashing:")
    print(f"  Original: {password}")
    print(f"  MD5:      {hash_text(password, 'md5')}")
    print(f"  SHA256:   {hash_text(password, 'sha256')}")
    
    # Masking sensitive data
    credit_card = "1234567890123456"
    masked = mask_text(credit_card, visible_end=4)
    print(f"\nData masking:")
    print(f"  Original: {credit_card}")
    print(f"  Masked:   {masked}")
    
    email = "user@example.com"
    masked_email = mask_text(email, visible_start=2, visible_end=10)
    print(f"  Email original: {email}")
    print(f"  Email masked:   {masked_email}")


def example_string_operations():
    """Example: String Operations"""
    print_section("String Operations Examples")
    
    # Reverse
    text = "Hello World"
    print(f"Original: {text}")
    print(f"Reversed: {reverse_string(text)}")
    
    # Palindrome check
    test_strings = ["radar", "hello", "A man a plan a canal Panama"]
    print(f"\nPalindrome checks:")
    for s in test_strings:
        result = is_palindrome(s)
        print(f"  '{s}' -> {result}")
    
    # String similarity
    s1, s2 = "kitten", "sitting"
    distance = levenshtein_distance(s1, s2)
    similarity = similarity_ratio(s1, s2)
    print(f"\nString comparison:")
    print(f"  '{s1}' vs '{s2}'")
    print(f"  Levenshtein distance: {distance}")
    print(f"  Similarity ratio:     {similarity:.2%}")


def example_extraction():
    """Example: Data Extraction"""
    print_section("Data Extraction Examples")
    
    # Extract numbers
    text = "I bought 3 apples for $15 and 5 oranges for $20"
    numbers = extract_numbers(text)
    print(f"Text: {text}")
    print(f"Numbers found: {numbers}")
    print(f"Total items: {sum(numbers)}")
    
    # Extract emails
    contact_info = """
    Contact us:
    - Support: support@example.com
    - Sales: sales@company.org
    - Info: info@test.net
    """
    emails = extract_emails(contact_info)
    print(f"\nContact info text:")
    print(f"Emails found: {emails}")
    
    # Find all patterns
    text_with_dates = "Events on 2024-01-15, 2024-02-20, and 2024-03-25"
    dates = find_all(text_with_dates, r'\d{4}-\d{2}-\d{2}')
    print(f"\nText: {text_with_dates}")
    print(f"Dates found: {dates}")


def example_real_world():
    """Example: Real-world Scenarios"""
    print_section("Real-world Scenarios")
    
    # Scenario 1: Processing user-generated content
    print("Scenario 1: Processing User Content")
    print("-" * 40)
    user_content = """
    <p>Check out this deal: https://spam-site.com!!! 😍😍😍</p>
    <script>malicious()</script>
    """
    
    # Clean the content
    step1 = remove_html_tags(user_content)
    step2 = remove_urls(step1)
    step3 = remove_emojis(step2)
    step4 = clean_whitespace(step3)
    
    print(f"Original: {repr(user_content)}")
    print(f"Cleaned:  {repr(step4)}")
    
    # Scenario 2: Variable name conversion
    print("\n\nScenario 2: API Response to Python Variables")
    print("-" * 40)
    api_fields = ["user_id", "first_name", "last_name", "created_at"]
    python_vars = [to_camel_case(f) for f in api_fields]
    
    print(f"API fields (snake_case): {api_fields}")
    print(f"Python vars (camelCase): {python_vars}")
    
    # Scenario 3: Password strength indicator
    print("\n\nScenario 3: Password Analysis")
    print("-" * 40)
    passwords = ["123456", "Password1", "MyC0mpl3x!Pass", "a"]
    
    for pwd in passwords:
        length = len(pwd)
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd)
        
        score = sum([
            length >= 8,
            length >= 12,
            has_upper,
            has_lower,
            has_digit,
            has_special
        ])
        
        strength = "Weak" if score < 3 else "Medium" if score < 5 else "Strong"
        print(f"  '{pwd}' -> {strength} (score: {score}/6)")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("  AllToolkit Text Utils - Usage Examples")
    print("="*60)
    
    example_cleaning()
    example_formatting()
    example_case_conversion()
    example_analysis()
    example_security()
    example_string_operations()
    example_extraction()
    example_real_world()
    
    print("\n" + "="*60)
    print("  Examples Complete!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
