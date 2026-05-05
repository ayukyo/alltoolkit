"""
Bayesian Estimator Utils - 贝叶斯估计器工具集

零依赖实现的贝叶斯统计和推断工具，包括：
- 贝叶斯参数估计
- 朴素贝叶斯分类器
- 贝叶斯平均（评分系统）
- 贝叶斯更新
- 贝叶斯假设检验

特点：
- 完全零外部依赖
- 支持多种分布（Beta、正态、泊松等）
- 高效的在线学习
- 可解释的概率输出

使用场景：
- A/B 测试分析
- 评分系统（如电影评分）
- 文本分类
- 异常检测
- 参数估计与不确定性量化
"""

from typing import Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import math
import random


# ============================================================================
# 数据类
# ============================================================================

@dataclass
class BetaDistribution:
    """
    Beta 分布参数
    
    Beta 分布常用于表示 0-1 之间的概率估计，
    如成功率、转化率等。
    
    参数:
        alpha: 成功次数 + 先验成功次数
        beta: 失败次数 + 先验失败次数
    
    示例:
        >>> bd = BetaDistribution(10, 5)
        >>> bd.mean  # 期望值
        0.666...
    """
    alpha: float
    beta: float
    
    @property
    def mean(self) -> float:
        """期望值 E[X] = alpha / (alpha + beta)"""
        return self.alpha / (self.alpha + self.beta)
    
    @property
    def variance(self) -> float:
        """方差 Var[X]"""
        total = self.alpha + self.beta
        return (self.alpha * self.beta) / (total ** 2 * (total + 1))
    
    @property
    def std_dev(self) -> float:
        """标准差"""
        return math.sqrt(self.variance)
    
    @property
    def mode(self) -> float:
        """众数（当 alpha, beta > 1 时）"""
        if self.alpha <= 1 or self.beta <= 1:
            return 0.0 if self.alpha < self.beta else 1.0
        return (self.alpha - 1) / (self.alpha + self.beta - 2)
    
    def pdf(self, x: float) -> float:
        """
        概率密度函数
        
        Args:
            x: 0-1 之间的值
        
        Returns:
            概率密度
        """
        if not 0 <= x <= 1:
            raise ValueError("x must be between 0 and 1")
        
        # Beta(x; alpha, beta) = x^(alpha-1) * (1-x)^(beta-1) / B(alpha, beta)
        log_pdf = (
            (self.alpha - 1) * math.log(x) if x > 0 else 0
        ) + (
            (self.beta - 1) * math.log(1 - x) if x < 1 else 0
        ) - math.lgamma(self.alpha) - math.lgamma(self.beta) + math.lgamma(self.alpha + self.beta)
        
        return math.exp(log_pdf)
    
    def cdf_approx(self, x: float) -> float:
        """
        累积分布函数近似值（使用正态近似）
        
        对于大 alpha, beta 时效果好
        """
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        
        # 正态近似
        z = (x - self.mean) / self.std_dev if self.std_dev > 0 else 0
        return _normal_cdf(z)
    
    def credible_interval(self, confidence: float = 0.95) -> Tuple[float, float]:
        """
        贝叶斯可信区间
        
        使用 Beta 分布的分位数近似
        
        Args:
            confidence: 置信水平 (默认 0.95)
        
        Returns:
            (下界, 上界)
        """
        # 使用 Wilson-Hilferty 近似转换为正态分布
        # 或者使用数值近似
        
        # 简化的近似方法
        margin = self.std_dev * _normal_quantile((1 + confidence) / 2)
        lower = max(0, self.mean - margin)
        upper = min(1, self.mean + margin)
        
        return (lower, upper)
    
    def sample(self, n: int = 1) -> List[float]:
        """
        从 Beta 分布采样
        
        使用 Beta 分布与 Gamma 分布的关系：
        Beta(a, b) = Gamma(a, 1) / (Gamma(a, 1) + Gamma(b, 1))
        
        Args:
            n: 采样数量
        
        Returns:
            样本列表
        """
        samples = []
        for _ in range(n):
            # 使用 Johnk's 方法（适用于 a, b <= 1）
            # 或使用 Gamma 分布近似
            
            # 使用拒绝采样方法
            if self.alpha < 1 and self.beta < 1:
                samples.append(_beta_sample_johnk(self.alpha, self.beta))
            else:
                # Gamma 分布方法
                ga = _gamma_sample(self.alpha)
                gb = _gamma_sample(self.beta)
                samples.append(ga / (ga + gb))
        
        return samples
    
    def update(self, successes: int, failures: int) -> 'BetaDistribution':
        """
        贝叶斯更新
        
        Args:
            successes: 新的成功次数
            failures: 新的失败次数
        
        Returns:
            更新后的 Beta 分布
        """
        return BetaDistribution(
            alpha=self.alpha + successes,
            beta=self.beta + failures
        )
    
    def __repr__(self) -> str:
        return f"BetaDistribution(alpha={self.alpha:.2f}, beta={self.beta:.2f}, mean={self.mean:.3f})"


