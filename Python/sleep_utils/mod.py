"""
Sleep Utils - 睡眠周期与质量计算工具

功能：
- 睡眠周期计算（90分钟周期）
- 最佳就寝/起床时间计算
- 睡眠质量评分
- 睡眠负债计算
- 昼夜节律分析
- 小睡建议
"""

from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Dict
import math


# 常量定义
SLEEP_CYCLE_MINUTES = 90  # 一个睡眠周期约90分钟
FALL_ASLEEP_MINUTES = 15  # 平均入睡时间（分钟）
RECOMMENDED_CYCLES_MIN = 4  # 最少推荐周期数
RECOMMENDED_CYCLES_MAX = 6  # 最多推荐周期数
OPTIMAL_CYCLES = 5  # 最佳周期数


class SleepCycleResult:
    """睡眠周期计算结果"""
    
    def __init__(self, 
                 bedtime: datetime,
                 wake_time: datetime,
                 cycles: int,
                 total_sleep_minutes: int,
                 quality_score: float,
                 sleep_debt: int = 0):
        self.bedtime = bedtime
        self.wake_time = wake_time
        self.cycles = cycles
        self.total_sleep_minutes = total_sleep_minutes
        self.quality_score = quality_score
        self.sleep_debt = sleep_debt
    
    def __repr__(self):
        return (f"SleepCycleResult(bedtime={self.bedtime.strftime('%H:%M')}, "
                f"wake_time={self.wake_time.strftime('%H:%M')}, "
                f"cycles={self.cycles}, "
                f"quality={self.quality_score:.1f}/10)")


class SleepQuality:
    """睡眠质量评级"""
    
    EXCELLENT = "excellent"  # 9-10分
    GOOD = "good"           # 7-8分
    FAIR = "fair"           # 5-6分
    POOR = "poor"           # 3-4分
    VERY_POOR = "very_poor" # 1-2分
    
    @staticmethod
    def from_score(score: float) -> str:
        """根据分数返回质量等级"""
        if score >= 9:
            return SleepQuality.EXCELLENT
        elif score >= 7:
            return SleepQuality.GOOD
        elif score >= 5:
            return SleepQuality.FAIR
        elif score >= 3:
            return SleepQuality.POOR
        else:
            return SleepQuality.VERY_POOR


class CircadianRhythm:
    """昼夜节律分析"""
    
    # 不同时间段的身体状态
    PERIODS = {
        (6, 9): {"name": "早晨清醒期", "alertness": 8, "melatonin": "low"},
        (9, 12): {"name": "高效工作期", "alertness": 9, "melatonin": "low"},
        (12, 14): {"name": "午后低谷期", "alertness": 6, "melatonin": "low"},
        (14, 17): {"name": "下午活跃期", "alertness": 7, "melatonin": "low"},
        (17, 20): {"name": "傍晚过渡期", "alertness": 6, "melatonin": "rising"},
        (20, 22): {"name": "夜间放松期", "alertness": 4, "melatonin": "high"},
        (22, 2): {"name": "深度睡眠期", "alertness": 1, "melatonin": "peak"},
        (2, 6): {"name": "凌晨恢复期", "alertness": 2, "melatonin": "high"},
    }
    
    @staticmethod
    def get_period(hour: int) -> Dict:
        """获取指定小时的身体状态"""
        for (start, end), info in CircadianRhythm.PERIODS.items():
            if start <= hour < end or (start > end and (hour >= start or hour < end)):
                return info
        return {"name": "未知", "alertness": 5, "melatonin": "unknown"}


def calculate_wake_times(bedtime: datetime, 
                         cycles_range: Tuple[int, int] = (RECOMMENDED_CYCLES_MIN, RECOMMENDED_CYCLES_MAX),
                         fall_asleep_minutes: int = FALL_ASLEEP_MINUTES) -> List[SleepCycleResult]:
    """
    根据就寝时间计算推荐起床时间
    
    Args:
        bedtime: 就寝时间
        cycles_range: 周期数范围（最小，最大）
        fall_asleep_minutes: 入睡所需时间（分钟）
    
    Returns:
        按质量排序的起床时间列表
    """
    results = []
    min_cycles, max_cycles = cycles_range
    
    # 加入入睡时间
    actual_sleep_start = bedtime + timedelta(minutes=fall_asleep_minutes)
    
    for cycles in range(min_cycles, max_cycles + 1):
        total_sleep = cycles * SLEEP_CYCLE_MINUTES
        wake_time = actual_sleep_start + timedelta(minutes=total_sleep)
        
        # 计算质量分数
        quality = calculate_quality_score(cycles, wake_time)
        
        results.append(SleepCycleResult(
            bedtime=bedtime,
            wake_time=wake_time,
            cycles=cycles,
            total_sleep_minutes=total_sleep,
            quality_score=quality
        ))
    
    # 按质量分数降序排序
    results.sort(key=lambda x: x.quality_score, reverse=True)
    return results


