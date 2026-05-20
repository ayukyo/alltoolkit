"""
plant_care_utils - 植物养护工具

功能：
- 植物信息管理和养护追踪
- 浇水频率计算（基于植物类型、季节、环境）
- 施肥计划和提醒
- 日照需求分析
- 植物生长阶段管理
- 季节性养护建议
- 植物健康状态评估
- 零外部依赖
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum
import math


class PlantType(Enum):
    """植物类型枚举"""
    SUCCULENT = "succulent"  # 多肉植物
    TROPICAL = "tropical"  # 热带植物
    FERN = "fern"  # 蕨类植物
    CACTUS = "cactus"  # 仙人掌
    FLOWERING = "flowering"  # 开花植物
    FOLIAGE = "foliage"  # 观叶植物
    HERB = "herb"  # 草本植物
    VEGETABLE = "vegetable"  # 蔬菜
    FRUIT = "fruit"  # 水果
    TREE = "tree"  # 树木
    PALM = "palm"  # 棕榈
    ORCHID = "orchid"  # 兰花
    BONSAI = "bonsai"  # 盆景


class Season(Enum):
    """季节枚举"""
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"


class LightLevel(Enum):
    """光照强度枚举"""
    LOW = "low"  # 低光照（<1000 lux）
    MEDIUM = "medium"  # 中等光照（1000-2500 lux）
    BRIGHT = "bright"  # 明亮光照（2500-10000 lux）
    DIRECT = "direct"  # 直射阳光（>10000 lux）


class WaterFrequency(Enum):
    """浇水频率枚举"""
    RARELY = "rarely"  # 很少（每2-4周）
    INFREQUENT = "infrequent"  # 不频繁（每1-2周）
    MODERATE = "moderate"  # 适中（每周）
    FREQUENT = "frequent"  # 频繁（每3-4天）
    VERY_FREQUENT = "very_frequent"  # 非常频繁（每天）


class HealthStatus(Enum):
    """健康状态枚举"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class GrowthStage(Enum):
    """生长阶段枚举"""
    SEED = "seed"  # 种子期
    SEEDLING = "seedling"  # 幼苗期
    VEGETATIVE = "vegetative"  # 营养生长期
    BUDDING = "budding"  # 花蕾期
    FLOWERING = "flowering"  # 开花期
    FRUITING = "fruiting"  # 结果期
    DORMANT = "dormant"  # 休眠期
    MATURE = "mature"  # 成熟期


