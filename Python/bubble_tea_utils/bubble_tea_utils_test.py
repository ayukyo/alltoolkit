#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Bubble Tea Calories Calculator Module Tests
=========================================================
Comprehensive tests for bubble_tea_utils module.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bubble_tea_utils.mod import (
    # Core functions
    get_base_calories,
    get_sugar_calories,
    get_additive_calories,
    get_size_ml,
    calculate_calories,
    calculate_calories_simple,
    
    # Data classes
    BubbleTeaOrder,
    CalorieResult,
    
    # Enums
    SugarLevel,
    TeaSize,
    HealthLevel,
    
    # Health functions
    get_health_level,
    get_health_suggestion,
    get_daily_calorie_comparison,
    compare_teas,
    
    # Recommend functions
    recommend_low_calorie_options,
    find_calorie_range,
    
    # Utility functions
    get_additive_list,
    get_base_tea_list,
    get_sugar_level_list,
    get_size_list,
    print_calorie_report,
    
    # Constants
    BASE_TEA_CALORIES,
    ADDITIVE_CALORIES,
    SUGAR_LEVEL_CALORIES,
    SIZE_VOLUME,
)


def test_constants():
    """Test that all constants are properly defined."""
    print("Testing constants...")
    
    # Test base tea calories
    assert '奶茶' in BASE_TEA_CALORIES
    assert BASE_TEA_CALORIES['奶茶'] == 35
    assert BASE_TEA_CALORIES['绿茶'] == 2
    assert BASE_TEA_CALORIES['奶茶'] > BASE_TEA_CALORIES['绿茶']
    
    # Test additive calories
    assert '珍珠' in ADDITIVE_CALORIES
    assert ADDITIVE_CALORIES['珍珠'] == 120
    assert '椰果' in ADDITIVE_CALORIES
    assert ADDITIVE_CALORIES['蒟蒻'] == 20  # Low calorie
    
    # Test sugar levels
    assert SUGAR_LEVEL_CALORIES['无糖'] == 0
    assert SUGAR_LEVEL_CALORIES['半糖'] == 20
    assert SUGAR_LEVEL_CALORIES['全糖'] == 40
    
    # Test sizes
    assert SIZE_VOLUME['中杯'] == 400
    assert SIZE_VOLUME['大杯'] == 500
    assert SIZE_VOLUME['超大杯'] == 700
    
    print("  ✓ Constants test passed")


def test_get_base_calories():
    """Test base calorie calculation."""
    print("Testing get_base_calories...")
    
    # Tea bases
    assert get_base_calories('奶茶', 500) == 175.0  # 35 * 5
    assert get_base_calories('绿茶', 500) == 10.0   # 2 * 5
    assert get_base_calories('黑糖奶茶', 400) == 280.0  # 70 * 4
    
    # Small cup
    assert get_base_calories('奶茶', 300) == 105.0  # 35 * 3
    
    # Unknown base (default)
    assert get_base_calories('未知茶', 500) == 150.0
    
    print("  ✓ get_base_calories test passed")


def test_get_sugar_calories():
    """Test sugar calorie calculation."""
    print("Testing get_sugar_calories...")
    
    # Standard sugar levels
    assert get_sugar_calories('无糖', 500) == 0.0
    assert get_sugar_calories('半糖', 500) == 100.0  # 20 * 5
    assert get_sugar_calories('全糖', 500) == 200.0  # 40 * 5
    
    # Percentage format
    assert get_sugar_calories('0%', 500) == 0.0
    assert get_sugar_calories('50%', 500) == 100.0
    assert get_sugar_calories('100%', 500) == 200.0
    
    # "分糖" format
    assert get_sugar_calories('3分糖', 500) == 60.0  # 40 * 0.3 * 5
    assert get_sugar_calories('5分糖', 500) == 100.0
    
    # Unknown sugar level (default)
    result = get_sugar_calories('未知', 500)
    assert result == 100.0  # Default 20 per 100ml
    
    print("  ✓ get_sugar_calories test passed")


def test_get_additive_calories():
    """Test additive calorie calculation."""
    print("Testing get_additive_calories...")
    
    # Single additive
    assert get_additive_calories(['珍珠']) == 120
    assert get_additive_calories(['椰果']) == 50
    assert get_additive_calories(['布丁']) == 90
    
    # Multiple additives
    assert get_additive_calories(['珍珠', '椰果']) == 170
    assert get_additive_calories(['珍珠', '布丁', '奶盖']) == 290
    
    # Empty list
    assert get_additive_calories([]) == 0
    
    # Unknown additive (default)
    assert get_additive_calories(['未知配料']) == 50
    
    print("  ✓ get_additive_calories test passed")


