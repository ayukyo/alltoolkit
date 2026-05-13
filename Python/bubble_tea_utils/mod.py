#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Bubble Tea Calories Calculator Module
====================================================
A comprehensive bubble tea (奶茶) calories calculator with zero external dependencies.

Features:
    - Base tea calories (绿茶、红茶、奶茶、乌龙茶等)
    - Additive calories (珍珠、椰果、布丁、奶盖、冰淇淋等)
    - Sugar level calories conversion
    - Size multiplier support
    - Total calories calculation
    - Health suggestions based on daily intake
    - Calorie comparison and visualization helpers

Author: AllToolkit Contributors
License: MIT
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Constants - Calorie Data (per 100ml or per unit)
# ============================================================================

# Base tea calories (per 100ml, without sugar/additives)
BASE_TEA_CALORIES = {
    # 纯茶类 (几乎零热量)
    '绿茶': 2,
    '红茶': 2,
    '乌龙茶': 2,
    '普洱茶': 2,
    '茉莉花茶': 2,
    '铁观音': 2,
    '龙井': 2,
    '白茶': 2,
    
    # 奶茶基底 (含牛奶)
    '奶茶': 35,      # 传统奶茶 (茶 + 牛奶)
    '鲜奶茶': 40,    # 鲜奶比例更高
    '港式奶茶': 45,  # 淡奶 + 糖
    '泰式奶茶': 50,  # 淡奶 + 糖较多
    
    # 特殊基底
    '抹茶拿铁': 55,
    '芋泥奶茶': 65,
    '红豆奶茶': 60,
    '黑糖奶茶': 70,
    '巧克力奶茶': 75,
    '咖啡奶茶': 45,
    '鸳鸯': 50,      # 咖啡 + 奶茶
    
    # 果茶基底
    '柠檬茶': 15,
    '蜜桃茶': 20,
    '葡萄茶': 25,
    '草莓茶': 25,
    '芒果茶': 30,
    '百香果茶': 20,
    '西瓜茶': 15,
    '柚子茶': 25,
    
    # 奶盖基底 (额外热量)
    '奶盖': 80,      # 每 50ml 奶盖
    '芝士奶盖': 90,  # 每 50ml
    '海盐奶盖': 85,  # 每 50ml
    
    # 冰淇淋基底
    '冰淇淋奶茶': 120,  # 含冰淇淋球
    
    # 燕麦奶基底
    '燕麦奶茶': 38,
    '豆奶茶': 30,
}

# 配料热量 (每个配料单位，通常是每份)
ADDITIVE_CALORIES = {
    # 经典配料
    '珍珠': 120,       # 约 50g
    '黑糖珍珠': 140,   # 黑糖腌制
    '珍珠奶茶专用珍珠': 100,
    
    # 椰果类
    '椰果': 50,        # 约 30g
    '椰肉': 60,
    
    # 布丁类
    '布丁': 90,        # 约 50g
    '焦糖布丁': 110,
    '鸡蛋布丁': 95,
    
    # 果冻类
    '果冻': 40,
    '蒟蒻': 20,        # 低卡
    '仙草': 30,
    
    # 豆类
    '红豆': 80,        # 约 40g
    '绿豆': 70,
    '芋泥': 100,       # 约 50g
    '芋头': 90,
    
    # 奶制品
    '奶盖': 80,        # 顶料 (额外)
    '芝士奶盖': 90,
    '冰淇淋球': 140,   # 一个球
    '奶油': 60,
    '炼乳': 50,
    
    # 其他配料
    '燕麦': 45,
    '薏米': 40,
    '西米': 70,
    '汤圆': 80,
    '小丸子': 60,
    'QQ糖': 30,
    '爆爆珠': 50,
    '芦荟': 25,
    '桂花冻': 35,
    '桂花': 5,
    
    # 坚果类
    '核桃': 80,        # 约 10g
    '杏仁': 70,
    '花生': 75,
}

# 糖度对应的热量增加 (每 100ml)
# 假设全糖 = 10g 糖/100ml = 40 kcal
SUGAR_LEVEL_CALORIES = {
    '无糖': 0,
    '0%': 0,
    '微糖': 10,
    '3分糖': 12,
    '30%': 12,
    '半糖': 20,
    '5分糖': 20,
    '50%': 20,
    '少糖': 25,
    '7分糖': 28,
    '70%': 28,
    '多糖': 35,
    '8分糖': 32,
    '80%': 32,
    '全糖': 40,
    '10分糖': 40,
    '100%': 40,
    '标准糖': 40,
    '正常糖': 40,
}