def calculate_bedtimes(wake_time: datetime,
                       cycles_range: Tuple[int, int] = (RECOMMENDED_CYCLES_MIN, RECOMMENDED_CYCLES_MAX),
                       fall_asleep_minutes: int = FALL_ASLEEP_MINUTES) -> List[SleepCycleResult]:
    """
    根据起床时间计算推荐就寝时间
    
    Args:
        wake_time: 期望起床时间
        cycles_range: 周期数范围（最小，最大）
        fall_asleep_minutes: 入睡所需时间（分钟）
    
    Returns:
        按质量排序的就寝时间列表
    """
    results = []
    min_cycles, max_cycles = cycles_range
    
    for cycles in range(min_cycles, max_cycles + 1):
        total_sleep = cycles * SLEEP_CYCLE_MINUTES
        # 需要提前入睡时间，以便在起床时间正好完成睡眠周期
        sleep_start = wake_time - timedelta(minutes=total_sleep)
        # 再提前入睡准备时间
        bedtime = sleep_start - timedelta(minutes=fall_asleep_minutes)
        
        # 计算质量分数
        quality = calculate_quality_score(cycles, wake_time)
        
        results.append(SleepCycleResult(
            bedtime=bedtime,
            wake_time=wake_time,
            cycles=cycles,
            total_sleep_minutes=total_sleep,
            quality_score=quality
        ))
    
    # 按质量分数降序排序
    results.sort(key=lambda x: x.quality_score, reverse=True)
    return results


def calculate_quality_score(cycles: int, wake_time: datetime) -> float:
    """
    计算睡眠质量分数
    
    Args:
        cycles: 睡眠周期数
        wake_time: 起床时间
    
    Returns:
        质量分数（1-10）
    """
    score = 0.0
    
    # 周期数评分（5个周期最优）
    if cycles == OPTIMAL_CYCLES:
        score += 4.0
    elif cycles == OPTIMAL_CYCLES - 1:
        score += 3.5
    elif cycles == OPTIMAL_CYCLES + 1:
        score += 3.0
    elif cycles >= RECOMMENDED_CYCLES_MIN and cycles <= RECOMMENDED_CYCLES_MAX:
        score += 2.5
    else:
        score += 1.0
    
    # 起床时间评分（6-8点最佳）
    wake_hour = wake_time.hour + wake_time.minute / 60
    if 6 <= wake_hour <= 8:
        score += 3.0
    elif 5 <= wake_hour <= 9:
        score += 2.0
    elif 4 <= wake_hour <= 10:
        score += 1.0
    else:
        score += 0.5
    
    # 总睡眠时长评分
    total_hours = cycles * SLEEP_CYCLE_MINUTES / 60
    if 7 <= total_hours <= 9:
        score += 3.0
    elif 6 <= total_hours <= 10:
        score += 2.0
    elif 5 <= total_hours <= 11:
        score += 1.0
    else:
        score += 0.5
    
    return min(10.0, max(1.0, score))


def calculate_sleep_debt(target_hours: float = 7.5,
                         actual_hours_list: List[float] = None,
                         days: int = 7) -> Dict:
    """
    计算睡眠负债
    
    Args:
        target_hours: 目标睡眠时长（小时）
        actual_hours_list: 实际睡眠时长列表（小时）
        days: 计算天数
    
    Returns:
        包含睡眠负债信息的字典
    """
    if actual_hours_list is None:
        actual_hours_list = []
    
    # 如果提供的数据少于天数，用平均值填充
    if len(actual_hours_list) < days:
        if actual_hours_list:
            avg = sum(actual_hours_list) / len(actual_hours_list)
            actual_hours_list = actual_hours_list + [avg] * (days - len(actual_hours_list))
        else:
            actual_hours_list = [target_hours] * days
    
    # 只取最近N天
    actual_hours_list = actual_hours_list[-days:]
    
    total_target = target_hours * days
    total_actual = sum(actual_hours_list)
    debt = total_target - total_actual
    
    # 计算负债百分比
    debt_percentage = (debt / total_target) * 100 if total_target > 0 else 0
    
    # 计算需要多少天补回
    daily_catch_up = 1  # 每天多睡1小时
    days_to_recover = max(0, int(math.ceil(debt / daily_catch_up))) if debt > 0 else 0
    
    return {
        "target_hours": target_hours,
        "actual_total_hours": total_actual,
        "debt_hours": max(0, debt),
        "debt_minutes": max(0, int(debt * 60)),
        "debt_percentage": debt_percentage,
        "days_analyzed": len(actual_hours_list),
        "average_actual": total_actual / len(actual_hours_list),
        "days_to_recover": days_to_recover,
        "status": "good" if debt <= 0 else ("mild" if debt <= 7 else ("moderate" if debt <= 14 else "severe"))
    }


