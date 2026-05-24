"""
One Rep Max (1RM) Utilities - 单次最大重量计算工具

提供多种科学公式估算单次最大重量（1RM），用于力量训练规划和追踪。

支持的公式：
- Brzycki (最常用)
- Epley
- Lander
- Lombardi
- O'Conner
- Wathan
- Mayhew
- Baechle (Wathan的别名)

零依赖，仅使用Python标准库。
"""

from typing import Dict, List, Optional, Tuple, Callable


# ============================================================
# 核心公式实现
# ============================================================

def brzycki(weight: float, reps: int) -> float:
    """
    Brzycki 公式计算1RM
    
    公式: 1RM = weight × 36 / (37 - reps)
    
    Args:
        weight: 使用的重量（公斤或磅）
        reps: 完成的次数（1-10次推荐）
    
    Returns:
        估算的单次最大重量
    
    Raises:
        ValueError: reps < 1 或 weight <= 0
    
    Example:
        >>> brzycki(100, 5)
        116.12903225806451
    """
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if reps < 1:
        raise ValueError("Reps must be at least 1")
    if reps == 1:
        return weight
    
    return weight * 36 / (37 - reps)


def epley(weight: float, reps: int) -> float:
    """
    Epley 公式计算1RM
    
    公式: 1RM = weight × (1 + reps/30)
    
    Args:
        weight: 使用的重量
        reps: 完成的次数
    
    Returns:
        估算的单次最大重量
    
    Example:
        >>> epley(100, 5)
        116.66666666666667
    """
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if reps < 1:
        raise ValueError("Reps must be at least 1")
    if reps == 1:
        return weight
    
    return weight * (1 + reps / 30)


def lander(weight: float, reps: int) -> float:
    """
    Lander 公式计算1RM
    
    公式: 1RM = 100 × weight / (101.3 - 2.67123 × reps)
    
    Args:
        weight: 使用的重量
        reps: 完成的次数
    
    Returns:
        估算的单次最大重量
    
    Example:
        >>> lander(100, 5)
        115.95887611749581
    """
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if reps < 1:
        raise ValueError("Reps must be at least 1")
    if reps == 1:
        return weight
    
    return 100 * weight / (101.3 - 2.67123 * reps)


def lombardi(weight: float, reps: int) -> float:
    """
    Lombardi 公式计算1RM
    
    公式: 1RM = weight × reps^0.10
    
    Args:
        weight: 使用的重量
        reps: 完成的次数
    
    Returns:
        估算的单次最大重量
    
    Example:
        >>> lombardi(100, 5)
        117.46189817169163
    """
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if reps < 1:
        raise ValueError("Reps must be at least 1")
    if reps == 1:
        return weight
    
    return weight * (reps ** 0.10)


def oconner(weight: float, reps: int) -> float:
    """
    O'Conner 公式计算1RM
    
    公式: 1RM = weight × (1 + reps/40)
    
    Args:
        weight: 使用的重量
        reps: 完成的次数
    
    Returns:
        估算的单次最大重量
    
    Example:
        >>> oconner(100, 5)
        112.5
    """
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if reps < 1:
        raise ValueError("Reps must be at least 1")
    if reps == 1:
        return weight
    
    return weight * (1 + reps / 40)


def wathan(weight: float, reps: int) -> float:
    """
    Wathan 公式计算1RM
    
    公式: 1RM = 100 × weight / (48.8 + 53.8 × e^(-0.075 × reps))
    
    Args:
        weight: 使用的重量
        reps: 完成的次数
    
    Returns:
        估算的单次最大重量
    
    Example:
        >>> round(wathan(100, 5), 2)
        116.34
    """
    import math
    
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if reps < 1:
        raise ValueError("Reps must be at least 1")
    if reps == 1:
        return weight
    
    return 100 * weight / (48.8 + 53.8 * math.exp(-0.075 * reps))


def mayhew(weight: float, reps: int) -> float:
    """
    Mayhew 公式计算1RM
    
    公式: 1RM = 100 × weight / (52.2 + 41.9 × e^(-0.055 × reps))
    
    Args:
        weight: 使用的重量
        reps: 完成的次数
    
    Returns:
        估算的单次最大重量
    
    Example:
        >>> round(mayhew(100, 5), 2)
        115.55
    """
    import math
    
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if reps < 1:
        raise ValueError("Reps must be at least 1")
    if reps == 1:
        return weight
    
    return 100 * weight / (52.2 + 41.9 * math.exp(-0.055 * reps))


