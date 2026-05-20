"""
Water Intake Utilities - 饮水量追踪工具

功能：
- 根据体重、活动水平、气候计算每日建议饮水量
- 追踪饮水量记录
- 生成饮水提醒时间表
- 分析饮水习惯
- 提供水分补给建议

零依赖，仅使用 Python 标准库
"""

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from enum import Enum
from typing import Optional, Callable, List, Tuple, Dict
import json
import math


class ActivityLevel(Enum):
    """活动水平"""
    SEDENTARY = "sedentary"      # 久坐不动
    LIGHT = "light"              # 轻度活动
    MODERATE = "moderate"        # 中度活动
    ACTIVE = "active"            # 活跃
    VERY_ACTIVE = "very_active"  # 非常活跃


class Climate(Enum):
    """气候类型"""
    COLD = "cold"          # 寒冷 (< 10°C)
    MILD = "mild"          # 温和 (10-20°C)
    WARM = "warm"          # 温暖 (20-25°C)
    HOT = "hot"            # 炎热 (25-30°C)
    VERY_HOT = "very_hot"  # 酷热 (> 30°C)


class DrinkType(Enum):
    """饮品类型"""
    WATER = "water"                    # 纯净水
    SPARKLING_WATER = "sparkling_water" # 气泡水
    TEA = "tea"                        # 茶
    COFFEE = "coffee"                  # 咖啡
    JUICE = "juice"                    # 果汁
    SPORTS_DRINK = "sports_drink"      # 运动饮料
    MILK = "milk"                      # 牛奶
    SOUP = "soup"                      # 汤


# 饮品水分含量系数（相对于纯水）
DRINK_HYDRATION_FACTOR = {
    DrinkType.WATER: 1.0,
    DrinkType.SPARKLING_WATER: 1.0,
    DrinkType.TEA: 0.95,
    DrinkType.COFFEE: 0.85,  # 咖啡有轻微利尿作用
    DrinkType.JUICE: 0.9,
    DrinkType.SPORTS_DRINK: 1.0,
    DrinkType.MILK: 0.9,
    DrinkType.SOUP: 0.85,
}


@dataclass
class DrinkRecord:
    """饮水记录"""
    timestamp: datetime
    amount_ml: float
    drink_type: DrinkType = DrinkType.WATER
    effective_ml: float = field(init=False)
    note: str = ""

    def __post_init__(self):
        self.effective_ml = self.amount_ml * DRINK_HYDRATION_FACTOR.get(self.drink_type, 1.0)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "amount_ml": self.amount_ml,
            "drink_type": self.drink_type.value,
            "effective_ml": self.effective_ml,
            "note": self.note
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DrinkRecord':
        # Python 3.6 不支持 fromisoformat，手动解析
        ts_str = data["timestamp"]
        # 尝试两种格式：带微秒和不带微秒
        try:
            timestamp = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            timestamp = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S")
        record = cls(
            timestamp=timestamp,
            amount_ml=data["amount_ml"],
            drink_type=DrinkType(data["drink_type"]),
            note=data.get("note", "")
        )
        return record


@dataclass
class DailySummary:
    """每日饮水汇总"""
    date: str  # YYYY-MM-DD
    total_ml: float
    effective_ml: float
    target_ml: float
    records: List[DrinkRecord] = field(default_factory=list)
    
    @property
    def completion_rate(self) -> float:
        """完成率"""
        if self.target_ml <= 0:
            return 0.0
        return min(1.0, self.effective_ml / self.target_ml)
    
    @property
    def is_goal_met(self) -> bool:
        """是否达成目标"""
        return self.effective_ml >= self.target_ml
    
    @property
    def deficit_ml(self) -> float:
        """缺口（负数表示超额）"""
        return self.target_ml - self.effective_ml


