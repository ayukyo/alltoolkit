#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Bubble Tea Calories Calculator Examples
=====================================================
Usage examples for bubble_tea_utils module.
"""

import sys
import os

# Add parent directory (Python/) to path for proper imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from bubble_tea_utils.mod import (
    BubbleTeaOrder,
    calculate_calories,
    calculate_calories_simple,
    print_calorie_report,
    get_daily_calorie_comparison,
    compare_teas,
    recommend_low_calorie_options,
    find_calorie_range,
    get_additive_list,
    get_base_tea_list,
    get_sugar_level_list,
    get_size_list,
)


def example_basic_calculation():
    """Example 1: Basic calorie calculation."""
    print("\n" + "=" * 50)
    print("Example 1: Basic Calorie Calculation")
    print("=" * 50)
    
    # Create an order
    order = BubbleTeaOrder(
        base_tea='奶茶',
        sugar_level='半糖',
        size='大杯',
        additives=['珍珠', '椰果']
    )
    
    # Calculate calories
    result = calculate_calories(order)
    
    # Print detailed report
    print(print_calorie_report(result))


def example_simple_calculation():
    """Example 2: Simple one-line calculation."""
    print("\n" + "=" * 50)
    print("Example 2: Simple One-Line Calculation")
    print("=" * 50)
    
    # Just get the calorie number
    calories = calculate_calories_simple('奶茶', '少糖', '中杯', ['布丁'])
    print(f"奶茶 + 少糖 + 中杯 + 布丁 = {calories} kcal")
    
    # Pure tea
    calories2 = calculate_calories_simple('绿茶', '无糖', '小杯')
    print(f"纯绿茶(无糖小杯) = {calories2} kcal")


def example_daily_comparison():
    """Example 3: Daily intake comparison."""
    print("\n" + "=" * 50)
    print("Example 3: Daily Intake Comparison")
    print("=" * 50)
    
    # High calorie drink
    order = BubbleTeaOrder('黑糖奶茶', '全糖', '超大杯', ['珍珠', '奶盖'])
    result = calculate_calories(order)
    
    print(f"饮品热量: {result.total_calories} kcal")
    
    # Compare with daily intake
    comparison = get_daily_calorie_comparison(result.total_calories)
    print(f"占每日摄入比例: {comparison['percentage']}%")
    print(f"剩余可摄入热量: {comparison['remaining']} kcal")
    print(f"相当于 {comparison['meals_equivalent']} 顿正餐")
    
    # Custom daily target (e.g., for weight loss)
    comparison2 = get_daily_calorie_comparison(result.total_calories, 1500)
    print(f"\n如果每日目标是 1500 kcal:")
    print(f"占每日摄入比例: {comparison2['percentage']}%")


def example_compare_options():
    """Example 4: Comparing multiple options."""
    print("\n" + "=" * 50)
    print("Example 4: Comparing Multiple Options")
    print("=" * 50)
    
    # Different options
    options = [
        BubbleTeaOrder('绿茶', '无糖', '中杯', []),
        BubbleTeaOrder('奶茶', '半糖', '大杯', ['珍珠']),
        BubbleTeaOrder('鲜奶茶', '微糖', '中杯', ['椰果']),
        BubbleTeaOrder('黑糖奶茶', '全糖', '大杯', ['珍珠', '布丁']),
    ]
    
    results = compare_teas(options)
    
    print("热量排名 (从低到高):")
    print("-" * 40)
    for order, result in results:
        additives_str = ', '.join(order.additives) if order.additives else '无配料'
        print(f"{result.total_calories} kcal | {order.base_tea} + {order.sugar_level} + {order.size} + [{additives_str}]")
    
    # Find the lowest calorie option
    lowest = results[0]
    print(f"\n推荐最低热量选择: {lowest[0].base_tea} ({lowest[1].total_calories} kcal)")


def example_recommendations():
    """Example 5: Getting recommendations."""
    print("\n" + "=" * 50)
    print("Example 5: Low Calorie Recommendations")
    print("=" * 50)
    
    recommendations = recommend_low_calorie_options()
    
    print("推荐低热量饮品:")
    print("-" * 40)
    for rec in recommendations[:5]:
        additives_str = ', '.join(rec['additives']) if rec['additives'] else '无配料'
        print(f"{rec['calories']} kcal | {rec['base']} + {rec['sugar']} + {rec['size']} + [{additives_str}]")
        print(f"    {rec['note']}")


def example_find_range():
    """Example 6: Finding teas within calorie range."""
    print("\n" + "=" * 50)
    print("Example 6: Finding Teas Within Calorie Range")
    print("=" * 50)
    
    # Find teas around 150 kcal
    target = 150
    tolerance = 30
    
    print(f"寻找热量在 {target-tolerance}~{target+tolerance} kcal 范围内的饮品:")
    print("-" * 40)
    
    orders = find_calorie_range(target, tolerance)
    
    for order in orders[:5]:
        result = calculate_calories(order)
        additives_str = ', '.join(order.additives) if order.additives else '无配料'
        print(f"{result.total_calories} kcal | {order.base_tea} + {order.sugar_level} + {order.size} + [{additives_str}]")


def example_list_all_options():
    """Example 7: Listing all available options."""
    print("\n" + "=" * 50)
    print("Example 7: All Available Options")
    print("=" * 50)
    
    print("\n基底茶列表:")
    bases = get_base_tea_list()
    for base in bases[:10]:
        print(f"  - {base}")
    print(f"  ... 共 {len(bases)} 种")
    
    print("\n配料列表:")
    additives = get_additive_list()
    for add in additives[:10]:
        print(f"  - {add}")
    print(f"  ... 共 {len(additives)} 种")
    
    print("\n糖度列表:")
    sugars = get_sugar_level_list()
    for sugar in sugars[:8]:
        print(f"  - {sugar}")
    print(f"  ... 共 {len(sugars)} 种")
    
    print("\n杯型列表:")
    sizes = get_size_list()
    for size in sizes[:8]:
        print(f"  - {size}")
    print(f"  ... 共 {len(sizes)} 种")


def example_real_world_scenario():
    """Example 8: Real-world decision making."""
    print("\n" + "=" * 50)
    print("Example 8: Real-World Decision Making")
    print("=" * 50)
    
    print("\n场景: 想喝奶茶但正在控制热量...")
    print("\n方案比较:")
    
    # Compare different sugar levels for same drink
    base = '奶茶'
    size = '大杯'
    additives = ['珍珠']
    
    for sugar in ['全糖', '半糖', '微糖', '无糖']:
        cal = calculate_calories_simple(base, sugar, size, additives)
        print(f"  {sugar}: {cal} kcal")
    
    print("\n降糖建议: 从全糖改为微糖可减少约 80 kcal")
    
    # Compare with different additives
    print("\n配料热量比较:")
    for add in ['珍珠', '椰果', '布丁', '蒟蒻', '仙草']:
        cal = calculate_calories_simple('奶茶', '半糖', '大杯', [add])
        print(f"  奶茶+半糖+大杯+{add}: {cal} kcal")
    
    print("\n建议: 选择蒟蒻或仙草作为配料，热量更低")


def run_all_examples():
    """Run all examples."""
    print("=" * 60)
    print("Bubble Tea Calories Calculator - Usage Examples")
    print("=" * 60)
    
    example_basic_calculation()
    example_simple_calculation()
    example_daily_comparison()
    example_compare_options()
    example_recommendations()
    example_find_range()
    example_list_all_options()
    example_real_world_scenario()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()