# 植物基础信息数据库
PLANT_DATABASE = {
    PlantType.SUCCULENT: {
        "name": "多肉植物",
        "water_frequency": WaterFrequency.INFREQUENT,
        "light_requirement": LightLevel.BRIGHT,
        "humidity_range": (30, 50),
        "temperature_range": (15, 30),
        "fertilizer_frequency_days": 60,
        "common_issues": ["过度浇水", "日照不足", "根部腐烂"],
        "care_tips": ["排水良好的土壤", "避免叶面浇水", "冬季减少浇水"]
    },
    PlantType.TROPICAL: {
        "name": "热带植物",
        "water_frequency": WaterFrequency.MODERATE,
        "light_requirement": LightLevel.MEDIUM,
        "humidity_range": (60, 80),
        "temperature_range": (18, 30),
        "fertilizer_frequency_days": 30,
        "common_issues": ["叶尖枯黄", "低温伤害", "红蜘蛛"],
        "care_tips": ["定期喷水增湿", "避免空调直吹", "保持土壤湿润"]
    },
    PlantType.FERN: {
        "name": "蕨类植物",
        "water_frequency": WaterFrequency.FREQUENT,
        "light_requirement": LightLevel.LOW,
        "humidity_range": (70, 90),
        "temperature_range": (15, 25),
        "fertilizer_frequency_days": 45,
        "common_issues": ["叶尖干枯", "湿度不足", "阳光灼伤"],
        "care_tips": ["高湿度环境", "间接光线", "保持土壤湿润"]
    },
    PlantType.CACTUS: {
        "name": "仙人掌",
        "water_frequency": WaterFrequency.RARELY,
        "light_requirement": LightLevel.DIRECT,
        "humidity_range": (10, 30),
        "temperature_range": (10, 35),
        "fertilizer_frequency_days": 90,
        "common_issues": ["过度浇水", "根部腐烂", "缺乏阳光"],
        "care_tips": ["排水良好的沙质土壤", "冬季休眠期停止浇水", "充足阳光"]
    },
    PlantType.FLOWERING: {
        "name": "开花植物",
        "water_frequency": WaterFrequency.MODERATE,
        "light_requirement": LightLevel.BRIGHT,
        "humidity_range": (40, 60),
        "temperature_range": (15, 25),
        "fertilizer_frequency_days": 21,
        "common_issues": ["花苞脱落", "花期短", "养分不足"],
        "care_tips": ["花期增加磷肥", "摘除残花", "充足光照"]
    },
    PlantType.FOLIAGE: {
        "name": "观叶植物",
        "water_frequency": WaterFrequency.MODERATE,
        "light_requirement": LightLevel.MEDIUM,
        "humidity_range": (50, 70),
        "temperature_range": (18, 28),
        "fertilizer_frequency_days": 30,
        "common_issues": ["叶边枯黄", "叶片褪色", "叶斑病"],
        "care_tips": ["定期擦拭叶片", "适度光照", "避免积水"]
    },
    PlantType.HERB: {
        "name": "草本植物",
        "water_frequency": WaterFrequency.FREQUENT,
        "light_requirement": LightLevel.BRIGHT,
        "humidity_range": (40, 60),
        "temperature_range": (15, 28),
        "fertilizer_frequency_days": 21,
        "common_issues": ["徒长", "根系受限", "虫害"],
        "care_tips": ["充足阳光", "定期修剪", "良好排水"]
    },
    PlantType.VEGETABLE: {
        "name": "蔬菜",
        "water_frequency": WaterFrequency.FREQUENT,
        "light_requirement": LightLevel.BRIGHT,
        "humidity_range": (50, 70),
        "temperature_range": (15, 30),
        "fertilizer_frequency_days": 14,
        "common_issues": ["虫害", "营养不足", "日照不足"],
        "care_tips": ["定期施肥", "充足日照", "保持土壤湿润"]
    },
    PlantType.FRUIT: {
        "name": "水果植物",
        "water_frequency": WaterFrequency.MODERATE,
        "light_requirement": LightLevel.BRIGHT,
        "humidity_range": (50, 70),
        "temperature_range": (15, 30),
        "fertilizer_frequency_days": 21,
        "common_issues": ["落果", "授粉不足", "病虫害"],
        "care_tips": ["人工授粉", "结果期增施钾肥", "充足阳光"]
    },
    PlantType.TREE: {
        "name": "树木",
        "water_frequency": WaterFrequency.INFREQUENT,
        "light_requirement": LightLevel.BRIGHT,
        "humidity_range": (40, 60),
        "temperature_range": (10, 35),
        "fertilizer_frequency_days": 90,
        "common_issues": ["根系受限", "叶黄", "虫害"],
        "care_tips": ["定期换盆", "修剪整形", "深层浇水"]
    },
    PlantType.PALM: {
        "name": "棕榈",
        "water_frequency": WaterFrequency.MODERATE,
        "light_requirement": LightLevel.BRIGHT,
        "humidity_range": (50, 70),
        "temperature_range": (18, 30),
        "fertilizer_frequency_days": 45,
        "common_issues": ["叶尖枯黄", "红蜘蛛", "低温伤害"],
        "care_tips": ["定期清洁叶片", "避免积水", "温暖环境"]
    },
    PlantType.ORCHID: {
        "name": "兰花",
        "water_frequency": WaterFrequency.INFREQUENT,
        "light_requirement": LightLevel.MEDIUM,
        "humidity_range": (60, 80),
        "temperature_range": (18, 28),
        "fertilizer_frequency_days": 21,
        "common_issues": ["根部腐烂", "叶片发黄", "不开花"],
        "care_tips": ["透气介质", "高湿度", "适度遮阴"]
    },
    PlantType.BONSAI: {
        "name": "盆景",
        "water_frequency": WaterFrequency.FREQUENT,
        "light_requirement": LightLevel.BRIGHT,
        "humidity_range": (40, 60),
        "temperature_range": (10, 30),
        "fertilizer_frequency_days": 30,
        "common_issues": ["积水", "修剪过度", "根系老化"],
        "care_tips": ["精细浇水", "定期修剪", "换盆更新"]
    }
}


