"""
Hydration Utils - 水分摄入追踪工具

零依赖的水分摄入追踪库，支持：
- 每日饮水量计算（基于体重、活动量、气候）
- 实时水分状态追踪
- 饮水提醒建议
- 咖啡因和酒精的利尿影响计算
- 运动补水建议
- 水分平衡报告生成

Author: AllToolkit
License: MIT
"""

from datetime import datetime, timedelta, date
from typing import Optional, List, Dict, Tuple
from enum import Enum
from dataclasses import dataclass, field
import math


class ActivityLevel(Enum):
    """活动水平"""
    SEDENTARY = "sedentary"        # 久坐不动
    LIGHT = "light"                # 轻度活动
    MODERATE = "moderate"          # 中度活动
    ACTIVE = "active"              # 活跃
    VERY_ACTIVE = "very_active"    # 非常活跃


class ClimateType(Enum):
    """气候类型"""
    COOL = "cool"          # 凉爽 (< 20°C)
    TEMPERATE = "temperate"  # 温和 (20-25°C)
    WARM = "warm"          # 温暖 (25-30°C)
    HOT = "hot"            # 炎热 (> 30°C)


class BeverageType(Enum):
    """饮料类型"""
    WATER = "water"                    # 纯净水
    SPARKLING_WATER = "sparkling"      # 气泡水
    TEA = "tea"                        # 茶
    COFFEE = "coffee"                  # 咖啡
    SPORTS_DRINK = "sports_drink"      # 运动饮料
    JUICE = "juice"                    # 果汁
    MILK = "milk"                      # 牛奶
    SODA = "soda"                      # 碳酸饮料
    ALCOHOL_BEER = "beer"              # 啤酒
    ALCOHOL_WINE = "wine"              # 葡萄酒
    ALCOHOL_SPIRITS = "spirits"        # 烈酒
    SOUP = "soup"                      # 汤


class HydrationStatus(Enum):
    """水分状态"""
    DEHYDRATED_SEVERE = "severe_dehydration"   # 严重脱水
    DEHYDRATED_MODERATE = "moderate_dehydration"  # 中度脱水
    DEHYDRATED_MILD = "mild_dehydration"       # 轻度脱水
    OPTIMAL = "optimal"                         # 最佳状态
    OVERHYDRATED = "overhydrated"              # 过度补水


@dataclass
class Beverage:
    """饮料记录"""
    beverage_type: BeverageType
    volume_ml: float
    timestamp: datetime = field(default_factory=datetime.now)
    caffeine_mg: float = 0
    alcohol_percent: float = 0
    
    @property
    def hydration_value(self) -> float:
        """
        计算饮料的有效补水值（ml）
        
        考虑咖啡因和酒精的利尿作用
        """
        base_value = self.volume_ml
        
        # 咖啡因利尿影响（每100mg咖啡因减少约10%补水效果）
        if self.caffeine_mg > 0:
            caffeine_factor = 1 - min(0.5, self.caffeine_mg / 100 * 0.1)
            base_value *= caffeine_factor
        
        # 酒精利尿影响
        if self.alcohol_percent > 0:
            # 酒精含量越高，利尿效果越强
            alcohol_factor = 1 - min(0.7, self.alcohol_percent * 0.03)
            base_value *= alcohol_factor
        
        return base_value


@dataclass
class DailyLog:
    """每日饮水日志"""
    date: date
    beverages: List[Beverage] = field(default_factory=list)
    weight_kg: Optional[float] = None
    activity_level: ActivityLevel = ActivityLevel.MODERATE
    climate: ClimateType = ClimateType.TEMPERATE
    exercise_minutes: int = 0
    
    @property
    def total_intake_ml(self) -> float:
        """总摄入量"""
        return sum(b.volume_ml for b in self.beverages)
    
    @property
    def effective_hydration_ml(self) -> float:
        """有效补水量"""
        return sum(b.hydration_value for b in self.beverages)
    
    @property
    def total_caffeine_mg(self) -> float:
        """总咖啡因摄入"""
        return sum(b.caffeine_mg for b in self.beverages)
    
    @property
    def water_intake_ml(self) -> float:
        """纯水摄入量"""
        return sum(b.volume_ml for b in self.beverages 
                   if b.beverage_type == BeverageType.WATER)


