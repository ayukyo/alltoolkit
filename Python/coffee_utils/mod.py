"""
Coffee Utils - 咖啡冲泡工具库

提供咖啡冲泡计算、研磨度建议、冲泡时间计算等功能，零外部依赖。

功能:
- 咖啡萃取比例计算（金杯标准）
- 研磨度建议（根据冲泡方式）
- 冲泡时间和温度建议
- 咖啡因含量估算
- 咖啡种类信息
- 烘焙程度分析
- 水质影响评估
- 冲泡方式参数推荐
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum
import math


class BrewMethod(Enum):
    """冲泡方式"""
    DRIP = "drip"  # 滴滤
    FRENCH_PRESS = "french_press"  # 法压壶
    ESPRESSO = "espresso"  # 意式浓缩
    POUR_OVER = "pour_over"  # 手冲
    COLD_BREW = "cold_brew"  # 冷萃
    AEROPRESS = "aeropress"  # 爱乐压
    MOKA_POT = "moka_pot"  # 摩卡壶
    SIPHON = "siphon"  # 虹吸壶
    TURKISH = "turkish"  # 土耳其咖啡
    CHEMEX = "chemex"  # Chemex
    V60 = "v60"  # V60
    KALITA = "kalita"  # Kalita Wave


class GrindSize(Enum):
    """研磨粗细"""
    EXTRA_FINE = "extra_fine"  # 极细（面粉状）
    FINE = "fine"  # 细（食盐状）
    MEDIUM_FINE = "medium_fine"  # 中细
    MEDIUM = "medium"  # 中（海盐状）
    MEDIUM_COARSE = "medium_coarse"  # 中粗
    COARSE = "coarse"  # 粗（粗盐状）
    EXTRA_COARSE = "extra_coarse"  # 极粗


class RoastLevel(Enum):
    """烘焙程度"""
    LIGHT = "light"  # 浅烘
    LIGHT_MEDIUM = "light_medium"  # 中浅烘
    MEDIUM = "medium"  # 中烘
    MEDIUM_DARK = "medium_dark"  # 中深烘
    DARK = "dark"  # 深烘
    VERY_DARK = "very_dark"  # 极深烘


class CoffeeOrigin(Enum):
    """咖啡产地"""
    ETHIOPIA = "ethiopia"  # 埃塞俄比亚
    KENYA = "kenya"  # 肯尼亚
    COLOMBIA = "colombia"  # 哥伦比亚
    BRAZIL = "brazil"  # 巴西
    GUATEMALA = "guatemala"  # 危地马拉
    COSTA_RICA = "costa_rica"  # 哥斯达黎加
    SUMATRA = "sumatra"  # 苏门答腊
    YEMEN = "yemen"  # 也门
    JAMAICA = "jamaica"  # 牙买加
    HAWAII = "hawaii"  # 夏威夷
    PANAMA = "panama"  # 巴拿马
    INDONESIA = "indonesia"  # 印度尼西亚
    VIETNAM = "vietnam"  # 越南
    INDIA = "india"  # 印度


@dataclass
class GrindRecommendation:
    """研磨建议"""
    size: GrindSize
    description: str
    particle_size_um: Tuple[int, int]  # 微米范围
    mesh_size: Tuple[int, int]  # 筛网目数


@dataclass
class BrewParameters:
    """冲泡参数"""
    method: BrewMethod
    grind_size: GrindSize
    coffee_grams: float
    water_ml: float
    ratio: str
    temperature_c: Tuple[int, int]
    brew_time_seconds: Tuple[int, int]
    extraction_yield: Tuple[float, float]  # 萃取率范围 (%)
    tds_target: Tuple[float, float]  # TDS目标范围 (%)


@dataclass
class CaffeineInfo:
    """咖啡因信息"""
    mg_per_cup: float
    mg_per_gram: float
    sensitivity_level: str


@dataclass
class CoffeeBean:
    """咖啡豆信息"""
    origin: CoffeeOrigin
    name: str
    altitude_range: Tuple[int, int]  # 海拔范围(米)
    flavor_notes: List[str]
    acidity: str  # low, medium, high
    body: str  # light, medium, full
    processing: List[str]  # 处理方式


# 冲泡方式默认参数
BREW_PARAMETERS: Dict[BrewMethod, Dict] = {
    BrewMethod.ESPRESSO: {
        "grind": GrindSize.FINE,
        "ratio": "1:2",
        "coffee_per_shot_g": 18,
        "water_ml": 36,
        "temperature": (90, 96),
        "time": (25, 30),
        "extraction": (18, 22),
        "tds": (8, 12),
    },
    BrewMethod.POUR_OVER: {
        "grind": GrindSize.MEDIUM_FINE,
        "ratio": "1:15",
        "coffee_per_cup_g": 15,
        "water_ml": 225,
        "temperature": (90, 96),
        "time": (180, 240),
        "extraction": (18, 22),
        "tds": (1.15, 1.35),
    },
    BrewMethod.V60: {
        "grind": GrindSize.MEDIUM_FINE,
        "ratio": "1:15",
        "coffee_per_cup_g": 15,
        "water_ml": 225,
        "temperature": (91, 96),
        "time": (150, 210),
        "extraction": (18, 22),
        "tds": (1.2, 1.4),
    },
    BrewMethod.CHEMEX: {
        "grind": GrindSize.MEDIUM_COARSE,
        "ratio": "1:16",
        "coffee_per_cup_g": 15,
        "water_ml": 240,
        "temperature": (90, 96),
        "time": (240, 300),
        "extraction": (18, 22),
        "tds": (1.1, 1.3),
    },
    BrewMethod.FRENCH_PRESS: {
        "grind": GrindSize.COARSE,
        "ratio": "1:15",
        "coffee_per_cup_g": 15,
        "water_ml": 225,
        "temperature": (93, 96),
        "time": (240, 360),
        "extraction": (18, 22),
        "tds": (1.2, 1.5),
    },
    BrewMethod.COLD_BREW: {
        "grind": GrindSize.COARSE,
        "ratio": "1:8",
        "coffee_per_cup_g": 30,
        "water_ml": 240,
        "temperature": (0, 25),  # 室温或冰箱
        "time": (43200, 86400),  # 12-24小时
        "extraction": (18, 22),
        "tds": (2.5, 4.0),
    },
    BrewMethod.AEROPRESS: {
        "grind": GrindSize.MEDIUM_FINE,
        "ratio": "1:16",
        "coffee_per_cup_g": 15,
        "water_ml": 240,
        "temperature": (80, 90),
        "time": (60, 180),
        "extraction": (18, 22),
        "tds": (1.3, 1.6),
    },
    BrewMethod.MOKA_POT: {
        "grind": GrindSize.MEDIUM_FINE,
        "ratio": "1:10",
        "coffee_per_cup_g": 20,
        "water_ml": 200,
        "temperature": (95, 100),
        "time": (300, 420),
        "extraction": (18, 22),
        "tds": (2.5, 4.0),
    },
    BrewMethod.DRIP: {
        "grind": GrindSize.MEDIUM,
        "ratio": "1:16",
        "coffee_per_cup_g": 10,
        "water_ml": 160,
        "temperature": (90, 96),
        "time": (300, 420),
        "extraction": (18, 22),
        "tds": (1.1, 1.3),
    },
    BrewMethod.SIPHON: {
        "grind": GrindSize.MEDIUM,
        "ratio": "1:15",
        "coffee_per_cup_g": 15,
        "water_ml": 225,
        "temperature": (90, 95),
        "time": (60, 90),
        "extraction": (18, 22),
        "tds": (1.2, 1.4),
    },
    BrewMethod.TURKISH: {
        "grind": GrindSize.EXTRA_FINE,
        "ratio": "1:10",
        "coffee_per_cup_g": 10,
        "water_ml": 100,
        "temperature": (90, 95),
        "time": (120, 180),
        "extraction": (20, 25),
        "tds": (3.0, 5.0),
    },
    BrewMethod.KALITA: {
        "grind": GrindSize.MEDIUM,
        "ratio": "1:15",
        "coffee_per_cup_g": 15,
        "water_ml": 225,
        "temperature": (90, 96),
        "time": (180, 240),
        "extraction": (18, 22),
        "tds": (1.15, 1.35),
    },
}

# 研磨度详细信息
GRIND_SIZES: Dict[GrindSize, GrindRecommendation] = {
    GrindSize.EXTRA_FINE: GrindRecommendation(
        size=GrindSize.EXTRA_FINE,
        description="极细，面粉状质地",
        particle_size_um=(50, 150),
        mesh_size=(400, 500),
    ),
    GrindSize.FINE: GrindRecommendation(
        size=GrindSize.FINE,
        description="细，食盐状质地",
        particle_size_um=(150, 300),
        mesh_size=(200, 400),
    ),
    GrindSize.MEDIUM_FINE: GrindRecommendation(
        size=GrindSize.MEDIUM_FINE,
        description="中细，砂糖状质地",
        particle_size_um=(300, 500),
        mesh_size=(140, 200),
    ),
    GrindSize.MEDIUM: GrindRecommendation(
        size=GrindSize.MEDIUM,
        description="中等，海盐状质地",
        particle_size_um=(500, 800),
        mesh_size=(80, 140),
    ),
    GrindSize.MEDIUM_COARSE: GrindRecommendation(
        size=GrindSize.MEDIUM_COARSE,
        description="中粗，粗砂状质地",
        particle_size_um=(800, 1200),
        mesh_size=(50, 80),
    ),
    GrindSize.COARSE: GrindRecommendation(
        size=GrindSize.COARSE,
        description="粗，粗盐状质地",
        particle_size_um=(1200, 2000),
        mesh_size=(25, 50),
    ),
    GrindSize.EXTRA_COARSE: GrindRecommendation(
        size=GrindSize.EXTRA_COARSE,
        description="极粗，碎石状质地",
        particle_size_um=(2000, 3500),
        mesh_size=(10, 25),
    ),
}

# 烘焙程度特性
ROAST_CHARACTERISTICS: Dict[RoastLevel, Dict] = {
    RoastLevel.LIGHT: {
        "color": "浅棕色",
        "surface": "干燥无油",
        "flavor": "果酸明亮，花香，原产地特色突出",
        "acidity": "高",
        "body": "清淡",
        "caffeine": "高",
        "brew_temp": (88, 93),
        "notes": ["花香", "果香", "柑橘", "浆果", "茶感"],
    },
    RoastLevel.LIGHT_MEDIUM: {
        "color": "中浅棕色",
        "surface": "几乎无油",
        "flavor": "平衡的酸度与甜度，风味层次丰富",
        "acidity": "中高",
        "body": "中等",
        "caffeine": "中高",
        "brew_temp": (90, 94),
        "notes": ["蜂蜜", "焦糖", "坚果", "水果"],
    },
    RoastLevel.MEDIUM: {
        "color": "中棕色",
        "surface": "轻微出油",
        "flavor": "平衡，坚果和焦糖风味",
        "acidity": "中",
        "body": "中等到饱满",
        "caffeine": "中",
        "brew_temp": (91, 95),
        "notes": ["焦糖", "巧克力", "坚果", "香料"],
    },
    RoastLevel.MEDIUM_DARK: {
        "color": "深棕色",
        "surface": "中等出油",
        "flavor": "浓郁，苦甜平衡，烘焙风味明显",
        "acidity": "低",
        "body": "饱满",
        "caffeine": "中低",
        "brew_temp": (92, 96),
        "notes": ["黑巧克力", "烤坚果", "烟熏", "香料"],
    },
    RoastLevel.DARK: {
        "color": "深棕近黑色",
        "surface": "明显出油",
        "flavor": "浓郁苦味，烘焙和焦糖风味主导",
        "acidity": "极低",
        "body": "厚重",
        "caffeine": "低",
        "brew_temp": (93, 96),
        "notes": ["黑巧克力", "焦糖", "烟熏", "泥土"],
    },
    RoastLevel.VERY_DARK: {
        "color": "近黑色",
        "surface": "大量出油",
        "flavor": "强烈苦味，焦糖和烟熏味",
        "acidity": "无",
        "body": "厚重油润",
        "caffeine": "最低",
        "brew_temp": (94, 96),
        "notes": ["焦糖", "烟熏", "碳烤", "焦油"],
    },
}

# 咖啡产地信息
COFFEE_ORIGINS: Dict[CoffeeOrigin, CoffeeBean] = {
    CoffeeOrigin.ETHIOPIA: CoffeeBean(
        origin=CoffeeOrigin.ETHIOPIA,
        name="埃塞俄比亚",
        altitude_range=(1500, 2200),
        flavor_notes=["花香", "柑橘", "浆果", "茉莉", "桃子"],
        acidity="高",
        body="中轻",
        processing=["水洗", "日晒"],
    ),
    CoffeeOrigin.KENYA: CoffeeBean(
        origin=CoffeeOrigin.KENYA,
        name="肯尼亚",
        altitude_range=(1400, 2000),
        flavor_notes=["黑加仑", "番茄", "柑橘", "红酒", "浆果"],
        acidity="高",
        body="中等",
        processing=["水洗"],
    ),
    CoffeeOrigin.COLOMBIA: CoffeeBean(
        origin=CoffeeOrigin.COLOMBIA,
        name="哥伦比亚",
        altitude_range=(1200, 2000),
        flavor_notes=["焦糖", "坚果", "巧克力", "水果", "甜味"],
        acidity="中",
        body="中等到饱满",
        processing=["水洗"],
    ),
    CoffeeOrigin.BRAZIL: CoffeeBean(
        origin=CoffeeOrigin.BRAZIL,
        name="巴西",
        altitude_range=(800, 1600),
        flavor_notes=["坚果", "巧克力", "焦糖", "低酸", "甜味"],
        acidity="低",
        body="饱满",
        processing=["日晒", "半日晒", "水洗"],
    ),
    CoffeeOrigin.GUATEMALA: CoffeeBean(
        origin=CoffeeOrigin.GUATEMALA,
        name="危地马拉",
        altitude_range=(1300, 2000),
        flavor_notes=["巧克力", "香料", "坚果", "柑橘", "烟熏"],
        acidity="中高",
        body="饱满",
        processing=["水洗"],
    ),
    CoffeeOrigin.COSTA_RICA: CoffeeBean(
        origin=CoffeeOrigin.COSTA_RICA,
        name="哥斯达黎加",
        altitude_range=(1200, 1800),
        flavor_notes=["蜂蜜", "苹果", "柑橘", "焦糖", "甜味"],
        acidity="中高",
        body="中等",
        processing=["水洗", "蜜处理"],
    ),
    CoffeeOrigin.SUMATRA: CoffeeBean(
        origin=CoffeeOrigin.SUMATRA,
        name="苏门答腊",
        altitude_range=(750, 1500),
        flavor_notes=["泥土", "烟熏", "草本", "香料", "巧克力"],
        acidity="低",
        body="厚重",
        processing=["湿刨法"],
    ),
    CoffeeOrigin.YEMEN: CoffeeBean(
        origin=CoffeeOrigin.YEMEN,
        name="也门",
        altitude_range=(1500, 2500),
        flavor_notes=["干果", "巧克力", "香料", "烟草", "红酒"],
        acidity="中",
        body="饱满",
        processing=["日晒"],
    ),
    CoffeeOrigin.JAMAICA: CoffeeBean(
        origin=CoffeeOrigin.JAMAICA,
        name="牙买加(蓝山)",
        altitude_range=(900, 1700),
        flavor_notes=["巧克力", "坚果", "奶油", "花香", "甜味"],
        acidity="中",
        body="饱满顺滑",
        processing=["水洗"],
    ),
    CoffeeOrigin.HAWAII: CoffeeBean(
        origin=CoffeeOrigin.HAWAII,
        name="夏威夷(科纳)",
        altitude_range=(200, 800),
        flavor_notes=["坚果", "焦糖", "水果", "花香", "甜味"],
        acidity="中",
        body="中等",
        processing=["水洗"],
    ),
    CoffeeOrigin.PANAMA: CoffeeBean(
        origin=CoffeeOrigin.PANAMA,
        name="巴拿马",
        altitude_range=(1200, 2000),
        flavor_notes=["花香", "热带水果", "柑橘", "茉莉", "蜂蜜"],
        acidity="高",
        body="丝滑",
        processing=["水洗", "日晒", "蜜处理"],
    ),
    CoffeeOrigin.INDONESIA: CoffeeBean(
        origin=CoffeeOrigin.INDONESIA,
        name="印度尼西亚",
        altitude_range=(800, 1500),
        flavor_notes=["泥土", "烟熏", "草本", "香料", "黑巧克力"],
        acidity="低",
        body="厚重",
        processing=["湿刨法", "日晒"],
    ),
    CoffeeOrigin.VIETNAM: CoffeeBean(
        origin=CoffeeOrigin.VIETNAM,
        name="越南",
        altitude_range=(500, 1200),
        flavor_notes=["坚果", "巧克力", "泥土", "香料"],
        acidity="低",
        body="厚重",
        processing=["日晒", "湿法"],
    ),
    CoffeeOrigin.INDIA: CoffeeBean(
        origin=CoffeeOrigin.INDIA,
        name="印度",
        altitude_range=(800, 1600),
        flavor_notes=["香料", "坚果", "巧克力", "草本", "烟熏"],
        acidity="低",
        body="饱满",
        processing=["水洗", "日晒", "季风"],
    ),
}


class CoffeeCalculator:
    """咖啡计算器"""
    
    # 金杯标准参数
    GOLDEN_CUP_EXTRACTION_MIN = 18.0  # 最低萃取率 %
    GOLDEN_CUP_EXTRACTION_MAX = 22.0  # 最高萃取率 %
    GOLDEN_CUP_TDS_MIN = 1.15  # 最低TDS %
    GOLDEN_CUP_TDS_MAX = 1.35  # 最高TDS %
    
    @staticmethod
    def calculate_ratio(coffee_g: float, water_ml: float) -> str:
        """计算咖啡与水的比例
        
        Args:
            coffee_g: 咖啡粉重量(克)
            water_ml: 水量(毫升)
            
        Returns:
            比例字符串，如 "1:15"
        """
        if coffee_g <= 0:
            return "1:0"
        ratio = water_ml / coffee_g
        return f"1:{ratio:.1f}"
    
    @staticmethod
    def calculate_coffee_for_water(water_ml: float, ratio: str = "1:15") -> float:
        """根据水量和比例计算所需咖啡粉量
        
        Args:
            water_ml: 水量(毫升)
            ratio: 比例字符串，如 "1:15"
            
        Returns:
            咖啡粉重量(克)
        """
        try:
            parts = ratio.split(":")
            water_ratio = float(parts[1])
            return round(water_ml / water_ratio, 1)
        except (IndexError, ValueError):
            return round(water_ml / 15, 1)  # 默认1:15
    
    @staticmethod
    def calculate_water_for_coffee(coffee_g: float, ratio: str = "1:15") -> float:
        """根据咖啡粉量和比例计算所需水量
        
        Args:
            coffee_g: 咖啡粉重量(克)
            ratio: 比例字符串，如 "1:15"
            
        Returns:
            水量(毫升)
        """
        try:
            parts = ratio.split(":")
            water_ratio = float(parts[1])
            return round(coffee_g * water_ratio, 0)
        except (IndexError, ValueError):
            return round(coffee_g * 15, 0)  # 默认1:15
    
    @staticmethod
    def calculate_extraction_yield(
        coffee_g: float, 
        water_ml: float, 
        tds_percent: float
    ) -> float:
        """计算萃取率
        
        Args:
            coffee_g: 咖啡粉重量(克)
            water_ml: 水量(毫升)
            tds_percent: 溶解性总固体(TDS)百分比
            
        Returns:
            萃取率百分比
        """
        if coffee_g <= 0:
            return 0.0
        # 萃取率 = (TDS% × 液重) / 咖啡粉重 × 100
        # 假设液重 ≈ 水重 (简化计算)
        extraction = (tds_percent / 100) * water_ml / coffee_g * 100
        return round(extraction, 2)
    
    @staticmethod
    def calculate_tds(
        coffee_g: float,
        water_ml: float,
        extraction_yield_percent: float
    ) -> float:
        """根据萃取率计算TDS
        
        Args:
            coffee_g: 咖啡粉重量(克)
            water_ml: 水量(毫升)
            extraction_yield_percent: 萃取率百分比
            
        Returns:
            TDS百分比
        """
        if water_ml <= 0:
            return 0.0
        # TDS = (萃取率% × 咖啡粉重) / 液重 × 100
        tds = (extraction_yield_percent / 100) * coffee_g / water_ml * 100
        return round(tds, 2)
    
    @staticmethod
    def is_golden_cup(extraction_yield: float, tds: float) -> Dict:
        """检查是否符合金杯标准
        
        Args:
            extraction_yield: 萃取率百分比
            tds: TDS百分比
            
        Returns:
            包含评估结果的字典
        """
        extraction_ok = (
            CoffeeCalculator.GOLDEN_CUP_EXTRACTION_MIN <= 
            extraction_yield <= 
            CoffeeCalculator.GOLDEN_CUP_EXTRACTION_MAX
        )
        tds_ok = (
            CoffeeCalculator.GOLDEN_CUP_TDS_MIN <= 
            tds <= 
            CoffeeCalculator.GOLDEN_CUP_TDS_MAX
        )
        
        result = {
            "is_golden_cup": extraction_ok and tds_ok,
            "extraction": {
                "value": extraction_yield,
                "in_range": extraction_ok,
                "min": CoffeeCalculator.GOLDEN_CUP_EXTRACTION_MIN,
                "max": CoffeeCalculator.GOLDEN_CUP_EXTRACTION_MAX,
                "status": "perfect" if extraction_ok else ("under" if extraction_yield < CoffeeCalculator.GOLDEN_CUP_EXTRACTION_MIN else "over")
            },
            "tds": {
                "value": tds,
                "in_range": tds_ok,
                "min": CoffeeCalculator.GOLDEN_CUP_TDS_MIN,
                "max": CoffeeCalculator.GOLDEN_CUP_TDS_MAX,
                "status": "perfect" if tds_ok else ("weak" if tds < CoffeeCalculator.GOLDEN_CUP_TDS_MIN else "strong")
            }
        }
        
        # 调整建议
        if not extraction_ok or not tds_ok:
            suggestions = []
            if extraction_yield < CoffeeCalculator.GOLDEN_CUP_EXTRACTION_MIN:
                suggestions.append("提高萃取率: 延长萃取时间、调细研磨度、提高水温")
            elif extraction_yield > CoffeeCalculator.GOLDEN_CUP_EXTRACTION_MAX:
                suggestions.append("降低萃取率: 缩短萃取时间、调粗研磨度、降低水温")
            
            if tds < CoffeeCalculator.GOLDEN_CUP_TDS_MIN:
                suggestions.append("提高浓度: 增加咖啡粉量、减少水量")
            elif tds > CoffeeCalculator.GOLDEN_CUP_TDS_MAX:
                suggestions.append("降低浓度: 减少咖啡粉量、增加水量")
            
            result["suggestions"] = suggestions
        else:
            result["suggestions"] = ["完美！您的咖啡符合金杯标准"]
        
        return result
    
    @staticmethod
    def calculate_bloom_water(coffee_g: float, multiplier: float = 2.0) -> float:
        """计算闷蒸水量
        
        Args:
            coffee_g: 咖啡粉重量(克)
            multiplier: 水量倍数，默认2倍
            
        Returns:
            闷蒸水量(毫升)
        """
        return round(coffee_g * multiplier, 0)
    
    @staticmethod
    def calculate_bloom_time(roast_level: RoastLevel) -> int:
        """根据烘焙程度建议闷蒸时间
        
        Args:
            roast_level: 烘焙程度
            
        Returns:
            闷蒸时间(秒)
        """
        bloom_times = {
            RoastLevel.LIGHT: 45,
            RoastLevel.LIGHT_MEDIUM: 40,
            RoastLevel.MEDIUM: 35,
            RoastLevel.MEDIUM_DARK: 30,
            RoastLevel.DARK: 25,
            RoastLevel.VERY_DARK: 20,
        }
        return bloom_times.get(roast_level, 30)


class CaffeineCalculator:
    """咖啡因计算器"""
    
    # 不同冲泡方式的咖啡因含量 (mg/g 咖啡粉)
    CAFFEINE_PER_GRAM: Dict[BrewMethod, float] = {
        BrewMethod.ESPRESSO: 12.0,
        BrewMethod.POUR_OVER: 10.0,
        BrewMethod.V60: 10.0,
        BrewMethod.CHEMEX: 9.5,
        BrewMethod.FRENCH_PRESS: 11.0,
        BrewMethod.COLD_BREW: 14.0,
        BrewMethod.AEROPRESS: 11.0,
        BrewMethod.MOKA_POT: 13.0,
        BrewMethod.DRIP: 10.0,
        BrewMethod.SIPHON: 10.0,
        BrewMethod.TURKISH: 15.0,
        BrewMethod.KALITA: 10.0,
    }
    
    # 不同烘焙程度的咖啡因系数
    ROAST_CAFFEINE_FACTOR: Dict[RoastLevel, float] = {
        RoastLevel.LIGHT: 1.1,
        RoastLevel.LIGHT_MEDIUM: 1.05,
        RoastLevel.MEDIUM: 1.0,
        RoastLevel.MEDIUM_DARK: 0.95,
        RoastLevel.DARK: 0.9,
        RoastLevel.VERY_DARK: 0.85,
    }
    
    @staticmethod
    def estimate_caffeine(
        coffee_g: float,
        brew_method: BrewMethod,
        roast_level: RoastLevel = RoastLevel.MEDIUM
    ) -> CaffeineInfo:
        """估算咖啡因含量
        
        Args:
            coffee_g: 咖啡粉重量(克)
            brew_method: 冲泡方式
            roast_level: 烘焙程度
            
        Returns:
            咖啡因信息
        """
        base_caffeine = CaffeineCalculator.CAFFEINE_PER_GRAM.get(brew_method, 10.0)
        roast_factor = CaffeineCalculator.ROAST_CAFFEINE_FACTOR.get(roast_level, 1.0)
        
        mg_per_gram = base_caffeine * roast_factor
        total_mg = coffee_g * mg_per_gram
        
        # 敏感度评估
        if total_mg < 50:
            sensitivity = "低"
        elif total_mg < 100:
            sensitivity = "中低"
        elif total_mg < 200:
            sensitivity = "中等"
        elif total_mg < 300:
            sensitivity = "中高"
        else:
            sensitivity = "高"
        
        return CaffeineInfo(
            mg_per_cup=round(total_mg, 1),
            mg_per_gram=round(mg_per_gram, 2),
            sensitivity_level=sensitivity
        )
    
    @staticmethod
    def daily_limit_check(total_mg: float, limit_mg: float = 400.0) -> Dict:
        """检查每日咖啡因摄入限制
        
        Args:
            total_mg: 已摄入咖啡因(mg)
            limit_mg: 每日限制(mg)，默认400mg
            
        Returns:
            检查结果字典
        """
        remaining = limit_mg - total_mg
        percent = (total_mg / limit_mg) * 100
        
        return {
            "consumed_mg": total_mg,
            "limit_mg": limit_mg,
            "remaining_mg": round(remaining, 1),
            "percentage": round(percent, 1),
            "status": "safe" if percent < 70 else ("caution" if percent < 100 else "exceeded"),
            "cups_remaining": {
                "espresso": max(0, int(remaining / 63)),
                "drip": max(0, int(remaining / 95)),
                "cold_brew": max(0, int(remaining / 120)),
            }
        }
    
    @staticmethod
    def half_life_hours(
        current_mg: float,
        target_mg: float,
        half_life_hours: float = 5.0
    ) -> float:
        """计算咖啡因代谢到目标量所需时间
        
        Args:
            current_mg: 当前咖啡因量(mg)
            target_mg: 目标咖啡因量(mg)
            half_life_hours: 半衰期(小时)，默认5小时
            
        Returns:
            所需小时数
        """
        if current_mg <= target_mg:
            return 0.0
        
        import math
        # N = N0 * (1/2)^(t/half_life)
        # t = half_life * log2(N0/N)
        hours = half_life_hours * math.log2(current_mg / target_mg)
        return round(hours, 1)


class BrewRecommender:
    """冲泡推荐器"""
    
    @staticmethod
    def get_brew_parameters(method: BrewMethod) -> BrewParameters:
        """获取冲泡方式的推荐参数
        
        Args:
            method: 冲泡方式
            
        Returns:
            冲泡参数
        """
        params = BREW_PARAMETERS.get(method, BREW_PARAMETERS[BrewMethod.POUR_OVER])
        grind = params["grind"]
        
        # 兼容两种键名: coffee_per_cup_g 或 coffee_per_shot_g
        coffee_g = params.get("coffee_per_cup_g", params.get("coffee_per_shot_g", 15))
        
        return BrewParameters(
            method=method,
            grind_size=grind,
            coffee_grams=coffee_g,
            water_ml=params["water_ml"],
            ratio=params["ratio"],
            temperature_c=params["temperature"],
            brew_time_seconds=params["time"],
            extraction_yield=params["extraction"],
            tds_target=params["tds"],
        )
    
    @staticmethod
    def get_grind_recommendation(grind_size: GrindSize) -> GrindRecommendation:
        """获取研磨度详细信息
        
        Args:
            grind_size: 研磨粗细
            
        Returns:
            研磨建议
        """
        return GRIND_SIZES.get(grind_size, GRIND_SIZES[GrindSize.MEDIUM])
    
    @staticmethod
    def recommend_for_cups(
        method: BrewMethod,
        num_cups: int = 1,
        cup_size_ml: float = 240
    ) -> Dict:
        """为多杯咖啡推荐参数
        
        Args:
            method: 冲泡方式
            num_cups: 杯数
            cup_size_ml: 每杯容量(ml)
            
        Returns:
            推荐参数字典
        """
        base = BREW_PARAMETERS.get(method, BREW_PARAMETERS[BrewMethod.POUR_OVER])
        total_water = cup_size_ml * num_cups
        
        # 解析比例
        ratio_parts = base["ratio"].split(":")
        water_ratio = float(ratio_parts[1])
        
        total_coffee = round(total_water / water_ratio, 1)
        
        return {
            "method": method.value,
            "cups": num_cups,
            "total_water_ml": total_water,
            "total_coffee_g": total_coffee,
            "grind": base["grind"].value,
            "ratio": base["ratio"],
            "temperature_c": base["temperature"],
            "brew_time_seconds": base["time"],
            "bloom_water_ml": round(total_coffee * 2, 0),
            "bloom_time_seconds": 30,
        }
    
    @staticmethod
    def adjust_for_taste(
        method: BrewMethod,
        taste_preference: str
    ) -> Dict:
        """根据口味偏好调整参数
        
        Args:
            method: 冲泡方式
            taste_preference: 口味偏好 ("stronger", "weaker", "balanced")
            
        Returns:
            调整后的参数
        """
        base = BrewRecommender.get_brew_parameters(method)
        
        if taste_preference == "stronger":
            # 更浓: 增加咖啡量，提高水温，延长时间
            return {
                "coffee_grams": round(base.coffee_grams * 1.15, 1),
                "water_ml": base.water_ml,
                "ratio": f"1:{round(base.water_ml / (base.coffee_grams * 1.15), 0):.0f}",
                "temperature_c": (
                    min(base.temperature_c[0] + 2, 96),
                    min(base.temperature_c[1] + 2, 98)
                ),
                "brew_time_seconds": (
                    base.brew_time_seconds[0] + 15,
                    base.brew_time_seconds[1] + 30
                ),
                "notes": "增加咖啡量15%，水温提高2°C，时间延长15-30秒"
            }
        elif taste_preference == "weaker":
            # 更淡: 减少咖啡量，降低水温，缩短时间
            return {
                "coffee_grams": round(base.coffee_grams * 0.85, 1),
                "water_ml": base.water_ml,
                "ratio": f"1:{round(base.water_ml / (base.coffee_grams * 0.85), 0):.0f}",
                "temperature_c": (
                    max(base.temperature_c[0] - 2, 85),
                    max(base.temperature_c[1] - 2, 92)
                ),
                "brew_time_seconds": (
                    max(base.brew_time_seconds[0] - 15, 60),
                    max(base.brew_time_seconds[1] - 30, 90)
                ),
                "notes": "减少咖啡量15%，水温降低2°C，时间缩短15-30秒"
            }
        else:
            # 平衡，使用默认参数
            return {
                "coffee_grams": base.coffee_grams,
                "water_ml": base.water_ml,
                "ratio": base.ratio,
                "temperature_c": base.temperature_c,
                "brew_time_seconds": base.brew_time_seconds,
                "notes": "使用标准金杯参数"
            }


class WaterQualityAnalyzer:
    """水质分析器"""
    
    # 理想水质参数
    IDEAL_HARDNESS = (50, 175)  # ppm CaCO3
    IDEAL_PH = (6.5, 7.5)
    IDEAL_ALKALINITY = (40, 75)  # ppm
    
    @staticmethod
    def assess_water(
        hardness_ppm: float,
        ph: float,
        alkalinity_ppm: float = None
    ) -> Dict:
        """评估水质
        
        Args:
            hardness_ppm: 硬度(ppm CaCO3)
            ph: pH值
            alkalinity_ppm: 碱度(ppm)，可选
            
        Returns:
            评估结果
        """
        # 硬度评估
        if hardness_ppm < 50:
            hardness_status = "soft"
            hardness_note = "水太软，可能导致萃取过度，咖啡偏苦"
        elif hardness_ppm > 175:
            hardness_status = "hard"
            hardness_note = "水太硬，可能导致萃取不足，咖啡平淡"
        else:
            hardness_status = "ideal"
            hardness_note = "硬度理想，有助于平衡萃取"
        
        # pH评估
        if ph < 6.5:
            ph_status = "acidic"
            ph_note = "酸性水可能使咖啡偏酸"
        elif ph > 7.5:
            ph_status = "alkaline"
            ph_note = "碱性水可能使咖啡偏苦"
        else:
            ph_status = "ideal"
            ph_note = "pH理想，有助于风味平衡"
        
        result = {
            "hardness": {
                "value": hardness_ppm,
                "status": hardness_status,
                "ideal_range": WaterQualityAnalyzer.IDEAL_HARDNESS,
                "note": hardness_note,
            },
            "ph": {
                "value": ph,
                "status": ph_status,
                "ideal_range": WaterQualityAnalyzer.IDEAL_PH,
                "note": ph_note,
            },
            "overall": "good" if (hardness_status == "ideal" and ph_status == "ideal") else "needs_adjustment",
        }
        
        # 碱度评估（如果提供）
        if alkalinity_ppm is not None:
            if alkalinity_ppm < 40:
                alk_status = "low"
                alk_note = "碱度过低，可能导致pH不稳定"
            elif alkalinity_ppm > 75:
                alk_status = "high"
                alk_note = "碱度过高，可能抑制酸度"
            else:
                alk_status = "ideal"
                alk_note = "碱度理想"
            
            result["alkalinity"] = {
                "value": alkalinity_ppm,
                "status": alk_status,
                "ideal_range": WaterQualityAnalyzer.IDEAL_ALKALINITY,
                "note": alk_note,
            }
        
        # 建议
        suggestions = []
        if hardness_status == "soft":
            suggestions.append("考虑使用矿泉水或添加矿物质")
        elif hardness_status == "hard":
            suggestions.append("考虑使用过滤水或纯净水")
        
        if ph_status == "acidic":
            suggestions.append("可考虑使用中性滤水器")
        elif ph_status == "alkaline":
            suggestions.append("可考虑使用反渗透水或酸性矿物调节")
        
        result["suggestions"] = suggestions if suggestions else ["水质适合冲泡咖啡"]
        
        return result
    
    @staticmethod
    def magnesium_benefit(hardness_ppm: float) -> Dict:
        """评估镁含量对咖啡的影响
        
        Args:
            hardness_ppm: 硬度(ppm)
            
        Returns:
            镁益处评估
        """
        # 镁离子有助于提取水果风味和酸度
        # 理想镁含量约 20-50 ppm
        if hardness_ppm < 20:
            return {
                "magnesium_level": "low",
                "effect": "缺乏镁离子可能导致风味平淡",
                "recommendation": "可添加镁盐提升水果风味",
            }
        elif hardness_ppm > 100:
            return {
                "magnesium_level": "high",
                "effect": "过多镁离子可能导致过度萃取",
                "recommendation": "考虑稀释或使用混合水",
            }
        else:
            return {
                "magnesium_level": "optimal",
                "effect": "镁含量有助于提取水果和花香风味",
                "recommendation": "保持当前水质",
            }


class RoastAnalyzer:
    """烘焙分析器"""
    
    @staticmethod
    def get_roast_characteristics(roast_level: RoastLevel) -> Dict:
        """获取烘焙程度特性
        
        Args:
            roast_level: 烘焙程度
            
        Returns:
            烘焙特性字典
        """
        return ROAST_CHARACTERISTICS.get(roast_level, ROAST_CHARACTERISTICS[RoastLevel.MEDIUM])
    
    @staticmethod
    def recommend_brew_temp(roast_level: RoastLevel) -> Tuple[int, int]:
        """根据烘焙程度推荐冲泡温度
        
        Args:
            roast_level: 烘焙程度
            
        Returns:
            温度范围(°C)
        """
        chars = ROAST_CHARACTERISTICS.get(roast_level, ROAST_CHARACTERISTICS[RoastLevel.MEDIUM])
        return chars["brew_temp"]
    
    @staticmethod
    def suggest_origin_for_roast(roast_level: RoastLevel) -> List[CoffeeOrigin]:
        """根据烘焙程度推荐咖啡产地
        
        Args:
            roast_level: 烘焙程度
            
        Returns:
            推荐产地列表
        """
        recommendations = {
            RoastLevel.LIGHT: [
                CoffeeOrigin.ETHIOPIA,
                CoffeeOrigin.KENYA,
                CoffeeOrigin.PANAMA,
                CoffeeOrigin.COSTA_RICA,
            ],
            RoastLevel.LIGHT_MEDIUM: [
                CoffeeOrigin.ETHIOPIA,
                CoffeeOrigin.COLOMBIA,
                CoffeeOrigin.COSTA_RICA,
                CoffeeOrigin.GUATEMALA,
            ],
            RoastLevel.MEDIUM: [
                CoffeeOrigin.COLOMBIA,
                CoffeeOrigin.BRAZIL,
                CoffeeOrigin.COSTA_RICA,
                CoffeeOrigin.JAMAICA,
            ],
            RoastLevel.MEDIUM_DARK: [
                CoffeeOrigin.SUMATRA,
                CoffeeOrigin.INDONESIA,
                CoffeeOrigin.BRAZIL,
                CoffeeOrigin.INDIA,
            ],
            RoastLevel.DARK: [
                CoffeeOrigin.SUMATRA,
                CoffeeOrigin.INDONESIA,
                CoffeeOrigin.VIETNAM,
                CoffeeOrigin.INDIA,
            ],
            RoastLevel.VERY_DARK: [
                CoffeeOrigin.VIETNAM,
                CoffeeOrigin.INDONESIA,
                CoffeeOrigin.INDIA,
            ],
        }
        return recommendations.get(roast_level, recommendations[RoastLevel.MEDIUM])


class OriginInfo:
    """产地信息查询"""
    
    @staticmethod
    def get_origin_info(origin: CoffeeOrigin) -> CoffeeBean:
        """获取咖啡产地信息
        
        Args:
            origin: 咖啡产地
            
        Returns:
            咖啡豆信息
        """
        return COFFEE_ORIGINS.get(origin, COFFEE_ORIGINS[CoffeeOrigin.BRAZIL])
    
    @staticmethod
    def search_by_flavor(flavor_note: str) -> List[CoffeeOrigin]:
        """根据风味特征搜索产地
        
        Args:
            flavor_note: 风味描述（如"巧克力"、"水果"、"花香"）
            
        Returns:
            匹配的产地列表
        """
        matching = []
        flavor_lower = flavor_note.lower()
        
        for origin, bean in COFFEE_ORIGINS.items():
            for note in bean.flavor_notes:
                if flavor_lower in note.lower():
                    matching.append(origin)
                    break
        
        return matching
    
    @staticmethod
    def search_by_acidity(acidity_level: str) -> List[CoffeeOrigin]:
        """根据酸度搜索产地
        
        Args:
            acidity_level: 酸度等级 ("low"/"低", "medium"/"中", "high"/"高")
            
        Returns:
            匹配的产地列表
        """
        matching = []
        # 支持英文和中文
        acidity_mapping = {
            "low": ["低", "low"],
            "medium": ["中", "中高", "medium"],
            "high": ["高", "中高", "high"],
        }
        
        target_terms = acidity_mapping.get(acidity_level.lower(), [acidity_level])
        
        for origin, bean in COFFEE_ORIGINS.items():
            for term in target_terms:
                if term.lower() in bean.acidity.lower():
                    matching.append(origin)
                    break
        
        return matching
    
    @staticmethod
    def search_by_body(body_level: str) -> List[CoffeeOrigin]:
        """根据醇厚度搜索产地
        
        Args:
            body_level: 醇厚度等级 ("light", "medium", "full")
            
        Returns:
            匹配的产地列表
        """
        matching = []
        body_mapping = {
            "light": ["轻", "中轻", "清淡"],
            "medium": ["中", "中等"],
            "full": ["饱满", "厚重", "厚"],
        }
        
        target_terms = body_mapping.get(body_level.lower(), [])
        
        for origin, bean in COFFEE_ORIGINS.items():
            for term in target_terms:
                if term in bean.body:
                    matching.append(origin)
                    break
        
        return matching


# 便捷函数
def calculate_ratio(coffee_g: float, water_ml: float) -> str:
    """计算咖啡与水的比例"""
    return CoffeeCalculator.calculate_ratio(coffee_g, water_ml)


def estimate_caffeine(coffee_g: float, method: str = "pour_over") -> CaffeineInfo:
    """估算咖啡因含量"""
    brew_method = BrewMethod(method) if method in [m.value for m in BrewMethod] else BrewMethod.POUR_OVER
    return CaffeineCalculator.estimate_caffeine(coffee_g, brew_method)


def get_brew_recipe(method: str, cups: int = 1) -> Dict:
    """获取冲泡配方"""
    brew_method = BrewMethod(method) if method in [m.value for m in BrewMethod] else BrewMethod.POUR_OVER
    return BrewRecommender.recommend_for_cups(brew_method, cups)


def golden_cup_check(coffee_g: float, water_ml: float, tds: float) -> Dict:
    """检查是否符合金杯标准"""
    extraction = CoffeeCalculator.calculate_extraction_yield(coffee_g, water_ml, tds)
    return CoffeeCalculator.is_golden_cup(extraction, tds)


def search_coffee_by_flavor(flavor: str) -> List[str]:
    """根据风味搜索咖啡产地"""
    origins = OriginInfo.search_by_flavor(flavor)
    return [COFFEE_ORIGINS[o].name for o in origins]


if __name__ == "__main__":
    # 示例用法
    print("=== 咖啡冲泡工具库 ===\n")
    
    # 计算比例
    print("1. 计算咖啡比例:")
    ratio = calculate_ratio(15, 225)
    print(f"   15g咖啡 + 225ml水 = {ratio}")
    
    # 获取冲泡参数
    print("\n2. V60冲泡参数:")
    recipe = get_brew_recipe("v60", 2)
    for key, value in recipe.items():
        print(f"   {key}: {value}")
    
    # 估算咖啡因
    print("\n3. 咖啡因估算:")
    caffeine = estimate_caffeine(18, "espresso")
    print(f"   双份浓缩(18g): {caffeine.mg_per_cup}mg 咖啡因")
    
    # 金杯检查
    print("\n4. 金杯标准检查:")
    check = golden_cup_check(15, 225, 1.25)
    print(f"   TDS 1.25%: {check['is_golden_cup']}")
    
    # 风味搜索
    print("\n5. 搜索巧克力风味的咖啡:")
    origins = search_coffee_by_flavor("巧克力")
    print(f"   匹配产地: {', '.join(origins)}")