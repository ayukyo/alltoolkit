#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Coupon Utilities Usage Examples

Practical examples demonstrating coupon generation, validation, and discount calculation.

Author: AllToolkit
License: MIT
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # Enums
    CouponFormat, DiscountType, CouponStatus,
    # Data Classes
    CouponConfig, DiscountConfig, Coupon, DiscountResult,
    # Generation
    generate_code, generate_phonetic_code, generate_readable_code,
    generate_pattern_code, generate_codes, generate_phonetic_codes,
    generate_readable_codes,
    # Validation
    validate_code, validate_checksum,
    # Discount Calculation
    calculate_discount, calculate_tiered_discount,
    # Coupon Management
    create_coupon, create_coupons, apply_coupon,
    # Utilities
    normalize_code, format_code, mask_code, code_strength
)


def example_01_basic_generation():
    """Example 1: Basic coupon code generation."""
    print("\n" + "="*60)
    print("Example 1: Basic Coupon Code Generation")
    print("="*60)
    
    # Simple random code
    code = generate_code()
    print(f"Default code: {code}")
    
    # With custom length
    config = CouponConfig(length=12)
    code = generate_code(config)
    print(f"12-character code: {code}")
    
    # Numeric only
    config = CouponConfig(format=CouponFormat.NUMERIC, length=10, include_checksum=False)
    code = generate_code(config)
    print(f"Numeric code: {code}")
    
    # Alpha only
    config = CouponConfig(format=CouponFormat.ALPHA, length=8, include_checksum=False)
    code = generate_code(config)
    print(f"Alpha code: {code}")


def example_02_prefix_suffix():
    """Example 2: Codes with prefix and suffix."""
    print("\n" + "="*60)
    print("Example 2: Codes with Prefix and Suffix")
    print("="*60)
    
    # Campaign prefix
    config = CouponConfig(prefix="SUMMER2024", length=8)
    code = generate_code(config)
    print(f"Campaign prefix: {code}")
    
    # Brand prefix with year suffix
    config = CouponConfig(prefix="BRAND", suffix="2024", length=6)
    code = generate_code(config)
    print(f"Brand prefix + year suffix: {code}")
    
    # Store location prefix
    config = CouponConfig(prefix="STORE-NYC", length=8)
    code = generate_code(config)
    print(f"Location prefix: {code}")


def example_03_phonetic_readable():
    """Example 3: Phonetic and readable codes."""
    print("\n" + "="*60)
    print("Example 3: Phonetic and Readable Codes")
    print("="*60)
    
    # Phonetic codes (easy to say)
    print("Phonetic codes (pronounceable):")
    for i in range(5):
        code = generate_phonetic_code("SAVE", 8)
        print(f"  {code}")
    
    # Readable codes (words + numbers)
    print("\nReadable codes (memorable words):")
    for i in range(5):
        code = generate_readable_code()
        print(f"  {code}")
    
    # Readable without number
    print("\nReadable codes (no numbers):")
    for i in range(5):
        code = generate_readable_code(number=False)
        print(f"  {code}")


def example_04_pattern_based():
    """Example 4: Pattern-based generation."""
    print("\n" + "="*60)
    print("Example 4: Pattern-Based Generation")
    print("="*60)
    
    patterns = [
        "SAVE-XXXX-9999",
        "COUPON-AAAA-9999-AAAA",
        "2024-****-****",
        "SUMMER-9X9X",
        "VIP-AAAA-AAAA",
    ]
    
    print("Custom pattern codes:")
    for pattern in patterns:
        code = generate_pattern_code(pattern)
        print(f"  Pattern: {pattern}")
        print(f"  Result:  {code}")
        print()


def example_05_batch_generation():
    """Example 5: Batch generation for campaigns."""
    print("\n" + "="*60)
    print("Example 5: Batch Generation for Campaigns")
    print("="*60)
    
    # Generate 10 unique codes
    print("10 standard codes:")
    codes = generate_codes(10)
    for code in codes:
        print(f"  {code}")
    
    # Generate with prefix
    print("\n5 codes with 'VIP' prefix:")
    config = CouponConfig(prefix="VIP", length=8)
    codes = generate_codes(5, config)
    for code in codes:
        print(f"  {code}")
    
    # Generate phonetic batch
    print("\n5 phonetic codes:")
    codes = generate_phonetic_codes(5, "GIFT")
    for code in codes:
        print(f"  {code}")