class HydrationError(Exception):
    """水分追踪相关错误的基类"""
    pass


class InvalidInputError(HydrationError):
    """无效输入"""
    pass


# 常量定义
# 基础水需求：每公斤体重约30-35ml
BASE_WATER_PER_KG = 32  # ml/kg

# 活动量修正系数
ACTIVITY_MULTIPLIERS = {
    ActivityLevel.SEDENTARY: 1.0,
    ActivityLevel.LIGHT: 1.1,
    ActivityLevel.MODERATE: 1.2,
    ActivityLevel.ACTIVE: 1.3,
    ActivityLevel.VERY_ACTIVE: 1.4
}

# 气候修正系数
CLIMATE_MULTIPLIERS = {
    ClimateType.COOL: 0.9,
    ClimateType.TEMPERATE: 1.0,
    ClimateType.WARM: 1.15,
    ClimateType.HOT: 1.3
}

# 运动额外补水（每分钟运动额外需要的ml）
EXERCISE_WATER_PER_MINUTE = 10

# 饮料咖啡因含量参考（每100ml）
CAFFEINE_CONTENT = {
    BeverageType.COFFEE: 40,      # 普通咖啡
    BeverageType.TEA: 20,         # 茶
    BeverageType.SODA: 10,        # 可乐等
}

# 饮料酒精含量参考（体积百分比）
ALCOHOL_CONTENT = {
    BeverageType.ALCOHOL_BEER: 5,
    BeverageType.ALCOHOL_WINE: 12,
    BeverageType.ALCOHOL_SPIRITS: 40,
}

# 饮水时间建议
OPTIMAL_DRINKING_INTERVALS = 60  # 分钟，建议每小时饮水一次
HOURLY_TARGET_RATIO = 1/12       # 每小时目标 = 日总量的1/12（醒着12小时计算）


def calculate_daily_water_needs(
    weight_kg: float,
    age: int = 30,
    gender: str = "male",
    activity_level: ActivityLevel = ActivityLevel.MODERATE,
    climate: ClimateType = ClimateType.TEMPERATE,
    exercise_minutes: int = 0,
    is_pregnant: bool = False,
    is_breastfeeding: bool = False
) -> Dict[str, float]:
    """
    计算每日水需求量
    
    基于多项因素综合计算：
    - 基础需求：体重 × 32ml/kg
    - 活动量调整
    - 气候调整
    - 运动额外需求
    - 特殊状态调整（孕期/哺乳期）
    
    Args:
        weight_kg: 体重（公斤）
        age: 年龄
        gender: 性别 (male/female)
        activity_level: 活动水平
        climate: 气候类型
        exercise_minutes: 运动时长（分钟）
        is_pregnant: 是否怀孕
        is_breastfeeding: 是否哺乳
    
    Returns:
        包含各项需求数据的字典
    """
    if weight_kg <= 0:
        raise InvalidInputError("体重必须大于0")
    
    # 基础需求
    base_need = weight_kg * BASE_WATER_PER_KG
    
    # 活动量调整
    activity_mult = ACTIVITY_MULTIPLIERS.get(activity_level, 1.0)
    adjusted_need = base_need * activity_mult
    
    # 气候调整
    climate_mult = CLIMATE_MULTIPLIERS.get(climate, 1.0)
    adjusted_need *= climate_mult
    
    # 年龄调整（老年人需水量略减）
    if age >= 65:
        adjusted_need *= 0.95
    elif age < 18:
        adjusted_need *= 0.9
    
    # 性别调整（女性通常略少）
    if gender.lower() == "female" and not is_pregnant and not is_breastfeeding:
        adjusted_need *= 0.95
    
    # 运动额外补水
    exercise_need = exercise_minutes * EXERCISE_WATER_PER_MINUTE
    
    # 孕期/哺乳期调整
    pregnancy_addition = 0
    if is_pregnant:
        pregnancy_addition = 300  # 孕期额外300ml
    if is_breastfeeding:
        pregnancy_addition = 700  # 哺乳期额外700ml
    
    total_need = adjusted_need + exercise_need + pregnancy_addition
    
    return {
        "base_need_ml": round(base_need),
        "activity_adjusted_ml": round(adjusted_need),
        "exercise_addition_ml": round(exercise_need),
        "pregnancy_addition_ml": pregnancy_addition,
        "total_need_ml": round(total_need),
        "recommended_glasses": round(total_need / 250, 1),  # 250ml每杯
        "hourly_target_ml": round(total_need / 12),  # 每小时目标（假设醒着12小时）
    }


