"""
probability_utils - 概率与统计计算工具集

提供常见的概率分布计算、组合数学、统计函数等功能。
零外部依赖，纯 Python 标准库实现。

核心功能：
- 概率分布：正态分布、泊松分布、二项分布、指数分布、几何分布
- 组合数学：排列、组合、阶乘
- 统计函数：均值、方差、标准差、协方差、相关系数
- 概率计算：条件概率、贝叶斯定理
- 随机采样：加权随机选择、拒绝采样
"""

import math
import random
from typing import List, Tuple, Optional, Dict, Any, Callable
from functools import lru_cache
from decimal import Decimal, getcontext

# 设置高精度计算上下文
getcontext().prec = 50


# ============================================================
# 基础数学函数
# ============================================================

@lru_cache(maxsize=1000)
def factorial(n: int) -> int:
    """
    计算阶乘 n!
    
    Args:
        n: 非负整数
        
    Returns:
        n 的阶乘
        
    Raises:
        ValueError: n 为负数
    """
    if n < 0:
        raise ValueError("阶乘不支持负数")
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@lru_cache(maxsize=1000)
def permutation(n: int, k: int) -> int:
    """
    计算排列数 P(n, k) = n! / (n-k)!
    
    从 n 个不同元素中取出 k 个进行排列的方法数。
    
    Args:
        n: 总元素数
        k: 选取元素数
        
    Returns:
        排列数
        
    Raises:
        ValueError: 参数无效
    """
    if n < 0 or k < 0:
        raise ValueError("参数必须为非负整数")
    if k > n:
        return 0
    return factorial(n) // factorial(n - k)


@lru_cache(maxsize=1000)
def combination(n: int, k: int) -> int:
    """
    计算组合数 C(n, k) = n! / (k! * (n-k)!)
    
    从 n 个不同元素中取出 k 个的组合方法数。
    
    Args:
        n: 总元素数
        k: 选取元素数
        
    Returns:
        组合数
        
    Raises:
        ValueError: 参数无效
    """
    if n < 0 or k < 0:
        raise ValueError("参数必须为非负整数")
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1
    # 使用对称性优化
    if k > n - k:
        k = n - k
    return factorial(n) // (factorial(k) * factorial(n - k))


def gcd(a: int, b: int) -> int:
    """
    计算最大公约数
    
    Args:
        a, b: 两个整数
        
    Returns:
        最大公约数
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """
    计算最小公倍数
    
    Args:
        a, b: 两个整数
        
    Returns:
        最小公倍数
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


# ============================================================
# 统计函数
# ============================================================

def mean(data: List[float]) -> float:
    """
    计算算术平均值
    
    Args:
        data: 数据列表
        
    Returns:
        平均值
        
    Raises:
        ValueError: 数据为空
    """
    if not data:
        raise ValueError("数据不能为空")
    return sum(data) / len(data)


def median(data: List[float]) -> float:
    """
    计算中位数
    
    Args:
        data: 数据列表
        
    Returns:
        中位数
    """
    if not data:
        raise ValueError("数据不能为空")
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]


def mode(data: List[float]) -> List[float]:
    """
    计算众数（出现频率最高的值）
    
    Args:
        data: 数据列表
        
    Returns:
        众数列表（可能有多个）
    """
    if not data:
        raise ValueError("数据不能为空")
    counts = {}
    for x in data:
        counts[x] = counts.get(x, 0) + 1
    max_count = max(counts.values())
    return sorted([k for k, v in counts.items() if v == max_count])


def variance(data: List[float], population: bool = True) -> float:
    """
    计算方差
    
    Args:
        data: 数据列表
        population: True 为总体方差，False 为样本方差
        
    Returns:
        方差值
    """
    if not data:
        raise ValueError("数据不能为空")
    m = mean(data)
    n = len(data)
    divisor = n if population else n - 1
    return sum((x - m) ** 2 for x in data) / divisor


def std_dev(data: List[float], population: bool = True) -> float:
    """
    计算标准差
    
    Args:
        data: 数据列表
        population: True 为总体标准差，False 为样本标准差
        
    Returns:
        标准差
    """
    return math.sqrt(variance(data, population))


def covariance(x: List[float], y: List[float], population: bool = True) -> float:
    """
    计算协方差
    
    Args:
        x, y: 两个数据列表
        population: True 为总体协方差，False 为样本协方差
        
    Returns:
        协方差
    """
    if len(x) != len(y):
        raise ValueError("两个数据列表长度必须相同")
    if not x:
        raise ValueError("数据不能为空")
    n = len(x)
    mx, my = mean(x), mean(y)
    divisor = n if population else n - 1
    return sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / divisor


