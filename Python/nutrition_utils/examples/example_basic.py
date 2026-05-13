#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Nutrition Utilities Examples
===========================================
Basic usage examples for nutrition_utils module.
"""

import sys
sys.path.insert(0, '..')

from mod import (
    get_food_info,
    search_foods,
    calculate_food_nutrition,
    calculate_meal_nutrition,
    calculate_daily_needs,
    analyze_nutrition,
    get_meal_suggestion,
    format_nutrition_label,
    format_meal_summary,
    ActivityLevel,
    Goal,
    Gender,
)


def example_food_search():
    """示例：食物搜索"""
    print("\n" + "=" * 50)
    print("示例 1: 食物搜索")
    print("=" * 50)
    
    # 搜索包含"鸡"的食物
    results = search_foods('鸡')
    print(f"搜索 '鸡': {results}")
    
    # 搜索包含"米"的食物
    results = search_foods('米')
    print(f"搜索 '米': {results}")
    
    # 获取食物详细信息
    info = get_food_info('鸡胸肉')
    print(f"\n鸡胸肉营养信息: {info}")


def example_food_nutrition():
    """示例：单个食物营养计算"""
    print("\n" + "=" * 50)
    print("示例 2: 单个食物营养计算")
    print("=" * 50)
    
    # 计算 100g 米饭的营养
    print(format_nutrition_label('米饭', 100))
    
    # 计算 150g 鸡胸肉的营养
    print("\n" + format_nutrition_label('鸡胸肉', 150))
    
    # 计算 200g 西兰花
    print("\n" + format_nutrition_label('西兰花', 200))


def example_meal_calculation():
    """示例：餐饮营养计算"""
    print("\n" + "=" * 50)
    print("示例 3: 餐饮营养计算")
    print("=" * 50)
    
    # 定义一餐的食物
    lunch = [
        ('米饭', 200),        # 200g 米饭
        ('鸡胸肉', 150),      # 150g 鸡胸肉
        ('西兰花', 100),      # 100g 西兰花
        ('橄榄油', 10),       # 10g 橄榄油（烹饪用）
    ]
    
    print(format_meal_summary(lunch))


def example_daily_needs():
    """示例：每日营养需求计算"""
    print("\n" + "=" * 50)
    print("示例 4: 每日营养需求计算")
    print("=" * 50)
    
    # 计算不同目标的营养需求
    person = {'weight': 70, 'height': 175, 'age': 30, 'gender': Gender.MALE}
    
    # 维持期
    needs_maintain = calculate_daily_needs(
        person['weight'], person['height'], person['age'], person['gender'],
        ActivityLevel.MODERATE, Goal.MAINTAIN
    )
    print(f"维持期营养需求:")
    print(f"  热量: {needs_maintain.calories:.0f} kcal")
    print(f"  蛋白质: {needs_maintain.protein:.1f}g")
    print(f"  碳水: {needs_maintain.carbs:.1f}g")
    print(f"  脂肪: {needs_maintain.fat:.1f}g")
    
    # 减脂期
    needs_loss = calculate_daily_needs(
        person['weight'], person['height'], person['age'], person['gender'],
        ActivityLevel.MODERATE, Goal.LOSE_WEIGHT
    )
    print(f"\n减脂期营养需求:")
    print(f"  烎量: {needs_loss.calories:.0f} kcal (减少约 {(needs_maintain.calories - needs_loss.calories):.0f} kcal)")
    
    # 增肌期
    needs_gain = calculate_daily_needs(
        person['weight'], person['height'], person['age'], person['gender'],
        ActivityLevel.ACTIVE, Goal.GAIN_MUSCLE
    )
    print(f"\n增肌期营养需求:")
    print(f"  烎量: {needs_gain.calories:.0f} kcal (增加约 {(needs_gain.calories - needs_maintain.calories):.0f} kcal)")


def example_nutrition_analysis():
    """示例：营养分析"""
    print("\n" + "=" * 50)
    print("示例 5: 营养分析")
    print("=" * 50)
    
    # 计算每日需求
    needs = calculate_daily_needs(70, 175, 30, Gender.MALE)
    
    # 定义一天的饮食
    daily_food = [
        # 早餐
        ('全麦面包', 60),
        ('鸡蛋', 50),
        ('牛奶', 200),
        
        # 午餐
        ('米饭', 200),
        ('鸡胸肉', 150),
        ('西兰花', 100),
        
        # 晚餐
        ('三文鱼', 120),
        ('糙米饭', 150),
        ('菠菜', 100),
        
        # 加餐
        ('香蕉', 100),
        ('杏仁', 20),
    ]
    
    analysis = analyze_nutrition(daily_food, needs)
    
    print(f"每日目标: {needs.calories:.0f} kcal")
    print(f"实际摄入: {analysis.calories:.0f} kcal ({analysis.calories_percent}%)")
    print(f"蛋白质: {analysis.protein:.1f}g ({analysis.protein_percent}%)")
    print(f"碳水化合物: {analysis.carbs:.1f}g ({analysis.carbs_percent}%)")
    print(f"脂肪: {analysis.fat:.1f}g ({analysis.fat_percent}%)")
    print(f"膳食纤维: {analysis.fiber:.1f}g ({analysis.fiber_percent}%)")
    print(f"营养平衡分数: {analysis.balance_score}/100")
    print(f"\n建议: {analysis.recommendations[0]}")


def example_meal_suggestion():
    """示例：饮食建议"""
    print("\n" + "=" * 50)
    print("示例 6: 饮食建议生成")
    print("=" * 50)
    
    # 生成 500 kcal, 30g 蛋白质的餐食建议
    suggestions = get_meal_suggestion(500, 35)
    
    print("目标: 500 kcal, 35g 蛋白质")
    print("\n建议食物:")
    for food, amount in suggestions:
        info = calculate_food_nutrition(food, amount)
        if info:
            print(f"  {food}: {amount}g → {info.calories:.0f} kcal, {info.protein:.1f}g 蛋白质")
    
    # 计算建议餐食的总营养
    summary = calculate_meal_nutrition(suggestions)
    print(f"\n总营养:")
    print(f"  烎量: {summary.total_calories:.0f} kcal")
    print(f"  蛋白质: {summary.total_protein:.1f}g")


def example_different_activities():
    """示例：不同活动水平的对比"""
    print("\n" + "=" * 50)
    print("示例 7: 不同活动水平的营养需求对比")
    print("=" * 50)
    
    levels = [
        ActivityLevel.SEDENTARY,
        ActivityLevel.LIGHT,
        ActivityLevel.MODERATE,
        ActivityLevel.ACTIVE,
        ActivityLevel.VERY_ACTIVE,
    ]
    
    print("体重 70kg, 身高 175cm, 年龄 30, 男性")
    print("-" * 50)
    
    for level in levels:
        needs = calculate_daily_needs(70, 175, 30, Gender.MALE, level)
        print(f"{level.value:15}: {needs.calories:>6.0f} kcal")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("AllToolkit - Nutrition Utilities 使用示例")
    print("=" * 50)
    
    example_food_search()
    example_food_nutrition()
    example_meal_calculation()
    example_daily_needs()
    example_nutrition_analysis()
    example_meal_suggestion()
    example_different_activities()
    
    print("\n" + "=" * 50)
    print("示例演示完成")
    print("=" * 50)


if __name__ == '__main__':
    main()