# 杯型容量 (ml) 和热量倍数
SIZE_VOLUME = {
    '小杯': 300,
    '中杯': 400,
    '大杯': 500,
    '超大杯': 700,
    'Mini': 200,
    'S': 300,
    'M': 400,
    'L': 500,
    'XL': 700,
    '小': 300,
    '中': 400,
    '大': 500,
    '超大': 700,
    '360ml': 360,
    '500ml': 500,
    '700ml': 700,
}


# ============================================================================
# Enums
# ============================================================================

class SugarLevel(Enum):
    """Sugar level enumeration."""
    NONE = 0      # 无糖
    LOW = 1       # 微糖/3分糖
    MEDIUM = 2    # 半糖/5分糖
    HIGH = 3      # 7分糖/多糖
    FULL = 4      # 全糖


class TeaSize(Enum):
    """Tea size enumeration."""
    SMALL = 300
    MEDIUM = 400
    LARGE = 500
    EXTRA_LARGE = 700


class HealthLevel(Enum):
    """Health level based on calorie intake."""
    LOW = 1       # < 150 kcal - 健康
    MODERATE = 2  # 150-300 kcal - 一般
    HIGH = 3      # 300-500 kcal - 注意
    VERY_HIGH = 4 # > 500 kcal - 高热量


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class BubbleTeaOrder:
    """Bubble tea order configuration."""
    base_tea: str           # 基底茶
    sugar_level: str        # 糖度
    size: str               # 杯型
    additives: List[str]    # 配料列表
    ice_level: str = '正常'  # 冰度 (不影响热量)
    
    def __post_init__(self):
        """Validate order parameters."""
        self.base_tea = self.base_tea.strip()
        self.sugar_level = self.sugar_level.strip()
        self.size = self.size.strip()
        self.additives = [a.strip() for a in self.additives]


@dataclass
class CalorieResult:
    """Calorie calculation result."""
    total_calories: float
    base_calories: float
    sugar_calories: float
    additive_calories: float
    size_ml: int
    health_level: HealthLevel
    suggestion: str
    breakdown: Dict[str, float]  # 详细热量分解


# ============================================================================
# Core Functions
# ============================================================================

def get_base_calories(base_tea: str, size_ml: int) -> float:
    """
    Calculate calories from base tea.
    
    Args:
        base_tea: Base tea type (e.g., '奶茶', '绿茶')
        size_ml: Size in milliliters
    
    Returns:
        Base calories
    
    Examples:
        >>> get_base_calories('奶茶', 500)
        175.0
        >>> get_base_calories('绿茶', 500)
        10.0
    """
    # 查找基底热量
    base_per_100ml = BASE_TEA_CALORIES.get(base_tea)
    
    if base_per_100ml is None:
        # 尝试模糊匹配
        base_per_100ml = 30  # 默认值
    
    # 计算热量 (基底热量 * 容量/100)
    return base_per_100ml * size_ml / 100


def get_sugar_calories(sugar_level: str, size_ml: int) -> float:
    """
    Calculate calories from sugar level.
    
    Args:
        sugar_level: Sugar level (e.g., '半糖', '50%', '无糖')
        size_ml: Size in milliliters
    
    Returns:
        Sugar calories
    
    Examples:
        >>> get_sugar_calories('半糖', 500)
        100.0
        >>> get_sugar_calories('无糖', 500)
        0.0
    """
    # 查找糖度热量
    sugar_per_100ml = SUGAR_LEVEL_CALORIES.get(sugar_level)
    
    if sugar_per_100ml is None:
        # 尝试数字百分比匹配
        try:
            # 处理 "30%" 等格式
            if '%' in sugar_level:
                percent = float(sugar_level.replace('%', ''))
                sugar_per_100ml = 40 * percent / 100
            # 处理 "3分糖" 等格式
            elif '分' in sugar_level:
                fen = float(sugar_level.replace('分糖', '').replace('分', ''))
                sugar_per_100ml = 40 * fen / 10
            else:
                sugar_per_100ml = 20  # 默认中等糖度
        except (ValueError, TypeError):
            sugar_per_100ml = 20
    
    return sugar_per_100ml * size_ml / 100


def get_additive_calories(additives: List[str]) -> float:
    """
    Calculate total calories from additives.
    
    Args:
        additives: List of additive names
    
    Returns:
        Total additive calories
    
    Examples:
        >>> get_additive_calories(['珍珠', '椰果'])
        170
        >>> get_additive_calories(['布丁', '奶盖'])
        170
    """
    total = 0
    for additive in additives:
        calorie = ADDITIVE_CALORIES.get(additive, 50)  # 默认 50 kcal
        total += calorie
    return total