class Plant:
    """植物类"""
    
    def __init__(
        self,
        name: str,
        plant_type: PlantType,
        location: str = "室内",
        purchase_date: Optional[datetime] = None,
        last_watered: Optional[datetime] = None,
        last_fertilized: Optional[datetime] = None,
        notes: str = ""
    ):
        """
        初始化植物
        
        Args:
            name: 植物名称
            plant_type: 植物类型
            location: 位置（室内/室外/阳台等）
            purchase_date: 购买日期
            last_watered: 上次浇水日期
            last_fertilized: 上次施肥日期
            notes: 备注
        """
        self.name = name
        self.plant_type = plant_type
        self.location = location
        self.purchase_date = purchase_date or datetime.now()
        self.last_watered = last_watered
        self.last_fertilized = last_fertilized
        self.notes = notes
        self.health_history: List[Dict[str, Any]] = []
        self.care_log: List[Dict[str, Any]] = []
        
    def get_info(self) -> Dict[str, Any]:
        """获取植物基础信息"""
        info = PLANT_DATABASE.get(self.plant_type, {})
        return {
            "name": self.name,
            "type": self.plant_type.value,
            "type_name": info.get("name", "未知"),
            "location": self.location,
            "age_days": (datetime.now() - self.purchase_date).days,
            "purchase_date": self.purchase_date.strftime("%Y-%m-%d") if self.purchase_date else None,
            "last_watered": self.last_watered.strftime("%Y-%m-%d %H:%M") if self.last_watered else None,
            "last_fertilized": self.last_fertilized.strftime("%Y-%m-%d") if self.last_fertilized else None,
            "notes": self.notes
        }
    
    def record_watering(self, date: Optional[datetime] = None, amount_ml: Optional[int] = None):
        """记录浇水"""
        date = date or datetime.now()
        self.last_watered = date
        self.care_log.append({
            "action": "watering",
            "date": date,
            "amount_ml": amount_ml
        })
    
    def record_fertilizing(self, date: Optional[datetime] = None, fertilizer_type: str = "复合肥"):
        """记录施肥"""
        date = date or datetime.now()
        self.last_fertilized = date
        self.care_log.append({
            "action": "fertilizing",
            "date": date,
            "fertilizer_type": fertilizer_type
        })
    
    def record_health_check(self, status: HealthStatus, notes: str = ""):
        """记录健康检查"""
        self.health_history.append({
            "date": datetime.now(),
            "status": status.value,
            "notes": notes
        })
    
    def get_care_history(self, days: int = 30) -> List[Dict[str, Any]]:
        """获取养护历史"""
        cutoff = datetime.now() - timedelta(days=days)
        return [
            log for log in self.care_log
            if log["date"] >= cutoff
        ]