def suggest_nap(duration_minutes: int = None,
                time_since_last_sleep: float = None,
                current_hour: int = None) -> Dict:
    """
    小睡建议
    
    Args:
        duration_minutes: 计划小睡时长（分钟）
        time_since_last_sleep: 距离上次睡眠的时间（小时）
        current_hour: 当前小时（0-23）
    
    Returns:
        小睡建议字典
    """
    suggestions = []
    
    # 根据时长推荐
    if duration_minutes:
        if duration_minutes <= 20:
            # 短小睡：主要是浅睡眠，快速恢复精力
            suggestions.append({
                "type": "power_nap",
                "duration": duration_minutes,
                "description": "强力小睡：快速恢复警觉性，不会进入深度睡眠",
                "recommended": duration_minutes <= 20,
                "tip": "设置闹钟在20分钟内，避免进入深度睡眠后醒来感到昏沉"
            })
        elif duration_minutes <= 30:
            suggestions.append({
                "type": "short_nap",
                "duration": duration_minutes,
                "description": "短小睡：可能进入轻度睡眠，醒来可能有睡眠惯性",
                "recommended": False,
                "tip": "建议缩短到20分钟或延长到90分钟（完整周期）"
            })
        elif duration_minutes <= 60:
            suggestions.append({
                "type": "moderate_nap",
                "duration": duration_minutes,
                "description": "中等小睡：会进入深度睡眠，醒来可能有严重睡眠惯性",
                "recommended": False,
                "tip": "不建议，醒来会感到非常困倦。要么缩短到20分钟，要么延长到90分钟"
            })
        else:
            # 完整周期
            full_cycles = duration_minutes // SLEEP_CYCLE_MINUTES
            remainder = duration_minutes % SLEEP_CYCLE_MINUTES
            
            if remainder <= 20:
                suggestions.append({
                    "type": "full_cycle_nap",
                    "duration": duration_minutes,
                    "description": f"完整周期小睡：约{full_cycles}个睡眠周期，醒来后精力充沛",
                    "recommended": True,
                    "tip": "确保有足够时间完成周期，避免被中途打断"
                })
            else:
                suggestions.append({
                    "type": "partial_cycle_nap",
                    "duration": duration_minutes,
                    "description": "部分周期小睡：可能在深度睡眠中醒来",
                    "recommended": False,
                    "tip": f"建议调整为{(full_cycles + 1) * SLEEP_CYCLE_MINUTES}分钟（完整周期）或20分钟（强力小睡）"
                })
    
    # 根据时间推荐
    if current_hour is not None:
        time_advice = []
        if 13 <= current_hour <= 15:
            time_advice.append({
                "period": "午后低谷期",
                "suitability": "最佳",
                "reason": "符合自然昼夜节律的午后低谷期"
            })
        elif 6 <= current_hour <= 10:
            time_advice.append({
                "period": "早晨清醒期",
                "suitability": "一般",
                "reason": "自然警觉性较高，小睡可能影响夜间睡眠"
            })
        elif 17 <= current_hour <= 19:
            time_advice.append({
                "period": "傍晚过渡期",
                "suitability": "较差",
                "reason": "可能影响夜间睡眠质量"
            })
        elif 20 <= current_hour <= 23:
            time_advice.append({
                "period": "夜间准备期",
                "suitability": "不推荐",
                "reason": "干扰正常睡眠周期"
            })
        elif 0 <= current_hour <= 5:
            time_advice.append({
                "period": "夜间睡眠期",
                "suitability": "应该睡觉",
                "reason": "应该在正常睡眠中"
            })
        else:
            time_advice.append({
                "period": "日间活跃期",
                "suitability": "可以",
                "reason": "如果感到疲劳可以小睡"
            })
        
        suggestions.append({"time_advice": time_advice})
    
    # 根据上次睡眠时间推荐
    if time_since_last_sleep is not None:
        if time_since_last_sleep < 6:
            suggestions.append({
                "fatigue_status": "低疲劳",
                "recommendation": "暂不需要小睡，除非感到困倦"
            })
        elif time_since_last_sleep < 10:
            suggestions.append({
                "fatigue_status": "轻度疲劳",
                "recommendation": "可以考虑15-20分钟的强力小睡"
            })
        elif time_since_last_sleep < 16:
            suggestions.append({
                "fatigue_status": "中度疲劳",
                "recommendation": "建议小睡20-30分钟恢复精力"
            })
        else:
            suggestions.append({
                "fatigue_status": "严重疲劳",
                "recommendation": "强烈建议小睡或提前就寝"
            })
    
    return {
        "duration_minutes": duration_minutes,
        "suggestions": suggestions,
        "best_nap_duration": [20, 90],  # 推荐的小睡时长
        "best_nap_time": (13, 15)  # 推荐的小睡时间段
    }