def baechle(weight: float, reps: int) -> float:
    """
    Baechle 公式（Wathan公式的别名）
    
    Args:
        weight: 使用的重量
        reps: 完成的次数
    
    Returns:
        估算的单次最大重量
    """
    return wathan(weight, reps)


# 公式注册表
FORMULAS: Dict[str, Callable[[float, int], float]] = {
    'brzycki': brzycki,
    'epley': epley,
    'lander': lander,
    'lombardi': lombardi,
    'oconner': oconner,
    'wathan': wathan,
    'mayhew': mayhew,
    'baechle': baechle,
}


# ============================================================
# 综合计算函数
# ============================================================

def calculate_1rm(weight: float, reps: int, formula: str = 'brzycki') -> float:
    """
    使用指定公式计算1RM
    
    Args:
        weight: 使用的重量
        reps: 完成的次数
        formula: 使用的公式名称，支持：
                 - 'brzycki' (默认)
                 - 'epley'
                 - 'lander'
                 - 'lombardi'
                 - 'oconner'
                 - 'wathan'
                 - 'mayhew'
                 - 'baechle'
    
    Returns:
        估算的单次最大重量
    
    Raises:
        ValueError: 无效的公式名称或参数
    
    Example:
        >>> calculate_1rm(100, 5, 'epley')
        116.66666666666667
    """
    formula = formula.lower()
    if formula not in FORMULAS:
        available = ', '.join(FORMULAS.keys())
        raise ValueError(f"Unknown formula '{formula}'. Available: {available}")
    
    return FORMULAS[formula](weight, reps)


def calculate_all_formulas(weight: float, reps: int) -> Dict[str, float]:
    """
    使用所有公式计算1RM，返回对比结果
    
    Args:
        weight: 使用的重量
        reps: 完成的次数
    
    Returns:
        各公式计算的1RM结果字典
    
    Example:
        >>> results = calculate_all_formulas(100, 5)
        >>> round(results['brzycki'], 2)
        116.13
    """
    return {name: func(weight, reps) for name, func in FORMULAS.items()}


def average_1rm(weight: float, reps: int, 
                formulas: Optional[List[str]] = None) -> float:
    """
    计算多个公式结果的平均值
    
    Args:
        weight: 使用的重量
        reps: 完成的次数
        formulas: 要使用的公式列表，默认使用全部
    
    Returns:
        平均1RM值
    
    Example:
        >>> round(average_1rm(100, 5), 2)
        116.17
    """
    if formulas is None:
        results = calculate_all_formulas(weight, reps)
    else:
        results = {f: calculate_1rm(weight, reps, f) for f in formulas}
    
    return sum(results.values()) / len(results)


# ============================================================
# 反向计算：根据目标1RM计算训练重量
# ============================================================

def calculate_weight_for_reps(one_rm: float, reps: int, 
                              formula: str = 'brzycki') -> float:
    """
    根据目标1RM和目标次数，计算应使用的训练重量
    
    Args:
        one_rm: 单次最大重量
        reps: 目标次数
        formula: 使用的公式
    
    Returns:
        建议使用的训练重量
    
    Example:
        >>> round(calculate_weight_for_reps(120, 5), 2)
        103.23
    """
    # 使用Brzycki反推: weight = 1RM × (37 - reps) / 36
    if formula.lower() == 'brzycki':
        if reps == 1:
            return one_rm
        return one_rm * (37 - reps) / 36
    
    # 使用Epley反推: weight = 1RM / (1 + reps/30)
    elif formula.lower() == 'epley':
        if reps == 1:
            return one_rm
        return one_rm / (1 + reps / 30)
    
    # 其他公式使用数值逼近
    else:
        # 二分查找
        low, high = 0, one_rm
        target = one_rm
        
        for _ in range(50):  # 足够精确
            mid = (low + high) / 2
            estimated = calculate_1rm(mid, reps, formula)
            if estimated < target:
                low = mid
            else:
                high = mid
        
        return (low + high) / 2


def calculate_percentage_weight(one_rm: float, percentage: float) -> float:
    """
    根据1RM百分比计算训练重量
    
    Args:
        one_rm: 单次最大重量
        percentage: 百分比（如80表示80%）
    
    Returns:
        训练重量
    
    Example:
        >>> calculate_percentage_weight(100, 80)
        80.0
    """
    return one_rm * percentage / 100


# ============================================================
# 训练计划生成
# ============================================================

