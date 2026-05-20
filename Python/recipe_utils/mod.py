"""
recipe_utils - 食谱工具

功能：
- 食谱缩放（按人数、份量调整配料）
- 计量单位转换（公制/英制/美制）
- 配料替代建议
- 营养成分计算
- 烹饪时间估算
- 成本计算
- 购物清单生成
- 食谱分类和标签
- 零外部依赖
"""

from typing import Optional, List, Dict, Any, Tuple, Union
from enum import Enum
from dataclasses import dataclass, field
import math
import re


class UnitType(Enum):
    """单位类型"""
    # 体积单位
    MILLILITER = "ml"
    LITER = "l"
    TEASPOON = "tsp"
    TABLESPOON = "tbsp"
    FLUID_OUNCE = "fl_oz"
    CUP = "cup"
    PINT = "pint"
    QUART = "quart"
    GALLON = "gallon"
    
    # 重量单位
    MILLIGRAM = "mg"
    GRAM = "g"
    KILOGRAM = "kg"
    OUNCE = "oz"
    POUND = "lb"
    
    # 计数单位
    PIECE = "piece"
    CLOVE = "clove"
    PINCH = "pinch"
    DASH = "dash"
    
    # 温度单位
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


class IngredientCategory(Enum):
    """配料分类"""
    PROTEIN = "protein"
    VEGETABLE = "vegetable"
    FRUIT = "fruit"
    GRAIN = "grain"
    DAIRY = "dairy"
    SPICE = "spice"
    HERB = "herb"
    OIL = "oil"
    SWEETENER = "sweetener"
    LIQUID = "liquid"
    BAKING = "baking"
    NUT = "nut"
    SEAFOOD = "seafood"
    CONDIMENT = "condiment"
    OTHER = "other"


class DietaryRestriction(Enum):
    """饮食限制"""
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    NUT_FREE = "nut_free"
    EGG_FREE = "egg_free"
    LOW_SODIUM = "low_sodium"
    LOW_CARB = "low_carb"
    KETO = "keto"
    PALEO = "paleo"