def analyze_circadian_rhythm(wake_time: datetime,
                              bedtime: datetime,
                              age: int = 30) -> Dict:
    """
    昼夜节律分析
    
    Args:
        wake_time: 起床时间
        bedtime: 就寝时间
        age: 年龄
    
    Returns:
        昼夜节律分析结果
    """
    analysis = {
        "wake_period": {},
        "bedtime_period": {},
        "chronotype": "unknown",
        "recommendations": [],
        "alerts": []
    }
    
    # 获取起床时间段状态
    wake_hour = wake_time.hour
    analysis["wake_period"] = CircadianRhythm.get_period(wake_hour)
    
    # 获取就寝时间段状态
    bed_hour = bedtime.hour
    analysis["bedtime_period"] = CircadianRhythm.get_period(bed_hour)
    
    # 判断时型（昼夜节律类型）
    if wake_hour < 6:
        analysis["chronotype"] = "early_bird"  # 早鸟型
        analysis["recommendations"].append("您是早鸟型，早起对您来说很自然")
    elif wake_hour >= 9:
        analysis["chronotype"] = "night_owl"  # 夜猫子型
        analysis["recommendations"].append("您是夜猫子型，晚睡晚起更符合您的生物钟")
    else:
        analysis["chronotype"] = "intermediate"  # 中间型
        analysis["recommendations"].append("您是中间型，可以灵活适应不同的作息时间")
    
    # 年龄相关建议
    if age < 25:
        analysis["alerts"].append("年轻人昼夜节律可能偏向晚睡，这很正常")
    elif age > 65:
        analysis["alerts"].append("老年人昼夜节律可能偏向早睡早起")
    
    # 起床时间建议
    if 6 <= wake_hour <= 8:
        analysis["recommendations"].append("起床时间在理想范围内")
    elif wake_hour < 5:
        analysis["alerts"].append("起床时间过早，可能影响睡眠质量")
    elif wake_hour > 10:
        analysis["alerts"].append("起床时间过晚，可能影响昼夜节律")
    
    # 就寝时间建议
    if 22 <= bed_hour <= 23:
        analysis["recommendations"].append("就寝时间在理想范围内")
    elif bed_hour < 21:
        analysis["alerts"].append("就寝时间可能过早")
    elif bed_hour >= 1:
        analysis["alerts"].append("就寝时间过晚，建议调整作息")
    
    return analysis


