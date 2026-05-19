#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Discount Utilities Tests
=====================================
Comprehensive tests for discount_utils module.
"""

import unittest
from mod import (
    # Enums
    DiscountType, StackStrategy, TaxTiming,
    # Data classes
    Discount, TieredDiscount, BundleDiscount, PriceBreakdown,
    # Basic calculations
    apply_percentage_discount, apply_fixed_discount,
    calculate_discount_amount, calculate_discount_percentage,
    calculate_original_price,
    # Multiple discounts
    apply_sequential_discounts, apply_max_discount,
    apply_combined_discount, apply_weighted_discounts,
    apply_discount_with_strategy,
    # Tiered
    apply_tiered_discount, find_best_tier, suggest_upgrade_for_tier,
    # Bundle and Buy X Get Y
    calculate_bundle_savings, apply_buy_x_get_y, calculate_free_items,
    # Tax
    calculate_tax, apply_tax, calculate_price_with_tax_and_discount,
    # Profit
    calculate_profit_margin, calculate_markup,
    calculate_cost_from_margin, calculate_break_even_discount,
    # Comparison
    compare_prices, find_best_bulk_price,
    # Formatting
    format_price, format_percentage, format_savings,
    # Complete
    calculate_complete_breakdown,
    # Validation
    validate_coupon,
    # History
    analyze_price_history, is_good_deal,
    # Constants
    COMMON_DISCOUNTS, TAX_RATES,
)


class TestBasicDiscountCalculations(unittest.TestCase):
    """Test basic discount calculations."""
    
    def test_apply_percentage_discount(self):
        self.assertEqual(apply_percentage_discount(100, 20), 80.0)
        self.assertEqual(apply_percentage_discount(100, 50), 50.0)
        self.assertEqual(apply_percentage_discount(100, 0), 100.0)
        self.assertEqual(apply_percentage_discount(100, 100), 0.0)
        
    def test_apply_percentage_discount_bounds(self):
        # Negative discount should be capped to 0
        self.assertEqual(apply_percentage_discount(100, -10), 100.0)
        # Discount > 100 should be capped to 100
        self.assertEqual(apply_percentage_discount(100, 150), 0.0)
        
    def test_apply_fixed_discount(self):
        self.assertEqual(apply_fixed_discount(100, 20), 80.0)
        self.assertEqual(apply_fixed_discount(50, 30), 20.0)
        
    def test_apply_fixed_discount_bounds(self):
        # Should not go below 0
        self.assertEqual(apply_fixed_discount(30, 40), 0.0)
        
    def test_calculate_discount_amount(self):
        self.assertEqual(calculate_discount_amount(100, 20), 20.0)
        self.assertEqual(calculate_discount_amount(200, 25), 50.0)
        
    def test_calculate_discount_percentage(self):
        self.assertEqual(calculate_discount_percentage(100, 80), 20.0)
        self.assertEqual(calculate_discount_percentage(100, 50), 50.0)
        self.assertEqual(calculate_discount_percentage(200, 180), 10.0)
        
    def test_calculate_original_price(self):
        self.assertEqual(calculate_original_price(80, 20), 100.0)
        self.assertEqual(calculate_original_price(45, 10), 50.0)


class TestMultipleDiscounts(unittest.TestCase):
    """Test multiple discount handling."""
    
    def test_apply_sequential_discounts(self):
        # 100 - 10% = 90, 90 - 10% = 81
        self.assertEqual(apply_sequential_discounts(100, [10, 10]), 81.0)
        # 100 - 20% = 80, 80 - 30% = 56
        self.assertEqual(apply_sequential_discounts(100, [20, 30]), 56.0)
        
    def test_apply_max_discount(self):
        self.assertEqual(apply_max_discount(100, [10, 20, 15]), 80.0)
        self.assertEqual(apply_max_discount(100, [5, 5, 5]), 95.0)
        
    def test_apply_combined_discount(self):
        # 10 + 20 + 30 = 60% combined
        self.assertEqual(apply_combined_discount(100, [10, 20, 30]), 40.0)
        # Combined capped at 25%
        self.assertEqual(apply_combined_discount(100, [10, 20], 25), 75.0)
        
    def test_apply_weighted_discounts(self):
        # (20 * 1.0 + 10 * 0.5) / 1.5 = 16.67%
        result = apply_weighted_discounts(100, [(20, 1.0), (10, 0.5)])
        self.assertAlmostEqual(result, 83.33, places=2)
        
    def test_apply_discount_with_strategy(self):
        d1 = Discount(DiscountType.PERCENTAGE, 10)
        d2 = Discount(DiscountType.PERCENTAGE, 20)
        
        # Sequential: 100 - 10% = 90, 90 - 20% = 72
        result = apply_discount_with_strategy(100, [d1, d2], StackStrategy.SEQUENTIAL)
        self.assertEqual(result, 72.0)
        
        # Max only
        result = apply_discount_with_strategy(100, [d1, d2], StackStrategy.MAX_ONLY)
        self.assertEqual(result, 80.0)
        
    def test_min_purchase_requirement(self):
        d = Discount(DiscountType.PERCENTAGE, 10, 'Member', min_purchase=50)
        # Price below min_purchase - discount not applied
        result = apply_discount_with_strategy(30, [d], StackStrategy.SEQUENTIAL)
        self.assertEqual(result, 30.0)
        # Price meets min_purchase - discount applied
        result = apply_discount_with_strategy(100, [d], StackStrategy.SEQUENTIAL)
        self.assertEqual(result, 90.0)


class TestTieredDiscount(unittest.TestCase):
    """Test tiered discount calculations."""
    
    def setUp(self):
        self.tiers = TieredDiscount([(100, 5), (500, 10), (1000, 15)])
    
    def test_apply_tiered_discount(self):
        # Below first tier - no discount
        self.assertEqual(apply_tiered_discount(50, self.tiers), 50.0)
        # In first tier
        self.assertEqual(apply_tiered_discount(300, self.tiers), 285.0)  # 5% off
        # In second tier
        self.assertEqual(apply_tiered_discount(800, self.tiers), 720.0)  # 10% off
        # In third tier
        self.assertEqual(apply_tiered_discount(1200, self.tiers), 1020.0)  # 15% off
        
    def test_find_best_tier(self):
        min_amount, discount = find_best_tier(300, self.tiers)
        self.assertEqual(min_amount, 100)
        self.assertEqual(discount, 5)
        
    def test_suggest_upgrade_for_tier(self):
        result = suggest_upgrade_for_tier(300, self.tiers)
        self.assertEqual(result, (200, 10))
        
        # Already at highest tier
        result = suggest_upgrade_for_tier(1500, self.tiers)
        self.assertIsNone(result)


class TestBundleDiscount(unittest.TestCase):
    """Test bundle discount calculations."""
    
    def test_bundle_savings(self):
        bundle = BundleDiscount([('Item1', 30), ('Item2', 20)], 40)
        savings = calculate_bundle_savings(bundle)
        
        self.assertEqual(savings['original_total'], 50)
        self.assertEqual(savings['bundle_price'], 40)
        self.assertEqual(savings['savings'], 10)
        self.assertEqual(savings['savings_percent'], 20.0)
        
    def test_bundle_discount_dataclass(self):
        bundle = BundleDiscount([('A', 100), ('B', 50), ('C', 25)], 150)
        self.assertEqual(bundle.savings(), 25)
        self.assertAlmostEqual(bundle.savings_percentage(), 14.29, places=2)


class TestBuyXGetY(unittest.TestCase):
    """Test Buy X Get Y promotion."""
    
    def test_apply_buy_x_get_y_free(self):
        # Buy 2 get 1 free, buying 3 items at $10 each
        # 3 items = 1 cycle (2 paid + 1 free)
        # Cost = 2 * $10 = $20
        self.assertEqual(apply_buy_x_get_y(10, 3, 2, 1), 20.0)
        
        # Buy 2 get 1 free, buying 5 items
        # 1 cycle (2 paid + 1 free) + 2 remaining (paid)
        # Cost = 2*10 + 2*10 = $40
        self.assertEqual(apply_buy_x_get_y(10, 5, 2, 1), 40.0)
        
        # Buy 2 get 1 free, buying 6 items
        # 2 cycles (4 paid + 2 free)
        # Cost = 4 * $10 = $40
        self.assertEqual(apply_buy_x_get_y(10, 6, 2, 1), 40.0)
        
    def test_apply_buy_x_get_y_partial_discount(self):
        # Buy 2 get 1 at 50% off
        self.assertEqual(apply_buy_x_get_y(10, 3, 2, 1, 50), 25.0)  # 2*10 + 1*5
        
    def test_calculate_free_items(self):
        self.assertEqual(calculate_free_items(3, 2, 1), 1)
        self.assertEqual(calculate_free_items(5, 2, 1), 1)
        self.assertEqual(calculate_free_items(6, 2, 1), 2)
        self.assertEqual(calculate_free_items(4, 2, 1), 1)  # 4 = 2 paid + 1 free + 1 paid


class TestTaxCalculations(unittest.TestCase):
    """Test tax calculations."""
    
    def test_calculate_tax(self):
        self.assertEqual(calculate_tax(100, 10), 10.0)
        self.assertEqual(calculate_tax(50, 20), 10.0)
        
    def test_apply_tax(self):
        self.assertEqual(apply_tax(100, 10), 110.0)
        
    def test_price_with_tax_and_discount_after(self):
        # Discount first, then tax
        result = calculate_price_with_tax_and_discount(100, 20, 10)
        self.assertEqual(result['original'], 100)
        self.assertEqual(result['discount_amount'], 20.0)
        self.assertEqual(result['subtotal'], 80.0)
        self.assertEqual(result['tax'], 8.0)
        self.assertEqual(result['final'], 88.0)
        
    def test_price_with_tax_and_discount_before(self):
        # Tax first, then discount
        result = calculate_price_with_tax_and_discount(
            100, 20, 10, TaxTiming.BEFORE_DISCOUNT
        )
        self.assertEqual(result['original'], 100)
        self.assertEqual(result['subtotal'], 110.0)  # Taxed price before discount


class TestProfitCalculations(unittest.TestCase):
    """Test profit and margin calculations."""
    
    def test_calculate_profit_margin(self):
        self.assertEqual(calculate_profit_margin(60, 100), 40.0)
        self.assertEqual(calculate_profit_margin(80, 100), 20.0)
        
    def test_calculate_markup(self):
        self.assertEqual(calculate_markup(60, 50), 90.0)
        self.assertEqual(calculate_markup(100, 25), 125.0)
        
    def test_calculate_cost_from_margin(self):
        self.assertEqual(calculate_cost_from_margin(100, 40), 60.0)
        
    def test_calculate_break_even_discount(self):
        # Cost 60, Price 100, Min margin 10%
        # Minimum price = 60 / 0.9 = 66.67
        # Max discount = (100 - 66.67) / 100 * 100 = 33.33%
        result = calculate_break_even_discount(60, 100, 10)
        self.assertAlmostEqual(result, 33.33, places=2)


class TestPriceComparison(unittest.TestCase):
    """Test price comparison functions."""
    
    def test_compare_prices(self):
        result = compare_prices([
            ('Store A', 100, 10),
            ('Store B', 95, 0),
            ('Store C', 98, 5),
        ])
        
        # Store A: 100 - 10% = 90
        # Store B: 95
        # Store C: 98 - 5% = 93.1
        self.assertEqual(result['best_source'], 'Store A')
        self.assertEqual(result['best_price'], 90.0)
        
    def test_find_best_bulk_price(self):
        result = find_best_bulk_price([(1, 10), (5, 40), (10, 70)])
        self.assertEqual(result, (10, 70, 7.0))


class TestFormatting(unittest.TestCase):
    """Test price formatting functions."""
    
    def test_format_price(self):
        self.assertEqual(format_price(1234.56), '$1,234.56')
        self.assertEqual(format_price(100, '¥', 0), '¥100')
        self.assertEqual(format_price(1000000.5), '$1,000,000.50')
        
    def test_format_percentage(self):
        self.assertEqual(format_percentage(20.5), '20.5%')
        self.assertEqual(format_percentage(20.567, 2), '20.57%')
        
    def test_format_savings(self):
        self.assertEqual(format_savings(100, 80), 'Save $20.00 (20.0%)')


class TestCompleteBreakdown(unittest.TestCase):
    """Test complete price breakdown."""
    
    def test_calculate_complete_breakdown(self):
        d1 = Discount(DiscountType.PERCENTAGE, 10, 'Member')
        d2 = Discount(DiscountType.PERCENTAGE, 5, 'Coupon')
        
        breakdown = calculate_complete_breakdown(100, [d1, d2], 10)
        
        self.assertEqual(breakdown.original_price, 100)
        # Sequential: 100 - 10% = 90, 90 - 5% = 85.5
        self.assertAlmostEqual(breakdown.subtotal_after_discount, 85.5, places=2)
        self.assertEqual(breakdown.tax_rate, 10)
        self.assertAlmostEqual(breakdown.tax_amount, 8.55, places=2)
        self.assertAlmostEqual(breakdown.final_price, 94.05, places=2)


class TestCouponValidation(unittest.TestCase):
    """Test coupon validation."""
    
    def test_validate_coupon_min_purchase(self):
        d = Discount(DiscountType.PERCENTAGE, 10, 'Coupon', min_purchase=50)
        
        result = validate_coupon(d, 30)
        self.assertFalse(result['valid'])
        
        result = validate_coupon(d, 100)
        self.assertTrue(result['valid'])
        
    def test_validate_coupon_expiration(self):
        d = Discount(DiscountType.PERCENTAGE, 10, 'Coupon', expires='2024-12-31')
        
        result = validate_coupon(d, 100, '2024-06-01')
        self.assertTrue(result['valid'])
        
        result = validate_coupon(d, 100, '2025-01-01')
        self.assertFalse(result['valid'])


class TestPriceHistory(unittest.TestCase):
    """Test price history analysis."""
    
    def test_analyze_price_history(self):
        history = [('2024-01', 100), ('2024-02', 90), ('2024-03', 85)]
        result = analyze_price_history(history)
        
        self.assertEqual(result['lowest'], 85)
        self.assertEqual(result['highest'], 100)
        self.assertEqual(result['trend'], 'down')
        
    def test_is_good_deal(self):
        history = [('2024-01', 100), ('2024-02', 100), ('2024-03', 100)]
        result = is_good_deal(80, history, 20)
        
        self.assertTrue(result['is_good_deal'])
        self.assertEqual(result['average'], 100)


class TestConstants(unittest.TestCase):
    """Test predefined constants."""
    
    def test_common_discounts(self):
        self.assertEqual(COMMON_DISCOUNTS['half'], 50)
        self.assertEqual(COMMON_DISCOUNTS['clearance'], 60)
        
    def test_tax_rates(self):
        self.assertEqual(TAX_RATES['UK'], 20.0)
        self.assertEqual(TAX_RATES['CN'], 13.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)