class PlantCareScheduler:
    """植物养护调度器"""
    
    def __init__(self):
        """初始化调度器"""
        self.plants: List[Plant] = []
    
    def add_plant(self, plant: Plant):
        """添加植物"""
        self.plants.append(plant)
    
    def remove_plant(self, plant_name: str) -> bool:
        """移除植物"""
        for i, plant in enumerate(self.plants):
            if plant.name == plant_name:
                self.plants.pop(i)
                return True
        return False
    
    def get_plant(self, plant_name: str) -> Optional[Plant]:
        """获取植物"""
        for plant in self.plants:
            if plant.name == plant_name:
                return plant
        return None
    
    def get_watering_schedule(
        self,
        season: Season,
        indoor_temperature: float = 22,
        humidity: float = 50
    ) -> List[Dict[str, Any]]:
        """
        获取浇水计划
        
        Args:
            season: 当前季节
            indoor_temperature: 室内温度
            humidity: 湿度
            
        Returns:
            浇水计划列表
        """
        schedule = []
        
        for plant in self.plants:
            info = PLANT_DATABASE.get(plant.plant_type, {})
            base_frequency = info.get("water_frequency", WaterFrequency.MODERATE)
            
            # 根据季节调整
            days = self._calculate_watering_days(
                base_frequency,
                season,
                indoor_temperature,
                humidity
            )
            
            next_watering = datetime.now() + timedelta(days=days)
            if plant.last_watered:
                days_since = (datetime.now() - plant.last_watered).days
                urgency = "high" if days_since >= days else "normal" if days_since >= days - 2 else "low"
            else:
                urgency = "high"
            
            schedule.append({
                "plant_name": plant.name,
                "plant_type": plant.plant_type.value,
                "days_until_watering": days,
                "next_watering_date": next_watering.strftime("%Y-%m-%d"),
                "last_watered": plant.last_watered.strftime("%Y-%m-%d") if plant.last_watered else "从未",
                "urgency": urgency,
                "location": plant.location
            })
        
        # 按紧急程度排序
        urgency_order = {"high": 0, "normal": 1, "low": 2}
        schedule.sort(key=lambda x: urgency_order[x["urgency"]])
        
        return schedule
    
    def _calculate_watering_days(
        self,
        base_frequency: WaterFrequency,
        season: Season,
        temperature: float,
        humidity: float
    ) -> int:
        """计算浇水间隔天数"""
        # 基础天数
        base_days = {
            WaterFrequency.RARELY: 21,
            WaterFrequency.INFREQUENT: 14,
            WaterFrequency.MODERATE: 7,
            WaterFrequency.FREQUENT: 3,
            WaterFrequency.VERY_FREQUENT: 1
        }.get(base_frequency, 7)
        
        # 季节调整
        season_factor = {
            Season.SPRING: 0.9,
            Season.SUMMER: 0.7,  # 夏季需要更多水
            Season.AUTUMN: 1.0,
            Season.WINTER: 1.5   # 冬季需要更少水
        }.get(season, 1.0)
        
        # 温度调整（温度越高，蒸发越快）
        temp_factor = 1.0
        if temperature > 28:
            temp_factor = 0.7
        elif temperature > 25:
            temp_factor = 0.85
        elif temperature < 15:
            temp_factor = 1.3
        
        # 湿度调整（湿度越低，蒸发越快）
        humidity_factor = 1.0
        if humidity < 30:
            humidity_factor = 0.7
        elif humidity < 50:
            humidity_factor = 0.85
        elif humidity > 70:
            humidity_factor = 1.2
        
        days = int(base_days * season_factor * temp_factor * humidity_factor)
        return max(1, min(30, days))  # 限制在1-30天之间
    
    def get_fertilizing_schedule(self) -> List[Dict[str, Any]]:
        """获取施肥计划"""
        schedule = []
        
        for plant in self.plants:
            info = PLANT_DATABASE.get(plant.plant_type, {})
            frequency_days = info.get("fertilizer_frequency_days", 30)
            
            if plant.last_fertilized:
                days_since = (datetime.now() - plant.last_fertilized).days
                days_until = max(0, frequency_days - days_since)
                next_date = datetime.now() + timedelta(days=days_until)
                needs_fertilizer = days_since >= frequency_days
            else:
                days_until = 0
                next_date = datetime.now()
                needs_fertilizer = True
            
            schedule.append({
                "plant_name": plant.name,
                "plant_type": plant.plant_type.value,
                "frequency_days": frequency_days,
                "days_until_fertilizing": days_until,
                "next_fertilizing_date": next_date.strftime("%Y-%m-%d"),
                "last_fertilized": plant.last_fertilized.strftime("%Y-%m-%d") if plant.last_fertilized else "从未",
                "needs_fertilizer": needs_fertilizer
            })
        
        # 按需施肥排序
        schedule.sort(key=lambda x: (not x["needs_fertilizer"], x["days_until_fertilizing"]))
        
        return schedule
    
    def get_seasonal_care_tips(self, season: Season) -> Dict[str, Any]:
        """获取季节性养护建议"""
        tips = {
            Season.SPRING: {
                "title": "春季养护要点",
                "general_tips": [
                    "春季是植物生长旺季，逐渐增加浇水频率",
                    "开始施用氮肥促进叶片生长",
                    "检查是否需要换盆",
                    "修剪枯枝病叶，促进新芽萌发",
                    "注意防治春季病虫害"
                ],
                "watering": "逐渐恢复正常浇水频率",
                "fertilizing": "开始生长季施肥计划",
                "light": "注意防止春末强光灼伤"
            },
            Season.SUMMER: {
                "title": "夏季养护要点",
                "general_tips": [
                    "高温季节增加浇水频率，避免植物脱水",
                    "注意遮阴，防止强光灼伤叶片",
                    "增加环境湿度，可向叶面喷水",
                    "避免正午高温时浇水",
                    "注意通风，防止病虫害滋生"
                ],
                "watering": "早晚浇水，避开正午高温",
                "fertilizing": "减少施肥，避免烧根",
                "light": "遮阴防护，避免直射阳光"
            },
            Season.AUTUMN: {
                "title": "秋季养护要点",
                "general_tips": [
                    "逐渐减少浇水频率，准备入冬",
                    "增施磷钾肥，增强植物抗寒性",
                    "移入室内的植物注意适应光照变化",
                    "收集落叶制作堆肥",
                    "做好防寒保暖准备"
                ],
                "watering": "逐渐减少浇水频率",
                "fertilizing": "施用磷钾肥，停止氮肥",
                "light": "尽可能提供充足光照"
            },
            Season.WINTER: {
                "title": "冬季养护要点",
                "general_tips": [
                    "大幅减少浇水，避免根部腐烂",
                    "停止施肥或大幅减少",
                    "移至温暖向阳处",
                    "远离暖气和空调出风口",
                    "注意保温，夜间可套塑料袋"
                ],
                "watering": "严格控制浇水，保持偏干",
                "fertilizing": "停止或极少施肥",
                "light": "放置在阳光充足处"
            }
        }
        
        return tips.get(season, tips[Season.SPRING])