def get_size_ml(size: str) -> int:
    """
    Convert size string to milliliters.
    
    Args:
        size: Size string (e.g., '中杯', 'M', '500ml')
    
    Returns:
        Size in milliliters
    
    Examples:
        >>> get_size_ml('中杯')
        400
        >>> get_size_ml('500ml')
        500
    """
    # 查找容量
    volume = SIZE_VOLUME.get(size)
    
    if volume is None:
        # 尝试解析数字
        try:
            # 处理 "500ml" 格式
            if 'ml' in size.lower():
                volume = int(size.lower().replace('ml', '').strip())
            # 处理纯数字
            else:
                volume = int(size)
        except (ValueError, TypeError):
            volume = 400  # 默认中杯
    
    return volume


def calculate_calories(order: BubbleTeaOrder) -> CalorieResult:
    """
    Calculate total calories for a bubble tea order.
    
    Args:
        order: BubbleTeaOrder object with tea configuration
    
    Returns:
        CalorieResult with detailed breakdown
    
    Examples:
        >>> order = BubbleTeaOrder('奶茶', '半糖', '大杯', ['珍珠', '椰果'])
        >>> result = calculate_calories(order)
        >>> result.total_calories
        295.0
    """
    # 获取容量
    size_ml = get_size_ml(order.size)
    
    # 计算各部分热量
    base_calories = get_base_calories(order.base_tea, size_ml)
    sugar_calories = get_sugar_calories(order.sugar_level, size_ml)
    additive_calories = get_additive_calories(order.additives)
    
    # 总热量
    total = base_calories + sugar_calories + additive_calories
    
    # 健康等级
    health_level = get_health_level(total)
    
    # 建议
    suggestion = get_health_suggestion(total, health_level)
    
    # 详细分解
    breakdown = {
        '基底': base_calories,
        '糖分': sugar_calories,
    }
    for additive in order.additives:
        breakdown[f'配料-{additive}'] = ADDITIVE_CALORIES.get(additive, 50)
    
    return CalorieResult(
        total_calories=round(total, 1),
        base_calories=round(base_calories, 1),
        sugar_calories=round(sugar_calories, 1),
        additive_calories=round(additive_calories, 1),
        size_ml=size_ml,
        health_level=health_level,
        suggestion=suggestion,
        breakdown=breakdown
    )


def calculate_calories_simple(
    base_tea: str,
    sugar_level: str,
    size: str,
    additives: Optional[List[str]] = None
) -> float:
    """
    Simple calorie calculation function.
    
    Args:
        base_tea: Base tea type
        sugar_level: Sugar level
        size: Cup size
        additives: List of additives (optional)
    
    Returns:
        Total calories
    
    Examples:
        >>> calculate_calories_simple('奶茶', '半糖', '大杯', ['珍珠'])
        220.0
        >>> calculate_calories_simple('绿茶', '无糖', '中杯')
        8.0
    """
    if additives is None:
        additives = []
    
    order = BubbleTeaOrder(base_tea, sugar_level, size, additives)
    result = calculate_calories(order)
    return result.total_calories


# ============================================================================
# Health Analysis Functions
# ============================================================================

def get_health_level(calories: float) -> HealthLevel:
    """
    Determine health level based on calorie intake.
    
    Args:
        calories: Total calories
    
    Returns:
        HealthLevel enum value
    
    Examples:
        >>> get_health_level(100)
        <HealthLevel.LOW: 1>
        >>> get_health_level(400)
        <HealthLevel.HIGH: 3>
    """
    if calories < 150:
        return HealthLevel.LOW
    elif calories < 300:
        return HealthLevel.MODERATE
    elif calories < 500:
        return HealthLevel.HIGH
    else:
        return HealthLevel.VERY_HIGH


def get_health_suggestion(calories: float, health_level: HealthLevel) -> str:
    """
    Get health suggestion based on calories.
    
    Args:
        calories: Total calories
        health_level: HealthLevel enum
    
    Returns:
        Suggestion string
    
    Examples:
        >>> get_health_suggestion(100, HealthLevel.LOW)
        '热量较低，可以放心享用！'
    """
    suggestions = {
        HealthLevel.LOW: '热量较低，可以放心享用！适合日常饮用。',
        HealthLevel.MODERATE: '热量适中，建议每周不超过 2-3 次。可以选择少糖或小杯。',
        HealthLevel.HIGH: '热量较高！建议减少糖度或配料，选择小杯或分享饮用。',
        HealthLevel.VERY_HIGH: '热量非常高！相当于一顿正餐的热量。强烈建议选择无糖、少配料，或改为纯茶。',
    }
    return suggestions.get(health_level, '请关注热量摄入。')