def calculate_hydration_status(
    current_intake_ml: float,
    target_ml: float,
    hours_elapsed: float = 12
) -> Tuple[HydrationStatus, float]:
    """
    计算当前水分状态
    
    Args:
        current_intake_ml: 当前摄入量
        target_ml: 目标摄入量
        hours_elapsed: 已过小时数
    
    Returns:
        (水分状态, 完成百分比)
    """
    if target_ml <= 0:
        return HydrationStatus.OPTIMAL, 100.0
    
    # 计算预期进度
    expected_ratio = min(1.0, hours_elapsed / 12)  # 假设12小时醒着
    expected_intake = target_ml * expected_ratio
    
    # 实际进度
    actual_ratio = current_intake_ml / target_ml
    
    # 完成百分比
    completion_pct = min(100, actual_ratio * 100)
    
    # 判断状态
    ratio = actual_ratio / expected_ratio if expected_ratio > 0 else actual_ratio
    
    if ratio < 0.5:
        return HydrationStatus.DEHYDRATED_SEVERE, completion_pct
    elif ratio < 0.7:
        return HydrationStatus.DEHYDRATED_MODERATE, completion_pct
    elif ratio < 0.9:
        return HydrationStatus.DEHYDRATED_MILD, completion_pct
    elif ratio <= 1.1:
        return HydrationStatus.OPTIMAL, completion_pct
    else:
        return HydrationStatus.OVERHYDRATED, completion_pct


def get_drinking_schedule(
    target_ml: float,
    wake_time: str = "07:00",
    sleep_time: str = "23:00",
    intervals: int = 12
) -> List[Dict]:
    """
    生成饮水时间表
    
    Args:
        target_ml: 目标摄入量
        wake_time: 起床时间 (HH:MM)
        sleep_time: 睡眠时间 (HH:MM)
        intervals: 饮水次数
    
    Returns:
        饮水时间表列表
    """
    wake = datetime.strptime(wake_time, "%H:%M")
    sleep = datetime.strptime(sleep_time, "%H:%M")
    
    # 处理跨午夜情况
    if sleep <= wake:
        sleep += timedelta(days=1)
    
    awake_minutes = (sleep - wake).seconds / 60
    interval_minutes = awake_minutes / intervals
    
    per_intake = target_ml / intervals
    
    schedule = []
    current_time = wake
    
    for i in range(intervals):
        schedule.append({
            "time": current_time.strftime("%H:%M"),
            "amount_ml": round(per_intake),
            "cumulative_ml": round(per_intake * (i + 1)),
            "percentage": round((i + 1) / intervals * 100, 1)
        })
        current_time += timedelta(minutes=interval_minutes)
    
    return schedule


def calculate_beverage_hydration(
    beverage_type: BeverageType,
    volume_ml: float
) -> Dict[str, float]:
    """
    计算特定饮料的有效补水量
    
    Args:
        beverage_type: 饮料类型
        volume_ml: 容量（毫升）
    
    Returns:
        包含补水效果的字典
    """
    beverage = Beverage(
        beverage_type=beverage_type,
        volume_ml=volume_ml
    )
    
    # 设置默认咖啡因含量
    if beverage_type in CAFFEINE_CONTENT:
        beverage.caffeine_mg = CAFFEINE_CONTENT[beverage_type] * volume_ml / 100
    
    # 设置默认酒精含量
    if beverage_type in ALCOHOL_CONTENT:
        beverage.alcohol_percent = ALCOHOL_CONTENT[beverage_type]
    
    return {
        "volume_ml": volume_ml,
        "effective_hydration_ml": round(beverage.hydration_value, 1),
        "caffeine_mg": beverage.caffeine_mg,
        "alcohol_percent": beverage.alcohol_percent,
        "hydration_efficiency": round(beverage.hydration_value / volume_ml * 100, 1)
    }


