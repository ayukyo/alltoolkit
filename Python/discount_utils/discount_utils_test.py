#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Discount Utilities Test
=====================================
Comprehensive tests for discount_utils module.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Enums
    DiscountType, StackStrategy, TaxTiming,
    
    # Data classes
    Discount, TieredDiscount, BundleDiscount, PriceBreakdown,
    
    # Basic discount functions
    apply_percentage_discount,
    apply_fixed_discount,
    calculate_discount_amount,
    calculate_discount_percentage,
    calculate_original_price,
    
    # Multiple discount functions
    apply_sequential_discounts,
    apply_max_discount,
    apply_combined_discount,
    apply_weighted_discounts,
    apply_discount_with_strategy,
    
    # Tiered discount
    apply_tiered_discount,
    find_best_tier,
    suggest_upgrade_for_tier,
    
    # Bundle and Buy-X-Get-Y
    calculate_bundle_savings,
    apply_buy_x_get_y,
    calculate_free_items,
    
    # Tax calculations
    calculate_tax,
    apply_tax,
    calculate_price_with_tax_and_discount,
    
    # Profit and margin
    calculate_profit_margin,
    calculate_markup,
    calculate_cost_from_margin,
    calculate_break_even_discount,
    
    # Price comparison
    compare_prices,
    find_best_bulk_price,
    
    # Formatting
    format_price,
    format_percentage,
    format_savings,
    
    # Complete breakdown
    calculate_complete_breakdown,
    
    # Coupon validation
    validate_coupon,
    
    # Price history
    analyze_price_history,
    is_good_deal,
    
    # Constants
    COMMON_DISCOUNTS, TAX_RATES,
)


class TestBasicDiscountCalculations(unittest.TestCase):
    """Test basic discount calculation functions."""
    
    def test_apply_percentage_discount(self):
        """Test percentage discount application."""
        self.assertEqual(apply_percentage_discount(100, 20), 80.0)
        self.assertEqual(apply_percentage_discount(50, 10), 45.0)
        self.assertEqual(apply_percentage_discount(100, 0), 100.0)
        self.assertEqual(apply_percentage_discount(100, 100), 0.0)
        
        # Edge cases - invalid percentages are clamped
        self.assertEqual(apply_percentage_discount(100, -10), 100.0)  # Clamped to 0
        self.assertEqual(apply_percentage_discount(100, 150), 0.0)     # Clamped to 100
    
    def test_apply_fixed_discount(self):
        """Test fixed discount application."""
        self.assertEqual(apply_fixed_discount(100, 20), 80.0)
        self.assertEqual(apply_fixed_discount(30, 40), 0.0)  # Floor at 0
        self.assertEqual(apply_fixed_discount(100, 0), 100.0)
    
    def test_calculate_discount_amount(self):
        """Test discount amount calculation."""
        self.assertEqual(calculate_discount_amount(100, 20), 20.0)
        self.assertEqual(calculate_discount_amount(50, 10), 5.0)
    
    def test_calculate_discount_percentage(self):
        """Test discount percentage calculation."""
        self.assertEqual(calculate_discount_percentage(100, 80), 20.0)
        self.assertEqual(calculate_discount_percentage(100, 50), 50.0)
        self.assertEqual(calculate_discount_percentage(0, 0), 0)  # Edge case
    
    def test_calculate_original_price(self):
        """Test original price calculation."""
        self.assertEqual(calculate_original_price(80, 20), 100.0)
        self.assertEqual(calculate_original_price(45, 10), 50.0)
        self.assertEqual(calculate_original_price(0, 100), 0)


class TestMultipleDiscountHandling(unittest.TestCase):
    """Test multiple discount handling functions."""
    
    def test_apply_sequential_discounts(self):
        """Test sequential discount application."""
        # 10% then 10% = 100 * 0.9 * 0.9 = 81
        self.assertEqual(apply_sequential_discounts(100, [10, 10]), 81.0)
        # 20% then 30% = 100 * 0.8 * 0.7 = 56
        self.assertEqual(apply_sequential_discounts(100, [20, 30]), 56.0)
    
    def test_apply_max_discount(self):
        """Test max-only discount application."""
        self.assertEqual(apply_max_discount(100, [10, 20, 15]), 80.0)
        self.assertEqual(apply_max_discount(100, []), 100)  # Empty list
    
    def test_apply_combined_discount(self):
        """Test combined discount application."""
        # 10 + 20 + 30 = 60% total
        self.assertEqual(apply_combined_discount(100, [10, 20, 30]), 40.0)
        # Combined capped at 25%
        self.assertEqual(apply_combined_discount(100, [10, 20], 25), 75.0)
    
    def test_apply_weighted_discounts(self):
        """Test weighted discount application."""
        # Equal weights = average
        result = apply_weighted_discounts(100, [(20, 1.0), (10, 1.0)])
        self.assertEqual(result, 85.0)


