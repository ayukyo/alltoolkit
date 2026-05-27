"""
Menstrual Cycle Utils - 月经周期计算工具

功能：
- 计算月经周期各阶段（月经期、卵泡期、排卵期、黄体期）
- 预测下次月经日期
- 计算排卵日和易孕期
- 计算安全期和危险期
- 周期规律性分析
- 多周期预测
- 个性化建议

使用示例：
    from menstrual_cycle_utils import MenstrualCycleCalculator, calculate_next_period
    
    from datetime import datetime
    
    # 上次月经开始日期
    last_period = datetime(2024, 1, 1)
    
    # 创建计算器
    calc = MenstrualCycleCalculator(last_period, cycle_length=28, period_length=5)
    
    # 预测下一个周期
    pred = calc.predict()
    print(f"下次月经: {pred.next_period_start}")
    print(f"排卵日: {pred.ovulation_date}")
    print(f"易孕期: {pred.fertile_window_start} - {pred.fertile_window_end}")
"""

from .menstrual_cycle import (
    # 类
    MenstrualCycleCalculator,
    CyclePhase,
    FertilityLevel,
    CycleDay,
    CyclePrediction,
    CycleAnalysis,
    # 便捷函数
    calculate_next_period,
    get_fertile_days,
    get_ovulation_date,
    format_date
)

__all__ = [
    "MenstrualCycleCalculator",
    "CyclePhase",
    "FertilityLevel",
    "CycleDay",
    "CyclePrediction",
    "CycleAnalysis",
    "calculate_next_period",
    "get_fertile_days",
    "get_ovulation_date",
    "format_date"
]

__version__ = "1.0.0"