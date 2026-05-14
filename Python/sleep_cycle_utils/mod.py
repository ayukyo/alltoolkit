"""
Sleep Cycle Utilities - 睡眠周期计算工具库

功能:
- 基于睡眠周期（约90分钟）计算最佳入睡/起床时间
- 睡眠质量评估和建议
- 睡眠债务计算
- 昼夜节律分析
- 小睡时间建议
- JSON 序列化/反序列化
- 零外部依赖
"""

import json
import re
from datetime import datetime, timedelta, time
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum
from dataclasses import dataclass, field


def _parse_iso_datetime(iso_str: str) -> datetime:
    """
    解析 ISO 格式的日期时间字符串（兼容 Python 3.6+）
    
    Args:
        iso_str: ISO 格式字符串 (YYYY-MM-DDTHH:MM:SS 或 YYYY-MM-DDTHH:MM:SS.ffffff)
        
    Returns:
        datetime 对象
    """
    # 处理带微秒的格式
    if '.' in iso_str:
        # 移除可能的时区信息（简化处理）
        iso_str = re.sub(r'[+-]\d{2}:\d{2}$', '', iso_str)
        iso_str = re.sub(r'Z$', '', iso_str)
        main_part, micro_part = iso_str.split('.')
        # 只保留6位微秒
        micro_part = micro_part[:6]
        dt = datetime.strptime(f"{main_part}.{micro_part}", "%Y-%m-%dT%H:%M:%S.%f")
    else:
        # 移除可能的时区信息
        iso_str = re.sub(r'[+-]\d{2}:\d{2}$', '', iso_str)
        iso_str = re.sub(r'Z$', '', iso_str)
        dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S")
    return dt


def _parse_iso_time(iso_str: str) -> time:
    """
    解析 ISO 格式的时间字符串（兼容 Python 3.6+）
    
    Args:
        iso_str: ISO 格式字符串 (HH:MM:SS 或 HH:MM:SS.ffffff)
        
    Returns:
        time 对象
    """
    # 处理带微秒的格式
    if '.' in iso_str:
        main_part, micro_part = iso_str.split('.')
        micro_part = micro_part[:6]
        t = datetime.strptime(f"{main_part}.{micro_part}", "%H:%M:%S.%f").time()
    else:
        t = datetime.strptime(iso_str, "%H:%M:%S").time()
    return t


class SleepStage(Enum):
    """睡眠阶段"""
    AWAKE = "awake"
    LIGHT = "light"
    DEEP = "deep"
    REM = "rem"


class SleepQuality(Enum):
    """睡眠质量等级"""
    EXCELLENT = "excellent"      # 优秀：5个完整周期
    GOOD = "good"                # 良好：4个完整周期
    FAIR = "fair"                # 一般：3个完整周期
    POOR = "poor"                # 较差：少于3个周期
    INSUFFICIENT = "insufficient"  # 不足：少于2个周期


class NapType(Enum):
    """小睡类型"""
    POWER = "power"              # 能量小睡（10-20分钟）
    SHORT = "short"              # 短小睡（20-30分钟）
    IDEAL = "ideal"              # 理想小睡（90分钟）
    LONG = "long"                # 长小睡（不超过3小时）


# 常量
DEFAULT_CYCLE_DURATION = 90  # 默认睡眠周期时长（分钟）
FALL_ASLEEP_TIME = 15  # 平均入睡时间（分钟）
MIN_SLEEP_HOURS = 6  # 最少推荐睡眠时长
OPTIMAL_SLEEP_HOURS = 8  # 最佳睡眠时长
MAX_SLEEP_HOURS = 10  # 最大推荐睡眠时长
POWER_NAP_MINUTES = 20  # 能量小睡时长
IDEAL_NAP_MINUTES = 90  # 理想小睡时长