def estimate_water_from_foods(foods: List[Dict]) -> float:
    """
    估算食物中的水分含量
    
    常见食物含水量参考：
    - 水果：约80-90%
    - 蔬菜：约90-95%
    - 汤类：约90-95%
    - 米饭：约65-70%
    - 肉类：约60-70%
    
    Args:
        foods: 食物列表，每项包含 name, weight_g, water_percent
    
    Returns:
        估算的总水分含量（毫升）
    """
    total_water = 0.0
    
    for food in foods:
        weight_g = food.get("weight_g", 0)
        water_percent = food.get("water_percent", 70)  # 默认70%
        total_water += weight_g * water_percent / 100
    
    return round(total_water)


# 常见食物含水量参考
FOOD_WATER_CONTENT = {
    "watermelon": 92,
    "cucumber": 96,
    "tomato": 94,
    "orange": 87,
    "apple": 86,
    "banana": 75,
    "grapes": 81,
    "strawberry": 91,
    "soup": 90,
    "rice": 70,
    "pasta": 65,
    "bread": 35,
    "chicken": 65,
    "beef": 60,
    "fish": 75,
    "egg": 75,
    "yogurt": 85,
    "milk": 87,
}


def get_exercise_hydration_plan(
    exercise_type: str,
    duration_minutes: int,
    intensity: str = "moderate",
    weight_kg: float = 70,
    temperature_celsius: float = 22
) -> Dict:
    """
    生成运动补水计划
    
    Args:
        exercise_type: 运动类型
        duration_minutes: 运动时长
        intensity: 强度 (low/moderate/high/extreme)
        weight_kg: 体重
        temperature_celsius: 环境温度
    
    Returns:
        补水计划字典
    """
    # 基础出汗率（ml/分钟）
    base_sweat_rate = {
        "low": 8,
        "moderate": 12,
        "high": 18,
        "extreme": 25
    }
    
    rate = base_sweat_rate.get(intensity, 12)
    
    # 体重调整
    rate *= weight_kg / 70
    
    # 温度调整
    if temperature_celsius > 30:
        rate *= 1.3
    elif temperature_celsius > 25:
        rate *= 1.15
    elif temperature_celsius < 15:
        rate *= 0.85
    
    # 计算总失水量
    total_sweat = rate * duration_minutes
    
    # 补水建议
    # 运动前：2小时前500ml，30分钟前250ml
    # 运动中：每15-20分钟150-200ml
    # 运动后：每丢失1kg体重补充150%的水分
    
    during_exercise_intervals = duration_minutes // 20
    during_exercise_amount = min(200, during_exercise_intervals * 175)
    
    return {
        "exercise_type": exercise_type,
        "estimated_sweat_loss_ml": round(total_sweat),
        "pre_exercise": {
            "2_hours_before_ml": 500,
            "30_min_before_ml": 250
        },
        "during_exercise": {
            "interval_minutes": 15,
            "per_interval_ml": 175,
            "total_ml": during_exercise_amount
        },
        "post_exercise": {
            "recommended_ml": round(total_sweat * 1.5),
            "timing": "运动后2小时内完成"
        },
        "electrolyte_needed": intensity in ["high", "extreme"] and duration_minutes > 60,
        "sports_drink_recommended": intensity in ["high", "extreme"] or duration_minutes > 90
    }


