"""
AllToolkit - Phone Utils Advanced Examples

Advanced use cases demonstrating comprehensive phone number processing workflows.
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


# ============================================================================
# Example 1: CRM Contact Import and Validation
# ============================================================================

def example_crm_import():
    """
    Simulate importing contacts from a CSV file with phone validation.
    """
    print("=" * 60)
    print("Example 1: CRM Contact Import & Validation")
    print("=" * 60)
    
    # Simulated CSV data
    raw_contacts = [
        {"name": "John Smith", "phone": "+1-234-567-8900", "source": "web"},
        {"name": "Li Wei", "phone": "+86 138 1234 5678", "source": "wechat"},
        {"name": "Emma Wilson", "phone": "+44 7911 123456", "source": "referral"},
        {"name": "Invalid Entry", "phone": "not-a-phone", "source": "manual"},
        {"name": "Hans Mueller", "phone": "+49 151 2345 6789", "source": "trade_show"},
        {"name": "John Smith", "phone": "(234) 567-8900", "source": "import"},  # Duplicate
        {"name": "Short Number", "phone": "12345", "source": "manual"},
        {"name": "Yuki Tanaka", "phone": "+81 90 1234 5678", "source": "partner"},
    ]
    
    valid_contacts = []
    invalid_entries = []
    
    for contact in raw_contacts:
        phone = contact["phone"]
        
        # Validate phone
        if not validate(phone):
            invalid_entries.append({
                "name": contact["name"],
                "phone": phone,
                "reason": "Invalid format"
            })
            continue
        
        # Parse and enrich
        parsed = parse(phone)
        if not parsed:
            invalid_entries.append({
                "name": contact["name"],
                "phone": phone,
                "reason": "Parse failed"
            })
            continue
        
        # Check if mobile (for SMS marketing)
        can_sms = is_mobile(phone, parsed.country)
        
        # Create enriched contact
        valid_contacts.append({
            "name": contact["name"],
            "phone_original": phone,
            "phone_e164": parsed.e164,
            "phone_international": parsed.international,
            "country": parsed.country,
            "country_name": get_country_name(parsed.country),
            "number_type": parsed.number_type,
            "can_sms": can_sms,
            "source": contact["source"],
        })
    
    # Deduplicate by E.164
    seen_e164 = set()
    unique_contacts = []
    duplicates = []
    
    for contact in valid_contacts:
        if contact["phone_e164"] not in seen_e164:
            seen_e164.add(contact["phone_e164"])
            unique_contacts.append(contact)
        else:
            duplicates.append(contact["name"])
    
    # Report results
    print(f"\n  Total imported: {len(raw_contacts)}")
    print(f"  Valid contacts: {len(valid_contacts)}")
    print(f"  Unique contacts: {len(unique_contacts)}")
    print(f"  Invalid entries: {len(invalid_entries)}")
    print(f"  Duplicates removed: {len(duplicates)}")
    
    if invalid_entries:
        print("\n  Invalid Entries:")
        for entry in invalid_entries:
            print(f"    - {entry['name']}: {entry['phone']} ({entry['reason']})")
    
    if duplicates:
        print(f"\n  Duplicates: {', '.join(duplicates)}")
    
    # Group by country
    by_country = group_by_country([c["phone_e164"] for c in unique_contacts])
    print("\n  Distribution by Country:")
    for country, phones in sorted(by_country.items()):
        name = get_country_name(country)
        print(f"    {country} ({name}): {len(phones)} contacts")
    
    # SMS-capable contacts
    sms_capable = [c for c in unique_contacts if c["can_sms"]]
    print(f"\n  SMS-capable contacts: {len(sms_capable)}")
    
    print()


# ============================================================================
# Example 2: International Business Card Parser
# ============================================================================

def example_business_card_parser():
    """
    Parse business card text and extract/normalize contact information.
    """
    print("=" * 60)
    print("Example 2: Business Card Parser")
    print("=" * 60)
    
    business_cards = [
        """
        John Smith
        Sales Director | Global Tech Inc.
        Office: +1 (234) 567-8900
        Mobile: +1 987 654 3210
        Fax: +1 234 567 8901
        Email: john.smith@globaltech.com
        """,
        """
        李明 (Li Ming)
        技术总监 | 创新科技有限公司
        手机：+86 138 1234 5678
        办公室：+86 10 8888 9999
        邮箱：liming@innovatech.cn
        """,
        """
        Emma Wilson
        Marketing Manager | UK Solutions Ltd
        Tel: +44 7911 123456
        Office: +44 20 7946 0958
        emma.wilson@uksolutions.co.uk
        """,
    ]
    
    all_contacts = []
    
    for i, card_text in enumerate(business_cards, 1):
        print(f"\n  Processing Card {i}...")
        
        # Extract all phone numbers
        phones = extract_from_text(card_text)
        
        # Classify each phone
        card_phones = []
        for phone in phones:
            parsed = parse(phone)
            if parsed:
                phone_type = "Mobile" if is_mobile(phone, parsed.country) else \
                            "Toll-Free" if is_toll_free(phone, parsed.country) else \
                            "Office"
                card_phones.append({
                    "original": phone,
                    "e164": parsed.e164,
                    "type": phone_type,
                    "country": parsed.country,
                })
        
        all_contacts.extend(card_phones)
        
        print(f"    Found {len(card_phones)} phone number(s):")
        for p in card_phones:
            print(f"      [{p['type']}] {p['e164']} ({p['country']})")
    
    # Summary
    print(f"\n  Total cards processed: {len(business_cards)}")
    print(f"  Total phone numbers extracted: {len(all_contacts)}")
    
    # Group by type
    by_type = {}
    for contact in all_contacts:
        phone_type = contact["type"]
        if phone_type not in by_type:
            by_type[phone_type] = []
        by_type[phone_type].append(contact)
    
    print("\n  By Type:")
    for phone_type, contacts in sorted(by_type.items()):
        print(f"    {phone_type}: {len(contacts)}")
    
    print()


# ============================================================================
# Example 3: Phone Number Privacy Display System
# ============================================================================

def example_privacy_display():
    """
    Demonstrate different privacy levels for phone number display.
    """
    print("=" * 60)
    print("Example 3: Privacy Display System")
    print("=" * 60)
    
    contacts = [
        {"name": "John Smith", "phone": "+12345678900"},
        {"name": "Li Wei", "phone": "+8613812345678"},
        {"name": "Emma Wilson", "phone": "+447911123456"},
    ]
    
    print("\n  Display Modes:")
    print("  " + "-" * 56)
    
    for contact in contacts:
        name = contact["name"]
        phone = contact["phone"]
        parsed = parse(phone)
        
        print(f"\n  {name}:")
        print(f"    Full (admin):     {parsed.international}")
        print(f"    Masked (public):  {mask(phone, show_last=4)}")
        print(f"    Hidden (list):    {mask(phone, show_last=2)}")
        print(f"    Country only:     {parsed.country} ({get_country_name(parsed.country)})")
    
    print()


# ============================================================================
# Example 4: Bulk Phone List Analysis
# ============================================================================

def example_list_analysis():
    """
    Analyze a bulk list of phone numbers for marketing campaign.
    """
    print("=" * 60)
    print("Example 4: Bulk List Analysis for Marketing")
    print("=" * 60)
    
    # Simulated marketing list
    marketing_list = [
        "+12345678900", "+19876543210", "+15551234567",
        "+8613812345678", "+8615912345678", "+8618812345678",
        "+447911123456", "+447922123456",
        "+4915123456789", "+4915223456789",
        "+819012345678", "+818012345678",
        "+61412345678", "+61423456789",
        "+5511987654321", "+5521987654321",
        "+18001234567", "+18881234567",  # Toll-free
        "+19001234567",  # Premium
    ]
    
    # Analysis
    total = len(marketing_list)
    valid = [p for p in marketing_list if validate(p)]
    mobiles = [p for p in valid if is_mobile(p, get_country(p))]
    toll_free = [p for p in valid if is_toll_free(p, get_country(p))]
    premium = [p for p in valid if get_number_type(p, get_country(p)) == "premium"]
    
    by_country = group_by_country(valid)
    
    print(f"\n  List Statistics:")
    print(f"    Total numbers:      {total}")
    print(f"    Valid numbers:      {len(valid)} ({100*len(valid)/total:.1f}%)")
    print(f"    Mobile numbers:     {len(mobiles)} ({100*len(mobiles)/total:.1f}%)")
    print(f"    Toll-free numbers:  {len(toll_free)}")
    print(f"    Premium numbers:    {len(premium)}")
    
    print(f"\n  Geographic Distribution:")
    for country, phones in sorted(by_country.items(), key=lambda x: -len(x[1])):
        name = get_country_name(country)
        pct = 100 * len(phones) / len(valid)
        mobile_count = len([p for p in phones if is_mobile(p, country)])
        print(f"    {country} ({name}): {len(phones)} ({pct:.1f}%) - {mobile_count} mobile")
    
    # SMS Campaign eligibility
    sms_eligible = mobiles  # Only mobiles can receive SMS
    print(f"\n  SMS Campaign:")
    print(f"    Eligible contacts: {len(sms_eligible)}")
    print(f"    Coverage: {100*len(sms_eligible)/len(valid):.1f}% of valid numbers")
    
    print()


# ============================================================================
# Example 5: Phone Number Format Converter
# ============================================================================

def example_format_converter():
    """
    Convert phone numbers between different formats.
    """
    print("=" * 60)
    print("Example 5: Format Converter")
    print("=" * 60)
    
    test_numbers = [
        "+1-234-567-8900",
        "+86 138 1234 5678",
        "+44 7911 123456",
    ]
    
    print("\n  Format Comparison:")
    print("  " + "-" * 56)
    
    for original in test_numbers:
        parsed = parse(original)
        if parsed:
            print(f"\n  Original: {original}")
            print(f"    E.164:           {parsed.e164}")
            print(f"    International:   {parsed.international}")
            print(f"    National:        {parsed.national}")
            print(f"    Country Code:    {parsed.country_code}")
            print(f"    National Number: {parsed.national_number}")
    
    print()


# ============================================================================
# Example 6: Validation Rules Engine
# ============================================================================

def example_validation_engine():
    """
    Demonstrate a flexible validation rules engine.
    """
    print("=" * 60)
    print("Example 6: Validation Rules Engine")
    print("=" * 60)
    
    def validate_with_rules(phone: str, rules: dict) -> tuple:
        """
        Validate phone against custom rules.
        Returns (is_valid, message)
        """
        # Rule 1: Basic format validation
        if not validate(phone):
            return False, "Invalid phone format"
        
        parsed = parse(phone)
        if not parsed:
            return False, "Cannot parse phone number"
        
        # Rule 2: Country restriction
        if "allowed_countries" in rules:
            if parsed.country not in rules["allowed_countries"]:
                return False, f"Country {parsed.country} not allowed"
        
        # Rule 3: Number type requirement
        if "require_mobile" in rules and rules["require_mobile"]:
            if not is_mobile(phone, parsed.country):
                return False, "Mobile number required"
        
        # Rule 4: No toll-free numbers
        if "no_toll_free" in rules and rules["no_toll_free"]:
            if is_toll_free(phone, parsed.country):
                return False, "Toll-free numbers not allowed"
        
        return True, "Valid"
    
    # Test cases
    test_phones = [
        "+12345678900",
        "+8613812345678",
        "+18001234567",
        "+447911123456",
    ]
    
    # Rule set 1: US only, mobile required
    rules_us_mobile = {
        "allowed_countries": ["US"],
        "require_mobile": True,
    }
    
    print("\n  Rules: US only, Mobile required")
    print("  " + "-" * 56)
    for phone in test_phones:
        is_valid, message = validate_with_rules(phone, rules_us_mobile)
        status = "✓" if is_valid else "✗"
        print(f"    {status} {phone}: {message}")
    
    # Rule set 2: Multiple countries, no toll-free
    rules_multi = {
        "allowed_countries": ["US", "CN", "GB", "DE"],
        "no_toll_free": True,
    }
    
    print("\n  Rules: US/CN/GB/DE, No toll-free")
    print("  " + "-" * 56)
    for phone in test_phones:
        is_valid, message = validate_with_rules(phone, rules_multi)
        status = "✓" if is_valid else "✗"
        print(f"    {status} {phone}: {message}")
    
    print()


# ============================================================================
# Main
# ============================================================================

def main():
    """Run all advanced examples."""
    example_crm_import()
    example_business_card_parser()
    example_privacy_display()
    example_list_analysis()
    example_format_converter()
    example_validation_engine()
    
    print("=" * 60)
    print("All advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
