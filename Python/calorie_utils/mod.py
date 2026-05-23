"""
Calorie Utilities - 卡路里/热量计算工具

提供完整的热量计算功能：
- 基础代谢率 (BMR) 计算：Mifflin-St Jeor, Harris-Benedict, Katch-McArdle
- 每日总能量消耗 (TDEE) 计算
- 食物热量数据库和计算
- 运动消耗估算 (MET值方法)
- 体重目标计划
- 宏量营养素分配

零依赖，仅使用Python标准库。
"""

from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum
import math


class Gender(Enum):
    """性别枚举"""
    MALE = "male"
    FEMALE = "female"


class ActivityLevel(Enum):
    """活动水平枚举"""
    SEDENTARY = "sedentary"          # 久坐不动
    LIGHT = "light"                  # 轻度活动
    MODERATE = "moderate"             # 中度活动
    ACTIVE = "active"                # 活跃
    VERY_ACTIVE = "very_active"      # 非常活跃


class Goal(Enum):
    """目标枚举"""
    LOSE = "lose"           # 减重
    MAINTAIN = "maintain"   # 维持
    GAIN = "gain"           # 增重


# 活动系数映射
ACTIVITY_MULTIPLIERS = {
    ActivityLevel.SEDENTARY: 1.2,      # 久坐不动（几乎不运动）
    ActivityLevel.LIGHT: 1.375,        # 轻度活动（每周1-3天运动）
    ActivityLevel.MODERATE: 1.55,      # 中度活动（每周3-5天运动）
    ActivityLevel.ACTIVE: 1.725,       # 活跃（每周6-7天运动）
    ActivityLevel.VERY_ACTIVE: 1.9,    # 非常活跃（体力劳动或每天两次训练）
}

# 宏量营养素热量系数（每克热量）
MACRO_CALORIES = {
    "protein": 4,      # 蛋白质：4 kcal/g
    "carbs": 4,        # 碳水化合物：4 kcal/g
    "fat": 9,          # 脂肪：9 kcal/g
    "alcohol": 7,      # 酒精：7 kcal/g
    "fiber": 2,        # 膳食纤维：2 kcal/g（可发酵部分）
}

