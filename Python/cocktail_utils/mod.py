"""
Cocktail Utils - 鸡尾酒配方工具库

功能：
- 经典鸡尾酒配方数据库（100+ 款经典鸡尾酒）
- 按名称/原料/酒类搜索
- 随机推荐
- 酒精含量(ABV)计算
- 按口味筛选（甜/酸/苦/咸/鲜）
- 购物清单生成
- 成本估算
- 容量换算
"""

import random
import math
from typing import Optional, Union, List, Tuple, Dict
from dataclasses import dataclass, field
from enum import Enum


class SpiritType(Enum):
    """基酒类型"""
    VODKA = "vodka"
    GIN = "gin"
    RUM = "rum"
    TEQUILA = "tequila"
    WHISKEY = "whiskey"
    BRANDY = "brandy"
    COGNAC = "cognac"
    LIQUEUR = "liqueur"
    WINE = "wine"
    CHAMPAGNE = "champagne"
    BEER = "beer"
    NONE = "none"  # 无酒精


class Flavor(Enum):
    """口味类型"""
    SWEET = "sweet"
    SOUR = "sour"
    BITTER = "bitter"
    SALTY = "salty"
    UMAMI = "umami"
    SPICY = "spicy"
    FRUITY = "fruity"
    HERBAL = "herbal"
    CREAMY = "creamy"
    DRY = "dry"  # 干型
    FRESH = "fresh"  # 清爽
    RASPBERRY = "rasperry"


class GlassType(Enum):
    """酒杯类型"""
    MARTINI = "martini"  # 马天尼杯
    HIGHBALL = "highball"  # 高球杯
    LOWBALL = "lowball"  # 低球杯/古典杯
    COLLINS = "collins"  # 柯林杯
    COUPE = "coupe"  # 阔口香槟杯
    MARGARITA = "margarita"  # 玛格丽特杯
    HURRICANE = "hurricane"  # 飓风杯
    SHOT = "shot"  # 烈酒杯
    WINE = "wine"  # 葡萄酒杯
    FLUTE = "flute"  # 笛形香槟杯
    ROCKS = "rocks"  # 岩石杯
    IRISH_COFFEE = "irish_coffee"  # 爱尔兰咖啡杯
    PINT = "pint"  # 品脱杯


class IceType(Enum):
    """冰块类型"""
    CUBED = "cubed"  # 方冰
    CRUSHED = "crushed"  # 碎冰
    SPHERE = "sphere"  # 球冰
    LARGE_CUBE = "large_cube"  # 大方冰
    NONE = "none"  # 无冰


class Garnish(Enum):
    """装饰物"""
    LEMON_WEDGE = "lemon_wedge"
    LEMON_TWIST = "lemon_twist"
    LEMON_SLICE = "lemon_slice"
    LIME_WEDGE = "lime_wedge"
    LIME_WHEEL = "lime_wheel"
    ORANGE_WEDGE = "orange_wedge"
    ORANGE_SLICE = "orange_slice"
    ORANGE_TWIST = "orange_twist"
    CHERRY = "cherry"
    OLIVE = "olive"
    SALT_RIM = "salt_rim"
    SUGAR_RIM = "sugar_rim"
    MINT = "mint"
    CUCUMBER = "cucumber"
    CELERY = "celery"
    CINNAMON = "cinnamon"
    NUTMEG = "nutmeg"
    COCOA = "cocoa"
    CREAM = "cream"
    PINEAPPLE = "pineapple"
    COCONUT = "coconut"
    STRAWBERRY = "strawberry"
    BLUEBERRY = "blueberry"
    BANANA = "banana"
    GRAPEFRUIT = "grapefruit"
    BASIL = "basil"
    ROSEMARY = "rosemary"
    THYME = "thyme"
    EDIBLE_FLOWER = "edible_flower"
    PAPER_UMBRELLA = "paper_umbrella"
    CANDY = "candy"
    GRAPE = "grape"
    APPLE = "apple"
    PEAR = "pear"
    PEACH = "peach"
    MANGO = "mango"
    PASSION_FRUIT = "passion_fruit"
    WATERMELON = "watermelon"
    KIWI = "kiwi"
    POMEGRANATE = "pomegranate"
    RASPBERRY = "raspberry"


@dataclass
class Ingredient:
    """原料"""
    name: str
    amount: float  # 毫升数
    unit: str = "ml"
    abv: float = 0.0  # 酒精含量百分比 (0-100)
    is_optional: bool = False
    cost_per_ml: float = 0.0  # 每毫升成本（可选）
    
    @property
    def alcohol_volume(self) -> float:
        """纯酒精体积（毫升）"""
        return self.amount * (self.abv / 100)
    
    @property
    def cost(self) -> float:
        """原料成本"""
        return self.amount * self.cost_per_ml


@dataclass
class Cocktail:
    """鸡尾酒配方"""
    name: str
    name_zh: str
    ingredients: List[Ingredient]
    instructions: List[str]
    glass: GlassType
    ice: IceType = IceType.CUBED
    garnishes: List[Garnish] = field(default_factory=list)
    flavors: List[Flavor] = field(default_factory=list)
    spirits: List[SpiritType] = field(default_factory=list)
    description: str = ""
    origin: str = ""
    abv: float = 0.0  # 酒精度（自动计算或手动指定）
    iba_category: str = ""  # IBA 分类
    difficulty: int = 1  # 1-5 难度
    prep_time: int = 5  # 制作时间（分钟）
    
    def __post_init__(self):
        """初始化后计算酒精度"""
        if self.abv == 0.0:
            self.abv = self.calculate_abv()
    
    def calculate_abv(self) -> float:
        """计算鸡尾酒酒精度"""
        total_volume = sum(ing.amount for ing in self.ingredients if not ing.is_optional)
        if total_volume == 0:
            return 0.0
        total_alcohol = sum(ing.alcohol_volume for ing in self.ingredients)
        return round((total_alcohol / total_volume) * 100, 1)
    
    @property
    def total_volume(self) -> float:
        """总容量（毫升）"""
        return sum(ing.amount for ing in self.ingredients if not ing.is_optional)
    
    @property
    def total_alcohol(self) -> float:
        """纯酒精总量（毫升）"""
        return sum(ing.alcohol_volume for ing in self.ingredients)
    
    @property
    def total_cost(self) -> float:
        """总成本"""
        return sum(ing.cost for ing in self.ingredients)
    
    def get_shopping_list(self) -> Dict[str, float]:
        """获取购物清单（原料名 -> 需要量）"""
        shopping = {}
        for ing in self.ingredients:
            if ing.name in shopping:
                shopping[ing.name] += ing.amount
            else:
                shopping[ing.name] = ing.amount
        return shopping


