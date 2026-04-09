"""
AllToolkit - Phone Utils Basic Usage Examples

Simple examples demonstrating common phone number utility operations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    validate, parse, normalize, format_international, format_national,
    get_country_code, get_country, get_country_name, get_number_type,
    is_mobile, is_landline, is_toll_free,
    extract_from_text, deduplicate, sort_by_country, group_by_country, mask
)


def main():
    print("=" * 60)
    print("AllToolkit - Phone Utils Basic Examples")
    print("=" * 60)
    print()
    
    # 1. Phone Number Validation
    print("1. Phone Number Validation")
    print("-" * 40)
    phones_to_check = [
        "+1-234-567-8900",
        "+8613812345678",
        "+447911123456",
        "invalid",
        "123",
        "+4915123456789",
    ]
    
    for phone in phones_to_check:
        is_valid = validate(phone)
        status = "✓ Valid" if is_valid else "✗ Invalid"
        print(f"  {phone}: {status}")
    print()
    
    # 2. Phone Number Parsing
    print("2. Phone Number Parsing")
    print("-" * 40)
    parsed = parse("+1-234-567-8900")
    if parsed:
        print(f"  Original: {parsed.original}")
        print(f"  Country Code: {parsed.country_code}")
        print(f"  National Number: {parsed.national_number}")
        print(f"  Country: {parsed.country} ({get_country_name(parsed.country)})")
        print(f"  E.164: {parsed.e164}")
        print(f"  International: {parsed.international}")
        print(f"  National: {parsed.national}")
        print(f"  Type: {parsed.number_type}")
    print()
    
    # 3. Normalization (E.164)
    print("3. Normalization (E.164 Format)")
    print("-" * 40)
    variants = [
        "+1 (234) 567-8900",
        "+1.234.567.8900",
        "+1 234 567 8900",
        "1-234-567-8900",
        "(234) 567-8900",
    ]
    
    print("  All these normalize to the same E.164:")
    for variant in variants:
        normalized = normalize(variant, "US")
        print(f"    {variant} → {normalized}")
    print()
    
    # 4. Country Detection
    print("4. Country Detection")
    print("-" * 40)
    test_phones = [
        "+12345678900",
        "+8613812345678",
        "+447911123456",
        "+4915123456789",
        "+819012345678",
        "+61412345678",
    ]
    
    for phone in test_phones:
        code = get_country_code(phone)
        country = get_country(phone)
        name = get_country_name(country) if country else "Unknown"
        print(f"  {phone}:")
        print(f"    Code: {code}, Country: {country} ({name})")
    print()
    
    # 5. Number Type Detection
    print("5. Number Type Detection")
    print("-" * 40)
    type_tests = [
        ("+8613812345678", "CN", "China Mobile"),
        ("+18001234567", "US", "US Toll-Free"),
        ("+19001234567", "US", "US Premium"),
        ("+447911123456", "GB", "UK Mobile"),
        ("+4915123456789", "DE", "Germany Mobile"),
    ]
    
    for phone, country, desc in type_tests:
        num_type = get_number_type(phone, country)
        mobile = is_mobile(phone, country)
        toll_free = is_toll_free(phone, country)
        print(f"  {desc}:")
        print(f"    {phone}")
        print(f"    Type: {num_type}, Mobile: {mobile}, Toll-Free: {toll_free}")
    print()
    
    # 6. Phone Number Masking
    print("6. Phone Number Masking (Privacy)")
    print("-" * 40)
    phone = "+12345678900"
    print(f"  Original: {phone}")
    print(f"  Masked (last 4): {mask(phone, show_last=4)}")
    print(f"  Masked (last 2): {mask(phone, show_last=2)}")
    print(f"  Masked (last 6): {mask(phone, show_last=6)}")
    
    cn_phone = "+8613812345678"
    print(f"\n  Original: {cn_phone}")
    print(f"  Masked (last 4): {mask(cn_phone, show_last=4)}")
    print()
    
    # 7. Extract from Text
    print("7. Extract Phone Numbers from Text")
    print("-" * 40)
    text = """
    Contact our international offices:
    - US Office: +1 (234) 567-8900
    - China Office: +86 138 1234 5678
    - UK Office: +44 7911 123456
    - Germany Office: +49 151 2345 6789
    - Fax: 234-567-8901
    """
    
    extracted = extract_from_text(text)
    print(f"  Found {len(extracted)} phone number(s):")
    for p in extracted:
        country = get_country(p)
        print(f"    - {p} ({country})")
    print()
    
    # 8. Deduplication
    print("8. Phone Number Deduplication")
    print("-" * 40)
    duplicate_phones = [
        "+1-234-567-8900",
        "+12345678900",
        "(234) 567-8900",
        "234-567-8900",
        "+8613812345678",
        "+86 138 1234 5678",
    ]
    
    print("  Input:")
    for p in duplicate_phones:
        print(f"    - {p}")
    
    unique = deduplicate(duplicate_phones, "US")
    print(f"\n  After deduplication ({len(unique)} unique):")
    for p in unique:
        print(f"    - {p}")
    print()
    
    # 9. Group by Country
    print("9. Group Phone Numbers by Country")
    print("-" * 40)
    phones = [
        "+12345678900",
        "+19876543210",
        "+8613812345678",
        "+447911123456",
        "+4915123456789",
        "+819012345678",
    ]
    
    grouped = group_by_country(phones)
    for country, country_phones in sorted(grouped.items()):
        print(f"  {country}:")
        for p in country_phones:
            print(f"    - {p}")
    print()
    
    # 10. Sort by Country
    print("10. Sort Phone Numbers by Country Code")
    print("-" * 40)
    unsorted = [
        "+8613812345678",
        "+12345678900",
        "+447911123456",
        "+4915123456789",
    ]
    
    print("  Unsorted:")
    for p in unsorted:
        print(f"    - {p}")
    
    sorted_phones = sort_by_country(unsorted)
    print("\n  Sorted:")
    for p in sorted_phones:
        country = get_country(p)
        print(f"    - {p} ({country})")
    print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