# 常见食物热量数据库（每100克）
FOOD_DATABASE: Dict[str, Dict[str, Any]] = {
    # 主食类
    "rice_white_cooked": {"name": "白米饭（熟）", "calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
    "rice_brown_cooked": {"name": "糙米饭（熟）", "calories": 112, "protein": 2.6, "carbs": 24, "fat": 0.9},
    "noodles_cooked": {"name": "面条（熟）", "calories": 138, "protein": 4.5, "carbs": 25, "fat": 2.0},
    "bread_white": {"name": "白面包", "calories": 265, "protein": 9, "carbs": 49, "fat": 3.2},
    "bread_whole_wheat": {"name": "全麦面包", "calories": 247, "protein": 13, "carbs": 41, "fat": 3.4},
    "oatmeal_cooked": {"name": "燕麦粥（熟）", "calories": 68, "protein": 2.4, "carbs": 12, "fat": 1.4},
    
    # 肉类
    "chicken_breast": {"name": "鸡胸肉", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
    "chicken_thigh": {"name": "鸡腿肉", "calories": 209, "protein": 26, "carbs": 0, "fat": 11},
    "beef_lean": {"name": "瘦牛肉", "calories": 250, "protein": 26, "carbs": 0, "fat": 15},
    "pork_lean": {"name": "瘦猪肉", "calories": 242, "protein": 27, "carbs": 0, "fat": 14},
    "fish_salmon": {"name": "三文鱼", "calories": 208, "protein": 20, "carbs": 0, "fat": 13},
    "fish_cod": {"name": "鳕鱼", "calories": 82, "protein": 18, "carbs": 0, "fat": 0.7},
    "shrimp": {"name": "虾", "calories": 99, "protein": 24, "carbs": 0.2, "fat": 0.3},
    "egg_whole": {"name": "鸡蛋", "calories": 155, "protein": 13, "carbs": 1.1, "fat": 11},
    "egg_white": {"name": "蛋白", "calories": 52, "protein": 11, "carbs": 0.7, "fat": 0.2},
    
    # 蔬菜类
    "broccoli": {"name": "西兰花", "calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4},
    "spinach": {"name": "菠菜", "calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
    "tomato": {"name": "番茄", "calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2},
    "carrot": {"name": "胡萝卜", "calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2},
    "potato": {"name": "土豆", "calories": 77, "protein": 2, "carbs": 17, "fat": 0.1},
    "cucumber": {"name": "黄瓜", "calories": 16, "protein": 0.7, "carbs": 3.6, "fat": 0.1},
    "lettuce": {"name": "生菜", "calories": 15, "protein": 1.4, "carbs": 2.9, "fat": 0.2},
    
    # 水果类
    "apple": {"name": "苹果", "calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2},
    "banana": {"name": "香蕉", "calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3},
    "orange": {"name": "橙子", "calories": 47, "protein": 0.9, "carbs": 12, "fat": 0.1},
    "grape": {"name": "葡萄", "calories": 69, "protein": 0.7, "carbs": 18, "fat": 0.2},
    "watermelon": {"name": "西瓜", "calories": 30, "protein": 0.6, "carbs": 8, "fat": 0.2},
    "strawberry": {"name": "草莓", "calories": 33, "protein": 0.7, "carbs": 8, "fat": 0.3},
    
    # 乳制品
    "milk_whole": {"name": "全脂牛奶", "calories": 61, "protein": 3.2, "carbs": 4.8, "fat": 3.3},
    "milk_skim": {"name": "脱脂牛奶", "calories": 34, "protein": 3.4, "carbs": 5, "fat": 0.1},
    "yogurt_plain": {"name": "原味酸奶", "calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.7},
    "cheese_cheddar": {"name": "切达奶酪", "calories": 403, "protein": 25, "carbs": 1.3, "fat": 33},
    
    # 坚果和种子
    "almond": {"name": "杏仁", "calories": 579, "protein": 21, "carbs": 22, "fat": 50},
    "walnut": {"name": "核桃", "calories": 654, "protein": 15, "carbs": 14, "fat": 65},
    "peanut": {"name": "花生", "calories": 567, "protein": 25, "carbs": 16, "fat": 49},
    "sunflower_seed": {"name": "葵花籽", "calories": 584, "protein": 21, "carbs": 20, "fat": 51},
    
    # 油脂类
    "olive_oil": {"name": "橄榄油", "calories": 884, "protein": 0, "carbs": 0, "fat": 100},
    "butter": {"name": "黄油", "calories": 717, "protein": 0.9, "carbs": 0.1, "fat": 81},
    
    # 饮品
    "coffee_black": {"name": "黑咖啡", "calories": 2, "protein": 0.3, "carbs": 0, "fat": 0},
    "tea_green": {"name": "绿茶", "calories": 0, "protein": 0, "carbs": 0, "fat": 0},
    "cola": {"name": "可乐", "calories": 42, "protein": 0, "carbs": 11, "fat": 0},
    "orange_juice": {"name": "橙汁", "calories": 45, "protein": 0.7, "carbs": 10, "fat": 0.2},
    
    # 豆类
    "tofu": {"name": "豆腐", "calories": 76, "protein": 8, "carbs": 2, "fat": 4.8},
    "soybean": {"name": "黄豆", "calories": 446, "protein": 36, "carbs": 30, "fat": 20},
    "black_bean": {"name": "黑豆", "calories": 339, "protein": 21, "carbs": 63, "fat": 0.9},
    
    # 快餐/加工食品
    "pizza_cheese": {"name": "芝士披萨", "calories": 266, "protein": 11, "carbs": 33, "fat": 10},
    "hamburger": {"name": "汉堡包", "calories": 295, "protein": 17, "carbs": 24, "fat": 14},
    "french_fries": {"name": "薯条", "calories": 312, "protein": 3.4, "carbs": 41, "fat": 15},
    "ice_cream": {"name": "冰淇淋", "calories": 207, "protein": 3.5, "carbs": 24, "fat": 11},
    "chocolate": {"name": "巧克力", "calories": 546, "protein": 5, "carbs": 60, "fat": 31},
}

# MET值数据库（代谢当量）
MET_DATABASE: Dict[str, Dict[str, Any]] = {
    # 日常生活
    "sleeping": {"name": "睡眠", "met": 0.9},
    "watching_tv": {"name": "看电视", "met": 1.0},
    "sitting": {"name": "静坐", "met": 1.3},
    "standing": {"name": "站立", "met": 1.8},
    "walking_slow": {"name": "慢走（散步）", "met": 2.0},
    "walking_normal": {"name": "正常步行", "met": 3.0},
    "walking_brisk": {"name": "快走", "met": 4.0},
    "walking_upstairs": {"name": "上楼梯", "met": 8.0},
    
    # 跑步
    "running_5kmh": {"name": "跑步（5 km/h）", "met": 5.0},
    "running_6kmh": {"name": "跑步（6 km/h）", "met": 6.0},
    "running_8kmh": {"name": "跑步（8 km/h）", "met": 8.0},
    "running_10kmh": {"name": "跑步（10 km/h）", "met": 10.0},
    "running_12kmh": {"name": "跑步（12 km/h）", "met": 12.0},
    "running_marathon": {"name": "马拉松配速", "met": 13.0},
    "sprinting": {"name": "冲刺跑", "met": 16.0},
    
    # 骑行
    "cycling_leisure": {"name": "休闲骑行", "met": 4.0},
    "cycling_moderate": {"name": "中速骑行", "met": 6.0},
    "cycling_vigorous": {"name": "剧烈骑行", "met": 10.0},
    "cycling_racing": {"name": "竞速骑行", "met": 16.0},
    
    # 游泳
    "swimming_leisure": {"name": "休闲游泳", "met": 6.0},
    "swimming_freestyle_moderate": {"name": "自由泳（中等）", "met": 7.0},
    "swimming_freestyle_vigorous": {"name": "自由泳（剧烈）", "met": 10.0},
    "swimming_breaststroke": {"name": "蛙泳", "met": 8.0},
    "swimming_butterfly": {"name": "蝶泳", "met": 11.0},
    
    # 健身
    "yoga": {"name": "瑜伽", "met": 3.0},
    "pilates": {"name": "普拉提", "met": 3.0},
    "weight_lifting_light": {"name": "力量训练（轻）", "met": 3.5},
    "weight_lifting_moderate": {"name": "力量训练（中）", "met": 5.0},
    "weight_lifting_vigorous": {"name": "力量训练（剧烈）", "met": 6.0},
    "calisthenics_moderate": {"name": "徒手训练（中）", "met": 4.0},
    "calisthenics_vigorous": {"name": "徒手训练（剧烈）", "met": 8.0},
    "hiit": {"name": "HIIT训练", "met": 8.0},
    "crossfit": {"name": "CrossFit", "met": 9.0},
    
    # 球类运动
    "basketball": {"name": "篮球", "met": 6.5},
    "soccer": {"name": "足球", "met": 7.0},
    "tennis": {"name": "网球", "met": 7.0},
    "badminton": {"name": "羽毛球", "met": 5.5},
    "table_tennis": {"name": "乒乓球", "met": 4.0},
    "volleyball": {"name": "排球", "met": 4.0},
    "golf": {"name": "高尔夫", "met": 4.5},
    "squash": {"name": "壁球", "met": 12.0},
    
    # 有氧运动
    "aerobics_low": {"name": "有氧操（低强度）", "met": 5.0},
    "aerobics_high": {"name": "有氧操（高强度）", "met": 8.0},
    "dancing": {"name": "跳舞", "met": 5.0},
    "jump_rope_slow": {"name": "跳绳（慢）", "met": 8.0},
    "jump_rope_fast": {"name": "跳绳（快）", "met": 12.0},
    "rowing_moderate": {"name": "划船机（中）", "met": 6.0},
    "rowing_vigorous": {"name": "划船机（剧烈）", "met": 8.5},
    "elliptical": {"name": "椭圆机", "met": 5.0},
    
    # 户外运动
    "hiking": {"name": "徒步", "met": 6.0},
    "rock_climbing": {"name": "攀岩", "met": 8.0},
    "skiing": {"name": "滑雪", "met": 7.0},
    "snowboarding": {"name": "单板滑雪", "met": 6.0},
    "skating": {"name": "滑冰", "met": 7.0},
    
    # 家务劳动
    "cleaning_house": {"name": "打扫卫生", "met": 3.5},
    "gardening": {"name": "园艺", "met": 4.0},
    "mowing_lawn": {"name": "割草", "met": 5.5},
    "cooking": {"name": "做饭", "met": 2.0},
    "shopping": {"name": "购物", "met": 2.5},
}


@dataclass
class NutritionInfo:
    """营养信息数据类"""
    calories: float       # 卡路里 (kcal)
    protein: float = 0    # 蛋白质 (g)
    carbs: float = 0       # 碳水化合物 (g)
    fat: float = 0         # 脂肪 (g)
    fiber: float = 0       # 膳食纤维 (g)
    alcohol: float = 0     # 酒精 (g)
    
    def __add__(self, other: "NutritionInfo") -> "NutritionInfo":
        """累加营养信息"""
        return NutritionInfo(
            calories=self.calories + other.calories,
            protein=self.protein + other.protein,
            carbs=self.carbs + other.carbs,
            fat=self.fat + other.fat,
            fiber=self.fiber + other.fiber,
            alcohol=self.alcohol + other.alcohol,
        )
    
    def __mul__(self, multiplier: float) -> "NutritionInfo":
        """缩放营养信息"""
        return NutritionInfo(
            calories=self.calories * multiplier,
            protein=self.protein * multiplier,
            carbs=self.carbs * multiplier,
            fat=self.fat * multiplier,
            fiber=self.fiber * multiplier,
            alcohol=self.alcohol * multiplier,
        )
    
    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return {
            "calories": round(self.calories, 1),
            "protein": round(self.protein, 1),
            "carbs": round(self.carbs, 1),
            "fat": round(self.fat, 1),
            "fiber": round(self.fiber, 1),
            "alcohol": round(self.alcohol, 1),
        }


@dataclass
class WeightGoalPlan:
    """体重目标计划"""
    target_weight: float         # 目标体重 (kg)
    weight_change: float        # 体重变化 (kg, 负数表示减重)
    daily_calorie_target: int   # 每日热量目标 (kcal)
    weeks_to_achieve: int       # 达成所需周数
    daily_deficit: int          # 每日热量差 (kcal)
    macro_split: Dict[str, int] # 宏量营养素分配 (g)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "target_weight": round(self.target_weight, 1),
            "weight_change": round(self.weight_change, 2),
            "daily_calorie_target": self.daily_calorie_target,
            "weeks_to_achieve": self.weeks_to_achieve,
            "daily_deficit": self.daily_deficit,
            "macro_split": self.macro_split,
        }


# ==================== BMR计算函数 ====================

def calculate_bmr_mifflin(weight: float, height: float, age: int, gender: Gender) -> float:
    """
    使用Mifflin-St Jeor公式计算基础代谢率 (BMR)
    
    公式：
    男性: BMR = 10 × 体重(kg) + 6.25 × 身高(cm) - 5 × 年龄 + 5
    女性: BMR = 10 × 体重(kg) + 6.25 × 身高(cm) - 5 × 年龄 - 161
    
    Mifflin-St Jeor公式被认为是目前最准确的BMR计算公式。
    
    Args:
        weight: 体重 (kg)
        height: 身高 (cm)
        age: 年龄 (年)
        gender: 性别 (Gender.MALE 或 Gender.FEMALE)
    
    Returns:
        基础代谢率 (kcal/天)
    
    Raises:
        ValueError: 参数无效
    
    Examples:
        >>> calculate_bmr_mifflin(70, 175, 30, Gender.MALE)
        1673.75
        >>> calculate_bmr_mifflin(55, 165, 25, Gender.FEMALE)
        1293.75
    """
    if weight <= 0:
        raise ValueError("体重必须大于0")
    if height <= 0:
        raise ValueError("身高必须大于0")
    if age <= 0:
        raise ValueError("年龄必须大于0")
    
    base = 10 * weight + 6.25 * height - 5 * age
    
    if gender == Gender.MALE:
        return base + 5
    else:
        return base - 161


def calculate_bmr_harris_benedict(weight: float, height: float, age: int, gender: Gender) -> float:
    """
    使用Harris-Benedict公式计算基础代谢率 (BMR)
    
    公式（1984年修订版）：
    男性: BMR = 88.362 + (13.397 × 体重) + (4.799 × 身高) - (5.677 × 年龄)
    女性: BMR = 447.593 + (9.247 × 体重) + (3.098 × 身高) - (4.330 × 年龄)
    
    Harris-Benedict公式是历史最悠久的BMR计算公式，略微高估现代人的代谢。
    
    Args:
        weight: 体重 (kg)
        height: 身高 (cm)
        age: 年龄 (年)
        gender: 性别
    
    Returns:
        基础代谢率 (kcal/天)
    
    Examples:
        >>> calculate_bmr_harris_benedict(70, 175, 30, Gender.MALE)
        1721.89
    """
    if weight <= 0:
        raise ValueError("体重必须大于0")
    if height <= 0:
        raise ValueError("身高必须大于0")
    if age <= 0:
        raise ValueError("年龄必须大于0")
    
    if gender == Gender.MALE:
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)


def calculate_bmr_katch_mcardle(lean_body_mass: float) -> float:
    """
    使用Katch-McArdle公式计算基础代谢率 (BMR)
    
    公式：BMR = 370 + (21.6 × 瘦体重)
    
    Katch-McArdle公式基于瘦体重计算，适合体脂率已知的情况。
    对于肌肉量较高的人群更准确。
    
    Args:
        lean_body_mass: 瘦体重 (kg)，即体重 × (1 - 体脂率)
    
    Returns:
        基础代谢率 (kcal/天)
    
    Examples:
        >>> calculate_bmr_katch_mcardle(56)  # 70kg体重，20%体脂
        1579.6
    """
    if lean_body_mass <= 0:
        raise ValueError("瘦体重必须大于0")
    
    return 370 + (21.6 * lean_body_mass)


def calculate_bmr_from_body_fat(weight: float, body_fat_percent: float, gender: Gender) -> float:
    """
    根据体重和体脂率计算BMR（使用Katch-McArdle公式）
    
    Args:
        weight: 体重 (kg)
        body_fat_percent: 体脂率 (百分比，如20表示20%)
        gender: 性别（未使用，但保留参数兼容性）
    
    Returns:
        基础代谢率 (kcal/天)
    
    Examples:
        >>> calculate_bmr_from_body_fat(70, 20, Gender.MALE)  # 70kg, 20%体脂
        1579.6
    """
    if weight <= 0:
        raise ValueError("体重必须大于0")
    if body_fat_percent < 0 or body_fat_percent > 100:
        raise ValueError("体脂率必须在0-100之间")
    
    lean_body_mass = weight * (1 - body_fat_percent / 100)
    return calculate_bmr_katch_mcardle(lean_body_mass)


# ==================== TDEE计算函数 ====================

def calculate_tdee(bmr: float, activity_level: ActivityLevel) -> float:
    """
    计算每日总能量消耗 (TDEE)
    
    TDEE = BMR × 活动系数
    
    活动系数：
    - 久坐不动: 1.2
    - 轻度活动: 1.375
    - 中度活动: 1.55
    - 活跃: 1.725
    - 非常活跃: 1.9
    
    Args:
        bmr: 基础代谢率 (kcal/天)
        activity_level: 活动水平
    
    Returns:
        每日总能量消耗 (kcal/天)
    
    Examples:
        >>> calculate_tdee(1700, ActivityLevel.MODERATE)
        2635.0
    """
    if bmr <= 0:
        raise ValueError("BMR必须大于0")
    
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level)
    if multiplier is None:
        raise ValueError(f"无效的活动水平: {activity_level}")
    
    return bmr * multiplier


def calculate_tdee_full(weight: float, height: float, age: int, gender: Gender,
                         activity_level: ActivityLevel,
                         method: str = "mifflin") -> Dict[str, float]:
    """
    完整的TDEE计算，返回BMR和TDEE
    
    Args:
        weight: 体重 (kg)
        height: 身高 (cm)
        age: 年龄 (年)
        gender: 性别
        activity_level: 活动水平
        method: BMR计算方法 ("mifflin" 或 "harris")
    
    Returns:
        包含BMR和TDEE的字典
    
    Examples:
        >>> result = calculate_tdee_full(70, 175, 30, Gender.MALE, ActivityLevel.MODERATE)
        >>> result["bmr"] > 0
        True
    """
    if method == "mifflin":
        bmr = calculate_bmr_mifflin(weight, height, age, gender)
    elif method == "harris":
        bmr = calculate_bmr_harris_benedict(weight, height, age, gender)
    else:
        raise ValueError(f"无效的计算方法: {method}")
    
    tdee = calculate_tdee(bmr, activity_level)
    
    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "activity_multiplier": ACTIVITY_MULTIPLIERS[activity_level],
        "activity_level": activity_level.value,
        "method": method,
    }


# ==================== 食物热量函数 ====================

def get_food_info(food_key: str) -> Optional[Dict[str, Any]]:
    """
    获取食物信息
    
    Args:
        food_key: 食物键名
    
    Returns:
        食物信息字典，不存在返回None
    
    Examples:
        >>> info = get_food_info("rice_white_cooked")
        >>> info["name"]
        '白米饭（熟）'
    """
    return FOOD_DATABASE.get(food_key)


def calculate_food_calories(food_key: str, grams: float) -> Optional[NutritionInfo]:
    """
    计算食物热量
    
    Args:
        food_key: 食物键名
        grams: 食物重量 (克)
    
    Returns:
        NutritionInfo对象，食物不存在返回None
    
    Examples:
        >>> info = calculate_food_calories("rice_white_cooked", 200)
        >>> info.calories
        260.0
    """
    food = FOOD_DATABASE.get(food_key)
    if food is None:
        return None
    
    multiplier = grams / 100
    
    return NutritionInfo(
        calories=food["calories"] * multiplier,
        protein=food.get("protein", 0) * multiplier,
        carbs=food.get("carbs", 0) * multiplier,
        fat=food.get("fat", 0) * multiplier,
    )


def calculate_meal_calories(ingredients: List[Tuple[str, float]]) -> NutritionInfo:
    """
    计算一餐的总热量
    
    Args:
        ingredients: 食材列表，每个元素为 (食物键名, 克数)
    
    Returns:
        NutritionInfo对象，包含总营养信息
    
    Examples:
        >>> meal = calculate_meal_calories([
        ...     ("rice_white_cooked", 200),
        ...     ("chicken_breast", 150),
        ...     ("broccoli", 100)
        ... ])
        >>> meal.calories
        487.5
    """
    total = NutritionInfo(calories=0)
    unknown_foods = []
    
    for food_key, grams in ingredients:
        info = calculate_food_calories(food_key, grams)
        if info:
            total = total + info
        else:
            unknown_foods.append(food_key)
    
    return total


def search_food(keyword: str) -> List[Dict[str, Any]]:
    """
    搜索食物
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        匹配的食物列表
    
    Examples:
        >>> results = search_food("chicken")
        >>> len(results) > 0
        True
    """
    keyword_lower = keyword.lower()
    results = []
    
    for key, info in FOOD_DATABASE.items():
        # 搜索键名和中文名
        if keyword_lower in key.lower() or keyword_lower in info.get("name", "").lower():
            results.append({"key": key, **info})
    
    return results


def list_all_foods() -> Dict[str, Dict[str, Any]]:
    """
    列出所有食物
    
    Returns:
        完整食物数据库
    """
    return FOOD_DATABASE.copy()


# ==================== 运动消耗函数 ====================

def get_exercise_info(exercise_key: str) -> Optional[Dict[str, Any]]:
    """
    获取运动信息
    
    Args:
        exercise_key: 运动键名
    
    Returns:
        运动信息字典，不存在返回None
    """
    return MET_DATABASE.get(exercise_key)


def calculate_exercise_calories(exercise_key: str, weight: float, duration_minutes: float) -> float:
    """
    计算运动消耗热量
    
    公式：消耗热量 (kcal) = MET × 体重 (kg) × 时长 (小时)
    
    Args:
        exercise_key: 运动键名
        weight: 体重 (kg)
        duration_minutes: 运动时长 (分钟)
    
    Returns:
        消耗热量 (kcal)
    
    Raises:
        ValueError: 运动不存在或参数无效
    
    Examples:
        >>> calories = calculate_exercise_calories("running_8kmh", 70, 30)
        >>> calories > 0
        True
    """
    if weight <= 0:
        raise ValueError("体重必须大于0")
    if duration_minutes <= 0:
        raise ValueError("运动时长必须大于0")
    
    exercise = MET_DATABASE.get(exercise_key)
    if exercise is None:
        raise ValueError(f"未找到运动: {exercise_key}")
    
    met = exercise["met"]
    duration_hours = duration_minutes / 60
    
    return met * weight * duration_hours


def calculate_custom_exercise_calories(met: float, weight: float, duration_minutes: float) -> float:
    """
    计算自定义运动消耗热量
    
    Args:
        met: MET值
        weight: 体重 (kg)
        duration_minutes: 运动时长 (分钟)
    
    Returns:
        消耗热量 (kcal)
    
    Examples:
        >>> calories = calculate_custom_exercise_calories(8.0, 70, 30)
        >>> calories
        280.0
    """
    if met <= 0:
        raise ValueError("MET值必须大于0")
    if weight <= 0:
        raise ValueError("体重必须大于0")
    if duration_minutes <= 0:
        raise ValueError("运动时长必须大于0")
    
    duration_hours = duration_minutes / 60
    return met * weight * duration_hours


def search_exercise(keyword: str) -> List[Dict[str, Any]]:
    """
    搜索运动
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        匹配的运动列表
    """
    keyword_lower = keyword.lower()
    results = []
    
    for key, info in MET_DATABASE.items():
        if keyword_lower in key.lower() or keyword_lower in info.get("name", "").lower():
            results.append({"key": key, **info})
    
    return results


def list_all_exercises() -> Dict[str, Dict[str, Any]]:
    """
    列出所有运动
    
    Returns:
        完整运动数据库
    """
    return MET_DATABASE.copy()


# ==================== 体重目标函数 ====================

def calculate_weight_goal_plan(
    current_weight: float,
    target_weight: float,
    tdee: float,
    weight_change_rate: float = 0.5,
    activity_level: Optional[ActivityLevel] = None
) -> WeightGoalPlan:
    """
    计算体重目标计划
    
    Args:
        current_weight: 当前体重 (kg)
        target_weight: 目标体重 (kg)
        tdee: 每日总能量消耗 (kcal)
        weight_change_rate: 每周体重变化目标 (kg/周)，默认0.5kg/周
                          减重时推荐0.5-1kg/周
                          增重时推荐0.25-0.5kg/周
        activity_level: 活动水平（可选，用于调整宏量营养素分配）
    
    Returns:
        WeightGoalPlan对象
    
    Examples:
        >>> plan = calculate_weight_goal_plan(80, 75, 2500)
        >>> plan.weeks_to_achieve
        10
    """
    if current_weight <= 0:
        raise ValueError("当前体重必须大于0")
    if target_weight <= 0:
        raise ValueError("目标体重必须大于0")
    if tdee <= 0:
        raise ValueError("TDEE必须大于0")
    
    weight_change = target_weight - current_weight
    
    # 计算每日热量差
    # 1kg脂肪约等于7700kcal
    CALORIES_PER_KG = 7700
    
    if weight_change > 0:
        # 增重
        weekly_change = min(weight_change_rate, 0.5)  # 限制增重速度
        daily_surplus = (weekly_change * CALORIES_PER_KG) / 7
        daily_target = int(tdee + daily_surplus)
        daily_deficit = int(daily_surplus)
    else:
        # 减重
        weekly_change = min(weight_change_rate, 1.0)  # 限制减重速度
        daily_deficit = (weekly_change * CALORIES_PER_KG) / 7
        daily_target = int(tdee - daily_deficit)
        daily_deficit = int(-daily_deficit)  # 负数表示热量缺口
    
    # 计算达成周数
    total_change = abs(weight_change)
    weeks = int(math.ceil(total_change / weekly_change)) if weekly_change > 0 else 0
    
    # 计算宏量营养素分配
    macro_split = calculate_macro_split(daily_target, goal=Goal.GAIN if weight_change > 0 else Goal.LOSE)
    
    return WeightGoalPlan(
        target_weight=target_weight,
        weight_change=weight_change,
        daily_calorie_target=daily_target,
        weeks_to_achieve=weeks,
        daily_deficit=daily_deficit,
        macro_split=macro_split,
    )


def calculate_weight_loss_calories(tdee: float, loss_rate: float = 0.5) -> Dict[str, Any]:
    """
    计算减重所需的热量摄入
    
    Args:
        tdee: 每日总能量消耗 (kcal)
        loss_rate: 每周减重目标 (kg/周)，推荐0.5-1.0
    
    Returns:
        包含热量目标和建议的字典
    
    Examples:
        >>> result = calculate_weight_loss_calories(2500, 0.5)
        >>> result["daily_target"]
        1950
    """
    if tdee <= 0:
        raise ValueError("TDEE必须大于0")
    if loss_rate <= 0 or loss_rate > 1.5:
        raise ValueError("减重速度应在0-1.5kg/周之间")
    
    CALORIES_PER_KG = 7700
    daily_deficit = (loss_rate * CALORIES_PER_KG) / 7
    daily_target = int(tdee - daily_deficit)
    
    # 确保不低于基础安全热量
    MIN_CALORIES = {
        "male": 1500,
        "female": 1200,
    }
    
    return {
        "daily_target": daily_target,
        "daily_deficit": int(daily_deficit),
        "weekly_loss": loss_rate,
        "calories_per_kg": CALORIES_PER_KG,
        "safe_minimum_male": MIN_CALORIES["male"],
        "safe_minimum_female": MIN_CALORIES["female"],
        "warning": None if daily_target >= MIN_CALORIES["female"] else "热量摄入过低，请咨询医生",
    }


def calculate_weight_gain_calories(tdee: float, gain_rate: float = 0.25) -> Dict[str, Any]:
    """
    计算增重所需的热量摄入
    
    Args:
        tdee: 每日总能量消耗 (kcal)
        gain_rate: 每周增重目标 (kg/周)，推荐0.25-0.5
    
    Returns:
        包含热量目标和建议的字典
    
    Examples:
        >>> result = calculate_weight_gain_calories(2500, 0.25)
        >>> result["daily_target"]
        2775
    """
    if tdee <= 0:
        raise ValueError("TDEE必须大于0")
    if gain_rate <= 0 or gain_rate > 1.0:
        raise ValueError("增重速度应在0-1.0kg/周之间")
    
    CALORIES_PER_KG = 7700
    daily_surplus = (gain_rate * CALORIES_PER_KG) / 7
    daily_target = int(tdee + daily_surplus)
    
    return {
        "daily_target": daily_target,
        "daily_surplus": int(daily_surplus),
        "weekly_gain": gain_rate,
        "calories_per_kg": CALORIES_PER_KG,
    }


# ==================== 宏量营养素函数 ====================

def calculate_macro_split(total_calories: float, 
                          goal: Goal = Goal.MAINTAIN,
                          protein_ratio: Optional[float] = None,
                          fat_ratio: Optional[float] = None) -> Dict[str, int]:
    """
    计算宏量营养素分配
    
    Args:
        total_calories: 总热量 (kcal)
        goal: 目标 (减重/维持/增重)
        protein_ratio: 自定义蛋白质比例 (可选)
        fat_ratio: 自定义脂肪比例 (可选)
    
    Returns:
        宏量营养素分配字典 {"protein": g, "carbs": g, "fat": g}
    
    Examples:
        >>> macros = calculate_macro_split(2000, Goal.MAINTAIN)
        >>> macros["protein"]
        150
    """
    if total_calories <= 0:
        raise ValueError("总热量必须大于0")
    
    # 默认比例分配（基于目标）
    if goal == Goal.LOSE:
        # 减重：高蛋白，中脂肪，低碳水
        protein_pct = 0.30
        fat_pct = 0.30
    elif goal == Goal.GAIN:
        # 增重：中蛋白，中脂肪，高碳水
        protein_pct = 0.20
        fat_pct = 0.25
    else:
        # 维持：标准比例
        protein_pct = 0.25
        fat_pct = 0.30
    
    # 应用自定义比例
    if protein_ratio is not None:
        protein_pct = protein_ratio
    if fat_ratio is not None:
        fat_pct = fat_ratio
    
    carbs_pct = 1.0 - protein_pct - fat_pct
    if carbs_pct < 0:
        carbs_pct = 0
    
    # 计算克数
    protein_g = int((total_calories * protein_pct) / MACRO_CALORIES["protein"])
    fat_g = int((total_calories * fat_pct) / MACRO_CALORIES["fat"])
    carbs_g = int((total_calories * carbs_pct) / MACRO_CALORIES["carbs"])
    
    return {
        "protein": protein_g,
        "carbs": carbs_g,
        "fat": fat_g,
        "protein_pct": round(protein_pct * 100, 1),
        "carbs_pct": round(carbs_pct * 100, 1),
        "fat_pct": round(fat_pct * 100, 1),
    }


def calculate_macro_calories(protein: float, carbs: float, fat: float,
                             alcohol: float = 0, fiber: float = 0) -> float:
    """
    从宏量营养素计算热量
    
    Args:
        protein: 蛋白质 (g)
        carbs: 碳水化合物 (g)
        fat: 脂肪 (g)
        alcohol: 酒精 (g)
        fiber: 膳食纤维 (g)
    
    Returns:
        总热量 (kcal)
    
    Examples:
        >>> calculate_macro_calories(100, 200, 50)
        1650.0
    """
    calories = (
        protein * MACRO_CALORIES["protein"] +
        carbs * MACRO_CALORIES["carbs"] +
        fat * MACRO_CALORIES["fat"] +
        alcohol * MACRO_CALORIES["alcohol"] +
        fiber * MACRO_CALORIES["fiber"]
    )
    return calories


def calculate_macro_percentages(protein: float, carbs: float, fat: float) -> Dict[str, float]:
    """
    计算宏量营养素热量占比
    
    Args:
        protein: 蛋白质 (g)
        carbs: 碳水化合物 (g)
        fat: 脂肪 (g)
    
    Returns:
        各营养素热量占比字典
    
    Examples:
        >>> pct = calculate_macro_percentages(100, 200, 50)
        >>> pct["protein_pct"]
        24.2
    """
    protein_cal = protein * MACRO_CALORIES["protein"]
    carbs_cal = carbs * MACRO_CALORIES["carbs"]
    fat_cal = fat * MACRO_CALORIES["fat"]
    total_cal = protein_cal + carbs_cal + fat_cal
    
    if total_cal == 0:
        return {"protein_pct": 0, "carbs_pct": 0, "fat_pct": 0}
    
    return {
        "protein_pct": round(protein_cal / total_cal * 100, 1),
        "carbs_pct": round(carbs_cal / total_cal * 100, 1),
        "fat_pct": round(fat_cal / total_cal * 100, 1),
        "total_calories": round(total_cal, 1),
    }


# ==================== 工具函数 ====================

def bmi_calculate(weight: float, height: float) -> Dict[str, Any]:
    """
    计算BMI（身体质量指数）
    
    Args:
        weight: 体重 (kg)
        height: 身高 (cm)
    
    Returns:
        包含BMI和分类的字典
    
    Examples:
        >>> result = bmi_calculate(70, 175)
        >>> 18.5 <= result["bmi"] <= 24.9
        True
    """
    if weight <= 0:
        raise ValueError("体重必须大于0")
    if height <= 0:
        raise ValueError("身高必须大于0")
    
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    
    # WHO分类标准
    if bmi < 18.5:
        category = "underweight"
        category_cn = "偏瘦"
    elif bmi < 25:
        category = "normal"
        category_cn = "正常"
    elif bmi < 30:
        category = "overweight"
        category_cn = "超重"
    elif bmi < 35:
        category = "obese_class_1"
        category_cn = "肥胖I级"
    elif bmi < 40:
        category = "obese_class_2"
        category_cn = "肥胖II级"
    else:
        category = "obese_class_3"
        category_cn = "肥胖III级"
    
    # 计算健康体重范围
    healthy_weight_min = 18.5 * (height_m ** 2)
    healthy_weight_max = 24.9 * (height_m ** 2)
    
    return {
        "bmi": round(bmi, 1),
        "category": category,
        "category_cn": category_cn,
        "healthy_weight_range": {
            "min": round(healthy_weight_min, 1),
            "max": round(healthy_weight_max, 1),
        },
    }


def ideal_body_weight(height: float, gender: Gender, formula: str = "devine") -> Dict[str, float]:
    """
    计算理想体重
    
    支持多种公式：
    - Devine公式（最常用）
    - Robinson公式
    - Miller公式
    - Hamwi公式
    
    Args:
        height: 身高 (cm)
        gender: 性别
        formula: 公式名称 ("devine", "robinson", "miller", "hamwi")
    
    Returns:
        包含不同公式结果的字典
    
    Examples:
        >>> result = ideal_body_weight(175, Gender.MALE)
        >>> result["devine"]
        71.0
    """
    if height <= 0:
        raise ValueError("身高必须大于0")
    
    # 超过5英尺的英寸数
    height_inches = height / 2.54
    inches_over_5ft = height_inches - 60
    
    results = {}
    
    # Devine公式
    if gender == Gender.MALE:
        devine = 50 + 2.3 * inches_over_5ft
    else:
        devine = 45.5 + 2.3 * inches_over_5ft
    results["devine"] = round(devine, 1)
    
    # Robinson公式
    if gender == Gender.MALE:
        robinson = 52 + 1.9 * inches_over_5ft
    else:
        robinson = 49 + 1.7 * inches_over_5ft
    results["robinson"] = round(robinson, 1)
    
    # Miller公式
    if gender == Gender.MALE:
        miller = 56.2 + 1.41 * inches_over_5ft
    else:
        miller = 53.1 + 1.36 * inches_over_5ft
    results["miller"] = round(miller, 1)
    
    # Hamwi公式
    if gender == Gender.MALE:
        hamwi = 48 + 2.7 * inches_over_5ft
    else:
        hamwi = 45.5 + 2.2 * inches_over_5ft
    results["hamwi"] = round(hamwi, 1)
    
    # 返回平均值
    results["average"] = round(sum(results.values()) / 4, 1)
    results["recommended_formula"] = formula
    
    return results


def lean_body_mass_calculate(weight: float, body_fat_percent: float) -> Dict[str, float]:
    """
    计算瘦体重
    
    Args:
        weight: 体重 (kg)
        body_fat_percent: 体脂率 (百分比，如20表示20%)
    
    Returns:
        包含瘦体重和脂肪量的字典
    
    Examples:
        >>> result = lean_body_mass_calculate(70, 20)
        >>> result["lean_body_mass"]
        56.0
    """
    if weight <= 0:
        raise ValueError("体重必须大于0")
    if body_fat_percent < 0 or body_fat_percent > 100:
        raise ValueError("体脂率必须在0-100之间")
    
    fat_mass = weight * (body_fat_percent / 100)
    lean_mass = weight - fat_mass
    
    return {
        "lean_body_mass": round(lean_mass, 1),
        "fat_mass": round(fat_mass, 1),
        "body_fat_percent": body_fat_percent,
    }


def calorie_deficit_timeline(current_weight: float, target_weight: float,
                             daily_deficit: int) -> Dict[str, Any]:
    """
    计算减重时间线
    
    Args:
        current_weight: 当前体重 (kg)
        target_weight: 目标体重 (kg)
        daily_deficit: 每日热量缺口 (kcal)
    
    Returns:
        包含时间线和进度预测的字典
    
    Examples:
        >>> result = calorie_deficit_timeline(80, 75, 500)
        >>> result["total_days"] > 0
        True
    """
    if current_weight <= 0:
        raise ValueError("当前体重必须大于0")
    if target_weight <= 0:
        raise ValueError("目标体重必须大于0")
    if daily_deficit <= 0:
        raise ValueError("热量缺口必须大于0")
    
    weight_to_lose = current_weight - target_weight
    
    if weight_to_lose <= 0:
        return {
            "total_days": 0,
            "total_weeks": 0,
            "weekly_loss": 0,
            "message": "目标体重已达成或需要增重",
        }
    
    CALORIES_PER_KG = 7700
    total_calories_to_burn = weight_to_lose * CALORIES_PER_KG
    total_days = int(total_calories_to_burn / daily_deficit)
    total_weeks = total_days / 7
    
    return {
        "total_days": total_days,
        "total_weeks": round(total_weeks, 1),
        "weight_to_lose": round(weight_to_lose, 1),
        "daily_deficit": daily_deficit,
        "weekly_loss": round(daily_deficit * 7 / CALORIES_PER_KG, 2),
        "total_calories_to_burn": int(total_calories_to_burn),
        "milestones": _calculate_milestones(current_weight, target_weight, total_days),
    }


def _calculate_milestones(current: float, target: float, total_days: int) -> List[Dict[str, Any]]:
    """计算里程碑"""
    milestones = []
    weight_diff = current - target
    
    for percent in [25, 50, 75, 100]:
        days = int(total_days * percent / 100)
        weight = current - (weight_diff * percent / 100)
        milestones.append({
            "percent": percent,
            "days": days,
            "weight": round(weight, 1),
        })
    
    return milestones


def daily_water_intake(weight: float, activity_level: ActivityLevel = ActivityLevel.SEDENTARY) -> Dict[str, Any]:
    """
    计算每日建议饮水量
    
    基于体重和活动水平计算
    
    Args:
        weight: 体重 (kg)
        activity_level: 活动水平
    
    Returns:
        包含建议饮水量的字典
    
    Examples:
        >>> result = daily_water_intake(70, ActivityLevel.MODERATE)
        >>> result["liters"] > 2
        True
    """
    if weight <= 0:
        raise ValueError("体重必须大于0")
    
    # 基础：每公斤体重30-35ml
    base_ml = weight * 33
    
    # 活动水平调整系数
    activity_multipliers = {
        ActivityLevel.SEDENTARY: 1.0,
        ActivityLevel.LIGHT: 1.1,
        ActivityLevel.MODERATE: 1.2,
        ActivityLevel.ACTIVE: 1.3,
        ActivityLevel.VERY_ACTIVE: 1.4,
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.0)
    total_ml = base_ml * multiplier
    
    return {
        "ml": int(total_ml),
        "liters": round(total_ml / 1000, 1),
        "glasses_250ml": int(total_ml / 250),
        "glasses_500ml": int(total_ml / 500),
        "base_per_kg": 33,
        "activity_multiplier": multiplier,
    }