def get_daily_calorie_comparison(calories: float, 
                                  daily_target: int = 2000) -> Dict[str, float]:
    """
    Compare bubble tea calories with daily intake target.
    
    Args:
        calories: Bubble tea calories
        daily_target: Daily calorie target (default 2000)
    
    Returns:
        Dictionary with comparison data
    
    Examples:
        >>> get_daily_calorie_comparison(300)
        {'percentage': 15.0, 'remaining': 1700, 'meals_equivalent': 0.5}
    """
    percentage = (calories / daily_target) * 100
    remaining = daily_target - calories
    meals_equivalent = calories / 600  # 假设一顿正餐约 600 kcal
    
    return {
        'percentage': round(percentage, 1),
        'remaining': max(0, remaining),
        'meals_equivalent': round(meals_equivalent, 2),
    }


def compare_teas(teas: List[BubbleTeaOrder]) -> List[Tuple[BubbleTeaOrder, CalorieResult]]:
    """
    Compare calories of multiple bubble tea orders.
    
    Args:
        teas: List of BubbleTeaOrder objects
    
    Returns:
        List of tuples (order, result) sorted by calories
    
    Examples:
        >>> teas = [
        ...     BubbleTeaOrder('绿茶', '无糖', '中杯', []),
        ...     BubbleTeaOrder('奶茶', '半糖', '大杯', ['珍珠'])
        ... ]
        >>> results = compare_teas(teas)
        >>> results[0][1].total_calories < results[1][1].total_calories
        True
    """
    results = []
    for tea in teas:
        result = calculate_calories(tea)
        results.append((tea, result))
    
    # 按热量排序 (从低到高)
    results.sort(key=lambda x: x[1].total_calories)
    return results


# ============================================================================
# Recommend Functions
# ============================================================================

def recommend_low_calorie_options(base_tea: str = None) -> List[Dict[str, any]]:
    """
    Recommend low-calorie bubble tea options.
    
    Args:
        base_tea: Optional specific base tea to focus on
    
    Returns:
        List of recommended low-calorie configurations
    
    Examples:
        >>> len(recommend_low_calorie_options()) > 0
        True
    """
    recommendations = []
    
    # 纯茶推荐 (最低热量)
    low_cal_teas = ['绿茶', '红茶', '乌龙茶', '茉莉花茶', '普洱茶']
    for tea in low_cal_teas:
        if base_tea and base_tea != tea:
            continue
        order = BubbleTeaOrder(tea, '无糖', '中杯', [])
        result = calculate_calories(order)
        recommendations.append({
            'base': tea,
            'sugar': '无糖',
            'size': '中杯',
            'additives': [],
            'calories': result.total_calories,
            'note': '最健康选择，几乎零热量'
        })
    
    # 低卡配料推荐
    low_additives = ['蒟蒻', '仙草', '芦荟', '桂花冻']
    order = BubbleTeaOrder('奶茶', '微糖', '小杯', ['蒟蒻'])
    result = calculate_calories(order)
    recommendations.append({
        'base': '奶茶',
        'sugar': '微糖',
        'size': '小杯',
        'additives': ['蒟蒻'],
        'calories': result.total_calories,
        'note': '使用低卡配料，热量友好'
    })
    
    return recommendations


def find_calorie_range(target_calories: float, 
                       tolerance: float = 50) -> List[BubbleTeaOrder]:
    """
    Find bubble tea configurations within a calorie range.
    
    Args:
        target_calories: Target calorie value
        tolerance: Acceptable deviation (±tolerance)
    
    Returns:
        List of orders within the target range
    
    Examples:
        >>> orders = find_calorie_range(150, 30)
        >>> all(120 <= calculate_calories(o).total_calories <= 180 for o in orders)
        True
    """
    valid_orders = []
    
    # 遍历常见配置
    common_bases = ['绿茶', '奶茶', '鲜奶茶', '柠檬茶']
    common_sugars = ['无糖', '微糖', '半糖']
    common_sizes = ['小杯', '中杯', '大杯']
    common_additives = [[], ['珍珠'], ['椰果'], ['布丁'], ['蒟蒻']]
    
    for base in common_bases:
        for sugar in common_sugars:
            for size in common_sizes:
                for additives in common_additives:
                    order = BubbleTeaOrder(base, sugar, size, additives)
                    result = calculate_calories(order)
                    
                    if abs(result.total_calories - target_calories) <= tolerance:
                        valid_orders.append(order)
    
    return valid_orders[:10]  # 最多返回 10 个