class DifficultyLevel(Enum):
    """难度等级"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class MealType(Enum):
    """餐食类型"""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    DESSERT = "dessert"
    APPETIZER = "appetizer"
    SIDE_DISH = "side_dish"
    BEVERAGE = "beverage"


# 单位转换表（基准单位：克或毫升）
UNIT_CONVERSIONS = {
    # 体积 -> 毫升
    UnitType.MILLILITER: 1,
    UnitType.LITER: 1000,
    UnitType.TEASPOON: 4.92892,
    UnitType.TABLESPOON: 14.7868,
    UnitType.FLUID_OUNCE: 29.5735,
    UnitType.CUP: 236.588,
    UnitType.PINT: 473.176,
    UnitType.QUART: 946.353,
    UnitType.GALLON: 3785.41,
    
    # 重量 -> 克
    UnitType.MILLIGRAM: 0.001,
    UnitType.GRAM: 1,
    UnitType.KILOGRAM: 1000,
    UnitType.OUNCE: 28.3495,
    UnitType.POUND: 453.592,
    
    # 计数单位（近似值，实际因食材而异）
    UnitType.PIECE: 1,
    UnitType.CLOVE: 5,  # 蒜瓣约5克
    UnitType.PINCH: 0.5,  # 一撮约0.5克
    UnitType.DASH: 0.6,  # 一小撮约0.6克
}

# 常见食材密度（克/毫升），用于体积和重量转换
INGREDIENT_DENSITY = {
    "水": 1.0,
    "water": 1.0,
    "牛奶": 1.03,
    "milk": 1.03,
    "面粉": 0.59,
    "flour": 0.59,
    "糖": 0.85,
    "sugar": 0.85,
    "盐": 1.15,
    "salt": 1.15,
    "黄油": 0.91,
    "butter": 0.91,
    "植物油": 0.92,
    "vegetable_oil": 0.92,
    "橄榄油": 0.91,
    "olive_oil": 0.91,
    "蜂蜜": 1.42,
    "honey": 1.42,
    "米饭": 0.75,
    "rice": 0.75,
    "燕麦": 0.43,
    "oats": 0.43,
}

# 常见配料营养信息（每100克）
NUTRITION_DATABASE = {
    "鸡蛋": {"calories": 155, "protein": 12.6, "carbs": 1.1, "fat": 10.6, "fiber": 0, "sodium": 124},
    "egg": {"calories": 155, "protein": 12.6, "carbs": 1.1, "fat": 10.6, "fiber": 0, "sodium": 124},
    "鸡胸肉": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0, "sodium": 74},
    "chicken_breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0, "sodium": 74},
    "牛肉": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15, "fiber": 0, "sodium": 72},
    "beef": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15, "fiber": 0, "sodium": 72},
    "猪肉": {"calories": 242, "protein": 27, "carbs": 0, "fat": 14, "fiber": 0, "sodium": 62},
    "pork": {"calories": 242, "protein": 27, "carbs": 0, "fat": 14, "fiber": 0, "sodium": 62},
    "三文鱼": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13, "fiber": 0, "sodium": 59},
    "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13, "fiber": 0, "sodium": 59},
    "米饭": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "fiber": 0.4, "sodium": 1},
    "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "fiber": 0.4, "sodium": 1},
    "面条": {"calories": 138, "protein": 4.5, "carbs": 25, "fat": 2, "fiber": 1.8, "sodium": 5},
    "noodles": {"calories": 138, "protein": 4.5, "carbs": 25, "fat": 2, "fiber": 1.8, "sodium": 5},
    "土豆": {"calories": 77, "protein": 2, "carbs": 17, "fat": 0.1, "fiber": 2.2, "sodium": 6},
    "potato": {"calories": 77, "protein": 2, "carbs": 17, "fat": 0.1, "fiber": 2.2, "sodium": 6},
    "番茄": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "fiber": 1.2, "sodium": 5},
    "tomato": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "fiber": 1.2, "sodium": 5},
    "洋葱": {"calories": 40, "protein": 1.1, "carbs": 9.3, "fat": 0.1, "fiber": 1.7, "sodium": 4},
    "onion": {"calories": 40, "protein": 1.1, "carbs": 9.3, "fat": 0.1, "fiber": 1.7, "sodium": 4},
    "大蒜": {"calories": 149, "protein": 6.4, "carbs": 33, "fat": 0.5, "fiber": 2.1, "sodium": 17},
    "garlic": {"calories": 149, "protein": 6.4, "carbs": 33, "fat": 0.5, "fiber": 2.1, "sodium": 17},
    "胡萝卜": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2, "fiber": 2.8, "sodium": 69},
    "carrot": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2, "fiber": 2.8, "sodium": 69},
    "西兰花": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "fiber": 2.6, "sodium": 33},
    "broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "fiber": 2.6, "sodium": 33},
    "菠菜": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4, "fiber": 2.2, "sodium": 79},
    "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4, "fiber": 2.2, "sodium": 79},
    "面粉": {"calories": 364, "protein": 10, "carbs": 76, "fat": 1, "fiber": 2.7, "sodium": 2},
    "flour": {"calories": 364, "protein": 10, "carbs": 76, "fat": 1, "fiber": 2.7, "sodium": 2},
    "糖": {"calories": 387, "protein": 0, "carbs": 100, "fat": 0, "fiber": 0, "sodium": 1},
    "sugar": {"calories": 387, "protein": 0, "carbs": 100, "fat": 0, "fiber": 0, "sodium": 1},
    "盐": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "sodium": 38758},
    "salt": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "sodium": 38758},
    "黄油": {"calories": 717, "protein": 0.9, "carbs": 0.1, "fat": 81, "fiber": 0, "sodium": 643},
    "butter": {"calories": 717, "protein": 0.9, "carbs": 0.1, "fat": 81, "fiber": 0, "sodium": 643},
    "橄榄油": {"calories": 884, "protein": 0, "carbs": 0, "fat": 100, "fiber": 0, "sodium": 2},
    "olive_oil": {"calories": 884, "protein": 0, "carbs": 0, "fat": 100, "fiber": 0, "sodium": 2},
    "牛奶": {"calories": 42, "protein": 3.4, "carbs": 5, "fat": 1, "fiber": 0, "sodium": 44},
    "milk": {"calories": 42, "protein": 3.4, "carbs": 5, "fat": 1, "fiber": 0, "sodium": 44},
    "芝士": {"calories": 402, "protein": 25, "carbs": 1.3, "fat": 33, "fiber": 0, "sodium": 621},
    "cheese": {"calories": 402, "protein": 25, "carbs": 1.3, "fat": 33, "fiber": 0, "sodium": 621},
    "豆腐": {"calories": 76, "protein": 8, "carbs": 1.9, "fat": 4.8, "fiber": 0.3, "sodium": 7},
    "tofu": {"calories": 76, "protein": 8, "carbs": 1.9, "fat": 4.8, "fiber": 0.3, "sodium": 7},
    "苹果": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2, "fiber": 2.4, "sodium": 1},
    "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2, "fiber": 2.4, "sodium": 1},
    "香蕉": {"calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "fiber": 2.6, "sodium": 1},
    "banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "fiber": 2.6, "sodium": 1},
}

# 配料替代建议
INGREDIENT_SUBSTITUTIONS = {
    "鸡蛋": [
        {"substitute": "亚麻蛋 (1大匙亚麻粉+3大匙水)", "ratio": 1, "note": "适合烘焙，不适合做蛋料理"},
        {"substitute": "香蕉泥", "ratio": 0.5, "note": "适合烘焙，会增加甜味"},
        {"substitute": "苹果酱", "ratio": 0.25, "note": "适合烘焙，减少其他液体"},
        {"substitute": "嫩豆腐", "ratio": 0.25, "note": "适合烘焙，增加蛋白质"},
    ],
    "牛奶": [
        {"substitute": "豆浆", "ratio": 1, "note": "适合大多数料理"},
        {"substitute": "杏仁奶", "ratio": 1, "note": "适合烘焙和饮品"},
        {"substitute": "椰奶", "ratio": 1, "note": "适合咖喱和甜点"},
        {"substitute": "燕麦奶", "ratio": 1, "note": "适合烘焙和咖啡"},
    ],
    "黄油": [
        {"substitute": "椰子油", "ratio": 0.75, "note": "适合烘焙"},
        {"substitute": "植物油", "ratio": 0.75, "note": "适合大多数料理"},
        {"substitute": "苹果酱", "ratio": 0.5, "note": "适合烘焙，减少脂肪"},
        {"substitute": "牛油果泥", "ratio": 1, "note": "适合烘焙"},
    ],
    "面粉": [
        {"substitute": "杏仁粉", "ratio": 1, "note": "低碳水，适合烘焙"},
        {"substitute": "椰子粉", "ratio": 0.25, "note": "需增加液体"},
        {"substitute": "燕麦粉", "ratio": 1, "note": "适合烘焙"},
        {"substitute": "全麦面粉", "ratio": 1, "note": "更健康的选择"},
    ],
    "糖": [
        {"substitute": "蜂蜜", "ratio": 0.75, "note": "减少其他液体"},
        {"substitute": "枫糖浆", "ratio": 0.75, "note": "减少其他液体"},
        {"substitute": "甜菊糖", "ratio": 0.01, "note": "无热量甜味剂"},
        {"substitute": "木糖醇", "ratio": 1, "note": "低热量代糖"},
    ],
    "盐": [
        {"substitute": "酱油", "ratio": 2, "note": "增加鲜味"},
        {"substitute": "海盐", "ratio": 1, "note": "矿物质更丰富"},
        {"substitute": "低钠盐", "ratio": 1, "note": "适合低钠饮食"},
    ],
    "大蒜": [
        {"substitute": "蒜粉", "ratio": 0.25, "note": "更方便储存"},
        {"substitute": "蒜泥", "ratio": 0.5, "note": "蒜味更浓"},
    ],
    "洋葱": [
        {"substitute": "葱", "ratio": 0.5, "note": "味道更清淡"},
        {"substitute": "韭葱", "ratio": 1, "note": "味道更温和"},
        {"substitute": "洋葱粉", "ratio": 0.1, "note": "适合调味"},
    ],
}


@dataclass
class Ingredient:
    """配料"""
    name: str
    amount: float
    unit: UnitType
    category: IngredientCategory = IngredientCategory.OTHER
    notes: str = ""
    
    def to_grams(self) -> float:
        """转换为克"""
        if self.unit in [UnitType.GRAM, UnitType.MILLIGRAM, UnitType.KILOGRAM, 
                         UnitType.OUNCE, UnitType.POUND]:
            return self.amount * UNIT_CONVERSIONS.get(self.unit, 1)
        
        # 尝试使用密度转换
        density = INGREDIENT_DENSITY.get(self.name.lower(), INGREDIENT_DENSITY.get(self.name, 1.0))
        
        if self.unit in [UnitType.MILLILITER, UnitType.LITER, UnitType.TEASPOON,
                         UnitType.TABLESPOON, UnitType.FLUID_OUNCE, UnitType.CUP,
                         UnitType.PINT, UnitType.QUART, UnitType.GALLON]:
            ml = self.amount * UNIT_CONVERSIONS.get(self.unit, 1)
            return ml * density
        
        return self.amount  # 计数单位，返回原值
    
    def to_milliliters(self) -> float:
        """转换为毫升"""
        if self.unit in [UnitType.MILLILITER, UnitType.LITER, UnitType.TEASPOON,
                         UnitType.TABLESPOON, UnitType.FLUID_OUNCE, UnitType.CUP,
                         UnitType.PINT, UnitType.QUART, UnitType.GALLON]:
            return self.amount * UNIT_CONVERSIONS.get(self.unit, 1)
        
        # 尝试使用密度反向转换
        density = INGREDIENT_DENSITY.get(self.name.lower(), INGREDIENT_DENSITY.get(self.name, 1.0))
        grams = self.to_grams()
        return grams / density


@dataclass
class NutritionInfo:
    """营养信息"""
    calories: float = 0
    protein: float = 0
    carbs: float = 0
    fat: float = 0
    fiber: float = 0
    sodium: float = 0
    
    def __add__(self, other: 'NutritionInfo') -> 'NutritionInfo':
        return NutritionInfo(
            calories=self.calories + other.calories,
            protein=self.protein + other.protein,
            carbs=self.carbs + other.carbs,
            fat=self.fat + other.fat,
            fiber=self.fiber + other.fiber,
            sodium=self.sodium + other.sodium
        )
    
    def __mul__(self, factor: float) -> 'NutritionInfo':
        return NutritionInfo(
            calories=self.calories * factor,
            protein=self.protein * factor,
            carbs=self.carbs * factor,
            fat=self.fat * factor,
            fiber=self.fiber * factor,
            sodium=self.sodium * factor
        )
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "calories": round(self.calories, 1),
            "protein": round(self.protein, 1),
            "carbs": round(self.carbs, 1),
            "fat": round(self.fat, 1),
            "fiber": round(self.fiber, 1),
            "sodium": round(self.sodium, 1)
        }


@dataclass
class RecipeStep:
    """食谱步骤"""
    step_number: int
    instruction: str
    duration_minutes: int = 0
    temperature: Optional[int] = None
    temperature_unit: str = "celsius"
    tips: List[str] = field(default_factory=list)


@dataclass
class Recipe:
    """食谱"""
    name: str
    servings: int
    ingredients: List[Ingredient]
    steps: List[RecipeStep]
    prep_time_minutes: int = 0
    cook_time_minutes: int = 0
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    meal_type: MealType = MealType.DINNER
    tags: List[str] = field(default_factory=list)
    dietary_restrictions: List[DietaryRestriction] = field(default_factory=list)
    
    @property
    def total_time_minutes(self) -> int:
        return self.prep_time_minutes + self.cook_time_minutes
    
    def scale(self, target_servings: int) -> 'Recipe':
        """缩放食谱"""
        factor = target_servings / self.servings
        scaled_ingredients = [
            Ingredient(
                name=ing.name,
                amount=ing.amount * factor,
                unit=ing.unit,
                category=ing.category,
                notes=ing.notes
            )
            for ing in self.ingredients
        ]
        return Recipe(
            name=self.name,
            servings=target_servings,
            ingredients=scaled_ingredients,
            steps=self.steps,
            prep_time_minutes=self.prep_time_minutes,
            cook_time_minutes=self.cook_time_minutes,
            difficulty=self.difficulty,
            meal_type=self.meal_type,
            tags=self.tags.copy(),
            dietary_restrictions=self.dietary_restrictions.copy()
        )


class RecipeScaler:
    """食谱缩放器"""
    
    @staticmethod
    def scale_recipe(recipe: Recipe, target_servings: int) -> Recipe:
        """缩放食谱到目标份数"""
        return recipe.scale(target_servings)
    
    @staticmethod
    def scale_ingredient(ingredient: Ingredient, factor: float) -> Ingredient:
        """缩放单个配料"""
        return Ingredient(
            name=ingredient.name,
            amount=ingredient.amount * factor,
            unit=ingredient.unit,
            category=ingredient.category,
            notes=ingredient.notes
        )
    
    @staticmethod
    def smart_round(amount: float, unit: UnitType) -> float:
        """智能舍入，避免产生不切实际的数值"""
        if unit in [UnitType.PIECE, UnitType.CLOVE]:
            return max(1, round(amount))
        
        if amount >= 1:
            # 四舍五入到最接近的0.25
            return round(amount * 4) / 4
        elif amount >= 0.25:
            # 四舍五入到最接近的0.125
            return round(amount * 8) / 8
        else:
            # 保留两位小数
            return round(amount, 2)


class UnitConverter:
    """单位转换器"""
    
    @staticmethod
    def convert(amount: float, from_unit: UnitType, to_unit: UnitType,
                ingredient_name: str = "") -> Tuple[float, bool]:
        """
        转换单位
        返回: (转换后的数量, 是否成功)
        """
        # 如果单位相同
        if from_unit == to_unit:
            return amount, True
        
        # 检查是否都是体积单位
        volume_units = {UnitType.MILLILITER, UnitType.LITER, UnitType.TEASPOON,
                        UnitType.TABLESPOON, UnitType.FLUID_OUNCE, UnitType.CUP,
                        UnitType.PINT, UnitType.QUART, UnitType.GALLON}
        
        # 检查是否都是重量单位
        weight_units = {UnitType.MILLIGRAM, UnitType.GRAM, UnitType.KILOGRAM,
                       UnitType.OUNCE, UnitType.POUND}
        
        from_is_volume = from_unit in volume_units
        to_is_volume = to_unit in volume_units
        from_is_weight = from_unit in weight_units
        to_is_weight = to_unit in weight_units
        
        # 体积到体积 或 重量到重量
        if (from_is_volume and to_is_volume) or (from_is_weight and to_is_weight):
            base_value = amount * UNIT_CONVERSIONS.get(from_unit, 1)
            result = base_value / UNIT_CONVERSIONS.get(to_unit, 1)
            return result, True
        
        # 体积到重量 或 重量到体积（需要密度）
        if ingredient_name:
            density = INGREDIENT_DENSITY.get(ingredient_name.lower(), 
                                            INGREDIENT_DENSITY.get(ingredient_name))
            if density:
                if from_is_volume and to_is_weight:
                    # 体积 -> 重量
                    ml = amount * UNIT_CONVERSIONS.get(from_unit, 1)
                    grams = ml * density
                    result = grams / UNIT_CONVERSIONS.get(to_unit, 1)
                    return result, True
                elif from_is_weight and to_is_volume:
                    # 重量 -> 体积
                    grams = amount * UNIT_CONVERSIONS.get(from_unit, 1)
                    ml = grams / density
                    result = ml / UNIT_CONVERSIONS.get(to_unit, 1)
                    return result, True
        
        return amount, False
    
    @staticmethod
    def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
        """温度转换"""
        if from_unit.lower() == to_unit.lower():
            return value
        
        if from_unit.lower() == "celsius" or from_unit.lower() == "c":
            if to_unit.lower() == "fahrenheit" or to_unit.lower() == "f":
                return value * 9/5 + 32
        elif from_unit.lower() == "fahrenheit" or from_unit.lower() == "f":
            if to_unit.lower() == "celsius" or to_unit.lower() == "c":
                return (value - 32) * 5/9
        
        return value
    
    @staticmethod
    def get_common_conversions() -> Dict[str, List[str]]:
        """获取常用转换对照"""
        return {
            "体积": ["1杯 = 240毫升", "1大匙 = 15毫升", "1小匙 = 5毫升", 
                   "1液盎司 = 30毫升", "1品脱 = 473毫升", "1夸脱 = 946毫升"],
            "重量": ["1磅 = 454克", "1盎司 = 28克", "1公斤 = 2.2磅", "1斤 = 500克"],
            "温度": ["摄氏 × 9/5 + 32 = 华氏", "华氏 - 32 × 5/9 = 摄氏",
                   "180°C = 350°F", "200°C = 400°F", "220°C = 425°F"]
        }


class NutritionCalculator:
    """营养计算器"""
    
    @staticmethod
    def get_ingredient_nutrition(ingredient: Ingredient) -> NutritionInfo:
        """获取单个配料的营养信息"""
        nutrition_data = NUTRITION_DATABASE.get(ingredient.name.lower(),
                                                 NUTRITION_DATABASE.get(ingredient.name))
        
        if not nutrition_data:
            return NutritionInfo()
        
        # 获取以克为单位的重量
        grams = ingredient.to_grams()
        factor = grams / 100
        
        return NutritionInfo(
            calories=nutrition_data["calories"] * factor,
            protein=nutrition_data["protein"] * factor,
            carbs=nutrition_data["carbs"] * factor,
            fat=nutrition_data["fat"] * factor,
            fiber=nutrition_data["fiber"] * factor,
            sodium=nutrition_data["sodium"] * factor
        )
    
    @staticmethod
    def get_recipe_nutrition(recipe: Recipe) -> NutritionInfo:
        """获取整份食谱的营养信息"""
        total = NutritionInfo()
        for ingredient in recipe.ingredients:
            total += NutritionCalculator.get_ingredient_nutrition(ingredient)
        return total
    
    @staticmethod
    def get_nutrition_per_serving(recipe: Recipe) -> NutritionInfo:
        """获取每份的营养信息"""
        total = NutritionCalculator.get_recipe_nutrition(recipe)
        return total * (1 / recipe.servings)


class IngredientSubstitutor:
    """配料替代器"""
    
    @staticmethod
    def get_substitutions(ingredient_name: str) -> List[Dict[str, Any]]:
        """获取配料的替代建议"""
        return INGREDIENT_SUBSTITUTIONS.get(ingredient_name, 
                                            INGREDIENT_SUBSTITUTIONS.get(ingredient_name.lower(), []))
    
    @staticmethod
    def find_vegan_alternative(ingredient_name: str) -> Optional[str]:
        """查找素食替代品"""
        vegan_alternatives = {
            "鸡蛋": "亚麻蛋或嫩豆腐",
            "牛奶": "豆浆或杏仁奶",
            "黄油": "椰子油或植物黄油",
            "蜂蜜": "枫糖浆或龙舌兰蜜",
            "芝士": "素食芝士或营养酵母",
            "酸奶": "椰奶酸奶或豆浆酸奶",
        }
        return vegan_alternatives.get(ingredient_name, 
                                       vegan_alternatives.get(ingredient_name.lower()))
    
    @staticmethod
    def find_gluten_free_alternative(ingredient_name: str) -> Optional[str]:
        """查找无麸质替代品"""
        gf_alternatives = {
            "面粉": "杏仁粉、椰子粉或无麸质面粉混合",
            "面条": "米粉或荞麦面",
            "面包糠": "碎玉米片或杏仁碎",
            "酱油": "无麸质酱油或椰子氨基酸",
        }
        return gf_alternatives.get(ingredient_name,
                                    gf_alternatives.get(ingredient_name.lower()))


class ShoppingListGenerator:
    """购物清单生成器"""
    
    @staticmethod
    def generate(recipes: List[Recipe], servings_per_recipe: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        从多个食谱生成购物清单
        
        Args:
            recipes: 食谱列表
            servings_per_recipe: 每个食谱的目标份数，如果提供则缩放
        
        Returns:
            购物清单字典
        """
        ingredient_totals: Dict[str, Dict[str, float]] = {}
        
        for i, recipe in enumerate(recipes):
            target_recipe = recipe
            if servings_per_recipe and i < len(servings_per_recipe):
                target_recipe = recipe.scale(servings_per_recipe[i])
            
            for ing in target_recipe.ingredients:
                key = ing.name.lower()
                if key not in ingredient_totals:
                    ingredient_totals[key] = {
                        "name": ing.name,
                        "amounts": [],
                        "total_grams": 0,
                        "category": ing.category.value
                    }
                
                ingredient_totals[key]["amounts"].append({
                    "amount": ing.amount,
                    "unit": ing.unit.value
                })
                ingredient_totals[key]["total_grams"] += ing.to_grams()
        
        # 按类别分组
        by_category: Dict[str, List[Dict[str, Any]]] = {}
        for data in ingredient_totals.values():
            cat = data["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append({
                "name": data["name"],
                "amounts": data["amounts"],
                "estimated_grams": round(data["total_grams"], 1)
            })
        
        return {
            "total_ingredients": len(ingredient_totals),
            "by_category": by_category,
            "flat_list": list(ingredient_totals.values())
        }


