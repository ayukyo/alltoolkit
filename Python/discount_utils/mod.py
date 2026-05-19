#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Discount Utilities Module
========================================
A comprehensive discount and price calculation utility module with zero external dependencies.

Features:
    - Single discount calculation (percentage and fixed amount)
    - Multiple discount stacking strategies
    - Tiered/progressive discount calculation
    - Tax calculation (before/after discount)
    - Price comparison and best deal finder
    - Bundle discount calculation
    - Coupon and promotion code validation
    - Profit margin and markup calculations
    - Price history and trend analysis
    - Currency formatting utilities

Author: AllToolkit Contributors
License: MIT
"""

import math
from typing import Union, List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Constants
# ============================================================================

# Common discount percentages
COMMON_DISCOUNTS = {
    'minimal': 5,
    'small': 10,
    'medium': 15,
    'standard': 20,
    'large': 25,
    'significant': 30,
    'major': 40,
    'half': 50,
    'clearance': 60,
    'deep': 70,
    'liquidation': 80,
    'fire_sale': 90,
}

# Common tax rates by region (approximate)
TAX_RATES = {
    'US_CA': 7.25,      # California
    'US_TX': 6.25,      # Texas
    'US_NY': 8.0,       # New York
    'US_FL': 6.0,       # Florida
    'UK': 20.0,         # UK VAT
    'DE': 19.0,         # Germany VAT
    'FR': 20.0,         # France VAT
    'JP': 10.0,         # Japan consumption tax
    'CN': 13.0,         # China VAT (standard)
    'AU': 10.0,         # Australia GST
    'CA': 5.0,          # Canada GST
    'SG': 8.0,          # Singapore GST
    'IN': 18.0,         # India GST (standard)
    'NONE': 0.0,        # No tax
}


# ============================================================================
# Enums
# ============================================================================

class DiscountType(Enum):
    """Discount type enumeration."""
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'
    TIERED = 'tiered'
    BUNDLE = 'bundle'
    BUY_X_GET_Y = 'buy_x_get_y'


class StackStrategy(Enum):
    """Discount stacking strategy."""
    SEQUENTIAL = 'sequential'      # Apply discounts one after another
    MAX_ONLY = 'max_only'          # Apply only the largest discount
    COMBINED = 'combined'          # Combine all discounts (capped at certain limit)
    WEIGHTED = 'weighted'          # Apply discounts with weights


class TaxTiming(Enum):
    """When to apply tax."""
    BEFORE_DISCOUNT = 'before_discount'
    AFTER_DISCOUNT = 'after_discount'


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Discount:
    """Single discount representation."""
    type: DiscountType
    value: float
    name: Optional[str] = None
    min_purchase: Optional[float] = None  # Minimum purchase amount to qualify
    max_discount: Optional[float] = None  # Maximum discount amount cap
    expires: Optional[str] = None         # Expiration date (YYYY-MM-DD format)
    
    def __post_init__(self):
        """Validate discount values."""
        if self.type == DiscountType.PERCENTAGE:
            self.value = max(0, min(100, self.value))
        elif self.type == DiscountType.FIXED:
            self.value = max(0, self.value)


@dataclass
class PriceBreakdown:
    """Detailed price breakdown."""
    original_price: float
    discounts_applied: List[Tuple[str, float]]
    subtotal_after_discount: float
    tax_rate: float
    tax_amount: float
    final_price: float
    total_savings: float
    savings_percentage: float


@dataclass
class TieredDiscount:
    """Tiered discount configuration."""
    tiers: List[Tuple[float, float]]  # (min_amount, discount_percent)
    name: Optional[str] = None
    
    def __post_init__(self):
        """Sort tiers by minimum amount."""
        self.tiers = sorted(self.tiers, key=lambda x: x[0])


@dataclass
class BundleDiscount:
    """Bundle discount configuration."""
    items: List[Tuple[str, float]]  # (item_name, original_price)
    bundle_price: float
    name: Optional[str] = None
    
    def savings(self) -> float:
        """Calculate bundle savings."""
        total_original = sum(price for _, price in self.items)
        return total_original - self.bundle_price
    
    def savings_percentage(self) -> float:
        """Calculate savings percentage."""
        total_original = sum(price for _, price in self.items)
        if total_original == 0:
            return 0
        return (self.savings() / total_original) * 100


# ============================================================================
# Basic Discount Calculations
# ============================================================================

def apply_percentage_discount(price: float, discount_percent: float) -> float:
    """
    Apply a percentage discount to a price.
    
    Args:
        price: Original price
        discount_percent: Discount percentage (0-100)
    
    Returns:
        Price after discount
    
    Examples:
        >>> apply_percentage_discount(100, 20)
        80.0
        >>> apply_percentage_discount(50, 10)
        45.0
    """
    discount_percent = max(0, min(100, discount_percent))
    return price * (1 - discount_percent / 100)


def apply_fixed_discount(price: float, discount_amount: float) -> float:
    """
    Apply a fixed amount discount to a price.
    
    Args:
        price: Original price
        discount_amount: Discount amount to subtract
    
    Returns:
        Price after discount (minimum 0)
    
    Examples:
        >>> apply_fixed_discount(100, 20)
        80.0
        >>> apply_fixed_discount(30, 40)
        0.0
    """
    return max(0, price - discount_amount)


def calculate_discount_amount(price: float, discount_percent: float) -> float:
    """
    Calculate the discount amount from a percentage.
    
    Args:
        price: Original price
        discount_percent: Discount percentage
    
    Returns:
        Discount amount
    
    Examples:
        >>> calculate_discount_amount(100, 20)
        20.0
    """
    return price * discount_percent / 100


def calculate_discount_percentage(original: float, discounted: float) -> float:
    """
    Calculate the discount percentage from original and discounted prices.
    
    Args:
        original: Original price
        discounted: Discounted price
    
    Returns:
        Discount percentage
    
    Examples:
        >>> calculate_discount_percentage(100, 80)
        20.0
        >>> calculate_discount_percentage(100, 50)
        50.0
    """
    if original <= 0:
        return 0
    return ((original - discounted) / original) * 100


def calculate_original_price(discounted: float, discount_percent: float) -> float:
    """
    Calculate original price from discounted price and discount percentage.
    
    Args:
        discounted: Discounted price
        discount_percent: Discount percentage applied
    
    Returns:
        Original price before discount
    
    Examples:
        >>> calculate_original_price(80, 20)
        100.0
        >>> calculate_original_price(45, 10)
        50.0
    """
    if discount_percent >= 100:
        return 0
    return discounted / (1 - discount_percent / 100)


# ============================================================================
# Multiple Discount Handling
# ============================================================================

def apply_sequential_discounts(price: float, discounts: List[float]) -> float:
    """
    Apply multiple percentage discounts sequentially.
    
    Each discount is applied to the price after previous discounts.
    Total savings can exceed single discount equivalent.
    
    Args:
        price: Original price
        discounts: List of discount percentages
    
    Returns:
        Final price after all discounts
    
    Examples:
        >>> apply_sequential_discounts(100, [10, 10])
        81.0
        >>> apply_sequential_discounts(100, [20, 30])
        56.0
    """
    for discount in discounts:
        price = apply_percentage_discount(price, discount)
    return price


def apply_max_discount(price: float, discounts: List[float]) -> float:
    """
    Apply only the largest discount.
    
    Args:
        price: Original price
        discounts: List of discount percentages
    
    Returns:
        Price after largest discount
    
    Examples:
        >>> apply_max_discount(100, [10, 20, 15])
        80.0
    """
    if not discounts:
        return price
    max_discount = max(discounts)
    return apply_percentage_discount(price, max_discount)


def apply_combined_discount(price: float, 
                             discounts: List[float],
                             max_combined: float = 100) -> float:
    """
    Combine multiple discounts with a cap.
    
    Args:
        price: Original price
        discounts: List of discount percentages
        max_combined: Maximum combined discount (default 100)
    
    Returns:
        Price after combined discount
    
    Examples:
        >>> apply_combined_discount(100, [10, 20, 30], 100)
        40.0
        >>> apply_combined_discount(100, [10, 20], 25)
        75.0
    """
    total_discount = sum(discounts)
    capped_discount = min(total_discount, max_combined)
    return apply_percentage_discount(price, capped_discount)


def apply_weighted_discounts(price: float,
                             discounts: List[Tuple[float, float]],
                             max_total: float = 100) -> float:
    """
    Apply weighted discounts.
    
    Args:
        price: Original price
        discounts: List of (discount_percent, weight) tuples
        max_total: Maximum total discount percentage
    
    Returns:
        Price after weighted discounts
    
    Examples:
        >>> apply_weighted_discounts(100, [(20, 1.0), (10, 0.5)])
        70.0
    """
    total_weight = sum(weight for _, weight in discounts)
    if total_weight == 0:
        return price
    
    weighted_sum = sum(d * w for d, w in discounts)
    effective_discount = weighted_sum / total_weight
    effective_discount = min(effective_discount, max_total)
    
    return apply_percentage_discount(price, effective_discount)


def apply_discount_with_strategy(price: float,
                                  discounts: List[Discount],
                                  strategy: StackStrategy = StackStrategy.SEQUENTIAL,
                                  max_total_discount: float = 100) -> float:
    """
    Apply multiple discounts using specified strategy.
    
    Args:
        price: Original price
        discounts: List of Discount objects
        strategy: Stacking strategy to use
        max_total_discount: Maximum total discount percentage
    
    Returns:
        Final price
    
    Examples:
        >>> d1 = Discount(DiscountType.PERCENTAGE, 10)
        >>> d2 = Discount(DiscountType.PERCENTAGE, 20)
        >>> apply_discount_with_strategy(100, [d1, d2], StackStrategy.SEQUENTIAL)
        72.0
    """
    # Filter valid discounts (min purchase requirement)
    valid_discounts = []
    for d in discounts:
        if d.min_purchase and price < d.min_purchase:
            continue
        
        discount_value = d.value
        if d.type == DiscountType.FIXED:
            # Convert fixed to percentage for comparison
            discount_value = (d.value / price) * 100 if price > 0 else 0
        
        # Apply cap if specified
        if d.max_discount and d.type == DiscountType.PERCENTAGE:
            max_percent = (d.max_discount / price) * 100 if price > 0 else 0
            discount_value = min(discount_value, max_percent)
        
        valid_discounts.append(discount_value)
    
    if not valid_discounts:
        return price
    
    # Apply strategy
    if strategy == StackStrategy.SEQUENTIAL:
        return apply_sequential_discounts(price, valid_discounts)
    elif strategy == StackStrategy.MAX_ONLY:
        return apply_max_discount(price, valid_discounts)
    elif strategy == StackStrategy.COMBINED:
        return apply_combined_discount(price, valid_discounts, max_total_discount)
    elif strategy == StackStrategy.WEIGHTED:
        # Equal weights for all discounts
        weighted = [(d, 1.0) for d in valid_discounts]
        return apply_weighted_discounts(price, weighted, max_total_discount)
    
    return price


# ============================================================================
# Tiered Discount Calculations
# ============================================================================

def apply_tiered_discount(price: float, tiers: TieredDiscount) -> float:
    """
    Apply tiered discount based on purchase amount.
    
    Args:
        price: Original price
        tiers: TieredDiscount configuration
    
    Returns:
        Price after applicable tier discount
    
    Examples:
        >>> tiers = TieredDiscount([(100, 5), (500, 10), (1000, 15)])
        >>> apply_tiered_discount(300, tiers)
        285.0
        >>> apply_tiered_discount(1200, tiers)
        1020.0
    """
    applicable_discount = 0
    
    for min_amount, discount_percent in tiers.tiers:
        if price >= min_amount:
            applicable_discount = discount_percent
    
    return apply_percentage_discount(price, applicable_discount)


def find_best_tier(price: float, tiers: TieredDiscount) -> Tuple[float, float]:
    """
    Find the best applicable discount tier for a given price.
    
    Args:
        price: Original price
        tiers: TieredDiscount configuration
    
    Returns:
        Tuple of (min_amount_for_next_tier, discount_percent_for_next_tier)
        Returns (0, 0) if no tier applies
    
    Examples:
        >>> tiers = TieredDiscount([(100, 5), (500, 10)])
        >>> find_best_tier(300, tiers)
        (100, 5)
    """
    applicable_discount = 0
    applicable_min = 0
    
    for min_amount, discount_percent in tiers.tiers:
        if price >= min_amount:
            applicable_discount = discount_percent
            applicable_min = min_amount
    
    return (applicable_min, applicable_discount)


def suggest_upgrade_for_tier(price: float, tiers: TieredDiscount) -> Optional[Tuple[float, float]]:
    """
    Suggest amount needed to reach next discount tier.
    
    Args:
        price: Original price
        tiers: TieredDiscount configuration
    
    Returns:
        Tuple of (additional_amount_needed, next_discount_percent)
        None if already at highest tier
    
    Examples:
        >>> tiers = TieredDiscount([(100, 5), (500, 10)])
        >>> suggest_upgrade_for_tier(300, tiers)
        (200, 10)
    """
    next_tier_min = None
    next_tier_discount = None
    
    for min_amount, discount_percent in tiers.tiers:
        if price < min_amount:
            next_tier_min = min_amount
            next_tier_discount = discount_percent
            break
    
    if next_tier_min is None:
        return None
    
    additional_needed = next_tier_min - price
    return (additional_needed, next_tier_discount)


# ============================================================================
# Bundle and Buy-X-Get-Y Discounts
# ============================================================================

def calculate_bundle_savings(bundle: BundleDiscount) -> Dict[str, float]:
    """
    Calculate bundle discount details.
    
    Args:
        bundle: BundleDiscount configuration
    
    Returns:
        Dictionary with savings details
    
    Examples:
        >>> bundle = BundleDiscount([('Item1', 30), ('Item2', 20)], 40)
        >>> calculate_bundle_savings(bundle)
        {'original_total': 50, 'bundle_price': 40, 'savings': 10, 'savings_percent': 20.0}
    """
    original_total = sum(price for _, price in bundle.items)
    savings = bundle.savings()
    savings_percent = bundle.savings_percentage()
    
    return {
        'original_total': original_total,
        'bundle_price': bundle.bundle_price,
        'savings': savings,
        'savings_percent': savings_percent,
        'items_count': len(bundle.items),
    }


def apply_buy_x_get_y(price: float,
                      quantity: int,
                      buy_x: int,
                      get_y: int,
                      discount_percent: float = 100) -> float:
    """
    Calculate price for Buy X Get Y promotion.
    
    Args:
        price: Unit price
        quantity: Total quantity purchased
        buy_x: Number to buy
        get_y: Number free/at discount
        discount_percent: Discount on get_y items (100 = free)
    
    Returns:
        Total price after promotion
    
    Examples:
        >>> apply_buy_x_get_y(10, 3, 2, 1)  # Buy 2 get 1 free
        20.0
        >>> apply_buy_x_get_y(10, 5, 2, 1)  # Buy 2 get 1 free, buying 5
        40.0
    """
    if buy_x <= 0 or get_y <= 0:
        return price * quantity
    
    # Calculate how many complete "buy x get y" cycles
    cycle_size = buy_x + get_y
    complete_cycles = quantity // cycle_size
    remaining = quantity % cycle_size
    
    # Price for complete cycles
    paid_in_cycle = buy_x + get_y * (1 - discount_percent / 100)
    cycle_price = price * paid_in_cycle
    total_price = complete_cycles * cycle_price
    
    # Price for remaining items
    # First buy_x items are paid, rest may get discount
    if remaining <= buy_x:
        total_price += remaining * price
    else:
        paid_items = buy_x
        discounted_items = remaining - buy_x
        total_price += paid_items * price
        total_price += discounted_items * price * (1 - discount_percent / 100)
    
    return total_price


def calculate_free_items(quantity: int, buy_x: int, get_y: int) -> int:
    """
    Calculate how many free items in a Buy X Get Y promotion.
    
    Args:
        quantity: Total quantity
        buy_x: Number to buy
        get_y: Number free
    
    Returns:
        Number of free items
    
    Examples:
        >>> calculate_free_items(3, 2, 1)
        1
        >>> calculate_free_items(5, 2, 1)
        1
        >>> calculate_free_items(6, 2, 1)
        2
    """
    cycle_size = buy_x + get_y
    complete_cycles = quantity // cycle_size
    
    free_from_cycles = complete_cycles * get_y
    
    # Check remaining items
    remaining = quantity % cycle_size
    if remaining > buy_x:
        free_from_remaining = remaining - buy_x
    else:
        free_from_remaining = 0
    
    return free_from_cycles + free_from_remaining


# ============================================================================
# Tax Calculations
# ============================================================================

def calculate_tax(price: float, tax_rate: float) -> float:
    """
    Calculate tax amount.
    
    Args:
        price: Price before tax
        tax_rate: Tax rate percentage
    
    Returns:
        Tax amount
    
    Examples:
        >>> calculate_tax(100, 10)
        10.0
    """
    return price * tax_rate / 100


def apply_tax(price: float, tax_rate: float) -> float:
    """
    Apply tax to price.
    
    Args:
        price: Price before tax
        tax_rate: Tax rate percentage
    
    Returns:
        Price including tax
    
    Examples:
        >>> apply_tax(100, 10)
        110.0
    """
    return price + calculate_tax(price, tax_rate)


def calculate_price_with_tax_and_discount(
    original_price: float,
    discount_percent: float,
    tax_rate: float,
    tax_timing: TaxTiming = TaxTiming.AFTER_DISCOUNT
) -> Dict[str, float]:
    """
    Calculate final price considering both discount and tax.
    
    Args:
        original_price: Original price
        discount_percent: Discount percentage
        tax_rate: Tax rate percentage
        tax_timing: When to apply tax
    
    Returns:
        Dictionary with detailed breakdown
    
    Examples:
        >>> calculate_price_with_tax_and_discount(100, 20, 10)
        {'original': 100, 'discount_amount': 20.0, 'subtotal': 80.0, 'tax': 8.0, 'final': 88.0}
    """
    discount_amount = calculate_discount_amount(original_price, discount_percent)
    
    if tax_timing == TaxTiming.BEFORE_DISCOUNT:
        # Apply tax first, then discount
        taxed_price = apply_tax(original_price, tax_rate)
        tax_amount = calculate_tax(original_price, tax_rate)
        subtotal = taxed_price
        final_price = apply_percentage_discount(taxed_price, discount_percent)
        total_discount = taxed_price - final_price
    else:
        # Apply discount first, then tax (common case)
        subtotal = apply_percentage_discount(original_price, discount_percent)
        tax_amount = calculate_tax(subtotal, tax_rate)
        final_price = subtotal + tax_amount
        total_discount = discount_amount
    
    return {
        'original': original_price,
        'discount_amount': discount_amount,
        'subtotal': subtotal,
        'tax': tax_amount,
        'final': final_price,
        'savings': discount_amount,
    }


# ============================================================================
# Profit and Margin Calculations
# ============================================================================

def calculate_profit_margin(cost: float, price: float) -> float:
    """
    Calculate profit margin percentage.
    
    Args:
        cost: Cost of item
        price: Selling price
    
    Returns:
        Profit margin percentage
    
    Examples:
        >>> calculate_profit_margin(60, 100)
        40.0
    """
    if price <= 0:
        return 0
    return ((price - cost) / price) * 100


def calculate_markup(cost: float, markup_percent: float) -> float:
    """
    Calculate selling price from cost and markup.
    
    Args:
        cost: Cost of item
        markup_percent: Markup percentage
    
    Returns:
        Selling price
    
    Examples:
        >>> calculate_markup(60, 50)
        90.0
    """
    return cost * (1 + markup_percent / 100)


def calculate_cost_from_margin(price: float, margin_percent: float) -> float:
    """
    Calculate cost from price and desired margin.
    
    Args:
        price: Selling price
        margin_percent: Desired profit margin
    
    Returns:
        Maximum cost to achieve margin
    
    Examples:
        >>> calculate_cost_from_margin(100, 40)
        60.0
    """
    return price * (1 - margin_percent / 100)


def calculate_break_even_discount(cost: float, 
                                   original_price: float,
                                   min_margin: float = 0) -> float:
    """
    Calculate maximum discount while maintaining minimum margin.
    
    Args:
        cost: Cost of item
        original_price: Original selling price
        min_margin: Minimum acceptable margin percentage
    
    Returns:
        Maximum discount percentage possible
    
    Examples:
        >>> calculate_break_even_discount(60, 100, 10)
        34.0
    """
    min_price = cost / (1 - min_margin / 100) if min_margin < 100 else cost
    if original_price <= min_price:
        return 0
    return calculate_discount_percentage(original_price, min_price)


# ============================================================================
# Price Comparison
# ============================================================================

def compare_prices(items: List[Tuple[str, float, Optional[float]]]) -> Dict[str, any]:
    """
    Compare prices of same item from different sources.
    
    Args:
        items: List of (source_name, price, discount_percent)
    
    Returns:
        Comparison results with best deal
    
    Examples:
        >>> compare_prices([('Store A', 100, 10), ('Store B', 95, 0)])
        {'best_source': 'Store A', 'best_price': 90.0, 'savings': 5.0}
    """
    if not items:
        return {'best_source': None, 'best_price': None, 'savings': 0}
    
    processed = []
    for source, price, discount in items:
        if discount:
            final_price = apply_percentage_discount(price, discount)
        else:
            final_price = price
        processed.append((source, price, discount or 0, final_price))
    
    # Find best deal
    best = min(processed, key=lambda x: x[3])
    worst = max(processed, key=lambda x: x[3])
    
    return {
        'best_source': best[0],
        'best_original': best[1],
        'best_discount': best[2],
        'best_price': best[3],
        'worst_source': worst[0],
        'worst_price': worst[3],
        'savings_vs_worst': worst[3] - best[3],
        'all_options': processed,
    }


def find_best_bulk_price(prices: List[Tuple[int, float]]) -> Tuple[int, float, float]:
    """
    Find best bulk pricing option.
    
    Args:
        prices: List of (quantity, price) options
    
    Returns:
        Tuple of (best_quantity, best_price, unit_price)
    
    Examples:
        >>> find_best_bulk_price([(1, 10), (5, 40), (10, 70)])
        (10, 70, 7.0)
    """
    if not prices:
        return (0, 0, 0)
    
    best = min(prices, key=lambda x: x[1] / x[0] if x[0] > 0 else float('inf'))
    unit_price = best[1] / best[0] if best[0] > 0 else 0
    
    return (best[0], best[1], unit_price)


# ============================================================================
# Price Formatting
# ============================================================================

def format_price(price: float, 
                  currency: str = '$',
                  decimal_places: int = 2,
                  thousands_separator: str = ',') -> str:
    """
    Format price for display.
    
    Args:
        price: Price value
        currency: Currency symbol
        decimal_places: Number of decimal places
        thousands_separator: Thousands separator character
    
    Returns:
        Formatted price string
    
    Examples:
        >>> format_price(1234.56)
        '$1,234.56'
        >>> format_price(100, '¥', 0)
        '¥100'
    """
    # Format number
    if decimal_places == 0:
        formatted = f"{int(round(price)):,}"
    else:
        formatted = f"{price:,.{decimal_places}f}"
    
    # Replace separator if needed
    if thousands_separator != ',':
        formatted = formatted.replace(',', thousands_separator)
    
    # Add currency symbol
    if currency in ['¥', '€', '£', '₩']:
        return f"{currency}{formatted}"
    else:
        return f"{currency}{formatted}"


def format_percentage(percent: float, decimal_places: int = 1) -> str:
    """
    Format percentage for display.
    
    Args:
        percent: Percentage value
        decimal_places: Number of decimal places
    
    Returns:
        Formatted percentage string
    
    Examples:
        >>> format_percentage(20.5)
        '20.5%'
        >>> format_percentage(20.567, 2)
        '20.57%'
    """
    return f"{percent:.{decimal_places}f}%"


def format_savings(original: float, discounted: float, currency: str = '$') -> str:
    """
    Format savings message.
    
    Args:
        original: Original price
        discounted: Discounted price
        currency: Currency symbol
    
    Returns:
        Savings message string
    
    Examples:
        >>> format_savings(100, 80)
        'Save $20.00 (20%)'
    """
    savings_amount = original - discounted
    savings_percent = calculate_discount_percentage(original, discounted)
    return f"Save {format_price(savings_amount, currency)} ({format_percentage(savings_percent)})"


# ============================================================================
# Complete Price Breakdown
# ============================================================================

def calculate_complete_breakdown(
    original_price: float,
    discounts: List[Discount],
    tax_rate: float = 0,
    tax_timing: TaxTiming = TaxTiming.AFTER_DISCOUNT,
    stack_strategy: StackStrategy = StackStrategy.SEQUENTIAL,
    max_total_discount: float = 100
) -> PriceBreakdown:
    """
    Calculate complete price breakdown with all details.
    
    Args:
        original_price: Original price
        discounts: List of discounts to apply
        tax_rate: Tax rate percentage
        tax_timing: When to apply tax
        stack_strategy: Discount stacking strategy
        max_total_discount: Maximum combined discount
    
    Returns:
        Complete PriceBreakdown
    
    Examples:
        >>> d1 = Discount(DiscountType.PERCENTAGE, 10, 'Member')
        >>> d2 = Discount(DiscountType.PERCENTAGE, 5, 'Coupon')
        >>> breakdown = calculate_complete_breakdown(100, [d1, d2], 10)
    """
    # Apply discounts
    subtotal = apply_discount_with_strategy(
        original_price, discounts, stack_strategy, max_total_discount
    )
    
    # Calculate applied discounts
    discounts_applied = []
    total_savings = original_price - subtotal
    
    for d in discounts:
        if d.min_purchase and original_price < d.min_purchase:
            continue
        
        if d.type == DiscountType.PERCENTAGE:
            amount = calculate_discount_amount(original_price, d.value)
            discounts_applied.append((d.name or f"{d.value}% discount", amount))
        elif d.type == DiscountType.FIXED:
            discounts_applied.append((d.name or "Fixed discount", d.value))
    
    # Apply tax
    if tax_timing == TaxTiming.BEFORE_DISCOUNT:
        tax_base = original_price
    else:
        tax_base = subtotal
    
    tax_amount = calculate_tax(tax_base, tax_rate)
    final_price = subtotal + tax_amount
    
    savings_percentage = calculate_discount_percentage(original_price, subtotal)
    
    return PriceBreakdown(
        original_price=original_price,
        discounts_applied=discounts_applied,
        subtotal_after_discount=subtotal,
        tax_rate=tax_rate,
        tax_amount=tax_amount,
        final_price=final_price,
        total_savings=total_savings,
        savings_percentage=savings_percentage,
    )


# ============================================================================
# Coupon Validation
# ============================================================================

def validate_coupon(discount: Discount, 
                     price: float,
                     purchase_date: Optional[str] = None) -> Dict[str, any]:
    """
    Validate if a coupon/discount can be applied.
    
    Args:
        discount: Discount to validate
        price: Purchase price
        purchase_date: Date of purchase (YYYY-MM-DD format)
    
    Returns:
        Validation result dictionary
    
    Examples:
        >>> d = Discount(DiscountType.PERCENTAGE, 10, 'Coupon', min_purchase=50)
        >>> validate_coupon(d, 30)
        {'valid': False, 'reason': 'Minimum purchase requirement not met'}
    """
    result = {'valid': True, 'reason': None}
    
    # Check minimum purchase
    if discount.min_purchase and price < discount.min_purchase:
        result['valid'] = False
        result['reason'] = f"Minimum purchase requirement not met (need ${discount.min_purchase})"
        return result
    
    # Check expiration
    if discount.expires and purchase_date:
        if purchase_date > discount.expires:
            result['valid'] = False
            result['reason'] = f"Coupon expired on {discount.expires}"
            return result
    
    # Check discount cap
    if discount.type == DiscountType.FIXED and discount.value > price:
        result['valid'] = True
        result['warning'] = "Discount amount exceeds price (will be capped)"
    
    return result


# ============================================================================
# Price History Analysis
# ============================================================================

def analyze_price_history(prices: List[Tuple[str, float]]) -> Dict[str, float]:
    """
    Analyze price history for trends.
    
    Args:
        prices: List of (date, price) tuples
    
    Returns:
        Analysis results
    
    Examples:
        >>> analyze_price_history([('2024-01', 100), ('2024-02', 90), ('2024-03', 85)])
        {'lowest': 85, 'highest': 100, 'average': 91.67, 'trend': 'down'}
    """
    if len(prices) < 2:
        return {
            'lowest': prices[0][1] if prices else 0,
            'highest': prices[0][1] if prices else 0,
            'average': prices[0][1] if prices else 0,
            'trend': 'unknown',
        }
    
    price_values = [p for _, p in prices]
    lowest = min(price_values)
    highest = max(price_values)
    average = sum(price_values) / len(price_values)
    
    # Determine trend (simple: compare first half avg to second half avg)
    mid = len(prices) // 2
    first_half_avg = sum(price_values[:mid]) / mid if mid > 0 else price_values[0]
    second_half_avg = sum(price_values[mid:]) / (len(price_values) - mid)
    
    if second_half_avg < first_half_avg * 0.95:
        trend = 'down'
    elif second_half_avg > first_half_avg * 1.05:
        trend = 'up'
    else:
        trend = 'stable'
    
    return {
        'lowest': lowest,
        'highest': highest,
        'average': round(average, 2),
        'trend': trend,
        'range': highest - lowest,
        'range_percent': round(((highest - lowest) / lowest) * 100, 2) if lowest > 0 else 0,
    }


def is_good_deal(current_price: float, 
                  price_history: List[Tuple[str, float]],
                  threshold_percent: float = 20) -> Dict[str, any]:
    """
    Determine if current price is a good deal based on history.
    
    Args:
        current_price: Current price
        price_history: Historical prices
        threshold_percent: How much below average to be considered good
    
    Returns:
        Deal assessment
    
    Examples:
        >>> is_good_deal(80, [('2024-01', 100), ('2024-02', 100), ('2024-03', 100)])
        {'is_good_deal': True, 'savings_vs_avg': 20.0}
    """
    analysis = analyze_price_history(price_history)
    average = analysis['average']
    lowest = analysis['lowest']
    
    savings_vs_avg = ((average - current_price) / average) * 100 if average > 0 else 0
    
    is_good = current_price <= average * (1 - threshold_percent / 100)
    is_best = current_price <= lowest
    
    return {
        'is_good_deal': is_good,
        'is_best_price': is_best,
        'current': current_price,
        'average': average,
        'lowest': lowest,
        'savings_vs_avg': round(savings_vs_avg, 2),
        'savings_vs_lowest': round(((lowest - current_price) / lowest) * 100, 2) if lowest > 0 else 0,
    }


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=== Discount Utilities Demo ===\n")
    
    # Basic discount
    print("Basic Discount:")
    print(f"  20% off $100 = ${apply_percentage_discount(100, 20)}")
    print(f"  $20 off $100 = ${apply_fixed_discount(100, 20)}")
    
    # Multiple discounts
    print("\nMultiple Discounts:")
    print(f"  Sequential (10% + 20%): ${apply_sequential_discounts(100, [10, 20])}")
    print(f"  Max only: ${apply_max_discount(100, [10, 20, 15])}")
    print(f"  Combined: ${apply_combined_discount(100, [10, 20])}")
    
    # Tiered discount
    print("\nTiered Discount:")
    tiers = TieredDiscount([(50, 5), (100, 10), (200, 15), (500, 20)])
    print(f"  $80 purchase: ${apply_tiered_discount(80, tiers)}")
    print(f"  $300 purchase: ${apply_tiered_discount(300, tiers)}")
    print(f"  Upgrade suggestion for $180: {suggest_upgrade_for_tier(180, tiers)}")
    
    # Bundle discount
    print("\nBundle Discount:")
    bundle = BundleDiscount([('Laptop', 800), ('Mouse', 30), ('Bag', 20)], 820)
    savings = calculate_bundle_savings(bundle)
    print(f"  Original: ${savings['original_total']}, Bundle: ${savings['bundle_price']}")
    print(f"  Savings: ${savings['savings']} ({savings['savings_percent']}%)")
    
    # Buy X Get Y
    print("\nBuy X Get Y:")
    print(f"  Buy 2 Get 1 free, 3 items @ $10 each: ${apply_buy_x_get_y(10, 3, 2, 1)}")
    print(f"  Free items: {calculate_free_items(3, 2, 1)}")
    
    # Tax
    print("\nTax Calculation:")
    result = calculate_price_with_tax_and_discount(100, 20, 10)
    print(f"  Original: ${result['original']}")
    print(f"  After 20% discount: ${result['subtotal']}")
    print(f"  After 10% tax: ${result['final']}")
    
    # Price comparison
    print("\nPrice Comparison:")
    comparison = compare_prices([
        ('Amazon', 100, 10),
        ('BestBuy', 95, 0),
        ('Walmart', 98, 5),
    ])
    print(f"  Best deal: {comparison['best_source']} at ${comparison['best_price']}")
    
    # Profit margin
    print("\nProfit & Margin:")
    print(f"  Cost $60, Price $100 -> Margin: {calculate_profit_margin(60, 100)}%")
    print(f"  Max discount at 10% margin: {calculate_break_even_discount(60, 100, 10)}%")
    
    # Formatting
    print("\nFormatting:")
    print(f"  {format_price(1234.5678)}")
    print(f"  {format_price(1000000, '¥', 0)}")
    print(f"  {format_savings(100, 75)}")
    
    # Complete breakdown
    print("\nComplete Price Breakdown:")
    d1 = Discount(DiscountType.PERCENTAGE, 10, 'Member Discount')
    d2 = Discount(DiscountType.PERCENTAGE, 5, 'Coupon', min_purchase=50)
    breakdown = calculate_complete_breakdown(100, [d1, d2], 10)
    print(f"  Original: ${breakdown.original_price}")
    for name, amount in breakdown.discounts_applied:
        print(f"    {name}: -${amount:.2f}")
    print(f"  Subtotal: ${breakdown.subtotal_after_discount:.2f}")
    print(f"  Tax (10%): ${breakdown.tax_amount:.2f}")
    print(f"  Final: ${breakdown.final_price:.2f}")
    print(f"  Total Savings: ${breakdown.total_savings:.2f} ({breakdown.savings_percentage:.1f}%)")