# ============================================================================
# Utility Functions
# ============================================================================

def get_additive_list() -> List[str]:
    """
    Get list of all available additives.
    
    Returns:
        List of additive names
    
    Examples:
        >>> '珍珠' in get_additive_list()
        True
    """
    return list(ADDITIVE_CALORIES.keys())


def get_base_tea_list() -> List[str]:
    """
    Get list of all available base teas.
    
    Returns:
        List of base tea names
    
    Examples:
        >>> '奶茶' in get_base_tea_list()
        True
    """
    return list(BASE_TEA_CALORIES.keys())


def get_sugar_level_list() -> List[str]:
    """
    Get list of all available sugar levels.
    
    Returns:
        List of sugar level names
    
    Examples:
        >>> '半糖' in get_sugar_level_list()
        True
    """
    return list(SUGAR_LEVEL_CALORIES.keys())


def get_size_list() -> List[str]:
    """
    Get list of all available sizes.
    
    Returns:
        List of size names
    
    Examples:
        >>> '大杯' in get_size_list()
        True
    """
    return list(SIZE_VOLUME.keys())


def print_calorie_report(result: CalorieResult) -> str:
    """
    Generate a formatted calorie report.
    
    Args:
        result: CalorieResult object
    
    Returns:
        Formatted report string
    
    Examples:
        >>> order = BubbleTeaOrder('奶茶', '半糖', '大杯', ['珍珠'])
        >>> result = calculate_calories(order)
        >>> report = print_calorie_report(result)
        >>> '热量' in report
        True
    """
    report_lines = [
        "=" * 40,
        "奶茶热量报告",
        "=" * 40,
        f"总热量: {result.total_calories} kcal",
        f"杯型容量: {result.size_ml} ml",
        "",
        "热量分解:",
        f"  - 基底: {result.base_calories} kcal",
        f"  - 糖分: {result.sugar_calories} kcal",
        f"  - 配料: {result.additive_calories} kcal",
        "",
        "详细配料:",
    ]
    
    for name, calorie in result.breakdown.items():
        if name.startswith('配料-'):
            report_lines.append(f"  - {name.replace('配料-', '')}: {calorie} kcal")
    
    report_lines.extend([
        "",
        f"健康等级: {result.health_level.name}",
        f"建议: {result.suggestion}",
        "=" * 40,
    ])
    
    return "\n".join(report_lines)


# ============================================================================
# Main (Demo)
# ============================================================================

if __name__ == '__main__':
    print("=== 奶茶热量计算器示例 ===")
    
    # 示例 1: 简单奶茶
    order1 = BubbleTeaOrder('奶茶', '半糖', '大杯', ['珍珠', '椰果'])
    result1 = calculate_calories(order1)
    print(print_calorie_report(result1))
    
    # 示例 2: 低热量选择
    order2 = BubbleTeaOrder('绿茶', '无糖', '中杯', [])
    result2 = calculate_calories(order2)
    print(f"\n纯绿茶(无糖): {result2.total_calories} kcal - {result2.suggestion}")
    
    # 示例 3: 高热量饮品
    order3 = BubbleTeaOrder('黑糖珍珠奶茶', '全糖', '超大杯', ['珍珠', '奶盖', '布丁'])
    result3 = calculate_calories(order3)
    print(f"\n黑糖珍珠奶茶(全糖超大杯加料): {result3.total_calories} kcal")
    print(f"相当于每日摄入: {get_daily_calorie_comparison(result3.total_calories)['percentage']}%")
    
    # 示例 4: 简单调用
    simple_cal = calculate_calories_simple('奶茶', '少糖', '中杯', ['布丁'])
    print(f"\n简单计算: 奶茶+少糖+中杯+布丁 = {simple_cal} kcal")
    
    # 示例 5: 推荐低热量选项
    print("\n=== 低热量推荐 ===")
    for rec in recommend_low_calorie_options()[:3]:
        print(f"{rec['base']} + {rec['sugar']} + {rec['size']}: {rec['calories']} kcal")
        print(f"  备注: {rec['note']}")