class RecipeParser:
    """食谱解析器"""
    
    # 单位模式（按优先级排序，长的单位先匹配）
    UNIT_PATTERNS = [
        (r'(?:kg|公斤|千克)', UnitType.KILOGRAM),  # kg要先于g
        (r'(?:tbsp|大匙|汤匙)', UnitType.TABLESPOON),  # tbsp要先于tsp
        (r'(?:tsp|小匙|茶匙)', UnitType.TEASPOON),
        (r'(?:ml|毫升)', UnitType.MILLILITER),
        (r'(?:cup|杯)', UnitType.CUP),
        (r'(?:g|克)', UnitType.GRAM),
        (r'(?:oz|盎司)', UnitType.OUNCE),
        (r'(?:lb|磅)', UnitType.POUND),
        (r'(?:个|只|片)', UnitType.PIECE),
        (r'(?:瓣)', UnitType.CLOVE),
        (r'(?:l|升)', UnitType.LITER),
    ]
    
    @staticmethod
    def parse_ingredient_line(line: str) -> Optional[Ingredient]:
        """
        解析配料行
        支持格式:
        - "100g 面粉"
        - "面粉 100克"
        - "2 个鸡蛋"
        - "1/2 杯牛奶"
        """
        line = line.strip()
        if not line:
            return None
        
        # 尝试匹配数量和单位
        amount = 0
        unit = UnitType.PIECE
        name = line
        
        # 尝试解析分数
        fraction_pattern = r'(\d+)\s*/\s*(\d+)'
        match = re.search(fraction_pattern, line)
        if match:
            numerator = int(match.group(1))
            denominator = int(match.group(2))
            amount = numerator / denominator
        
        # 尝试解析小数或整数
        number_pattern = r'(\d+(?:\.\d+)?)'
        if amount == 0:
            match = re.search(number_pattern, line)
            if match:
                amount = float(match.group(1))
        
        if amount > 0:
            # 查找单位（按优先级顺序）
            for pattern, unit_type in RecipeParser.UNIT_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    unit = unit_type
                    break
            
            # 提取名称（移除数字和单位）
            name = re.sub(fraction_pattern, '', line)
            name = re.sub(number_pattern, '', name)
            for pattern, _ in RecipeParser.UNIT_PATTERNS:
                name = re.sub(pattern, '', name, flags=re.IGNORECASE)
            name = name.strip()
        
        if not name:
            return None
        
        return Ingredient(
            name=name,
            amount=amount if amount > 0 else 1,
            unit=unit
        )