@dataclass
class NormalDistribution:
    """
    正态分布参数
    
    用于表示连续值的贝叶斯估计。
    
    参数:
        mu: 均值
        sigma: 标准差
        precision: 精度 (1/sigma^2)
        n: 观测数量（用于在线更新）
    """
    mu: float
    sigma: float
    n: int = 1
    
    @property
    def variance(self) -> float:
        return self.sigma ** 2
    
    @property
    def precision(self) -> float:
        return 1 / self.variance
    
    def pdf(self, x: float) -> float:
        """概率密度函数"""
        z = (x - self.mu) / self.sigma
        return (1 / (self.sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * z ** 2)
    
    def cdf(self, x: float) -> float:
        """累积分布函数"""
        z = (x - self.mu) / self.sigma
        return _normal_cdf(z)
    
    def credible_interval(self, confidence: float = 0.95) -> Tuple[float, float]:
        """可信区间"""
        z = _normal_quantile((1 + confidence) / 2)
        return (self.mu - z * self.sigma, self.mu + z * self.sigma)
    
    def sample(self, n: int = 1) -> List[float]:
        """采样"""
        samples = []
        for _ in range(n):
            # Box-Muller 变换
            u1 = random.random()
            u2 = random.random()
            z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            samples.append(self.mu + self.sigma * z)
        return samples
    
    def update(self, observations: List[float], prior_sigma: Optional[float] = None) -> 'NormalDistribution':
        """
        贝叶斯更新
        
        Args:
            observations: 新观测值列表
            prior_sigma: 先验标准差（可选）
        
        Returns:
            更新后的正态分布
        """
        if not observations:
            return self
        
        # 简化的在线更新
        new_n = len(observations)
        total_n = self.n + new_n
        
        # 计算新均值
        new_mean = sum(observations) / new_n
        
        # 加权更新均值
        updated_mu = (self.n * self.mu + new_n * new_mean) / total_n
        
        # 更新方差（使用合并方差公式）
        new_var = sum((x - new_mean) ** 2 for x in observations) / new_n
        
        # 合并方差
        combined_var = (
            (self.n - 1) * self.variance + (new_n - 1) * new_var +
            self.n * new_n / total_n * (self.mu - new_mean) ** 2
        ) / (total_n - 1) if total_n > 1 else 0
        
        return NormalDistribution(
            mu=updated_mu,
            sigma=math.sqrt(combined_var),
            n=total_n
        )
    
    def __repr__(self) -> str:
        return f"NormalDistribution(mu={self.mu:.3f}, sigma={self.sigma:.3f}, n={self.n})"


@dataclass
class PoissonDistribution:
    """
    泊松分布参数
    
    用于表示计数数据的贝叶斯估计（如访问量、点击数）。
    
    参数:
        lambda_: 速率参数（期望计数）
        n: 观测数量
        total: 总计数
    """
    lambda_: float
    n: int = 1
    total: int = 0
    
    @property
    def mean(self) -> float:
        return self.lambda_
    
    @property
    def variance(self) -> float:
        return self.lambda_
    
    def pmf(self, k: int) -> float:
        """概率质量函数 P(X = k)"""
        if k < 0:
            return 0.0
        
        # P(X = k) = lambda^k * e^(-lambda) / k!
        log_pmf = k * math.log(self.lambda_) - self.lambda_ - _log_factorial(k)
        return math.exp(log_pmf)
    
    def cdf(self, k: int) -> float:
        """累积分布函数 P(X <= k)"""
        return sum(self.pmf(i) for i in range(k + 1))
    
    def update(self, observations: List[int]) -> 'PoissonDistribution':
        """
        贝叶斯更新（使用 Gamma 先验）
        
        Args:
            observations: 新观测的计数列表
        
        Returns:
            更新后的泊松分布
        """
        if not observations:
            return self
        
        new_n = len(observations)
        new_total = sum(observations)
        
        total_n = self.n + new_n
        total_sum = self.total + new_total
        
        # 后验均值（使用 Gamma(a+n, b+total) 的均值）
        # 这里使用简化的估计：lambda = total_sum / total_n
        updated_lambda = total_sum / total_n
        
        return PoissonDistribution(
            lambda_=updated_lambda,
            n=total_n,
            total=total_sum
        )
    
    def sample(self, n: int = 1) -> List[int]:
        """采样"""
        samples = []
        for _ in range(n):
            # Knuth 算法
            L = math.exp(-self.lambda_)
            k = 0
            p = 1.0
            while p > L:
                k += 1
                p *= random.random()
            samples.append(k - 1)
        return samples
    
    def __repr__(self) -> str:
        return f"PoissonDistribution(lambda={self.lambda_:.3f}, n={self.n}, total={self.total})"


@dataclass
class BayesianResult:
    """贝叶斯估计结果"""
    estimate: float
    lower_bound: float
    upper_bound: float
    confidence: float
    distribution: Union[BetaDistribution, NormalDistribution, PoissonDistribution]
    
    def __repr__(self) -> str:
        return (
            f"BayesianResult(estimate={self.estimate:.3f}, "
            f"ci=[{self.lower_bound:.3f}, {self.upper_bound:.3f}], "
            f"confidence={self.confidence:.1%})"
        )
    
    def contains(self, value: float) -> bool:
        """检查值是否在可信区间内"""
        return self.lower_bound <= value <= self.upper_bound
    
    def probability_above(self, threshold: float) -> float:
        """估计值超过阈值的概率"""
        if isinstance(self.distribution, BetaDistribution):
            if threshold >= 1:
                return 0.0
            if threshold <= 0:
                return 1.0
            # 使用 Beta 分布近似
            return 1 - self.distribution.cdf_approx(threshold)
        elif isinstance(self.distribution, NormalDistribution):
            return 1 - self.distribution.cdf(threshold)
        return 0.5  # 默认


# ============================================================================
# 贝叶斯估计器
# ============================================================================

class BayesianEstimator:
    """
    贝叶斯估计器
    
    支持多种分布的贝叶斯参数估计。
    
    示例:
        >>> estimator = BayesianEstimator()
        >>> estimator.update_beta(10, 5)  # 10次成功，5次失败
        >>> estimator.beta_mean  # 估计的概率
        0.666...
        >>> estimator.beta_credible_interval(0.95)  # 95%可信区间
        (0.4, 0.9)
    """
    
    def __init__(
        self,
        prior_alpha: float = 1.0,
        prior_beta: float = 1.0,
        prior_mu: float = 0.0,
        prior_sigma: float = 1.0
    ):
        """
        初始化贝叶斯估计器
        
        Args:
            prior_alpha: Beta 分布先验 alpha（成功参数）
            prior_beta: Beta 分布先验 beta（失败参数）
            prior_mu: 正态分布先验均值
            prior_sigma: 正态分布先验标准差
        """
        self._beta = BetaDistribution(prior_alpha, prior_beta)
        self._normal = NormalDistribution(prior_mu, prior_sigma)
        self._poisson = PoissonDistribution(1.0)
    
    # Beta 分布估计（概率/比率）
    
    def update_beta(self, successes: int, failures: int) -> BetaDistribution:
        """
        更新 Beta 分布估计
        
        Args:
            successes: 成功次数
            failures: 失败次数
        
        Returns:
            更新后的 Beta 分布
        """
        self._beta = self._beta.update(successes, failures)
        return self._beta
    
    def beta_mean(self) -> float:
        """Beta 分布估计均值"""
        return self._beta.mean
    
    def beta_variance(self) -> float:
        """Beta 分布估计方差"""
        return self._beta.variance
    
    def beta_credible_interval(self, confidence: float = 0.95) -> Tuple[float, float]:
        """Beta 分布可信区间"""
        return self._beta.credible_interval(confidence)
    
    def beta_estimate(self, confidence: float = 0.95) -> BayesianResult:
        """获取 Beta 分布估计结果"""
        ci = self.beta_credible_interval(confidence)
        return BayesianResult(
            estimate=self._beta.mean,
            lower_bound=ci[0],
            upper_bound=ci[1],
            confidence=confidence,
            distribution=self._beta
        )
    
    def beta_sample(self, n: int = 1) -> List[float]:
        """从 Beta 后验分布采样"""
        return self._beta.sample(n)
    
    # 正态分布估计
    
    def update_normal(self, observations: List[float]) -> NormalDistribution:
        """
        更新正态分布估计
        
        Args:
            observations: 观测值列表
        
        Returns:
            更新后的正态分布
        """
        self._normal = self._normal.update(observations)
        return self._normal
    
    def normal_mean(self) -> float:
        """正态分布估计均值"""
        return self._normal.mu
    
    def normal_credible_interval(self, confidence: float = 0.95) -> Tuple[float, float]:
        """正态分布可信区间"""
        return self._normal.credible_interval(confidence)
    
    def normal_estimate(self, confidence: float = 0.95) -> BayesianResult:
        """获取正态分布估计结果"""
        ci = self.normal_credible_interval(confidence)
        return BayesianResult(
            estimate=self._normal.mu,
            lower_bound=ci[0],
            upper_bound=ci[1],
            confidence=confidence,
            distribution=self._normal
        )
    
    # 泊松分布估计
    
    def update_poisson(self, observations: List[int]) -> PoissonDistribution:
        """更新泊松分布估计"""
        self._poisson = self._poisson.update(observations)
        return self._poisson
    
    def poisson_mean(self) -> float:
        """泊松分布估计均值"""
        return self._poisson.lambda_
    
    def poisson_estimate(self) -> BayesianResult:
        """获取泊松分布估计结果"""
        # 使用正态近似计算可信区间
        sigma = math.sqrt(self._poisson.lambda_)
        z = _normal_quantile(0.975)
        return BayesianResult(
            estimate=self._poisson.lambda_,
            lower_bound=max(0, self._poisson.lambda_ - z * sigma),
            upper_bound=self._poisson.lambda_ + z * sigma,
            confidence=0.95,
            distribution=self._poisson
        )
    
    def reset(self) -> None:
        """重置估计器"""
        self._beta = BetaDistribution(1.0, 1.0)
        self._normal = NormalDistribution(0.0, 1.0)
        self._poisson = PoissonDistribution(1.0)
    
    def __repr__(self) -> str:
        return (
            f"BayesianEstimator(beta={self._beta}, "
            f"normal={self._normal}, "
            f"poisson={self._poisson})"
        )


# ============================================================================
# 贝叶斯平均（评分系统）
# ============================================================================

class BayesianAverage:
    """
    贝叶斯平均
    
    用于解决评分系统中的小样本问题。
    当评分数量较少时，使用全局平均作为先验，
    避免极端评分的影响。
    
    公式: (C * m + n * r) / (C + n)
    其中:
        C: 先验权重（常数）
        m: 全局平均（先验均值）
        n: 该项目的评分数量
        r: 该项目的平均评分
    
    示例:
        >>> ba = BayesianAverage(global_mean=3.5, prior_weight=10)
        >>> ba.add_item("movie1", ratings=[5, 5, 4])
        >>> ba.add_item("movie2", ratings=[1])
        >>> ba.get_bayesian_average("movie1")  # 有足够评分，接近实际平均
        4.5
        >>> ba.get_bayesian_average("movie2")  # 评分少，向全局平均收缩
        2.5
    """
    
    def __init__(
        self,
        global_mean: float = 3.0,
        prior_weight: float = 5.0,
        min_value: float = 1.0,
        max_value: float = 5.0
    ):
        """
        初始化贝叶斯平均
        
        Args:
            global_mean: 全局平均评分（先验）
            prior_weight: 先验权重（C）
            min_value: 最小评分值
            max_value: 最大评分值
        """
        self.global_mean = global_mean
        self.prior_weight = prior_weight
        self.min_value = min_value
        self.max_value = max_value
        
        self._items: Dict[str, Dict] = defaultdict(lambda: {
            'ratings': [],
            'sum': 0,
            'count': 0
        })
        self._global_total = 0.0
        self._global_count = 0
    
    def add_item(self, item_id: str, ratings: List[float]) -> None:
        """
        添加项目的评分
        
        Args:
            item_id: 项目标识
            ratings: 评分列表
        """
        for rating in ratings:
            if not self.min_value <= rating <= self.max_value:
                raise ValueError(f"Rating must be between {self.min_value} and {self.max_value}")
            
            self._items[item_id]['ratings'].append(rating)
            self._items[item_id]['sum'] += rating
            self._items[item_id]['count'] += 1
            
            self._global_total += rating
            self._global_count += 1
    
    def add_rating(self, item_id: str, rating: float) -> None:
        """添加单个评分"""
        self.add_item(item_id, [rating])
    
    def get_average(self, item_id: str) -> float:
        """获取项目的简单平均"""
        data = self._items[item_id]
        if data['count'] == 0:
            return self.global_mean
        return data['sum'] / data['count']
    
    def get_bayesian_average(self, item_id: str) -> float:
        """
        获取贝叶斯平均
        
        公式: (C * m + n * r) / (C + n)
        """
        data = self._items[item_id]
        n = data['count']
        r = data['sum'] / n if n > 0 else self.global_mean
        
        # 使用更新的全局平均（如果有数据）
        m = self._global_total / self._global_count if self._global_count > 0 else self.global_mean
        
        # 贝叶斯平均
        bayesian_avg = (self.prior_weight * m + n * r) / (self.prior_weight + n)
        
        return bayesian_avg
    
    def get_item_count(self, item_id: str) -> int:
        """获取项目评分数量"""
        return self._items[item_id]['count']
    
    def get_all_items(self) -> List[str]:
        """获取所有项目ID"""
        return list(self._items.keys())
    
    def rank_items(self, use_bayesian: bool = True) -> List[Tuple[str, float]]:
        """
        对项目排名
        
        Args:
            use_bayesian: 是否使用贝叶斯平均
        
        Returns:
            排名列表 [(item_id, score), ...]
        """
        if use_bayesian:
            scores = [(id, self.get_bayesian_average(id)) for id in self._items.keys()]
        else:
            scores = [(id, self.get_average(id)) for id in self._items.keys()]
        
        return sorted(scores, key=lambda x: x[1], reverse=True)
    
    def update_global_mean(self) -> None:
        """更新全局平均"""
        if self._global_count > 0:
            self.global_mean = self._global_total / self._global_count
    
    def set_prior_weight(self, weight: float) -> None:
        """设置先验权重"""
        self.prior_weight = weight
    
    def clear(self) -> None:
        """清空所有数据"""
        self._items.clear()
        self._global_total = 0.0
        self._global_count = 0
    
    @property
    def total_ratings(self) -> int:
        """总评分数量"""
        return self._global_count
    
    @property
    def total_items(self) -> int:
        """总项目数量"""
        return len(self._items)
    
    def __repr__(self) -> str:
        return (
            f"BayesianAverage(items={self.total_items}, "
            f"ratings={self.total_ratings}, "
            f"global_mean={self.global_mean:.2f}, "
            f"prior_weight={self.prior_weight})"
        )


# ============================================================================
# 朴素贝叶斯分类器
# ============================================================================

class NaiveBayesClassifier:
    """
    朴素贝叶斯分类器
    
    零依赖实现的朴素贝叶斯分类器，适用于文本分类等场景。
    
    特点:
        - 支持离散特征（词频等）
        - 支持连续特征（使用正态分布）
        - 支持拉普拉斯平滑
        - 支持在线学习
    
    示例:
        >>> clf = NaiveBayesClassifier()
        >>> clf.train("positive", ["good", "great", "awesome"])
        >>> clf.train("negative", ["bad", "terrible", "awful"])
        >>> clf.predict(["good", "movie"])
        {'positive': 0.8, 'negative': 0.2}
    """
    
    def __init__(self, laplace_smoothing: float = 1.0):
        """
        初始化朴素贝叶斯分类器
        
        Args:
            laplace_smoothing: 拉普拉斯平滑参数（避免零概率）
        """
        self.smoothing = laplace_smoothing
        
        # 类别统计
        self._class_counts: Dict[str, int] = defaultdict(int)
        self._total_docs = 0
        
        # 特征统计
        self._feature_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._feature_totals: Dict[str, int] = defaultdict(int)
        
        # 词汇表
        self._vocab: set = set()
        
        # 连续特征统计（用于正态分布）
        self._continuous_stats: Dict[str, Dict[str, Dict]] = defaultdict(lambda: defaultdict(lambda: {
            'sum': 0.0,
            'sum_sq': 0.0,
            'count': 0
        }))
    
    def train(self, label: str, features: Union[List[str], Dict[str, Union[int, float]]]) -> None:
        """
        训练一个样本
        
        Args:
            label: 类别标签
            features: 特征列表（离散）或字典（可包含连续特征）
        """
        self._class_counts[label] += 1
        self._total_docs += 1
        
        if isinstance(features, list):
            # 离散特征（词列表）
            for feature in features:
                self._feature_counts[label][feature] += 1
                self._feature_totals[label] += 1
                self._vocab.add(feature)
        
        elif isinstance(features, dict):
            # 混合特征
            for feature, value in features.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    # 连续特征
                    stats = self._continuous_stats[label][feature]
                    stats['sum'] += value
                    stats['sum_sq'] += value ** 2
                    stats['count'] += 1
                else:
                    # 离散特征
                    count = value if isinstance(value, int) else 1
                    self._feature_counts[label][feature] += count
                    self._feature_totals[label] += count
                    self._vocab.add(feature)
    
    def train_batch(self, samples: List[Tuple[str, Union[List[str], Dict]]]) -> None:
        """
        批量训练
        
        Args:
            samples: [(label, features), ...] 列表
        """
        for label, features in samples:
            self.train(label, features)
    
    def predict(self, features: Union[List[str], Dict[str, Union[int, float]]]) -> Dict[str, float]:
        """
        预测概率
        
        Args:
            features: 特征
        
        Returns:
            各类别的概率字典
        """
        if self._total_docs == 0:
            raise ValueError("Model not trained yet")
        
        log_probs = {}
        
        for label in self._class_counts.keys():
            # 类别先验概率
            log_prob = math.log(self._class_counts[label] / self._total_docs)
            
            if isinstance(features, list):
                # 离散特征
                for feature in features:
                    # 特征条件概率 P(feature | label)
                    count = self._feature_counts[label][feature]
                    total = self._feature_totals[label]
                    vocab_size = len(self._vocab)
                    
                    # 拉普拉斯平滑
                    prob = (count + self.smoothing) / (total + self.smoothing * vocab_size)
                    log_prob += math.log(prob)
            
            elif isinstance(features, dict):
                for feature, value in features.items():
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        # 连续特征：使用正态分布
                        stats = self._continuous_stats[label][feature]
                        if stats['count'] > 0:
                            mean = stats['sum'] / stats['count']
                            var = (stats['sum_sq'] / stats['count']) - mean ** 2
                            var = max(var, 1e-10)  # 防止方差为0
                            
                            # 正态分布概率密度
                            log_prob += -0.5 * math.log(2 * math.pi * var) - 0.5 * ((value - mean) ** 2) / var
                    else:
                        count = self._feature_counts[label][feature]
                        total = self._feature_totals[label]
                        vocab_size = len(self._vocab)
                        prob = (count + self.smoothing) / (total + self.smoothing * vocab_size)
                        log_prob += math.log(prob) if prob > 0 else -20
            
            log_probs[label] = log_prob
        
        # 转换为概率（减去最大值避免溢出）
        max_log = max(log_probs.values())
        probs = {label: math.exp(log_prob - max_log) for label, log_prob in log_probs.items()}
        
        # 归一化
        total = sum(probs.values())
        return {label: p / total for label, p in probs.items()}
    
    def predict_label(self, features: Union[List[str], Dict]) -> str:
        """预测最可能的类别"""
        probs = self.predict(features)
        return max(probs.keys(), key=lambda k: probs[k])
    
    def get_class_probability(self, label: str) -> float:
        """获取类别先验概率"""
        return self._class_counts[label] / self._total_docs if self._total_docs > 0 else 0
    
    def get_feature_probability(self, label: str, feature: str) -> float:
        """获取特征条件概率"""
        count = self._feature_counts[label][feature]
        total = self._feature_totals[label]
        vocab_size = len(self._vocab)
        
        return (count + self.smoothing) / (total + self.smoothing * vocab_size)
    
    def get_top_features(self, label: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        获取类别最重要的特征
        
        Args:
            label: 类别标签
            top_n: 返回数量
        
        Returns:
            [(feature, probability), ...]
        """
        features = self._feature_counts[label]
        probs = [(f, self.get_feature_probability(label, f)) for f in features.keys()]
        return sorted(probs, key=lambda x: x[1], reverse=True)[:top_n]
    
    def get_classes(self) -> List[str]:
        """获取所有类别"""
        return list(self._class_counts.keys())
    
    def get_vocab_size(self) -> int:
        """获取词汇表大小"""
        return len(self._vocab)
    
    def clear(self) -> None:
        """清空模型"""
        self._class_counts.clear()
        self._total_docs = 0
        self._feature_counts.clear()
        self._feature_totals.clear()
        self._vocab.clear()
        self._continuous_stats.clear()
    
    def __repr__(self) -> str:
        return (
            f"NaiveBayesClassifier(classes={len(self._class_counts)}, "
            f"docs={self._total_docs}, "
            f"vocab={len(self._vocab)}, "
            f"smoothing={self.smoothing})"
        )


# ============================================================================
# 贝叶斯假设检验（A/B 测试）
# ============================================================================

class ABTestBayesian:
    """
    贝叶斯 A/B 测试
    
    使用贝叶斯方法进行 A/B 测试分析，
    输出概率而非 p 值。
    
    示例:
        >>> test = ABTestBayesian()
        >>> test.add_result('A', successes=100, failures=900)
        >>> test.add_result('B', successes=120, failures=880)
        >>> test.probability_b_better()
        0.85  # B 比 A 好的概率
        >>> test.expected_loss()
        0.02  # 选择 B 的期望损失
    """
    
    def __init__(self, prior_alpha: float = 1.0, prior_beta: float = 1.0):
        """
        初始化 A/B 测试
        
        Args:
            prior_alpha: Beta 分布先验 alpha
            prior_beta: Beta 分布先验 beta
        """
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta
        
        self._variants: Dict[str, BetaDistribution] = {}
    
    def add_result(self, variant: str, successes: int, failures: int) -> None:
        """
        添加变体的结果
        
        Args:
            variant: 变体名称（如 'A', 'B'）
            successes: 成功次数
            failures: 失败次数
        """
        self._variants[variant] = BetaDistribution(
            alpha=self.prior_alpha + successes,
            beta=self.prior_beta + failures
        )
    
    def get_rate_estimate(self, variant: str) -> float:
        """获取变体的率估计"""
        return self._variants[variant].mean
    
    def get_credible_interval(self, variant: str, confidence: float = 0.95) -> Tuple[float, float]:
        """获取变体的可信区间"""
        return self._variants[variant].credible_interval(confidence)
    
    def probability_better(self, variant1: str, variant2: str, n_samples: int = 10000) -> float:
        """
        计算一个变体比另一个更好的概率
        
        Args:
            variant1: 第一个变体
            variant2: 第二个变体
            n_samples: 采样数量
        
        Returns:
            variant1 > variant2 的概率
        """
        if variant1 not in self._variants or variant2 not in self._variants:
            raise ValueError("Both variants must have results")
        
        # 从两个 Beta 分布采样并比较
        samples1 = self._variants[variant1].sample(n_samples)
        samples2 = self._variants[variant2].sample(n_samples)
        
        wins = sum(1 for s1, s2 in zip(samples1, samples2) if s1 > s2)
        ties = sum(1 for s1, s2 in zip(samples1, samples2) if s1 == s2)
        
        return (wins + ties * 0.5) / n_samples
    
    def probability_b_better(self, n_samples: int = 10000) -> float:
        """计算 B 比 A 好的概率（需要 'A' 和 'B' 变体）"""
        if 'A' not in self._variants or 'B' not in self._variants:
            raise ValueError("Need 'A' and 'B' variants")
        return self.probability_better('B', 'A', n_samples)
    
    def expected_loss(self, chosen: str, other: str, n_samples: int = 10000) -> float:
        """
        计算选择某个变体的期望损失
        
        Args:
            chosen: 选择的变体
            other: 其他变体
            n_samples: 采样数量
        
        Returns:
            期望损失（如果选择错误）
        """
        if chosen not in self._variants or other not in self._variants:
            raise ValueError("Both variants must have results")
        
        samples_chosen = self._variants[chosen].sample(n_samples)
        samples_other = self._variants[other].sample(n_samples)
        
        # 期望损失 = max(0, other - chosen) 的期望
        losses = [max(0, s_other - s_chosen) for s_chosen, s_other in zip(samples_chosen, samples_other)]
        return sum(losses) / n_samples
    
    def expected_gain(self, variant1: str, variant2: str, n_samples: int = 10000) -> float:
        """
        计算选择 variant1 优于 variant2 的期望增益
        
        Args:
            variant1: 第一个变体
            variant2: 第二个变体
            n_samples: 采样数量
        
        Returns:
            期望增益
        """
        if variant1 not in self._variants or variant2 not in self._variants:
            raise ValueError("Both variants must have results")
        
        samples1 = self._variants[variant1].sample(n_samples)
        samples2 = self._variants[variant2].sample(n_samples)
        
        gains = [max(0, s1 - s2) for s1, s2 in zip(samples1, samples2)]
        return sum(gains) / n_samples
    
    def recommend(self, threshold: float = 0.95, n_samples: int = 10000) -> Dict[str, Union[str, float]]:
        """
        推荐最佳变体
        
        Args:
            threshold: 确定性阈值（超过此值才推荐）
            n_samples: 采样数量
        
        Returns:
            推荐结果字典
        """
        variants = list(self._variants.keys())
        if len(variants) < 2:
            return {'recommendation': variants[0] if variants else None, 'confidence': 1.0}
        
        # 找到最好的变体
        best_variant = max(variants, key=lambda v: self._variants[v].mean)
        
        # 计算它比其他所有变体都好的概率
        probs = []
        for other in variants:
            if other != best_variant:
                prob = self.probability_better(best_variant, other, n_samples)
                probs.append(prob)
        
        min_prob = min(probs) if probs else 1.0
        
        return {
            'recommendation': best_variant if min_prob >= threshold else None,
            'confidence': min_prob,
            'rates': {v: self._variants[v].mean for v in variants},
            'expected_loss': {v: self.expected_loss(v, best_variant, n_samples) for v in variants if v != best_variant}
        }
    
    def get_variants(self) -> List[str]:
        """获取所有变体"""
        return list(self._variants.keys())
    
    def summary(self, n_samples: int = 10000) -> Dict:
        """
        获取测试摘要
        
        Returns:
            包含所有统计的字典
        """
        variants = list(self._variants.keys())
        
        summary = {
            'variants': variants,
            'rates': {v: self._variants[v].mean for v in variants},
            'credible_intervals': {v: self._variants[v].credible_interval(0.95) for v in variants},
        }
        
        if len(variants) >= 2:
            # 添加比较统计
            v1, v2 = variants[0], variants[1]
            summary['comparison'] = {
                f'{v2}_vs_{v1}': {
                    'prob_better': self.probability_better(v2, v1, n_samples),
                    'expected_gain': self.expected_gain(v2, v1, n_samples),
                    'expected_loss_if_choose_v2': self.expected_loss(v2, v1, n_samples),
                    'expected_loss_if_choose_v1': self.expected_loss(v1, v2, n_samples),
                }
            }
        
        return summary
    
    def clear(self) -> None:
        """清空测试"""
        self._variants.clear()
    
    def __repr__(self) -> str:
        rates = {v: self._variants[v].mean for v in self._variants}
        return f"ABTestBayesian(variants={list(self._variants.keys())}, rates={rates})"


# ============================================================================
# 辅助函数
# ============================================================================

def _normal_cdf(z: float) -> float:
    """
    标准正态分布累积分布函数近似
    
    使用 Abramowitz and Stegun 近似
    """
    if z < -8:
        return 0.0
    if z > 8:
        return 1.0
    
    # Abramowitz and Stegun 公式 7.1.26
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    
    sign = 1 if z >= 0 else -1
    z = abs(z) / math.sqrt(2)
    
    t = 1.0 / (1.0 + p * z)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-z * z)
    
    return 0.5 * (1.0 + sign * y)


def _normal_quantile(p: float) -> float:
    """
    标准正态分布分位数近似
    
    使用简单近似
    """
    if p <= 0:
        return -float('inf')
    if p >= 1:
        return float('inf')
    
    # Beasley-Springer-Moro 算法简化版
    if p == 0.5:
        return 0.0
    
    # 使用 Rational approximation
    if p < 0.5:
        return -_normal_quantile(1 - p)
    
    # p > 0.5
    q = p - 0.5
    r = q * q
    
    # 简化的近似公式
    x = q * (
        2.50662823884 +
        r * (
            -18.61500062529 +
            r * (
                41.39119773534 +
                r * (
                    -25.44106049637
                )
            )
        )
    ) / (
        1 +
        r * (
            -8.47351093090 +
            r * (
                23.08336743743 +
                r * (
                    -20.51823782853 +
                    r * 5.54161136669
                )
            )
        )
    )
    
    return x


def _log_factorial(n: int) -> float:
    """计算 log(n!)"""
    if n <= 1:
        return 0.0
    return sum(math.log(i) for i in range(2, n + 1))


def _gamma_sample(alpha: float) -> float:
    """
    Gamma 分布采样
    
    使用 Marsaglia and Tsang's 方法
    """
    if alpha < 1:
        # 转换为 alpha >= 1
        u = random.random()
        return _gamma_sample(alpha + 1) * (u ** (1 / alpha))
    
    d = alpha - 1 / 3
    c = 1 / math.sqrt(9 * d)
    
    while True:
        x = random.gauss(0, 1)
        v = (1 + c * x) ** 3
        
        if v > 0:
            u = random.random()
            
            # 检验条件
            if u < 1 - 0.0331 * (x ** 2) ** 2:
                return d * v
            
            if math.log(u) < 0.5 * x ** 2 + d * (1 - v + math.log(v)):
                return d * v


def _beta_sample_johnk(alpha: float, beta: float) -> float:
    """
    Beta 分布采样（Johnk's 方法）
    
    适用于 alpha, beta <= 1
    """
    while True:
        u1 = random.random()
        u2 = random.random()
        
        v1 = u1 ** (1 / alpha)
        v2 = u2 ** (1 / beta)
        
        s = v1 + v2
        
        if s <= 1:
            return v1 / s


# ============================================================================
# 便捷函数
# ============================================================================

def beta_estimate(successes: int, failures: int, confidence: float = 0.95) -> BayesianResult:
    """
    快速 Beta 分布估计
    
    Args:
        successes: 成功次数
        failures: 失败次数
        confidence: 置信水平
    
    Returns:
        贝叶斯估计结果
    
    示例:
        >>> result = beta_estimate(100, 50)
        >>> result.estimate  # 估计概率
        0.666...
    """
    dist = BetaDistribution(1 + successes, 1 + failures)
    ci = dist.credible_interval(confidence)
    
    return BayesianResult(
        estimate=dist.mean,
        lower_bound=ci[0],
        upper_bound=ci[1],
        confidence=confidence,
        distribution=dist
    )


def normal_estimate(observations: List[float], confidence: float = 0.95) -> BayesianResult:
    """
    快速正态分布估计
    
    Args:
        observations: 观测值列表
        confidence: 置信水平
    
    Returns:
        贝叶斯估计结果
    """
    if not observations:
        raise ValueError("Need at least one observation")
    
    n = len(observations)
    mean = sum(observations) / n
    variance = sum((x - mean) ** 2 for x in observations) / n
    sigma = math.sqrt(variance)
    
    # 考虑样本大小调整可信区间
    adjusted_sigma = sigma / math.sqrt(n)
    
    dist = NormalDistribution(mean, adjusted_sigma, n)
    ci = dist.credible_interval(confidence)
    
    return BayesianResult(
        estimate=mean,
        lower_bound=ci[0],
        upper_bound=ci[1],
        confidence=confidence,
        distribution=dist
    )


def poisson_estimate(observations: List[int]) -> BayesianResult:
    """
    快速泊松分布估计
    
    Args:
        observations: 计数观测值列表
    
    Returns:
        贝叶斯估计结果
    """
    if not observations:
        raise ValueError("Need at least one observation")
    
    n = len(observations)
    total = sum(observations)
    lambda_ = total / n
    
    # 使用正态近似计算可信区间
    sigma = math.sqrt(lambda_ / n)
    z = _normal_quantile(0.975)
    
    return BayesianResult(
        estimate=lambda_,
        lower_bound=max(0, lambda_ - z * sigma),
        upper_bound=lambda_ + z * sigma,
        confidence=0.95,
        distribution=PoissonDistribution(lambda_, n, total)
    )


def create_classifier(smoothing: float = 1.0) -> NaiveBayesClassifier:
    """创建朴素贝叶斯分类器"""
    return NaiveBayesClassifier(smoothing)


def create_ab_test(prior_alpha: float = 1.0, prior_beta: float = 1.0) -> ABTestBayesian:
    """创建贝叶斯 A/B 测试"""
    return ABTestBayesian(prior_alpha, prior_beta)


def create_bayesian_average(
    global_mean: float = 3.0,
    prior_weight: float = 5.0
) -> BayesianAverage:
    """创建贝叶斯平均评分系统"""
    return BayesianAverage(global_mean, prior_weight)


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Bayesian Estimator Utils - 贝叶斯估计器工具集")
    print("=" * 60)
    
    # 1. Beta 分布估计示例
    print("\n1. Beta 分布估计（概率估计）")
    print("-" * 40)
    
    result = beta_estimate(100, 50, 0.95)
    print(f"成功: 100, 失败: 50")
    print(f"估计概率: {result.estimate:.3f}")
    print(f"95% 可信区间: [{result.lower_bound:.3f}, {result.upper_bound:.3f}]")
    
    # 2. 贝叶斯 A/B 测试示例
    print("\n2. 贝叶斯 A/B 测试")
    print("-" * 40)
    
    ab_test = create_ab_test()
    ab_test.add_result('A', successes=100, failures=900)
    ab_test.add_result('B', successes=150, failures=850)
    
    print(f"A 版本转化率: {ab_test.get_rate_estimate('A'):.3f}")
    print(f"B 版本转化率: {ab_test.get_rate_estimate('B'):.3f}")
    print(f"B 比 A 好的概率: {ab_test.probability_b_better():.1%}")
    
    recommendation = ab_test.recommend()
    print(f"推荐: {recommendation['recommendation']} (置信度: {recommendation['confidence']:.1%})")
    
    # 3. 贝叶斯平均示例
    print("\n3. 贝叶斯平均（评分系统）")
    print("-" * 40)
    
    ba = create_bayesian_average(global_mean=3.5, prior_weight=10)
    ba.add_item("热门电影", [5, 5, 4, 4, 5, 4, 5, 3, 4, 5])
    ba.add_item("新电影", [5])  # 只有一个评分
    
    print(f"热门电影: 普通平均={ba.get_average('热门电影'):.2f}, 贝叶斯平均={ba.get_bayesian_average('热门电影'):.2f}")
    print(f"新电影: 普通平均={ba.get_average('新电影'):.2f}, 贝叶斯平均={ba.get_bayesian_average('新电影'):.2f}")
    print("\n排名（贝叶斯平均）:")
    for item, score in ba.rank_items():
        print(f"  {item}: {score:.2f}")
    
    # 4. 朴素贝叶斯分类器示例
    print("\n4. 朴素贝叶斯分类器")
    print("-" * 40)
    
    clf = create_classifier()
    
    # 训练样本
    positive_samples = [
        ["good", "great", "excellent", "awesome"],
        ["love", "this", "product"],
        ["happy", "satisfied", "quality"],
    ]
    negative_samples = [
        ["bad", "terrible", "awful", "disappointed"],
        ["hate", "this", "product"],
        ["poor", "quality", "broken"],
    ]
    
    for features in positive_samples:
        clf.train("positive", features)
    
    for features in negative_samples:
        clf.train("negative", features)
    
    # 预测
    test_features = ["good", "quality", "product"]
    probs = clf.predict(test_features)
    
    print(f"测试: {test_features}")
    print(f"预测: {clf.predict_label(test_features)}")
    print(f"概率: positive={probs['positive']:.2f}, negative={probs['negative']:.2f}")
    
    # 5. 正态分布估计示例
    print("\n5. 正态分布估计")
    print("-" * 40)
    
    measurements = [25.3, 24.8, 25.1, 25.5, 24.9, 25.2, 25.0]
    result = normal_estimate(measurements, 0.95)
    
    print(f"测量值: {measurements}")
    print(f"估计均值: {result.estimate:.2f}")
    print(f"95% 可信区间: [{result.lower_bound:.2f}, {result.upper_bound:.2f}]")
    
    print("\n" + "=" * 60)
    print("所有测试完成!")