def example_06_validation():
    """Example 6: Coupon validation."""
    print("\n" + "="*60)
    print("Example 6: Coupon Validation")
    print("="*60)
    
    # Generate and validate
    config = CouponConfig(prefix="TEST", length=8, include_checksum=True)
    code = generate_code(config)
    
    print(f"Generated code: {code}")
    print(f"Valid: {validate_code(code, config)}")
    
    # Test invalid code
    invalid_code = "TEST-INVALID123"
    print(f"\nInvalid code: {invalid_code}")
    print(f"Valid: {validate_code(invalid_code, config)}")
    
    # Checksum validation
    clean_code = code.replace('-', '')
    print(f"\nChecksum test on: {clean_code}")
    print(f"Checksum valid: {validate_checksum(clean_code)}")


def example_07_percentage_discount():
    """Example 7: Percentage discount calculation."""
    print("\n" + "="*60)
    print("Example 7: Percentage Discount Calculation")
    print("="*60)
    
    config = DiscountConfig(
        discount_type=DiscountType.PERCENTAGE,
        value=25  # 25% off
    )
    
    amounts = [50, 100, 200, 500]
    
    print("25% discount:")
    for amount in amounts:
        result = calculate_discount(amount, config)
        print(f"  $${amount} → Discount: ${result.discount_amount}, Final: ${result.final_amount}")


def example_08_fixed_discount():
    """Example 8: Fixed discount calculation."""
    print("\n" + "="*60)
    print("Example 8: Fixed Discount Calculation")
    print("="*60)
    
    config = DiscountConfig(
        discount_type=DiscountType.FIXED,
        value=20  # $20 off
    )
    
    amounts = [15, 25, 50, 100]
    
    print("$20 fixed discount:")
    for amount in amounts:
        result = calculate_discount(amount, config)
        print(f"  ${amount} → Discount: ${result.discount_amount}, Final: ${result.final_amount}")
        print(f"    Message: {result.message}")


def example_09_min_purchase():
    """Example 9: Minimum purchase requirement."""
    print("\n" + "="*60)
    print("Example 9: Minimum Purchase Requirement")
    print("="*60)
    
    config = DiscountConfig(
        discount_type=DiscountType.PERCENTAGE,
        value=30,
        min_purchase=100  # Minimum $100 purchase
    )
    
    amounts = [50, 80, 100, 150]
    
    print("30% off, min purchase $100:")
    for amount in amounts:
        result = calculate_discount(amount, config)
        print(f"  ${amount}: {result.message}")
        print(f"    Applied: {result.applied}, Discount: ${result.discount_amount}")


def example_10_max_discount():
    """Example 10: Maximum discount cap."""
    print("\n" + "="*60)
    print("Example 10: Maximum Discount Cap")
    print("="*60)
    
    config = DiscountConfig(
        discount_type=DiscountType.PERCENTAGE,
        value=50,  # 50% off
        max_discount=100  # Max $100 discount
    )
    
    amounts = [100, 200, 300, 500]
    
    print("50% off, max discount $100:")
    for amount in amounts:
        result = calculate_discount(amount, config)
        print(f"  ${amount}: {result.message}")
        print(f"    Discount: ${result.discount_amount} (capped at $100)")


def example_11_bogo_discount():
    """Example 11: BOGO (Buy One Get One) discount."""
    print("\n" + "="*60)
    print("Example 11: BOGO Discount")
    print("="*60)
    
    config = DiscountConfig(discount_type=DiscountType.BOGO)
    
    # BOGO means every 2nd item is free
    scenarios = [
        (100, 1),   # 1 item at $100 - no discount
        (100, 2),   # 2 items at $100 total - 1 free ($50 discount)
        (100, 3),   # 3 items at $100 total - 1 free
        (100, 4),   # 4 items at $100 total - 2 free ($50 discount)
        (200, 6),   # 6 items at $200 total - 3 free
    ]
    
    print("BOGO: Buy One Get One Free:")
    for total, quantity in scenarios:
        result = calculate_discount(total, config, quantity)
        print(f"  {quantity} items, ${total} total → Discount: ${result.discount_amount}")
        print(f"    {result.message}")


