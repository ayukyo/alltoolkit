"""
Cooking Utils - 烹饪工具模块

提供烹饪相关的实用功能，包括：
- 温度单位转换（摄氏/华氏）
- 重量单位转换（克/盎司/磅）
- 容积单位转换（毫升/杯/茶匙/汤匙）
- 烘焙时间计算
- 食物保存时间指南
- 烹饪术语词典
- 食材替代建议
- 火候控制指南

零外部依赖，纯 Python 标准库实现。
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum


class TemperatureUnit(Enum):
    """温度单位"""
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


class WeightUnit(Enum):
    """重量单位"""
    GRAM = "gram"
    KILOGRAM = "kilogram"
    OUNCE = "ounce"
    POUND = "pound"
    MILLIGRAM = "milligram"


class VolumeUnit(Enum):
    """容积单位"""
    MILLILITER = "milliliter"
    LITER = "liter"
    CUP = "cup"
    TABLESPOON = "tablespoon"
    TEASPOON = "teaspoon"
    FLUID_OUNCE = "fluid_ounce"
    GALLON = "gallon"
    PINT = "pint"
    QUART = "quart"


# ============ 温度转换 ============

def celsius_to_fahrenheit(celsius: float) -> float:
    """
    摄氏转华氏
    
    Args:
        celsius: 摄氏温度
        
    Returns:
        华氏温度
    """
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    华氏转摄氏
    
    Args:
        fahrenheit: 华氏温度
        
    Returns:
        摄氏温度
    """
    return (fahrenheit - 32) * 5 / 9


def convert_temperature(value: float, from_unit: TemperatureUnit, to_unit: TemperatureUnit) -> float:
    """
    温度单位转换
    
    Args:
        value: 温度值
        from_unit: 原始单位
        to_unit: 目标单位
        
    Returns:
        转换后的温度值
    """
    if from_unit == to_unit:
        return value
    
    if from_unit == TemperatureUnit.CELSIUS and to_unit == TemperatureUnit.FAHRENHEIT:
        return celsius_to_fahrenheit(value)
    elif from_unit == TemperatureUnit.FAHRENHEIT and to_unit == TemperatureUnit.CELSIUS:
        return fahrenheit_to_celsius(value)
    
    return value


def get_common_temperatures() -> Dict[str, Tuple[float, float]]:
    """
    获取常见烹饪温度参考
    
    Returns:
        温度名称到 (摄氏, 华氏) 的映射
    """
    return {
        "室温": (20, 68),
        "低温慢煮": (63, 145),
        "中温烘烤": (175, 350),
        "高温烘烤": (200, 400),
        "煎炸温度": (190, 375),
        "水沸腾": (100, 212),
        "慢炖": (85, 185),
        "温热": (60, 140),
        "冷藏温度": (4, 40),
        "冷冻温度": (-18, 0),
    }


# ============ 重量转换 ============

# 基础换算因子
GRAM_TO_OUNCE = 0.035274
OUNCE_TO_GRAM = 28.3495
POUND_TO_GRAM = 453.592
OUNCE_TO_POUND = 16


def grams_to_ounces(grams: float) -> float:
    """克转盎司"""
    return grams * GRAM_TO_OUNCE


def ounces_to_grams(ounces: float) -> float:
    """盎司转克"""
    return ounces * OUNCE_TO_GRAM


def grams_to_pounds(grams: float) -> float:
    """克转磅"""
    return grams / POUND_TO_GRAM


def pounds_to_grams(pounds: float) -> float:
    """磅转克"""
    return pounds * POUND_TO_GRAM


def kilograms_to_pounds(kilograms: float) -> float:
    """千克转磅"""
    return kilograms * 2.20462


def pounds_to_kilograms(pounds: float) -> float:
    """磅转千克"""
    return pounds / 2.20462