def calculate_caffeine_impact(
    caffeine_mg: float,
    hours_since_intake: float = 0
) -> Dict:
    """
    计算咖啡因对水分的影响
    
    Args:
        caffeine_mg: 咖啡因摄入量（mg）
        hours_since_intake: 摄入后经过的小时数
    
    Returns:
        影响分析字典
    """
    # 无咖啡因时返回默认值
    if caffeine_mg <= 0:
        return {
            "initial_caffeine_mg": 0,
            "remaining_caffeine_mg": 0,
            "metabolized_percent": 100,
            "diuretic_effect_ml": 0,
            "sleep_disruption_risk": False,
            "safe_to_sleep": True,
            "recommended_wait_hours": 0
        }
    
    # 咖啡因半衰期约5-6小时
    half_life_hours = 5.5
    
    # 计算剩余咖啡因
    remaining = caffeine_mg * (0.5 ** (hours_since_intake / half_life_hours))
    
    # 利尿效果（额外流失的水分）
    # 每100mg咖啡因可能导致约100ml额外排尿
    diuretic_effect_ml = caffeine_mg / 100 * 100
    
    # 对睡眠的影响
    sleep_impact = remaining > 100
    
    return {
        "initial_caffeine_mg": caffeine_mg,
        "remaining_caffeine_mg": round(remaining, 1),
        "metabolized_percent": round((1 - remaining / caffeine_mg) * 100, 1),
        "diuretic_effect_ml": round(diuretic_effect_ml),
        "sleep_disruption_risk": sleep_impact,
        "safe_to_sleep": remaining < 100,
        "recommended_wait_hours": max(0, math.log(100 / caffeine_mg) / math.log(0.5) * half_life_hours) if caffeine_mg > 100 else 0
    }


def assess_dehydration_risk(
    daily_log: DailyLog,
    target_ml: float
) -> Dict:
    """
    评估脱水风险
    
    Args:
        daily_log: 每日日志
        target_ml: 目标摄入量
    
    Returns:
        风险评估结果
    """
    current_intake = daily_log.effective_hydration_ml
    now = datetime.now()
    
    # 计算已过时间比例
    day_start = datetime.combine(daily_log.date, datetime.min.time())
    hours_elapsed = (now - day_start).seconds / 3600 if now.date() == daily_log.date else 12
    
    status, completion = calculate_hydration_status(current_intake, target_ml, hours_elapsed)
    
    # 计算咖啡因影响
    caffeine_total = daily_log.total_caffeine_mg
    caffeine_impact = calculate_caffeine_impact(caffeine_total)
    
    # 生成风险等级和建议
    risk_level = "low"
    recommendations = []
    
    if status == HydrationStatus.DEHYDRATED_SEVERE:
        risk_level = "critical"
        recommendations.extend([
            "严重脱水！立即补充500ml水分",
            "避免含咖啡因饮料",
            "如出现头晕、乏力，请休息并补充电解质"
        ])
    elif status == HydrationStatus.DEHYDRATED_MODERATE:
        risk_level = "high"
        recommendations.extend([
            "水分摄入严重不足",
            "建议未来2小时内补充400-500ml水分",
            "设置定时提醒，每小时饮水一次"
        ])
    elif status == HydrationStatus.DEHYDRATED_MILD:
        risk_level = "moderate"
        recommendations.extend([
            "水分摄入略低于目标",
            "建议补充200-300ml水分"
        ])
    elif status == HydrationStatus.OVERHYDRATED:
        risk_level = "low"
        recommendations.append("水分摄入充足，注意不要过量饮水")
    else:
        risk_level = "low"
        recommendations.append("水分摄入良好，继续保持")
    
    # 咖啡因相关建议
    if caffeine_impact["remaining_caffeine_mg"] > 200:
        recommendations.append(
            f"咖啡因摄入较高（剩余约{caffeine_impact['remaining_caffeine_mg']:.0f}mg），"
            "建议增加水分补充以抵消利尿效果"
        )
    
    return {
        "risk_level": risk_level,
        "hydration_status": status.value,
        "completion_percentage": completion,
        "current_intake_ml": current_intake,
        "target_ml": target_ml,
        "deficit_ml": round(max(0, target_ml - current_intake)),
        "recommendations": recommendations,
        "caffeine_remaining_mg": caffeine_impact["remaining_caffeine_mg"]
    }


