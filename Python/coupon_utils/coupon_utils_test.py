#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Coupon Utilities Test Suite

Comprehensive tests for coupon generation, validation, and discount calculation.

Author: AllToolkit
License: MIT
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from coupon_utils.mod import (
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


class TestCouponGeneration(unittest.TestCase):
    """Test coupon code generation functions."""
    
    def test_generate_code_default(self):
        """Test default code generation."""
        code = generate_code()
        # Default includes checksum and may have grouping
        clean_code = code.replace('-', '')
        self.assertTrue(clean_code.isalnum())
        self.assertGreaterEqual(len(clean_code), 8)
    
    def test_generate_code_with_prefix(self):
        """Test code generation with prefix."""
        config = CouponConfig(prefix="SAVE", length=8)
        code = generate_code(config)
        self.assertTrue(code.startswith("SAVE"))
    
    def test_generate_code_with_suffix(self):
        """Test code generation with suffix."""
        config = CouponConfig(suffix="2024", length=8)
        code = generate_code(config)
        self.assertTrue(code.endswith("2024"))
    
    def test_generate_code_numeric(self):
        """Test numeric-only code generation."""
        config = CouponConfig(
            format=CouponFormat.NUMERIC,
            length=8,
            include_checksum=False,
            group_size=0  # No separator
        )
        code = generate_code(config)
        self.assertTrue(code.isdigit())
    
    def test_generate_code_alpha(self):
        """Test alpha-only code generation."""
        config = CouponConfig(format=CouponFormat.ALPHA, length=8, include_checksum=False, group_size=0)
        code = generate_code(config)
        self.assertTrue(code.isalpha())
    
    def test_generate_code_phonetic(self):
        """Test phonetic code generation."""
        code = generate_phonetic_code("SAVE", 8)
        self.assertTrue(code.startswith("SAVE-"))
        # Should have alternating consonants and vowels
        core = code.split('-')[1]
        self.assertEqual(len(core), 8)
    
    def test_generate_readable_code(self):
        """Test readable code generation."""
        code = generate_readable_code()
        self.assertTrue(len(code) >= 4)  # At least one noun
        self.assertTrue(any(c.isdigit() for c in code))  # Has number suffix
    
    def test_generate_readable_code_no_number(self):
        """Test readable code without number."""
        code = generate_readable_code(number=False)
        self.assertTrue(code.isalpha())
    
    def test_generate_pattern_code(self):
        """Test pattern-based code generation."""
        # Use pattern with literals and X/9 patterns
        code = generate_pattern_code("CODE-XXXX-9999")
        self.assertTrue(code.startswith("CODE-"))
        parts = code.split('-')
        self.assertEqual(len(parts), 3)
        self.assertTrue(parts[2].isdigit())  # Last part should be digits
    
    def test_generate_codes_batch(self):
        """Test batch code generation."""
        codes = generate_codes(10)
        self.assertEqual(len(codes), 10)
        # All codes should be unique
        self.assertEqual(len(set(codes)), 10)
    
    def test_generate_codes_no_deduplicate(self):
        """Test batch generation without deduplication."""
        config = CouponConfig(length=4, include_checksum=False)
        codes = generate_codes(5, config, deduplicate=False)
        self.assertEqual(len(codes), 5)
    
    def test_generate_phonetic_codes_batch(self):
        """Test batch phonetic code generation."""
        codes = generate_phonetic_codes(5, "GIFT")
        self.assertEqual(len(codes), 5)
        for code in codes:
            self.assertTrue(code.startswith("GIFT-"))
    
    def test_generate_readable_codes_batch(self):
        """Test batch readable code generation."""
        codes = generate_readable_codes(5)
        self.assertEqual(len(codes), 5)
    
    def test_excluded_characters(self):
        """Test that excluded characters are not in generated codes."""
        config = CouponConfig(
            format=CouponFormat.ALPHANUMERIC,
            length=100,
            include_checksum=False,
            excluded_chars="0O1lI"
        )
        code = generate_code(config)
        for char in "0O1lI":
            self.assertNotIn(char, code)


class TestCouponValidation(unittest.TestCase):
    """Test coupon validation functions."""
    
    def test_validate_code_default(self):
        """Test validation of properly generated code."""
        code = generate_code()
        self.assertTrue(validate_code(code))
    
    def test_validate_code_with_prefix(self):
        """Test validation with prefix."""
        config = CouponConfig(prefix="SAVE", length=8)
        code = generate_code(config)
        self.assertTrue(validate_code(code, config))
    
    def test_validate_code_wrong_prefix(self):
        """Test validation fails with wrong prefix."""
        config = CouponConfig(prefix="SAVE", length=8)
        code = generate_code(config)
        self.assertFalse(validate_code("GIFT" + code[4:], config))
    
    def test_validate_code_wrong_length(self):
        """Test validation fails with wrong length."""
        config = CouponConfig(length=8, include_checksum=False)
        self.assertFalse(validate_code("ABCD", config))  # Too short
    
    def test_validate_checksum(self):
        """Test checksum validation."""
        config = CouponConfig(include_checksum=True, length=8)
        code = generate_code(config)
        clean_code = code.replace('-', '')
        self.assertTrue(validate_checksum(clean_code))
    
    def test_validate_checksum_invalid(self):
        """Test invalid checksum detection."""
        self.assertFalse(validate_checksum("ABCD123X"))  # Wrong checksum


class TestDiscountCalculation(unittest.TestCase):
    """Test discount calculation functions."""
    
    def test_percentage_discount(self):
        """Test percentage discount calculation."""
        config = DiscountConfig(discount_type=DiscountType.PERCENTAGE, value=20)
        result = calculate_discount(100.0, config)
        self.assertEqual(result.discount_amount, 20.0)
        self.assertEqual(result.final_amount, 80.0)
        self.assertTrue(result.applied)
    
    def test_fixed_discount(self):
        """Test fixed discount calculation."""
        config = DiscountConfig(discount_type=DiscountType.FIXED, value=15)
        result = calculate_discount(100.0, config)
        self.assertEqual(result.discount_amount, 15.0)
        self.assertEqual(result.final_amount, 85.0)
    
    def test_fixed_discount_exceeds_amount(self):
        """Test fixed discount capped at amount."""
        config = DiscountConfig(discount_type=DiscountType.FIXED, value=150)
        result = calculate_discount(100.0, config)
        self.assertEqual(result.discount_amount, 100.0)
        self.assertEqual(result.final_amount, 0.0)
    
    def test_min_purchase_not_met(self):
        """Test minimum purchase requirement."""
        config = DiscountConfig(
            discount_type=DiscountType.PERCENTAGE,
            value=20,
            min_purchase=100
        )
        result = calculate_discount(50.0, config)
        self.assertEqual(result.discount_amount, 0.0)
        self.assertFalse(result.applied)
    
    def test_min_purchase_met(self):
        """Test minimum purchase met."""
        config = DiscountConfig(
            discount_type=DiscountType.PERCENTAGE,
            value=20,
            min_purchase=100
        )
        result = calculate_discount(100.0, config)
        self.assertEqual(result.discount_amount, 20.0)
        self.assertTrue(result.applied)
    
    def test_max_discount_cap(self):
        """Test maximum discount cap."""
        config = DiscountConfig(
            discount_type=DiscountType.PERCENTAGE,
            value=50,
            max_discount=30
        )
        result = calculate_discount(100.0, config)
        self.assertEqual(result.discount_amount, 30.0)  # Capped at 30
    
    def test_bogo_discount(self):
        """Test BOGO discount calculation."""
        config = DiscountConfig(discount_type=DiscountType.BOGO)
        # 4 items at $25 each = $100 total, BOGO gives 2 free = $50 discount
        result = calculate_discount(100.0, config, quantity=4)
        self.assertEqual(result.discount_amount, 50.0)
    
    def test_bogo_single_item(self):
        """Test BOGO with single item (no discount)."""
        config = DiscountConfig(discount_type=DiscountType.BOGO)
        result = calculate_discount(50.0, config, quantity=1)
        self.assertEqual(result.discount_amount, 0.0)
        self.assertFalse(result.applied)
    
    def test_free_shipping_discount(self):
        """Test free shipping discount."""
        config = DiscountConfig(
            discount_type=DiscountType.FREE_SHIPPING,
            value=10
        )
        result = calculate_discount(100.0, config)
        self.assertEqual(result.discount_amount, 10.0)
    
    def test_tiered_discount(self):
        """Test tiered discount calculation."""
        tiers = [(100, 5), (200, 10), (500, 20)]
        
        # Below first tier
        result = calculate_tiered_discount(50, tiers)
        self.assertEqual(result.discount_amount, 0.0)
        
        # First tier
        result = calculate_tiered_discount(150, tiers)
        self.assertEqual(result.discount_value, 5)
        self.assertEqual(result.discount_amount, 7.5)
        
        # Second tier
        result = calculate_tiered_discount(300, tiers)
        self.assertEqual(result.discount_value, 10)
        self.assertEqual(result.discount_amount, 30.0)
        
        # Third tier
        result = calculate_tiered_discount(600, tiers)
        self.assertEqual(result.discount_value, 20)
        self.assertEqual(result.discount_amount, 120.0)


class TestCouponManagement(unittest.TestCase):
    """Test coupon creation and management functions."""
    
    def test_create_coupon_default(self):
        """Test default coupon creation."""
        coupon = create_coupon()
        self.assertIsNotNone(coupon.code)
        self.assertTrue(coupon.is_valid())
    
    def test_create_coupon_with_code(self):
        """Test coupon creation with specific code."""
        coupon = create_coupon("SAVE20")
        self.assertEqual(coupon.code, "SAVE20")
    
    def test_create_coupon_percentage(self):
        """Test percentage discount coupon."""
        coupon = create_coupon(
            "PERCENT20",
            discount_type=DiscountType.PERCENTAGE,
            discount_value=20
        )
        self.assertEqual(coupon.discount_config.discount_type, DiscountType.PERCENTAGE)
        self.assertEqual(coupon.discount_config.value, 20)
    
    def test_create_coupon_fixed(self):
        """Test fixed discount coupon."""
        coupon = create_coupon(
            "FIXED10",
            discount_type=DiscountType.FIXED,
            discount_value=10
        )
        self.assertEqual(coupon.discount_config.discount_type, DiscountType.FIXED)
    
    def test_create_coupon_with_expiry(self):
        """Test coupon with expiry date."""
        coupon = create_coupon(expires_in_days=30)
        self.assertIsNotNone(coupon.expires_at)
    
    def test_create_coupon_no_expiry(self):
        """Test coupon without expiry."""
        coupon = create_coupon(expires_in_days=None)
        self.assertIsNone(coupon.expires_at)
    
    def test_coupon_usage_limit(self):
        """Test coupon usage limit."""
        coupon = create_coupon(usage_limit=3)
        self.assertEqual(coupon.usage_limit, 3)
        self.assertEqual(coupon.usage_count, 0)
        
        # Use coupon multiple times
        self.assertTrue(coupon.use())
        self.assertEqual(coupon.usage_count, 1)
        self.assertTrue(coupon.use())
        self.assertEqual(coupon.usage_count, 2)
        self.assertTrue(coupon.use())
        self.assertEqual(coupon.usage_count, 3)
        self.assertEqual(coupon.status, CouponStatus.USED)
        
        # Can't use anymore
        self.assertFalse(coupon.use())
    
    def test_create_coupons_batch(self):
        """Test batch coupon creation."""
        coupons = create_coupons(5, prefix="SAVE")
        self.assertEqual(len(coupons), 5)
        # All codes should be unique
        codes = [c.code for c in coupons]
        self.assertEqual(len(set(codes)), 5)
    
    def test_apply_coupon_valid(self):
        """Test applying a valid coupon."""
        coupon = create_coupon("TEST20", DiscountType.PERCENTAGE, 20)
        result, success = apply_coupon(coupon, 100.0)
        self.assertTrue(success)
        self.assertEqual(result.discount_amount, 20.0)
    
    def test_apply_coupon_invalid(self):
        """Test applying an invalid coupon."""
        coupon = create_coupon("TEST", usage_limit=1)
        coupon.use()  # Mark as used
        
        result, success = apply_coupon(coupon, 100.0)
        self.assertFalse(success)
        self.assertEqual(result.discount_amount, 0.0)
    
    def test_coupon_metadata(self):
        """Test coupon metadata."""
        coupon = create_coupon(
            "META",
            metadata={"campaign": "summer2024", "source": "email"}
        )
        self.assertEqual(coupon.metadata["campaign"], "summer2024")
        self.assertEqual(coupon.metadata["source"], "email")


class TestCouponUtilities(unittest.TestCase):
    """Test coupon utility functions."""
    
    def test_normalize_code(self):
        """Test code normalization."""
        self.assertEqual(normalize_code("SAVE-20-ABC"), "SAVE20ABC")
        self.assertEqual(normalize_code("save_20_abc"), "SAVE20ABC")
        self.assertEqual(normalize_code("save 20 abc"), "SAVE20ABC")
    
    def test_format_code(self):
        """Test code formatting."""
        self.assertEqual(format_code("ABCDEFGHIJ"), "ABCD-EFGH-IJ")
        self.assertEqual(format_code("ABCD", group_size=2), "AB-CD")
    
    def test_mask_code(self):
        """Test code masking."""
        # For 10 chars with visible_chars=4: ABCD (4) + middle (2) + GHIJ (4)
        self.assertEqual(mask_code("ABCDEFGHIJ"), "ABCD**GHIJ")
        # For 12 chars: ABCD (4) + middle (4) + IJKL (4)
        self.assertEqual(mask_code("ABCDEFGHIJKL"), "ABCD****IJKL")
        self.assertEqual(mask_code("ABCD"), "ABCD")  # Too short to mask
    
    def test_code_strength(self):
        """Test code strength analysis."""
        strength = code_strength("ABCD1234")
        self.assertEqual(strength["length"], 8)
        self.assertTrue(strength["has_uppercase"])
        self.assertTrue(strength["has_digits"])
        self.assertIn(strength["rating"], ["weak", "fair", "good", "strong"])
    
    def test_code_strength_weak(self):
        """Test weak code strength."""
        strength = code_strength("AAAA")
        self.assertEqual(strength["rating"], "weak")
    
    def test_code_entropy(self):
        """Test entropy calculation."""
        strength = code_strength("ABCD1234")
        self.assertGreater(strength["entropy_bits"], 0)


class TestCouponDataClasses(unittest.TestCase):
    """Test coupon data class behavior."""
    
    def test_coupon_is_valid(self):
        """Test Coupon.is_valid() method."""
        coupon = Coupon(
            code="TEST",
            discount_config=DiscountConfig(),
            usage_limit=1
        )
        self.assertTrue(coupon.is_valid())
    
    def test_coupon_is_valid_expired(self):
        """Test Coupon.is_valid() with expired coupon."""
        from datetime import datetime, timedelta
        
        coupon = Coupon(
            code="TEST",
            discount_config=DiscountConfig(),
            expires_at=datetime.now() - timedelta(days=1)
        )
        self.assertFalse(coupon.is_valid())
    
    def test_coupon_is_valid_used(self):
        """Test Coupon.is_valid() with used coupon."""
        coupon = Coupon(
            code="TEST",
            discount_config=DiscountConfig(),
            status=CouponStatus.USED
        )
        self.assertFalse(coupon.is_valid())
    
    def test_coupon_use_success(self):
        """Test Coupon.use() success."""
        coupon = Coupon(
            code="TEST",
            discount_config=DiscountConfig(),
            usage_limit=2
        )
        self.assertTrue(coupon.use())
        self.assertEqual(coupon.usage_count, 1)
        self.assertEqual(coupon.status, CouponStatus.ACTIVE)
    
    def test_coupon_use_limit_reached(self):
        """Test Coupon.use() limit reached."""
        coupon = Coupon(
            code="TEST",
            discount_config=DiscountConfig(),
            usage_limit=1
        )
        self.assertTrue(coupon.use())
        self.assertEqual(coupon.status, CouponStatus.USED)
        self.assertFalse(coupon.use())


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_zero_amount(self):
        """Test discount on zero amount."""
        config = DiscountConfig(discount_type=DiscountType.PERCENTAGE, value=20)
        result = calculate_discount(0.0, config)
        self.assertEqual(result.discount_amount, 0.0)
        self.assertEqual(result.final_amount, 0.0)
    
    def test_negative_amount(self):
        """Test discount on negative amount (edge case)."""
        config = DiscountConfig(discount_type=DiscountType.PERCENTAGE, value=20)
        result = calculate_discount(-10.0, config)
        # Implementation allows negative, but discount is calculated
        self.assertEqual(result.original_amount, -10.0)
    
    def test_empty_pattern(self):
        """Test empty pattern generation."""
        code = generate_pattern_code("")
        self.assertEqual(code, "")
    
    def test_literal_pattern(self):
        """Test pattern with only literals."""
        # Use pattern without pattern characters (A, a, X, 9, *)
        code = generate_pattern_code("HELLO-WORLD")
        self.assertEqual(code, "HELLO-WORLD")
    
    def test_large_batch_generation(self):
        """Test large batch generation."""
        codes = generate_codes(100)
        self.assertEqual(len(codes), 100)
        self.assertEqual(len(set(codes)), 100)  # All unique
    
    def test_very_long_code(self):
        """Test very long code generation."""
        config = CouponConfig(length=100, include_checksum=False, group_size=0)
        code = generate_code(config)
        self.assertEqual(len(code), 100)
    
    def test_custom_charset(self):
        """Test custom character set."""
        config = CouponConfig(
            length=10,
            include_checksum=False,
            group_size=0,  # No grouping/separator
            custom_charset="ABC123"
        )
        code = generate_code(config)
        for char in code:
            self.assertIn(char, "ABC123")


if __name__ == '__main__':
    unittest.main(verbosity=2)