def generate_rep_max_table(one_rm: float, 
                           formula: str = 'brzycki',
                           max_reps: int = 12) -> Dict[int, float]:
    """
    生成多次最大重量表（nRM表）
    
    Args:
        one_rm: 单次最大重量
        formula: 使用的公式
        max_reps: 最大次数（默认12）
    
    Returns:
        次数到重量的映射表
    
    Example:
        >>> table = generate_rep_max_table(100)
        >>> round(table[5], 2)
        86.05
    """
    table = {1: one_rm}
    for reps in range(2, max_reps + 1):
        table[reps] = calculate_weight_for_reps(one_rm, reps, formula)
    return table


def generate_percentage_table(one_rm: float, 
                              percentages: Optional[List[int]] = None) -> Dict[int, float]:
    """
    生成百分比重量表
    
    Args:
        one_rm: 单次最大重量
        percentages: 百分比列表，默认[95, 90, 85, 80, 75, 70, 65, 60, 55, 50]
    
    Returns:
        百分比到重量的映射表
    
    Example:
        >>> table = generate_percentage_table(100)
        >>> table[80]
        80.0
    """
    if percentages is None:
        percentages = [95, 90, 85, 80, 75, 70, 65, 60, 55, 50]
    
    return {p: calculate_percentage_weight(one_rm, p) for p in percentages}


def estimate_reps_at_weight(one_rm: float, weight: float, 
                            formula: str = 'brzycki') -> int:
    """
    根据重量估算可以完成的次数
    
    Args:
        one_rm: 单次最大重量
        weight: 目标重量
        formula: 使用的公式
    
    Returns:
        估算可完成的次数
    
    Example:
        >>> estimate_reps_at_weight(100, 80)
        8
    """
    if weight >= one_rm:
        return 1
    if weight <= 0:
        return 0
    
    # 逆向计算
    for reps in range(2, 30):
        est_weight = calculate_weight_for_reps(one_rm, reps, formula)
        if est_weight <= weight:
            return reps
    
    return 30


# ============================================================
# 进度追踪与比较
# ============================================================

def calculate_strength_level(one_rm: float, bodyweight: float,
                            gender: str = 'male',
                            exercise: str = 'bench_press') -> str:
    """
    根据力量体重比评估力量等级
    
    Args:
        one_rm: 单次最大重量（公斤）
        bodyweight: 体重（公斤）
        gender: 性别（'male' 或 'female'）
        exercise: 动作类型
    
    Returns:
        力量等级描述
    
    Example:
        >>> calculate_strength_level(100, 80, 'male', 'bench_press')
        'Intermediate'
    """
    ratio = one_rm / bodyweight
    
    # 不同动作的力量标准（基于力量体重比）
    standards = {
        'bench_press': {
            'male': [(1.5, 'Elite'), (1.2, 'Advanced'), (1.0, 'Intermediate'), 
                    (0.75, 'Novice'), (0, 'Beginner')],
            'female': [(1.0, 'Elite'), (0.8, 'Advanced'), (0.6, 'Intermediate'), 
                      (0.4, 'Novice'), (0, 'Beginner')]
        },
        'squat': {
            'male': [(2.0, 'Elite'), (1.7, 'Advanced'), (1.4, 'Intermediate'), 
                    (1.0, 'Novice'), (0, 'Beginner')],
            'female': [(1.5, 'Elite'), (1.2, 'Advanced'), (1.0, 'Intermediate'), 
                      (0.7, 'Novice'), (0, 'Beginner')]
        },
        'deadlift': {
            'male': [(2.5, 'Elite'), (2.0, 'Advanced'), (1.7, 'Intermediate'), 
                    (1.2, 'Novice'), (0, 'Beginner')],
            'female': [(1.8, 'Elite'), (1.4, 'Advanced'), (1.1, 'Intermediate'), 
                      (0.8, 'Novice'), (0, 'Beginner')]
        },
        'overhead_press': {
            'male': [(1.0, 'Elite'), (0.85, 'Advanced'), (0.7, 'Intermediate'), 
                    (0.5, 'Novice'), (0, 'Beginner')],
            'female': [(0.65, 'Elite'), (0.5, 'Advanced'), (0.4, 'Intermediate'), 
                      (0.3, 'Novice'), (0, 'Beginner')]
        }
    }
    
    if exercise not in standards:
        exercise = 'bench_press'
    
    gender_standards = standards[exercise].get(gender, standards[exercise]['male'])
    
    for threshold, level in gender_standards:
        if ratio >= threshold:
            return level
    
    return 'Beginner'


