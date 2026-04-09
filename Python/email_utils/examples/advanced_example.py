"""
AllToolkit - Email Utils Advanced Examples

Advanced use cases for email processing, validation, and analysis.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    EmailUtils, EmailAddress,
    validate, parse, normalize, is_disposable, is_free_provider,
    extract_from_text, deduplicate, group_by_domain
)


def validate_user_registration(email: str) -> dict:
    """
    Validate an email for user registration.
    
    Returns a dict with validation results and recommendations.
    """
    result = {
        "email": email,
        "is_valid": False,
        "is_disposable": False,
        "is_free_provider": False,
        "normalized": None,
        "recommendation": "",
    }
    
    # Check validity
    if not validate(email):
        result["recommendation"] = "Please enter a valid email address"
        return result
    
    result["is_valid"] = True
    result["normalized"] = normalize(email)
    result["is_disposable"] = is_disposable(email)
    result["is_free_provider"] = is_free_provider(email)
    
    # Generate recommendation
    if result["is_disposable"]:
        result["recommendation"] = "Disposable email addresses are not allowed"
    elif result["is_free_provider"]:
        result["recommendation"] = "Consider using a business email for professional accounts"
    else:
        result["recommendation"] = "Email accepted"
    
    return result


def analyze_email_list(emails: list) -> dict:
    """
    Analyze a list of emails for quality and segmentation.
    """
    # Filter valid emails
    valid_emails = [e for e in emails if validate(e)]
    
    # Deduplicate
    unique_emails = deduplicate(valid_emails)
    
    # Categorize
    disposable = [e for e in unique_emails if is_disposable(e)]
    free_providers = [e for e in unique_emails if is_free_provider(e) and not is_disposable(e)]
    business = [e for e in unique_emails if not is_free_provider(e) and not is_disposable(e)]
    
    # Group by domain
    domain_groups = group_by_domain(unique_emails)
    
    # Find most common domains
    domain_counts = [(domain, len(emails)) for domain, emails in domain_groups.items()]
    domain_counts.sort(key=lambda x: x[1], reverse=True)
    
    return {
        "total_input": len(emails),
        "valid_count": len(valid_emails),
        "unique_count": len(unique_emails),
        "invalid_count": len(emails) - len(valid_emails),
        "duplicate_count": len(valid_emails) - len(unique_emails),
        "disposable_count": len(disposable),
        "free_provider_count": len(free_providers),
        "business_count": len(business),
        "top_domains": domain_counts[:5],
        "disposable_emails": disposable,
        "free_provider_emails": free_providers,
        "business_emails": business,
    }


def clean_contact_list(raw_text: str) -> list:
    """
    Extract and clean email addresses from raw text (e.g., email signature, document).
    """
    # Extract all potential emails
    extracted = extract_from_text(raw_text)
    
    # Validate and normalize
    cleaned = []
    seen = set()
    
    for email in extracted:
        normalized = normalize(email)
        if normalized and normalized.lower() not in seen:
            seen.add(normalized.lower())
            cleaned.append(normalized)
    
    return cleaned


def format_mailing_list(emails: list, format_type: str = "simple") -> list:
    """
    Format a list of emails for different mailing list formats.
    
    format_type: "simple", "rfc2822", "obfuscated"
    """
    if format_type == "simple":
        return [normalize(e) for e in emails if validate(e)]
    
    elif format_type == "rfc2822":
        # Format with display names if available
        formatted = []
        for email in emails:
            parsed = parse(email)
            if parsed:
                formatted.append(EmailUtils.format_with_name(email))
        return formatted
    
    elif format_type == "obfuscated":
        # Obfuscate for public display
        return [obfuscate(e) for e in emails if validate(e)]
    
    return emails


def obfuscate(email: str, show_chars: int = 2) -> str:
    """Helper to access obfuscate from mod."""
    from mod import obfuscate as _obfuscate
    return _obfuscate(email, show_chars)


def main():
    print("=" * 60)
    print("AllToolkit - Email Utils Advanced Examples")
    print("=" * 60)
    print()
    
    # Example 1: User Registration Validation
    print("1. User Registration Validation")
    print("-" * 40)
    test_registrations = [
        "user@gmail.com",
        "temp@mailinator.com",
        "invalid-email",
        "business@company.com",
    ]
    
    for email in test_registrations:
        result = validate_user_registration(email)
        print(f"  {email}:")
        print(f"    Valid: {result['is_valid']}")
        print(f"    Normalized: {result['normalized']}")
        print(f"    Recommendation: {result['recommendation']}")
    print()
    
    # Example 2: Email List Analysis
    print("2. Email List Quality Analysis")
    print("-" * 40)
    sample_list = [
        "alice@gmail.com",
        "bob@company.com",
        "charlie@gmail.com",
        "spam@tempmail.com",
        "alice@gmail.com",  # Duplicate
        "dave@yahoo.com",
        "eve@business.org",
        "invalid",
        "temp@10minutemail.com",
        "frank@company.com",
    ]
    
    analysis = analyze_email_list(sample_list)
    print(f"  Total input: {analysis['total_input']}")
    print(f"  Valid: {analysis['valid_count']}")
    print(f"  Unique: {analysis['unique_count']}")
    print(f"  Duplicates removed: {analysis['duplicate_count']}")
    print(f"  Invalid: {analysis['invalid_count']}")
    print(f"  Disposable: {analysis['disposable_count']}")
    print(f"  Free providers: {analysis['free_provider_count']}")
    print(f"  Business emails: {analysis['business_count']}")
    print(f"  Top domains: {analysis['top_domains'][:3]}")
    print()
    
    # Example 3: Clean Contact List from Text
    print("3. Extract Contacts from Document")
    print("-" * 40)
    raw_document = """
    Our Team Contacts:
    
    John Smith - CEO
    Email: john.smith@company.com
    Phone: 555-0100
    
    Jane Doe - CTO  
    Contact: jane.doe@company.com or jdoe@personal.gmail.com
    
    Support Team:
    - support@company.com
    - help@company.com
    - info@company.com
    
    External partners:
    partner1@vendor.com, partner2@vendor.com
    """
    
    cleaned = clean_contact_list(raw_document)
    print(f"  Extracted {len(cleaned)} unique valid emails:")
    for email in cleaned:
        print(f"    - {email}")
    print()
    
    # Example 4: Mailing List Formatting
    print("4. Mailing List Formatting")
    print("-" * 40)
    mailing_list = [
        '"John Doe" <john@example.com>',
        "Jane.Smith+newsletter@gmail.com",
        "bob@company.com",
    ]
    
    print("  Simple format:")
    simple = format_mailing_list(mailing_list, "simple")
    for email in simple:
        print(f"    {email}")
    
    print("\n  RFC2822 format:")
    rfc = format_mailing_list(mailing_list, "rfc2822")
    for email in rfc:
        print(f"    {email}")
    
    print("\n  Obfuscated format (for public display):")
    obfuscated = format_mailing_list(mailing_list, "obfuscated")
    for email in obfuscated:
        print(f"    {email}")
    print()
    
    # Example 5: Bulk Email Processing Pipeline
    print("5. Complete Email Processing Pipeline")
    print("-" * 40)
    
    # Simulate importing contacts from multiple sources
    raw_imports = [
        "User1@GMAIL.COM",
        "user1@gmail.com",  # Duplicate
        "user2@TEMPMAIL.COM",  # Disposable
        "User3@Company.com",
        "user3@company.com",  # Duplicate (case)
        "invalid-email",
        "user4@yahoo.com",
        "user5@business.org",
    ]
    
    print(f"  Raw imports: {len(raw_imports)} emails")
    
    # Step 1: Validate
    valid = [e for e in raw_imports if validate(e)]
    print(f"  After validation: {len(valid)} valid")
    
    # Step 2: Filter disposable
    non_disposable = [e for e in valid if not is_disposable(e)]
    print(f"  After filtering disposable: {len(non_disposable)}")
    
    # Step 3: Deduplicate
    unique = deduplicate(non_disposable)
    print(f"  After deduplication: {len(unique)} unique")
    
    # Step 4: Normalize
    normalized = [normalize(e) for e in unique]
    print(f"  Final clean list:")
    for email in sorted(normalized):
        print(f"    - {email}")
    print()
    
    print("=" * 60)
    print("Advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