class CostCalculator:
    """成本计算器"""
    
    # 简化的配料价格数据库（每100克/100毫升的价格，单位：元）
    INGREDIENT_PRICES = {
        "鸡蛋": 1.0,
        "egg": 1.0,
        "鸡胸肉": 3.5,
        "chicken_breast": 3.5,
        "牛肉": 6.0,
        "beef": 6.0,
        "猪肉": 4.0,
        "pork": 4.0,
        "米饭": 0.5,
        "rice": 0.5,
        "面粉": 0.4,
        "flour": 0.4,
        "糖": 0.8,
        "sugar": 0.8,
        "盐": 0.2,
        "salt": 0.2,
        "黄油": 10.0,
        "butter": 10.0,
        "牛奶": 1.2,
        "milk": 1.2,
        "橄榄油": 15.0,
        "olive_oil": 15.0,
        "蔬菜": 2.0,
        "vegetable": 2.0,
        "水果": 3.0,
        "fruit": 3.0,
    }
    
    @staticmethod
    def estimate_cost(recipe: Recipe) -> Dict[str, Any]:
        """估算食谱成本"""
        total_cost = 0
        ingredient_costs = []
        
        for ing in recipe.ingredients:
            price_per_100g = CostCalculator.INGREDIENT_PRICES.get(
                ing.name.lower(),
                CostCalculator.INGREDIENT_PRICES.get(ing.name, 2.0)  # 默认价格
            )
            grams = ing.to_grams()
            cost = (grams / 100) * price_per_100g
            total_cost += cost
            
            ingredient_costs.append({
                "name": ing.name,
                "amount": ing.amount,
                "unit": ing.unit.value,
                "estimated_grams": round(grams, 1),
                "cost": round(cost, 2)
            })
        
        return {
            "total_cost": round(total_cost, 2),
            "cost_per_serving": round(total_cost / recipe.servings, 2),
            "ingredient_costs": ingredient_costs,
            "currency": "CNY"
        }