def convert_weight(value: float, from_unit: WeightUnit, to_unit: WeightUnit) -> float:
    """
    重量单位转换
    
    Args:
        value: 重量值
        from_unit: 原始单位
        to_unit: 目标单位
        
    Returns:
        转换后的重量值
    """
    if from_unit == to_unit:
        return value
    
    # 先转换到克作为中间单位
    grams = value
    if from_unit == WeightUnit.KILOGRAM:
        grams = value * 1000
    elif from_unit == WeightUnit.OUNCE:
        grams = ounces_to_grams(value)
    elif from_unit == WeightUnit.POUND:
        grams = pounds_to_grams(value)
    elif from_unit == WeightUnit.MILLIGRAM:
        grams = value / 1000
    
    # 从克转换到目标单位
    if to_unit == WeightUnit.GRAM:
        return grams
    elif to_unit == WeightUnit.KILOGRAM:
        return grams / 1000
    elif to_unit == WeightUnit.OUNCE:
        return grams_to_ounces(grams)
    elif to_unit == WeightUnit.POUND:
        return grams_to_pounds(grams)
    elif to_unit == WeightUnit.MILLIGRAM:
        return grams * 1000
    
    return value


# ============ 容积转换 ============

# 基础换算因子（以毫升为基准）
ML_TO_CUP = 0.00422675
ML_TO_TABLESPOON = 0.067628
ML_TO_TEASPOON = 0.202884
ML_TO_FLUID_OUNCE = 0.033814
ML_TO_GALLON = 0.000264172
ML_TO_PINT = 0.00211338
ML_TO_QUART = 0.00105669

CUP_TO_ML = 240  # 美式杯
TABLESPOON_TO_ML = 15
TEASPOON_TO_ML = 5


def milliliters_to_cups(ml: float) -> float:
    """毫升转杯"""
    return ml * ML_TO_CUP


def cups_to_milliliters(cups: float) -> float:
    """杯转毫升"""
    return cups * CUP_TO_ML


def milliliters_to_tablespoons(ml: float) -> float:
    """毫升转汤匙"""
    return ml * ML_TO_TABLESPOON


def tablespoons_to_milliliters(tbsp: float) -> float:
    """汤匙转毫升"""
    return tbsp * TABLESPOON_TO_ML


def milliliters_to_teaspoons(ml: float) -> float:
    """毫升转茶匙"""
    return ml * ML_TO_TEASPOON


def teaspoons_to_milliliters(tsp: float) -> float:
    """茶匙转毫升"""
    return tsp * TEASPOON_TO_ML


def convert_volume(value: float, from_unit: VolumeUnit, to_unit: VolumeUnit) -> float:
    """
    容积单位转换
    
    Args:
        value: 容积值
        from_unit: 原始单位
        to_unit: 目标单位
        
    Returns:
        转换后的容积值
    """
    if from_unit == to_unit:
        return value
    
    # 先转换到毫升作为中间单位
    ml = value
    if from_unit == VolumeUnit.LITER:
        ml = value * 1000
    elif from_unit == VolumeUnit.CUP:
        ml = cups_to_milliliters(value)
    elif from_unit == VolumeUnit.TABLESPOON:
        ml = tablespoons_to_milliliters(value)
    elif from_unit == VolumeUnit.TEASPOON:
        ml = teaspoons_to_milliliters(value)
    elif from_unit == VolumeUnit.FLUID_OUNCE:
        ml = value / ML_TO_FLUID_OUNCE
    elif from_unit == VolumeUnit.GALLON:
        ml = value / ML_TO_GALLON
    elif from_unit == VolumeUnit.PINT:
        ml = value / ML_TO_PINT
    elif from_unit == VolumeUnit.QUART:
        ml = value / ML_TO_QUART
    
    # 从毫升转换到目标单位
    if to_unit == VolumeUnit.MILLILITER:
        return ml
    elif to_unit == VolumeUnit.LITER:
        return ml / 1000
    elif to_unit == VolumeUnit.CUP:
        return milliliters_to_cups(ml)
    elif to_unit == VolumeUnit.TABLESPOON:
        return milliliters_to_tablespoons(ml)
    elif to_unit == VolumeUnit.TEASPOON:
        return milliliters_to_teaspoons(ml)
    elif to_unit == VolumeUnit.FLUID_OUNCE:
        return ml * ML_TO_FLUID_OUNCE
    elif to_unit == VolumeUnit.GALLON:
        return ml * ML_TO_GALLON
    elif to_unit == VolumeUnit.PINT:
        return ml * ML_TO_PINT
    elif to_unit == VolumeUnit.QUART:
        return ml * ML_TO_QUART
    
    return value