def correlation(x: List[float], y: List[float]) -> float:
    """
    计算皮尔逊相关系数
    
    Args:
        x, y: 两个数据列表
        
    Returns:
        相关系数 (-1 到 1)
    """
    if len(x) != len(y):
        raise ValueError("两个数据列表长度必须相同")
    cov = covariance(x, y)
    std_x = std_dev(x)
    std_y = std_dev(y)
    if std_x == 0 or std_y == 0:
        return 0.0
    return cov / (std_x * std_y)


def percentile(data: List[float], p: float) -> float:
    """
    计算百分位数
    
    Args:
        data: 数据列表
        p: 百分位 (0-100)
        
    Returns:
        百分位数值
    """
    if not data:
        raise ValueError("数据不能为空")
    if not 0 <= p <= 100:
        raise ValueError("百分位必须在 0-100 之间")
    sorted_data = sorted(data)
    n = len(sorted_data)
    if p == 0:
        return sorted_data[0]
    if p == 100:
        return sorted_data[-1]
    # 线性插值
    k = (n - 1) * p / 100
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    return sorted_data[int(f)] * (c - k) + sorted_data[int(c)] * (k - f)


def quartiles(data: List[float]) -> Tuple[float, float, float]:
    """
    计算四分位数
    
    Args:
        data: 数据列表
        
    Returns:
        (Q1, Q2, Q3) 第一四分位、中位数、第三四分位
    """
    return (
        percentile(data, 25),
        percentile(data, 50),
        percentile(data, 75)
    )


def iqr(data: List[float]) -> float:
    """
    计算四分位距 (Interquartile Range)
    
    Args:
        data: 数据列表
        
    Returns:
        IQR = Q3 - Q1
    """
    q1, _, q3 = quartiles(data)
    return q3 - q1


def skewness(data: List[float]) -> float:
    """
    计算偏度（衡量分布的不对称性）
    
    Args:
        data: 数据列表
        
    Returns:
        偏度值
    """
    if not data:
        raise ValueError("数据不能为空")
    n = len(data)
    m = mean(data)
    s = std_dev(data, population=False)
    if s == 0:
        return 0.0
    return (n / ((n - 1) * (n - 2))) * sum(((x - m) / s) ** 3 for x in data)


def kurtosis(data: List[float]) -> float:
    """
    计算峰度（衡量分布的尖锐程度）
    
    Args:
        data: 数据列表
        
    Returns:
        峰度值（正态分布为0）
    """
    if not data:
        raise ValueError("数据不能为空")
    n = len(data)
    m = mean(data)
    s = std_dev(data, population=False)
    if s == 0:
        return 0.0
    return (
        (n * (n + 1) / ((n - 1) * (n - 2) * (n - 3))) *
        sum(((x - m) / s) ** 4 for x in data) -
        3 * (n - 1) ** 2 / ((n - 2) * (n - 3))
    )


# ============================================================
# 概率分布函数
# ============================================================

def normal_pdf(x: float, mu: float = 0, sigma: float = 1) -> float:
    """
    正态分布概率密度函数
    
    Args:
        x: 变量值
        mu: 均值
        sigma: 标准差
        
    Returns:
        概率密度值
    """
    if sigma <= 0:
        raise ValueError("标准差必须为正数")
    return (1 / (sigma * math.sqrt(2 * math.pi))) * \
           math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


def normal_cdf(x: float, mu: float = 0, sigma: float = 1) -> float:
    """
    正态分布累积分布函数
    
    使用误差函数近似计算
    
    Args:
        x: 变量值
        mu: 均值
        sigma: 标准差
        
    Returns:
        累积概率
    """
    if sigma <= 0:
        raise ValueError("标准差必须为正数")
    z = (x - mu) / (sigma * math.sqrt(2))
    return 0.5 * (1 + math.erf(z))