class RecipeAnalyzer:
    """食谱分析器"""
    
    @staticmethod
    def analyze(recipe: Recipe) -> Dict[str, Any]:
        """全面分析食谱"""
        nutrition = NutritionCalculator.get_recipe_nutrition(recipe)
        nutrition_per_serving = NutritionCalculator.get_nutrition_per_serving(recipe)
        cost = CostCalculator.estimate_cost(recipe)
        
        # 分析饮食限制兼容性
        compatible_diets = RecipeAnalyzer._check_dietary_compatibility(recipe)
        
        # 计算健康评分
        health_score = RecipeAnalyzer._calculate_health_score(nutrition_per_serving)
        
        # 时间分析
        time_analysis = {
            "prep_time": recipe.prep_time_minutes,
            "cook_time": recipe.cook_time_minutes,
            "total_time": recipe.total_time_minutes,
            "time_category": RecipeAnalyzer._categorize_time(recipe.total_time_minutes)
        }
        
        return {
            "recipe_name": recipe.name,
            "servings": recipe.servings,
            "difficulty": recipe.difficulty.value,
            "meal_type": recipe.meal_type.value,
            "total_nutrition": nutrition.to_dict(),
            "nutrition_per_serving": nutrition_per_serving.to_dict(),
            "cost": cost,
            "health_score": health_score,
            "compatible_diets": [d.value for d in compatible_diets],
            "time_analysis": time_analysis,
            "tags": recipe.tags,
            "ingredient_count": len(recipe.ingredients),
            "step_count": len(recipe.steps)
        }
    
    @staticmethod
    def _check_dietary_compatibility(recipe: Recipe) -> List[DietaryRestriction]:
        """检查饮食兼容性"""
        compatible = []
        
        # 检查是否素食
        meat_ingredients = {"牛肉", "猪肉", "鸡肉", "羊肉", "beef", "pork", "chicken", "lamb"}
        has_meat = any(ing.name.lower() in meat_ingredients for ing in recipe.ingredients)
        
        if not has_meat:
            compatible.append(DietaryRestriction.VEGETARIAN)
            
            # 检查是否纯素
            animal_products = {"鸡蛋", "牛奶", "芝士", "黄油", "蜂蜜", 
                             "egg", "milk", "cheese", "butter", "honey"}
            has_animal = any(ing.name.lower() in animal_products for ing in recipe.ingredients)
            if not has_animal:
                compatible.append(DietaryRestriction.VEGAN)
        
        # 检查无麸质
        gluten_ingredients = {"面粉", "面条", "面包", "flour", "noodles", "bread"}
        has_gluten = any(ing.name.lower() in gluten_ingredients for ing in recipe.ingredients)
        if not has_gluten:
            compatible.append(DietaryRestriction.GLUTEN_FREE)
        
        # 检查无乳制品
        dairy_ingredients = {"牛奶", "芝士", "黄油", "酸奶", "cream",
                            "milk", "cheese", "butter", "yogurt"}
        has_dairy = any(ing.name.lower() in dairy_ingredients for ing in recipe.ingredients)
        if not has_dairy:
            compatible.append(DietaryRestriction.DAIRY_FREE)
        
        return compatible
    
    @staticmethod
    def _calculate_health_score(nutrition: NutritionInfo) -> Dict[str, Any]:
        """计算健康评分（0-100）"""
        score = 50  # 基础分
        
        # 蛋白质加分
        if nutrition.protein >= 20:
            score += 10
        elif nutrition.protein >= 10:
            score += 5
        
        # 纤维加分
        if nutrition.fiber >= 5:
            score += 10
        elif nutrition.fiber >= 3:
            score += 5
        
        # 钠含量扣分
        if nutrition.sodium > 1000:
            score -= 15
        elif nutrition.sodium > 600:
            score -= 10
        elif nutrition.sodium > 400:
            score -= 5
        
        # 饱和脂肪扣分（简化，用总脂肪）
        if nutrition.fat > 30:
            score -= 10
        elif nutrition.fat > 20:
            score -= 5
        
        # 热量评分
        if 300 <= nutrition.calories <= 600:
            score += 5
        elif nutrition.calories > 800:
            score -= 10
        
        score = max(0, min(100, score))
        
        return {
            "score": score,
            "grade": RecipeAnalyzer._score_to_grade(score),
            "highlights": RecipeAnalyzer._get_health_highlights(nutrition)
        }
    
    @staticmethod
    def _score_to_grade(score: int) -> str:
        """分数转等级"""
        if score >= 80:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 40:
            return "C"
        elif score >= 20:
            return "D"
        return "F"
    
    @staticmethod
    def _get_health_highlights(nutrition: NutritionInfo) -> List[str]:
        """获取健康亮点"""
        highlights = []
        
        if nutrition.protein >= 20:
            highlights.append("高蛋白")
        if nutrition.fiber >= 5:
            highlights.append("高纤维")
        if nutrition.sodium < 400:
            highlights.append("低钠")
        if nutrition.fat < 10:
            highlights.append("低脂")
        if nutrition.calories < 400:
            highlights.append("低热量")
        
        return highlights
    
    @staticmethod
    def _categorize_time(minutes: int) -> str:
        """时间分类"""
        if minutes <= 15:
            return "快手菜"
        elif minutes <= 30:
            return "简单快手"
        elif minutes <= 60:
            return "中等时长"
        elif minutes <= 120:
            return "需要耐心"
        return "复杂料理"


