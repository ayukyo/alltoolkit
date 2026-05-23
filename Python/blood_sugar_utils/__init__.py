"""
Blood Sugar Utils - 血糖计算工具

功能：
- 血糖单位转换 (mg/dL ↔ mmol/L)
- 血糖状态评估
- HbA1c 与平均血糖转换
- 胰岛素剂量计算
- 血糖趋势分析
- 血糖报告生成

使用示例:
    from blood_sugar_utils import mgdl_to_mmol, assess_glucose
    print(mgdl_to_mmol(100))  # 5.55
    result = assess_glucose(5.5, fasting=True)
"""

from .mod import (
    GlucoseUnit,
    GlucoseStatus,
    convert_glucose,
    assess_glucose,
    hba1c_to_average_glucose,
    average_glucose_to_hba1c,
    estimate_average_glucose,
    analyze_glucose_trend,
    calculate_insulin_sensitivity,
    carbohydrate_to_insulin,
    glucose_report,
    mgdl_to_mmol,
    mmol_to_mgdl,
)

__all__ = [
    'GlucoseUnit',
    'GlucoseStatus',
    'convert_glucose',
    'assess_glucose',
    'hba1c_to_average_glucose',
    'average_glucose_to_hba1c',
    'estimate_average_glucose',
    'analyze_glucose_trend',
    'calculate_insulin_sensitivity',
    'carbohydrate_to_insulin',
    'glucose_report',
    'mgdl_to_mmol',
    'mmol_to_mgdl',
]

__version__ = '1.0.0'