def generate_hydration_report(
    daily_log: DailyLog,
    target_ml: float
) -> Dict:
    """
    生成每日水分报告
    
    Args:
        daily_log: 每日日志
        target_ml: 目标摄入量
    
    Returns:
        完整报告字典
    """
    # 基本统计
    total_intake = daily_log.total_intake_ml
    effective_hydration = daily_log.effective_hydration_ml
    
    # 按饮料类型分组
    by_type = {}
    for b in daily_log.beverages:
        type_name = b.beverage_type.value
        if type_name not in by_type:
            by_type[type_name] = {"volume_ml": 0, "count": 0, "hydration_ml": 0}
        by_type[type_name]["volume_ml"] += b.volume_ml
        by_type[type_name]["count"] += 1
        by_type[type_name]["hydration_ml"] += b.hydration_value
    
    # 按小时分组
    hourly = {}
    for b in daily_log.beverages:
        hour = b.timestamp.strftime("%H:00")
        if hour not in hourly:
            hourly[hour] = 0
        hourly[hour] += b.volume_ml
    
    # 评估
    risk_assessment = assess_dehydration_risk(daily_log, target_ml)
    
    return {
        "date": daily_log.date.isoformat(),
        "summary": {
            "total_intake_ml": round(total_intake),
            "effective_hydration_ml": round(effective_hydration, 1),
            "target_ml": target_ml,
            "completion_percentage": round(effective_hydration / target_ml * 100, 1),
            "total_beverages": len(daily_log.beverages),
            "pure_water_ml": daily_log.water_intake_ml,
            "pure_water_percentage": round(daily_log.water_intake_ml / total_intake * 100, 1) if total_intake > 0 else 0
        },
        "by_beverage_type": by_type,
        "hourly_distribution": hourly,
        "hydration_efficiency": round(effective_hydration / total_intake * 100, 1) if total_intake > 0 else 100,
        "risk_assessment": risk_assessment,
        "recommendations": risk_assessment["recommendations"]
    }