# ============ 烘焙计算 ============

def calculate_baking_time(
    oven_temp: float,
    temp_unit: TemperatureUnit,
    food_type: str,
    weight: Optional[float] = None,
    weight_unit: Optional[WeightUnit] = None
) -> Dict[str, float]:
    """
    计算烘焙时间
    
    Args:
        oven_temp: 烘焙温度
        temp_unit: 温度单位
        food_type: 食物类型
        weight: 食物重量（可选）
        weight_unit: 重量单位（可选）
        
    Returns:
        包含建议时间的字典
    """
    # 标准烘焙温度（摄氏）
    standard_temp_celsius = {
        "蛋糕": 175,
        "面包": 200,
        "饼干": 180,
        "派": 190,
        "烤鸡": 180,
        "烤肉": 170,
        "烤蔬菜": 200,
    }
    
    # 标准烘焙时间（分钟/公斤或固定时间）
    base_times = {
        "蛋糕": (25, 35),  # 固定时间范围
        "面包": (40, 60),
        "饼干": (10, 15),
        "派": (45, 60),
        "烤鸡": (20, 30),  # 每公斤
        "烤肉": (25, 35),  # 每公斤
        "烤蔬菜": (20, 30),
    }
    
    result = {
        "oven_temp_celsius": convert_temperature(oven_temp, temp_unit, TemperatureUnit.CELSIUS),
        "oven_temp_fahrenheit": convert_temperature(oven_temp, temp_unit, TemperatureUnit.FAHRENHEIT),
        "food_type": food_type,
    }
    
    if food_type in base_times:
        min_time, max_time = base_times[food_type]
        
        # 如果是肉类，根据重量调整
        if food_type in ["烤鸡", "烤肉"] and weight is not None:
            weight_grams = convert_weight(weight, weight_unit or WeightUnit.GRAM, WeightUnit.GRAM)
            weight_kg = weight_grams / 1000
            min_time = min_time * weight_kg
            max_time = max_time * weight_kg
        
        result["min_time_minutes"] = min_time
        result["max_time_minutes"] = max_time
        result["recommended_time_minutes"] = (min_time + max_time) / 2
    
    return result


def get_oven_preheat_time(temp: float, temp_unit: TemperatureUnit = TemperatureUnit.CELSIUS) -> int:
    """
    获取烤箱预热时间
    
    Args:
        temp: 目标温度
        temp_unit: 温度单位
        
    Returns:
        预热时间（分钟）
    """
    celsius = convert_temperature(temp, temp_unit, TemperatureUnit.CELSIUS)
    
    if celsius < 150:
        return 5
    elif celsius < 200:
        return 10
    elif celsius < 250:
        return 15
    else:
        return 20


# ============ 食物保存指南 ============

def get_food_storage_info(food: str) -> Dict[str, any]:
    """
    获取食物保存信息
    
    Args:
        food: 食物名称
        
    Returns:
        保存信息字典
    """
    storage_guide = {
        "生肉": {
            "冷藏": "1-2天",
            "冷冻": "3-4个月",
            "温度": "4°C以下",
            "注意事项": "密封保存，避免与其他食物接触"
        },
        "熟肉": {
            "冷藏": "3-4天",
            "冷冻": "2-3个月",
            "温度": "4°C以下",
            "注意事项": "冷却后尽快冷藏"
        },
        "鱼类": {
            "冷藏": "1-2天",
            "冷冻": "3-6个月",
            "温度": "0-4°C",
            "注意事项": "尽快食用，冷冻前去内脏"
        },
        "蔬菜": {
            "冷藏": "3-7天",
            "冷冻": "8-12个月（需预处理）",
            "温度": "4-8°C",
            "注意事项": "避免与水果同放，保持干燥"
        },
        "水果": {
            "冷藏": "5-10天",
            "冷冻": "8-12个月",
            "温度": "4-10°C",
            "注意事项": "部分水果（香蕉、芒果）不宜冷藏"
        },
        "鸡蛋": {
            "冷藏": "3-5周",
            "冷冻": "不推荐",
            "温度": "4°C以下",
            "注意事项": "原包装保存，不要清洗"
        },
        "牛奶": {
            "冷藏": "5-7天",
            "冷冻": "3个月",
            "温度": "4°C以下",
            "注意事项": "开封后尽快饮用"
        },
        "面包": {
            "室温": "3-5天",
            "冷藏": "不推荐（加速变质）",
            "冷冻": "3-6个月",
            "注意事项": "切片冷冻便于取用"
        },
        "米饭": {
            "冷藏": "1-2天",
            "冷冻": "1个月",
            "温度": "4°C以下",
            "注意事项": "冷却后立即冷藏，不要室温放置过久"
        },
    }
    
    return storage_guide.get(food, {"提示": "未找到该食物的保存信息"})


