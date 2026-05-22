"""
Reaction Time Utilities - 反应时间计算与分析工具

A comprehensive toolkit for analyzing reaction time data and performance assessment.
Zero external dependencies - pure Python implementation.

Features:
- Reaction time statistics (mean, median, std, percentiles)
- Age-based reaction time benchmarks and comparison
- Performance classification (excellent, good, average, slow)
- Trend analysis and improvement tracking
- Fatigue effect calculation
- Sports/game specific reaction time evaluation
- Driving safety reaction time assessment
- Statistical significance testing for improvements

应用场景:
- 游戏玩家反应速度评估
- 运动员反应能力测试
- 驾驶员安全评估
- 认知功能监测
- 训练效果追踪
"""

from typing import List, Dict, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import math
import random
from datetime import datetime, timedelta


class PerformanceLevel(Enum):
    """表现等级"""
    EXCELLENT = "excellent"      # 优秀
    GOOD = "good"                # 良好
    AVERAGE = "average"          # 平均
    BELOW_AVERAGE = "below_average"  # 中下
    SLOW = "slow"                # 较慢
    VERY_SLOW = "very_slow"      # 很慢


class ReactionTestType(Enum):
    """反应测试类型"""
    SIMPLE = "simple"           # 简单反应（单一刺激）
    CHOICE = "choice"           # 选择反应（多种刺激）
    GO_NOGO = "go_nogo"         # Go/No-Go 测试
    VISUAL = "visual"           # 视觉反应
    AUDITORY = "auditory"       # 听觉反应
    TACTILE = "tactile"         # 触觉反应
    COMPLEX = "complex"         # 复杂反应（多步骤）


class ActivityType(Enum):
    """活动类型"""
    GENERAL = "general"         # 一般日常活动
    GAMING = "gaming"           # 游戏电竞
    SPORTS = "sports"           # 体育运动
    DRIVING = "driving"         # 驾驶
    COGNITIVE = "cognitive"     # 认知测试
    MEDICAL = "medical"         # 医疗监测


@dataclass
class ReactionTimeResult:
    """单次反应时间结果"""
    time_ms: float              # 反应时间（毫秒）
    test_type: ReactionTestType # 测试类型
    stimulus_time: datetime     # 刺激出现时间
    response_time: datetime     # 响应时间
    correct: bool = True        # 是否正确响应
    session_id: Optional[str] = None  # 测试会话ID


@dataclass
class ReactionTimeStatistics:
    """反应时间统计数据"""
    mean: float                 # 平均值 (ms)
    median: float               # 中位数 (ms)
    std: float                  # 标准差 (ms)
    min: float                  # 最小值 (ms)
    max: float                  # 最大值 (ms)
    count: int                  # 样本数量
    percentile_25: float        # 25百分位数
    percentile_75: float        # 75百分位数
    percentile_90: float        # 90百分位数
    percentile_95: float        # 95百分位数
    iqr: float                  # 四分位距
    coefficient_of_variation: float  # 变异系数
    outliers_removed: int = 0   # 移除的异常值数量


@dataclass
class PerformanceAssessment:
    """表现评估结果"""
    level: PerformanceLevel     # 表现等级
    score: float                # 综合得分 (0-100)
    percentile: float           # 在同龄人中的百分位
    age_benchmark_diff: float   # 与同龄基准的差距 (ms)
    classification_reason: str  # 分类原因
    recommendations: List[str] = field(default_factory=list)  # 改进建议


@dataclass
class TrendAnalysis:
    """趋势分析结果"""
    trend_direction: str        # 趋势方向: improving, stable, declining
    improvement_rate: float     # 改善速率 (ms/day)
    consistency_score: float    # 稳定性得分 (0-100)
    predicted_next: float       # 预测下次测试值
    confidence_level: float     # 预测置信度
    data_points: int            # 数据点数量


@dataclass
class FatigueAnalysis:
    """疲劳效应分析"""
    baseline_mean: float        # 基线平均值
    current_mean: float         # 当前平均值
    fatigue_effect: float       # 疲劳效应 (ms)
    fatigue_percentage: float   # 疲劳百分比
    recovery_time_estimate: float  # 预估恢复时间（分钟）
    alert_level: str            # 警示等级: normal, mild, moderate, severe


# ==================== 年龄基准数据 ====================

# 各年龄段平均反应时间基准（简单视觉反应）
AGE_BENCHMARKS: Dict[int, Dict[str, float]] = {
    # 年龄: {mean_ms, std_ms, excellent_threshold, slow_threshold}
    10: {"mean": 250, "std": 40, "excellent": 180, "slow": 350},
    15: {"mean": 200, "std": 30, "excellent": 150, "slow": 280},
    20: {"mean": 180, "std": 25, "excellent": 130, "slow": 250},
    25: {"mean": 190, "std": 28, "excellent": 140, "slow": 260},
    30: {"mean": 200, "std": 30, "excellent": 150, "slow": 280},
    35: {"mean": 210, "std": 32, "excellent": 160, "slow": 300},
    40: {"mean": 220, "std": 35, "excellent": 170, "slow": 320},
    45: {"mean": 230, "std": 38, "excellent": 180, "slow": 340},
    50: {"mean": 250, "std": 40, "excellent": 200, "slow": 360},
    55: {"mean": 270, "std": 45, "excellent": 220, "slow": 380},
    60: {"mean": 290, "std": 50, "excellent": 240, "slow": 400},
    65: {"mean": 320, "std": 55, "excellent": 260, "slow": 450},
    70: {"mean": 350, "std": 60, "excellent": 290, "slow": 500},
    75: {"mean": 380, "std": 70, "excellent": 320, "slow": 550},
}