class HydrationTracker:
    """水分追踪器 - 管理多日饮水记录"""
    
    def __init__(
        self,
        weight_kg: float = 70,
        activity_level: ActivityLevel = ActivityLevel.MODERATE,
        climate: ClimateType = ClimateType.TEMPERATE
    ):
        self.weight_kg = weight_kg
        self.activity_level = activity_level
        self.climate = climate
        self.daily_logs: Dict[date, DailyLog] = {}
    
    def _get_or_create_log(self, log_date: Optional[date] = None) -> DailyLog:
        """获取或创建日志"""
        if log_date is None:
            log_date = date.today()
        
        if log_date not in self.daily_logs:
            self.daily_logs[log_date] = DailyLog(
                date=log_date,
                weight_kg=self.weight_kg,
                activity_level=self.activity_level,
                climate=self.climate
            )
        
        return self.daily_logs[log_date]
    
    def log_beverage(
        self,
        beverage_type: BeverageType,
        volume_ml: float,
        timestamp: Optional[datetime] = None,
        caffeine_mg: float = 0,
        alcohol_percent: float = 0,
        log_date: Optional[date] = None
    ) -> Beverage:
        """记录饮料摄入"""
        if volume_ml <= 0:
            raise InvalidInputError("饮料容量必须大于0")
        
        log = self._get_or_create_log(log_date)
        
        beverage = Beverage(
            beverage_type=beverage_type,
            volume_ml=volume_ml,
            timestamp=timestamp or datetime.now(),
            caffeine_mg=caffeine_mg,
            alcohol_percent=alcohol_percent
        )
        
        log.beverages.append(beverage)
        return beverage
    
    def log_water(
        self,
        volume_ml: float,
        timestamp: Optional[datetime] = None,
        log_date: Optional[date] = None
    ) -> Beverage:
        """快速记录纯水"""
        return self.log_beverage(
            BeverageType.WATER,
            volume_ml,
            timestamp,
            log_date=log_date
        )
    
    def log_coffee(
        self,
        volume_ml: float,
        caffeine_mg: Optional[float] = None,
        timestamp: Optional[datetime] = None,
        log_date: Optional[date] = None
    ) -> Beverage:
        """快速记录咖啡"""
        if caffeine_mg is None:
            caffeine_mg = CAFFEINE_CONTENT[BeverageType.COFFEE] * volume_ml / 100
        
        return self.log_beverage(
            BeverageType.COFFEE,
            volume_ml,
            timestamp,
            caffeine_mg=caffeine_mg,
            log_date=log_date
        )
    
    def log_tea(
        self,
        volume_ml: float,
        caffeine_mg: Optional[float] = None,
        timestamp: Optional[datetime] = None,
        log_date: Optional[date] = None
    ) -> Beverage:
        """快速记录茶"""
        if caffeine_mg is None:
            caffeine_mg = CAFFEINE_CONTENT[BeverageType.TEA] * volume_ml / 100
        
        return self.log_beverage(
            BeverageType.TEA,
            volume_ml,
            timestamp,
            caffeine_mg=caffeine_mg,
            log_date=log_date
        )
    
    def get_daily_target(self, log_date: Optional[date] = None) -> float:
        """获取每日目标"""
        log = self._get_or_create_log(log_date)
        needs = calculate_daily_water_needs(
            weight_kg=log.weight_kg or self.weight_kg,
            activity_level=log.activity_level,
            climate=log.climate,
            exercise_minutes=log.exercise_minutes
        )
        return needs["total_need_ml"]
    
    def get_current_status(self, log_date: Optional[date] = None) -> Dict:
        """获取当前状态"""
        log = self._get_or_create_log(log_date)
        target = self.get_daily_target(log_date)
        return assess_dehydration_risk(log, target)
    
    def get_daily_report(self, log_date: Optional[date] = None) -> Dict:
        """获取每日报告"""
        log = self._get_or_create_log(log_date)
        target = self.get_daily_target(log_date)
        return generate_hydration_report(log, target)
    
    def get_weekly_summary(self) -> Dict:
        """获取周总结"""
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        daily_summaries = []
        total_intake = 0
        total_target = 0
        total_effective = 0
        
        for i in range(7):
            current_date = week_start + timedelta(days=i)
            if current_date in self.daily_logs:
                log = self.daily_logs[current_date]
                target = self.get_daily_target(current_date)
                intake = log.total_intake_ml
                effective = log.effective_hydration_ml
                
                daily_summaries.append({
                    "date": current_date.isoformat(),
                    "intake_ml": intake,
                    "effective_ml": effective,
                    "target_ml": target,
                    "completion": round(effective / target * 100, 1) if target > 0 else 0
                })
                
                total_intake += intake
                total_target += target
                total_effective += effective
        
        avg_completion = round(total_effective / total_target * 100, 1) if total_target > 0 else 0
        
        return {
            "week_start": week_start.isoformat(),
            "total_intake_ml": round(total_intake),
            "total_effective_ml": round(total_effective, 1),
            "daily_target_ml": round(total_target / 7) if len(daily_summaries) > 0 else 0,
            "average_completion": avg_completion,
            "days_logged": len(daily_summaries),
            "daily_summaries": daily_summaries
        }
    
    def get_drinking_reminder(self) -> Dict:
        """获取饮水提醒"""
        now = datetime.now()
        log = self._get_or_create_log(now.date())
        target = self.get_daily_target()
        
        # 计算今天应该喝多少
        hours_elapsed = now.hour + now.minute / 60
        
        # 假设从6点开始喝水，到22点结束
        drinking_hours = 16
        day_start_hour = 6
        
        elapsed_drinking_hours = max(0, min(drinking_hours, hours_elapsed - day_start_hour))
        
        expected_intake = target * (elapsed_drinking_hours / drinking_hours)
        current_intake = log.effective_hydration_ml
        
        if current_intake < expected_intake:
            deficit = expected_intake - current_intake
            return {
                "should_remind": True,
                "message": f"该喝水了！距目标还差{deficit:.0f}ml",
                "deficit_ml": round(deficit),
                "current_ml": round(current_intake),
                "target_ml": target,
                "suggested_amount_ml": min(250, round(deficit))
            }
        else:
            return {
                "should_remind": False,
                "message": "水分摄入充足，继续保持",
                "current_ml": round(current_intake),
                "target_ml": target
            }