def calculate_water_needs(
    plant_type: PlantType,
    pot_diameter_cm: float,
    season: Season = Season.SPRING,
    temperature: float = 22,
    humidity: float = 50
) -> Dict[str, Any]:
    """
    计算植物需水量
    
    Args:
        plant_type: 植物类型
        pot_diameter_cm: 花盆直径（厘米）
        season: 季节
        temperature: 环境温度
        humidity: 环境湿度
        
    Returns:
        需水量和浇水建议
    """
    info = PLANT_DATABASE.get(plant_type, {})
    base_frequency = info.get("water_frequency", WaterFrequency.MODERATE)
    
    # 根据花盆大小计算基础水量
    # 大致规则：直径每10cm需要约200ml水
    base_ml = (pot_diameter_cm / 10) * 200
    
    # 季节调整
    season_factor = {
        Season.SPRING: 1.0,
        Season.SUMMER: 1.3,
        Season.AUTUMN: 0.9,
        Season.WINTER: 0.6
    }.get(season, 1.0)
    
    # 温度调整
    temp_factor = 1.0
    if temperature > 28:
        temp_factor = 1.2
    elif temperature < 15:
        temp_factor = 0.7
    
    # 湿度调整
    humidity_factor = 1.0
    if humidity < 30:
        humidity_factor = 1.3
    elif humidity > 70:
        humidity_factor = 0.8
    
    water_ml = int(base_ml * season_factor * temp_factor * humidity_factor)
    
    # 计算浇水间隔
    base_days = {
        WaterFrequency.RARELY: 21,
        WaterFrequency.INFREQUENT: 14,
        WaterFrequency.MODERATE: 7,
        WaterFrequency.FREQUENT: 3,
        WaterFrequency.VERY_FREQUENT: 1
    }.get(base_frequency, 7)
    
    return {
        "water_amount_ml": water_ml,
        "watering_frequency_days": base_days,
        "adjusted_for_season": season.value,
        "recommendations": [
            f"每次浇水约 {water_ml} 毫升",
            f"建议每 {base_days} 天浇水一次",
            "浇水前检查土壤表面是否干燥",
            "确保花盆有良好排水孔"
        ]
    }


def analyze_light_requirements(
    plant_type: PlantType,
    current_light_level: LightLevel
) -> Dict[str, Any]:
    """
    分析光照需求
    
    Args:
        plant_type: 植物类型
        current_light_level: 当前光照水平
        
    Returns:
        光照分析和建议
    """
    info = PLANT_DATABASE.get(plant_type, {})
    required_light = info.get("light_requirement", LightLevel.MEDIUM)
    
    light_order = {
        LightLevel.LOW: 1,
        LightLevel.MEDIUM: 2,
        LightLevel.BRIGHT: 3,
        LightLevel.DIRECT: 4
    }
    
    current_level = light_order[current_light_level]
    required_level = light_order[required_light]
    
    if current_level < required_level:
        status = "不足"
        suggestions = [
            "将植物移至更明亮的位置",
            "考虑使用植物补光灯",
            "定期旋转花盆，确保均匀受光",
            "清洁叶片以提高光吸收"
        ]
    elif current_level > required_level:
        status = "过强"
        suggestions = [
            "移至稍阴的位置",
            "使用遮阳网或窗帘",
            "避免正午直射阳光",
            "注意观察叶片是否有灼伤"
        ]
    else:
        status = "适宜"
        suggestions = [
            "保持当前位置",
            "定期旋转花盆",
            "清洁叶片保持光吸收"
        ]
    
    return {
        "plant_type": plant_type.value,
        "required_light": required_light.value,
        "current_light": current_light_level.value,
        "status": status,
        "suggestions": suggestions,
        "light_level_description": {
            LightLevel.LOW: "低光照（<1000 lux），适合卫生间、走廊",
            LightLevel.MEDIUM: "中等光照（1000-2500 lux），适合客厅、卧室",
            LightLevel.BRIGHT: "明亮光照（2500-10000 lux），适合阳台、窗边",
            LightLevel.DIRECT: "直射阳光（>10000 lux），适合室外、南向阳台"
        }.get(current_light_level)
    }