# 游戏玩家基准（毫秒）
GAMING_BENCHMARKS: Dict[str, Dict[str, float]] = {
    # 游戏类型: {excellent, good, average, slow}
    "fps": {"excellent": 150, "good": 200, "average": 250, "slow": 350},
    "racing": {"excellent": 200, "good": 250, "average": 300, "slow": 400},
    "sports": {"excellent": 180, "good": 230, "average": 280, "slow": 380},
    "rhythm": {"excellent": 100, "good": 150, "average": 200, "slow": 300},
    "fighting": {"excellent": 120, "good": 170, "average": 220, "slow": 320},
    "moba": {"excellent": 180, "good": 230, "average": 280, "slow": 380},
}

# 运动项目基准（毫秒）
SPORTS_BENCHMARKS: Dict[str, Dict[str, float]] = {
    # 运动项目: {excellent, good, average, slow}
    "sprinting": {"excellent": 100, "good": 150, "average": 200, "slow": 300},
    "boxing": {"excellent": 120, "good": 170, "average": 220, "slow": 320},
    "tennis": {"excellent": 150, "good": 200, "average": 250, "slow": 350},
    "baseball": {"excellent": 140, "good": 190, "average": 240, "slow": 340},
    "soccer": {"excellent": 180, "good": 230, "average": 280, "slow": 380},
    "basketball": {"excellent": 160, "good": 210, "average": 260, "slow": 360},
    "table_tennis": {"excellent": 100, "good": 150, "average": 200, "slow": 300},
    "badminton": {"excellent": 120, "good": 170, "average": 220, "slow": 320},
}

# 驾驶安全基准（毫秒）
DRIVING_BENCHMARKS: Dict[str, Dict[str, float]] = {
    # 场景: {safe, caution, warning, danger}
    "normal": {"safe": 300, "caution": 400, "warning": 500, "danger": 600},
    "emergency": {"safe": 250, "caution": 350, "warning": 450, "danger": 550},
    "high_speed": {"safe": 200, "caution": 300, "warning": 400, "danger": 500},
    "night": {"safe": 350, "caution": 450, "warning": 550, "danger": 650},
    "fatigue": {"safe": 400, "caution": 500, "warning": 600, "danger": 700},
}

# 测试类型修正系数（相对于简单反应）
TEST_TYPE_MULTIPLIERS: Dict[ReactionTestType, float] = {
    ReactionTestType.SIMPLE: 1.0,
    ReactionTestType.CHOICE: 1.3,      # 选择反应通常慢30%
    ReactionTestType.GO_NOGO: 1.2,     # Go/No-Go 慢20%
    ReactionTestType.VISUAL: 1.0,      # 基准
    ReactionTestType.AUDITORY: 0.95,   # 听觉反应快5%
    ReactionTestType.TACTILE: 0.9,     # 触觉反应快10%
    ReactionTestType.COMPLEX: 1.5,     # 复杂反应慢50%
}


# ==================== 统计计算 ====================