# 便捷函数
def scale_recipe(recipe: Recipe, target_servings: int) -> Recipe:
    """缩放食谱"""
    return RecipeScaler.scale_recipe(recipe, target_servings)


def convert_unit(amount: float, from_unit: UnitType, to_unit: UnitType,
                ingredient_name: str = "") -> Tuple[float, bool]:
    """转换单位"""
    return UnitConverter.convert(amount, from_unit, to_unit, ingredient_name)


def get_nutrition(ingredient: Ingredient) -> NutritionInfo:
    """获取配料营养信息"""
    return NutritionCalculator.get_ingredient_nutrition(ingredient)


def get_substitutions(ingredient_name: str) -> List[Dict[str, Any]]:
    """获取配料替代建议"""
    return IngredientSubstitutor.get_substitutions(ingredient_name)


def analyze_recipe(recipe: Recipe) -> Dict[str, Any]:
    """分析食谱"""
    return RecipeAnalyzer.analyze(recipe)


def generate_shopping_list(recipes: List[Recipe], 
                          servings_per_recipe: Optional[List[int]] = None) -> Dict[str, Any]:
    """生成购物清单"""
    return ShoppingListGenerator.generate(recipes, servings_per_recipe)


def parse_ingredient(text: str) -> Optional[Ingredient]:
    """解析配料文本"""
    return RecipeParser.parse_ingredient_line(text)