def get_seasonal_fertilizer_recommendation(
    plant_type: PlantType,
    season: Season,
    growth_stage: GrowthStage = GrowthStage.VEGETATIVE
) -> Dict[str, Any]:
    """
    获取季节性施肥建议
    
    Args:
        plant_type: 植物类型
        season: 季节
        growth_stage: 生长阶段
        
    Returns:
        施肥建议
    """
    info = PLANT_DATABASE.get(plant_type, {})
    base_frequency = info.get("fertilizer_frequency_days", 30)
    
    # 季节施肥建议
    season_fertilizer = {
        Season.SPRING: {
            "type": "氮肥为主，促进枝叶生长",
            "frequency": "每2-3周一次",
            "dilution": "标准浓度或稍淡",
            "notes": "生长旺季，可适当增加频率"
        },
        Season.SUMMER: {
            "type": "平衡肥或稍减量",
            "frequency": "每3-4周一次",
            "dilution": "稀释至1/2浓度",
            "notes": "高温期避免浓肥烧根"
        },
        Season.AUTUMN: {
            "type": "磷钾肥为主，增强抗寒性",
            "frequency": "每3-4周一次",
            "dilution": "标准浓度",
            "notes": "为越冬做准备"
        },
        Season.WINTER: {
            "type": "停止施肥或微量",
            "frequency": "每月一次或不施肥",
            "dilution": "稀释至1/4浓度",
            "notes": "休眠期，植物吸收能力弱"
        }
    }
    
    # 生长阶段施肥建议
    stage_fertilizer = {
        GrowthStage.SEED: {"N": 10, "P": 10, "P": 10, "note": "均衡营养"},
        GrowthStage.SEEDLING: {"N": 20, "P": 10, "K": 10, "note": "氮肥促进生长"},
        GrowthStage.VEGETATIVE: {"N": 20, "P": 10, "K": 10, "note": "氮肥为主"},
        GrowthStage.BUDDING: {"N": 10, "P": 20, "K": 10, "note": "增磷促进开花"},
        GrowthStage.FLOWERING: {"N": 5, "P": 20, "K": 15, "note": "磷钾促进花期"},
        GrowthStage.FRUITING: {"N": 10, "P": 15, "K": 20, "note": "钾肥促进果实"},
        GrowthStage.DORMANT: {"N": 0, "P": 5, "K": 5, "note": "停止或微量"},
        GrowthStage.MATURE: {"N": 15, "P": 15, "K": 15, "note": "均衡养护"}
    }
    
    return {
        "plant_type": plant_type.value,
        "season": season.value,
        "growth_stage": growth_stage.value,
        "seasonal_advice": season_fertilizer.get(season),
        "stage_formula": stage_fertilizer.get(growth_stage),
        "base_frequency_days": base_frequency
    }


def diagnose_plant_issue(
    plant_type: PlantType,
    symptoms: List[str]
) -> Dict[str, Any]:
    """
    诊断植物问题
    
    Args:
        plant_type: 植物类型
        symptoms: 症状列表
        
    Returns:
        诊断结果和建议
    """
    # 症状-问题映射
    symptom_map = {
        "叶尖枯黄": {
            "causes": ["湿度不足", "浇水过多或过少", "空气干燥"],
            "solutions": ["增加环境湿度", "检查土壤湿度", "向叶面喷水"],
            "severity": "minor"
        },
        "叶片发黄": {
            "causes": ["缺氮", "浇水过多", "光照不足", "根部问题"],
            "solutions": ["施用氮肥", "减少浇水频率", "移至光线充足处", "检查根系"],
            "severity": "moderate"
        },
        "叶片脱落": {
            "causes": ["环境突变", "浇水不当", "温度过低", "光照不足"],
            "solutions": ["保持环境稳定", "调整浇水", "移至温暖处", "增加光照"],
            "severity": "moderate"
        },
        "徒长": {
            "causes": ["光照不足", "氮肥过多"],
            "solutions": ["增加光照", "减少氮肥", "适当修剪"],
            "severity": "minor"
        },
        "不开花": {
            "causes": ["光照不足", "养分不均衡", "未到花期", "休眠期"],
            "solutions": ["提供充足光照", "增施磷钾肥", "耐心等待", "检查生长阶段"],
            "severity": "moderate"
        },
        "根部腐烂": {
            "causes": ["浇水过多", "排水不良", "土壤过湿"],
            "solutions": ["减少浇水", "换盆换土", "修剪腐烂根系", "改善排水"],
            "severity": "severe"
        },
        "叶片卷曲": {
            "causes": ["水分胁迫", "虫害", "温度过高"],
            "solutions": ["调整浇水", "检查虫害", "降温通风"],
            "severity": "moderate"
        },
        "叶斑": {
            "causes": ["真菌感染", "细菌感染", "虫害"],
            "solutions": ["摘除病叶", "喷洒杀菌剂", "改善通风"],
            "severity": "moderate"
        },
        "生长缓慢": {
            "causes": ["养分不足", "光照不足", "根系受限", "温度不适"],
            "solutions": ["适当施肥", "增加光照", "换盆", "调整温度"],
            "severity": "minor"
        },
        "叶缘焦枯": {
            "causes": ["盐分积累", "施肥过浓", "水质问题"],
            "solutions": ["大量浇水冲洗", "减少施肥", "使用过滤水"],
            "severity": "minor"
        }
    }
    
    diagnoses = []
    for symptom in symptoms:
        if symptom in symptom_map:
            info = symptom_map[symptom]
            diagnoses.append({
                "symptom": symptom,
                "possible_causes": info["causes"],
                "solutions": info["solutions"],
                "severity": info["severity"]
            })
    
    # 添加植物类型的常见问题
    plant_info = PLANT_DATABASE.get(plant_type, {})
    common_issues = plant_info.get("common_issues", [])
    care_tips = plant_info.get("care_tips", [])
    
    # 严重程度排序
    severity_order = {"severe": 0, "moderate": 1, "minor": 2}
    diagnoses.sort(key=lambda x: severity_order[x["severity"]])
    
    return {
        "plant_type": plant_type.value,
        "diagnoses": diagnoses,
        "common_issues_for_type": common_issues,
        "general_care_tips": care_tips
    }