def example_12_tiered_discount():
    """Example 12: Tiered discount based on amount."""
    print("\n" + "="*60)
    print("Example 12: Tiered Discount")
    print("="*60)
    
    # Discount tiers: spend more, save more
    tiers = [
        (100, 5),   # Spend $100+ → 5% off
        (200, 10),  # Spend $200+ → 10% off
        (500, 20),  # Spend $500+ → 20% off
        (1000, 30), # Spend $1000+ → 30% off
    ]
    
    amounts = [50, 150, 300, 600, 1200]
    
    print("Tiered discount:")
    print("  Tiers: $100→5%, $200→10%, $500→20%, $1000→30%")
    for amount in amounts:
        result = calculate_tiered_discount(amount, tiers)
        print(f"  ${amount}: {result.message}")
        print(f"    Discount: ${result.discount_amount}, Final: ${result.final_amount}")


def example_13_create_coupon():
    """Example 13: Creating complete coupon objects."""
    print("\n" + "="*60)
    print("Example 13: Creating Coupon Objects")
    print("="*60)
    
    # Percentage coupon
    coupon1 = create_coupon(
        "SAVE20",
        discount_type=DiscountType.PERCENTAGE,
        discount_value=20,
        min_purchase=50,
        expires_in_days=30
    )
    print(f"Coupon 1: {coupon1.code}")
    print(f"  Type: {coupon1.discount_config.discount_type.value}")
    print(f"  Value: {coupon1.discount_config.value}%")
    print(f"  Min purchase: ${coupon1.discount_config.min_purchase}")
    print(f"  Expires in: 30 days")
    print(f"  Valid: {coupon1.is_valid()}")
    
    # Fixed amount coupon
    coupon2 = create_coupon(
        "OFF10",
        discount_type=DiscountType.FIXED,
        discount_value=10,
        usage_limit=3
    )
    print(f"\nCoupon 2: {coupon2.code}")
    print(f"  Type: {coupon2.discount_config.discount_type.value}")
    print(f"  Value: ${coupon2.discount_config.value}")
    print(f"  Usage limit: {coupon2.usage_limit}")
    
    # Auto-generated code
    coupon3 = create_coupon(
        discount_type=DiscountType.PERCENTAGE,
        discount_value=15,
        expires_in_days=7
    )
    print(f"\nCoupon 3 (auto-generated): {coupon3.code}")
    print(f"  Type: {coupon3.discount_config.discount_type.value}")
    print(f"  Value: {coupon3.discount_config.value}%")
    print(f"  Expires in: 7 days")


def example_14_batch_coupons():
    """Example 14: Batch coupon creation."""
    print("\n" + "="*60)
    print("Example 14: Batch Coupon Creation")
    print("="*60)
    
    # Create 5 coupons with same settings
    coupons = create_coupons(
        count=5,
        discount_type=DiscountType.PERCENTAGE,
        discount_value=25,
        min_purchase=100,
        expires_in_days=30,
        prefix="SUMMER"
    )
    
    print("5 campaign coupons:")
    for coupon in coupons:
        print(f"  {coupon.code}: 25% off, min $100, expires in 30 days")


def example_15_apply_coupon():
    """Example 15: Applying coupons to purchases."""
    print("\n" + "="*60)
    print("Example 15: Applying Coupons")
    print("="*60)
    
    # Create coupon
    coupon = create_coupon(
        "VIP20",
        discount_type=DiscountType.PERCENTAGE,
        discount_value=20,
        min_purchase=100,
        usage_limit=2
    )
    
    print(f"Coupon: {coupon.code} (20% off, min $100)")
    print(f"Usage limit: {coupon.usage_limit}")
    
    # Apply to purchase
    amounts = [80, 150, 200]
    for amount in amounts:
        result, success = apply_coupon(coupon, amount)
        print(f"\n  Purchase: ${amount}")
        print(f"    Applied: {success}")
        print(f"    Message: {result.message}")
        print(f"    Discount: ${result.discount_amount}")
        print(f"    Final: ${result.final_amount}")
    
    print(f"\nUses remaining: {coupon.usage_limit - coupon.usage_count}")


def example_16_code_utilities():
    """Example 16: Code utilities."""
    print("\n" + "="*60)
    print("Example 16: Code Utilities")
    print("="*60)
    
    code = "SAVE-20-ABC-123"
    
    # Normalization
    normalized = normalize_code(code)
    print(f"Original: {code}")
    print(f"Normalized: {normalized}")
    
    # Formatting
    formatted = format_code("ABCDEFGHIJKL")
    print(f"\nFormatted (default): {formatted}")
    formatted2 = format_code("ABCDEFGHIJKL", group_size=3, separator=".")
    print(f"Formatted (custom): {formatted2}")
    
    # Masking
    masked = mask_code("ABCDEFGHIJKL")
    print(f"\nMasked: {masked}")
    
    # Strength analysis
    strength = code_strength("ABCD1234XYZ")
    print(f"\nCode strength analysis for 'ABCD1234XYZ':")
    print(f"  Length: {strength['length']}")
    print(f"  Unique chars: {strength['unique_chars']}")
    print(f"  Has uppercase: {strength['has_uppercase']}")
    print(f"  Has digits: {strength['has_digits']}")
    print(f"  Entropy bits: {strength['entropy_bits']}")
    print(f"  Rating: {strength['rating']}")