def calculate_oral_rehydration_solution(
    weight_kg: float,
    dehydration_level: str = "mild"
) -> Dict:
    """
    计算口服补液盐配方
    
    用于轻度到中度脱水时的电解质补充
    
    Args:
        weight_kg: 体重
        dehydration_level: 脱水程度 (mild/moderate)
    
    Returns:
        ORS配方和建议
    """
    # WHO标准ORS配方
    # 葡萄糖20g + 氯化钠3.5g + 柠檬酸钠2.9g + 氯化钾1.5g
    # 溶于1升水中
    
    # 简化版家庭配方
    simplified_recipe = {
        "water_ml": 1000,
        "salt_g": 3,
        "sugar_g": 18
    }
    
    # 根据脱水程度计算需要量
    if dehydration_level == "mild":
        volume_per_kg = 50  # ml/kg
    else:  # moderate
        volume_per_kg = 100  # ml/kg
    
    total_volume = weight_kg * volume_per_kg
    
    # 分次服用建议
    first_hour = total_volume * 0.5  # 第一小时喝一半
    remaining = total_volume * 0.5   # 剩余在后续3-4小时喝完
    
    return {
        "standard_ors_per_liter": {
            "glucose_g": 20,
            "sodium_chloride_g": 3.5,
            "trisodium_citrate_g": 2.9,
            "potassium_chloride_g": 1.5
        },
        "simplified_home_recipe": simplified_recipe,
        "recommended_total_ml": round(total_volume),
        "administration": {
            "first_hour_ml": round(first_hour),
            "next_3_4_hours_ml": round(remaining),
            "sips": "少量多次，每次10-20ml"
        },
        "warning": "重度脱水请立即就医！"
    }


def get_weather_adjusted_target(
    base_target_ml: float,
    temperature_celsius: float,
    humidity_percent: float = 50,
    is_sunny: bool = True
) -> float:
    """
    根据天气调整水分目标
    
    Args:
        base_target_ml: 基础目标量
        temperature_celsius: 温度（摄氏度）
        humidity_percent: 湿度百分比
        is_sunny: 是否晴天
    
    Returns:
        调整后的目标量
    """
    adjusted = base_target_ml
    
    # 温度调整
    if temperature_celsius > 35:
        adjusted *= 1.4
    elif temperature_celsius > 30:
        adjusted *= 1.25
    elif temperature_celsius > 25:
        adjusted *= 1.1
    elif temperature_celsius <= 15:  # 凉爽天气（15°C或以下）
        adjusted *= 0.9
    
    # 湿度调整（高湿度减少汗液蒸发，需要更多水分）
    if humidity_percent > 80:
        adjusted *= 1.1
    elif humidity_percent < 30:
        adjusted *= 1.05  # 低湿度也会增加水分流失
    
    # 阳光直射增加水分需求
    if is_sunny and temperature_celsius > 20:
        adjusted *= 1.05
    
    return round(adjusted)


# 导出公共API
__all__ = [
    # 枚举和类
    'ActivityLevel',
    'ClimateType',
    'BeverageType',
    'HydrationStatus',
    'Beverage',
    'DailyLog',
    'HydrationError',
    'InvalidInputError',
    'HydrationTracker',
    # 核心函数
    'calculate_daily_water_needs',
    'calculate_hydration_status',
    'get_drinking_schedule',
    'calculate_beverage_hydration',
    'estimate_water_from_foods',
    'get_exercise_hydration_plan',
    'calculate_caffeine_impact',
    'assess_dehydration_risk',
    'generate_hydration_report',
    'calculate_oral_rehydration_solution',
    'get_weather_adjusted_target',
    # 常量
    'BASE_WATER_PER_KG',
    'ACTIVITY_MULTIPLIERS',
    'CLIMATE_MULTIPLIERS',
    'FOOD_WATER_CONTENT',
    'CAFFEINE_CONTENT',
    'ALCOHOL_CONTENT',
]