def create_plant_care_calendar(
    year: int,
    month: int,
    plants: List[Plant],
    location: str = "north"  # north 或 south hemisphere
) -> Dict[str, Any]:
    """
    创建植物养护日历
    
    Args:
        year: 年份
        month: 月份
        plants: 植物列表
        location: 地区（北半球/南半球）
        
    Returns:
        月度养护日历
    """
    # 确定季节
    if location == "north":
        season_map = {
            3: Season.SPRING, 4: Season.SPRING, 5: Season.SPRING,
            6: Season.SUMMER, 7: Season.SUMMER, 8: Season.SUMMER,
            9: Season.AUTUMN, 10: Season.AUTUMN, 11: Season.AUTUMN,
            12: Season.WINTER, 1: Season.WINTER, 2: Season.WINTER
        }
    else:
        season_map = {
            9: Season.SPRING, 10: Season.SPRING, 11: Season.SPRING,
            12: Season.SUMMER, 1: Season.SUMMER, 2: Season.SUMMER,
            3: Season.AUTUMN, 4: Season.AUTUMN, 5: Season.AUTUMN,
            6: Season.WINTER, 7: Season.WINTER, 8: Season.WINTER
        }
    
    season = season_map.get(month, Season.SPRING)
    
    # 生成日历
    from calendar import monthrange
    days_in_month = monthrange(year, month)[1]
    
    calendar = {
        "year": year,
        "month": month,
        "season": season.value,
        "tasks": []
    }
    
    # 为每株植物规划养护任务
    for plant in plants:
        info = PLANT_DATABASE.get(plant.plant_type, {})
        water_freq = info.get("water_frequency", WaterFrequency.MODERATE)
        fertilizer_freq = info.get("fertilizer_frequency_days", 30)
        
        # 浇水日
        water_days = {
            WaterFrequency.RARELY: [15],
            WaterFrequency.INFREQUENT: [7, 21],
            WaterFrequency.MODERATE: [3, 10, 17, 24],
            WaterFrequency.FREQUENT: [1, 4, 7, 10, 13, 16, 19, 22, 25, 28],
            WaterFrequency.VERY_FREQUENT: list(range(1, days_in_month + 1))
        }.get(water_freq, [3, 10, 17, 24])
        
        for day in water_days:
            if day <= days_in_month:
                calendar["tasks"].append({
                    "day": day,
                    "plant": plant.name,
                    "task": "浇水",
                    "type": "watering"
                })
        
        # 施肥日（月中）
        fertilize_day = 15 if 15 <= days_in_month else days_in_month
        calendar["tasks"].append({
            "day": fertilize_day,
            "plant": plant.name,
            "task": "施肥",
            "type": "fertilizing"
        })
    
    # 按日期排序
    calendar["tasks"].sort(key=lambda x: (x["day"], x["plant"]))
    
    # 添加月度总结
    calendar["monthly_summary"] = {
        "total_watering_tasks": sum(1 for t in calendar["tasks"] if t["type"] == "watering"),
        "total_fertilizing_tasks": sum(1 for t in calendar["tasks"] if t["type"] == "fertilizing"),
        "seasonal_tips": get_seasonal_care_tips_by_enum(season)
    }
    
    return calendar