def example_17_ecommerce_scenario():
    """Example 17: E-commerce discount scenario."""
    print("\n" + "="*60)
    print("Example 17: E-commerce Scenario")
    print("="*60)
    
    # Create coupons for a sale event
    print("Creating Black Friday coupons...")
    
    black_friday_coupons = create_coupons(
        count=10,
        discount_type=DiscountType.PERCENTAGE,
        discount_value=40,
        min_purchase=200,
        max_discount=100,
        expires_in_days=7,
        prefix="BF2024"
    )
    
    print(f"Generated {len(black_friday_coupons)} coupons")
    
    # Simulate customer purchase
    coupon = black_friday_coupons[0]
    print(f"\nCustomer uses coupon: {coupon.code}")
    
    # Cart total
    cart_total = 300.0
    print(f"Cart total: ${cart_total}")
    
    # Apply coupon
    result, success = apply_coupon(coupon, cart_total)
    
    if success:
        print(f"  Discount applied: ${result.discount_amount}")
        print(f"  Final amount: ${result.final_amount}")
        print(f"  {result.message}")
    else:
        print(f"  Coupon not applied: {result.message}")


def example_18_loyalty_program():
    """Example 18: Loyalty program tiered rewards."""
    print("\n" + "="*60)
    print("Example 18: Loyalty Program Rewards")
    print("="*60)
    
    # Create tiered loyalty coupons
    tiers = [
        ("BRONZE", DiscountType.PERCENTAGE, 5, None),
        ("SILVER", DiscountType.PERCENTAGE, 10, 50),
        ("GOLD", DiscountType.PERCENTAGE, 15, 100),
        ("PLATINUM", DiscountType.PERCENTAGE, 20, 200),
    ]
    
    coupons = []
    for tier_name, discount_type, value, max_disc in tiers:
        coupon = create_coupon(
            f"{tier_name}REWARD",
            discount_type=discount_type,
            discount_value=value,
            max_discount=max_disc,
            usage_limit=100,  # Many uses for loyalty members
            expires_in_days=365
        )
        coupons.append(coupon)
        print(f"  {tier_name}: {coupon.code} - {value}% off, max ${max_disc or 'unlimited'}")
    
    # Test Gold member purchase
    gold_coupon = coupons[2]
    print(f"\nGold member purchase of $500:")
    result, success = apply_coupon(gold_coupon, 500.0)
    print(f"  Discount: ${result.discount_amount}")
    print(f"  Final: ${result.final_amount}")


def example_19_free_shipping():
    """Example 19: Free shipping coupon."""
    print("\n" + "="*60)
    print("Example 19: Free Shipping Coupon")
    print("="*60)
    
    # Free shipping coupon (typically $10-15 shipping cost)
    coupon = create_coupon(
        "FREESHIP",
        discount_type=DiscountType.FREE_SHIPPING,
        discount_value=15,  # $15 shipping fee
        min_purchase=75
    )
    
    print(f"Coupon: {coupon.code} - Free shipping on orders $75+")
    
    # Test different purchase amounts
    amounts = [50, 75, 100, 200]
    for amount in amounts:
        result, success = apply_coupon(coupon, amount)
        print(f"  ${amount}: {result.message}")
        if success:
            print(f"    Final (after free shipping): ${result.final_amount}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "="*60)
    print("COUPON UTILITIES - USAGE EXAMPLES")
    print("="*60)
    
    example_01_basic_generation()
    example_02_prefix_suffix()
    example_03_phonetic_readable()
    example_04_pattern_based()
    example_05_batch_generation()
    example_06_validation()
    example_07_percentage_discount()
    example_08_fixed_discount()
    example_09_min_purchase()
    example_10_max_discount()
    example_11_bogo_discount()
    example_12_tiered_discount()
    example_13_create_coupon()
    example_14_batch_coupons()
    example_15_apply_coupon()
    example_16_code_utilities()
    example_17_ecommerce_scenario()
    example_18_loyalty_program()
    example_19_free_shipping()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == '__main__':
    run_all_examples()