# ============ 食材替代建议 ============

def get_ingredient_substitutes(ingredient: str) -> List[Dict[str, str]]:
    """
    获取食材替代建议
    
    Args:
        ingredient: 原食材名称
        
    Returns:
        替代方案列表
    """
    substitutes = {
        "鸡蛋": [
            {"替代": "亚麻籽粉+水", "比例": "1大勺亚麻籽粉+3大勺水=1个鸡蛋", "适用": "烘焙"},
            {"替代": "香蕉", "比例": "半个香蕉=1个鸡蛋", "适用": "烘焙（会增加香蕉味）"},
            {"替代": "豆腐", "比例": "60克豆腐=1个鸡蛋", "适用": "烘焙"},
        ],
        "黄油": [
            {"替代": "植物油", "比例": "3/4杯油=1杯黄油", "适用": "烘焙"},
            {"替代": "椰子油", "比例": "1:1", "适用": "烘焙"},
            {"替代": "苹果酱", "比例": "半杯苹果酱=半杯黄油", "适用": "烘焙（减少脂肪）"},
        ],
        "牛奶": [
            {"替代": "豆浆", "比例": "1:1", "适用": "烘焙、烹饪"},
            {"替代": "杏仁奶", "比例": "1:1", "适用": "烘焙"},
            {"替代": "椰奶", "比例": "1:1", "适用": "烹饪（增加椰香味）"},
        ],
        "白糖": [
            {"替代": "蜂蜜", "比例": "半杯蜂蜜=1杯糖（需减少其他液体）", "适用": "烘焙"},
            {"替代": "枫糖浆", "比例": "3/4杯枫糖=1杯糖", "适用": "烘焙"},
            {"替代": "红糖", "比例": "1:1", "适用": "烘焙（颜色和口感略有不同）"},
        ],
        "面粉": [
            {"替代": "全麦面粉", "比例": "可部分替代", "适用": "烘焙"},
            {"替代": "杏仁粉", "比例": "适合无面粉食谱", "适用": "烘焙"},
            {"替代": "燕麦粉", "比例": "1:1", "适用": "部分烘焙"},
        ],
        "柠檬汁": [
            {"替代": "醋", "比例": "相同用量", "适用": "烹饪"},
            {"替代": "青柠汁", "比例": "1:1", "适用": "烹饪、烘焙"},
        ],
        "大蒜": [
            {"替代": "蒜粉", "比例": "1/8茶匙蒜粉=1瓣大蒜", "适用": "烹饪"},
            {"替代": "洋葱", "比例": "增加洋葱用量", "适用": "烹饪"},
        ],
        "酱油": [
            {"替代": "鱼露", "比例": "减量使用", "适用": "亚洲烹饪"},
            {"替代": "盐+蘑菇粉", "比例": "根据口味调整", "适用": "烹饪"},
        ],
    }
    
    return substitutes.get(ingredient, [{"提示": "未找到替代建议"}])


# ============ 烹饪术语词典 ============