@dataclass
class HydrationStatus:
    """水分状态"""
    current_ml: float
    target_ml: float
    last_drink_time: Optional[datetime] = None
    
    @property
    def completion_rate(self) -> float:
        if self.target_ml <= 0:
            return 0.0
        return min(1.0, self.current_ml / self.target_ml)
    
    @property
    def remaining_ml(self) -> float:
        return max(0, self.target_ml - self.current_ml)
    
    @property
    def status_text(self) -> str:
        rate = self.completion_rate
        if rate < 0.3:
            return "💧 需要补水"
        elif rate < 0.6:
            return "💧💧 继续保持"
        elif rate < 0.9:
            return "💧💧💧 快达标了"
        else:
            return "✅ 今日目标达成！"


class WaterIntakeCalculator:
    """饮水量计算器"""
    
    # 基础水量系数（每公斤体重需要的毫升数）
    BASE_WATER_PER_KG = 30  # ml/kg
    
    # 活动水平调整系数
    ACTIVITY_MULTIPLIERS = {
        ActivityLevel.SEDENTARY: 1.0,
        ActivityLevel.LIGHT: 1.1,
        ActivityLevel.MODERATE: 1.2,
        ActivityLevel.ACTIVE: 1.3,
        ActivityLevel.VERY_ACTIVE: 1.4,
    }
    
    # 气候调整系数
    CLIMATE_MULTIPLIERS = {
        Climate.COLD: 0.9,
        Climate.MILD: 1.0,
        Climate.WARM: 1.1,
        Climate.HOT: 1.2,
        Climate.VERY_HOT: 1.3,
    }
    
    def __init__(
        self,
        weight_kg: float,
        activity_level: ActivityLevel = ActivityLevel.MODERATE,
        climate: Climate = Climate.MILD,
        age: Optional[int] = None,
        is_pregnant: bool = False,
        is_breastfeeding: bool = False,
    ):
        """
        初始化计算器
        
        Args:
            weight_kg: 体重（公斤）
            activity_level: 活动水平
            climate: 气候类型
            age: 年龄（可选，影响代谢）
            is_pregnant: 是否怀孕
            is_breastfeeding: 是否哺乳
        """
        self.weight_kg = weight_kg
        self.activity_level = activity_level
        self.climate = climate
        self.age = age
        self.is_pregnant = is_pregnant
        self.is_breastfeeding = is_breastfeeding
    
    def calculate_daily_target(self) -> float:
        """
        计算每日建议饮水量（毫升）
        
        Returns:
            每日建议饮水量（毫升）
        """
        # 基础水量
        base_water = self.weight_kg * self.BASE_WATER_PER_KG
        
        # 活动水平调整
        base_water *= self.ACTIVITY_MULTIPLIERS[self.activity_level]
        
        # 气候调整
        base_water *= self.CLIMATE_MULTIPLIERS[self.climate]
        
        # 年龄调整（老年人代谢降低）
        if self.age is not None:
            if self.age > 65:
                base_water *= 0.9
            elif self.age < 18:
                base_water *= 0.85
        
        # 怀孕和哺乳调整
        if self.is_pregnant:
            base_water += 300  # 额外300ml
        if self.is_breastfeeding:
            base_water += 700  # 额外700ml
        
        # 取整到100ml
        return round(base_water / 100) * 100
    
    def get_drink_schedule(
        self,
        start_time: time = time(7, 0),
        end_time: time = time(22, 0),
        interval_minutes: int = 60,
        drink_size_ml: int = 250,
    ) -> List[Tuple[time, int]]:
        """
        生成饮水时间表
        
        Args:
            start_time: 开始时间
            end_time: 结束时间
            interval_minutes: 间隔分钟
            drink_size_ml: 每次饮水量（毫升）
        
        Returns:
            [(时间, 饮水量), ...]
        """
        target = self.calculate_daily_target()
        schedule = []
        
        current = datetime.combine(datetime.today(), start_time)
        end = datetime.combine(datetime.today(), end_time)
        
        total = 0
        while current <= end and total < target:
            schedule.append((current.time(), drink_size_ml))
            total += drink_size_ml
            current += timedelta(minutes=interval_minutes)
        
        # 调整最后一次饮水量
        if schedule and total > target:
            last_time, _ = schedule[-1]
            excess = total - target
            schedule[-1] = (last_time, drink_size_ml - excess)
        
        return schedule
    
    def get_recommendations(self) -> List[str]:
        """获取饮水建议"""
        target = self.calculate_daily_target()
        recommendations = [
            f"每日建议饮水量：{target/1000:.1f}升",
            "分多次少量饮用，避免一次大量饮水",
            "早起一杯温水有助于唤醒身体",
            "运动前后适量补水",
        ]
        
        if self.activity_level in [ActivityLevel.ACTIVE, ActivityLevel.VERY_ACTIVE]:
            recommendations.append("运动量大，建议补充电解质饮料")
        
        if self.climate in [Climate.HOT, Climate.VERY_HOT]:
            recommendations.append("天气炎热，注意增加饮水量")
        
        if self.is_pregnant:
            recommendations.append("孕期需保证充足水分，预防水肿")
        
        if self.is_breastfeeding:
            recommendations.append("哺乳期需多喝水促进乳汁分泌")
        
        return recommendations


