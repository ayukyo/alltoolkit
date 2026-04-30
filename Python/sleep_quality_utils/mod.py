"""
Sleep Quality Utils - 睡眠质量分析工具

零依赖的睡眠质量分析库，支持：
- 睡眠记录和评分
- 睡眠效率计算
- 睡眠债务计算
- 最佳睡眠时间建议
- 睡眠周期分析
- 睡眠趋势分析
- 睡眠阶段分布

Author: AllToolkit
License: MIT
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple, NamedTuple
from enum import Enum
from dataclasses import dataclass, field
import math


class SleepStage(Enum):
    """睡眠阶段枚举"""
    AWAKE = "awake"           # 清醒
    LIGHT = "light"           # 浅睡眠
    DEEP = "deep"             # 深睡眠
    REM = "rem"               # 快速眼动睡眠


class SleepQuality(Enum):
    """睡眠质量等级"""
    EXCELLENT = "excellent"   # 优秀 (90-100)
    GOOD = "good"             # 良好 (80-89)
    FAIR = "fair"             # 一般 (70-79)
    POOR = "poor"             # 较差 (60-69)
    VERY_POOR = "very_poor"   # 很差 (<60)


@dataclass
class SleepSession:
    """单次睡眠记录"""
    start_time: datetime              # 入睡时间
    end_time: datetime                # 醒来时间
    awakenings: int = 0               # 夜间醒来次数
    awakening_duration_minutes: int = 0  # 醒来总时长（分钟）
    sleep_stages: Dict[SleepStage, int] = field(default_factory=dict)  # 各阶段时长（分钟）
    rating: Optional[int] = None      # 用户主观评分 (1-10)
    notes: str = ""                   # 备注
    
    @property
    def total_time_in_bed(self) -> timedelta:
        """总在床时间"""
        return self.end_time - self.start_time
    
    @property
    def total_sleep_time(self) -> timedelta:
        """总睡眠时间 = 在床时间 - 醒来时长"""
        return self.total_time_in_bed - timedelta(minutes=self.awakening_duration_minutes)
    
    @property
    def sleep_efficiency(self) -> float:
        """睡眠效率 = 总睡眠时间 / 总在床时间"""
        if self.total_time_in_bed.total_seconds() == 0:
            return 0.0
        return (self.total_sleep_time.total_seconds() / 
                self.total_time_in_bed.total_seconds()) * 100


@dataclass
class SleepAnalysis:
    """睡眠分析结果"""
    quality_score: float              # 质量评分 (0-100)
    quality_level: SleepQuality       # 质量等级
    efficiency: float                 # 睡眠效率 (%)
    total_sleep_hours: float          # 总睡眠时长（小时）
    deep_sleep_percentage: float      # 深睡眠占比 (%)
    rem_sleep_percentage: float        # REM睡眠占比 (%)
    sleep_debt_hours: float           # 睡眠债务（小时）
    recommendations: List[str]        # 改进建议
    optimal_bedtime: Optional[datetime]  # 建议入睡时间
    optimal_wake_time: Optional[datetime]  # 建议醒来时间


class SleepQualityError(Exception):
    """睡眠质量相关错误的基类"""
    pass


class InvalidSleepSessionError(SleepQualityError):
    """无效的睡眠记录"""
    pass


# 常量定义
OPTIMAL_SLEEP_HOURS = {
    "child": (9, 11),      # 儿童
    "teenager": (8, 10),   # 青少年
    "adult": (7, 9),       # 成人
    "elderly": (7, 8)      # 老年人
}

SLEEP_CYCLE_DURATION = 90  # 睡眠周期时长（分钟）

IDEAL_SLEEP_STAGE_PERCENTAGES = {
    SleepStage.LIGHT: (45, 55),   # 浅睡眠理想占比
    SleepStage.DEEP: (13, 23),    # 深睡眠理想占比
    SleepStage.REM: (20, 25)      # REM睡眠理想占比
}


def calculate_sleep_quality_score(session: SleepSession, 
                                   age_group: str = "adult") -> float:
    """
    计算睡眠质量评分
    
    评分因素：
    - 睡眠时长 (40%)
    - 睡眠效率 (25%)
    - 深睡眠占比 (15%)
    - REM睡眠占比 (10%)
    - 夜间醒来次数 (10%)
    
    Args:
        session: 睡眠记录
        age_group: 年龄组 (child/teenager/adult/elderly)
    
    Returns:
        睡眠质量评分 (0-100)
    """
    score = 0.0
    
    # 1. 睡眠时长评分 (40分)
    sleep_hours = session.total_sleep_time.total_seconds() / 3600
    optimal_range = OPTIMAL_SLEEP_HOURS.get(age_group, (7, 9))
    
    if optimal_range[0] <= sleep_hours <= optimal_range[1]:
        duration_score = 40
    elif sleep_hours < optimal_range[0]:
        # 睡眠不足，按比例扣分
        deficit = optimal_range[0] - sleep_hours
        duration_score = max(0, 40 - deficit * 8)
    else:
        # 睡眠过多，轻微软扣分
        excess = sleep_hours - optimal_range[1]
        duration_score = max(20, 40 - excess * 5)
    
    score += duration_score
    
    # 2. 睡眠效率评分 (25分)
    efficiency = session.sleep_efficiency
    if efficiency >= 95:
        efficiency_score = 25
    elif efficiency >= 90:
        efficiency_score = 22
    elif efficiency >= 85:
        efficiency_score = 18
    elif efficiency >= 80:
        efficiency_score = 12
    else:
        efficiency_score = max(0, efficiency / 5)
    
    score += efficiency_score
    
    # 3. 深睡眠占比评分 (15分)
    deep_pct = _calculate_stage_percentage(session, SleepStage.DEEP)
    ideal_deep = IDEAL_SLEEP_STAGE_PERCENTAGES[SleepStage.DEEP]
    deep_score = _calculate_stage_score(deep_pct, ideal_deep, 15)
    score += deep_score
    
    # 4. REM睡眠占比评分 (10分)
    rem_pct = _calculate_stage_percentage(session, SleepStage.REM)
    ideal_rem = IDEAL_SLEEP_STAGE_PERCENTAGES[SleepStage.REM]
    rem_score = _calculate_stage_score(rem_pct, ideal_rem, 10)
    score += rem_score
    
    # 5. 夜间醒来评分 (10分)
    if session.awakenings == 0:
        awake_score = 10
    elif session.awakenings == 1:
        awake_score = 8
    elif session.awakenings == 2:
        awake_score = 5
    elif session.awakenings == 3:
        awake_score = 2
    else:
        awake_score = max(0, 10 - session.awakenings * 2)
    
    score += awake_score
    
    return min(100, max(0, score))


def _calculate_stage_percentage(session: SleepSession, stage: SleepStage) -> float:
    """计算特定睡眠阶段的占比"""
    if not session.sleep_stages or stage not in session.sleep_stages:
        return 0.0
    
    total_sleep = session.total_sleep_time.total_seconds() / 60
    if total_sleep == 0:
        return 0.0
    
    stage_minutes = session.sleep_stages[stage]
    return (stage_minutes / total_sleep) * 100


def _calculate_stage_score(actual: float, ideal_range: Tuple[float, float], 
                           max_score: float) -> float:
    """计算睡眠阶段评分"""
    if ideal_range[0] <= actual <= ideal_range[1]:
        return max_score
    
    # 计算与理想范围的偏差
    if actual < ideal_range[0]:
        deviation = ideal_range[0] - actual
    else:
        deviation = actual - ideal_range[1]
    
    # 每偏离1%，扣10%的分数
    penalty = deviation * 0.1 * max_score
    return max(0, max_score - penalty)


def get_quality_level(score: float) -> SleepQuality:
    """
    根据评分获取睡眠质量等级
    
    Args:
        score: 睡眠质量评分 (0-100)
    
    Returns:
        睡眠质量等级
    """
    if score >= 90:
        return SleepQuality.EXCELLENT
    elif score >= 80:
        return SleepQuality.GOOD
    elif score >= 70:
        return SleepQuality.FAIR
    elif score >= 60:
        return SleepQuality.POOR
    else:
        return SleepQuality.VERY_POOR


def calculate_sleep_debt(sessions: List[SleepSession], 
                         target_hours: float = 8.0,
                         days: int = 7) -> float:
    """
    计算睡眠债务
    
    睡眠债务 = 目标睡眠时长 - 实际睡眠时长（过去N天）
    
    Args:
        sessions: 睡眠记录列表
        target_hours: 目标睡眠时长（小时）
        days: 统计天数
    
    Returns:
        睡眠债务（小时），正值表示欠债，负值表示盈余
    """
    if not sessions:
        return target_hours * days
    
    # 按日期排序并取最近N天的记录
    sorted_sessions = sorted(sessions, key=lambda s: s.start_time, reverse=True)
    recent_sessions = sorted_sessions[:days] if len(sorted_sessions) > days else sorted_sessions
    
    actual_sleep = sum(s.total_sleep_time.total_seconds() / 3600 for s in recent_sessions)
    target_sleep = target_hours * len(recent_sessions)
    
    return target_sleep - actual_sleep


def calculate_sleep_efficiency(session: SleepSession) -> float:
    """
    计算睡眠效率
    
    睡眠效率 = (总睡眠时间 / 总在床时间) × 100%
    
    Args:
        session: 睡眠记录
    
    Returns:
        睡眠效率百分比
    """
    return session.sleep_efficiency


def suggest_optimal_sleep_time(wake_time: datetime, 
                                target_hours: float = 8.0,
                                num_cycles: int = 5) -> Tuple[datetime, datetime]:
    """
    建议最佳睡眠时间
    
    基于睡眠周期（90分钟）计算最佳入睡时间
    
    Args:
        wake_time: 目标醒来时间
        target_hours: 目标睡眠时长
        num_cycles: 睡眠周期数
    
    Returns:
        (建议入睡时间, 建议醒来时间)
    """
    # 每个周期90分钟，加上15分钟入睡时间
    total_minutes = num_cycles * SLEEP_CYCLE_DURATION + 15
    suggested_bedtime = wake_time - timedelta(minutes=total_minutes)
    
    return suggested_bedtime, wake_time


def analyze_sleep_patterns(sessions: List[SleepSession]) -> Dict:
    """
    分析睡眠模式
    
    Args:
        sessions: 睡眠记录列表
    
    Returns:
        睡眠模式分析结果
    """
    if not sessions:
        return {
            "average_sleep_hours": 0,
            "average_efficiency": 0,
            "average_quality_score": 0,
            "average_bedtime": None,
            "average_wake_time": None,
            "consistency_score": 0,
            "best_day": None,
            "worst_day": None
        }
    
    # 基本统计
    sleep_hours = [s.total_sleep_time.total_seconds() / 3600 for s in sessions]
    efficiencies = [s.sleep_efficiency for s in sessions]
    quality_scores = [calculate_sleep_quality_score(s) for s in sessions]
    
    # 平均入睡和醒来时间
    bedtimes = [s.start_time.time() for s in sessions]
    wake_times = [s.end_time.time() for s in sessions]
    
    # 计算平均时间（转换为分钟处理）
    def average_time(times):
        total_minutes = sum(t.hour * 60 + t.minute for t in times)
        avg_minutes = total_minutes / len(times)
        hours = int(avg_minutes // 60) % 24
        minutes = int(avg_minutes % 60)
        return f"{hours:02d}:{minutes:02d}"
    
    # 一致性评分（基于睡眠时长和入睡时间的标准差）
    if len(sleep_hours) > 1:
        variance = sum((h - sum(sleep_hours)/len(sleep_hours))**2 for h in sleep_hours) / len(sleep_hours)
        std_dev = math.sqrt(variance)
        consistency = max(0, 100 - std_dev * 20)
    else:
        consistency = 100
    
    # 找出最佳和最差的一天
    best_idx = quality_scores.index(max(quality_scores))
    worst_idx = quality_scores.index(min(quality_scores))
    
    return {
        "average_sleep_hours": round(sum(sleep_hours) / len(sleep_hours), 2),
        "average_efficiency": round(sum(efficiencies) / len(efficiencies), 2),
        "average_quality_score": round(sum(quality_scores) / len(quality_scores), 2),
        "average_bedtime": average_time(bedtimes),
        "average_wake_time": average_time(wake_times),
        "consistency_score": round(consistency, 2),
        "best_day": {
            "date": sessions[best_idx].start_time.strftime("%Y-%m-%d"),
            "score": round(quality_scores[best_idx], 2)
        },
        "worst_day": {
            "date": sessions[worst_idx].start_time.strftime("%Y-%m-%d"),
            "score": round(quality_scores[worst_idx], 2)
        }
    }


def analyze_sleep_cycles(sleep_duration_hours: float) -> Dict:
    """
    分析睡眠周期
    
    Args:
        sleep_duration_hours: 睡眠时长（小时）
    
    Returns:
        睡眠周期分析结果
    """
    total_minutes = sleep_duration_hours * 60
    complete_cycles = int(total_minutes / SLEEP_CYCLE_DURATION)
    remaining_minutes = total_minutes % SLEEP_CYCLE_DURATION
    
    # 估算各阶段时长
    # 假设每个周期的阶段分布
    deep_per_cycle = 20  # 每个周期深睡眠约20分钟
    rem_per_cycle = 25   # 每个周期REM约25分钟
    light_per_cycle = 45  # 每个周期浅睡眠约45分钟
    
    estimated_deep = complete_cycles * deep_per_cycle + min(remaining_minutes * 0.15, remaining_minutes)
    estimated_rem = complete_cycles * rem_per_cycle + max(0, (remaining_minutes - 20) * 0.3)
    estimated_light = total_minutes - estimated_deep - estimated_rem
    
    return {
        "complete_cycles": complete_cycles,
        "remaining_minutes": round(remaining_minutes, 1),
        "estimated_deep_minutes": round(estimated_deep, 1),
        "estimated_rem_minutes": round(estimated_rem, 1),
        "estimated_light_minutes": round(estimated_light, 1),
        "cycle_quality": "optimal" if 4 <= complete_cycles <= 6 else "suboptimal"
    }


def generate_sleep_recommendations(analysis: SleepAnalysis, 
                                    age_group: str = "adult") -> List[str]:
    """
    生成睡眠改进建议
    
    Args:
        analysis: 睡眠分析结果
        age_group: 年龄组
    
    Returns:
        改进建议列表
    """
    recommendations = []
    
    # 睡眠时长建议
    optimal = OPTIMAL_SLEEP_HOURS.get(age_group, (7, 9))
    if analysis.total_sleep_hours < optimal[0]:
        deficit = optimal[0] - analysis.total_sleep_hours
        recommendations.append(
            f"您的睡眠时长不足。建议每晚睡 {optimal[0]}-{optimal[1]} 小时，"
            f"目前欠约 {deficit:.1f} 小时。"
        )
    elif analysis.total_sleep_hours > optimal[1]:
        recommendations.append(
            f"睡眠时间偏长，可能影响日间精力。建议控制在 {optimal[1]} 小时以内。"
        )
    
    # 睡眠效率建议
    if analysis.efficiency < 85:
        recommendations.append(
            f"睡眠效率较低 ({analysis.efficiency:.1f}%)。"
            "建议：1) 保持规律作息；2) 睡前避免蓝光；3) 创造安静黑暗的睡眠环境。"
        )
    
    # 深睡眠建议
    if analysis.deep_sleep_percentage < 13:
        recommendations.append(
            "深睡眠不足。建议：增加日间运动、避免睡前饮酒、保持卧室温度凉爽。"
        )
    
    # REM睡眠建议
    if analysis.rem_sleep_percentage < 20:
        recommendations.append(
            "REM睡眠不足可能影响记忆和情绪。建议：减少咖啡因摄入、保持规律作息。"
        )
    
    # 睡眠债务建议
    if analysis.sleep_debt_hours > 5:
        recommendations.append(
            f"存在 {analysis.sleep_debt_hours:.1f} 小时的睡眠债务。"
            "建议本周每天早睡30分钟逐步偿还。"
        )
    
    # 质量等级建议
    if analysis.quality_level in [SleepQuality.POOR, SleepQuality.VERY_POOR]:
        recommendations.append(
            "睡眠质量较差。如持续两周以上，建议咨询睡眠专科医生。"
        )
    
    if not recommendations:
        recommendations.append("睡眠质量良好，请继续保持当前作息习惯！")
    
    return recommendations


def analyze_sleep_session(session: SleepSession, 
                          age_group: str = "adult",
                          target_hours: float = 8.0) -> SleepAnalysis:
    """
    综合分析单次睡眠
    
    Args:
        session: 睡眠记录
        age_group: 年龄组
        target_hours: 目标睡眠时长
    
    Returns:
        睡眠分析结果
    """
    quality_score = calculate_sleep_quality_score(session, age_group)
    quality_level = get_quality_level(quality_score)
    
    deep_pct = _calculate_stage_percentage(session, SleepStage.DEEP)
    rem_pct = _calculate_stage_percentage(session, SleepStage.REM)
    
    # 计算睡眠债务（假设这是最近一次睡眠）
    sleep_debt = target_hours - (session.total_sleep_time.total_seconds() / 3600)
    
    # 建议最佳睡眠时间
    optimal_bedtime, optimal_wake = suggest_optimal_sleep_time(
        session.end_time, target_hours
    )
    
    # 创建临时分析对象用于生成建议
    temp_analysis = SleepAnalysis(
        quality_score=quality_score,
        quality_level=quality_level,
        efficiency=session.sleep_efficiency,
        total_sleep_hours=session.total_sleep_time.total_seconds() / 3600,
        deep_sleep_percentage=deep_pct,
        rem_sleep_percentage=rem_pct,
        sleep_debt_hours=sleep_debt,
        recommendations=[],
        optimal_bedtime=optimal_bedtime,
        optimal_wake_time=optimal_wake
    )
    
    temp_analysis.recommendations = generate_sleep_recommendations(temp_analysis, age_group)
    
    return temp_analysis


def calculate_optimal_wake_times(bedtime: datetime, 
                                  min_cycles: int = 4,
                                  max_cycles: int = 6) -> List[Tuple[datetime, int]]:
    """
    根据入睡时间计算最佳醒来时间
    
    Args:
        bedtime: 入睡时间
        min_cycles: 最小周期数
        max_cycles: 最大周期数
    
    Returns:
        列表 of (醒来时间, 周期数)
    """
    wake_times = []
    
    for cycles in range(min_cycles, max_cycles + 1):
        # 加15分钟入睡时间
        wake_time = bedtime + timedelta(minutes=cycles * SLEEP_CYCLE_DURATION + 15)
        wake_times.append((wake_time, cycles))
    
    return wake_times


def format_sleep_duration(duration: timedelta) -> str:
    """
    格式化睡眠时长为可读字符串
    
    Args:
        duration: 时间间隔
    
    Returns:
        格式化字符串，如 "7小时30分钟"
    """
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if hours > 0 and minutes > 0:
        return f"{hours}小时{minutes}分钟"
    elif hours > 0:
        return f"{hours}小时"
    else:
        return f"{minutes}分钟"


def get_sleep_stage_distribution(session: SleepSession) -> Dict[str, float]:
    """
    获取睡眠阶段分布
    
    Args:
        session: 睡眠记录
    
    Returns:
        各阶段占比字典
    """
    if not session.sleep_stages:
        return {
            "deep": 0,
            "light": 0,
            "rem": 0,
            "awake": session.awakening_duration_minutes / 
                     (session.total_sleep_time.total_seconds() / 60 + 1) * 100
        }
    
    total_sleep = session.total_sleep_time.total_seconds() / 60
    
    return {
        "deep": round(_calculate_stage_percentage(session, SleepStage.DEEP), 1),
        "light": round(_calculate_stage_percentage(session, SleepStage.LIGHT), 1),
        "rem": round(_calculate_stage_percentage(session, SleepStage.REM), 1),
        "awake": round(
            (session.awakening_duration_minutes / total_sleep * 100) if total_sleep > 0 else 0, 1
        )
    }


class SleepTracker:
    """睡眠追踪器 - 管理多日睡眠记录"""
    
    def __init__(self, target_hours: float = 8.0, age_group: str = "adult"):
        self.sessions: List[SleepSession] = []
        self.target_hours = target_hours
        self.age_group = age_group
    
    def add_session(self, session: SleepSession) -> None:
        """添加睡眠记录"""
        if session.end_time <= session.start_time:
            raise InvalidSleepSessionError("结束时间必须晚于开始时间")
        self.sessions.append(session)
    
    def get_recent_sessions(self, days: int = 7) -> List[SleepSession]:
        """获取最近N天的睡眠记录"""
        cutoff = datetime.now() - timedelta(days=days)
        return [s for s in self.sessions if s.start_time >= cutoff]
    
    def get_sleep_debt(self, days: int = 7) -> float:
        """获取睡眠债务"""
        return calculate_sleep_debt(self.get_recent_sessions(days), 
                                    self.target_hours, days)
    
    def get_average_quality(self, days: int = 7) -> float:
        """获取平均睡眠质量"""
        recent = self.get_recent_sessions(days)
        if not recent:
            return 0.0
        scores = [calculate_sleep_quality_score(s, self.age_group) for s in recent]
        return sum(scores) / len(scores)
    
    def get_weekly_report(self) -> Dict:
        """生成周报告"""
        return analyze_sleep_patterns(self.get_recent_sessions(7))
    
    def get_trend(self, days: int = 14) -> str:
        """获取睡眠趋势"""
        if len(self.sessions) < 3:
            return "数据不足，无法分析趋势"
        
        recent = self.get_recent_sessions(days)
        if len(recent) < 3:
            return "数据不足，无法分析趋势"
        
        # 简单线性趋势分析
        mid = len(recent) // 2
        first_half = recent[:mid]
        second_half = recent[mid:]
        
        first_avg = sum(s.total_sleep_time.total_seconds() / 3600 for s in first_half) / len(first_half)
        second_avg = sum(s.total_sleep_time.total_seconds() / 3600 for s in second_half) / len(second_half)
        
        diff = second_avg - first_avg
        
        if diff > 0.5:
            return f"睡眠时长呈上升趋势，增加约 {diff:.1f} 小时"
        elif diff < -0.5:
            return f"睡眠时长呈下降趋势，减少约 {abs(diff):.1f} 小时"
        else:
            return "睡眠时长稳定"


def estimate_sleep_stages(total_sleep_minutes: int, age: int = 30) -> Dict[SleepStage, int]:
    """
    根据总睡眠时长估算各阶段时长
    
    基于年龄和睡眠生理学研究数据估算
    
    Args:
        total_sleep_minutes: 总睡眠时长（分钟）
        age: 年龄
    
    Returns:
        各阶段时长字典（分钟）
    """
    # 年龄相关调整
    # 深睡眠随年龄减少，REM相对稳定
    if age < 20:
        deep_pct, rem_pct = 0.20, 0.25
    elif age < 40:
        deep_pct, rem_pct = 0.15, 0.23
    elif age < 60:
        deep_pct, rem_pct = 0.12, 0.22
    else:
        deep_pct, rem_pct = 0.10, 0.20
    
    light_pct = 1 - deep_pct - rem_pct
    
    deep = int(total_sleep_minutes * deep_pct)
    rem = int(total_sleep_minutes * rem_pct)
    light = total_sleep_minutes - deep - rem
    
    return {
        SleepStage.DEEP: deep,
        SleepStage.LIGHT: light,
        SleepStage.REM: rem
    }


def calculate_sleep_onset_latency(hours_in_bed_before_sleep: float) -> str:
    """
    评估入睡潜伏期
    
    Args:
        hours_in_bed_before_sleep: 上床到入睡的时间（小时）
    
    Returns:
        入睡潜伏期评估结果
    """
    minutes = hours_in_bed_before_sleep * 60
    
    if minutes <= 15:
        return "正常 (< 15分钟)"
    elif minutes <= 30:
        return "略长 (15-30分钟)，考虑睡前放松活动"
    elif minutes <= 60:
        return "较长 (30-60分钟)，建议建立固定睡前仪式"
    else:
        return "过长 (> 60分钟)，建议咨询医生"


def get_nap_recommendation(nap_duration_minutes: int) -> str:
    """
    获取小睡建议
    
    Args:
        nap_duration_minutes: 小睡时长（分钟）
    
    Returns:
        小睡评估和建议
    """
    if nap_duration_minutes <= 0:
        return "无需小睡"
    elif nap_duration_minutes <= 20:
        return "理想的小睡时长，可以提升警觉性而不影响夜间睡眠"
    elif nap_duration_minutes <= 30:
        return "稍长，可能在醒来时有短暂困倦感"
    elif nap_duration_minutes <= 60:
        return "过长，可能进入深睡眠，醒来后感到昏沉"
    else:
        return "过长，可能严重影响夜间睡眠质量"


def calculate_ideal_nap_time(last_night_sleep_hours: float, 
                              sleep_debt_hours: float = 0) -> Tuple[int, str]:
    """
    计算理想小睡时长
    
    Args:
        last_night_sleep_hours: 昨晚睡眠时长
        sleep_debt_hours: 睡眠债务
    
    Returns:
        (建议小睡时长（分钟）, 说明)
    """
    if last_night_sleep_hours >= 8 and sleep_debt_hours <= 0:
        return 0, "睡眠充足，无需小睡"
    
    if sleep_debt_hours > 2:
        return 30, f"存在 {sleep_debt_hours:.1f} 小时睡眠债务，建议30分钟恢复性小睡"
    elif sleep_debt_hours > 0:
        return 20, f"轻微睡眠不足，建议20分钟能量小睡"
    else:
        return 15, "建议15分钟短小睡提升精力"


# 导出公共API
__all__ = [
    # 枚举和类
    'SleepStage',
    'SleepQuality', 
    'SleepSession',
    'SleepAnalysis',
    'SleepQualityError',
    'InvalidSleepSessionError',
    'SleepTracker',
    # 核心函数
    'calculate_sleep_quality_score',
    'get_quality_level',
    'calculate_sleep_debt',
    'calculate_sleep_efficiency',
    'suggest_optimal_sleep_time',
    'analyze_sleep_patterns',
    'analyze_sleep_cycles',
    'generate_sleep_recommendations',
    'analyze_sleep_session',
    'calculate_optimal_wake_times',
    'format_sleep_duration',
    'get_sleep_stage_distribution',
    'estimate_sleep_stages',
    'calculate_sleep_onset_latency',
    'get_nap_recommendation',
    'calculate_ideal_nap_time',
    # 常量
    'OPTIMAL_SLEEP_HOURS',
    'SLEEP_CYCLE_DURATION',
    'IDEAL_SLEEP_STAGE_PERCENTAGES',
]