def calculate_wilks_score(one_rm: float, bodyweight: float, 
                         gender: str = 'male', 
                         unit: str = 'kg') -> float:
    """
    计算Wilks得分（力量举标准化得分）
    
    使用2020版Wilks公式系数。
    
    Args:
        one_rm: 单次最大重量
        bodyweight: 体重
        gender: 性别
        unit: 单位（'kg' 或 'lb'）
    
    Returns:
        Wilks得分
    
    Example:
        >>> round(calculate_wilks_score(150, 75, 'male'), 2)
        108.52
    """
    import math
    
    # 转换为公斤
    if unit == 'lb':
        bodyweight = bodyweight * 0.453592
        one_rm = one_rm * 0.453592
    
    # Wilks 2020 公式系数
    # Coefficient = 500 / (a + b*x + c*x^2 + d*x^3 + e*x^4 + f*x^5)
    x = bodyweight
    
    if gender.lower() == 'male':
        a = -216.0475144
        b = 16.2606339
        c = -0.002388645
        d = -0.00113732
        e = 7.01863e-05
        f = -1.291e-08
    else:
        a = 594.31747775582
        b = -27.238415364474
        c = 0.82112226871
        d = -0.00930733913
        e = 4.731582e-05
        f = -9.054e-08
    
    denominator = a + b*x + c*x**2 + d*x**3 + e*x**4 + f*x**5
    coefficient = 500 / denominator
    
    return one_rm * coefficient


def compare_1rm(old_1rm: float, new_1rm: float) -> Dict[str, float]:
    """
    比较两次1RM的变化
    
    Args:
        old_1rm: 旧的1RM
        new_1rm: 新的1RM
    
    Returns:
        包含变化量和百分比的字典
    
    Example:
        >>> compare_1rm(100, 110)
        {'change': 10.0, 'percentage': 10.0, 'is_improvement': True}
    """
    change = new_1rm - old_1rm
    percentage = (change / old_1rm * 100) if old_1rm != 0 else 0
    
    return {
        'change': change,
        'percentage': percentage,
        'is_improvement': change > 0
    }


# ============================================================
# 辅助功能
# ============================================================

def round_to_plate(weight: float, plate_sizes: Optional[List[float]] = None,
                  unit: str = 'kg') -> float:
    """
    将重量四舍五入到可用的杠铃片组合
    
    Args:
        weight: 目标重量
        plate_sizes: 可用杠铃片大小列表
        unit: 单位（'kg' 或 'lb'）
    
    Returns:
        调整后的重量
    
    Example:
        >>> round_to_plate(87.5)
        87.5
    """
    if plate_sizes is None:
        if unit == 'kg':
            plate_sizes = [1.25, 2.5, 5, 10, 15, 20, 25]
        else:
            plate_sizes = [2.5, 5, 10, 25, 35, 45, 55]
    
    # 杠铃片是成对的，所以最小增量是最小板的两倍
    min_increment = min(plate_sizes) * 2
    
    # 四舍五入到最近的最小增量
    rounded = round(weight / min_increment) * min_increment
    
    return rounded


def suggest_warmup_weights(one_rm: float, working_weight: float,
                          unit: str = 'kg') -> List[Tuple[float, int]]:
    """
    建议热身组重量和次数
    
    Args:
        one_rm: 单次最大重量
        working_weight: 工作组重量
        unit: 单位
    
    Returns:
        热身组列表，每项为(重量, 次数)
    
    Example:
        >>> suggest_warmup_weights(100, 80)
        [(50.0, 10), (60.0, 5), (70.0, 3), (80.0, 1)]
    """
    warmup_percentages = [50, 60, 70, 80]
    warmup_reps = [10, 5, 3, 1]
    
    warmup_sets = []
    for pct, reps in zip(warmup_percentages, warmup_reps):
        weight = round_to_plate(one_rm * pct / 100, unit=unit)
        if weight < working_weight:
            warmup_sets.append((weight, reps))
    
    return warmup_sets


def validate_input(weight: float, reps: int) -> Tuple[bool, str]:
    """
    验证输入参数
    
    Args:
        weight: 重量
        reps: 次数
    
    Returns:
        (是否有效, 错误信息)
    
    Example:
        >>> validate_input(100, 5)
        (True, '')
        >>> validate_input(-10, 5)
        (False, 'Weight must be positive')
    """
    if weight <= 0:
        return False, 'Weight must be positive'
    if reps < 1:
        return False, 'Reps must be at least 1'
    if reps > 30:
        return False, 'Reps should be <= 30 for accurate estimation'
    return True, ''


