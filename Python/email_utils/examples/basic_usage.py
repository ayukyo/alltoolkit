"""
AllToolkit - Email Utils Basic Usage Examples

Simple examples demonstrating common email utility operations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    validate, parse, normalize, is_disposable, is_free_provider,
    get_domain, get_local, obfuscate, format_with_name,
    extract_from_text, deduplicate, sort_by_domain, group_by_domain
)


def main():
    print("=" * 60)
    print("AllToolkit - Email Utils Basic Examples")
    print("=" * 60)
    print()
    
    # 1. Email Validation
    print("1. Email Validation")
    print("-" * 40)
    emails_to_check = [
        "user@example.com",
        "invalid.email",
        "test+tag@gmail.com",
        "@bad.com",
    ]
    
    for email in emails_to_check:
        is_valid = validate(email)
        status = "✓ Valid" if is_valid else "✗ Invalid"
        print(f"  {email}: {status}")
    print()
    
    # 2. Email Parsing
    print("2. Email Parsing")
    print("-" * 40)
    parsed = parse("John Doe <john@example.com>")
    if parsed:
        print(f"  Original: {parsed.original}")
        print(f"  Local: {parsed.local}")
        print(f"  Domain: {parsed.domain}")
        print(f"  Normalized: {parsed.normalized}")
        print(f"  Display Name: {parsed.display_name}")
    print()
    
    # 3. Email Normalization
    print("3. Email Normalization (Gmail)")
    print("-" * 40)
    gmail_variants = [
        "John.Doe@gmail.com",
        "johndoe@gmail.com",
        "john.doe+newsletter@gmail.com",
    ]
    
    print("  All these normalize to the same address:")
    for variant in gmail_variants:
        normalized = normalize(variant)
        print(f"    {variant} → {normalized}")
    print()
    
    # 4. Disposable Email Detection
    print("4. Disposable Email Detection")
    print("-" * 40)
    test_emails = [
        "user@mailinator.com",
        "temp@10minutemail.com",
        "real@gmail.com",
        "business@company.com",
    ]
    
    for email in test_emails:
        is_disp = is_disposable(email)
        is_free = is_free_provider(email)
        print(f"  {email}:")
        print(f"    Disposable: {is_disp}, Free Provider: {is_free}")
    print()
    
    # 5. Email Obfuscation
    print("5. Email Obfuscation (for display)")
    print("-" * 40)
    email = "john.doe@example.com"
    obfuscated = obfuscate(email, show_chars=2)
    print(f"  Original: {email}")
    print(f"  Obfuscated: {obfuscated}")
    print()
    
    # 6. Extract Emails from Text
    print("6. Extract Emails from Text")
    print("-" * 40)
    text = """
    Contact our team:
    - Sales: sales@company.com
    - Support: support@company.com  
    - HR: hr@company.com
    
    Or email info@example.org for general inquiries.
    """
    
    extracted = extract_from_text(text)
    print(f"  Found {len(extracted)} email(s):")
    for e in extracted:
        print(f"    - {e}")
    print()
    
    # 7. Deduplication
    print("7. Email Deduplication")
    print("-" * 40)
    duplicate_emails = [
        "User@Gmail.com",
        "user@gmail.com",
        "u.s.e.r@gmail.com",
        "user+tag@gmail.com",
        "other@yahoo.com",
    ]
    
    print("  Input:")
    for e in duplicate_emails:
        print(f"    - {e}")
    
    unique = deduplicate(duplicate_emails)
    print(f"\n  After deduplication ({len(unique)} unique):")
    for e in unique:
        print(f"    - {e}")
    print()
    
    # 8. Group by Domain
    print("8. Group Emails by Domain")
    print("-" * 40)
    emails = [
        "alice@gmail.com",
        "bob@yahoo.com",
        "charlie@gmail.com",
        "dave@company.com",
        "eve@yahoo.com",
    ]
    
    grouped = group_by_domain(emails)
    for domain, domain_emails in sorted(grouped.items()):
        print(f"  {domain}:")
        for e in domain_emails:
            print(f"    - {e}")
    print()
    
    # 9. Sort by Domain
    print("9. Sort Emails by Domain")
    print("-" * 40)
    unsorted = ["z@yahoo.com", "a@gmail.com", "m@aol.com", "b@gmail.com"]
    sorted_emails = sort_by_domain(unsorted)
    
    print("  Sorted:")
    for e in sorted_emails:
        print(f"    - {e}")
    print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