def calculate_optimal_sleep_schedule(wake_time_target: datetime = None,
                                      bedtime_target: datetime = None,
                                      sleep_hours_target: float = 7.5,
                                      flexibility_minutes: int = 30) -> Dict:
    """
    计算最佳睡眠时间表
    
    Args:
        wake_time_target: 目标起床时间
        bedtime_target: 目标就寝时间
        sleep_hours_target: 目标睡眠时长（小时）
        flexibility_minutes: 灵活性（分钟）
    
    Returns:
        最佳睡眠时间表建议
    """
    results = {
        "options": [],
        "recommended": None
    }
    
    if wake_time_target:
        # 根据起床时间计算就寝时间
        bedtimes = calculate_bedtimes(wake_time_target)
        for bt in bedtimes:
            results["options"].append({
                "type": "wake_based",
                "bedtime": bt.bedtime.strftime("%H:%M"),
                "wake_time": bt.wake_time.strftime("%H:%M"),
                "cycles": bt.cycles,
                "sleep_hours": bt.total_sleep_minutes / 60,
                "quality_score": bt.quality_score,
                "quality_level": SleepQuality.from_score(bt.quality_score)
            })
        
        # 选择最佳方案
        if results["options"]:
            results["recommended"] = results["options"][0]
    
    if bedtime_target:
        # 根据就寝时间计算起床时间
        wake_times = calculate_wake_times(bedtime_target)
        for wt in wake_times:
            results["options"].append({
                "type": "bedtime_based",
                "bedtime": wt.bedtime.strftime("%H:%M"),
                "wake_time": wt.wake_time.strftime("%H:%M"),
                "cycles": wt.cycles,
                "sleep_hours": wt.total_sleep_minutes / 60,
                "quality_score": wt.quality_score,
                "quality_level": SleepQuality.from_score(wt.quality_score)
            })
        
        # 如果没有起床时间目标，选择最佳方案
        if not wake_time_target and results["options"]:
            results["recommended"] = results["options"][0]
    
    return results


def get_sleep_stage_distribution(cycles: int) -> Dict:
    """
    获取睡眠阶段分布
    
    Args:
        cycles: 睡眠周期数
    
    Returns:
        睡眠阶段分布信息
    """
    total_minutes = cycles * SLEEP_CYCLE_MINUTES
    
    # 每个周期的睡眠阶段分布（近似）
    # 第一周期：浅睡 -> 深睡 -> REM
    # 后续周期：浅睡减少，深睡减少，REM增加
    
    light_sleep = 0
    deep_sleep = 0
    rem_sleep = 0
    
    for cycle in range(1, cycles + 1):
        cycle_light = 10 + (cycle - 1) * 3  # 浅睡逐周期略增
        cycle_deep = max(20 - (cycle - 1) * 5, 5)  # 深睡逐周期减少
        cycle_rem = 10 + (cycle - 1) * 8  # REM逐周期增加
        
        cycle_total = cycle_light + cycle_deep + cycle_rem
        # 确保每周期90分钟
        cycle_light = int(SLEEP_CYCLE_MINUTES * cycle_light / cycle_total)
        cycle_deep = int(SLEEP_CYCLE_MINUTES * cycle_deep / cycle_total)
        cycle_rem = SLEEP_CYCLE_MINUTES - cycle_light - cycle_deep
        
        light_sleep += cycle_light
        deep_sleep += cycle_deep
        rem_sleep += cycle_rem
    
    return {
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 1),
        "stages": {
            "light_sleep": {
                "minutes": light_sleep,
                "percentage": round(light_sleep / total_minutes * 100, 1),
                "description": "浅睡眠：身体放松，容易被唤醒"
            },
            "deep_sleep": {
                "minutes": deep_sleep,
                "percentage": round(deep_sleep / total_minutes * 100, 1),
                "description": "深度睡眠：身体修复，免疫系统增强"
            },
            "rem_sleep": {
                "minutes": rem_sleep,
                "percentage": round(rem_sleep / total_minutes * 100, 1),
                "description": "快速眼动期：梦境发生，记忆巩固"
            }
        },
        "cycles": cycles,
        "cycle_duration_minutes": SLEEP_CYCLE_MINUTES
    }


def calculate_sleep_efficiency(time_in_bed_minutes: int,
                                actual_sleep_minutes: int) -> Dict:
    """
    计算睡眠效率
    
    Args:
        time_in_bed_minutes: 在床上的总时间（分钟）
        actual_sleep_minutes: 实际睡眠时间（分钟）
    
    Returns:
        睡眠效率分析结果
    """
    if time_in_bed_minutes <= 0:
        raise ValueError("在床时间必须大于0")
    
    efficiency = (actual_sleep_minutes / time_in_bed_minutes) * 100
    
    # 睡眠效率评级
    if efficiency >= 90:
        rating = "excellent"
        description = "睡眠效率优秀，几乎一上床就能入睡并保持睡眠"
    elif efficiency >= 85:
        rating = "good"
        description = "睡眠效率良好，入睡和保持睡眠都比较顺利"
    elif efficiency >= 75:
        rating = "fair"
        description = "睡眠效率一般，可能有入睡困难或夜间醒来"
    else:
        rating = "poor"
        description = "睡眠效率较低，建议改善睡眠习惯或咨询医生"
    
    return {
        "time_in_bed_minutes": time_in_bed_minutes,
        "time_in_bed_hours": round(time_in_bed_minutes / 60, 1),
        "actual_sleep_minutes": actual_sleep_minutes,
        "actual_sleep_hours": round(actual_sleep_minutes / 60, 1),
        "efficiency_percentage": round(efficiency, 1),
        "rating": rating,
        "description": description,
        "recommendations": _get_efficiency_recommendations(efficiency)
    }