def normal_inv(p: float, mu: float = 0, sigma: float = 1) -> float:
    """
    正态分布逆累积分布函数（分位数函数）
    
    使用有理近似计算
    
    Args:
        p: 概率 (0-1)
        mu: 均值
        sigma: 标准差
        
    Returns:
        分位数
    """
    if not 0 < p < 1:
        raise ValueError("概率必须在 0-1 之间")
    if sigma <= 0:
        raise ValueError("标准差必须为正数")
    
    # Beasley-Springer-Moro 算法
    a = [
        -3.969683028665376e+01,
        2.209460984245205e+02,
        -2.759285104469687e+02,
        1.383577518672690e+02,
        -3.066479806614716e+01,
        2.506628277459239e+00
    ]
    b = [
        -5.447609879822406e+01,
        1.615858368580409e+02,
        -1.556989798598866e+02,
        6.680131188771972e+01,
        -1.328068155288572e+01
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e+00,
        -2.549732539343734e+00,
        4.374664141464968e+00,
        2.938163982698783e+00
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e+00,
        3.754408661907416e+00
    ]
    
    p_low = 0.02425
    p_high = 1 - p_low
    
    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        z = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        z = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
            (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        z = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    
    return mu + sigma * z


def binomial_pmf(k: int, n: int, p: float) -> float:
    """
    二项分布概率质量函数
    
    P(X = k) = C(n, k) * p^k * (1-p)^(n-k)
    
    Args:
        k: 成功次数
        n: 试验次数
        p: 成功概率
        
    Returns:
        概率值
    """
    if not 0 <= p <= 1:
        raise ValueError("概率必须在 0-1 之间")
    if k < 0 or k > n:
        return 0.0
    return combination(n, k) * (p ** k) * ((1 - p) ** (n - k))


def binomial_cdf(k: int, n: int, p: float) -> float:
    """
    二项分布累积分布函数
    
    P(X <= k)
    
    Args:
        k: 成功次数上限
        n: 试验次数
        p: 成功概率
        
    Returns:
        累积概率
    """
    return sum(binomial_pmf(i, n, p) for i in range(k + 1))


def poisson_pmf(k: int, lam: float) -> float:
    """
    泊松分布概率质量函数
    
    P(X = k) = (λ^k * e^-λ) / k!
    
    Args:
        k: 事件发生次数
        lam: 期望值 λ
        
    Returns:
        概率值
    """
    if lam < 0:
        raise ValueError("λ 必须为非负数")
    if k < 0:
        return 0.0
    return (lam ** k) * math.exp(-lam) / factorial(k)


def poisson_cdf(k: int, lam: float) -> float:
    """
    泊松分布累积分布函数
    
    Args:
        k: 事件发生次数上限
        lam: 期望值 λ
        
    Returns:
        累积概率
    """
    return sum(poisson_pmf(i, lam) for i in range(k + 1))


def exponential_pdf(x: float, lam: float = 1.0) -> float:
    """
    指数分布概率密度函数
    
    f(x) = λ * e^(-λx) for x >= 0
    
    Args:
        x: 变量值
        lam: 率参数 λ
        
    Returns:
        概率密度值
    """
    if lam <= 0:
        raise ValueError("λ 必须为正数")
    if x < 0:
        return 0.0
    return lam * math.exp(-lam * x)


def exponential_cdf(x: float, lam: float = 1.0) -> float:
    """
    指数分布累积分布函数
    
    F(x) = 1 - e^(-λx) for x >= 0
    
    Args:
        x: 变量值
        lam: 率参数 λ
        
    Returns:
        累积概率
    """
    if lam <= 0:
        raise ValueError("λ 必须为正数")
    if x < 0:
        return 0.0
    return 1 - math.exp(-lam * x)


def geometric_pmf(k: int, p: float) -> float:
    """
    几何分布概率质量函数
    
    P(X = k) = (1-p)^(k-1) * p
    
    表示第一次成功发生在第 k 次试验的概率
    
    Args:
        k: 试验次数
        p: 成功概率
        
    Returns:
        概率值
    """
    if not 0 < p <= 1:
        raise ValueError("概率必须在 (0, 1] 之间")
    if k < 1:
        return 0.0
    return ((1 - p) ** (k - 1)) * p


def geometric_cdf(k: int, p: float) -> float:
    """
    几何分布累积分布函数
    
    P(X <= k) = 1 - (1-p)^k
    
    Args:
        k: 试验次数上限
        p: 成功概率
        
    Returns:
        累积概率
    """
    if not 0 < p <= 1:
        raise ValueError("概率必须在 (0, 1] 之间")
    if k < 1:
        return 0.0
    return 1 - (1 - p) ** k


def hypergeometric_pmf(k: int, N: int, K: int, n: int) -> float:
    """
    超几何分布概率质量函数
    
    从 N 个物品中（其中 K 个为"成功"）无放回抽取 n 个，
    恰好有 k 个成功的概率。
    
    P(X = k) = C(K, k) * C(N-K, n-k) / C(N, n)
    
    Args:
        k: 成功数量
        N: 总物品数
        K: 成功物品数
        n: 抽取数量
        
    Returns:
        概率值
    """
    if k < 0 or k > min(K, n):
        return 0.0
    if n - k > N - K:
        return 0.0
    return combination(K, k) * combination(N - K, n - k) / combination(N, n)


def negative_binomial_pmf(k: int, r: int, p: float) -> float:
    """
    负二项分布概率质量函数
    
    第 r 次成功发生在第 k 次试验的概率
    
    P(X = k) = C(k-1, r-1) * p^r * (1-p)^(k-r)
    
    Args:
        k: 总试验次数
        r: 成功次数
        p: 成功概率
        
    Returns:
        概率值
    """
    if not 0 < p <= 1:
        raise ValueError("概率必须在 (0, 1] 之间")
    if k < r:
        return 0.0
    return combination(k - 1, r - 1) * (p ** r) * ((1 - p) ** (k - r))


# ============================================================
# 贝叶斯与条件概率
# ============================================================

def conditional_probability(p_a_and_b: float, p_b: float) -> float:
    """
    条件概率 P(A|B) = P(A∩B) / P(B)
    
    Args:
        p_a_and_b: A 和 B 同时发生的概率
        p_b: B 发生的概率
        
    Returns:
        条件概率 P(A|B)
    """
    if p_b == 0:
        raise ValueError("P(B) 不能为 0")
    return p_a_and_b / p_b


def bayes_theorem(p_b_given_a: float, p_a: float, p_b: float) -> float:
    """
    贝叶斯定理
    
    P(A|B) = P(B|A) * P(A) / P(B)
    
    Args:
        p_b_given_a: P(B|A) - 在 A 发生条件下 B 发生的概率
        p_a: P(A) - A 的先验概率
        p_b: P(B) - B 的边际概率
        
    Returns:
        P(A|B) - 后验概率
    """
    if p_b == 0:
        raise ValueError("P(B) 不能为 0")
    return (p_b_given_a * p_a) / p_b


def bayes_theorem_multiple(
    p_b_given_a: float,
    p_a: float,
    hypotheses: List[Tuple[float, float]]
) -> float:
    """
    多假设贝叶斯定理
    
    P(A|B) = P(B|A) * P(A) / Σ P(B|Hi) * P(Hi)
    
    Args:
        p_b_given_a: P(B|A)
        p_a: P(A)
        hypotheses: [(P(B|H1), P(H1)), (P(B|H2), P(H2)), ...]
        
    Returns:
        后验概率
    """
    marginal = sum(p_bh * p_h for p_bh, p_h in hypotheses)
    if marginal == 0:
        raise ValueError("边际概率为 0")
    return (p_b_given_a * p_a) / marginal


# ============================================================
# 随机采样工具
# ============================================================

def weighted_choice(items: List[Any], weights: List[float]) -> Any:
    """
    加权随机选择
    
    Args:
        items: 选项列表
        weights: 权重列表
        
    Returns:
        随机选中的项目
    """
    if len(items) != len(weights):
        raise ValueError("选项和权重列表长度必须相同")
    if not items:
        raise ValueError("选项列表不能为空")
    
    total = sum(weights)
    if total <= 0:
        raise ValueError("权重总和必须为正数")
    
    r = random.random() * total
    cumulative = 0
    for item, weight in zip(items, weights):
        cumulative += weight
        if r <= cumulative:
            return item
    return items[-1]


def sample_without_replacement(
    population: List[Any],
    k: int,
    weights: Optional[List[float]] = None
) -> List[Any]:
    """
    无放回抽样
    
    Args:
        population: 总体
        k: 样本数量
        weights: 可选权重
        
    Returns:
        样本列表
    """
    if k > len(population):
        raise ValueError("样本数量不能超过总体大小")
    
    if weights is None:
        return random.sample(population, k)
    
    # 加权无放回抽样
    result = []
    remaining = list(zip(population, weights))
    for _ in range(k):
        total = sum(w for _, w in remaining)
        r = random.random() * total
        cumulative = 0
        for i, (item, weight) in enumerate(remaining):
            cumulative += weight
            if r <= cumulative:
                result.append(item)
                remaining.pop(i)
                break
    return result


def rejection_sampling(
    pdf: Callable[[float], float],
    x_min: float,
    x_max: float,
    y_max: float,
    n_samples: int = 1
) -> List[float]:
    """
    拒绝采样法
    
    Args:
        pdf: 概率密度函数
        x_min, x_max: x 范围
        y_max: y 最大值（需要 >= pdf 的最大值）
        n_samples: 样本数量
        
    Returns:
        样本列表
    """
    samples = []
    while len(samples) < n_samples:
        x = random.uniform(x_min, x_max)
        y = random.uniform(0, y_max)
        if y <= pdf(x):
            samples.append(x)
    return samples


# ============================================================
# 统计检验
# ============================================================

def z_score(x: float, mu: float, sigma: float) -> float:
    """
    计算 Z 分数（标准分数）
    
    Args:
        x: 观测值
        mu: 总体均值
        sigma: 总体标准差
        
    Returns:
        Z 分数
    """
    if sigma <= 0:
        raise ValueError("标准差必须为正数")
    return (x - mu) / sigma


def z_test(
    sample_mean: float,
    population_mean: float,
    population_std: float,
    sample_size: int,
    two_tailed: bool = True
) -> Tuple[float, float]:
    """
    Z 检验
    
    Args:
        sample_mean: 样本均值
        population_mean: 总体均值
        population_std: 总体标准差
        sample_size: 样本大小
        two_tailed: 是否双尾检验
        
    Returns:
        (z 统计量, p 值)
    """
    if population_std <= 0:
        raise ValueError("标准差必须为正数")
    if sample_size <= 0:
        raise ValueError("样本大小必须为正数")
    
    # 计算标准误
    se = population_std / math.sqrt(sample_size)
    z = (sample_mean - population_mean) / se
    
    # 计算 p 值
    p = 2 * (1 - normal_cdf(abs(z)))
    if not two_tailed:
        p = p / 2
    
    return z, p


def confidence_interval(
    sample_mean: float,
    sample_std: float,
    sample_size: int,
    confidence: float = 0.95
) -> Tuple[float, float]:
    """
    计算置信区间
    
    Args:
        sample_mean: 样本均值
        sample_std: 样本标准差
        sample_size: 样本大小
        confidence: 置信水平 (0-1)
        
    Returns:
        (下限, 上限)
    """
    if not 0 < confidence < 1:
        raise ValueError("置信水平必须在 0-1 之间")
    if sample_size <= 0:
        raise ValueError("样本大小必须为正数")
    if sample_std < 0:
        raise ValueError("标准差必须为非负数")
    
    # 对于大样本，使用正态分布
    alpha = 1 - confidence
    z = normal_inv(1 - alpha / 2)
    
    se = sample_std / math.sqrt(sample_size)
    margin = z * se
    
    return (sample_mean - margin, sample_mean + margin)


# ============================================================
# 信息论
# ============================================================

def entropy(probabilities: List[float], base: float = 2) -> float:
    """
    计算信息熵
    
    H(X) = -Σ p(x) * log p(x)
    
    Args:
        probabilities: 概率分布
        base: 对数底数 (默认 2 为比特)
        
    Returns:
        熵值
    """
    if not probabilities:
        raise ValueError("概率列表不能为空")
    if not all(0 <= p <= 1 for p in probabilities):
        raise ValueError("概率必须在 0-1 之间")
    
    total = sum(probabilities)
    if abs(total - 1.0) > 1e-10:
        raise ValueError(f"概率总和必须为 1，当前为 {total}")
    
    h = 0.0
    for p in probabilities:
        if p > 0:
            h -= p * math.log(p, base)
    return h


def kl_divergence(p: List[float], q: List[float], base: float = 2) -> float:
    """
    计算 KL 散度（相对熵）
    
    D_KL(P||Q) = Σ p(x) * log(p(x) / q(x))
    
    Args:
        p: 真实分布
        q: 近似分布
        base: 对数底数
        
    Returns:
        KL 散度
    """
    if len(p) != len(q):
        raise ValueError("两个分布长度必须相同")
    
    kl = 0.0
    for pi, qi in zip(p, q):
        if pi > 0:
            if qi <= 0:
                raise ValueError("当 P(x) > 0 时，Q(x) 必须大于 0")
            kl += pi * math.log(pi / qi, base)
    return kl


def mutual_information(
    joint_prob: List[List[float]],
    base: float = 2
) -> float:
    """
    计算互信息
    
    I(X;Y) = Σ Σ p(x,y) * log(p(x,y) / (p(x) * p(y)))
    
    Args:
        joint_prob: 联合概率分布矩阵
        base: 对数底数
        
    Returns:
        互信息值
    """
    # 计算边际分布
    rows = len(joint_prob)
    cols = len(joint_prob[0]) if joint_prob else 0
    
    p_x = [sum(joint_prob[i][j] for j in range(cols)) for i in range(rows)]
    p_y = [sum(joint_prob[i][j] for i in range(rows)) for j in range(cols)]
    
    mi = 0.0
    for i in range(rows):
        for j in range(cols):
            p_xy = joint_prob[i][j]
            if p_xy > 0 and p_x[i] > 0 and p_y[j] > 0:
                mi += p_xy * math.log(p_xy / (p_x[i] * p_y[j]), base)
    return mi


# ============================================================
# 实用工具
# ============================================================

def describe(data: List[float]) -> Dict[str, float]:
    """
    生成数据的描述性统计
    
    Args:
        data: 数据列表
        
    Returns:
        统计摘要字典
    """
    if not data:
        raise ValueError("数据不能为空")
    
    sorted_data = sorted(data)
    n = len(data)
    
    return {
        'count': n,
        'mean': mean(data),
        'std': std_dev(data, population=False),
        'min': sorted_data[0],
        '25%': percentile(data, 25),
        '50%': percentile(data, 50),
        '75%': percentile(data, 75),
        'max': sorted_data[-1],
        'variance': variance(data, population=False),
        'skewness': skewness(data),
        'kurtosis': kurtosis(data),
        'iqr': iqr(data),
        'range': sorted_data[-1] - sorted_data[0]
    }


def probability_of_at_least_one(probabilities: List[float]) -> float:
    """
    计算至少一个事件发生的概率
    
    P(至少一个) = 1 - P(全不发生) = 1 - Π(1 - p_i)
    
    Args:
        probabilities: 各独立事件发生的概率列表
        
    Returns:
        至少一个发生的概率
    """
    if not probabilities:
        return 0.0
    if not all(0 <= p <= 1 for p in probabilities):
        raise ValueError("概率必须在 0-1 之间")
    
    p_none = 1.0
    for p in probabilities:
        p_none *= (1 - p)
    return 1 - p_none


def probability_of_all(probabilities: List[float]) -> float:
    """
    计算所有独立事件同时发生的概率
    
    P(全部发生) = Π p_i
    
    Args:
        probabilities: 各独立事件发生的概率列表
        
    Returns:
        全部发生的概率
    """
    if not probabilities:
        return 0.0
    if not all(0 <= p <= 1 for p in probabilities):
        raise ValueError("概率必须在 0-1 之间")
    
    result = 1.0
    for p in probabilities:
        result *= p
    return result


# ============================================================
# 主函数入口
# ============================================================

if __name__ == "__main__":
    # 演示用法
    print("=" * 60)
    print("Probability Utils - 概率与统计计算工具集")
    print("=" * 60)
    
    # 组合数学示例
    print("\n【组合数学】")
    print(f"5! = {factorial(5)}")
    print(f"P(10, 3) = {permutation(10, 3)}")
    print(f"C(10, 3) = {combination(10, 3)}")
    
    # 统计函数示例
    print("\n【统计函数】")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    stats = describe(data)
    for key, value in stats.items():
        print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")
    
    # 概率分布示例
    print("\n【概率分布】")
    print(f"正态分布 N(0,1) 在 x=1.96 处的 CDF: {normal_cdf(1.96):.4f}")
    print(f"二项分布 B(10, 0.5) P(X=5): {binomial_pmf(5, 10, 0.5):.4f}")
    print(f"泊松分布 Poisson(3) P(X=5): {poisson_pmf(5, 3):.4f}")
    
    # 贝叶斯定理示例
    print("\n【贝叶斯定理】")
    # 医学测试示例
    p_disease = 0.01  # 患病率
    p_positive_given_disease = 0.95  # 灵敏度
    p_positive_given_healthy = 0.05  # 假阳性率
    p_positive = p_positive_given_disease * p_disease + \
                 p_positive_given_healthy * (1 - p_disease)
    p_disease_given_positive = bayes_theorem(
        p_positive_given_disease, p_disease, p_positive
    )
    print(f"测试阳性时实际患病的概率: {p_disease_given_positive:.2%}")
    
    # 信息论示例
    print("\n【信息论】")
    print(f"公平硬币的熵: {entropy([0.5, 0.5]):.4f} 比特")
    print(f"偏倚硬币 (0.9, 0.1) 的熵: {entropy([0.9, 0.1]):.4f} 比特")
    
    print("\n" + "=" * 60)
    print("模块加载完成！")