class WaterTracker:
    """饮水追踪器"""
    
    def __init__(self, calculator: Optional[WaterIntakeCalculator] = None):
        """
        初始化追踪器
        
        Args:
            calculator: 饮水量计算器（可选）
        """
        self.calculator = calculator
        self.records: List[DrinkRecord] = []
    
    def add_drink(
        self,
        amount_ml: float,
        drink_type: DrinkType = DrinkType.WATER,
        timestamp: Optional[datetime] = None,
        note: str = "",
    ) -> DrinkRecord:
        """
        添加饮水记录
        
        Args:
            amount_ml: 饮水量（毫升）
            drink_type: 饮品类型
            timestamp: 时间（默认当前时间）
            note: 备注
        
        Returns:
            饮水记录
        """
        record = DrinkRecord(
            timestamp=timestamp or datetime.now(),
            amount_ml=amount_ml,
            drink_type=drink_type,
            note=note,
        )
        self.records.append(record)
        return record
    
    def get_today_records(self) -> List[DrinkRecord]:
        """获取今日饮水记录"""
        today = datetime.now().date()
        return [r for r in self.records if r.timestamp.date() == today]
    
    def get_records_by_date(self, date: datetime) -> List[DrinkRecord]:
        """获取指定日期的饮水记录"""
        return [r for r in self.records if r.timestamp.date() == date.date()]
    
    def get_total_today(self) -> float:
        """获取今日总饮水量（有效毫升）"""
        return sum(r.effective_ml for r in self.get_today_records())
    
    def get_hydration_status(self) -> HydrationStatus:
        """获取当前水分状态"""
        target = self.calculator.calculate_daily_target() if self.calculator else 2000
        today_records = self.get_today_records()
        last_drink = today_records[-1].timestamp if today_records else None
        
        return HydrationStatus(
            current_ml=sum(r.effective_ml for r in today_records),
            target_ml=target,
            last_drink_time=last_drink,
        )
    
    def get_daily_summary(self, date: Optional[datetime] = None) -> DailySummary:
        """
        获取每日汇总
        
        Args:
            date: 日期（默认今天）
        
        Returns:
            每日汇总
        """
        if date is None:
            date = datetime.now()
        
        records = self.get_records_by_date(date)
        total_ml = sum(r.amount_ml for r in records)
        effective_ml = sum(r.effective_ml for r in records)
        target_ml = self.calculator.calculate_daily_target() if self.calculator else 2000
        
        return DailySummary(
            date=date.strftime("%Y-%m-%d"),
            total_ml=total_ml,
            effective_ml=effective_ml,
            target_ml=target_ml,
            records=records,
        )
    
    def get_weekly_summary(self) -> List[DailySummary]:
        """获取本周汇总"""
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        
        summaries = []
        for i in range(7):
            date = start_of_week + timedelta(days=i)
            summaries.append(self.get_daily_summary(date))
        
        return summaries
    
    def get_statistics(self, days: int = 7) -> dict:
        """
        获取统计数据
        
        Args:
            days: 统计天数
        
        Returns:
            统计数据
        """
        today = datetime.now()
        summaries = []
        
        for i in range(days):
            date = today - timedelta(days=i)
            summaries.append(self.get_daily_summary(date))
        
        valid_summaries = [s for s in summaries if s.total_ml > 0]
        
        if not valid_summaries:
            return {
                "average_ml": 0,
                "average_completion_rate": 0,
                "days_tracked": 0,
                "days_goal_met": 0,
                "goal_met_rate": 0,
                "best_day": None,
                "total_ml": 0,
            }
        
        total_ml = sum(s.effective_ml for s in valid_summaries)
        days_goal_met = sum(1 for s in valid_summaries if s.is_goal_met)
        
        return {
            "average_ml": total_ml / len(valid_summaries),
            "average_completion_rate": sum(s.completion_rate for s in valid_summaries) / len(valid_summaries),
            "days_tracked": len(valid_summaries),
            "days_goal_met": days_goal_met,
            "goal_met_rate": days_goal_met / len(valid_summaries),
            "best_day": max(valid_summaries, key=lambda s: s.effective_ml).date,
            "total_ml": total_ml,
        }
    
    def clear_today(self) -> None:
        """清空今日记录"""
        today = datetime.now().date()
        self.records = [r for r in self.records if r.timestamp.date() != today]
    
    def to_json(self) -> str:
        """导出为JSON"""
        return json.dumps({
            "records": [r.to_dict() for r in self.records],
            "calculator": {
                "weight_kg": self.calculator.weight_kg if self.calculator else None,
                "activity_level": self.calculator.activity_level.value if self.calculator else None,
                "climate": self.calculator.climate.value if self.calculator else None,
                "age": self.calculator.age if self.calculator else None,
                "is_pregnant": self.calculator.is_pregnant if self.calculator else False,
                "is_breastfeeding": self.calculator.is_breastfeeding if self.calculator else False,
            } if self.calculator else None,
        }, ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'WaterTracker':
        """从JSON导入"""
        data = json.loads(json_str)
        tracker = cls()
        
        if data.get("calculator"):
            calc_data = data["calculator"]
            tracker.calculator = WaterIntakeCalculator(
                weight_kg=calc_data["weight_kg"],
                activity_level=ActivityLevel(calc_data["activity_level"]),
                climate=Climate(calc_data["climate"]),
                age=calc_data.get("age"),
                is_pregnant=calc_data.get("is_pregnant", False),
                is_breastfeeding=calc_data.get("is_breastfeeding", False),
            )
        
        tracker.records = [DrinkRecord.from_dict(r) for r in data.get("records", [])]
        return tracker


class DrinkReminder:
    """饮水提醒器"""
    
    def __init__(
        self,
        tracker: WaterTracker,
        interval_minutes: int = 60,
        start_time: time = time(7, 0),
        end_time: time = time(22, 0),
    ):
        """
        初始化提醒器
        
        Args:
            tracker: 饮水追踪器
            interval_minutes: 提醒间隔（分钟）
            start_time: 开始时间
            end_time: 结束时间
        """
        self.tracker = tracker
        self.interval_minutes = interval_minutes
        self.start_time = start_time
        self.end_time = end_time
        self._callback: Optional[Callable[[str], None]] = None
    
    def set_callback(self, callback: Callable[[str], None]) -> None:
        """设置提醒回调函数"""
        self._callback = callback
    
    def check_reminder(self) -> Optional[str]:
        """
        检查是否需要提醒
        
        Returns:
            提醒消息，如果不需要提醒则返回None
        """
        now = datetime.now()
        current_time = now.time()
        
        # 检查是否在提醒时间范围内
        if current_time < self.start_time or current_time > self.end_time:
            return None
        
        # 获取今日记录
        today_records = self.tracker.get_today_records()
        
        # 如果没有记录，提醒喝水
        if not today_records:
            return "💧 早上好！记得喝第一杯水哦"
        
        # 检查距离上次喝水的时间
        last_drink = today_records[-1]
        time_since_last = now - last_drink.timestamp
        
        if time_since_last >= timedelta(minutes=self.interval_minutes):
            status = self.tracker.get_hydration_status()
            if status.remaining_ml > 0:
                return f"💧 该喝水啦！今日还差 {int(status.remaining_ml)}ml 达标"
        
        return None
    
    def get_next_reminder_time(self) -> Optional[datetime]:
        """获取下次提醒时间"""
        now = datetime.now()
        today_records = self.tracker.get_today_records()
        
        if not today_records:
            # 没有记录，返回当前时间（如果在工作时间内）
            if self.start_time <= now.time() <= self.end_time:
                return now
            return None
        
        last_drink = today_records[-1]
        next_time = last_drink.timestamp + timedelta(minutes=self.interval_minutes)
        
        # 检查是否在工作时间内
        if next_time.time() > self.end_time:
            return None
        
        return next_time
    
    def get_remaining_reminders_today(self) -> int:
        """获取今日剩余提醒次数"""
        now = datetime.now()
        status = self.tracker.get_hydration_status()
        
        if status.remaining_ml <= 0:
            return 0
        
        # 假设每次喝水250ml
        drinks_needed = math.ceil(status.remaining_ml / 250)
        
        # 计算剩余时间能容纳多少次提醒
        end_datetime = datetime.combine(now.date(), self.end_time)
        remaining_minutes = (end_datetime - now).total_seconds() / 60
        possible_reminders = int(remaining_minutes / self.interval_minutes)
        
        return min(drinks_needed, possible_reminders)


def calculate_water_needs(
    weight_kg: float,
    activity_level: str = "moderate",
    climate: str = "mild",
    age: Optional[int] = None,
    is_pregnant: bool = False,
    is_breastfeeding: bool = False,
) -> float:
    """
    计算每日建议饮水量（便捷函数）
    
    Args:
        weight_kg: 体重（公斤）
        activity_level: 活动水平（sedentary/light/moderate/active/very_active）
        climate: 气候类型（cold/mild/warm/hot/very_hot）
        age: 年龄
        is_pregnant: 是否怀孕
        is_breastfeeding: 是否哺乳
    
    Returns:
        每日建议饮水量（毫升）
    """
    calculator = WaterIntakeCalculator(
        weight_kg=weight_kg,
        activity_level=ActivityLevel(activity_level),
        climate=Climate(climate),
        age=age,
        is_pregnant=is_pregnant,
        is_breastfeeding=is_breastfeeding,
    )
    return calculator.calculate_daily_target()


def format_water_amount(ml: float) -> str:
    """
    格式化水量显示
    
    Args:
        ml: 毫升数
    
    Returns:
        格式化字符串
    """
    if ml >= 1000:
        return f"{ml/1000:.1f}L"
    return f"{int(ml)}ml"


def get_water_percentage(ml: float, target_ml: float = 2000) -> str:
    """
    获取饮水进度条
    
    Args:
        ml: 当前饮水量
        target_ml: 目标饮水量
    
    Returns:
        进度条字符串
    """
    percentage = min(100, ml / target_ml * 100)
    filled = int(percentage / 5)  # 20格
    empty = 20 - filled
    bar = "💧" * filled + "⬜" * empty
    return f"[{bar}] {percentage:.0f}%"