def _get_efficiency_recommendations(efficiency: float) -> List[str]:
    """根据睡眠效率获取建议"""
    recommendations = []
    
    if efficiency < 75:
        recommendations.extend([
            "保持规律的作息时间",
            "睡前1小时避免使用电子设备",
            "保持卧室安静、黑暗、凉爽",
            "避免睡前饮用咖啡因或酒精",
            "如果20分钟内无法入睡，起床做些放松活动"
        ])
    elif efficiency < 85:
        recommendations.extend([
            "建立放松的睡前例行程序",
            "避免在床上做与睡眠无关的事",
            "限制午睡时间"
        ])
    elif efficiency < 90:
        recommendations.append("保持当前的睡眠习惯")
    else:
        recommendations.append("您的睡眠效率非常好，继续保持！")
    
    return recommendations


def format_duration(minutes: int) -> str:
    """
    格式化时长显示
    
    Args:
        minutes: 分钟数
    
    Returns:
        格式化的时长字符串
    """
    hours = minutes // 60
    mins = minutes % 60
    
    if hours > 0 and mins > 0:
        return f"{hours}小时{mins}分钟"
    elif hours > 0:
        return f"{hours}小时"
    else:
        return f"{mins}分钟"


# 便捷函数
def when_to_wake(bedtime: datetime, 
                 fall_asleep_minutes: int = FALL_ASLEEP_MINUTES) -> List[Dict]:
    """便捷函数：根据就寝时间计算起床时间"""
    results = calculate_wake_times(bedtime, fall_asleep_minutes=fall_asleep_minutes)
    return [{
        "wake_time": r.wake_time.strftime("%H:%M"),
        "cycles": r.cycles,
        "sleep_hours": round(r.total_sleep_minutes / 60, 1),
        "quality": r.quality_score
    } for r in results]


def when_to_sleep(wake_time: datetime,
                  fall_asleep_minutes: int = FALL_ASLEEP_MINUTES) -> List[Dict]:
    """便捷函数：根据起床时间计算就寝时间"""
    results = calculate_bedtimes(wake_time, fall_asleep_minutes=fall_asleep_minutes)
    return [{
        "bedtime": r.bedtime.strftime("%H:%M"),
        "cycles": r.cycles,
        "sleep_hours": round(r.total_sleep_minutes / 60, 1),
        "quality": r.quality_score
    } for r in results]


if __name__ == "__main__":
    # 演示用法
    from datetime import datetime
    
    print("=== 睡眠工具演示 ===\n")
    
    # 1. 根据就寝时间计算起床时间
    print("1. 如果 23:00 就寝，推荐起床时间：")
    bedtime = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
    wake_options = when_to_wake(bedtime)
    for opt in wake_options:
        print(f"   {opt['wake_time']} - {opt['cycles']}个周期, {opt['sleep_hours']}小时, 质量: {opt['quality']:.1f}/10")
    
    print()
    
    # 2. 根据起床时间计算就寝时间
    print("2. 如果需要 7:00 起床，推荐就寝时间：")
    wake_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    bed_options = when_to_sleep(wake_time)
    for opt in bed_options:
        print(f"   {opt['bedtime']} - {opt['cycles']}个周期, {opt['sleep_hours']}小时, 质量: {opt['quality']:.1f}/10")
    
    print()
    
    # 3. 睡眠负债计算
    print("3. 睡眠负债计算（过去7天）：")
    debt = calculate_sleep_debt(target_hours=7.5, actual_hours_list=[6, 7, 5, 8, 6, 7, 6.5])
    print(f"   累计负债: {debt['debt_hours']:.1f}小时")
    print(f"   平均睡眠: {debt['average_actual']:.1f}小时/天")
    print(f"   状态: {debt['status']}")
    
    print()
    
    # 4. 睡眠阶段分布
    print("4. 5个睡眠周期的阶段分布：")
    stages = get_sleep_stage_distribution(5)
    print(f"   总时长: {stages['total_hours']}小时")
    for stage, info in stages['stages'].items():
        print(f"   {stage}: {info['minutes']}分钟 ({info['percentage']}%)")