def get_seasonal_care_tips_by_enum(season: Season) -> List[str]:
    """获取季节性养护建议"""
    tips = {
        Season.SPRING: [
            "开始增加浇水频率",
            "施用氮肥促进生长",
            "检查是否需要换盆",
            "修剪促进新芽"
        ],
        Season.SUMMER: [
            "注意遮阴防暑",
            "早晚浇水避高温",
            "增加环境湿度",
            "注意通风防病"
        ],
        Season.AUTUMN: [
            "逐渐减少浇水",
            "施磷钾肥抗寒",
            "收集落叶堆肥",
            "准备防寒措施"
        ],
        Season.WINTER: [
            "严格控制浇水",
            "停止或减少施肥",
            "注意保温防寒",
            "远离暖气出风口"
        ]
    }
    return tips.get(season, [])


# 便捷函数
def quick_water_check(
    plant_type: PlantType,
    days_since_watering: int,
    season: Season = Season.SPRING
) -> Dict[str, Any]:
    """
    快速浇水检查
    
    Args:
        plant_type: 植物类型
        days_since_watering: 距离上次浇水的天数
        season: 当前季节
        
    Returns:
        浇水建议
    """
    info = PLANT_DATABASE.get(plant_type, {})
    base_frequency = info.get("water_frequency", WaterFrequency.MODERATE)
    
    base_days = {
        WaterFrequency.RARELY: 21,
        WaterFrequency.INFREQUENT: 14,
        WaterFrequency.MODERATE: 7,
        WaterFrequency.FREQUENT: 3,
        WaterFrequency.VERY_FREQUENT: 1
    }.get(base_frequency, 7)
    
    # 季节调整
    season_factor = {
        Season.SPRING: 1.0,
        Season.SUMMER: 0.7,
        Season.AUTUMN: 1.0,
        Season.WINTER: 1.5
    }.get(season, 1.0)
    
    recommended_days = int(base_days * season_factor)
    
    needs_water = days_since_watering >= recommended_days
    urgency = "立即浇水" if days_since_watering >= recommended_days + 3 else \
              "今天浇水" if needs_water else \
              "可以等待" if days_since_watering >= recommended_days - 2 else \
              "暂不需要"
    
    return {
        "plant_type": plant_type.value,
        "days_since_watering": days_since_watering,
        "recommended_interval": recommended_days,
        "needs_water": needs_water,
        "urgency": urgency,
        "next_watering_in_days": max(0, recommended_days - days_since_watering)
    }


def get_plant_database_info(plant_type: PlantType) -> Dict[str, Any]:
    """获取植物类型信息"""
    return PLANT_DATABASE.get(plant_type, {})


def list_all_plant_types() -> List[Dict[str, str]]:
    """列出所有植物类型"""
    return [
        {"type": pt.value, "name": info["name"]}
        for pt, info in PLANT_DATABASE.items()
    ]


if __name__ == "__main__":
    # 示例使用
    print("植物养护工具示例")
    print("=" * 50)
    
    # 创建植物
    my_monstera = Plant(
        name="我的龟背竹",
        plant_type=PlantType.TROPICAL,
        location="客厅",
        purchase_date=datetime(2025, 1, 15)
    )
    
    # 记录养护
    my_monstera.record_watering()
    my_monstera.record_fertilizing(fertilizer_type="复合肥")
    
    # 获取信息
    info = my_monstera.get_info()
    print(f"\n植物信息: {info}")
    
    # 计算需水量
    water_needs = calculate_water_needs(
        PlantType.TROPICAL,
        pot_diameter_cm=25,
        season=Season.SPRING
    )
    print(f"\n需水量计算: {water_needs}")
    
    # 光照分析
    light_analysis = analyze_light_requirements(
        PlantType.TROPICAL,
        LightLevel.MEDIUM
    )
    print(f"\n光照分析: {light_analysis}")
    
    # 快速浇水检查
    water_check = quick_water_check(
        PlantType.TROPICAL,
        days_since_watering=5,
        season=Season.SUMMER
    )
    print(f"\n浇水检查: {water_check}")
    
    # 诊断问题
    diagnosis = diagnose_plant_issue(
        PlantType.TROPICAL,
        ["叶尖枯黄", "叶片发黄"]
    )
    print(f"\n问题诊断: {diagnosis}")