def get_available_formulas() -> List[str]:
    """
    获取所有可用公式名称
    
    Returns:
        公式名称列表
    
    Example:
        >>> get_available_formulas()
        ['brzycki', 'epley', 'lander', 'lombardi', 'oconner', 'wathan', 'mayhew', 'baechle']
    """
    return list(FORMULAS.keys())


def get_formula_description(formula: str) -> str:
    """
    获取公式描述
    
    Args:
        formula: 公式名称
    
    Returns:
        公式描述
    
    Example:
        >>> get_formula_description('brzycki')
        'Brzycki公式 - 最常用的1RM估算公式，适用于1-10次'
    """
    descriptions = {
        'brzycki': 'Brzycki公式 - 最常用的1RM估算公式，适用于1-10次',
        'epley': 'Epley公式 - 适合高次数估算（最多10次）',
        'lander': 'Lander公式 - 与Brzycki类似，略有不同的精确度',
        'lombardi': 'Lombardi公式 - 使用幂函数，适合各种次数',
        'oconner': "O'Conner公式 - 简单线性公式，适合快速估算",
        'wathan': 'Wathan公式 - 考虑指数衰减，较为精确',
        'mayhew': 'Mayhew公式 - 类似Wathan，适合不同经验水平',
        'baechle': 'Baechle公式 - Wathan公式的别名'
    }
    return descriptions.get(formula.lower(), 'Unknown formula')


# ============================================================
# 便捷类
# ============================================================

class OneRepMaxCalculator:
    """
    1RM计算器类
    
    提供面向对象的接口进行1RM计算
    
    Example:
        >>> calc = OneRepMaxCalculator(formula='brzycki')
        >>> calc.calculate(100, 5)
        116.12903225806451
        >>> calc.generate_table(100)
        {1: 100.0, 2: 97.22..., 3: 94.59..., ...}
    """
    
    def __init__(self, formula: str = 'brzycki'):
        """
        初始化计算器
        
        Args:
            formula: 默认使用的公式
        """
        formula = formula.lower()
        if formula not in FORMULAS:
            raise ValueError(f"Unknown formula '{formula}'. "
                           f"Available: {', '.join(FORMULAS.keys())}")
        self.formula = formula
    
    def calculate(self, weight: float, reps: int) -> float:
        """计算1RM"""
        return calculate_1rm(weight, reps, self.formula)
    
    def calculate_all(self, weight: float, reps: int) -> Dict[str, float]:
        """使用所有公式计算"""
        return calculate_all_formulas(weight, reps)
    
    def calculate_average(self, weight: float, reps: int,
                         formulas: Optional[List[str]] = None) -> float:
        """计算平均1RM"""
        return average_1rm(weight, reps, formulas)
    
    def calculate_weight_for_reps(self, one_rm: float, reps: int) -> float:
        """计算指定次数的训练重量"""
        return calculate_weight_for_reps(one_rm, reps, self.formula)
    
    def generate_table(self, one_rm: float, max_reps: int = 12) -> Dict[int, float]:
        """生成nRM表"""
        return generate_rep_max_table(one_rm, self.formula, max_reps)
    
    def estimate_reps(self, one_rm: float, weight: float) -> int:
        """估算可完成次数"""
        return estimate_reps_at_weight(one_rm, weight, self.formula)
    
    def suggest_warmup(self, one_rm: float, working_weight: float,
                       unit: str = 'kg') -> List[Tuple[float, int]]:
        """建议热身组"""
        return suggest_warmup_weights(one_rm, working_weight, unit)
    
    def compare(self, old_1rm: float, new_1rm: float) -> Dict[str, float]:
        """比较进步"""
        return compare_1rm(old_1rm, new_1rm)


# 导出的公共API
__all__ = [
    # 核心公式
    'brzycki',
    'epley',
    'lander',
    'lombardi',
    'oconner',
    'wathan',
    'mayhew',
    'baechle',
    # 综合计算
    'calculate_1rm',
    'calculate_all_formulas',
    'average_1rm',
    # 反向计算
    'calculate_weight_for_reps',
    'calculate_percentage_weight',
    # 训练计划
    'generate_rep_max_table',
    'generate_percentage_table',
    'estimate_reps_at_weight',
    # 进度追踪
    'calculate_strength_level',
    'calculate_wilks_score',
    'compare_1rm',
    # 辅助功能
    'round_to_plate',
    'suggest_warmup_weights',
    'validate_input',
    'get_available_formulas',
    'get_formula_description',
    # 类
    'OneRepMaxCalculator',
    # 常量
    'FORMULAS',
]