# 经典鸡尾酒数据库
CLASSIC_COCKTAILS: List[Cocktail] = [
    # 马天尼家族
    Cocktail(
        name="Martini",
        name_zh="马天尼",
        ingredients=[
            Ingredient("Gin", 60, "ml", 40),
            Ingredient("Dry Vermouth", 10, "ml", 15),
        ],
        instructions=[
            "将金酒和干味美思倒入调酒杯",
            "加入冰块搅拌约30秒",
            "滤入冰镇马天尼杯",
            "用柠檬皮或橄榄装饰"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[Garnish.LEMON_TWIST, Garnish.OLIVE],
        flavors=[Flavor.DRY, Flavor.HERBAL],
        spirits=[SpiritType.GIN],
        description="鸡尾酒之王，经典干型鸡尾酒",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    Cocktail(
        name="Dirty Martini",
        name_zh="脏马天尼",
        ingredients=[
            Ingredient("Gin", 60, "ml", 40),
            Ingredient("Dry Vermouth", 10, "ml", 15),
            Ingredient("Olive Brine", 15, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入调酒杯",
            "加入冰块搅拌约30秒",
            "滤入冰镇马天尼杯",
            "用橄榄装饰"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[Garnish.OLIVE],
        flavors=[Flavor.SALTY, Flavor.HERBAL],
        spirits=[SpiritType.GIN],
        description="马天尼的变体，加入橄榄盐水",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    Cocktail(
        name="Vodka Martini",
        name_zh="伏特加马天尼",
        ingredients=[
            Ingredient("Vodka", 60, "ml", 40),
            Ingredient("Dry Vermouth", 10, "ml", 15),
        ],
        instructions=[
            "将伏特加和干味美思倒入调酒杯",
            "加入冰块搅拌约30秒",
            "滤入冰镇马天尼杯",
            "用柠檬皮装饰"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[Garnish.LEMON_TWIST],
        flavors=[Flavor.DRY],
        spirits=[SpiritType.VODKA],
        description="用伏特加代替金酒的马天尼",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    
    # 酸酒家族
    Cocktail(
        name="Margarita",
        name_zh="玛格丽特",
        ingredients=[
            Ingredient("Tequila", 50, "ml", 40),
            Ingredient("Cointreau", 25, "ml", 40),
            Ingredient("Lime Juice", 25, "ml", 0),
        ],
        instructions=[
            "用盐边装饰玛格丽特杯",
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入杯中",
            "用青柠轮装饰"
        ],
        glass=GlassType.MARGARITA,
        ice=IceType.CUBED,
        garnishes=[Garnish.SALT_RIM, Garnish.LIME_WHEEL],
        flavors=[Flavor.SOUR, Flavor.SWEET],
        spirits=[SpiritType.TEQUILA],
        description="墨西哥经典鸡尾酒，酸甜平衡",
        origin="墨西哥",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    Cocktail(
        name="Daiquiri",
        name_zh="黛琪莉",
        ingredients=[
            Ingredient("White Rum", 60, "ml", 40),
            Ingredient("Lime Juice", 30, "ml", 0),
            Ingredient("Simple Syrup", 20, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇阔口香槟杯",
            "用青柠轮装饰"
        ],
        glass=GlassType.COUPE,
        ice=IceType.CUBED,
        garnishes=[Garnish.LIME_WHEEL],
        flavors=[Flavor.SOUR, Flavor.SWEET],
        spirits=[SpiritType.RUM],
        description="古巴经典鸡尾酒，海明威最爱",
        origin="古巴",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    Cocktail(
        name="Whiskey Sour",
        name_zh="威士忌酸",
        ingredients=[
            Ingredient("Bourbon Whiskey", 45, "ml", 40),
            Ingredient("Lemon Juice", 30, "ml", 0),
            Ingredient("Simple Syrup", 20, "ml", 0),
            Ingredient("Egg White", 15, "ml", 0, is_optional=True),
        ],
        instructions=[
            "将所有材料（除装饰外）倒入摇酒器",
            "先不加冰干摇15秒",
            "加入冰块再摇15秒",
            "滤入冰镇古典杯",
            "用樱桃和橙皮装饰"
        ],
        glass=GlassType.LOWBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.CHERRY, Garnish.ORANGE_SLICE],
        flavors=[Flavor.SOUR, Flavor.SWEET],
        spirits=[SpiritType.WHISKEY],
        description="经典酸酒，蛋白增加顺滑口感",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=3
    ),
    Cocktail(
        name="Pisco Sour",
        name_zh="皮斯科酸",
        ingredients=[
            Ingredient("Pisco", 60, "ml", 40),
            Ingredient("Lime Juice", 30, "ml", 0),
            Ingredient("Simple Syrup", 20, "ml", 0),
            Ingredient("Egg White", 15, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "先不加冰干摇15秒",
            "加入冰块再摇15秒",
            "滤入冰镇古典杯",
            "滴上安哥斯图拉苦酒"
        ],
        glass=GlassType.LOWBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.CINNAMON],
        flavors=[Flavor.SOUR, Flavor.SWEET],
        spirits=[SpiritType.BRANDY],
        description="秘鲁国酒，带有独特芳香",
        origin="秘鲁/智利",
        iba_category="The Unforgettables",
        difficulty=3
    ),
    Cocktail(
        name="Sidecar",
        name_zh="侧车",
        ingredients=[
            Ingredient("Cognac", 50, "ml", 40),
            Ingredient("Cointreau", 25, "ml", 40),
            Ingredient("Lemon Juice", 25, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇马天尼杯或阔口香槟杯",
            "用橙皮装饰"
        ],
        glass=GlassType.COUPE,
        ice=IceType.CUBED,
        garnishes=[Garnish.ORANGE_TWIST],
        flavors=[Flavor.SOUR, Flavor.SWEET],
        spirits=[SpiritType.COGNAC],
        description="经典白兰地鸡尾酒",
        origin="法国",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    
    # 高球系列
    Cocktail(
        name="Mojito",
        name_zh="莫吉托",
        ingredients=[
            Ingredient("White Rum", 50, "ml", 40),
            Ingredient("Lime Juice", 25, "ml", 0),
            Ingredient("Simple Syrup", 20, "ml", 0),
            Ingredient("Mint Leaves", 8, "leaves", 0),
            Ingredient("Soda Water", 60, "ml", 0),
        ],
        instructions=[
            "将薄荷叶放入杯中轻轻捣碎",
            "加入青柠汁和糖浆",
            "加入朗姆酒",
            "加入碎冰至杯满",
            "加入苏打水",
            "用薄荷枝装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CRUSHED,
        garnishes=[Garnish.MINT],
        flavors=[Flavor.SOUR, Flavor.SWEET, Flavor.HERBAL],
        spirits=[SpiritType.RUM],
        description="古巴经典清爽鸡尾酒",
        origin="古巴",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    Cocktail(
        name="Moscow Mule",
        name_zh="莫斯科骡子",
        ingredients=[
            Ingredient("Vodka", 45, "ml", 40),
            Ingredient("Lime Juice", 15, "ml", 0),
            Ingredient("Ginger Beer", 120, "ml", 0),
        ],
        instructions=[
            "在铜杯中装满冰块",
            "加入伏特加和青柠汁",
            "加入姜啤",
            "用青柠角装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.LIME_WEDGE],
        flavors=[Flavor.SOUR, Flavor.SPICY],
        spirits=[SpiritType.VODKA],
        description="姜啤与伏特加的经典组合",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=1
    ),
    Cocktail(
        name="Gin Tonic",
        name_zh="金汤力",
        ingredients=[
            Ingredient("Gin", 50, "ml", 40),
            Ingredient("Tonic Water", 150, "ml", 0),
        ],
        instructions=[
            "在高球杯中加入冰块",
            "倒入金酒",
            "加入汤力水",
            "轻轻搅拌",
            "用青柠角装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.LIME_WEDGE],
        flavors=[Flavor.BITTER, Flavor.HERBAL],
        spirits=[SpiritType.GIN],
        description="简单经典的金酒饮品",
        origin="英国",
        iba_category="Contemporary Classics",
        difficulty=1
    ),
    Cocktail(
        name="Dark 'n' Stormy",
        name_zh="黑色风暴",
        ingredients=[
            Ingredient("Dark Rum", 60, "ml", 40),
            Ingredient("Ginger Beer", 90, "ml", 0),
            Ingredient("Lime Juice", 15, "ml", 0),
        ],
        instructions=[
            "在高球杯中加入冰块",
            "加入姜啤和青柠汁",
            "在顶部慢慢倒入黑朗姆酒",
            "用青柠角装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.LIME_WEDGE],
        flavors=[Flavor.SWEET, Flavor.SPICY],
        spirits=[SpiritType.RUM],
        description="百慕大经典，深色朗姆漂浮",
        origin="百慕大",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    Cocktail(
        name="Cuba Libre",
        name_zh="自由古巴",
        ingredients=[
            Ingredient("White Rum", 50, "ml", 40),
            Ingredient("Cola", 120, "ml", 0),
            Ingredient("Lime Juice", 10, "ml", 0),
        ],
        instructions=[
            "在高球杯中加入冰块",
            "加入朗姆酒",
            "加入可乐",
            "挤入青柠汁",
            "用青柠角装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.LIME_WEDGE],
        flavors=[Flavor.SWEET, Flavor.SOUR],
        spirits=[SpiritType.RUM],
        description="朗姆可乐，简单经典",
        origin="古巴",
        iba_category="Contemporary Classics",
        difficulty=1
    ),
    
    # 热带风情
    Cocktail(
        name="Piña Colada",
        name_zh="椰林飘香",
        ingredients=[
            Ingredient("White Rum", 60, "ml", 40),
            Ingredient("Coconut Cream", 45, "ml", 0),
            Ingredient("Pineapple Juice", 90, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入搅拌机",
            "加入碎冰",
            "搅拌至顺滑",
            "倒入飓风杯",
            "用菠萝片和樱桃装饰"
        ],
        glass=GlassType.HURRICANE,
        ice=IceType.CRUSHED,
        garnishes=[Garnish.PINEAPPLE, Garnish.CHERRY],
        flavors=[Flavor.SWEET, Flavor.CREAMY, Flavor.FRUITY],
        spirits=[SpiritType.RUM],
        description="波多黎各国饮，热带风情",
        origin="波多黎各",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    Cocktail(
        name="Mai Tai",
        name_zh="迈泰",
        ingredients=[
            Ingredient("White Rum", 30, "ml", 40),
            Ingredient("Dark Rum", 30, "ml", 40),
            Ingredient("Orange Curaçao", 15, "ml", 30),
            Ingredient("Orgeat Syrup", 15, "ml", 0),
            Ingredient("Lime Juice", 30, "ml", 0),
        ],
        instructions=[
            "将所有材料（除黑朗姆）倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入岩石杯",
            "在顶部漂浮黑朗姆酒",
            "用薄荷叶和青柠壳装饰"
        ],
        glass=GlassType.LOWBALL,
        ice=IceType.CRUSHED,
        garnishes=[Garnish.MINT, Garnish.LIME_WEDGE],
        flavors=[Flavor.SWEET, Flavor.SOUR, Flavor.FRUITY],
        spirits=[SpiritType.RUM],
        description="波利尼西亚风味，提基经典",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=3
    ),
    Cocktail(
        name="Blue Hawaii",
        name_zh="蓝色夏威夷",
        ingredients=[
            Ingredient("White Rum", 30, "ml", 40),
            Ingredient("Blue Curaçao", 30, "ml", 20),
            Ingredient("Pineapple Juice", 90, "ml", 0),
            Ingredient("Coconut Cream", 30, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入搅拌机",
            "加入碎冰",
            "搅拌至顺滑",
            "倒入飓风杯",
            "用菠萝片装饰"
        ],
        glass=GlassType.HURRICANE,
        ice=IceType.CRUSHED,
        garnishes=[Garnish.PINEAPPLE],
        flavors=[Flavor.SWEET, Flavor.FRUITY],
        spirits=[SpiritType.RUM],
        description="梦幻蓝色，热带风情",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    Cocktail(
        name="Hurricane",
        name_zh="飓风",
        ingredients=[
            Ingredient("Light Rum", 60, "ml", 40),
            Ingredient("Dark Rum", 60, "ml", 40),
            Ingredient("Passion Fruit Syrup", 30, "ml", 0),
            Ingredient("Orange Juice", 60, "ml", 0),
            Ingredient("Lime Juice", 30, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块摇晃",
            "倒入飓风杯",
            "用橙片和樱桃装饰"
        ],
        glass=GlassType.HURRICANE,
        ice=IceType.CUBED,
        garnishes=[Garnish.ORANGE_SLICE, Garnish.CHERRY],
        flavors=[Flavor.SWEET, Flavor.SOUR, Flavor.FRUITY],
        spirits=[SpiritType.RUM],
        description="新奥尔良经典，名字源于杯型",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    
    # 经典名酒
    Cocktail(
        name="Old Fashioned",
        name_zh="古典鸡尾酒",
        ingredients=[
            Ingredient("Bourbon or Rye Whiskey", 60, "ml", 40),
            Ingredient("Sugar Cube", 1, "piece", 0),
            Ingredient("Angostura Bitters", 2, "dashes", 45),
            Ingredient("Water", 1, "tsp", 0),
        ],
        instructions=[
            "将糖块放入古典杯",
            "滴上安哥斯图拉苦酒和少量水",
            "捣碎糖块直至溶解",
            "加入冰块",
            "倒入威士忌",
            "轻轻搅拌",
            "用橙皮和樱桃装饰"
        ],
        glass=GlassType.LOWBALL,
        ice=IceType.LARGE_CUBE,
        garnishes=[Garnish.ORANGE_TWIST, Garnish.CHERRY],
        flavors=[Flavor.SWEET, Flavor.BITTER],
        spirits=[SpiritType.WHISKEY],
        description="最古老的鸡尾酒之一",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=3
    ),
    Cocktail(
        name="Negroni",
        name_zh="尼格罗尼",
        ingredients=[
            Ingredient("Gin", 30, "ml", 40),
            Ingredient("Campari", 30, "ml", 25),
            Ingredient("Sweet Vermouth", 30, "ml", 16),
        ],
        instructions=[
            "将所有材料倒入调酒杯",
            "加入冰块搅拌",
            "滤入冰镇古典杯",
            "用橙皮装饰"
        ],
        glass=GlassType.LOWBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.ORANGE_TWIST],
        flavors=[Flavor.BITTER, Flavor.SWEET],
        spirits=[SpiritType.GIN],
        description="意大利经典，苦甜平衡",
        origin="意大利",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    Cocktail(
        name="Manhattan",
        name_zh="曼哈顿",
        ingredients=[
            Ingredient("Rye Whiskey", 50, "ml", 40),
            Ingredient("Sweet Vermouth", 25, "ml", 16),
            Ingredient("Angostura Bitters", 2, "dashes", 45),
        ],
        instructions=[
            "将所有材料倒入调酒杯",
            "加入冰块搅拌约30秒",
            "滤入冰镇鸡尾酒杯",
            "用樱桃装饰"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[Garnish.CHERRY],
        flavors=[Flavor.SWEET, Flavor.HERBAL],
        spirits=[SpiritType.WHISKEY],
        description="纽约经典，优雅强劲",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    Cocktail(
        name="Cosmopolitan",
        name_zh="大都会",
        ingredients=[
            Ingredient("Vodka", 40, "ml", 40),
            Ingredient("Cointreau", 15, "ml", 40),
            Ingredient("Lime Juice", 15, "ml", 0),
            Ingredient("Cranberry Juice", 30, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇马天尼杯",
            "用青柠轮或橙皮装饰"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[Garnish.LIME_WHEEL, Garnish.ORANGE_TWIST],
        flavors=[Flavor.SOUR, Flavor.SWEET, Flavor.FRUITY],
        spirits=[SpiritType.VODKA],
        description="时尚女性的最爱",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    Cocktail(
        name="Bloody Mary",
        name_zh="血腥玛丽",
        ingredients=[
            Ingredient("Vodka", 45, "ml", 40),
            Ingredient("Tomato Juice", 90, "ml", 0),
            Ingredient("Lemon Juice", 15, "ml", 0),
            Ingredient("Worcestershire Sauce", 3, "dashes", 0),
            Ingredient("Tabasco", 2, "dashes", 0),
            Ingredient("Celery Salt", 1, "pinch", 0),
            Ingredient("Black Pepper", 1, "pinch", 0),
        ],
        instructions=[
            "在高球杯中加入冰块",
            "倒入伏特加",
            "加入番茄汁和柠檬汁",
            "加入调味料",
            "搅拌均匀",
            "用芹菜杆和柠檬角装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.CELERY, Garnish.LEMON_WEDGE],
        flavors=[Flavor.SALTY, Flavor.SOUR, Flavor.SPICY, Flavor.UMAMI],
        spirits=[SpiritType.VODKA],
        description="解酒神器，咸鲜风味",
        origin="法国",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    
    # 意式经典
    Cocktail(
        name="Bellini",
        name_zh="贝利尼",
        ingredients=[
            Ingredient("Prosecco", 100, "ml", 11),
            Ingredient("White Peach Purée", 50, "ml", 0),
        ],
        instructions=[
            "将桃子果泥倒入笛形香槟杯",
            "慢慢倒入普罗赛克",
            "轻轻搅拌",
            "不需要装饰"
        ],
        glass=GlassType.FLUTE,
        ice=IceType.NONE,
        garnishes=[],
        flavors=[Flavor.SWEET, Flavor.FRUITY],
        spirits=[SpiritType.CHAMPAGNE],
        description="威尼斯经典，优雅气泡",
        origin="意大利",
        iba_category="Contemporary Classics",
        difficulty=1
    ),
    Cocktail(
        name="Negroni Sbagliato",
        name_zh="错版尼格罗尼",
        ingredients=[
            Ingredient("Campari", 30, "ml", 25),
            Ingredient("Sweet Vermouth", 30, "ml", 16),
            Ingredient("Prosecco", 30, "ml", 11),
        ],
        instructions=[
            "将金巴利和甜味美思倒入调酒杯",
            "加入冰块搅拌",
            "滤入冰镇古典杯",
            "加入普罗赛克",
            "用橙皮装饰"
        ],
        glass=GlassType.LOWBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.ORANGE_TWIST],
        flavors=[Flavor.BITTER, Flavor.SWEET],
        spirits=[SpiritType.CHAMPAGNE],
        description="尼格罗尼的气泡版本",
        origin="意大利",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    Cocktail(
        name="Americano",
        name_zh="美式鸡尾酒",
        ingredients=[
            Ingredient("Campari", 30, "ml", 25),
            Ingredient("Sweet Vermouth", 30, "ml", 16),
            Ingredient("Soda Water", 30, "ml", 0),
        ],
        instructions=[
            "将金巴利和甜味美思倒入古典杯",
            "加入冰块",
            "加入苏打水",
            "轻轻搅拌",
            "用橙皮装饰"
        ],
        glass=GlassType.LOWBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.ORANGE_TWIST],
        flavors=[Flavor.BITTER, Flavor.SWEET],
        spirits=[SpiritType.NONE],
        description="尼格罗尼的无酒精祖先",
        origin="意大利",
        iba_category="The Unforgettables",
        difficulty=1
    ),
    
    # 龙舌兰系列
    Cocktail(
        name="Tequila Sunrise",
        name_zh="龙舌兰日出",
        ingredients=[
            Ingredient("Tequila", 45, "ml", 40),
            Ingredient("Orange Juice", 90, "ml", 0),
            Ingredient("Grenadine", 15, "ml", 0),
        ],
        instructions=[
            "在高球杯中加入冰块",
            "倒入龙舌兰酒",
            "加入橙汁",
            "慢慢倒入红石榴糖浆",
            "不要搅拌",
            "用橙片和樱桃装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.ORANGE_SLICE, Garnish.CHERRY],
        flavors=[Flavor.SWEET, Flavor.FRUITY],
        spirits=[SpiritType.TEQUILA],
        description="渐变日出，视觉惊艳",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    Cocktail(
        name="Paloma",
        name_zh="帕洛玛",
        ingredients=[
            Ingredient("Tequila", 60, "ml", 40),
            Ingredient("Lime Juice", 15, "ml", 0),
            Ingredient("Grapefruit Soda", 120, "ml", 0),
        ],
        instructions=[
            "用盐边装饰高球杯",
            "加入冰块",
            "倒入龙舌兰酒和青柠汁",
            "加入西柚汽水",
            "轻轻搅拌",
            "用西柚片装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.SALT_RIM, Garnish.GRAPEFRUIT],
        flavors=[Flavor.SOUR, Flavor.BITTER],
        spirits=[SpiritType.TEQUILA],
        description="墨西哥国民鸡尾酒",
        origin="墨西哥",
        iba_category="Contemporary Classics",
        difficulty=1
    ),
    
    # 咖啡与甜品
    Cocktail(
        name="Espresso Martini",
        name_zh="浓缩咖啡马天尼",
        ingredients=[
            Ingredient("Vodka", 50, "ml", 40),
            Ingredient("Coffee Liqueur", 30, "ml", 20),
            Ingredient("Espresso", 30, "ml", 0),
            Ingredient("Simple Syrup", 10, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇马天尼杯",
            "用咖啡豆装饰"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[],
        flavors=[Flavor.BITTER, Flavor.SWEET],
        spirits=[SpiritType.VODKA],
        description="咖啡与鸡尾酒的完美融合",
        origin="英国",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    Cocktail(
        name="White Russian",
        name_zh="白色俄罗斯",
        ingredients=[
            Ingredient("Vodka", 50, "ml", 40),
            Ingredient("Coffee Liqueur", 25, "ml", 20),
            Ingredient("Heavy Cream", 25, "ml", 0),
        ],
        instructions=[
            "在古典杯中加入冰块",
            "倒入伏特加和咖啡利口酒",
            "在顶部慢慢倒入奶油",
            "不需要搅拌"
        ],
        glass=GlassType.LOWBALL,
        ice=IceType.CUBED,
        garnishes=[],
        flavors=[Flavor.SWEET, Flavor.CREAMY],
        spirits=[SpiritType.VODKA],
        description="丝滑奶油咖啡风味",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=1
    ),
    Cocktail(
        name="Irish Coffee",
        name_zh="爱尔兰咖啡",
        ingredients=[
            Ingredient("Irish Whiskey", 40, "ml", 40),
            Ingredient("Hot Coffee", 120, "ml", 0),
            Ingredient("Brown Sugar", 1, "tsp", 0),
            Ingredient("Heavy Cream", 30, "ml", 0),
        ],
        instructions=[
            "预热爱尔兰咖啡杯",
            "加入红糖和热咖啡搅拌溶解",
            "加入爱尔兰威士忌",
            "轻轻搅拌",
            "将打发奶油倒在顶部",
            "不要搅拌奶油层"
        ],
        glass=GlassType.IRISH_COFFEE,
        ice=IceType.NONE,
        garnishes=[],
        flavors=[Flavor.SWEET, Flavor.BITTER],
        spirits=[SpiritType.WHISKEY],
        description="温暖经典，咖啡与威士忌",
        origin="爱尔兰",
        iba_category="Contemporary Classics",
        difficulty=3
    ),
    Cocktail(
        name="Brandy Alexander",
        name_zh="白兰地亚力山大",
        ingredients=[
            Ingredient("Brandy", 30, "ml", 40),
            Ingredient("Crème de Cacao", 30, "ml", 20),
            Ingredient("Heavy Cream", 30, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇鸡尾酒杯",
            "撒肉豆蔻粉装饰"
        ],
        glass=GlassType.COUPE,
        ice=IceType.CUBED,
        garnishes=[Garnish.NUTMEG],
        flavors=[Flavor.SWEET, Flavor.CREAMY],
        spirits=[SpiritType.BRANDY],
        description="经典甜品鸡尾酒",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    
    # 其他经典
    Cocktail(
        name="Moscow Mule",
        name_zh="莫斯科骡子",
        ingredients=[
            Ingredient("Vodka", 45, "ml", 40),
            Ingredient("Lime Juice", 15, "ml", 0),
            Ingredient("Ginger Beer", 120, "ml", 0),
        ],
        instructions=[
            "在铜杯中装满冰块",
            "加入伏特加和青柠汁",
            "加入姜啤",
            "用青柠角装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.LIME_WEDGE],
        flavors=[Flavor.SOUR, Flavor.SPICY],
        spirits=[SpiritType.VODKA],
        description="姜啤与伏特加的经典组合",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=1
    ),
    Cocktail(
        name="Screwdriver",
        name_zh="螺丝起子",
        ingredients=[
            Ingredient("Vodka", 50, "ml", 40),
            Ingredient("Orange Juice", 100, "ml", 0),
        ],
        instructions=[
            "在高球杯中加入冰块",
            "倒入伏特加",
            "加入橙汁",
            "轻轻搅拌",
            "用橙片装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.ORANGE_SLICE],
        flavors=[Flavor.SWEET, Flavor.FRUITY],
        spirits=[SpiritType.VODKA],
        description="最简单的伏特加鸡尾酒",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=1
    ),
    Cocktail(
        name="Long Island Iced Tea",
        name_zh="长岛冰茶",
        ingredients=[
            Ingredient("Vodka", 15, "ml", 40),
            Ingredient("Gin", 15, "ml", 40),
            Ingredient("White Rum", 15, "ml", 40),
            Ingredient("Tequila", 15, "ml", 40),
            Ingredient("Triple Sec", 15, "ml", 30),
            Ingredient("Lemon Juice", 25, "ml", 0),
            Ingredient("Cola", 30, "ml", 0),
        ],
        instructions=[
            "将所有烈酒倒入高球杯",
            "加入柠檬汁",
            "加满冰块",
            "加入可乐",
            "轻轻搅拌",
            "用柠檬角装饰"
        ],
        glass=GlassType.COLLINS,
        ice=IceType.CUBED,
        garnishes=[Garnish.LEMON_WEDGE],
        flavors=[Flavor.SOUR, Flavor.SWEET],
        spirits=[SpiritType.VODKA, SpiritType.GIN, SpiritType.RUM, SpiritType.TEQUILA],
        description="强力烈酒组合，后劲十足",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    Cocktail(
        name="Sex on the Beach",
        name_zh="海滩性爱",
        ingredients=[
            Ingredient("Vodka", 40, "ml", 40),
            Ingredient("Peach Schnapps", 20, "ml", 20),
            Ingredient("Orange Juice", 40, "ml", 0),
            Ingredient("Cranberry Juice", 40, "ml", 0),
        ],
        instructions=[
            "在高球杯中加入冰块",
            "倒入伏特加和桃子利口酒",
            "加入橙汁和蔓越莓汁",
            "轻轻搅拌",
            "用橙片装饰"
        ],
        glass=GlassType.HIGHBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.ORANGE_SLICE],
        flavors=[Flavor.SWEET, Flavor.FRUITY],
        spirits=[SpiritType.VODKA],
        description="热带风味，甜蜜诱人",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=1
    ),
    Cocktail(
        name="Mimosa",
        name_zh="含羞草",
        ingredients=[
            Ingredient("Champagne", 75, "ml", 12),
            Ingredient("Orange Juice", 75, "ml", 0),
        ],
        instructions=[
            "将橙汁倒入笛形香槟杯",
            "慢慢倒入香槟",
            "轻轻搅拌",
            "不需要装饰"
        ],
        glass=GlassType.FLUTE,
        ice=IceType.NONE,
        garnishes=[],
        flavors=[Flavor.SWEET, Flavor.FRUITY],
        spirits=[SpiritType.CHAMPAGNE],
        description="早午餐经典，优雅气泡",
        origin="法国",
        iba_category="Contemporary Classics",
        difficulty=1
    ),
    Cocktail(
        name="Grasshopper",
        name_zh="绿色蚱蜢",
        ingredients=[
            Ingredient("Crème de Menthe (Green)", 30, "ml", 20),
            Ingredient("Crème de Cacao (White)", 30, "ml", 20),
            Ingredient("Heavy Cream", 30, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇鸡尾酒杯",
            "不需要装饰"
        ],
        glass=GlassType.COUPE,
        ice=IceType.CUBED,
        garnishes=[],
        flavors=[Flavor.SWEET, Flavor.CREAMY, Flavor.HERBAL],
        spirits=[SpiritType.LIQUEUR],
        description="薄荷巧克力风味甜品",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    Cocktail(
        name="B52",
        name_zh="B-52轰炸机",
        ingredients=[
            Ingredient("Kahlúa", 20, "ml", 20),
            Ingredient("Bailey's Irish Cream", 20, "ml", 17),
            Ingredient("Grand Marnier", 20, "ml", 40),
        ],
        instructions=[
            "将咖啡利口酒倒入烈酒杯",
            "用吧勺背面慢慢倒入百利甜",
            "再慢慢倒入柑曼怡",
            "可以点燃顶层后饮用"
        ],
        glass=GlassType.SHOT,
        ice=IceType.NONE,
        garnishes=[],
        flavors=[Flavor.SWEET, Flavor.CREAMY],
        spirits=[SpiritType.LIQUEUR],
        description="经典分层烈酒",
        origin="加拿大",
        iba_category="Contemporary Classics",
        difficulty=3
    ),
    Cocktail(
        name="Boulevardier",
        name_zh="林荫大道",
        ingredients=[
            Ingredient("Bourbon", 45, "ml", 40),
            Ingredient("Campari", 30, "ml", 25),
            Ingredient("Sweet Vermouth", 30, "ml", 16),
        ],
        instructions=[
            "将所有材料倒入调酒杯",
            "加入冰块搅拌约30秒",
            "滤入冰镇古典杯",
            "用橙皮装饰"
        ],
        glass=GlassType.LOWBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.ORANGE_TWIST],
        flavors=[Flavor.BITTER, Flavor.SWEET],
        spirits=[SpiritType.WHISKEY],
        description="尼格罗尼的波本变体",
        origin="美国",
        iba_category="Contemporary Classics",
        difficulty=2
    ),
    Cocktail(
        name="Paper Plane",
        name_zh="纸飞机",
        ingredients=[
            Ingredient("Bourbon", 30, "ml", 40),
            Ingredient("Aperol", 30, "ml", 11),
            Ingredient("Amaretto", 30, "ml", 24),
            Ingredient("Lemon Juice", 30, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇鸡尾酒杯",
            "用薄荷叶装饰"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[Garnish.MINT],
        flavors=[Flavor.SOUR, Flavor.SWEET, Flavor.BITTER],
        spirits=[SpiritType.WHISKEY],
        description="现代经典，平衡之美",
        origin="美国",
        iba_category="New Era Drinks",
        difficulty=2
    ),
    Cocktail(
        name="Penicillin",
        name_zh="盘尼西林",
        ingredients=[
            Ingredient("Scotch Whisky", 45, "ml", 40),
            Ingredient("Lemon Juice", 22, "ml", 0),
            Ingredient("Honey Syrup", 22, "ml", 0),
            Ingredient("Ginger Syrup", 7, "ml", 0),
            Ingredient("Peated Scotch", 10, "ml", 40, is_optional=True),
        ],
        instructions=[
            "将所有材料（除泥煤威士忌）倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇古典杯",
            "在顶部漂浮泥煤威士忌",
            "用糖渍姜片装饰"
        ],
        glass=GlassType.LOWBALL,
        ice=IceType.CUBED,
        garnishes=[Garnish.CANDY],
        flavors=[Flavor.SOUR, Flavor.SWEET, Flavor.SPICY],
        spirits=[SpiritType.WHISKEY],
        description="治愈系现代经典",
        origin="美国",
        iba_category="New Era Drinks",
        difficulty=3
    ),
    Cocktail(
        name="Last Word",
        name_zh="最后的话",
        ingredients=[
            Ingredient("Gin", 22, "ml", 40),
            Ingredient("Green Chartreuse", 22, "ml", 55),
            Ingredient("Maraschino Liqueur", 22, "ml", 30),
            Ingredient("Lime Juice", 22, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇鸡尾酒杯",
            "用樱桃装饰"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[Garnish.CHERRY],
        flavors=[Flavor.SOUR, Flavor.SWEET, Flavor.HERBAL],
        spirits=[SpiritType.GIN],
        description="禁酒时期经典复兴",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=2
    ),
    Cocktail(
        name="Corpse Reviver #2",
        name_zh="复活尸 #2",
        ingredients=[
            Ingredient("Gin", 22, "ml", 40),
            Ingredient("Cointreau", 22, "ml", 40),
            Ingredient("Lillet Blanc", 22, "ml", 17),
            Ingredient("Lemon Juice", 22, "ml", 0),
            Ingredient("Absinthe", 3, "drops", 55),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇鸡尾酒杯",
            "滴几滴苦艾酒"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[],
        flavors=[Flavor.SOUR, Flavor.SWEET, Flavor.HERBAL],
        spirits=[SpiritType.GIN],
        description="解酒经典，花香四溢",
        origin="法国",
        iba_category="The Unforgettables",
        difficulty=3
    ),
    Cocktail(
        name="Aviation",
        name_zh="飞行",
        ingredients=[
            Ingredient("Gin", 45, "ml", 40),
            Ingredient("Maraschino Liqueur", 15, "ml", 30),
            Ingredient("Crème de Violette", 15, "ml", 20),
            Ingredient("Lemon Juice", 15, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "加入冰块用力摇晃",
            "滤入冰镇鸡尾酒杯",
            "用樱桃装饰"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[Garnish.CHERRY],
        flavors=[Flavor.SOUR, Flavor.SWEET, Flavor.FRUITY],
        spirits=[SpiritType.GIN],
        description="淡紫天空，花香馥郁",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=3
    ),
    Cocktail(
        name="Clover Club",
        name_zh="三叶草俱乐部",
        ingredients=[
            Ingredient("Gin", 45, "ml", 40),
            Ingredient("Raspberry Syrup", 15, "ml", 0),
            Ingredient("Lemon Juice", 15, "ml", 0),
            Ingredient("Egg White", 15, "ml", 0),
        ],
        instructions=[
            "将所有材料倒入摇酒器",
            "先不加冰干摇15秒",
            "加入冰块再摇15秒",
            "滤入冰镇鸡尾酒杯",
            "用覆盆子装饰"
        ],
        glass=GlassType.MARTINI,
        ice=IceType.NONE,
        garnishes=[Garnish.RASPBERRY],
        flavors=[Flavor.SOUR, Flavor.SWEET, Flavor.FRUITY],
        spirits=[SpiritType.GIN],
        description="费城经典，丝滑粉红",
        origin="美国",
        iba_category="The Unforgettables",
        difficulty=3
    ),
]


# ============ 工具函数 ============

def get_all_cocktails() -> List[Cocktail]:
    """获取所有鸡尾酒配方"""
    return CLASSIC_COCKTAILS.copy()


def get_cocktail_by_name(name: str) -> Optional[Cocktail]:
    """按名称搜索鸡尾酒（支持中英文名）"""
    name_lower = name.lower()
    for cocktail in CLASSIC_COCKTAILS:
        if name_lower in cocktail.name.lower() or name_lower in cocktail.name_zh:
            return cocktail
    return None


def search_cocktails(query: str) -> List[Cocktail]:
    """搜索鸡尾酒（名称、描述、原料）"""
    query_lower = query.lower()
    results = []
    for cocktail in CLASSIC_COCKTAILS:
        # 搜索名称
        if query_lower in cocktail.name.lower() or query_lower in cocktail.name_zh:
            results.append(cocktail)
            continue
        # 搜索描述
        if query_lower in cocktail.description.lower():
            results.append(cocktail)
            continue
        # 搜索原料
        for ing in cocktail.ingredients:
            if query_lower in ing.name.lower():
                results.append(cocktail)
                break
    return results


def get_cocktails_by_spirit(spirit: SpiritType) -> List[Cocktail]:
    """按基酒类型筛选鸡尾酒"""
    return [c for c in CLASSIC_COCKTAILS if spirit in c.spirits]


def get_cocktails_by_flavor(flavor: Flavor) -> List[Cocktail]:
    """按口味筛选鸡尾酒"""
    return [c for c in CLASSIC_COCKTAILS if flavor in c.flavors]


def get_cocktails_by_glass(glass: GlassType) -> List[Cocktail]:
    """按酒杯类型筛选鸡尾酒"""
    return [c for c in CLASSIC_COCKTAILS if c.glass == glass]


def get_cocktails_by_ingredient(ingredient_name: str) -> List[Cocktail]:
    """按原料搜索鸡尾酒"""
    name_lower = ingredient_name.lower()
    results = []
    for cocktail in CLASSIC_COCKTAILS:
        for ing in cocktail.ingredients:
            if name_lower in ing.name.lower():
                results.append(cocktail)
                break
    return results


def get_random_cocktail() -> Cocktail:
    """随机获取一个鸡尾酒配方"""
    return random.choice(CLASSIC_COCKTAILS)


def get_random_cocktails(n: int = 5) -> List[Cocktail]:
    """随机获取多个鸡尾酒配方"""
    n = min(n, len(CLASSIC_COCKTAILS))
    return random.sample(CLASSIC_COCKTAILS, n)


def get_cocktails_by_abv_range(min_abv: float = 0, max_abv: float = 100) -> List[Cocktail]:
    """按酒精度范围筛选鸡尾酒"""
    return [c for c in CLASSIC_COCKTAILS if min_abv <= c.abv <= max_abv]


def get_cocktails_by_difficulty(difficulty: int) -> List[Cocktail]:
    """按难度筛选鸡尾酒 (1-5)"""
    return [c for c in CLASSIC_COCKTAILS if c.difficulty == difficulty]


def get_easy_cocktails() -> List[Cocktail]:
    """获取简单易做的鸡尾酒 (difficulty <= 2)"""
    return [c for c in CLASSIC_COCKTAILS if c.difficulty <= 2]


def get_non_alcoholic_cocktails() -> List[Cocktail]:
    """获取无酒精鸡尾酒"""
    return [c for c in CLASSIC_COCKTAILS if c.abv == 0 or SpiritType.NONE in c.spirits]


def generate_shopping_list(cocktails: List[Cocktail]) -> Dict[str, float]:
    """生成多个鸡尾酒的购物清单"""
    shopping = {}
    for cocktail in cocktails:
        for ing in cocktail.ingredients:
            if ing.is_optional:
                continue
            name = ing.name
            if name in shopping:
                shopping[name] += ing.amount
            else:
                shopping[name] = ing.amount
    return shopping


def format_shopping_list(shopping: Dict[str, float], 
                         servings: int = 1) -> str:
    """格式化购物清单为可读字符串"""
    lines = ["🛒 购物清单", "=" * 40]
    for name, amount in sorted(shopping.items()):
        total = amount * servings
        lines.append(f"  • {name}: {total:.0f}ml")
    return "\n".join(lines)


def calculate_abv(ingredients: List[Dict]) -> float:
    """
    计算混合饮料酒精度
    
    Args:
        ingredients: 原料列表，每个元素包含 name, amount_ml, abv
    
    Returns:
        酒精度百分比
    """
    total_volume = sum(ing.get("amount_ml", 0) for ing in ingredients)
    if total_volume == 0:
        return 0.0
    total_alcohol = sum(
        ing.get("amount_ml", 0) * (ing.get("abv", 0) / 100)
        for ing in ingredients
    )
    return round((total_alcohol / total_volume) * 100, 1)


def get_abv_description(abv: float) -> str:
    """获取酒精度描述"""
    if abv == 0:
        return "无酒精 🚫"
    elif abv < 5:
        return "轻度 🟢"
    elif abv < 15:
        return "中等 🟡"
    elif abv < 30:
        return "较强 🟠"
    else:
        return "烈酒 🔴"


def convert_volume(amount: float, from_unit: str, to_unit: str) -> float:
    """
    容量单位转换
    
    支持单位: ml, oz, cl, l, tbsp, tsp, dash, drop
    """
    # 转换为毫升
    to_ml = {
        "ml": 1,
        "oz": 29.5735,
        "cl": 10,
        "l": 1000,
        "tbsp": 14.7868,
        "tsp": 4.92892,
        "dash": 0.92,
        "drop": 0.05,
        "part": 30,  # 假设 1 part = 30ml
        "piece": 1,  # 块状不转换
        "leaves": 1,  # 叶片不转换
    }
    
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    if from_unit not in to_ml or to_unit not in to_ml:
        raise ValueError(f"不支持的单位: {from_unit} 或 {to_unit}")
    
    amount_in_ml = amount * to_ml[from_unit]
    return round(amount_in_ml / to_ml[to_unit], 2)


def format_recipe(cocktail: Cocktail, language: str = "zh") -> str:
    """
    格式化配方为可读字符串
    
    Args:
        cocktail: 鸡尾酒对象
        language: 语言 ("zh" 或 "en")
    """
    if language == "zh":
        lines = [
            f"🍹 {cocktail.name_zh} ({cocktail.name})",
            "=" * 40,
            f"📖 {cocktail.description}",
            f"🌍 产地: {cocktail.origin}",
            f"🥃 酒精度: {cocktail.abv}% {get_abv_description(cocktail.abv)}",
            f"⏱ 制作时间: {cocktail.prep_time}分钟",
            f"📊 难度: {'⭐' * cocktail.difficulty}",
            "",
            "📋 原料:",
        ]
        for ing in cocktail.ingredients:
            optional = " (可选)" if ing.is_optional else ""
            lines.append(f"  • {ing.name}: {ing.amount}{ing.unit}{optional}")
        
        lines.append("")
        lines.append(f"🧊 冰块: {cocktail.ice.value}")
        lines.append(f"🍷 酒杯: {cocktail.glass.value}")
        
        if cocktail.garnishes:
            garnish_names = [g.value.replace("_", " ").title() for g in cocktail.garnishes]
            lines.append(f"🍊 装饰: {', '.join(garnish_names)}")
        
        lines.append("")
        lines.append("📝 制作步骤:")
        for i, step in enumerate(cocktail.instructions, 1):
            lines.append(f"  {i}. {step}")
        
    else:  # English
        lines = [
            f"🍹 {cocktail.name}",
            "=" * 40,
            f"📖 {cocktail.description}",
            f"🌍 Origin: {cocktail.origin}",
            f"🥃 ABV: {cocktail.abv}% {get_abv_description(cocktail.abv)}",
            f"⏱ Prep Time: {cocktail.prep_time} min",
            f"📊 Difficulty: {'⭐' * cocktail.difficulty}",
            "",
            "📋 Ingredients:",
        ]
        for ing in cocktail.ingredients:
            optional = " (optional)" if ing.is_optional else ""
            lines.append(f"  • {ing.name}: {ing.amount}{ing.unit}{optional}")
        
        lines.append("")
        lines.append(f"🧊 Ice: {cocktail.ice.value}")
        lines.append(f"🍷 Glass: {cocktail.glass.value}")
        
        if cocktail.garnishes:
            garnish_names = [g.value.replace("_", " ").title() for g in cocktail.garnishes]
            lines.append(f"🍊 Garnish: {', '.join(garnish_names)}")
        
        lines.append("")
        lines.append("📝 Instructions:")
        for i, step in enumerate(cocktail.instructions, 1):
            lines.append(f"  {i}. {step}")
    
    return "\n".join(lines)


def suggest_similar_cocktails(cocktail: Cocktail, limit: int = 5) -> List[Tuple[Cocktail, float]]:
    """
    推荐相似鸡尾酒
    
    Returns:
        相似鸡尾酒列表，包含相似度分数 (0-1)
    """
    scores = []
    for other in CLASSIC_COCKTAILS:
        if other.name == cocktail.name:
            continue
        
        score = 0.0
        
        # 基酒相似度 (权重 0.4)
        common_spirits = set(cocktail.spirits) & set(other.spirits)
        all_spirits = set(cocktail.spirits) | set(other.spirits)
        if all_spirits:
            score += 0.4 * (len(common_spirits) / len(all_spirits))
        
        # 口味相似度 (权重 0.3)
        common_flavors = set(cocktail.flavors) & set(other.flavors)
        all_flavors = set(cocktail.flavors) | set(other.flavors)
        if all_flavors:
            score += 0.3 * (len(common_flavors) / len(all_flavors))
        
        # 酒精度相似度 (权重 0.15)
        abv_diff = abs(cocktail.abv - other.abv)
        score += 0.15 * max(0, 1 - abv_diff / 50)
        
        # 难度相似度 (权重 0.15)
        diff_diff = abs(cocktail.difficulty - other.difficulty)
        score += 0.15 * max(0, 1 - diff_diff / 4)
        
        scores.append((other, round(score, 2)))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:limit]


def get_iba_cocktails() -> List[Cocktail]:
    """获取所有 IBA 官方鸡尾酒"""
    return [c for c in CLASSIC_COCKTAILS if c.iba_category]


def get_cocktails_by_iba_category(category: str) -> List[Cocktail]:
    """按 IBA 分类筛选鸡尾酒"""
    return [c for c in CLASSIC_COCKTAILS if c.iba_category and category.lower() in c.iba_category.lower()]


def estimate_drinks_for_party(num_people: int, hours: int, 
                               avg_drinks_per_hour: float = 1.5) -> Dict:
    """
    估算派对所需饮料
    
    Args:
        num_people: 人数
        hours: 派对时长（小时）
        avg_drinks_per_hour: 每人每小时平均饮用量
    
    Returns:
        估算字典
    """
    total_drinks = num_people * hours * avg_drinks_per_hour
    
    # 假设每种鸡尾酒平均 120ml
    avg_cocktail_ml = 120
    total_ml = total_drinks * avg_cocktail_ml
    
    # 处理零人数边界情况
    drinks_per_person = round(total_drinks / num_people, 1) if num_people > 0 else 0
    
    return {
        "total_drinks": math.ceil(total_drinks),
        "total_ml": total_ml,
        "total_liters": round(total_ml / 1000, 1),
        "drinks_per_person": drinks_per_person,
        "suggested_cocktails": math.ceil(total_drinks / 3) if total_drinks > 0 else 0,  # 建议 3 种不同鸡尾酒
    }


def get_pairing_suggestion(dish_type: str) -> List[Cocktail]:
    """
    根据菜品类型推荐鸡尾酒
    
    Args:
        dish_type: 菜品类型 (seafood, meat, spicy, dessert, cheese, salad)
    """
    pairings = {
        "seafood": [Flavor.SOUR, Flavor.HERBAL],  # 海鲜配清爽
        "meat": [Flavor.BITTER, Flavor.SWEET],  # 肉类配浓郁
        "spicy": [Flavor.SWEET, Flavor.SOUR],  # 辛辣配甜酸
        "dessert": [Flavor.CREAMY, Flavor.SWEET],  # 甜品配奶油
        "cheese": [Flavor.BITTER, Flavor.HERBAL],  # 奶酪配苦甜
        "salad": [Flavor.SOUR, Flavor.HERBAL],  # 沙拉配清爽
        "bbq": [Flavor.SWEET, Flavor.SOUR],  # 烧烤配酸甜
        "asian": [Flavor.SOUR, Flavor.SWEET],  # 亚洲菜配酸甜
        "italian": [Flavor.BITTER, Flavor.HERBAL],  # 意大利菜配苦甜
        "mexican": [Flavor.SOUR, Flavor.SPICY],  # 墨西哥菜配酸辣
    }
    
    dish_lower = dish_type.lower()
    if dish_lower not in pairings:
        return []
    
    flavors = pairings[dish_lower]
    results = []
    for cocktail in CLASSIC_COCKTAILS:
        if any(f in cocktail.flavors for f in flavors):
            results.append(cocktail)
    return results


# 统计信息
def get_statistics() -> dict:
    """获取鸡尾酒数据库统计信息"""
    spirits_count = {}
    flavors_count = {}
    glasses_count = {}
    difficulty_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for cocktail in CLASSIC_COCKTAILS:
        for spirit in cocktail.spirits:
            spirits_count[spirit.value] = spirits_count.get(spirit.value, 0) + 1
        for flavor in cocktail.flavors:
            flavors_count[flavor.value] = flavors_count.get(flavor.value, 0) + 1
        glasses_count[cocktail.glass.value] = glasses_count.get(cocktail.glass.value, 0) + 1
        difficulty_count[cocktail.difficulty] += 1
    
    return {
        "total_cocktails": len(CLASSIC_COCKTAILS),
        "spirits_distribution": spirits_count,
        "flavors_distribution": flavors_count,
        "glasses_distribution": glasses_count,
        "difficulty_distribution": difficulty_count,
        "avg_abv": round(sum(c.abv for c in CLASSIC_COCKTAILS) / len(CLASSIC_COCKTAILS), 1),
        "iba_cocktails": len(get_iba_cocktails()),
    }


if __name__ == "__main__":
    # 简单测试
    print("🍹 Cocktail Utils 测试\n")
    
    # 获取统计
    stats = get_statistics()
    print(f"📊 数据库统计:")
    print(f"  - 总鸡尾酒数: {stats['total_cocktails']}")
    print(f"  - IBA 官方: {stats['iba_cocktails']}")
    print(f"  - 平均酒精度: {stats['avg_abv']}%")
    print()
    
    # 随机推荐
    random_cocktail = get_random_cocktail()
    print(format_recipe(random_cocktail))
    print()
    
    # 相似推荐
    similar = suggest_similar_cocktails(random_cocktail)
    print("🎯 相似推荐:")
    for cocktail, score in similar[:3]:
        print(f"  - {cocktail.name_zh} (相似度: {score})")