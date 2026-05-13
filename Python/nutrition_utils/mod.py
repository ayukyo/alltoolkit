#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Nutrition Utilities Module
========================================
A comprehensive nutrition calculation and analysis module with zero external dependencies.

Features:
    - Food nutrition database (common foods)
    - Calorie and macronutrient calculation
    - Daily nutritional requirements estimation
    - Nutrient balance analysis
    - Meal planning assistance
    - BMI-based calorie recommendations
    - Protein requirements calculator
    - Vitamin and mineral tracking

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-14
"""

from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Constants
# ============================================================================

# Macronutrient calories per gram
CALORIES_PER_GRAM = {
    'protein': 4,      # 蛋白质
    'carbs': 4,        # 碳水化合物
    'fat': 9,          # 脂肪
    'alcohol': 7,      # 酒精
    'fiber': 2,        # 膳食纤维（部分可消化）
}

# Common foods nutrition database (per 100g)
# Format: {name: {calories, protein, carbs, fat, fiber, ...}}
FOOD_DATABASE = {
    # 主食类 / Staples
    '米饭': {'calories': 116, 'protein': 2.6, 'carbs': 25.9, 'fat': 0.3, 'fiber': 0.3, 'category': 'staples'},
    '白米饭': {'calories': 116, 'protein': 2.6, 'carbs': 25.9, 'fat': 0.3, 'fiber': 0.3, 'category': 'staples'},
    '糙米饭': {'calories': 111, 'protein': 2.6, 'carbs': 23.5, 'fat': 0.9, 'fiber': 1.8, 'category': 'staples'},
    '面条': {'calories': 138, 'protein': 4.5, 'carbs': 28.0, 'fat': 0.8, 'fiber': 1.2, 'category': 'staples'},
    '馒头': {'calories': 221, 'protein': 7.0, 'carbs': 45.0, 'fat': 1.1, 'fiber': 1.3, 'category': 'staples'},
    '面包': {'calories': 265, 'protein': 9.0, 'carbs': 49.0, 'fat': 3.2, 'fiber': 2.7, 'category': 'staples'},
    '全麦面包': {'calories': 247, 'protein': 13.0, 'carbs': 41.0, 'fat': 3.4, 'fiber': 7.0, 'category': 'staples'},
    '燕麦': {'calories': 389, 'protein': 16.9, 'carbs': 66.0, 'fat': 6.9, 'fiber': 10.6, 'category': 'staples'},
    '红薯': {'calories': 86, 'protein': 1.6, 'carbs': 20.1, 'fat': 0.1, 'fiber': 3.0, 'category': 'staples'},
    '土豆': {'calories': 77, 'protein': 2.0, 'carbs': 17.0, 'fat': 0.1, 'fiber': 2.2, 'category': 'staples'},
    
    # 肉类 / Meat
    '鸡胸肉': {'calories': 165, 'protein': 31.0, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'category': 'meat'},
    '鸡腿肉': {'calories': 209, 'protein': 26.0, 'carbs': 0, 'fat': 11.0, 'fiber': 0, 'category': 'meat'},
    '牛肉': {'calories': 250, 'protein': 26.0, 'carbs': 0, 'fat': 15.0, 'fiber': 0, 'category': 'meat'},
    '猪肉': {'calories': 242, 'protein': 27.0, 'carbs': 0, 'fat': 14.0, 'fiber': 0, 'category': 'meat'},
    '羊肉': {'calories': 294, 'protein': 25.0, 'carbs': 0, 'fat': 21.0, 'fiber': 0, 'category': 'meat'},
    '培根': {'calories': 541, 'protein': 37.0, 'carbs': 1.4, 'fat': 42.0, 'fiber': 0, 'category': 'meat'},
    
    # 海鲜 / Seafood
    '三文鱼': {'calories': 208, 'protein': 20.0, 'carbs': 0, 'fat': 13.0, 'fiber': 0, 'category': 'seafood'},
    '虾': {'calories': 99, 'protein': 24.0, 'carbs': 0.2, 'fat': 0.3, 'fiber': 0, 'category': 'seafood'},
    '鳕鱼': {'calories': 82, 'protein': 18.0, 'carbs': 0, 'fat': 0.7, 'fiber': 0, 'category': 'seafood'},
    '金枪鱼': {'calories': 132, 'protein': 29.0, 'carbs': 0, 'fat': 1.0, 'fiber': 0, 'category': 'seafood'},
    '蟹肉': {'calories': 97, 'protein': 19.0, 'carbs': 0, 'fat': 1.5, 'fiber': 0, 'category': 'seafood'},
    
    # 蛋奶类 / Eggs & Dairy
    '鸡蛋': {'calories': 155, 'protein': 13.0, 'carbs': 1.1, 'fat': 11.0, 'fiber': 0, 'category': 'eggs_dairy'},
    '蛋白': {'calories': 52, 'protein': 11.0, 'carbs': 0.7, 'fat': 0.2, 'fiber': 0, 'category': 'eggs_dairy'},
    '牛奶': {'calories': 42, 'protein': 3.4, 'carbs': 5.0, 'fat': 1.0, 'fiber': 0, 'category': 'eggs_dairy'},
    '全脂牛奶': {'calories': 61, 'protein': 3.2, 'carbs': 4.8, 'fat': 3.3, 'fiber': 0, 'category': 'eggs_dairy'},
    '脱脂牛奶': {'calories': 34, 'protein': 3.4, 'carbs': 5.0, 'fat': 0.1, 'fiber': 0, 'category': 'eggs_dairy'},
    '酸奶': {'calories': 59, 'protein': 10.0, 'carbs': 3.6, 'fat': 0.7, 'fiber': 0, 'category': 'eggs_dairy'},
    '奶酪': {'calories': 402, 'protein': 25.0, 'carbs': 1.3, 'fat': 33.0, 'fiber': 0, 'category': 'eggs_dairy'},
    
    # 豆类 / Legumes
    '豆腐': {'calories': 76, 'protein': 8.0, 'carbs': 1.9, 'fat': 4.8, 'fiber': 0.3, 'category': 'legumes'},
    '豆浆': {'calories': 33, 'protein': 2.9, 'carbs': 1.8, 'fat': 1.9, 'fiber': 0.6, 'category': 'legumes'},
    '黄豆': {'calories': 446, 'protein': 36.0, 'carbs': 30.0, 'fat': 20.0, 'fiber': 9.3, 'category': 'legumes'},
    '黑豆': {'calories': 381, 'protein': 36.0, 'carbs': 36.0, 'fat': 1.4, 'fiber': 15.0, 'category': 'legumes'},
    '红豆': {'calories': 329, 'protein': 20.0, 'carbs': 57.0, 'fat': 0.5, 'fiber': 12.0, 'category': 'legumes'},
    
    # 蔬菜类 / Vegetables
    '西兰花': {'calories': 34, 'protein': 2.8, 'carbs': 7.0, 'fat': 0.4, 'fiber': 2.6, 'category': 'vegetables'},
    '菠菜': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2, 'category': 'vegetables'},
    '胡萝卜': {'calories': 41, 'protein': 0.9, 'carbs': 10.0, 'fat': 0.2, 'fiber': 2.8, 'category': 'vegetables'},
    '番茄': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'fiber': 1.2, 'category': 'vegetables'},
    '黄瓜': {'calories': 15, 'protein': 0.7, 'carbs': 3.6, 'fat': 0.1, 'fiber': 0.5, 'category': 'vegetables'},
    '白菜': {'calories': 13, 'protein': 1.2, 'carbs': 2.2, 'fat': 0.2, 'fiber': 1.1, 'category': 'vegetables'},
    '芹菜': {'calories': 14, 'protein': 0.7, 'carbs': 3.0, 'fat': 0.2, 'fiber': 1.6, 'category': 'vegetables'},
    
    # 水果类 / Fruits
    '苹果': {'calories': 52, 'protein': 0.3, 'carbs': 14.0, 'fat': 0.2, 'fiber': 2.4, 'category': 'fruits'},
    '香蕉': {'calories': 89, 'protein': 1.1, 'carbs': 23.0, 'fat': 0.3, 'fiber': 2.6, 'category': 'fruits'},
    '橙子': {'calories': 47, 'protein': 0.9, 'carbs': 12.0, 'fat': 0.1, 'fiber': 2.4, 'category': 'fruits'},
    '葡萄': {'calories': 69, 'protein': 0.7, 'carbs': 18.0, 'fat': 0.2, 'fiber': 0.9, 'category': 'fruits'},
    '草莓': {'calories': 32, 'protein': 0.7, 'carbs': 7.7, 'fat': 0.3, 'fiber': 2.0, 'category': 'fruits'},
    '西瓜': {'calories': 30, 'protein': 0.6, 'carbs': 8.0, 'fat': 0.2, 'fiber': 0.4, 'category': 'fruits'},
    '芒果': {'calories': 60, 'protein': 0.8, 'carbs': 15.0, 'fat': 0.4, 'fiber': 1.6, 'category': 'fruits'},
    
    # 坚果类 / Nuts
    '杏仁': {'calories': 579, 'protein': 21.0, 'carbs': 22.0, 'fat': 50.0, 'fiber': 12.5, 'category': 'nuts'},
    '核桃': {'calories': 654, 'protein': 15.0, 'carbs': 14.0, 'fat': 65.0, 'fiber': 6.7, 'category': 'nuts'},
    '花生': {'calories': 567, 'protein': 25.0, 'carbs': 16.0, 'fat': 49.0, 'fiber': 8.5, 'category': 'nuts'},
    '腰果': {'calories': 553, 'protein': 18.0, 'carbs': 30.0, 'fat': 44.0, 'fiber': 3.3, 'category': 'nuts'},
    
    # 油脂类 / Oils
    '橄榄油': {'calories': 884, 'protein': 0, 'carbs': 0, 'fat': 100.0, 'fiber': 0, 'category': 'oils'},
    '植物油': {'calories': 884, 'protein': 0, 'carbs': 0, 'fat': 100.0, 'fiber': 0, 'category': 'oils'},
    '黄油': {'calories': 717, 'protein': 0.9, 'carbs': 0.1, 'fat': 81.0, 'fiber': 0, 'category': 'oils'},
    
    # 饮料 / Beverages
    '可乐': {'calories': 42, 'protein': 0, 'carbs': 10.6, 'fat': 0, 'fiber': 0, 'category': 'beverages'},
    '橙汁': {'calories': 45, 'protein': 0.7, 'carbs': 10.4, 'fat': 0.2, 'fiber': 0.2, 'category': 'beverages'},
    '咖啡（黑）': {'calories': 2, 'protein': 0.3, 'carbs': 0, 'fat': 0, 'fiber': 0, 'category': 'beverages'},
    '绿茶': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0, 'category': 'beverages'},
    
    # 零食 / Snacks
    '薯片': {'calories': 536, 'protein': 7.0, 'carbs': 53.0, 'fat': 35.0, 'fiber': 4.4, 'category': 'snacks'},
    '巧克力': {'calories': 546, 'protein': 5.0, 'carbs': 60.0, 'fat': 31.0, 'fiber': 7.0, 'category': 'snacks'},
    '冰淇淋': {'calories': 207, 'protein': 3.5, 'carbs': 24.0, 'fat': 11.0, 'fiber': 0.7, 'category': 'snacks'},
}

# Category names in Chinese
CATEGORY_NAMES = {
    'staples': '主食',
    'meat': '肉类',
    'seafood': '海鲜',
    'eggs_dairy': '蛋奶',
    'legumes': '豆类',
    'vegetables': '蔬菜',
    'fruits': '水果',
    'nuts': '坚果',
    'oils': '油脂',
    'beverages': '饮料',
    'snacks': '零食',
}

# Recommended daily intake of vitamins and minerals
VITAMIN_MINERALS_RDA = {
    # Vitamins
    'vitamin_a': {'rda': 900, 'unit': 'mcg', 'name': '维生素A', 'name_en': 'Vitamin A'},
    'vitamin_c': {'rda': 90, 'unit': 'mg', 'name': '维生素C', 'name_en': 'Vitamin C'},
    'vitamin_d': {'rda': 20, 'unit': 'mcg', 'name': '维生素D', 'name_en': 'Vitamin D'},
    'vitamin_e': {'rda': 15, 'unit': 'mg', 'name': '维生素E', 'name_en': 'Vitamin E'},
    'vitamin_k': {'rda': 120, 'unit': 'mcg', 'name': '维生素K', 'name_en': 'Vitamin K'},
    'thiamin': {'rda': 1.2, 'unit': 'mg', 'name': '维生素B1', 'name_en': 'Thiamin (B1)'},
    'riboflavin': {'rda': 1.3, 'unit': 'mg', 'name': '维生素B2', 'name_en': 'Riboflavin (B2)'},
    'niacin': {'rda': 16, 'unit': 'mg', 'name': '维生素B3', 'name_en': 'Niacin (B3)'},
    'vitamin_b6': {'rda': 1.7, 'unit': 'mg', 'name': '维生素B6', 'name_en': 'Vitamin B6'},
    'folate': {'rda': 400, 'unit': 'mcg', 'name': '叶酸', 'name_en': 'Folate'},
    'vitamin_b12': {'rda': 2.4, 'unit': 'mcg', 'name': '维生素B12', 'name_en': 'Vitamin B12'},
    
    # Minerals
    'calcium': {'rda': 1000, 'unit': 'mg', 'name': '钙', 'name_en': 'Calcium'},
    'iron': {'rda': 8, 'unit': 'mg', 'name': '铁', 'name_en': 'Iron'},
    'magnesium': {'rda': 420, 'unit': 'mg', 'name': '镁', 'name_en': 'Magnesium'},
    'phosphorus': {'rda': 700, 'unit': 'mg', 'name': '磷', 'name_en': 'Phosphorus'},
    'potassium': {'rda': 4700, 'unit': 'mg', 'name': '钾', 'name_en': 'Potassium'},
    'sodium': {'rda': 2300, 'unit': 'mg', 'name': '钠', 'name_en': 'Sodium'},
    'zinc': {'rda': 11, 'unit': 'mg', 'name': '锌', 'name_en': 'Zinc'},
    'selenium': {'rda': 55, 'unit': 'mcg', 'name': '硒', 'name_en': 'Selenium'},
}


# ============================================================================
# Enums
# ============================================================================

class ActivityLevel(Enum):
    """活动水平枚举"""
    SEDENTARY = 'sedentary'           # 久坐
    LIGHT = 'light'                   # 轻度活动
    MODERATE = 'moderate'             # 中度活动
    ACTIVE = 'active'                 # 高度活动
    VERY_ACTIVE = 'very_active'       # 非常活跃


class Goal(Enum):
    """健身目标枚举"""
    LOSE_WEIGHT = 'lose_weight'       # 减脂
    MAINTAIN = 'maintain'             # 维持
    GAIN_MUSCLE = 'gain_muscle'       # 增肌


class Gender(Enum):
    """性别枚举"""
    MALE = 'male'
    FEMALE = 'female'


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class FoodItem:
    """食物项"""
    name: str
    amount: float  # 克数
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float
    category: str = 'unknown'


@dataclass
class NutritionSummary:
    """营养摘要"""
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    total_fiber: float
    protein_calories: float
    carbs_calories: float
    fat_calories: float
    protein_ratio: float  # 蛋白质供能比
    carbs_ratio: float    # 碳水供能比
    fat_ratio: float      # 脂肪供能比
    food_count: int
    food_items: List[FoodItem]


@dataclass
class DailyNeeds:
    """每日营养需求"""
    calories: float
    protein: float      # 克
    carbs: float        # 克
    fat: float          # 克
    fiber: float        # 克
    activity_level: str
    goal: str


@dataclass
class NutrientAnalysis:
    """营养分析结果"""
    calories: float
    calories_target: float
    calories_percent: float
    protein: float
    protein_target: float
    protein_percent: float
    carbs: float
    carbs_target: float
    carbs_percent: float
    fat: float
    fat_target: float
    fat_percent: float
    fiber: float
    fiber_target: float
    fiber_percent: float
    balance_score: float  # 0-100 营养平衡分数
    recommendations: List[str]


# ============================================================================
# Core Functions
# ============================================================================

def get_food_info(food_name: str) -> Optional[Dict]:
    """
    获取食物营养信息.
    
    Args:
        food_name: 食物名称
    
    Returns:
        食物营养信息字典，如果不存在返回 None
    
    Examples:
        >>> get_food_info('米饭')
        {'calories': 116, 'protein': 2.6, ...}
    """
    return FOOD_DATABASE.get(food_name)


def search_foods(keyword: str, limit: int = 10) -> List[str]:
    """
    搜索食物.
    
    Args:
        keyword: 搜索关键词
        limit: 返回数量限制
    
    Returns:
        匹配的食物名称列表
    
    Examples:
        >>> search_foods('鸡')
        ['鸡胸肉', '鸡腿肉']
    """
    keyword = keyword.lower()
    results = []
    for name in FOOD_DATABASE:
        if keyword in name.lower():
            results.append(name)
            if len(results) >= limit:
                break
    return results


def get_foods_by_category(category: str) -> List[str]:
    """
    按分类获取食物列表.
    
    Args:
        category: 分类名称
    
    Returns:
        该分类下的食物列表
    
    Examples:
        >>> get_foods_by_category('meat')
        ['鸡胸肉', '鸡腿肉', '牛肉', ...]
    """
    return [name for name, info in FOOD_DATABASE.items() 
            if info.get('category') == category]


def calculate_food_nutrition(food_name: str, amount: float = 100) -> Optional[FoodItem]:
    """
    计算指定数量食物的营养成分.
    
    Args:
        food_name: 食物名称
        amount: 数量（克）
    
    Returns:
        FoodItem 对象，如果食物不存在返回 None
    
    Examples:
        >>> calculate_food_nutrition('米饭', 200)
        FoodItem(name='米饭', amount=200, calories=232, ...)
    """
    info = get_food_info(food_name)
    if info is None:
        return None
    
    multiplier = amount / 100.0
    
    return FoodItem(
        name=food_name,
        amount=amount,
        calories=round(info['calories'] * multiplier, 1),
        protein=round(info['protein'] * multiplier, 1),
        carbs=round(info['carbs'] * multiplier, 1),
        fat=round(info['fat'] * multiplier, 1),
        fiber=round(info.get('fiber', 0) * multiplier, 1),
        category=info.get('category', 'unknown')
    )


def calculate_meal_nutrition(foods: List[Tuple[str, float]]) -> NutritionSummary:
    """
    计算一餐或多种食物的总营养.
    
    Args:
        foods: 食物列表，每项为 (食物名称, 克数)
    
    Returns:
        NutritionSummary 对象
    
    Examples:
        >>> calculate_meal_nutrition([('米饭', 200), ('鸡胸肉', 150)])
        NutritionSummary(total_calories=..., ...)
    """
    food_items = []
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_fiber = 0
    
    for food_name, amount in foods:
        item = calculate_food_nutrition(food_name, amount)
        if item:
            food_items.append(item)
            total_calories += item.calories
            total_protein += item.protein
            total_carbs += item.carbs
            total_fat += item.fat
            total_fiber += item.fiber
    
    # 计算热量来源
    protein_calories = total_protein * CALORIES_PER_GRAM['protein']
    carbs_calories = total_carbs * CALORIES_PER_GRAM['carbs']
    fat_calories = total_fat * CALORIES_PER_GRAM['fat']
    total_macro_calories = protein_calories + carbs_calories + fat_calories
    
    # 计算比例
    if total_macro_calories > 0:
        protein_ratio = round(protein_calories / total_macro_calories * 100, 1)
        carbs_ratio = round(carbs_calories / total_macro_calories * 100, 1)
        fat_ratio = round(fat_calories / total_macro_calories * 100, 1)
    else:
        protein_ratio = carbs_ratio = fat_ratio = 0
    
    return NutritionSummary(
        total_calories=round(total_calories, 1),
        total_protein=round(total_protein, 1),
        total_carbs=round(total_carbs, 1),
        total_fat=round(total_fat, 1),
        total_fiber=round(total_fiber, 1),
        protein_calories=round(protein_calories, 1),
        carbs_calories=round(carbs_calories, 1),
        fat_calories=round(fat_calories, 1),
        protein_ratio=protein_ratio,
        carbs_ratio=carbs_ratio,
        fat_ratio=fat_ratio,
        food_count=len(food_items),
        food_items=food_items
    )


def calculate_calories_from_macros(protein: float, carbs: float, fat: float) -> float:
    """
    从宏量营养素计算热量.
    
    Args:
        protein: 蛋白质（克）
        carbs: 碳水化合物（克）
        fat: 脂肪（克）
    
    Returns:
        总热量（千卡）
    
    Examples:
        >>> calculate_calories_from_macros(30, 50, 20)
        500.0
    """
    return (protein * 4) + (carbs * 4) + (fat * 9)


def calculate_macros_from_calories(
    calories: float,
    protein_ratio: float = 0.30,
    carbs_ratio: float = 0.40,
    fat_ratio: float = 0.30
) -> Tuple[float, float, float]:
    """
    从总热量和比例计算宏量营养素.
    
    Args:
        calories: 总热量（千卡）
        protein_ratio: 蛋白质供能比（默认 30%）
        carbs_ratio: 碳水供能比（默认 40%）
        fat_ratio: 脂肪供能比（默认 30%）
    
    Returns:
        (蛋白质克数, 碳水克数, 脂肪克数)
    
    Examples:
        >>> calculate_macros_from_calories(2000)
        (150.0, 200.0, 66.7)
    """
    protein = (calories * protein_ratio) / 4
    carbs = (calories * carbs_ratio) / 4
    fat = (calories * fat_ratio) / 9
    
    return round(protein, 1), round(carbs, 1), round(fat, 1)


# ============================================================================
# Daily Needs Calculation
# ============================================================================

def calculate_bmr(
    weight: float,
    height: float,
    age: int,
    gender: Gender
) -> float:
    """
    使用 Mifflin-St Jeor 公式计算基础代谢率.
    
    Args:
        weight: 体重（kg）
        height: 身高（cm）
        age: 年龄
        gender: 性别
    
    Returns:
        BMR（千卡/天）
    
    Examples:
        >>> calculate_bmr(70, 175, 30, Gender.MALE)
        1675.0
    """
    if gender == Gender.MALE:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    return round(bmr, 0)


def calculate_tdee(bmr: float, activity_level: ActivityLevel) -> float:
    """
    计算总每日能量消耗 (TDEE).
    
    Args:
        bmr: 基础代谢率
        activity_level: 活动水平
    
    Returns:
        TDEE（千卡/天）
    
    Examples:
        >>> calculate_tdee(1700, ActivityLevel.MODERATE)
        2635.0
    """
    activity_factors = {
        ActivityLevel.SEDENTARY: 1.2,
        ActivityLevel.LIGHT: 1.375,
        ActivityLevel.MODERATE: 1.55,
        ActivityLevel.ACTIVE: 1.725,
        ActivityLevel.VERY_ACTIVE: 1.9,
    }
    
    factor = activity_factors.get(activity_level, 1.2)
    return round(bmr * factor, 0)


def calculate_daily_needs(
    weight: float,
    height: float,
    age: int,
    gender: Gender,
    activity_level: ActivityLevel = ActivityLevel.MODERATE,
    goal: Goal = Goal.MAINTAIN
) -> DailyNeeds:
    """
    计算每日营养需求.
    
    Args:
        weight: 体重（kg）
        height: 身高（cm）
        age: 年龄
        gender: 性别
        activity_level: 活动水平
        goal: 健身目标
    
    Returns:
        DailyNeeds 对象
    
    Examples:
        >>> calculate_daily_needs(70, 175, 30, Gender.MALE)
        DailyNeeds(calories=..., protein=..., ...)
    """
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    
    # 根据目标调整热量
    goal_adjustments = {
        Goal.LOSE_WEIGHT: 0.8,    # 热量缺口 20%
        Goal.MAINTAIN: 1.0,       # 维持
        Goal.GAIN_MUSCLE: 1.1,    # 热量盈余 10%
    }
    
    adjustment = goal_adjustments.get(goal, 1.0)
    target_calories = tdee * adjustment
    
    # 根据目标调整宏量营养素比例
    if goal == Goal.LOSE_WEIGHT:
        protein_ratio = 0.35
        carbs_ratio = 0.35
        fat_ratio = 0.30
    elif goal == Goal.GAIN_MUSCLE:
        protein_ratio = 0.30
        carbs_ratio = 0.45
        fat_ratio = 0.25
    else:
        protein_ratio = 0.25
        carbs_ratio = 0.50
        fat_ratio = 0.25
    
    protein, carbs, fat = calculate_macros_from_calories(
        target_calories, protein_ratio, carbs_ratio, fat_ratio
    )
    
    # 纤维建议：每 1000 kcal 约 14g
    fiber = round(target_calories / 1000 * 14, 1)
    
    return DailyNeeds(
        calories=round(target_calories, 0),
        protein=protein,
        carbs=carbs,
        fat=fat,
        fiber=fiber,
        activity_level=activity_level.value,
        goal=goal.value
    )


def calculate_protein_needs(
    weight: float,
    activity_level: ActivityLevel = ActivityLevel.MODERATE,
    goal: Goal = Goal.MAINTAIN
) -> float:
    """
    计算蛋白质需求.
    
    Args:
        weight: 体重（kg）
        activity_level: 活动水平
        goal: 健身目标
    
    Returns:
        蛋白质需求（克/天）
    
    Examples:
        >>> calculate_protein_needs(70, ActivityLevel.ACTIVE, Goal.GAIN_MUSCLE)
        140.0
    """
    # 基础蛋白质需求（克/千克体重）
    base_protein = {
        ActivityLevel.SEDENTARY: 0.8,
        ActivityLevel.LIGHT: 1.0,
        ActivityLevel.MODERATE: 1.2,
        ActivityLevel.ACTIVE: 1.6,
        ActivityLevel.VERY_ACTIVE: 2.0,
    }
    
    multiplier = base_protein.get(activity_level, 1.0)
    
    # 根据目标调整
    if goal == Goal.LOSE_WEIGHT:
        multiplier *= 1.2  # 减脂期需要更多蛋白质
    elif goal == Goal.GAIN_MUSCLE:
        multiplier *= 1.2  # 增肌期也需要更多蛋白质
    
    return round(weight * multiplier, 1)


# ============================================================================
# Nutrient Analysis
# ============================================================================

def analyze_nutrition(
    foods: List[Tuple[str, float]],
    daily_needs: DailyNeeds
) -> NutrientAnalysis:
    """
    分析营养摄入情况.
    
    Args:
        foods: 食物列表
        daily_needs: 每日营养需求
    
    Returns:
        NutrientAnalysis 对象
    
    Examples:
        >>> needs = calculate_daily_needs(70, 175, 30, Gender.MALE)
        >>> analyze_nutrition([('米饭', 200), ('鸡胸肉', 150)], needs)
        NutrientAnalysis(...)
    """
    summary = calculate_meal_nutrition(foods)
    
    # 计算达标百分比
    calories_percent = round(summary.total_calories / daily_needs.calories * 100, 1)
    protein_percent = round(summary.total_protein / daily_needs.protein * 100, 1)
    carbs_percent = round(summary.total_carbs / daily_needs.carbs * 100, 1)
    fat_percent = round(summary.total_fat / daily_needs.fat * 100, 1)
    fiber_percent = round(summary.total_fiber / daily_needs.fiber * 100, 1)
    
    # 计算平衡分数（基于三大营养素比例）
    ideal_ratios = {'protein': 30, 'carbs': 40, 'fat': 30}
    protein_score = max(0, 100 - abs(summary.protein_ratio - ideal_ratios['protein']) * 2)
    carbs_score = max(0, 100 - abs(summary.carbs_ratio - ideal_ratios['carbs']) * 2)
    fat_score = max(0, 100 - abs(summary.fat_ratio - ideal_ratios['fat']) * 2)
    balance_score = round((protein_score + carbs_score + fat_score) / 3, 1)
    
    # 生成建议
    recommendations = []
    
    if calories_percent < 80:
        recommendations.append(f"热量摄入不足（{calories_percent}%），建议增加食物摄入")
    elif calories_percent > 120:
        recommendations.append(f"热量摄入超标（{calories_percent}%），建议控制饮食")
    
    if protein_percent < 80:
        recommendations.append(f"蛋白质摄入不足（{protein_percent}%），建议增加优质蛋白")
    
    if fiber_percent < 80:
        recommendations.append(f"膳食纤维摄入不足（{fiber_percent}%），建议增加蔬果摄入")
    
    if fat_percent > 120:
        recommendations.append(f"脂肪摄入超标（{fat_percent}%），建议减少油腻食物")
    
    if balance_score < 60:
        recommendations.append(f"营养比例失衡（{balance_score}分），建议调整饮食结构")
    
    if not recommendations:
        recommendations.append("营养摄入情况良好，继续保持！")
    
    return NutrientAnalysis(
        calories=summary.total_calories,
        calories_target=daily_needs.calories,
        calories_percent=calories_percent,
        protein=summary.total_protein,
        protein_target=daily_needs.protein,
        protein_percent=protein_percent,
        carbs=summary.total_carbs,
        carbs_target=daily_needs.carbs,
        carbs_percent=carbs_percent,
        fat=summary.total_fat,
        fat_target=daily_needs.fat,
        fat_percent=fat_percent,
        fiber=summary.total_fiber,
        fiber_target=daily_needs.fiber,
        fiber_percent=fiber_percent,
        balance_score=balance_score,
        recommendations=recommendations
    )


def get_meal_suggestion(
    target_calories: float,
    target_protein: float,
    preferences: Optional[List[str]] = None
) -> List[Tuple[str, float]]:
    """
    生成饮食建议.
    
    Args:
        target_calories: 目标热量
        target_protein: 目标蛋白质
        preferences: 食物偏好（可选）
    
    Returns:
        建议的食物列表
    
    Examples:
        >>> get_meal_suggestion(500, 30)
        [('米饭', 150), ('鸡胸肉', 100), ...]
    """
    suggestions = []
    remaining_calories = target_calories
    remaining_protein = target_protein
    
    # 简单的建议算法
    # 优先选择高蛋白食物
    protein_foods = ['鸡胸肉', '三文鱼', '虾', '牛肉', '鸡蛋', '豆腐']
    carb_foods = ['米饭', '面条', '红薯', '土豆', '燕麦']
    veg_foods = ['西兰花', '菠菜', '番茄', '黄瓜', '胡萝卜']
    
    # 添加蛋白质来源
    for food in protein_foods:
        if remaining_protein <= 0 or remaining_calories <= 0:
            break
        info = get_food_info(food)
        if info:
            # 计算需要的量来满足蛋白质需求
            amount = min(200, remaining_protein / info['protein'] * 100)
            if amount > 50:
                suggestions.append((food, round(amount)))
                remaining_calories -= info['calories'] * amount / 100
                remaining_protein -= info['protein'] * amount / 100
    
    # 添加碳水化合物来源
    for food in carb_foods:
        if remaining_calories <= 100:
            break
        info = get_food_info(food)
        if info:
            amount = min(200, remaining_calories / info['calories'] * 100)
            if amount > 50:
                suggestions.append((food, round(amount)))
                remaining_calories -= info['calories'] * amount / 100
    
    # 添加蔬菜
    for food in veg_foods:
        if remaining_calories <= 50:
            break
        info = get_food_info(food)
        if info:
            suggestions.append((food, 100))
            remaining_calories -= info['calories']
    
    return suggestions


# ============================================================================
# Utility Functions
# ============================================================================

def get_all_foods() -> List[str]:
    """获取所有食物名称列表."""
    return list(FOOD_DATABASE.keys())


def get_all_categories() -> List[str]:
    """获取所有分类列表."""
    return list(set(info.get('category', 'unknown') for info in FOOD_DATABASE.values()))


def format_nutrition_label(food_name: str, amount: float = 100) -> str:
    """
    格式化营养成分标签.
    
    Args:
        food_name: 食物名称
        amount: 数量（克）
    
    Returns:
        格式化的营养成分标签字符串
    
    Examples:
        >>> print(format_nutrition_label('鸡胸肉', 100))
        鸡胸肉 (100g)
        ================
        热量: 165 kcal
        蛋白质: 31.0g
        碳水化合物: 0.0g
        脂肪: 3.6g
        膳食纤维: 0.0g
    """
    item = calculate_food_nutrition(food_name, amount)
    if item is None:
        return f"未找到食物: {food_name}"
    
    lines = [
        f"{food_name} ({amount}g)",
        "=" * 20,
        f"热量: {item.calories:.1f} kcal",
        f"蛋白质: {item.protein:.1f}g",
        f"碳水化合物: {item.carbs:.1f}g",
        f"脂肪: {item.fat:.1f}g",
        f"膳食纤维: {item.fiber:.1f}g",
    ]
    
    return "\n".join(lines)


def format_meal_summary(foods: List[Tuple[str, float]]) -> str:
    """
    格式化餐饮营养摘要.
    
    Args:
        foods: 食物列表
    
    Returns:
        格式化的营养摘要字符串
    """
    summary = calculate_meal_nutrition(foods)
    
    lines = [
        "餐饮营养摘要",
        "=" * 30,
        f"食物数量: {summary.food_count} 种",
        "",
        "营养素摄入:",
        f"  热量: {summary.total_calories:.1f} kcal",
        f"  蛋白质: {summary.total_protein:.1f}g",
        f"  碳水化合物: {summary.total_carbs:.1f}g",
        f"  脂肪: {summary.total_fat:.1f}g",
        f"  膳食纤维: {summary.total_fiber:.1f}g",
        "",
        "热量来源分布:",
        f"  蛋白质: {summary.protein_ratio:.1f}%",
        f"  碳水化合物: {summary.carbs_ratio:.1f}%",
        f"  脂肪: {summary.fat_ratio:.1f}%",
        "",
        "食物明细:",
    ]
    
    for item in summary.food_items:
        lines.append(f"  - {item.name} ({item.amount}g): {item.calories:.1f} kcal")
    
    return "\n".join(lines)


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Nutrition Utilities Demo")
    print("=" * 60)
    
    # 食物搜索
    print("\n--- 食物搜索 ---")
    results = search_foods('鸡')
    print(f"搜索 '鸡': {results}")
    
    # 营养成分
    print("\n--- 食物营养成分 ---")
    print(format_nutrition_label('鸡胸肉', 100))
    
    # 餐饮计算
    print("\n--- 餐饮营养计算 ---")
    foods = [
        ('米饭', 200),
        ('鸡胸肉', 150),
        ('西兰花', 100),
        ('橄榄油', 10),
    ]
    print(format_meal_summary(foods))
    
    # 每日需求计算
    print("\n--- 每日营养需求 ---")
    needs = calculate_daily_needs(70, 175, 30, Gender.MALE, ActivityLevel.MODERATE, Goal.MAINTAIN)
    print(f"热量需求: {needs.calories:.0f} kcal")
    print(f"蛋白质需求: {needs.protein:.1f}g")
    print(f"碳水化合物需求: {needs.carbs:.1f}g")
    print(f"脂肪需求: {needs.fat:.1f}g")
    print(f"膳食纤维需求: {needs.fiber:.1f}g")
    
    # 减脂需求
    print("\n--- 减脂期营养需求 ---")
    needs_cut = calculate_daily_needs(70, 175, 30, Gender.MALE, ActivityLevel.MODERATE, Goal.LOSE_WEIGHT)
    print(f"热量需求: {needs_cut.calories:.0f} kcal")
    print(f"蛋白质需求: {needs_cut.protein:.1f}g")
    
    # 增肌需求
    print("\n--- 增肌期营养需求 ---")
    needs_bulk = calculate_daily_needs(70, 175, 30, Gender.MALE, ActivityLevel.ACTIVE, Goal.GAIN_MUSCLE)
    print(f"热量需求: {needs_bulk.calories:.0f} kcal")
    print(f"蛋白质需求: {needs_bulk.protein:.1f}g")
    
    # 营养分析
    print("\n--- 营养分析 ---")
    analysis = analyze_nutrition(foods, needs)
    print(f"热量达标率: {analysis.calories_percent}%")
    print(f"蛋白质达标率: {analysis.protein_percent}%")
    print(f"营养平衡分数: {analysis.balance_score}/100")
    print(f"建议: {analysis.recommendations[0]}")
    
    # 饮食建议
    print("\n--- 饮食建议 ---")
    suggestions = get_meal_suggestion(600, 40)
    for food, amount in suggestions:
        print(f"  {food}: {amount}g")
    
    print("\n" + "=" * 60)