def estimate_recipe_cost(recipe: Recipe) -> Dict[str, Any]:
    """估算食谱成本"""
    return CostCalculator.estimate_cost(recipe)


def get_common_conversions() -> Dict[str, List[str]]:
    """获取常用转换"""
    return UnitConverter.get_common_conversions()


# 示例食谱
def get_example_recipe() -> Recipe:
    """获取示例食谱"""
    return Recipe(
        name="番茄炒蛋",
        servings=2,
        ingredients=[
            Ingredient("鸡蛋", 3, UnitType.PIECE, IngredientCategory.PROTEIN),
            Ingredient("番茄", 2, UnitType.PIECE, IngredientCategory.VEGETABLE),
            Ingredient("油", 2, UnitType.TABLESPOON, IngredientCategory.OIL),
            Ingredient("盐", 1, UnitType.TEASPOON, IngredientCategory.SPICE),
            Ingredient("糖", 0.5, UnitType.TEASPOON, IngredientCategory.SWEETENER),
            Ingredient("葱", 1, UnitType.PIECE, IngredientCategory.HERB),
        ],
        steps=[
            RecipeStep(1, "鸡蛋打散，加少许盐调味", 2),
            RecipeStep(2, "番茄切块备用", 2),
            RecipeStep(3, "热锅下油，倒入蛋液炒至半熟盛出", 3),
            RecipeStep(4, "锅中加少许油，放入番茄翻炒", 3),
            RecipeStep(5, "加入糖和盐调味", 1),
            RecipeStep(6, "倒入炒好的鸡蛋，翻炒均匀即可", 2),
        ],
        prep_time_minutes=5,
        cook_time_minutes=10,
        difficulty=DifficultyLevel.EASY,
        meal_type=MealType.DINNER,
        tags=["家常菜", "快手菜", "素食可选"],
        dietary_restrictions=[DietaryRestriction.GLUTEN_FREE]
    )