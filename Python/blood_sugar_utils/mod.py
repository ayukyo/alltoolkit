"""
Blood Sugar Utils - 血糖计算工具

功能：
- 血糖单位转换 (mg/dL ↔ mmol/L)
- 血糖状态评估（低血糖、正常、偏高、糖尿病风险）
- HbA1c 与平均血糖转换
- 胰岛素剂量估算辅助
- 血糖趋势分析

零外部依赖，纯 Python 实现。
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from enum import Enum


class GlucoseUnit(Enum):
    """血糖单位枚举"""
    MG_DL = "mg/dL"  # 毫克/分升（美国常用）
    MMOL_L = "mmol/L"  # 毫摩尔/升（国际单位）


class GlucoseStatus(Enum):
    """血糖状态枚举"""
    SEVERE_HYPOGLYCEMIA = "严重低血糖"      # < 2.8 mmol/L (< 50 mg/dL)
    HYPOGLYCEMIA = "低血糖"                  # 2.8-3.9 mmol/L (50-70 mg/dL)
    NORMAL_FASTING = "正常（空腹）"          # 3.9-5.6 mmol/L (70-100 mg/dL)
    NORMAL_POST_MEAL = "正常（餐后）"        # < 7.8 mmol/L (< 140 mg/dL)
    PREDIABETES_FASTING = "糖尿病前期（空腹）"  # 5.6-6.9 mmol/L (100-125 mg/dL)
    PREDIABETES_POST_MEAL = "糖尿病前期（餐后）"  # 7.8-11.0 mmol/L (140-199 mg/dL)
    DIABETES_FASTING = "糖尿病（空腹）"      # >= 7.0 mmol/L (>= 126 mg/dL)
    DIABETES_POST_MEAL = "糖尿病（餐后）"    # >= 11.1 mmol/L (>= 200 mg/dL)
    HIGH = "高血糖"                          # 通用高血糖


# 单位转换常量
# 1 mmol/L = 18.018 mg/dL
MGDL_TO_MMOL = 0.0555
MMOL_TO_MGDL = 18.018


def convert_glucose(value: float, from_unit: GlucoseUnit, to_unit: GlucoseUnit) -> float:
    """
    血糖单位转换
    
    Args:
        value: 血糖值
        from_unit: 原始单位
        to_unit: 目标单位
    
    Returns:
        转换后的血糖值
    
    Examples:
        >>> convert_glucose(100, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)
        5.55
        >>> convert_glucose(5.5, GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL)
        99.1
    """
    if from_unit == to_unit:
        return value
    
    # 先转换为 mg/dL
    if from_unit == GlucoseUnit.MMOL_L:
        mgdl = value * MMOL_TO_MGDL
    else:
        mgdl = value
    
    # 再转换为目标单位
    if to_unit == GlucoseUnit.MMOL_L:
        return round(mgdl * MGDL_TO_MMOL, 2)
    return round(mgdl, 1)


def assess_glucose(value: float, unit: GlucoseUnit = GlucoseUnit.MMOL_L, 
                   fasting: bool = True, age: Optional[int] = None) -> Dict:
    """
    评估血糖状态
    
    Args:
        value: 血糖值
        unit: 血糖单位
        fasting: 是否为空腹血糖
        age: 年龄（可选，用于调整标准）
    
    Returns:
        评估结果字典，包含状态、建议等信息
    
    Examples:
        >>> assess_glucose(5.5, GlucoseUnit.MMOL_L, fasting=True)
        {'status': '正常（空腹）', 'risk_level': 'low', ...}
    """
    # 转换为 mmol/L 进行评估
    mmol_value = value if unit == GlucoseUnit.MMOL_L else convert_glucose(value, unit, GlucoseUnit.MMOL_L)
    mgdl_value = value if unit == GlucoseUnit.MG_DL else convert_glucose(value, unit, GlucoseUnit.MG_DL)
    
    # 年龄调整因子
    age_factor = 1.0
    if age is not None:
        if age >= 65:
            age_factor = 1.1  # 老年人标准稍宽
        elif age < 18:
            age_factor = 0.95  # 儿童标准稍严
    
    result = {
        'value_mmol': round(mmol_value, 2),
        'value_mgdl': round(mgdl_value, 1),
        'fasting': fasting,
        'age_adjusted': age is not None
    }
    
    # 评估血糖状态
    if fasting:
        if mmol_value < 2.8:
            result['status'] = GlucoseStatus.SEVERE_HYPOGLYCEMIA.value
            result['risk_level'] = 'critical'
            result['recommendation'] = '立即进食或就医，严重低血糖可能危及生命'
        elif mmol_value < 3.9:
            result['status'] = GlucoseStatus.HYPOGLYCEMIA.value
            result['risk_level'] = 'high'
            result['recommendation'] = '建议进食快速升糖食物，如糖果、果汁'
        elif mmol_value <= 5.6 * age_factor:
            result['status'] = GlucoseStatus.NORMAL_FASTING.value
            result['risk_level'] = 'low'
            result['recommendation'] = '血糖正常，继续保持健康生活方式'
        elif mmol_value < 7.0:
            result['status'] = GlucoseStatus.PREDIABETES_FASTING.value
            result['risk_level'] = 'medium'
            result['recommendation'] = '建议调整饮食，增加运动，定期复查'
        else:
            result['status'] = GlucoseStatus.DIABETES_FASTING.value
            result['risk_level'] = 'high'
            result['recommendation'] = '建议尽快就医，进行糖化血红蛋白等检查'
    else:
        # 餐后血糖（2小时后）
        if mmol_value < 3.9:
            result['status'] = GlucoseStatus.HYPOGLYCEMIA.value
            result['risk_level'] = 'high'
            result['recommendation'] = '餐后低血糖不常见，建议就医检查'
        elif mmol_value < 7.8 * age_factor:
            result['status'] = GlucoseStatus.NORMAL_POST_MEAL.value
            result['risk_level'] = 'low'
            result['recommendation'] = '餐后血糖正常'
        elif mmol_value < 11.1:
            result['status'] = GlucoseStatus.PREDIABETES_POST_MEAL.value
            result['risk_level'] = 'medium'
            result['recommendation'] = '糖耐量受损，建议调整饮食结构'
        else:
            result['status'] = GlucoseStatus.DIABETES_POST_MEAL.value
            result['risk_level'] = 'high'
            result['recommendation'] = '建议尽快就医，可能需要药物治疗'
    
    return result


def hba1c_to_average_glucose(hba1c: float) -> Dict:
    """
    糖化血红蛋白(HbA1c)转换为平均血糖
    
    使用公式: 平均血糖(mg/dL) = 28.7 × HbA1c - 46.7
    或: 平均血糖(mmol/L) = 1.59 × HbA1c - 2.59
    
    Args:
        hba1c: 糖化血红蛋白值（%）
    
    Returns:
        包含平均血糖（两种单位）和状态评估的字典
    
    Examples:
        >>> hba1c_to_average_glucose(6.5)
        {'hba1c': 6.5, 'avg_glucose_mmol': 7.73, 'avg_glucose_mgdl': 139.2, ...}
    """
    # ADAG研究公式
    avg_mgdl = 28.7 * hba1c - 46.7
    avg_mmol = 1.59 * hba1c - 2.59
    
    result = {
        'hba1c': hba1c,
        'avg_glucose_mmol': round(avg_mmol, 2),
        'avg_glucose_mgdl': round(avg_mgdl, 1)
    }
    
    # 评估 HbA1c 状态
    if hba1c < 5.7:
        result['status'] = '正常'
        result['risk'] = 'low'
        result['recommendation'] = '糖化血红蛋白正常，继续保持'
    elif hba1c < 6.5:
        result['status'] = '糖尿病前期'
        result['risk'] = 'medium'
        result['recommendation'] = '有糖尿病风险，建议改善生活方式'
    elif hba1c < 7.0:
        result['status'] = '糖尿病（控制尚可）'
        result['risk'] = 'medium'
        result['recommendation'] = '糖尿病诊断，需治疗控制'
    elif hba1c < 8.0:
        result['status'] = '糖尿病（控制不佳）'
        result['risk'] = 'high'
        result['recommendation'] = '血糖控制需要改善'
    else:
        result['status'] = '糖尿病（控制很差）'
        result['risk'] = 'critical'
        result['recommendation'] = '需要积极治疗干预'
    
    return result


def average_glucose_to_hba1c(avg_glucose: float, unit: GlucoseUnit = GlucoseUnit.MMOL_L) -> Dict:
    """
    平均血糖转换为糖化血红蛋白(HbA1c)
    
    使用公式: HbA1c(%) = (平均血糖(mg/dL) + 46.7) / 28.7
    或: HbA1c(%) = (平均血糖(mmol/L) + 2.59) / 1.59
    
    Args:
        avg_glucose: 平均血糖值
        unit: 血糖单位
    
    Returns:
        包含 HbA1c 估算值的字典
    
    Examples:
        >>> average_glucose_to_hba1c(7.8, GlucoseUnit.MMOL_L)
        {'hba1c': 6.52, 'avg_glucose_mmol': 7.8, ...}
    """
    if unit == GlucoseUnit.MMOL_L:
        hba1c = (avg_glucose + 2.59) / 1.59
        avg_mmol = avg_glucose
        avg_mgdl = convert_glucose(avg_glucose, GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL)
    else:
        hba1c = (avg_glucose + 46.7) / 28.7
        avg_mgdl = avg_glucose
        avg_mmol = convert_glucose(avg_glucose, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)
    
    result = {
        'hba1c': round(hba1c, 2),
        'avg_glucose_mmol': round(avg_mmol, 2),
        'avg_glucose_mgdl': round(avg_mgdl, 1)
    }
    
    # 评估状态
    if hba1c < 5.7:
        result['status'] = '正常范围'
    elif hba1c < 6.5:
        result['status'] = '糖尿病前期范围'
    else:
        result['status'] = '糖尿病范围'
    
    return result


def estimate_average_glucose(readings: List[Tuple[float, GlucoseUnit]]) -> Dict:
    """
    根据多次血糖读数估算平均血糖
    
    Args:
        readings: 血糖读数列表，每个元素为 (值, 单位) 元组
    
    Returns:
        包含平均值、标准差等统计信息的字典
    
    Examples:
        >>> readings = [(5.5, GlucoseUnit.MMOL_L), (6.0, GlucoseUnit.MMOL_L), (5.8, GlucoseUnit.MMOL_L)]
        >>> estimate_average_glucose(readings)
        {'avg_mmol': 5.77, 'avg_mgdl': 103.9, ...}
    """
    if not readings:
        return {'error': '没有血糖读数'}
    
    # 转换所有读数为 mmol/L
    mmol_readings = [r[0] if r[1] == GlucoseUnit.MMOL_L else convert_glucose(r[0], r[1], GlucoseUnit.MMOL_L) 
                     for r in readings]
    
    n = len(mmol_readings)
    avg = sum(mmol_readings) / n
    
    # 计算标准差
    if n > 1:
        variance = sum((x - avg) ** 2 for x in mmol_readings) / (n - 1)
        std_dev = variance ** 0.5
    else:
        std_dev = 0
    
    # 计算变异系数（CV）
    cv = (std_dev / avg * 100) if avg > 0 else 0
    
    # 最小值和最大值
    min_val = min(mmol_readings)
    max_val = max(mmol_readings)
    
    # 计算目标范围内时间（假设目标范围 3.9-10.0 mmol/L）
    target_range = (3.9, 10.0)
    in_range = sum(1 for x in mmol_readings if target_range[0] <= x <= target_range[1])
    time_in_range = (in_range / n * 100) if n > 0 else 0
    
    # 估算 HbA1c
    hba1c_est = average_glucose_to_hba1c(avg, GlucoseUnit.MMOL_L)
    
    return {
        'count': n,
        'avg_mmol': round(avg, 2),
        'avg_mgdl': round(convert_glucose(avg, GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL), 1),
        'std_dev_mmol': round(std_dev, 2),
        'cv_percent': round(cv, 1),
        'min_mmol': round(min_val, 2),
        'max_mmol': round(max_val, 2),
        'range_mmol': round(max_val - min_val, 2),
        'time_in_range_percent': round(time_in_range, 1),
        'estimated_hba1c': hba1c_est['hba1c'],
        'hba1c_status': hba1c_est['status'],
        'glucose_variability': '低' if cv < 36 else '中' if cv < 50 else '高'
    }


def analyze_glucose_trend(readings: List[Tuple[float, GlucoseUnit, datetime]]) -> Dict:
    """
    分析血糖趋势
    
    Args:
        readings: 血糖读数列表，每个元素为 (值, 单位, 时间) 元组
    
    Returns:
        趋势分析结果
    
    Examples:
        >>> from datetime import datetime, timedelta
        >>> now = datetime.now()
        >>> readings = [
        ...     (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=2)),
        ...     (6.0, GlucoseUnit.MMOL_L, now - timedelta(hours=1)),
        ...     (6.5, GlucoseUnit.MMOL_L, now)
        ... ]
        >>> analyze_glucose_trend(readings)
        {'trend': '上升', 'slope': 0.5, ...}
    """
    if not readings:
        return {'error': '没有血糖读数'}
    
    if len(readings) < 2:
        return {'error': '需要至少2个读数来分析趋势'}
    
    # 按时间排序
    sorted_readings = sorted(readings, key=lambda x: x[2])
    
    # 转换为 mmol/L 并提取时间和值
    times = [(r[2] - sorted_readings[0][2]).total_seconds() / 3600 for r in sorted_readings]  # 小时
    values = [r[0] if r[1] == GlucoseUnit.MMOL_L else convert_glucose(r[0], r[1], GlucoseUnit.MMOL_L) 
              for r in sorted_readings]
    
    # 线性回归计算趋势
    n = len(times)
    sum_x = sum(times)
    sum_y = sum(values)
    sum_xy = sum(t * v for t, v in zip(times, values))
    sum_xx = sum(t * t for t in times)
    
    # 斜率 (mmol/L/小时)
    denominator = n * sum_xx - sum_x * sum_x
    if denominator == 0:
        slope = 0
    else:
        slope = (n * sum_xy - sum_x * sum_y) / denominator
    
    # 判断趋势
    if slope > 0.1:
        trend = '上升'
        trend_arrow = '↑'
    elif slope > 0.05:
        trend = '轻微上升'
        trend_arrow = '↗'
    elif slope < -0.1:
        trend = '下降'
        trend_arrow = '↓'
    elif slope < -0.05:
        trend = '轻微下降'
        trend_arrow = '↘'
    else:
        trend = '平稳'
        trend_arrow = '→'
    
    # 预测下一小时血糖
    predicted_next = values[-1] + slope
    
    return {
        'trend': trend,
        'trend_arrow': trend_arrow,
        'slope_mmol_per_hour': round(slope, 3),
        'current_mmol': round(values[-1], 2),
        'current_mgdl': round(convert_glucose(values[-1], GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL), 1),
        'predicted_next_mmol': round(predicted_next, 2),
        'predicted_status': assess_glucose(predicted_next, GlucoseUnit.MMOL_L, fasting=False)['status'],
        'readings_count': n,
        'time_span_hours': round(times[-1], 2)
    }


def calculate_insulin_sensitivity(
    current_glucose: float,
    target_glucose: float,
    correction_factor: float,
    unit: GlucoseUnit = GlucoseUnit.MMOL_L
) -> Dict:
    """
    计算胰岛素敏感性校正剂量
    
    Args:
        current_glucose: 当前血糖
        target_glucose: 目标血糖
        correction_factor: 胰岛素敏感因子（ISF，每单位胰岛素降低的血糖值）
        unit: 血糖单位
    
    Returns:
        校正剂量计算结果
    
    Examples:
        >>> calculate_insulin_sensitivity(10.0, 6.0, 2.0, GlucoseUnit.MMOL_L)
        {'correction_units': 2.0, 'current_mmol': 10.0, ...}
    """
    # 确保单位一致
    if unit == GlucoseUnit.MG_DL:
        current_mmol = convert_glucose(current_glucose, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)
        target_mmol = convert_glucose(target_glucose, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)
        # ISF 也需要转换为 mmol/L
        cf_mmol = correction_factor * MGDL_TO_MMOL
    else:
        current_mmol = current_glucose
        target_mmol = target_glucose
        cf_mmol = correction_factor
    
    # 计算需要降低的血糖值
    glucose_diff = current_mmol - target_mmol
    
    # 计算校正剂量
    if cf_mmol > 0:
        correction_units = glucose_diff / cf_mmol
    else:
        correction_units = 0
    
    return {
        'current_mmol': round(current_mmol, 2),
        'current_mgdl': round(convert_glucose(current_mmol, GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL), 1),
        'target_mmol': round(target_mmol, 2),
        'target_mgdl': round(convert_glucose(target_mmol, GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL), 1),
        'glucose_difference_mmol': round(glucose_diff, 2),
        'correction_factor': correction_factor,
        'correction_units': round(correction_units, 2),
        'recommendation': f'建议注射 {max(0, round(correction_units, 1))} 单位胰岛素' if correction_units > 0 else '无需校正'
    }


def carbohydrate_to_insulin(
    carbs: float,
    icr: float,
    current_glucose: float = None,
    target_glucose: float = None,
    isf: float = None,
    unit: GlucoseUnit = GlucoseUnit.MMOL_L
) -> Dict:
    """
    碳水化合物转胰岛素剂量计算
    
    Args:
        carbs: 碳水化合物克数
        icr: 胰岛素与碳水比（Insulin-to-Carb Ratio，每单位胰岛素处理的碳水克数）
        current_glucose: 当前血糖（可选）
        target_glucose: 目标血糖（可选）
        isf: 胰岛素敏感因子（可选）
        unit: 血糖单位
    
    Returns:
        胰岛素剂量计算结果
    
    Examples:
        >>> carbohydrate_to_insulin(60, 10)  # 60g碳水，1:10的比例
        {'carb_units': 6.0, 'total_units': 6.0, ...}
    """
    # 计算餐时胰岛素
    carb_units = carbs / icr if icr > 0 else 0
    
    result = {
        'carbs_grams': carbs,
        'icr': icr,
        'carb_units': round(carb_units, 2)
    }
    
    # 如果提供了血糖信息，计算校正剂量
    if all(v is not None for v in [current_glucose, target_glucose, isf]):
        correction = calculate_insulin_sensitivity(current_glucose, target_glucose, isf, unit)
        correction_units = max(0, correction['correction_units'])
        total_units = carb_units + correction_units
        
        result['current_glucose_mmol'] = correction['current_mmol']
        result['target_glucose_mmol'] = correction['target_mmol']
        result['correction_units'] = round(correction_units, 2)
        result['total_units'] = round(total_units, 2)
        result['recommendation'] = f'餐时 {round(carb_units, 1)} 单位 + 校正 {round(correction_units, 1)} 单位 = 总计 {round(total_units, 1)} 单位'
    else:
        result['total_units'] = round(carb_units, 2)
        result['recommendation'] = f'建议餐时胰岛素 {round(carb_units, 1)} 单位'
    
    return result


def glucose_report(
    readings: List[Tuple[float, GlucoseUnit, datetime]],
    target_range: Tuple[float, float] = (3.9, 10.0),
    unit: GlucoseUnit = GlucoseUnit.MMOL_L
) -> Dict:
    """
    生成血糖报告
    
    Args:
        readings: 血糖读数列表，每个元素为 (值, 单位, 时间) 元组
        target_range: 目标范围 (下限, 上限)，默认 3.9-10.0 mmol/L
        unit: 报告中使用的单位
    
    Returns:
        详细的血糖分析报告
    
    Examples:
        >>> from datetime import datetime, timedelta
        >>> now = datetime.now()
        >>> readings = [(5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=i)) for i in range(10)]
        >>> report = glucose_report(readings)
    """
    if not readings:
        return {'error': '没有血糖读数'}
    
    # 按时间排序
    sorted_readings = sorted(readings, key=lambda x: x[2])
    
    # 转换为统一单位
    values = [r[0] if r[1] == unit else convert_glucose(r[0], r[1], unit) for r in sorted_readings]
    
    n = len(values)
    avg = sum(values) / n
    min_val = min(values)
    max_val = max(values)
    
    # 标准差
    variance = sum((x - avg) ** 2 for x in values) / n
    std_dev = variance ** 0.5
    
    # 变异系数
    cv = (std_dev / avg * 100) if avg > 0 else 0
    
    # 时间范围内
    in_range = sum(1 for v in values if target_range[0] <= v <= target_range[1])
    below_range = sum(1 for v in values if v < target_range[0])
    above_range = sum(1 for v in values if v > target_range[1])
    
    # GVI (Glucose Variability Index) 计算
    # 简化版本：标准差 / 平均值
    gvi = std_dev / avg if avg > 0 else 0
    
    # 估算 HbA1c
    if unit == GlucoseUnit.MMOL_L:
        avg_mmol = avg
    else:
        avg_mmol = convert_glucose(avg, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)
    
    hba1c_est = average_glucose_to_hba1c(avg_mmol, GlucoseUnit.MMOL_L)
    
    # 时间范围
    time_span = (sorted_readings[-1][2] - sorted_readings[0][2]).total_seconds() / 3600
    
    unit_str = unit.value
    
    return {
        'summary': {
            'total_readings': n,
            'time_span_hours': round(time_span, 2),
            'first_reading': sorted_readings[0][2].isoformat(),
            'last_reading': sorted_readings[-1][2].isoformat()
        },
        'statistics': {
            f'average_{unit_str}': round(avg, 2),
            f'min_{unit_str}': round(min_val, 2),
            f'max_{unit_str}': round(max_val, 2),
            f'range_{unit_str}': round(max_val - min_val, 2),
            f'std_dev_{unit_str}': round(std_dev, 2),
            'cv_percent': round(cv, 1)
        },
        'time_in_range': {
            'target_range': f'{target_range[0]}-{target_range[1]} {unit_str}',
            'in_range_percent': round(in_range / n * 100, 1),
            'below_range_percent': round(below_range / n * 100, 1),
            'above_range_percent': round(above_range / n * 100, 1),
            'in_range_count': in_range,
            'below_range_count': below_range,
            'above_range_count': above_range
        },
        'hba1c_estimate': {
            'estimated_hba1c': hba1c_est['hba1c'],
            'status': hba1c_est['status']
        },
        'glucose_variability': {
            'gvi': round(gvi, 3),
            'variability_level': '低' if cv < 36 else '中' if cv < 50 else '高'
        },
        'assessment': {
            'overall': '良好' if cv < 36 and in_range / n > 0.7 else '需改善' if cv < 50 else '需关注',
            'recommendations': _generate_recommendations(avg, cv, in_range / n * 100, unit, target_range)
        }
    }


def _generate_recommendations(avg: float, cv: float, tir: float, 
                              unit: GlucoseUnit, target_range: Tuple[float, float]) -> List[str]:
    """生成个性化建议"""
    recommendations = []
    
    # 根据平均血糖
    if unit == GlucoseUnit.MMOL_L:
        avg_status = assess_glucose(avg, unit, fasting=False)
    else:
        avg_status = assess_glucose(avg, unit, fasting=False)
    
    if avg_status['risk_level'] == 'high':
        recommendations.append('平均血糖偏高，建议咨询医生调整治疗方案')
    elif avg_status['risk_level'] == 'critical':
        recommendations.append('血糖控制不佳，请尽快就医')
    
    # 根据变异性
    if cv >= 50:
        recommendations.append('血糖波动较大，建议规律饮食和用药，避免大幅波动')
    elif cv >= 36:
        recommendations.append('血糖稳定性可进一步提升，建议记录饮食和运动情况')
    
    # 根据目标范围内时间
    if tir < 50:
        recommendations.append('目标范围内时间较低，建议增加血糖监测频率')
    elif tir < 70:
        recommendations.append('目标范围内时间有提升空间，建议分析高低血糖原因')
    else:
        recommendations.append('血糖控制良好，继续保持')
    
    return recommendations if recommendations else ['血糖控制情况良好，继续保持健康生活方式']


# 便捷函数
def mgdl_to_mmol(value: float) -> float:
    """mg/dL 转 mmol/L 的便捷函数"""
    return convert_glucose(value, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)


def mmol_to_mgdl(value: float) -> float:
    """mmol/L 转 mg/dL 的便捷函数"""
    return convert_glucose(value, GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL)


if __name__ == '__main__':
    # 示例用法
    print("=== 血糖工具示例 ===\n")
    
    # 单位转换
    print("1. 单位转换:")
    print(f"  100 mg/dL = {mgdl_to_mmol(100)} mmol/L")
    print(f"  5.5 mmol/L = {mmol_to_mgdl(5.5)} mg/dL")
    
    # 血糖评估
    print("\n2. 血糖评估:")
    result = assess_glucose(6.5, GlucoseUnit.MMOL_L, fasting=True)
    print(f"  空腹血糖 6.5 mmol/L: {result['status']}")
    print(f"  建议: {result['recommendation']}")
    
    # HbA1c 转换
    print("\n3. HbA1c 转换:")
    hba1c_result = hba1c_to_average_glucose(6.5)
    print(f"  HbA1c 6.5% -> 平均血糖: {hba1c_result['avg_glucose_mmol']} mmol/L")
    print(f"  状态: {hba1c_result['status']}")
    
    # 胰岛素计算
    print("\n4. 胰岛素剂量计算:")
    insulin_result = carbohydrate_to_insulin(60, 10, 8.5, 6.0, 2.0)
    print(f"  {insulin_result['recommendation']}")
    
    print("\n=== 示例完成 ===")