class TestTieredDiscount(unittest.TestCase):
    """Test tiered discount functions."""
    
    def setUp(self):
        """Set up tiered discount for tests."""
        self.tiers = TieredDiscount([(100, 5), (500, 10), (1000, 15)])
    
    def test_apply_tiered_discount(self):
        """Test tiered discount application."""
        # Price 300: matches tier at 100 (5% discount)
        self.assertEqual(apply_tiered_discount(300, self.tiers), 285.0)
        # Price 1200: matches tier at 1000 (15% discount)
        self.assertEqual(apply_tiered_discount(1200, self.tiers), 1020.0)
        # Price 50: no tier applies
        self.assertEqual(apply_tiered_discount(50, self.tiers), 50.0)
    
    def test_find_best_tier(self):
        """Test finding best tier."""
        result = find_best_tier(300, self.tiers)
        self.assertEqual(result, (100, 5))
    
    def test_suggest_upgrade_for_tier(self):
        """Test upgrade suggestion."""
        result = suggest_upgrade_for_tier(300, self.tiers)
        self.assertEqual(result, (200, 10))
        
        # Already at highest tier
        result = suggest_upgrade_for_tier(1200, self.tiers)
        self.assertIsNone(result)


class TestBundleAndBuyXGetY(unittest.TestCase):
    """Test bundle and Buy-X-Get-Y functions."""
    
    def test_calculate_bundle_savings(self):
        """Test bundle savings calculation."""
        bundle = BundleDiscount([('Item1', 30), ('Item2', 20)], 40)
        savings = calculate_bundle_savings(bundle)
        self.assertEqual(savings['original_total'], 50)
        self.assertEqual(savings['bundle_price'], 40)
        self.assertEqual(savings['savings'], 10)
        self.assertEqual(savings['savings_percent'], 20.0)
    
    def test_apply_buy_x_get_y(self):
        """Test Buy X Get Y calculation."""
        # Buy 2 Get 1 free, 3 items at $10 each
        result = apply_buy_x_get_y(10, 3, 2, 1)
        self.assertEqual(result, 20.0)
        
        # Buy 2 Get 1 free, 5 items
        result = apply_buy_x_get_y(10, 5, 2, 1)
        self.assertEqual(result, 40.0)
        
        # Buy 2 Get 1 at 50% off
        result = apply_buy_x_get_y(10, 3, 2, 1, 50)
        self.assertEqual(result, 25.0)
    
    def test_calculate_free_items(self):
        """Test free items calculation."""
        self.assertEqual(calculate_free_items(3, 2, 1), 1)
        self.assertEqual(calculate_free_items(5, 2, 1), 1)
        self.assertEqual(calculate_free_items(6, 2, 1), 2)


class TestTaxCalculations(unittest.TestCase):
    """Test tax calculation functions."""
    
    def test_calculate_tax(self):
        """Test tax amount calculation."""
        self.assertEqual(calculate_tax(100, 10), 10.0)
        self.assertEqual(calculate_tax(50, 20), 10.0)
    
    def test_apply_tax(self):
        """Test tax application."""
        self.assertEqual(apply_tax(100, 10), 110.0)
    
    def test_calculate_price_with_tax_and_discount(self):
        """Test combined tax and discount calculation."""
        result = calculate_price_with_tax_and_discount(100, 20, 10)
        self.assertEqual(result['original'], 100)
        self.assertEqual(result['discount_amount'], 20.0)
        self.assertEqual(result['subtotal'], 80.0)
        self.assertEqual(result['tax'], 8.0)
        self.assertEqual(result['final'], 88.0)


class TestProfitMarginCalculations(unittest.TestCase):
    """Test profit and margin calculations."""
    
    def test_calculate_profit_margin(self):
        """Test profit margin calculation."""
        self.assertEqual(calculate_profit_margin(60, 100), 40.0)
        self.assertEqual(calculate_profit_margin(50, 100), 50.0)
    
    def test_calculate_markup(self):
        """Test markup calculation."""
        self.assertEqual(calculate_markup(60, 50), 90.0)
    
    def test_calculate_cost_from_margin(self):
        """Test cost from margin calculation."""
        self.assertEqual(calculate_cost_from_margin(100, 40), 60.0)
    
    def test_calculate_break_even_discount(self):
        """Test break-even discount calculation."""
        # Cost 60, Price 100, Min margin 10%
        result = calculate_break_even_discount(60, 100, 10)
        self.assertAlmostEqual(result, 33.33, places=2)