@dataclass
class SleepCycleResult:
    """睡眠周期计算结果"""
    target_time: datetime           # 目标时间（入睡或起床）
    cycle_count: int                # 周期数
    duration_minutes: int           # 总时长（分钟）
    actual_sleep_minutes: int       # 实际睡眠时长（不含入睡时间）
    fall_asleep_minutes: int        # 入睡时间
    quality: SleepQuality           # 睡眠质量评估
    recommendation: str             # 建议
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "target_time": self.target_time.isoformat(),
            "cycle_count": self.cycle_count,
            "duration_minutes": self.duration_minutes,
            "actual_sleep_minutes": self.actual_sleep_minutes,
            "fall_asleep_minutes": self.fall_asleep_minutes,
            "quality": self.quality.value,
            "recommendation": self.recommendation
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SleepCycleResult":
        """从字典创建"""
        return cls(
            target_time=_parse_iso_datetime(data["target_time"]),
            cycle_count=data["cycle_count"],
            duration_minutes=data["duration_minutes"],
            actual_sleep_minutes=data["actual_sleep_minutes"],
            fall_asleep_minutes=data["fall_asleep_minutes"],
            quality=SleepQuality(data["quality"]),
            recommendation=data["recommendation"]
        )


@dataclass
class SleepDebt:
    """睡眠债务"""
    target_hours: float             # 目标睡眠时长
    actual_hours: float             # 实际睡眠时长
    debt_hours: float               # 睡眠债务（小时）
    debt_minutes: int               # 睡眠债务（分钟）
    accumulated_days: int           # 累计天数
    recovery_hours_needed: float    # 恢复所需额外睡眠
    recovery_plan: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "target_hours": self.target_hours,
            "actual_hours": self.actual_hours,
            "debt_hours": self.debt_hours,
            "debt_minutes": self.debt_minutes,
            "accumulated_days": self.accumulated_days,
            "recovery_hours_needed": self.recovery_hours_needed,
            "recovery_plan": self.recovery_plan
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SleepDebt":
        """从字典创建"""
        return cls(
            target_hours=data["target_hours"],
            actual_hours=data["actual_hours"],
            debt_hours=data["debt_hours"],
            debt_minutes=data["debt_minutes"],
            accumulated_days=data["accumulated_days"],
            recovery_hours_needed=data["recovery_hours_needed"],
            recovery_plan=data.get("recovery_plan", [])
        )


@dataclass
class NapRecommendation:
    """小睡建议"""
    nap_type: NapType
    duration_minutes: int
    best_time_start: time          # 最佳开始时间
    best_time_end: time            # 最佳结束时间
    benefits: List[str]
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "nap_type": self.nap_type.value,
            "duration_minutes": self.duration_minutes,
            "best_time_start": self.best_time_start.isoformat(),
            "best_time_end": self.best_time_end.isoformat(),
            "benefits": self.benefits,
            "warnings": self.warnings
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NapRecommendation":
        """从字典创建"""
        return cls(
            nap_type=NapType(data["nap_type"]),
            duration_minutes=data["duration_minutes"],
            best_time_start=_parse_iso_time(data["best_time_start"]),
            best_time_end=_parse_iso_time(data["best_time_end"]),
            benefits=data["benefits"],
            warnings=data["warnings"]
        )


@dataclass
class SleepWindow:
    """睡眠窗口"""
    start_time: datetime
    end_time: datetime
    cycle_count: int
    quality: SleepQuality
    score: float  # 0-100
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "cycle_count": self.cycle_count,
            "quality": self.quality.value,
            "score": self.score
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SleepWindow":
        """从字典创建"""
        return cls(
            start_time=_parse_iso_datetime(data["start_time"]),
            end_time=_parse_iso_datetime(data["end_time"]),
            cycle_count=data["cycle_count"],
            quality=SleepQuality(data["quality"]),
            score=data["score"]
        )


