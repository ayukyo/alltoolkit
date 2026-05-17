"""
钓鱼助手工具模块
提供钓鱼时间预测、气象指数计算、装备推荐等功能

功能:
- 最佳钓鱼时间计算（基于月相、气压、气温）
- 钓鱼气象指数评估
- 鱼竿选择推荐
- 鱼线配置计算
- 打窝料计算
- 渔获记录管理
- 月相对钓鱼的影响分析
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class FishType(Enum):
    """鱼类类型"""
    CARP = "鲤鱼"
    CRUCIAN = "鲫鱼"
    CATFISH = "鲶鱼"
    GRASS_CARP = "草鱼"
    SILVER_CARP = "鲢鱼"
    TILAPIA = "罗非鱼"
    BASS = "鲈鱼"
    TROUT = "鳟鱼"
    PERCH = "河鲈"
    PIKE = "狗鱼"


class WeatherCondition(Enum):
    """天气条件"""
    SUNNY = "晴天"
    CLOUDY = "多云"
    OVERCAST = "阴天"
    LIGHT_RAIN = "小雨"
    MODERATE_RAIN = "中雨"
    HEAVY_RAIN = "大雨"
    FOGGY = "雾天"
    WINDY = "大风"


class MoonPhase(Enum):
    """月相"""
    NEW_MOON = "新月"
    WAXING_CRESCENT = "蛾眉月"
    FIRST_QUARTER = "上弦月"
    WAXING_GIBBOUS = "盈凸月"
    FULL_MOON = "满月"
    WANING_GIBBOUS = "亏凸月"
    LAST_QUARTER = "下弦月"
    WANING_CRESCENT = "残月"


class RodType(Enum):
    """鱼竿类型"""
    HAND_ROD = "手竿"
    TELESCOPIC = "伸缩竿"
    CARBON = "碳素竿"
    GLASS_FIBER = "玻璃钢竿"
    COMPOSITE = "复合材料竿"


class FishingMethod(Enum):
    """钓法"""
    FLOAT_FISHING = "浮钓"
    BOTTOM_FISHING = "底钓"
    SUSPENDED_FISHING = "悬钓"
    LURE_FISHING = "路亚钓"
    FLY_FISHING = "飞钓"
    POLE_FISHING = "台钓"


@dataclass
class WeatherData:
    """天气数据"""
    temperature: float  # 温度（摄氏度）
    pressure: float  # 气压（hPa）
    humidity: float  # 湿度（%）
    wind_speed: float  # 风速（m/s）
    wind_direction: str  # 风向
    condition: WeatherCondition  # 天气状况
    visibility: float = 10.0  # 能见度（km）


@dataclass
class FishCatch:
    """渔获记录"""
    fish_type: FishType
    weight: float  # 重量（kg）
    length: float  # 长度（cm）
    catch_time: datetime
    location: str
    bait: str
    depth: float  # 钓深（米）
    notes: str = ""


@dataclass
class FishingSession:
    """钓鱼会话"""
    start_time: datetime
    end_time: Optional[datetime] = None
    location: str = ""
    weather: Optional[WeatherData] = None
    catches: List[FishCatch] = field(default_factory=list)
    total_weight: float = 0.0
    total_count: int = 0

    def add_catch(self, catch: FishCatch):
        """添加渔获"""
        self.catches.append(catch)
        self.total_weight += catch.weight
        self.total_count += 1

    def get_duration(self) -> timedelta:
        """获取时长"""
        end = self.end_time or datetime.now()
        return end - self.start_time

    def get_catch_rate(self) -> float:
        """获取渔获率（条/小时）"""
        duration = self.get_duration().total_seconds() / 3600
        if duration <= 0:
            return 0.0
        return self.total_count / duration


class FishingWeatherIndex:
    """钓鱼气象指数计算器"""

    # 最佳气温范围
    OPTIMAL_TEMP_RANGE = (18, 28)  # 摄氏度
    # 最佳气压范围
    OPTIMAL_PRESSURE_RANGE = (1000, 1020)  # hPa
    # 最佳湿度范围
    OPTIMAL_HUMIDITY_RANGE = (50, 80)  # %
    # 最大可接受风速
    MAX_ACCEPTABLE_WIND = 8.0  # m/s

    @classmethod
    def calculate_index(cls, weather: WeatherData) -> Dict[str, Any]:
        """
        计算钓鱼气象指数

        返回综合评分（0-100）和各项分值
        """
        scores = {
            "temperature": cls._score_temperature(weather.temperature),
            "pressure": cls._score_pressure(weather.pressure),
            "humidity": cls._score_humidity(weather.humidity),
            "wind": cls._score_wind(weather.wind_speed),
            "condition": cls._score_condition(weather.condition),
            "visibility": cls._score_visibility(weather.visibility),
        }

        # 检查是否有极端恶劣条件，直接返回很低评分
        if weather.condition == WeatherCondition.HEAVY_RAIN:
            total_score = 10
        elif weather.wind_speed > cls.MAX_ACCEPTABLE_WIND:
            # 风速超过最大可接受值
            total_score = 15
        elif weather.pressure < 970:
            # 极低气压（台风等）
            total_score = 20
        else:
            # 加权平均
            weights = {
                "temperature": 0.20,
                "pressure": 0.25,
                "humidity": 0.15,
                "wind": 0.20,
                "condition": 0.15,
                "visibility": 0.05,
            }
            total_score = sum(scores[k] * weights[k] for k in scores)

        return {
            "total_score": round(total_score, 1),
            "level": cls._get_level(total_score),
            "recommendation": cls._get_recommendation(total_score),
            "details": scores,
        }

    @classmethod
    def _score_temperature(cls, temp: float) -> float:
        """温度评分"""
        low, high = cls.OPTIMAL_TEMP_RANGE
        if low <= temp <= high:
            # 最佳范围内，越高分越高（适中最高）
            mid = (low + high) / 2
            return 100 - abs(temp - mid) * 2
        elif temp < low:
            # 低于最佳范围（低温相对可接受）
            return max(0, 100 - (low - temp) * 4)
        else:
            # 高于最佳范围（高温对钓鱼更不利）
            return max(0, 100 - (temp - high) * 6)

    @classmethod
    def _score_pressure(cls, pressure: float) -> float:
        """气压评分"""
        low, high = cls.OPTIMAL_PRESSURE_RANGE
        if low <= pressure <= high:
            # 最佳范围内
            return 100 - abs(pressure - 1010) * 0.5
        elif pressure < low:
            # 低气压，鱼不活跃
            return max(0, 100 - (low - pressure) * 5)
        else:
            # 高气压
            return max(0, 100 - (pressure - high) * 2)

    @classmethod
    def _score_humidity(cls, humidity: float) -> float:
        """湿度评分"""
        low, high = cls.OPTIMAL_HUMIDITY_RANGE
        if low <= humidity <= high:
            return 100
        elif humidity < low:
            return max(0, 100 - (low - humidity) * 1.5)
        else:
            return max(0, 100 - (humidity - high) * 1.5)

    @classmethod
    def _score_wind(cls, wind_speed: float) -> float:
        """风速评分"""
        if wind_speed <= 2.0:
            return 100
        elif wind_speed <= 4.0:
            return 85
        elif wind_speed <= 6.0:
            return 60
        elif wind_speed <= cls.MAX_ACCEPTABLE_WIND:
            return 30
        else:
            return 0  # 风太大，不建议钓鱼

    @classmethod
    def _score_condition(cls, condition: WeatherCondition) -> float:
        """天气状况评分"""
        scores = {
            WeatherCondition.SUNNY: 75,
            WeatherCondition.CLOUDY: 90,
            WeatherCondition.OVERCAST: 85,
            WeatherCondition.LIGHT_RAIN: 70,
            WeatherCondition.MODERATE_RAIN: 30,
            WeatherCondition.HEAVY_RAIN: 0,
            WeatherCondition.FOGGY: 40,
            WeatherCondition.WINDY: 10,
        }
        return scores.get(condition, 50)

    @classmethod
    def _score_visibility(cls, visibility: float) -> float:
        """能见度评分"""
        if visibility >= 10:
            return 100
        elif visibility >= 5:
            return 80
        elif visibility >= 2:
            return 50
        else:
            return max(0, visibility * 20)

    @classmethod
    def _get_level(cls, score: float) -> str:
        """获取等级"""
        if score >= 90:
            return "极好"
        elif score >= 75:
            return "很好"
        elif score >= 60:
            return "较好"
        elif score >= 45:
            return "一般"
        elif score >= 30:
            return "较差"
        else:
            return "不宜"

    @classmethod
    def _get_recommendation(cls, score: float) -> str:
        """获取建议"""
        if score >= 90:
            return "绝佳钓鱼天气！鱼儿活跃，渔获可期。"
        elif score >= 75:
            return "良好的钓鱼天气，把握机会出钓。"
        elif score >= 60:
            return "可以出钓，注意观察鱼情变化。"
        elif score >= 45:
            return "天气一般，建议选择早晚时段。"
        elif score >= 30:
            return "不太适合钓鱼，建议等待更好天气。"
        else:
            return "天气恶劣，不建议出钓。"


class MoonPhaseCalculator:
    """月相计算器"""

    # 已知新月时间（参考点）
    KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14, 0)
    LUNAR_CYCLE = 29.53058867  # 月相周期（天）

    @classmethod
    def get_moon_phase(cls, date: datetime) -> MoonPhase:
        """
        计算指定日期的月相

        Args:
            date: 日期时间

        Returns:
            MoonPhase 枚举值
        """
        # 计算从已知新月以来的天数
        days_since_new_moon = (date - cls.KNOWN_NEW_MOON).total_seconds() / 86400

        # 计算当前月相周期中的位置
        moon_age = days_since_new_moon % cls.LUNAR_CYCLE

        # 判断月相
        if moon_age < 1.85:
            return MoonPhase.NEW_MOON
        elif moon_age < 7.38:
            return MoonPhase.WAXING_CRESCENT
        elif moon_age < 9.23:
            return MoonPhase.FIRST_QUARTER
        elif moon_age < 14.77:
            return MoonPhase.WAXING_GIBBOUS
        elif moon_age < 16.61:
            return MoonPhase.FULL_MOON
        elif moon_age < 22.15:
            return MoonPhase.WANING_GIBBOUS
        elif moon_age < 24.00:
            return MoonPhase.LAST_QUARTER
        else:
            return MoonPhase.WANING_CRESCENT

    @classmethod
    def get_moon_illumination(cls, date: datetime) -> float:
        """
        计算月球照明度（0-100%）

        Args:
            date: 日期时间

        Returns:
            照明百分比
        """
        days_since_new_moon = (date - cls.KNOWN_NEW_MOON).total_seconds() / 86400
        moon_age = days_since_new_moon % cls.LUNAR_CYCLE

        # 使用余弦函数近似照明度
        illumination = (1 - math.cos(2 * math.pi * moon_age / cls.LUNAR_CYCLE)) / 2
        return round(illumination * 100, 1)

    @classmethod
    def get_fishing_quality(cls, date: datetime) -> Dict[str, Any]:
        """
        获取基于月相的钓鱼质量评估

        Args:
            date: 日期时间

        Returns:
            钓鱼质量评估字典
        """
        phase = cls.get_moon_phase(date)
        illumination = cls.get_moon_illumination(date)

        # 月相对钓鱼的影响评分
        phase_scores = {
            MoonPhase.NEW_MOON: {"score": 90, "description": "新月期，夜间无光，适合白天钓鱼"},
            MoonPhase.WAXING_CRESCENT: {"score": 80, "description": "蛾眉月，鱼儿活跃"},
            MoonPhase.FIRST_QUARTER: {"score": 70, "description": "上弦月，早晚垂钓效果好"},
            MoonPhase.WAXING_GIBBOUS: {"score": 60, "description": "盈凸月，夜间活动增加"},
            MoonPhase.FULL_MOON: {"score": 50, "description": "满月期，夜间觅食活跃，白天效果一般"},
            MoonPhase.WANING_GIBBOUS: {"score": 60, "description": "亏凸月，鱼儿逐渐恢复"},
            MoonPhase.LAST_QUARTER: {"score": 70, "description": "下弦月，适合早晚垂钓"},
            MoonPhase.WANING_CRESCENT: {"score": 80, "description": "残月期，白天钓鱼效果佳"},
        }

        info = phase_scores[phase]

        return {
            "phase": phase.value,
            "illumination": illumination,
            "score": info["score"],
            "description": info["description"],
            "best_time": cls._get_best_fishing_time(phase),
        }

    @classmethod
    def _get_best_fishing_time(cls, phase: MoonPhase) -> List[str]:
        """根据月相推荐最佳钓鱼时间"""
        recommendations = {
            MoonPhase.NEW_MOON: ["日出后2-3小时", "日落前2-3小时"],
            MoonPhase.WAXING_CRESCENT: ["清晨", "傍晚", "夜间前半夜"],
            MoonPhase.FIRST_QUARTER: ["上午", "傍晚"],
            MoonPhase.WAXING_GIBBOUS: ["清晨", "傍晚", "前半夜"],
            MoonPhase.FULL_MOON: ["清晨日出前", "傍晚日落后", "夜间"],
            MoonPhase.WANING_GIBBOUS: ["清晨", "傍晚", "后半夜"],
            MoonPhase.LAST_QUARTER: ["上午", "傍晚"],
            MoonPhase.WANING_CRESCENT: ["清晨", "傍晚", "白天"],
        }
        return recommendations[phase]

    @classmethod
    def find_next_best_period(cls, start_date: datetime, days: int = 14) -> List[Dict[str, Any]]:
        """
        找到未来最佳钓鱼时段

        Args:
            start_date: 开始日期
            days: 查找天数

        Returns:
            最佳时段列表
        """
        best_periods = []

        for i in range(days):
            date = start_date + timedelta(days=i)
            quality = cls.get_fishing_quality(date)

            if quality["score"] >= 80:
                best_periods.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "phase": quality["phase"],
                    "score": quality["score"],
                    "description": quality["description"],
                    "best_time": quality["best_time"],
                })

        return best_periods


class FishingTimePredictor:
    """钓鱼时间预测器"""

    # 各季节最佳时段
    SEASONAL_TIMES = {
        "spring": {
            "morning": (5, 9),  # 5:00-9:00
            "evening": (17, 20),  # 17:00-20:00
            "description": "春季早晚最佳，鱼儿活跃觅食",
        },
        "summer": {
            "morning": (4, 8),  # 4:00-8:00
            "evening": (18, 22),  # 18:00-22:00
            "night": (22, 2),  # 夜钓
            "description": "夏季早晚凉爽时段，夜钓效果好",
        },
        "autumn": {
            "morning": (5, 9),  # 5:00-9:00
            "evening": (16, 19),  # 16:00-19:00
            "description": "秋季全天适宜，尤其早晚",
        },
        "winter": {
            "midday": (10, 15),  # 10:00-15:00
            "description": "冬季中午温暖时段，鱼儿活动减少",
        },
    }

    @classmethod
    def get_best_times(cls, date: datetime) -> Dict[str, Any]:
        """
        获取指定日期的最佳钓鱼时间

        Args:
            date: 日期

        Returns:
            最佳时间推荐
        """
        season = cls._get_season(date)
        seasonal_info = cls.SEASONAL_TIMES[season]

        result = {
            "season": season,
            "description": seasonal_info["description"],
            "recommended_times": [],
        }

        for period, times in seasonal_info.items():
            if period == "description":
                continue
            start_hour, end_hour = times
            result["recommended_times"].append({
                "period": cls._period_name(period),
                "time_range": f"{start_hour:02d}:00 - {end_hour:02d}:00",
                "quality": cls._estimate_time_quality(date, start_hour, end_hour),
            })

        return result

    @classmethod
    def _get_season(cls, date: datetime) -> str:
        """获取季节"""
        month = date.month
        if month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "autumn"
        else:
            return "winter"

    @classmethod
    def _period_name(cls, period: str) -> str:
        """获取时段名称"""
        names = {
            "morning": "清晨",
            "evening": "傍晚",
            "night": "夜间",
            "midday": "中午",
        }
        return names.get(period, period)

    @classmethod
    def _estimate_time_quality(cls, date: datetime, start_hour: int, end_hour: int) -> str:
        """估计时段质量"""
        # 基于月相和季节估算
        moon_quality = MoonPhaseCalculator.get_fishing_quality(date)

        base_score = moon_quality["score"]

        # 季节修正
        season = cls._get_season(date)
        if season == "winter" and start_hour < 10:
            base_score -= 20
        elif season == "summer" and 11 <= start_hour <= 16:
            base_score -= 15

        if base_score >= 80:
            return "极佳"
        elif base_score >= 60:
            return "良好"
        elif base_score >= 40:
            return "一般"
        else:
            return "较差"


class RodSelector:
    """鱼竿选择器"""

    # 鱼竿规格数据库
    ROD_SPECS = {
        "hand_rod": {
            "name": "手竿",
            "lengths": [2.7, 3.6, 4.5, 5.4, 6.3, 7.2, 8.1],
            "materials": ["碳素", "玻璃钢", "复合材料"],
            "best_for": [FishType.CRUCIAN, FishType.CARP, FishType.GRASS_CARP],
            "water_types": ["池塘", "水库", "河流"],
        },
        "telescopic": {
            "name": "伸缩竿",
            "lengths": [3.0, 4.5, 5.4, 6.3, 7.2, 8.1, 9.0, 10.0],
            "materials": ["碳素", "复合材料"],
            "best_for": [FishType.CARP, FishType.CATFISH, FishType.GRASS_CARP],
            "water_types": ["水库", "河流", "湖泊"],
        },
        "lure_rod": {
            "name": "路亚竿",
            "lengths": [1.8, 2.1, 2.4, 2.7, 3.0],
            "materials": ["碳素"],
            "best_for": [FishType.BASS, FishType.PIKE, FishType.PERCH, FishType.TROUT],
            "water_types": ["河流", "湖泊", "海洋"],
        },
        "fly_rod": {
            "name": "飞钓竿",
            "lengths": [2.4, 2.7, 3.0, 3.3, 3.6],
            "materials": ["碳素", "玻璃钢"],
            "best_for": [FishType.TROUT, FishType.BASS],
            "water_types": ["河流", "湖泊"],
        },
        "pole_rod": {
            "name": "台钓竿",
            "lengths": [2.7, 3.6, 4.5, 5.4, 6.3, 7.2],
            "materials": ["碳素"],
            "best_for": [FishType.CRUCIAN, FishType.CARP, FishType.SILVER_CARP],
            "water_types": ["池塘", "水库", "竞技池"],
        },
    }

    @classmethod
    def recommend(
        cls,
        target_fish: List[FishType],
        water_type: str,
        fishing_style: str = "casual",
        budget: str = "medium",
    ) -> List[Dict[str, Any]]:
        """
        推荐鱼竿

        Args:
            target_fish: 目标鱼种
            water_type: 水域类型
            fishing_style: 钓鱼风格 (casual, sport, competition)
            budget: 预算 (low, medium, high)

        Returns:
            推荐列表
        """
        recommendations = []

        for rod_key, rod_spec in cls.ROD_SPECS.items():
            # 检查鱼种匹配
            fish_match = any(fish in rod_spec["best_for"] for fish in target_fish)

            # 检查水域匹配
            water_match = water_type in rod_spec["water_types"]

            if fish_match or water_match:
                match_score = 0
                if fish_match:
                    match_score += 50
                if water_match:
                    match_score += 30

                # 根据风格调整
                if fishing_style == "competition" and rod_key in ["pole_rod", "hand_rod"]:
                    match_score += 20
                elif fishing_style == "sport" and rod_key in ["lure_rod", "fly_rod"]:
                    match_score += 20

                # 材料推荐
                material_rec = cls._recommend_material(budget, rod_spec["materials"])

                # 长度推荐
                length_rec = cls._recommend_length(rod_key, water_type)

                recommendations.append({
                    "type": rod_key,
                    "name": rod_spec["name"],
                    "match_score": match_score,
                    "recommended_length": length_rec,
                    "recommended_material": material_rec,
                    "available_lengths": rod_spec["lengths"],
                    "suitable_fish": [f.value for f in rod_spec["best_for"]],
                })

        # 按匹配度排序
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return recommendations[:3]  # 返回前3个推荐

    @classmethod
    def _recommend_material(cls, budget: str, materials: List[str]) -> str:
        """根据预算推荐材料"""
        if budget == "high":
            if "碳素" in materials:
                return "碳素"
            return materials[0]
        elif budget == "medium":
            if "复合材料" in materials:
                return "复合材料"
            return materials[0]
        else:
            if "玻璃钢" in materials:
                return "玻璃钢"
            return materials[0]

    @classmethod
    def _recommend_length(cls, rod_type: str, water_type: str) -> str:
        """根据水域推荐长度"""
        length_guide = {
            "hand_rod": {
                "池塘": "3.6-4.5m",
                "水库": "5.4-7.2m",
                "河流": "4.5-6.3m",
                "default": "4.5m",
            },
            "telescopic": {
                "水库": "6.3-8.1m",
                "河流": "5.4-7.2m",
                "湖泊": "6.3-8.1m",
                "default": "6.3m",
            },
            "lure_rod": {
                "河流": "2.1-2.4m",
                "湖泊": "2.4-2.7m",
                "海洋": "2.7-3.0m",
                "default": "2.4m",
            },
            "fly_rod": {
                "河流": "2.7-3.0m",
                "湖泊": "3.0-3.6m",
                "default": "3.0m",
            },
            "pole_rod": {
                "池塘": "3.6-4.5m",
                "水库": "4.5-6.3m",
                "竞技池": "3.6-4.5m",
                "default": "4.5m",
            },
        }

        type_guide = length_guide.get(rod_type, {"default": "4.5m"})
        return type_guide.get(water_type, type_guide["default"])


class FishingLineCalculator:
    """鱼线配置计算器"""

    # 主线规格
    MAIN_LINE_SPECS = {
        "ultra_light": {"diameter": 0.08, "strength": 0.8, "fish_weight": (0, 0.5)},
        "light": {"diameter": 0.10, "strength": 1.5, "fish_weight": (0.5, 1.0)},
        "medium_light": {"diameter": 0.12, "strength": 2.0, "fish_weight": (1.0, 2.0)},
        "medium": {"diameter": 0.14, "strength": 3.0, "fish_weight": (2.0, 3.0)},
        "medium_heavy": {"diameter": 0.16, "strength": 4.0, "fish_weight": (3.0, 5.0)},
        "heavy": {"diameter": 0.18, "strength": 5.0, "fish_weight": (5.0, 8.0)},
        "ultra_heavy": {"diameter": 0.20, "strength": 6.5, "fish_weight": (8.0, 15.0)},
        "super_heavy": {"diameter": 0.25, "strength": 10.0, "fish_weight": (15.0, 30.0)},
    }

    # 子线规格（通常比主线细0.02-0.04mm）
    SUBLINE_RATIO = 0.8

    @classmethod
    def recommend_line(
        cls,
        target_fish: FishType,
        max_fish_weight: float,
        water_type: str = "still",
        line_type: str = "nylon",
    ) -> Dict[str, Any]:
        """
        推荐鱼线配置

        Args:
            target_fish: 目标鱼种
            max_fish_weight: 最大目标鱼重（kg）
            water_type: 水域类型 (still, flowing, sea)
            line_type: 线材类型 (nylon, fluorocarbon, pe)

        Returns:
            鱼线配置推荐
        """
        # 根据目标鱼重选择线号
        main_line = cls._select_line_by_weight(max_fish_weight)

        # 计算子线
        subline_diameter = round(main_line["diameter"] * cls.SUBLINE_RATIO, 2)
        subline_strength = round(main_line["strength"] * cls.SUBLINE_RATIO, 1)

        # 根据水域调整
        if water_type == "flowing":
            # 流水需要更结实的线
            main_line = cls._select_line_by_weight(max_fish_weight * 1.2)
        elif water_type == "sea":
            # 海钓需要更粗的线
            main_line = cls._select_line_by_weight(max_fish_weight * 1.5)

        # 线材特性
        line_properties = cls._get_line_properties(line_type)

        return {
            "main_line": {
                "diameter": main_line["diameter"],
                "strength": main_line["strength"],
                "recommended_length": cls._recommend_mainline_length(water_type),
            },
            "subline": {
                "diameter": subline_diameter,
                "strength": subline_strength,
                "recommended_length": cls._recommend_subline_length(target_fish),
            },
            "line_type": line_type,
            "line_properties": line_properties,
            "target_fish": target_fish.value,
            "tips": cls._get_tips(target_fish, water_type),
        }

    @classmethod
    def _select_line_by_weight(cls, weight: float) -> Dict[str, float]:
        """根据鱼重选择线"""
        for spec in cls.MAIN_LINE_SPECS.values():
            min_weight, max_weight = spec["fish_weight"]
            if min_weight <= weight < max_weight:
                return spec
        # 超大鱼
        return cls.MAIN_LINE_SPECS["super_heavy"]

    @classmethod
    def _get_line_properties(cls, line_type: str) -> Dict[str, Any]:
        """获取线材特性"""
        properties = {
            "nylon": {
                "name": "尼龙线",
                "stretch": "中等",
                "visibility": "中等",
                "abrasion_resistance": "中等",
                "knot_strength": "良好",
                "price": "经济",
                "pros": ["价格实惠", "结节强度好", "适合新手"],
                "cons": ["有延展性", "易老化"],
            },
            "fluorocarbon": {
                "name": "碳氟线",
                "stretch": "低",
                "visibility": "低（几乎隐形）",
                "abrasion_resistance": "高",
                "knot_strength": "中等",
                "price": "较高",
                "pros": ["隐蔽性好", "耐磨", "切水快"],
                "cons": ["价格较高", "结节需注意"],
            },
            "pe": {
                "name": "PE线（编织线）",
                "stretch": "极低",
                "visibility": "高",
                "abrasion_resistance": "高",
                "knot_strength": "高",
                "price": "高",
                "pros": ["强度极高", "无延展", "感度好"],
                "cons": ["价格高", "可见度高", "需配合前导"],
            },
        }
        return properties.get(line_type, properties["nylon"])

    @classmethod
    def _recommend_mainline_length(cls, water_type: str) -> str:
        """推荐主线长度"""
        lengths = {
            "still": "主线长度约为竿长的1.5-2倍",
            "flowing": "主线长度约为竿长的2-2.5倍",
            "sea": "主线长度根据钓法，一般100-200米",
        }
        return lengths.get(water_type, lengths["still"])

    @classmethod
    def _recommend_subline_length(cls, fish_type: FishType) -> str:
        """推荐子线长度"""
        # 根据鱼种习性推荐
        lengths = {
            FishType.CRUCIAN: "子线长度15-20cm",
            FishType.CARP: "子线长度20-30cm",
            FishType.CATFISH: "子线长度25-35cm",
            FishType.GRASS_CARP: "子线长度25-35cm",
            FishType.SILVER_CARP: "子线长度20-30cm",
            FishType.TILAPIA: "子线长度15-20cm",
            FishType.BASS: "前导线30-50cm",
            FishType.TROUT: "前导线40-60cm",
            FishType.PERCH: "前导线30-50cm",
            FishType.PIKE: "前导线50-80cm（金属前导）",
        }
        return lengths.get(fish_type, "子线长度20-30cm")

    @classmethod
    def _get_tips(cls, fish_type: FishType, water_type: str) -> List[str]:
        """获取使用建议"""
        tips = []

        # 鱼种建议
        fish_tips = {
            FishType.CRUCIAN: ["鲫鱼口轻，子线宜细", "调漂要灵敏"],
            FishType.CARP: ["鲤鱼力大，线组要结实", "中鱼后注意控鱼"],
            FishType.CATFISH: ["鲶鱼牙齿锋利，建议金属前导", "傍晚夜钓效果好"],
            FishType.GRASS_CARP: ["草鱼冲劲大，注意泄力", "可适当加长子线"],
            FishType.BASS: ["路亚建议用碳线前导", "注意配合假饵"],
            FishType.PIKE: ["必须使用金属前导", "牙齿锋利防切线"],
        }
        tips.extend(fish_tips.get(fish_type, []))

        # 水域建议
        if water_type == "flowing":
            tips.append("流水环境注意线的切水性")
        elif water_type == "sea":
            tips.append("海钓注意线的耐盐腐蚀")

        return tips


class BaitCalculator:
    """打窝料计算器"""

    # 窝料配方模板
    BAIT_RECIPES = {
        "spring_carb": {
            "name": "春季素窝",
            "ingredients": [
                {"name": "商品饵", "amount": 200, "unit": "g"},
                {"name": "玉米粒", "amount": 100, "unit": "g"},
                {"name": "小麦", "amount": 50, "unit": "g"},
            ],
            "water_ratio": 0.8,
            "target": [FishType.CRUCIAN, FishType.CARP],
            "season": ["spring"],
        },
        "summer_vegetable": {
            "name": "夏季果蔬窝",
            "ingredients": [
                {"name": "发酵玉米", "amount": 200, "unit": "g"},
                {"name": "小麦粒", "amount": 100, "unit": "g"},
                {"name": "豆饼", "amount": 100, "unit": "g"},
            ],
            "water_ratio": 0.6,
            "target": [FishType.GRASS_CARP, FishType.CARP],
            "season": ["summer"],
        },
        "autumn_protein": {
            "name": "秋季高蛋白窝",
            "ingredients": [
                {"name": "商品饵", "amount": 150, "unit": "g"},
                {"name": "蚕蛹粉", "amount": 50, "unit": "g"},
                {"name": "麝香米", "amount": 30, "unit": "g"},
            ],
            "water_ratio": 0.9,
            "target": [FishType.CARP, FishType.CATFISH],
            "season": ["autumn"],
        },
        "winter_warm": {
            "name": "冬季暖窝",
            "ingredients": [
                {"name": "红虫", "amount": 50, "unit": "g"},
                {"name": "蚯蚓段", "amount": 50, "unit": "g"},
                {"name": "商品饵", "amount": 100, "unit": "g"},
            ],
            "water_ratio": 1.0,
            "target": [FishType.CRUCIAN, FishType.CARP],
            "season": ["winter"],
        },
        "catfish_special": {
            "name": "鲶鱼腥窝",
            "ingredients": [
                {"name": "鸡肝", "amount": 100, "unit": "g"},
                {"name": "蚯蚓", "amount": 50, "unit": "g"},
                {"name": "商品饵(腥味)", "amount": 100, "unit": "g"},
            ],
            "water_ratio": 0.5,
            "target": [FishType.CATFISH],
            "season": ["spring", "summer", "autumn"],
        },
        "lure_bait": {
            "name": "路亚假饵建议",
            "ingredients": [
                {"name": "软饵", "amount": 1, "unit": "套"},
                {"name": "亮片", "amount": 1, "unit": "个"},
                {"name": "米诺", "amount": 1, "unit": "个"},
            ],
            "water_ratio": 0,
            "target": [FishType.BASS, FishType.PIKE, FishType.PERCH],
            "season": ["spring", "summer", "autumn"],
        },
    }

    @classmethod
    def calculate_bait(
        cls,
        target_fish: List[FishType],
        session_duration: float,  # 小时
        season: str,
        water_area: float = 100,  # 平方米
    ) -> Dict[str, Any]:
        """
        计算打窝料配置

        Args:
            target_fish: 目标鱼种
            session_duration: 作钓时长（小时）
            season: 季节
            water_area: 水域面积（平方米）

        Returns:
            窝料配置
        """
        # 找到匹配的配方
        matching_recipes = []
        for recipe_key, recipe in cls.BAIT_RECIPES.items():
            # 检查鱼种匹配
            fish_match = any(fish in recipe["target"] for fish in target_fish)
            # 检查季节匹配
            season_match = season in recipe["season"]

            if fish_match and season_match:
                matching_recipes.append((recipe_key, recipe))

        if not matching_recipes:
            # 如果没有完美匹配，选择季节合适的
            for recipe_key, recipe in cls.BAIT_RECIPES.items():
                if season in recipe["season"]:
                    matching_recipes.append((recipe_key, recipe))

        if not matching_recipes:
            matching_recipes = list(cls.BAIT_RECIPES.items())[:1]

        # 选择最佳配方
        best_recipe_key, best_recipe = matching_recipes[0]

        # 根据时长和面积调整用量
        duration_factor = session_duration / 4.0  # 以4小时为基准
        area_factor = water_area / 100.0  # 以100平方米为基准
        adjustment_factor = max(0.5, min(2.0, duration_factor * area_factor))

        adjusted_ingredients = []
        for ingredient in best_recipe["ingredients"]:
            adjusted_ingredients.append({
                "name": ingredient["name"],
                "amount": round(ingredient["amount"] * adjustment_factor),
                "unit": ingredient["unit"],
            })

        return {
            "recipe_name": best_recipe["name"],
            "recipe_key": best_recipe_key,
            "adjusted_for": {
                "duration": f"{session_duration}小时",
                "water_area": f"{water_area}平方米",
            },
            "ingredients": adjusted_ingredients,
            "water_ratio": best_recipe["water_ratio"],
            "target_fish": [f.value for f in best_recipe["target"]],
            "total_weight": sum(i["amount"] for i in adjusted_ingredients),
            "preparation_tips": cls._get_preparation_tips(best_recipe_key),
        }

    @classmethod
    def _get_preparation_tips(cls, recipe_key: str) -> List[str]:
        """获取制备建议"""
        tips = {
            "spring_carb": [
                "提前30分钟和饵，让饵料充分吸水",
                "饵料状态宜软不宜硬",
                "可添加少量酒米增强诱鱼效果",
            ],
            "summer_vegetable": [
                "玉米可提前一天发酵",
                "小麦提前泡软",
                "夏季可适当减少商品饵比例",
            ],
            "autumn_protein": [
                "蚕蛹粉气味浓郁，用量不宜过多",
                "可添加少量香精增强诱鱼",
                "秋季鱼食欲强，窝料可适当增加",
            ],
            "winter_warm": [
                "红虫需保持活性",
                "饵料宜小不宜大",
                "可添加腥味剂刺激鱼开口",
            ],
            "catfish_special": [
                "鸡肝需新鲜，切成小块",
                "傍晚打窝效果更佳",
                "可添加大蒜汁增强腥味",
            ],
            "lure_bait": [
                "软饵需定期更换保持形状",
                "根据水层选择沉水或浮水假饵",
                "亮片适合白天使用",
            ],
        }
        return tips.get(recipe_key, ["根据实际情况灵活调整"])


class FishingReportGenerator:
    """钓鱼报告生成器"""

    @classmethod
    def generate_report(
        cls,
        session: FishingSession,
        include_analysis: bool = True,
    ) -> str:
        """
        生成钓鱼报告

        Args:
            session: 钓鱼会话数据
            include_analysis: 是否包含分析

        Returns:
            格式化的报告文本
        """
        lines = []
        lines.append("=" * 50)
        lines.append("🎣 钓鱼报告")
        lines.append("=" * 50)
        lines.append("")

        # 基本信息
        lines.append("📍 基本信息")
        lines.append("-" * 30)
        lines.append(f"地点: {session.location}")
        lines.append(f"开始时间: {session.start_time.strftime('%Y-%m-%d %H:%M')}")
        if session.end_time:
            lines.append(f"结束时间: {session.end_time.strftime('%Y-%m-%d %H:%M')}")

        duration = session.get_duration()
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        lines.append(f"作钓时长: {hours}小时{minutes}分钟")
        lines.append("")

        # 天气信息
        if session.weather:
            lines.append("🌤️ 天气情况")
            lines.append("-" * 30)
            lines.append(f"天气: {session.weather.condition.value}")
            lines.append(f"气温: {session.weather.temperature}°C")
            lines.append(f"气压: {session.weather.pressure}hPa")
            lines.append(f"湿度: {session.weather.humidity}%")
            lines.append(f"风速: {session.weather.wind_speed}m/s")
            lines.append("")

        # 渔获统计
        lines.append("🐟 渔获统计")
        lines.append("-" * 30)
        lines.append(f"总尾数: {session.total_count}尾")
        lines.append(f"总重量: {session.total_weight:.2f}kg")

        if session.total_count > 0:
            avg_weight = session.total_weight / session.total_count
            lines.append(f"平均重量: {avg_weight:.2f}kg")
            catch_rate = session.get_catch_rate()
            lines.append(f"上鱼率: {catch_rate:.2f}尾/小时")

        lines.append("")

        # 渔获明细
        if session.catches:
            lines.append("📋 渔获明细")
            lines.append("-" * 30)

            # 按鱼种统计
            fish_stats = {}
            for catch in session.catches:
                fish_name = catch.fish_type.value
                if fish_name not in fish_stats:
                    fish_stats[fish_name] = {"count": 0, "total_weight": 0, "max_weight": 0}
                fish_stats[fish_name]["count"] += 1
                fish_stats[fish_name]["total_weight"] += catch.weight
                fish_stats[fish_name]["max_weight"] = max(
                    fish_stats[fish_name]["max_weight"], catch.weight
                )

            for fish_name, stats in fish_stats.items():
                avg = stats["total_weight"] / stats["count"]
                lines.append(
                    f"{fish_name}: {stats['count']}尾, "
                    f"总重{stats['total_weight']:.2f}kg, "
                    f"最大{stats['max_weight']:.2f}kg, "
                    f"均重{avg:.2f}kg"
                )

            lines.append("")

        # 分析建议
        if include_analysis and session.catches:
            lines.append("📊 分析建议")
            lines.append("-" * 30)
            analysis = cls._analyze_session(session)
            for tip in analysis:
                lines.append(f"• {tip}")

        lines.append("")
        lines.append("=" * 50)
        lines.append("祝下次爆护！🎣")

        return "\n".join(lines)

    @classmethod
    def _analyze_session(cls, session: FishingSession) -> List[str]:
        """分析钓鱼会话"""
        tips = []

        # 时段分析
        if session.catches:
            hours = [c.catch_time.hour for c in session.catches]
            most_catch_hour = max(set(hours), key=hours.count)

            if 5 <= most_catch_hour <= 9:
                tips.append("早晨时段上鱼率最高，建议抓住黄金时段")
            elif 17 <= most_catch_hour <= 20:
                tips.append("傍晚时段效果最佳，适合专注作钓")
            else:
                tips.append(f"上鱼高峰在{most_catch_hour}点，可根据此调整出钓时间")

        # 天气分析
        if session.weather:
            weather_index = FishingWeatherIndex.calculate_index(session.weather)
            tips.append(f"当日钓鱼气象指数: {weather_index['level']}({weather_index['total_score']}分)")

            if weather_index["total_score"] < 60:
                tips.append("气象条件一般，建议下次关注天气变化")

        # 渔获分析
        if session.total_count > 0:
            catch_rate = session.get_catch_rate()
            if catch_rate >= 3:
                tips.append("渔获出色！继续保持当前的钓组和饵料配置")
            elif catch_rate >= 1:
                tips.append("渔获正常，可尝试调整饵料或钓位提升效果")
            else:
                tips.append("渔获较少，建议检查饵料状态、调漂准确性，或更换钓位")

        return tips


# 便捷函数
def get_fishing_weather_index(
    temperature: float,
    pressure: float,
    humidity: float,
    wind_speed: float,
    condition: str,
) -> Dict[str, Any]:
    """
    快速获取钓鱼气象指数

    Args:
        temperature: 温度（摄氏度）
        pressure: 气压（hPa）
        humidity: 湿度（%）
        wind_speed: 风速（m/s）
        condition: 天气状况名称

    Returns:
        钓鱼气象指数评估
    """
    # 转换天气状况
    condition_map = {
        "晴": WeatherCondition.SUNNY,
        "晴朗": WeatherCondition.SUNNY,
        "多云": WeatherCondition.CLOUDY,
        "阴": WeatherCondition.OVERCAST,
        "小雨": WeatherCondition.LIGHT_RAIN,
        "中雨": WeatherCondition.MODERATE_RAIN,
        "大雨": WeatherCondition.HEAVY_RAIN,
        "雾": WeatherCondition.FOGGY,
        "大风": WeatherCondition.WINDY,
    }
    weather_condition = condition_map.get(condition, WeatherCondition.CLOUDY)

    weather = WeatherData(
        temperature=temperature,
        pressure=pressure,
        humidity=humidity,
        wind_speed=wind_speed,
        wind_direction="",
        condition=weather_condition,
    )

    return FishingWeatherIndex.calculate_index(weather)


def get_best_fishing_times(date: datetime = None) -> Dict[str, Any]:
    """
    获取最佳钓鱼时间

    Args:
        date: 日期，默认今天

    Returns:
        最佳钓鱼时间推荐
    """
    if date is None:
        date = datetime.now()

    return FishingTimePredictor.get_best_times(date)


def get_moon_phase_info(date: datetime = None) -> Dict[str, Any]:
    """
    获取月相信息

    Args:
        date: 日期，默认今天

    Returns:
        月相信息和钓鱼建议
    """
    if date is None:
        date = datetime.now()

    return MoonPhaseCalculator.get_fishing_quality(date)


def recommend_rod(
    fish_types: List[str],
    water_type: str,
    style: str = "casual",
    budget: str = "medium",
) -> List[Dict[str, Any]]:
    """
    推荐鱼竿

    Args:
        fish_types: 目标鱼种名称列表
        water_type: 水域类型
        style: 钓鱼风格
        budget: 预算

    Returns:
        鱼竿推荐列表
    """
    # 转换鱼种名称
    fish_type_map = {
        "鲤鱼": FishType.CARP,
        "鲫鱼": FishType.CRUCIAN,
        "鲶鱼": FishType.CATFISH,
        "草鱼": FishType.GRASS_CARP,
        "鲢鱼": FishType.SILVER_CARP,
        "罗非鱼": FishType.TILAPIA,
        "鲈鱼": FishType.BASS,
        "鳟鱼": FishType.TROUT,
        "河鲈": FishType.PERCH,
        "狗鱼": FishType.PIKE,
    }

    target_fish = []
    for name in fish_types:
        if name in fish_type_map:
            target_fish.append(fish_type_map[name])

    return RodSelector.recommend(target_fish, water_type, style, budget)


if __name__ == "__main__":
    # 简单测试
    print("🎣 钓鱼助手工具测试")
    print("=" * 50)

    # 测试气象指数
    print("\n1. 钓鱼气象指数测试")
    weather_index = get_fishing_weather_index(
        temperature=22,
        pressure=1013,
        humidity=65,
        wind_speed=3.0,
        condition="多云",
    )
    print(f"综合评分: {weather_index['total_score']}")
    print(f"等级: {weather_index['level']}")
    print(f"建议: {weather_index['recommendation']}")

    # 测试最佳时间
    print("\n2. 最佳钓鱼时间测试")
    times = get_best_fishing_times()
    print(f"季节: {times['season']}")
    print(f"描述: {times['description']}")
    for t in times["recommended_times"]:
        print(f"  {t['period']}: {t['time_range']} ({t['quality']})")

    # 测试月相
    print("\n3. 月相钓鱼质量测试")
    moon_info = get_moon_phase_info()
    print(f"月相: {moon_info['phase']}")
    print(f"照明度: {moon_info['illumination']}%")
    print(f"评分: {moon_info['score']}")
    print(f"最佳时段: {', '.join(moon_info['best_time'])}")

    print("\n✅ 测试完成")