def get_cooking_term_definition(term: str) -> Dict[str, str]:
    """
    获取烹饪术语定义
    
    Args:
        term: 烹饪术语
        
    Returns:
        术语定义字典
    """
    terms = {
        "焯水": "将食材放入沸水中短时间加热，去除异味、杂质或保持颜色",
        "爆香": "用少量油快速加热香料（如葱、姜、蒜）释放香气",
        "收汁": "加热让汤汁蒸发浓缩，使菜肴味道更浓郁",
        "勾芡": "加入淀粉水使汤汁变稠",
        "腌制": "用盐、糖、醋、香料等浸泡食材使其入味",
        "过油": "将食材在热油中快速滑过，使其定型或增香",
        "煎": "用少量油在锅中加热食材",
        "炒": "用油在高温下快速翻炒食材",
        "炖": "用小火长时间加热使食材入味变软",
        "焖": "加盖小火慢煮，保持食材水分",
        "蒸": "用水蒸气加热食材",
        "煮": "将食材放入水或汤汁中加热",
        "烤": "在烤箱或火上直接加热",
        "炸": "将食材完全浸入热油中加热",
        "涮": "将食材在沸腾的液体中快速烫熟",
        "凉拌": "将煮熟或生鲜食材加入调料拌匀",
        "醒面": "让面团静置松弛，便于后续操作",
        "发酵": "让面团或食材在适宜温度下让微生物作用",
        "打发": "用工具快速搅打使食材蓬松（如打发蛋清）",
        "揉面": "用手反复按压面团使其光滑有弹性",
        "切片": "将食材切成薄片",
        "切丝": "将食材切成细丝",
        "切块": "将食材切成块状",
        "切丁": "将食材切成小立方体",
        "剁碎": "将食材切成极小的碎块",
        "去骨": "从肉类中去除骨头",
        "去皮": "去除食材的外皮",
        "去鳞": "去除鱼类的鳞片",
    }
    
    return {"术语": term, "定义": terms.get(term, "未找到该术语的定义")}


def get_all_cooking_terms() -> Dict[str, str]:
    """获取所有烹饪术语"""
    return {
        "焯水": "将食材放入沸水中短时间加热，去除异味、杂质或保持颜色",
        "爆香": "用少量油快速加热香料释放香气",
        "收汁": "加热让汤汁蒸发浓缩",
        "勾芡": "加入淀粉水使汤汁变稠",
        "腌制": "用调料浸泡食材使其入味",
        "煎": "用少量油加热食材",
        "炒": "高温快速翻炒",
        "炖": "小火长时间加热",
        "焖": "加盖小火慢煮",
        "蒸": "用水蒸气加热",
        "煮": "放入液体中加热",
        "烤": "烤箱或火上加热",
        "炸": "完全浸入热油",
    }


# ============ 火候控制指南 ============

def get_heat_level_guide() -> Dict[str, Dict[str, any]]:
    """
    获取火候控制指南
    
    Returns:
        火候等级到描述的映射
    """
    return {
        "大火": {
            "温度": "200-300°C",
            "适用": "爆炒、煎炸、快速烹制",
            "特点": "快速加热，适合需要快速成型的菜肴",
            "注意事项": "注意翻动防止糊锅"
        },
        "中火": {
            "温度": "150-200°C",
            "适用": "普通炒菜、煎、烧",
            "特点": "均衡加热，适合大多数烹饪",
            "注意事项": "稳定火候，均匀加热"
        },
        "小火": {
            "温度": "80-150°C",
            "适用": "慢炖、煮汤、焖",
            "特点": "缓慢加热，适合需要时间入味的菜肴",
            "注意事项": "保持恒温，避免忽高忽低"
        },
        "微火": {
            "温度": "50-80°C",
            "适用": "保温、慢煮、温热",
            "特点": "极低温度，保持食物温度",
            "注意事项": "适合长时间保温"
        },
    }