def calculate_statistics(
    reaction_times: List[float],
    remove_outliers: bool = True,
    outlier_method: str = "iqr"
) -> ReactionTimeStatistics:
    """
    计算反应时间统计数据
    
    Args:
        reaction_times: 反应时间列表（毫秒）
        remove_outliers: 是否移除异常值
        outlier_method: 异常值检测方法 ("iqr", "zscore", "mad")
    
    Returns:
        ReactionTimeStatistics 统计数据
    
    Examples:
        >>> stats = calculate_statistics([180, 195, 200, 210, 220])
        >>> stats.mean
        201.0
        >>> stats.median
        200.0
    """
    if not reaction_times:
        raise ValueError("反应时间列表不能为空")
    
    # 过滤无效值
    times = [t for t in reaction_times if t > 0]
    
    if not times:
        raise ValueError("没有有效的反应时间数据")
    
    # 移除异常值
    outliers_removed = 0
    if remove_outliers:
        times, outliers_removed = _remove_outliers(times, outlier_method)
    
    # 计算基本统计量
    n = len(times)
    mean = sum(times) / n
    
    # 中位数
    sorted_times = sorted(times)
    if n % 2 == 0:
        median = (sorted_times[n // 2 - 1] + sorted_times[n // 2]) / 2
    else:
        median = sorted_times[n // 2]
    
    # 标准差
    variance = sum((t - mean) ** 2 for t in times) / n
    std = math.sqrt(variance)
    
    # 最小值和最大值
    min_val = sorted_times[0]
    max_val = sorted_times[-1]
    
    # 百分位数
    p25 = _percentile(sorted_times, 25)
    p75 = _percentile(sorted_times, 75)
    p90 = _percentile(sorted_times, 90)
    p95 = _percentile(sorted_times, 95)
    
    # 四分位距
    iqr = p75 - p25
    
    # 变异系数
    cv = (std / mean * 100) if mean > 0 else 0
    
    return ReactionTimeStatistics(
        mean=round(mean, 2),
        median=round(median, 2),
        std=round(std, 2),
        min=round(min_val, 2),
        max=round(max_val, 2),
        count=n,
        percentile_25=round(p25, 2),
        percentile_75=round(p75, 2),
        percentile_90=round(p90, 2),
        percentile_95=round(p95, 2),
        iqr=round(iqr, 2),
        coefficient_of_variation=round(cv, 2),
        outliers_removed=outliers_removed
    )


def _percentile(sorted_data: List[float], p: float) -> float:
    """计算百分位数"""
    n = len(sorted_data)
    if n == 1:
        return sorted_data[0]
    
    index = (p / 100) * (n - 1)
    lower = int(math.floor(index))
    upper = int(math.ceil(index))
    
    if lower == upper:
        return sorted_data[lower]
    
    # 线性插值
    weight = index - lower
    return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight


def _remove_outliers(data: List[float], method: str = "iqr") -> Tuple[List[float], int]:
    """移除异常值"""
    if len(data) < 4:
        return data, 0
    
    sorted_data = sorted(data)
    
    if method == "iqr":
        # IQR 方法：超出 Q1-1.5*IQR 或 Q3+1.5*IQR 的值为异常
        q1 = _percentile(sorted_data, 25)
        q3 = _percentile(sorted_data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
    elif method == "zscore":
        # Z-score 方法：|z| > 3 为异常
        mean = sum(data) / len(data)
        std = math.sqrt(sum((x - mean) ** 2 for x in data) / len(data))
        if std == 0:
            return data, 0
        lower_bound = mean - 3 * std
        upper_bound = mean + 3 * std
        
    elif method == "mad":
        # MAD 方法：使用中位数绝对偏差
        median = _percentile(sorted_data, 50)
        mad = sum(abs(x - median) for x in data) / len(data)
        lower_bound = median - 3 * mad
        upper_bound = median + 3 * mad
        
    else:
        return data, 0
    
    filtered = [x for x in data if lower_bound <= x <= upper_bound]
    outliers_removed = len(data) - len(filtered)
    
    return filtered, outliers_removed


# ==================== 表现评估 ====================

def assess_performance(
    reaction_times: List[float],
    age: Optional[int] = None,
    activity_type: ActivityType = ActivityType.GENERAL,
    test_type: ReactionTestType = ReactionTestType.SIMPLE,
    specific_activity: Optional[str] = None
) -> PerformanceAssessment:
    """
    评估反应时间表现
    
    Args:
        reaction_times: 反应时间列表（毫秒）
        age: 年龄（用于年龄基准对比）
        activity_type: 活动类型
        test_type: 测试类型
        specific_activity: 具体活动名称（如 "fps", "tennis"）
    
    Returns:
        PerformanceAssessment 评估结果
    
    Examples:
        >>> assessment = assess_performance([180, 190, 200], age=25)
        >>> assessment.level
        PerformanceLevel.GOOD
    """
    if not reaction_times:
        raise ValueError("需要反应时间数据")
    
    # 计算统计数据
    stats = calculate_statistics(reaction_times)
    mean_time = stats.mean
    
    # 应用测试类型修正
    multiplier = TEST_TYPE_MULTIPLIERS.get(test_type, 1.0)
    adjusted_time = mean_time / multiplier
    
    # 获取基准
    if age and activity_type == ActivityType.GENERAL:
        benchmark = _get_age_benchmark(age)
    elif activity_type == ActivityType.GAMING and specific_activity:
        benchmark = GAMING_BENCHMARKS.get(specific_activity, GAMING_BENCHMARKS["fps"])
    elif activity_type == ActivityType.SPORTS and specific_activity:
        benchmark = SPORTS_BENCHMARKS.get(specific_activity, SPORTS_BENCHMARKS["tennis"])
    elif activity_type == ActivityType.DRIVING:
        benchmark = DRIVING_BENCHMARKS.get(specific_activity or "normal", DRIVING_BENCHMARKS["normal"])
    else:
        benchmark = {"mean": 200, "std": 30, "excellent": 130, "slow": 280}
    
    # 确定表现等级
    level = _determine_performance_level(adjusted_time, benchmark, activity_type)
    
    # 计算百分位
    percentile = _calculate_percentile(adjusted_time, benchmark)
    
    # 计算与基准差距
    benchmark_mean = benchmark.get("mean", 200)
    diff_from_benchmark = adjusted_time - benchmark_mean
    
    # 计算综合得分（0-100，越高越好）
    score = _calculate_performance_score(adjusted_time, benchmark)
    
    # 生成分类原因
    reason = _generate_classification_reason(level, adjusted_time, benchmark, age)
    
    # 生成改进建议
    recommendations = _generate_recommendations(level, stats, activity_type)
    
    return PerformanceAssessment(
        level=level,
        score=round(score, 1),
        percentile=round(percentile, 1),
        age_benchmark_diff=round(diff_from_benchmark, 1),
        classification_reason=reason,
        recommendations=recommendations
    )


def _get_age_benchmark(age: int) -> Dict[str, float]:
    """获取年龄基准"""
    # 找到最接近的年龄组
    ages = list(AGE_BENCHMARKS.keys())
    closest_age = min(ages, key=lambda x: abs(x - age))
    return AGE_BENCHMARKS[closest_age]


def _determine_performance_level(
    time: float,
    benchmark: Dict[str, float],
    activity_type: ActivityType
) -> PerformanceLevel:
    """确定表现等级"""
    
    if activity_type == ActivityType.DRIVING:
        # 驾驶使用特殊评估标准
        safe = benchmark.get("safe", 300)
        caution = benchmark.get("caution", 400)
        warning = benchmark.get("warning", 500)
        danger = benchmark.get("danger", 600)
        
        if time <= safe:
            return PerformanceLevel.EXCELLENT
        elif time <= caution:
            return PerformanceLevel.GOOD
        elif time <= warning:
            return PerformanceLevel.AVERAGE
        elif time <= danger:
            return PerformanceLevel.SLOW
        else:
            return PerformanceLevel.VERY_SLOW
    
    else:
        # 一般评估标准
        excellent = benchmark.get("excellent", 130)
        good = benchmark.get("good", excellent + 50)
        avg = benchmark.get("mean", 200)
        slow = benchmark.get("slow", 280)
        
        if time <= excellent:
            return PerformanceLevel.EXCELLENT
        elif time <= good:
            return PerformanceLevel.GOOD
        elif time <= avg:
            return PerformanceLevel.AVERAGE
        elif time <= slow:
            return PerformanceLevel.BELOW_AVERAGE
        elif time <= slow + 50:
            return PerformanceLevel.SLOW
        else:
            return PerformanceLevel.VERY_SLOW


def _calculate_percentile(time: float, benchmark: Dict[str, float]) -> float:
    """计算百分位排名"""
    mean = benchmark.get("mean", 200)
    std = benchmark.get("std", 30)
    
    if std == 0:
        return 50.0
    
    # 使用正态分布估算百分位
    z = (mean - time) / std  # 时间越短越好，所以用 mean - time
    
    # 正态分布 CDF 估算
    percentile = 50 * (1 + math.erf(z / math.sqrt(2)))
    
    return max(0, min(100, percentile))


def _calculate_performance_score(time: float, benchmark: Dict[str, float]) -> float:
    """计算综合得分"""
    excellent = benchmark.get("excellent", 130)
    slow = benchmark.get("slow", 280)
    
    # 线性映射：excellent -> 100分，slow -> 0分
    if time <= excellent:
        return 100.0
    elif time >= slow + 50:
        return 0.0
    else:
        range_val = slow + 50 - excellent
        score = 100 - ((time - excellent) / range_val) * 100
        return max(0, min(100, score))


def _generate_classification_reason(
    level: PerformanceLevel,
    time: float,
    benchmark: Dict[str, float],
    age: Optional[int]
) -> str:
    """生成分类原因说明"""
    level_names = {
        PerformanceLevel.EXCELLENT: "优秀",
        PerformanceLevel.GOOD: "良好",
        PerformanceLevel.AVERAGE: "平均水平",
        PerformanceLevel.BELOW_AVERAGE: "中下水平",
        PerformanceLevel.SLOW: "较慢",
        PerformanceLevel.VERY_SLOW: "很慢，需要关注"
    }
    
    benchmark_mean = benchmark.get("mean", 200)
    diff = time - benchmark_mean
    
    if age:
        age_str = f"在{age}岁年龄组中，"
    else:
        age_str = ""
    
    if diff < 0:
        diff_str = f"比同龄平均水平快{abs(diff):.1f}毫秒"
    else:
        diff_str = f"比同龄平均水平慢{diff:.1f}毫秒"
    
    return f"{age_str}平均反应时间{time:.1f}毫秒，{diff_str}，属于{level_names[level]}表现。"


def _generate_recommendations(
    level: PerformanceLevel,
    stats: ReactionTimeStatistics,
    activity_type: ActivityType
) -> List[str]:
    """生成改进建议"""
    recommendations = []
    
    # 基于表现等级的建议
    if level == PerformanceLevel.VERY_SLOW:
        recommendations.append("建议进行专业认知功能评估")
        recommendations.append("检查是否存在疲劳、睡眠不足或健康问题")
    
    if level in [PerformanceLevel.SLOW, PerformanceLevel.BELOW_AVERAGE]:
        recommendations.append("建议每天进行反应训练练习")
        recommendations.append("保证充足睡眠和规律作息")
    
    # 基于变异系数的建议
    if stats.coefficient_of_variation > 20:
        recommendations.append("反应时间波动较大，建议提高稳定性训练")
    
    # 基于活动类型的建议
    if activity_type == ActivityType.GAMING:
        recommendations.append("尝试游戏内的反应训练模式")
        recommendations.append("保持游戏时的良好坐姿和环境光线")
    
    if activity_type == ActivityType.DRIVING:
        if level in [PerformanceLevel.SLOW, PerformanceLevel.VERY_SLOW]:
            recommendations.append("驾驶前确保充分休息")
            recommendations.append("避免疲劳驾驶，定期休息")
    
    if activity_type == ActivityType.SPORTS:
        recommendations.append("加入专项反应训练（如球类接发训练）")
        recommendations.append("加强视觉追踪和预判能力训练")
    
    return recommendations


# ==================== 趋势分析 ====================

def analyze_trend(
    session_results: List[Tuple[datetime, float]],
    min_data_points: int = 5
) -> TrendAnalysis:
    """
    分析反应时间趋势
    
    Args:
        session_results: 按时间顺序的测试结果 [(日期, 平均反应时间)]
        min_data_points: 最小数据点要求
    
    Returns:
        TrendAnalysis 趋势分析结果
    
    Examples:
        >>> from datetime import datetime, timedelta
        >>> sessions = [
        ...     (datetime.now() - timedelta(days=i), 200 + i*2)
        ...     for i in range(10, 0, -1)
        ... ]
        >>> trend = analyze_trend(sessions)
        >>> trend.trend_direction
        'improving'
    """
    if len(session_results) < min_data_points:
        return TrendAnalysis(
            trend_direction="insufficient_data",
            improvement_rate=0,
            consistency_score=0,
            predicted_next=0,
            confidence_level=0,
            data_points=len(session_results)
        )
    
    # 按时间排序
    sorted_results = sorted(session_results, key=lambda x: x[0])
    
    # 计算日期差和反应时间变化
    dates = [r[0] for r in sorted_results]
    times = [r[1] for r in sorted_results]
    
    # 使用线性回归计算趋势
    n = len(times)
    x_days = [(dates[i] - dates[0]).days for i in range(n)]
    
    # 简单线性回归
    sum_x = sum(x_days)
    sum_y = sum(times)
    sum_xy = sum(x * y for x, y in zip(x_days, times))
    sum_x2 = sum(x ** 2 for x in x_days)
    
    # slope = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x^2)
    denominator = n * sum_x2 - sum_x ** 2
    if denominator == 0:
        slope = 0
    else:
        slope = (n * sum_xy - sum_x * sum_y) / denominator
    
    # 计算改善速率（负斜率表示改善，因为时间减少是好事）
    improvement_rate = -slope  # 每天改善的毫秒数
    
    # 确定趋势方向
    if abs(slope) < 1:  # 变化小于1ms/day
        direction = "stable"
    elif slope < 0:
        direction = "improving"
    else:
        direction = "declining"
    
    # 计算稳定性得分（基于R²）
    mean_y = sum_y / n
    ss_tot = sum((y - mean_y) ** 2 for y in times)
    
    intercept = (sum_y - slope * sum_x) / n
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(x_days, times))
    
    if ss_tot == 0:
        r_squared = 1.0
    else:
        r_squared = 1 - ss_res / ss_tot
    
    # 稳定性得分（R²越高越稳定）
    consistency_score = max(0, min(100, r_squared * 100))
    
    # 预测下一次测试值
    last_day = x_days[-1]
    next_day = last_day + 1  # 假设每天测试
    predicted_next = slope * next_day + intercept
    
    # 计算置信度
    # 更多数据点和更高的R²意味着更高的置信度
    data_confidence = min(len(times) / 20, 1.0) * 50
    model_confidence = r_squared * 50
    confidence_level = data_confidence + model_confidence
    
    return TrendAnalysis(
        trend_direction=direction,
        improvement_rate=round(improvement_rate, 3),
        consistency_score=round(consistency_score, 1),
        predicted_next=round(predicted_next, 1),
        confidence_level=round(confidence_level, 1),
        data_points=n
    )


# ==================== 疲劳分析 ====================

def analyze_fatigue(
    baseline_results: List[float],
    current_results: List[float]
) -> FatigueAnalysis:
    """
    分析疲劳对反应时间的影响
    
    Args:
        baseline_results: 基线反应时间（良好状态下测得）
        current_results: 当前反应时间
    
    Returns:
        FatigueAnalysis 疲劳分析结果
    
    Examples:
        >>> fatigue = analyze_fatigue([180, 185, 190], [250, 260, 270])
        >>> fatigue.fatigue_percentage
        42.1...
    """
    if not baseline_results or not current_results:
        raise ValueError("需要基线和当前反应时间数据")
    
    baseline_mean = sum(baseline_results) / len(baseline_results)
    current_mean = sum(current_results) / len(current_results)
    
    # 疲劳效应（反应时间增加量）
    fatigue_effect = current_mean - baseline_mean
    
    # 疲劳百分比
    if baseline_mean > 0:
        fatigue_percentage = (fatigue_effect / baseline_mean) * 100
    else:
        fatigue_percentage = 0
    
    # 预估恢复时间（基于经验公式）
    # 每10%疲劳约需15分钟恢复
    recovery_time = abs(fatigue_percentage) * 1.5
    
    # 确定警示等级
    if fatigue_percentage <= 10:
        alert_level = "normal"
    elif fatigue_percentage <= 25:
        alert_level = "mild"
    elif fatigue_percentage <= 40:
        alert_level = "moderate"
    else:
        alert_level = "severe"
    
    return FatigueAnalysis(
        baseline_mean=round(baseline_mean, 1),
        current_mean=round(current_mean, 1),
        fatigue_effect=round(fatigue_effect, 1),
        fatigue_percentage=round(fatigue_percentage, 1),
        recovery_time_estimate=round(recovery_time, 1),
        alert_level=alert_level
    )


# ==================== 模拟测试生成 ====================

def generate_reaction_test_data(
    count: int = 20,
    base_mean: float = 200,
    std: float = 30,
    include_errors: bool = False,
    error_rate: float = 0.05
) -> List[ReactionTimeResult]:
    """
    生成模拟反应测试数据
    
    Args:
        count: 测试次数
        base_mean: 基准平均反应时间
        std: 标准差
        include_errors: 是否包含错误响应
        error_rate: 错误率
    
    Returns:
        ReactionTimeResult 列表
    
    Examples:
        >>> results = generate_reaction_test_data(10, 180, 20)
        >>> len(results)
        10
    """
    results = []
    base_time = datetime.now() - timedelta(minutes=count * 2)
    
    for i in range(count):
        # 生成随机反应时间（正态分布）
        time_ms = random.gauss(base_mean, std)
        time_ms = max(50, time_ms)  # 限制最小值
        
        # 判断是否错误
        correct = True
        if include_errors and random.random() < error_rate:
            correct = False
            time_ms = random.uniform(500, 1000)  # 错误反应通常较慢
        
        stimulus_time = base_time + timedelta(minutes=i * 2)
        response_time = stimulus_time + timedelta(milliseconds=time_ms)
        
        results.append(ReactionTimeResult(
            time_ms=round(time_ms, 1),
            test_type=ReactionTestType.SIMPLE,
            stimulus_time=stimulus_time,
            response_time=response_time,
            correct=correct,
            session_id="simulated"
        ))
    
    return results


def simulate_progressive_improvement(
    days: int = 30,
    start_mean: float = 250,
    end_mean: float = 180,
    daily_std: float = 25,
    tests_per_day: int = 5
) -> List[Tuple[datetime, List[float]]]:
    """
    模拟渐进式改善训练
    
    Args:
        days: 训练天数
        start_mean: 开始平均时间
        end_mean: 目标平均时间
        daily_std: 每日测试标准差
        tests_per_day: 每天测试次数
    
    Returns:
        [(日期, 该日测试结果列表)]
    
    Examples:
        >>> training = simulate_progressive_improvement(10, 250, 200)
        >>> len(training)
        10
    """
    results = []
    start_date = datetime.now() - timedelta(days=days)
    
    for day in range(days):
        # 计算当日目标均值（线性递减）
        progress = day / days
        current_mean = start_mean - (start_mean - end_mean) * progress
        
        # 生成当日测试
        day_tests = []
        for _ in range(tests_per_day):
            time_ms = random.gauss(current_mean, daily_std)
            time_ms = max(50, round(time_ms, 1))
            day_tests.append(time_ms)
        
        date = start_date + timedelta(days=day)
        results.append((date, day_tests))
    
    return results


# ==================== 比较分析 ====================

def compare_groups(
    group_a: List[float],
    group_b: List[float],
    group_a_name: str = "Group A",
    group_b_name: str = "Group B"
) -> Dict:
    """
    比较两组反应时间数据
    
    Args:
        group_a: 第一组反应时间
        group_b: 第二组反应时间
        group_a_name: 第一组名称
        group_b_name: 第二组名称
    
    Returns:
        比较结果字典
    
    Examples:
        >>> comparison = compare_groups([180, 190, 200], [210, 220, 230])
        >>> comparison['difference']
        30.0
    """
    stats_a = calculate_statistics(group_a)
    stats_b = calculate_statistics(group_b)
    
    # 计算差异
    mean_diff = stats_a.mean - stats_b.mean
    
    # 简单显著性检验（独立样本）
    # 使用 Welch's t-test 的简化版本
    n1, n2 = stats_a.count, stats_b.count
    s1, s2 = stats_a.std, stats_b.std
    
    # 标准误差
    se = math.sqrt(s1**2/n1 + s2**2/n2)
    
    # t 值
    if se > 0:
        t_value = abs(mean_diff) / se
    else:
        t_value = 0
    
    # 自由度（Welch-Satterthwaite 方程）
    if s1**2/n1 + s2**2/n2 > 0:
        df = ((s1**2/n1 + s2**2/n2)**2) / (
            (s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1)
        )
    else:
        df = n1 + n2 - 2
    
    # 简化的 p 值估算（使用正态近似）
    # t > 2 通常表示显著差异
    significant = t_value > 2
    
    # Cohen's d 效应量
    pooled_std = math.sqrt((s1**2 + s2**2) / 2)
    if pooled_std > 0:
        cohens_d = mean_diff / pooled_std
    else:
        cohens_d = 0
    
    return {
        "group_a_stats": stats_a,
        "group_b_stats": stats_b,
        "group_a_name": group_a_name,
        "group_b_name": group_b_name,
        "difference": round(mean_diff, 2),
        "faster_group": group_a_name if mean_diff < 0 else group_b_name,
        "t_value": round(t_value, 3),
        "degrees_of_freedom": round(df, 1),
        "significant_difference": significant,
        "cohens_d": round(cohens_d, 3),
        "effect_size_interpretation": _interpret_cohens_d(cohens_d),
        "comparison_summary": f"{group_a_name} 平均 {stats_a.mean}ms，"
                             f"{group_b_name} 平均 {stats_b.mean}ms，"
                             f"差异 {abs(mean_diff)}ms"
    }


def _interpret_cohens_d(d: float) -> str:
    """解释 Cohen's d 效应量"""
    abs_d = abs(d)
    if abs_d < 0.2:
        return "效果很小"
    elif abs_d < 0.5:
        return "效果较小"
    elif abs_d < 0.8:
        return "中等效果"
    else:
        return "效果显著"


# ==================== 驾驶安全评估 ====================

def assess_driving_safety(
    reaction_times: List[float],
    driving_scenario: str = "normal",
    driver_age: Optional[int] = None
) -> Dict:
    """
    评估驾驶安全性
    
    Args:
        reaction_times: 反应时间数据
        driving_scenario: 驾驶场景 (normal, emergency, high_speed, night, fatigue)
        driver_age: 驾驶员年龄
    
    Returns:
        驾驶安全评估结果
    
    Examples:
        >>> safety = assess_driving_safety([280, 300, 320])
        >>> safety['safety_rating']
        'safe'
    """
    if not reaction_times:
        raise ValueError("需要反应时间数据")
    
    stats = calculate_statistics(reaction_times)
    mean_time = stats.mean
    
    # 获取场景基准
    benchmark = DRIVING_BENCHMARKS.get(driving_scenario, DRIVING_BENCHMARKS["normal"])
    
    # 确定安全等级
    safe = benchmark["safe"]
    caution = benchmark["caution"]
    warning = benchmark["warning"]
    danger = benchmark["danger"]
    
    if mean_time <= safe:
        rating = "safe"
        message = "反应时间充足，驾驶安全性良好"
    elif mean_time <= caution:
        rating = "caution"
        message = "反应时间尚可，建议保持警觉"
    elif mean_time <= warning:
        rating = "warning"
        message = "反应时间偏慢，建议提高注意力和休息"
    else:
        rating = "danger"
        message = "反应时间过慢，存在安全隐患，不建议驾驶"
    
    # 计算理论制动距离（假设车速 60 km/h）
    # 反应时间内车辆行驶的距离
    speed_mps = 60 / 3.6  # 60 km/h 转换为 m/s
    reaction_distance = mean_time / 1000 * speed_mps
    
    # 年龄因素
    age_factor = None
    if driver_age:
        age_benchmark = _get_age_benchmark(driver_age)
        age_factor = {
            "age_group_mean": age_benchmark["mean"],
            "compared_to_age": mean_time - age_benchmark["mean"]
        }
    
    # 建议
    recommendations = []
    if rating in ["warning", "danger"]:
        recommendations.append("确保充分休息后再驾驶")
        recommendations.append("避免夜间或疲劳时驾驶")
        recommendations.append("保持更长的跟车距离")
    if stats.coefficient_of_variation > 20:
        recommendations.append("反应不稳定，需特别注意")
    
    return {
        "safety_rating": rating,
        "safety_message": message,
        "mean_reaction_time": round(mean_time, 1),
        "reaction_distance_at_60kmh": round(reaction_distance, 2),
        "scenario": driving_scenario,
        "statistics": stats,
        "age_comparison": age_factor,
        "recommendations": recommendations
    }


# ==================== 训练建议 ====================

def generate_training_plan(
    current_level: PerformanceLevel,
    target_level: PerformanceLevel = PerformanceLevel.GOOD,
    activity_type: ActivityType = ActivityType.GENERAL,
    weeks: int = 4
) -> Dict:
    """
    生成训练计划
    
    Args:
        current_level: 当前表现等级
        target_level: 目标表现等级
        activity_type: 活动类型
        weeks: 训练周数
    
    Returns:
        训练计划字典
    
    Examples:
        >>> plan = generate_training_plan(PerformanceLevel.AVERAGE)
        >>> plan['total_sessions']
        20
    """
    # 训练强度映射
    level_intensity = {
        PerformanceLevel.VERY_SLOW: {"sessions_per_week": 7, "duration_minutes": 20},
        PerformanceLevel.SLOW: {"sessions_per_week": 6, "duration_minutes": 15},
        PerformanceLevel.BELOW_AVERAGE: {"sessions_per_week": 5, "duration_minutes": 12},
        PerformanceLevel.AVERAGE: {"sessions_per_week": 4, "duration_minutes": 10},
        PerformanceLevel.GOOD: {"sessions_per_week": 3, "duration_minutes": 8},
        PerformanceLevel.EXCELLENT: {"sessions_per_week": 2, "duration_minutes": 5},
    }
    
    intensity = level_intensity.get(current_level, level_intensity[PerformanceLevel.AVERAGE])
    
    # 根据目标调整
    if target_level.value < current_level.value:  # 更高级别
        intensity["sessions_per_week"] = min(intensity["sessions_per_week"] + 1, 7)
    
    # 训练类型
    training_types = _get_training_types(activity_type)
    
    # 每周安排
    weekly_schedule = []
    for week in range(1, weeks + 1):
        week_plan = {
            "week": week,
            "sessions": intensity["sessions_per_week"],
            "session_duration": intensity["duration_minutes"],
            "focus": _get_weekly_focus(week, activity_type),
            "training_types": training_types[:3] if week <= 2 else training_types
        }
        weekly_schedule.append(week_plan)
    
    total_sessions = weeks * intensity["sessions_per_week"]
    
    return {
        "current_level": current_level.value,
        "target_level": target_level.value,
        "activity_type": activity_type.value,
        "weeks": weeks,
        "sessions_per_week": intensity["sessions_per_week"],
        "session_duration_minutes": intensity["duration_minutes"],
        "total_sessions": total_sessions,
        "weekly_schedule": weekly_schedule,
        "training_types": training_types,
        "expected_improvement": _estimate_improvement(current_level, target_level, weeks)
    }


def _get_training_types(activity_type: ActivityType) -> List[str]:
    """获取训练类型"""
    base_types = ["简单反应测试", "选择反应测试", "视觉追踪"]
    
    if activity_type == ActivityType.GAMING:
        return base_types + ["游戏场景模拟", "瞄准训练", "决策训练"]
    
    if activity_type == ActivityType.SPORTS:
        return base_types + ["球类反应", "预判训练", "敏捷性训练"]
    
    if activity_type == ActivityType.DRIVING:
        return base_types + ["驾驶模拟", "紧急制动训练", "路况判断"]
    
    return base_types + ["注意力训练", "节奏训练", "压力测试"]


def _get_weekly_focus(week: int, activity_type: ActivityType) -> str:
    """获取每周训练重点"""
    if week <= 1:
        return "基础反应建立"
    elif week <= 2:
        return "稳定性提升"
    elif week <= 3:
        return "速度突破"
    else:
        return "实战应用与巩固"


def _estimate_improvement(
    current: PerformanceLevel,
    target: PerformanceLevel,
    weeks: int
) -> str:
    """估算改善幅度"""
    level_values = {
        PerformanceLevel.VERY_SLOW: 400,
        PerformanceLevel.SLOW: 350,
        PerformanceLevel.BELOW_AVERAGE: 300,
        PerformanceLevel.AVERAGE: 250,
        PerformanceLevel.GOOD: 200,
        PerformanceLevel.EXCELLENT: 150,
    }
    
    current_ms = level_values.get(current, 250)
    target_ms = level_values.get(target, 200)
    
    improvement = current_ms - target_ms
    rate = improvement / weeks
    
    return f"预计每周改善约{rate:.1f}ms，{weeks}周后可能达到{target.value}水平"


# ==================== 辅助函数 ====================

def reaction_time_to_speed_category(time_ms: float) -> str:
    """
    将反应时间转换为速度类别描述
    
    Args:
        time_ms: 反应时间（毫秒）
    
    Returns:
        速度类别描述
    
    Examples:
        >>> reaction_time_to_speed_category(150)
        '极快'
    """
    if time_ms < 150:
        return "极快（专业级）"
    elif time_ms < 200:
        return "很快（优秀）"
    elif time_ms < 250:
        return "较快（良好）"
    elif time_ms < 300:
        return "正常（平均）"
    elif time_ms < 400:
        return "偏慢"
    else:
        return "较慢（需关注）"


def format_statistics_report(stats: ReactionTimeStatistics) -> str:
    """
    格式化统计报告
    
    Args:
        stats: 反应时间统计数据
    
    Returns:
        格式化报告字符串
    
    Examples:
        >>> stats = calculate_statistics([180, 190, 200, 210, 220])
        >>> print(format_statistics_report(stats))
    """
    report = f"""
反应时间统计报告
================
样本数量: {stats.count} (移除异常值: {stats.outliers_removed})
平均值: {stats.mean} ms
中位数: {stats.median} ms
标准差: {stats.std} ms
最小值: {stats.min} ms
最大值: {stats.max} ms
25百分位: {stats.percentile_25} ms
75百分位: {stats.percentile_75} ms
90百分位: {stats.percentile_90} ms
95百分位: {stats.percentile_95} ms
四分位距: {stats.iqr} ms
变异系数: {stats.coefficient_of_variation}%
"""
    return report.strip()


if __name__ == "__main__":
    # 示例用法
    print("=" * 60)
    print("反应时间工具 - 示例")
    print("=" * 60)
    
    # 1. 生成模拟数据
    print("\n1. 生成模拟反应测试数据:")
    test_data = generate_reaction_test_data(20, 200, 30)
    times = [r.time_ms for r in test_data if r.correct]
    print(f"  生成了 {len(times)} 个有效测试数据")
    
    # 2. 计算统计
    print("\n2. 反应时间统计:")
    stats = calculate_statistics(times)
    print(f"  平均: {stats.mean} ms")
    print(f"  中位数: {stats.median} ms")
    print(f"  标准差: {stats.std} ms")
    
    # 3. 表现评估
    print("\n3. 表现评估 (25岁):")
    assessment = assess_performance(times, age=25)
    print(f"  等级: {assessment.level.value}")
    print(f"  得分: {assessment.score}")
    print(f"  百分位: {assessment.percentile}%")
    
    # 4. 游戏玩家评估
    print("\n4. FPS 游戏玩家评估:")
    game_times = [180, 175, 190, 185, 200]
    game_assessment = assess_performance(
        game_times,
        activity_type=ActivityType.GAMING,
        specific_activity="fps"
    )
    print(f"  FPS 等级: {game_assessment.level.value}")
    print(f"  建议: {game_assessment.recommendations[:2]}")
    
    # 5. 趋势分析
    print("\n5. 训练趋势分析:")
    training = simulate_progressive_improvement(14, 250, 180)
    sessions = [(date, sum(times)/len(times)) for date, times in training]
    trend = analyze_trend(sessions)
    print(f"  趋势: {trend.trend_direction}")
    print(f"  改善速率: {trend.improvement_rate} ms/day")
    
    # 6. 疲劳分析
    print("\n6. 疲劳效应分析:")
    baseline = [180, 185, 190]
    current = [250, 260, 270]
    fatigue = analyze_fatigue(baseline, current)
    print(f"  疲劳效应: {fatigue.fatigue_effect} ms")
    print(f"  疲劳程度: {fatigue.fatigue_percentage}%")
    print(f"  警示等级: {fatigue.alert_level}")
    
    # 7. 驾驶安全评估
    print("\n7. 驾驶安全评估:")
    driving_times = [280, 290, 300, 310, 320]
    safety = assess_driving_safety(driving_times, "normal", 35)
    print(f"  安全等级: {safety['safety_rating']}")
    print(f"  消息: {safety['safety_message']}")
    print(f"  60km/h 反应距离: {safety['reaction_distance_at_60kmh']} m")
    
    # 8. 训练计划
    print("\n8. 训练计划生成:")
    plan = generate_training_plan(PerformanceLevel.AVERAGE)
    print(f"  每周训练: {plan['sessions_per_week']} 次")
    print(f"  每次时长: {plan['session_duration_minutes']} 分钟")
    print(f"  总课时: {plan['total_sessions']} 次")
    
    print("\n" + "=" * 60)