class SleepCycleCalculator:
    """
    睡眠周期计算器
    
    基于睡眠科学，一个完整的睡眠周期约90分钟，包含浅睡、深睡和REM睡眠。
    在周期结束时醒来会感觉更清醒。
    
    示例:
        >>> calc = SleepCycleCalculator()
        >>> # 计算起床时间（如果现在入睡）
        >>> times = calc.calculate_wake_times(datetime.now())
        >>> for t in times:
        ...     print(f"{t.target_time.strftime('%H:%M')} - {t.quality.value}")
    """
    
    def __init__(
        self,
        cycle_duration: int = DEFAULT_CYCLE_DURATION,
        fall_asleep_time: int = FALL_ASLEEP_TIME,
        target_sleep_hours: float = OPTIMAL_SLEEP_HOURS
    ):
        """
        初始化睡眠周期计算器
        
        Args:
            cycle_duration: 睡眠周期时长（分钟）
            fall_asleep_time: 平均入睡时间（分钟）
            target_sleep_hours: 目标睡眠时长（小时）
        """
        self.cycle_duration = cycle_duration
        self.fall_asleep_time = fall_asleep_time
        self.target_sleep_hours = target_sleep_hours
    
    def calculate_wake_times(
        self,
        bed_time: datetime,
        min_cycles: int = 3,
        max_cycles: int = 6,
        count: int = 4
    ) -> List[SleepCycleResult]:
        """
        计算推荐的起床时间
        
        Args:
            bed_time: 入睡时间
            min_cycles: 最少周期数
            max_cycles: 最多周期数
            count: 返回结果数量
            
        Returns:
            推荐起床时间列表
        """
        results = []
        
        for cycle_count in range(min_cycles, max_cycles + 1):
            # 实际睡眠时长 = 周期数 * 周期时长
            actual_sleep = cycle_count * self.cycle_duration
            
            # 总时长 = 入睡时间 + 实际睡眠
            total_duration = self.fall_asleep_time + actual_sleep
            
            # 计算起床时间
            wake_time = bed_time + timedelta(minutes=total_duration)
            
            # 评估睡眠质量
            quality = self._evaluate_quality(cycle_count)
            
            # 生成建议
            recommendation = self._generate_wake_recommendation(cycle_count, quality)
            
            results.append(SleepCycleResult(
                target_time=wake_time,
                cycle_count=cycle_count,
                duration_minutes=total_duration,
                actual_sleep_minutes=actual_sleep,
                fall_asleep_minutes=self.fall_asleep_time,
                quality=quality,
                recommendation=recommendation
            ))
        
        return results[:count]
    
    def calculate_bed_times(
        self,
        wake_time: datetime,
        min_cycles: int = 3,
        max_cycles: int = 6,
        count: int = 4
    ) -> List[SleepCycleResult]:
        """
        计算推荐的入睡时间
        
        Args:
            wake_time: 目标起床时间
            min_cycles: 最少周期数
            max_cycles: 最多周期数
            count: 返回结果数量
            
        Returns:
            推荐入睡时间列表
        """
        results = []
        
        for cycle_count in range(min_cycles, max_cycles + 1):
            # 实际睡眠时长
            actual_sleep = cycle_count * self.cycle_duration
            
            # 总时长
            total_duration = self.fall_asleep_time + actual_sleep
            
            # 计算入睡时间
            bed_time = wake_time - timedelta(minutes=total_duration)
            
            # 评估睡眠质量
            quality = self._evaluate_quality(cycle_count)
            
            # 生成建议
            recommendation = self._generate_bed_recommendation(cycle_count, quality)
            
            results.append(SleepCycleResult(
                target_time=bed_time,
                cycle_count=cycle_count,
                duration_minutes=total_duration,
                actual_sleep_minutes=actual_sleep,
                fall_asleep_minutes=self.fall_asleep_time,
                quality=quality,
                recommendation=recommendation
            ))
        
        # 按时间排序（最近的在前）
        results.sort(key=lambda x: x.target_time, reverse=True)
        
        return results[:count]
    
    def calculate_optimal_sleep_window(
        self,
        wake_time: datetime,
        preferred_duration_hours: Optional[float] = None
    ) -> SleepWindow:
        """
        计算最佳睡眠窗口
        
        Args:
            wake_time: 目标起床时间
            preferred_duration_hours: 偏好睡眠时长（小时）
            
        Returns:
            最佳睡眠窗口
        """
        duration = preferred_duration_hours or self.target_sleep_hours
        
        # 计算最接近的周期数
        target_minutes = duration * 60 - self.fall_asleep_time
        cycle_count = round(target_minutes / self.cycle_duration)
        cycle_count = max(3, min(6, cycle_count))  # 限制在3-6个周期
        
        # 计算实际睡眠时长
        actual_sleep = cycle_count * self.cycle_duration
        total_duration = self.fall_asleep_time + actual_sleep
        
        start_time = wake_time - timedelta(minutes=total_duration)
        
        quality = self._evaluate_quality(cycle_count)
        score = self._calculate_sleep_score(cycle_count, duration)
        
        return SleepWindow(
            start_time=start_time,
            end_time=wake_time,
            cycle_count=cycle_count,
            quality=quality,
            score=score
        )
    
    def calculate_sleep_debt(
        self,
        sleep_records: List[Dict[str, Any]],
        target_hours: Optional[float] = None,
        recovery_days: int = 3
    ) -> SleepDebt:
        """
        计算睡眠债务
        
        Args:
            sleep_records: 睡眠记录列表 [{"date": "2024-01-01", "hours": 6.5}, ...]
            target_hours: 目标睡眠时长
            recovery_days: 恢复天数
            
        Returns:
            睡眠债务信息
        """
        target = target_hours or self.target_sleep_hours
        
        total_debt = 0.0
        actual_total = 0.0
        days = len(sleep_records)
        
        for record in sleep_records:
            hours = record.get("hours", target)
            debt = target - hours
            total_debt += max(0, debt)
            actual_total += hours
        
        avg_actual = actual_total / days if days > 0 else target
        debt_hours = total_debt
        debt_minutes = int(debt_hours * 60)
        
        # 计算恢复计划
        recovery_hours_needed = debt_hours / recovery_days if recovery_days > 0 else 0
        recovery_plan = []
        
        for i in range(recovery_days):
            extra_sleep = recovery_hours_needed
            daily_target = target + extra_sleep
            recovery_plan.append({
                "day": i + 1,
                "extra_hours": round(extra_sleep, 1),
                "total_hours": round(daily_target, 1)
            })
        
        return SleepDebt(
            target_hours=target,
            actual_hours=avg_actual,
            debt_hours=round(debt_hours, 1),
            debt_minutes=debt_minutes,
            accumulated_days=days,
            recovery_hours_needed=round(recovery_hours_needed, 1),
            recovery_plan=recovery_plan
        )
    
    def get_nap_recommendation(
        self,
        current_time: Optional[datetime] = None,
        nap_type: Optional[NapType] = None
    ) -> NapRecommendation:
        """
        获取小睡建议
        
        Args:
            current_time: 当前时间
            nap_type: 小睡类型（None则返回最佳建议）
            
        Returns:
            小睡建议
        """
        now = current_time or datetime.now()
        current_hour = now.hour
        
        # 确定最佳小睡类型
        if nap_type is None:
            if current_hour < 12:
                nap_type = NapType.POWER  # 上午：能量小睡
            elif current_hour < 15:
                nap_type = NapType.SHORT  # 下午早些时候：短小睡
            elif current_hour < 17:
                nap_type = NapType.POWER  # 下午晚些时候：能量小睡（避免影响晚上睡眠）
            else:
                nap_type = NapType.POWER  # 傍晚：只能短睡
        
        # 根据类型设置时长
        if nap_type == NapType.POWER:
            duration = POWER_NAP_MINUTES
            benefits = ["快速恢复精力", "提高警觉性", "不影响夜间睡眠"]
            warnings = ["避免超过20分钟，否则可能进入深睡"]
            best_start = time(13, 0)
            best_end = time(15, 0)
        elif nap_type == NapType.SHORT:
            duration = 30
            benefits = ["适度恢复精力", "提高认知能力"]
            warnings = ["可能在深睡阶段醒来，有睡眠惯性"]
            best_start = time(14, 0)
            best_end = time(16, 0)
        elif nap_type == NapType.IDEAL:
            duration = IDEAL_NAP_MINUTES
            benefits = ["完整睡眠周期", "最佳恢复效果", "避免睡眠惯性"]
            warnings = ["需要足够时间", "可能影响夜间睡眠"]
            best_start = time(12, 0)
            best_end = time(14, 0)
        else:  # LONG
            duration = 120
            benefits = ["深度恢复", "补觉"]
            warnings = ["严重影响夜间睡眠", "可能导致入睡困难"]
            best_start = time(12, 0)
            best_end = time(14, 0)
        
        return NapRecommendation(
            nap_type=nap_type,
            duration_minutes=duration,
            best_time_start=best_start,
            best_time_end=best_end,
            benefits=benefits,
            warnings=warnings
        )
    
    def analyze_circadian_rhythm(
        self,
        preferred_wake_time: time,
        preferred_bed_time: time,
        age: int = 30
    ) -> Dict[str, Any]:
        """
        分析昼夜节律
        
        Args:
            preferred_wake_time: 偏好起床时间
            preferred_bed_time: 偏好入睡时间
            age: 年龄
            
        Returns:
            昼夜节律分析结果
        """
        # 计算睡眠时长
        wake_dt = datetime.combine(datetime.today(), preferred_wake_time)
        bed_dt = datetime.combine(datetime.today(), preferred_bed_time)
        
        if bed_dt > wake_dt:
            # 入睡时间在起床时间之后（同一天内），实际入睡时间是前一天
            bed_dt -= timedelta(days=1)
        
        sleep_duration = (wake_dt - bed_dt).total_seconds() / 3600
        
        # 判断昼夜节律类型
        if preferred_wake_time.hour < 6:
            chronotype = "extreme_early_bird"
            chronotype_name = "极度早起型"
            peak_hours = (6, 10)
            low_hours = (14, 16)
        elif preferred_wake_time.hour < 8:
            chronotype = "early_bird"
            chronotype_name = "早起型"
            peak_hours = (7, 11)
            low_hours = (14, 17)
        elif preferred_wake_time.hour < 10:
            chronotype = "intermediate"
            chronotype_name = "中间型"
            peak_hours = (9, 12)
            low_hours = (15, 18)
        elif preferred_wake_time.hour < 12:
            chronotype = "night_owl"
            chronotype_name = "晚睡型"
            peak_hours = (11, 14)
            low_hours = (16, 19)
        else:
            chronotype = "extreme_night_owl"
            chronotype_name = "极度晚睡型"
            peak_hours = (13, 17)
            low_hours = (17, 20)
        
        # 年龄调整
        if age < 25:
            age_adjustment = "年轻人通常需要更多睡眠，晚睡型比例更高"
            recommended_hours = 9
        elif age < 65:
            age_adjustment = "成年人建议7-9小时睡眠"
            recommended_hours = 8
        else:
            age_adjustment = "老年人睡眠需求可能略有减少，但深度睡眠减少"
            recommended_hours = 7.5
        
        # 评估睡眠充足性
        sleep_quality = self._evaluate_sleep_duration(sleep_duration)
        
        return {
            "chronotype": chronotype,
            "chronotype_name": chronotype_name,
            "sleep_duration_hours": round(sleep_duration, 1),
            "sleep_quality": sleep_quality.value,
            "peak_performance_hours": {
                "start": f"{peak_hours[0]:02d}:00",
                "end": f"{peak_hours[1]:02d}:00"
            },
            "energy_low_hours": {
                "start": f"{low_hours[0]:02d}:00",
                "end": f"{low_hours[1]:02d}:00"
            },
            "age_adjustment": age_adjustment,
            "recommended_hours": recommended_hours,
            "recommendations": self._get_chronotype_recommendations(chronotype)
        }
    
    def get_sleep_stages_timeline(
        self,
        bed_time: datetime,
        cycle_count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        获取睡眠阶段时间线
        
        Args:
            bed_time: 入睡时间
            cycle_count: 周期数
            
        Returns:
            睡眠阶段时间线
        """
        timeline = []
        current_time = bed_time + timedelta(minutes=self.fall_asleep_time)
        
        for cycle in range(1, cycle_count + 1):
            cycle_start = current_time
            cycle_end = current_time + timedelta(minutes=self.cycle_duration)
            
            # 每个周期的阶段分布（简化模型）
            # 前半夜深睡多，后半夜REM多
            deep_ratio = max(0.1, 0.35 - (cycle - 1) * 0.05)  # 逐渐减少
            rem_ratio = min(0.4, 0.15 + (cycle - 1) * 0.05)    # 逐渐增加
            light_ratio = 1 - deep_ratio - rem_ratio
            
            stages = [
                {
                    "stage": SleepStage.LIGHT.value,
                    "duration_minutes": int(self.cycle_duration * light_ratio),
                    "percentage": round(light_ratio * 100, 1)
                },
                {
                    "stage": SleepStage.DEEP.value,
                    "duration_minutes": int(self.cycle_duration * deep_ratio),
                    "percentage": round(deep_ratio * 100, 1)
                },
                {
                    "stage": SleepStage.REM.value,
                    "duration_minutes": int(self.cycle_duration * rem_ratio),
                    "percentage": round(rem_ratio * 100, 1)
                }
            ]
            
            timeline.append({
                "cycle": cycle,
                "start_time": cycle_start.strftime("%H:%M"),
                "end_time": cycle_end.strftime("%H:%M"),
                "stages": stages,
                "best_wake_window": {
                    "start": (cycle_end - timedelta(minutes=5)).strftime("%H:%M"),
                    "end": cycle_end.strftime("%H:%M")
                }
            })
            
            current_time = cycle_end
        
        return timeline
    
    def _evaluate_quality(self, cycle_count: int) -> SleepQuality:
        """评估睡眠质量"""
        if cycle_count >= 5:
            return SleepQuality.EXCELLENT
        elif cycle_count >= 4:
            return SleepQuality.GOOD
        elif cycle_count >= 3:
            return SleepQuality.FAIR
        elif cycle_count >= 2:
            return SleepQuality.POOR
        else:
            return SleepQuality.INSUFFICIENT
    
    def _evaluate_sleep_duration(self, hours: float) -> SleepQuality:
        """评估睡眠时长"""
        if hours >= 8:
            return SleepQuality.EXCELLENT
        elif hours >= 7:
            return SleepQuality.GOOD
        elif hours >= 6:
            return SleepQuality.FAIR
        elif hours >= 5:
            return SleepQuality.POOR
        else:
            return SleepQuality.INSUFFICIENT
    
    def _calculate_sleep_score(self, cycle_count: int, target_hours: float) -> float:
        """计算睡眠评分（0-100）"""
        # 基于周期数的分数
        cycle_score = min(100, cycle_count * 20)
        
        # 基于与目标时长匹配度的分数
        actual_hours = (cycle_count * self.cycle_duration) / 60
        match_score = max(0, 100 - abs(actual_hours - target_hours) * 10)
        
        return round((cycle_score + match_score) / 2, 1)
    
    def _generate_wake_recommendation(self, cycle_count: int, quality: SleepQuality) -> str:
        """生成起床时间建议"""
        recommendations = {
            6: "完美！6个周期约9小时，醒来时神清气爽，精力充沛。",
            5: "优秀！5个周期约7.5小时，是大多数成年人的理想睡眠时长。",
            4: "良好！4个周期约6小时，对于短睡眠者足够，但建议不要太频繁。",
            3: "一般。3个周期约4.5小时，勉强够用，但长期这样会影响健康。",
        }
        return recommendations.get(cycle_count, "睡眠周期不足，建议增加睡眠时间。")
    
    def _generate_bed_recommendation(self, cycle_count: int, quality: SleepQuality) -> str:
        """生成入睡时间建议"""
        recommendations = {
            6: "如果需要充足睡眠，这个入睡时间可以保证9小时睡眠。",
            5: "这是推荐的入睡时间，可以获得约7.5小时的理想睡眠。",
            4: "这个入睡时间可以保证约6小时睡眠，适合短睡眠者。",
            3: "这个入睡时间只能保证约4.5小时睡眠，谨慎选择。",
        }
        return recommendations.get(cycle_count, "睡眠时间过短，建议提前入睡。")
    
    def _get_chronotype_recommendations(self, chronotype: str) -> List[str]:
        """获取昼夜节律类型建议"""
        all_recommendations = {
            "extreme_early_bird": [
                "保持规律的早起习惯",
                "避免傍晚后摄入咖啡因",
                "晚上7点后避免剧烈运动",
                "晚上9点前结束晚餐"
            ],
            "early_bird": [
                "利用早晨的高效时段处理重要事务",
                "中午12点前避免小睡",
                "晚上保持放松的活动",
                "建立固定的睡前仪式"
            ],
            "intermediate": [
                "保持规律的作息时间",
                "周末不要大幅改变作息",
                "注意睡眠环境的光线控制",
                "睡前1小时避免使用电子设备"
            ],
            "night_owl": [
                "如果可能，选择灵活的工作时间",
                "早上接触阳光有助于调整生物钟",
                "避免睡前使用电子设备",
                "卧室保持凉爽黑暗"
            ],
            "extreme_night_owl": [
                "考虑逐步调整作息",
                "早上使用强光疗法",
                "晚上避免过度刺激",
                "必要时咨询睡眠专家"
            ]
        }
        return all_recommendations.get(chronotype, ["保持规律的作息时间"])
    
    def to_json(self) -> str:
        """序列化为 JSON"""
        data = {
            "cycle_duration": self.cycle_duration,
            "fall_asleep_time": self.fall_asleep_time,
            "target_sleep_hours": self.target_sleep_hours
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "SleepCycleCalculator":
        """从 JSON 反序列化"""
        data = json.loads(json_str)
        return cls(
            cycle_duration=data["cycle_duration"],
            fall_asleep_time=data["fall_asleep_time"],
            target_sleep_hours=data["target_sleep_hours"]
        )


# 便捷函数

def calculate_wake_times(
    bed_time: datetime,
    cycle_duration: int = 90,
    fall_asleep_time: int = 15,
    count: int = 4
) -> List[SleepCycleResult]:
    """
    计算推荐的起床时间
    
    Args:
        bed_time: 入睡时间
        cycle_duration: 睡眠周期时长（分钟）
        fall_asleep_time: 入睡时间（分钟）
        count: 返回结果数量
        
    Returns:
        推荐起床时间列表
    """
    calc = SleepCycleCalculator(cycle_duration, fall_asleep_time)
    return calc.calculate_wake_times(bed_time, count=count)


def calculate_bed_times(
    wake_time: datetime,
    cycle_duration: int = 90,
    fall_asleep_time: int = 15,
    count: int = 4
) -> List[SleepCycleResult]:
    """
    计算推荐的入睡时间
    
    Args:
        wake_time: 目标起床时间
        cycle_duration: 睡眠周期时长（分钟）
        fall_asleep_time: 入睡时间（分钟）
        count: 返回结果数量
        
    Returns:
        推荐入睡时间列表
    """
    calc = SleepCycleCalculator(cycle_duration, fall_asleep_time)
    return calc.calculate_bed_times(wake_time, count=count)


def get_optimal_sleep_duration(cycles: int = 5) -> int:
    """
    获取最佳睡眠时长（分钟）
    
    Args:
        cycles: 周期数
        
    Returns:
        睡眠时长（分钟）
    """
    return FALL_ASLEEP_TIME + cycles * DEFAULT_CYCLE_DURATION


def format_sleep_duration(minutes: int) -> str:
    """
    格式化睡眠时长
    
    Args:
        minutes: 分钟数
        
    Returns:
        格式化字符串
    """
    hours, mins = divmod(minutes, 60)
    if hours > 0 and mins > 0:
        return f"{hours}小时{mins}分钟"
    elif hours > 0:
        return f"{hours}小时"
    else:
        return f"{mins}分钟"


def get_quality_description(quality: SleepQuality) -> str:
    """
    获取睡眠质量描述
    
    Args:
        quality: 睡眠质量
        
    Returns:
        质量描述
    """
    descriptions = {
        SleepQuality.EXCELLENT: "优秀 - 充足的睡眠，精力充沛",
        SleepQuality.GOOD: "良好 - 足够的睡眠，状态良好",
        SleepQuality.FAIR: "一般 - 基本够用，可能有些疲惫",
        SleepQuality.POOR: "较差 - 睡眠不足，建议增加",
        SleepQuality.INSUFFICIENT: "不足 - 严重缺乏，影响健康"
    }
    return descriptions.get(quality, "未知")


def recommend_nap(
    current_hour: Optional[int] = None,
    energy_level: str = "medium"
) -> NapRecommendation:
    """
    推荐小睡时长
    
    Args:
        current_hour: 当前小时
        energy_level: 能量水平 (low, medium, high)
        
    Returns:
        小睡建议
    """
    calc = SleepCycleCalculator()
    now = datetime.now()
    if current_hour is not None:
        now = now.replace(hour=current_hour)
    
    # 根据能量水平调整建议
    if energy_level == "low":
        # 低能量时建议更长时间
        return calc.get_nap_recommendation(now, NapType.SHORT)
    elif energy_level == "high":
        # 高能量时短睡或不睡
        return calc.get_nap_recommendation(now, NapType.POWER)
    else:
        return calc.get_nap_recommendation(now)