def recommend_heat_level(dish_type: str) -> Dict[str, str]:
    """
    根据菜肴类型推荐火候
    
    Args:
        dish_type: 菜肴类型
        
    Returns:
        火候推荐信息
    """
    recommendations = {
        "炒菜": {"火候": "大火或中火", "说明": "快速翻炒保持食材脆嫩"},
        "炖汤": {"火候": "小火", "说明": "长时间慢炖使食材入味"},
        "煎蛋": {"火候": "中火", "说明": "中火煎制口感最佳"},
        "煎肉": {"火候": "先大火后小火", "说明": "大火定型，小火煎透"},
        "煮粥": {"火候": "大火烧开转小火", "说明": "大火快速煮开，小火慢熬"},
        "炒青菜": {"火候": "大火", "说明": "大火快炒保持翠绿和脆嫩"},
        "红烧": {"火候": "中火转小火", "说明": "中火收汁，小火入味"},
        "蒸菜": {"火候": "中火或大火", "说明": "保持蒸气充足"},
    }
    
    return recommendations.get(dish_type, {"提示": "未找到推荐火候"})


# ============ 便捷函数 ============

def quick_convert(value: float, unit_type: str, from_unit: str, to_unit: str) -> float:
    """
    快速单位转换便捷函数
    
    Args:
        value: 原始值
        unit_type: 单位类型 ('temperature', 'weight', 'volume')
        from_unit: 原始单位
        to_unit: 目标单位
        
    Returns:
        转换后的值
    """
    if unit_type == "temperature":
        from_enum = TemperatureUnit(from_unit.lower()) if from_unit.lower() in ["celsius", "fahrenheit"] else TemperatureUnit.CELSIUS
        to_enum = TemperatureUnit(to_unit.lower()) if to_unit.lower() in ["celsius", "fahrenheit"] else TemperatureUnit.CAHRENHEIT
        return convert_temperature(value, from_enum, to_enum)
    elif unit_type == "weight":
        from_enum = WeightUnit(from_unit.lower())
        to_enum = WeightUnit(to_unit.lower())
        return convert_weight(value, from_enum, to_enum)
    elif unit_type == "volume":
        from_enum = VolumeUnit(from_unit.lower())
        to_enum = VolumeUnit(to_unit.lower())
        return convert_volume(value, from_enum, to_enum)
    
    return value


def recipe_scale(original_amount: float, original_servings: int, target_servings: int) -> float:
    """
    按人数缩放食谱用量
    
    Args:
        original_amount: 原始用量
        original_servings: 原始人数
        target_servings: 目标人数
        
    Returns:
        缩放后的用量
    """
    if original_servings <= 0:
        raise ValueError("原始人数必须大于0")
    
    return original_amount * target_servings / original_servings


def calculate_cooking_water_ratio(rice_type: str = "普通米") -> Dict[str, float]:
    """
    计算米和水比例
    
    Args:
        rice_type: 米类型
        
    Returns:
        水米比例信息
    """
    ratios = {
        "普通米": {"比例": 1.5, "说明": "水是米的1.5倍"},
        "糯米": {"比例": 1.2, "说明": "水较少，保持粘性"},
        "糙米": {"比例": 2.0, "说明": "需要更多水"},
        "香米": {"比例": 1.3, "说明": "水稍少保持香气"},
        "寿司米": {"比例": 1.1, "说明": "水少，煮后更粘"},
    }
    
    return ratios.get(rice_type, {"比例": 1.5, "说明": "默认比例"})


if __name__ == '__main__':
    print("=== Cooking Utils Demo ===")
    
    # 温度转换
    print("\n温度转换:")
    print(f"180°C = {celsius_to_fahrenheit(180)}°F")
    print(f"350°F = {fahrenheit_to_celsius(350)}°C")
    
    # 重量转换
    print("\n重量转换:")
    print(f"500克 = {grams_to_ounces(500):.2f}盎司")
    print(f"1磅 = {pounds_to_grams(1):.2f}克")
    
    # 容积转换
    print("\n容积转换:")
    print(f"1杯 = {cups_to_milliliters(1)}毫升")
    print(f"100毫升 = {milliliters_to_teaspoons(100):.2f}茶匙")
    
    # 食物保存
    print("\n食物保存指南:")
    print(get_food_storage_info("鸡蛋"))
    
    # 食材替代
    print("\n食材替代:")
    for sub in get_ingredient_substitutes("鸡蛋"):
        print(f"  {sub}")
    
    # 烹饪术语
    print("\n烹饪术语:")
    print(get_cooking_term_definition("焯水"))
    
    # 火候推荐
    print("\n火候推荐:")
    print(recommend_heat_level("炒菜"))