class TestPriceComparison(unittest.TestCase):
    """Test price comparison functions."""
    
    def test_compare_prices(self):
        """Test price comparison."""
        result = compare_prices([('Store A', 100, 10), ('Store B', 95, 0)])
        self.assertEqual(result['best_source'], 'Store A')
        self.assertEqual(result['best_price'], 90.0)
        self.assertEqual(result['savings_vs_worst'], 5.0)
    
    def test_find_best_bulk_price(self):
        """Test bulk price comparison."""
        result = find_best_bulk_price([(1, 10), (5, 40), (10, 70)])
        self.assertEqual(result[0], 10)
        self.assertEqual(result[1], 70)
        self.assertEqual(result[2], 7.0)


class TestFormatting(unittest.TestCase):
    """Test formatting functions."""
    
    def test_format_price(self):
        """Test price formatting."""
        self.assertEqual(format_price(1234.56), '$1,234.56')
        self.assertEqual(format_price(100, '¥', 0), '¥100')
    
    def test_format_percentage(self):
        """Test percentage formatting."""
        self.assertEqual(format_percentage(20.5), '20.5%')
        self.assertEqual(format_percentage(20.567, 2), '20.57%')
    
    def test_format_savings(self):
        """Test savings formatting."""
        result = format_savings(100, 80)
        self.assertIn('$20', result)
        self.assertIn('20.0%', result)


class TestCouponValidation(unittest.TestCase):
    """Test coupon validation functions."""
    
    def test_validate_coupon_min_purchase(self):
        """Test minimum purchase validation."""
        discount = Discount(DiscountType.PERCENTAGE, 10, 'Coupon', min_purchase=50)
        result = validate_coupon(discount, 30)
        self.assertFalse(result['valid'])
        self.assertIn('Minimum purchase', result['reason'])
        
        result = validate_coupon(discount, 60)
        self.assertTrue(result['valid'])
    
    def test_validate_coupon_expiration(self):
        """Test expiration validation."""
        discount = Discount(DiscountType.PERCENTAGE, 10, 'Coupon', expires='2024-12-31')
        result = validate_coupon(discount, 100, '2025-01-01')
        self.assertFalse(result['valid'])
        self.assertIn('expired', result['reason'])


class TestPriceHistory(unittest.TestCase):
    """Test price history functions."""
    
    def test_analyze_price_history(self):
        """Test price history analysis."""
        history = [('2024-01', 100), ('2024-02', 90), ('2024-03', 85)]
        result = analyze_price_history(history)
        self.assertEqual(result['lowest'], 85)
        self.assertEqual(result['highest'], 100)
        self.assertAlmostEqual(result['average'], 91.67, places=1)
        self.assertEqual(result['trend'], 'down')
    
    def test_is_good_deal(self):
        """Test good deal detection."""
        history = [('2024-01', 100), ('2024-02', 100), ('2024-03', 100)]
        result = is_good_deal(80, history)
        self.assertTrue(result['is_good_deal'])
        self.assertEqual(result['savings_vs_avg'], 20.0)


class TestCompleteBreakdown(unittest.TestCase):
    """Test complete price breakdown."""
    
    def test_calculate_complete_breakdown(self):
        """Test complete breakdown calculation."""
        d1 = Discount(DiscountType.PERCENTAGE, 10, 'Member')
        d2 = Discount(DiscountType.PERCENTAGE, 5, 'Coupon')
        result = calculate_complete_breakdown(100, [d1, d2], 10)
        
        self.assertEqual(result.original_price, 100)
        self.assertEqual(result.tax_rate, 10)
        # Sequential: 100 * 0.9 * 0.95 = 85.5
        self.assertEqual(result.subtotal_after_discount, 85.5)


class TestDataClasses(unittest.TestCase):
    """Test data classes."""
    
    def test_discount_dataclass(self):
        """Test Discount dataclass."""
        d = Discount(DiscountType.PERCENTAGE, 150)  # Over 100
        self.assertEqual(d.value, 100)  # Clamped
        
        d = Discount(DiscountType.FIXED, -10)  # Negative
        self.assertEqual(d.value, 0)  # Clamped
    
    def test_tiered_discount_dataclass(self):
        """Test TieredDiscount sorting."""
        tiers = TieredDiscount([(500, 10), (100, 5)])  # Unsorted
        self.assertEqual(tiers.tiers[0], (100, 5))  # Sorted


class TestConstants(unittest.TestCase):
    """Test module constants."""
    
    def test_common_discounts(self):
        """Test common discount constants."""
        self.assertEqual(COMMON_DISCOUNTS['half'], 50)
        self.assertEqual(COMMON_DISCOUNTS['minimal'], 5)
    
    def test_tax_rates(self):
        """Test tax rate constants."""
        self.assertEqual(TAX_RATES['NONE'], 0.0)
        self.assertGreater(TAX_RATES['UK'], 0)


if __name__ == '__main__':
    unittest.main()