def test_get_size_ml():
    """Test size conversion."""
    print("Testing get_size_ml...")
    
    # Standard sizes
    assert get_size_ml('小杯') == 300
    assert get_size_ml('中杯') == 400
    assert get_size_ml('大杯') == 500
    assert get_size_ml('超大杯') == 700
    
    # Letter sizes
    assert get_size_ml('S') == 300
    assert get_size_ml('M') == 400
    assert get_size_ml('L') == 500
    assert get_size_ml('XL') == 700
    
    # ml format
    assert get_size_ml('500ml') == 500
    assert get_size_ml('360ml') == 360
    
    # Numeric format
    assert get_size_ml('400') == 400
    
    # Unknown size (default)
    assert get_size_ml('未知') == 400
    
    print("  ✓ get_size_ml test passed")


def test_calculate_calories():
    """Test complete calorie calculation."""
    print("Testing calculate_calories...")
    
    # Basic order
    order = BubbleTeaOrder('奶茶', '半糖', '大杯', ['珍珠'])
    result = calculate_calories(order)
    
    # Expected: 35*5 + 20*5 + 120 = 175 + 100 + 120 = 395
    assert result.total_calories == 395.0
    assert result.base_calories == 175.0
    assert result.sugar_calories == 100.0
    assert result.additive_calories == 120
    assert result.size_ml == 500
    
    # Pure tea (low calorie)
    order2 = BubbleTeaOrder('绿茶', '无糖', '中杯', [])
    result2 = calculate_calories(order2)
    assert result2.total_calories == 8.0
    assert result2.health_level == HealthLevel.LOW
    
    # High calorie drink
    order3 = BubbleTeaOrder('黑糖奶茶', '全糖', '超大杯', ['珍珠', '奶盖', '布丁'])
    result3 = calculate_calories(order3)
    # Expected: 70*7 + 40*7 + 120 + 80 + 90 = 490 + 280 + 290 = 1060
    assert result3.total_calories == 1060.0
    assert result3.health_level == HealthLevel.VERY_HIGH
    
    print("  ✓ calculate_calories test passed")


def test_calculate_calories_simple():
    """Test simple calorie calculation."""
    print("Testing calculate_calories_simple...")
    
    # Without additives
    assert calculate_calories_simple('奶茶', '半糖', '大杯') == 275.0
    
    # With additives
    assert calculate_calories_simple('奶茶', '半糖', '大杯', ['珍珠']) == 395.0
    
    # Pure tea
    assert calculate_calories_simple('绿茶', '无糖', '中杯') == 8.0
    
    print("  ✓ calculate_calories_simple test passed")


def test_health_level():
    """Test health level determination."""
    print("Testing get_health_level...")
    
    assert get_health_level(100) == HealthLevel.LOW
    assert get_health_level(150) == HealthLevel.MODERATE
    assert get_health_level(200) == HealthLevel.MODERATE
    assert get_health_level(300) == HealthLevel.HIGH
    assert get_health_level(400) == HealthLevel.HIGH
    assert get_health_level(500) == HealthLevel.VERY_HIGH
    assert get_health_level(600) == HealthLevel.VERY_HIGH
    
    print("  ✓ get_health_level test passed")


def test_health_suggestion():
    """Test health suggestions."""
    print("Testing get_health_suggestion...")
    
    sug1 = get_health_suggestion(100, HealthLevel.LOW)
    assert '较低' in sug1
    
    sug2 = get_health_suggestion(200, HealthLevel.MODERATE)
    assert '适中' in sug2
    
    sug3 = get_health_suggestion(400, HealthLevel.HIGH)
    assert '较高' in sug3
    
    sug4 = get_health_suggestion(600, HealthLevel.VERY_HIGH)
    assert '非常高' in sug4
    
    print("  ✓ get_health_suggestion test passed")


def test_daily_comparison():
    """Test daily calorie comparison."""
    print("Testing get_daily_calorie_comparison...")
    
    result = get_daily_calorie_comparison(300)
    assert result['percentage'] == 15.0
    assert result['remaining'] == 1700
    assert result['meals_equivalent'] == 0.5
    
    # High calorie drink
    result2 = get_daily_calorie_comparison(500)
    assert result2['percentage'] == 25.0
    assert result2['remaining'] == 1500
    assert result2['meals_equivalent'] == 0.83
    
    # Custom target
    result3 = get_daily_calorie_comparison(300, 1500)
    assert result3['percentage'] == 20.0
    
    print("  ✓ get_daily_calorie_comparison test passed")


def test_compare_teas():
    """Test comparing multiple teas."""
    print("Testing compare_teas...")
    
    teas = [
        BubbleTeaOrder('绿茶', '无糖', '中杯', []),        # 8 kcal
        BubbleTeaOrder('奶茶', '半糖', '大杯', ['珍珠']),   # 395 kcal
        BubbleTeaOrder('奶茶', '微糖', '小杯', ['椰果']),   # Lower
    ]
    
    results = compare_teas(teas)
    
    # Should be sorted by calories (ascending)
    assert results[0][1].total_calories < results[1][1].total_calories
    assert results[0][1].total_calories == 8.0  # Green tea is lowest
    
    print("  ✓ compare_teas test passed")


def test_recommendations():
    """Test recommendation functions."""
    print("Testing recommend_low_calorie_options...")
    
    recommendations = recommend_low_calorie_options()
    assert len(recommendations) > 0
    
    # All recommendations should be low calorie
    for rec in recommendations:
        assert rec['calories'] < 200
    
    print("  ✓ recommend_low_calorie_options test passed")


def test_find_calorie_range():
    """Test finding teas within calorie range."""
    print("Testing find_calorie_range...")
    
    orders = find_calorie_range(150, 50)
    
    # All orders should be within range
    for order in orders:
        result = calculate_calories(order)
        assert abs(result.total_calories - 150) <= 50
    
    print("  ✓ find_calorie_range test passed")


def test_utility_functions():
    """Test utility functions."""
    print("Testing utility functions...")
    
    # List functions
    additives = get_additive_list()
    assert '珍珠' in additives
    assert len(additives) > 10
    
    bases = get_base_tea_list()
    assert '奶茶' in bases
    assert len(bases) > 10
    
    sugars = get_sugar_level_list()
    assert '半糖' in sugars
    assert len(sugars) > 5
    
    sizes = get_size_list()
    assert '大杯' in sizes
    assert len(sizes) > 5
    
    print("  ✓ utility functions test passed")


def test_print_report():
    """Test calorie report generation."""
    print("Testing print_calorie_report...")
    
    order = BubbleTeaOrder('奶茶', '半糖', '大杯', ['珍珠'])
    result = calculate_calories(order)
    report = print_calorie_report(result)
    
    assert '热量' in report
    assert '奶茶' in report or '基底' in report
    assert 'kcal' in report
    assert '健康' in report
    
    print("  ✓ print_calorie_report test passed")


def test_bubble_tea_order():
    """Test BubbleTeaOrder dataclass."""
    print("Testing BubbleTeaOrder...")
    
    order = BubbleTeaOrder('奶茶', '半糖', '大杯', ['珍珠', '椰果'])
    
    assert order.base_tea == '奶茶'
    assert order.sugar_level == '半糖'
    assert order.size == '大杯'
    assert order.additives == ['珍珠', '椰果']
    assert order.ice_level == '正常'
    
    # Test with custom ice level
    order2 = BubbleTeaOrder('绿茶', '无糖', '中杯', [], ice_level='少冰')
    assert order2.ice_level == '少冰'
    
    print("  ✓ BubbleTeaOrder test passed")


def test_enum_values():
    """Test enum values."""
    print("Testing enums...")
    
    # SugarLevel
    assert SugarLevel.NONE.value == 0
    assert SugarLevel.FULL.value == 4
    
    # TeaSize
    assert TeaSize.SMALL.value == 300
    assert TeaSize.LARGE.value == 500
    
    # HealthLevel
    assert HealthLevel.LOW.value == 1
    assert HealthLevel.VERY_HIGH.value == 4
    
    print("  ✓ enum test passed")


def test_edge_cases():
    """Test edge cases."""
    print("Testing edge cases...")
    
    # Empty additives
    order = BubbleTeaOrder('绿茶', '无糖', '小杯', [])
    result = calculate_calories(order)
    assert result.total_calories == 6.0  # 2 * 3
    
    # Very large cup
    order2 = BubbleTeaOrder('奶茶', '全糖', '超大杯', ['珍珠', '珍珠'])  # Double pearls
    result2 = calculate_calories(order2)
    assert result2.total_calories == 245.0 + 280.0 + 240  # 765
    
    # Unknown everything (should use defaults)
    order3 = BubbleTeaOrder('未知茶', '未知糖', '未知大小', ['未知配料'])
    result3 = calculate_calories(order3)
    # Default: 30 * 4 + 20 * 4 + 50 = 250
    assert result3.total_calories == 250.0
    
    print("  ✓ edge cases test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Bubble Tea Utils Test Suite")
    print("=" * 50)
    
    test_constants()
    test_get_base_calories()
    test_get_sugar_calories()
    test_get_additive_calories()
    test_get_size_ml()
    test_calculate_calories()
    test_calculate_calories_simple()
    test_health_level()
    test_health_suggestion()
    test_daily_comparison()
    test_compare_teas()
    test_recommendations()
    test_find_calorie_range()
    test_utility_functions()
    test_print_report()
    test_bubble_tea_order()
    test_enum_values()
    test_edge_cases()
    
    print("=" * 50)
    print("All tests passed! ✓")
    print("=" * 50)


if __name__ == '__main__':
    run_all_tests()