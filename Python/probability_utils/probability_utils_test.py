"""
probability_utils 测试套件

测试覆盖：
- 基础数学函数
- 统计函数
- 概率分布
- 贝叶斯与条件概率
- 随机采样
- 信息论
"""

import unittest
import math
import random
from mod import (
    # 基础数学
    factorial, permutation, combination, gcd, lcm,
    # 统计函数
    mean, median, mode, variance, std_dev,
    covariance, correlation, percentile, quartiles, iqr,
    skewness, kurtosis, describe,
    # 概率分布
    normal_pdf, normal_cdf, normal_inv,
    binomial_pmf, binomial_cdf,
    poisson_pmf, poisson_cdf,
    exponential_pdf, exponential_cdf,
    geometric_pmf, geometric_cdf,
    hypergeometric_pmf,
    negative_binomial_pmf,
    # 贝叶斯
    conditional_probability, bayes_theorem, bayes_theorem_multiple,
    # 随机采样
    weighted_choice, sample_without_replacement, rejection_sampling,
    # 统计检验
    z_score, z_test, confidence_interval,
    # 信息论
    entropy, kl_divergence, mutual_information,
    # 实用工具
    probability_of_at_least_one, probability_of_all
)


class TestBasicMath(unittest.TestCase):
    """测试基础数学函数"""
    
    def test_factorial(self):
        """测试阶乘"""
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)
        
    def test_factorial_negative(self):
        """测试负数阶乘抛出异常"""
        with self.assertRaises(ValueError):
            factorial(-1)
    
    def test_permutation(self):
        """测试排列"""
        self.assertEqual(permutation(5, 3), 60)
        self.assertEqual(permutation(10, 2), 90)
        self.assertEqual(permutation(5, 0), 1)
        self.assertEqual(permutation(5, 5), 120)
        self.assertEqual(permutation(5, 6), 0)
    
    def test_combination(self):
        """测试组合"""
        self.assertEqual(combination(5, 3), 10)
        self.assertEqual(combination(10, 2), 45)
        self.assertEqual(combination(5, 0), 1)
        self.assertEqual(combination(5, 5), 1)
        # 测试对称性
        self.assertEqual(combination(10, 3), combination(10, 7))
    
    def test_gcd(self):
        """测试最大公约数"""
        self.assertEqual(gcd(12, 8), 4)
        self.assertEqual(gcd(17, 13), 1)
        self.assertEqual(gcd(100, 25), 25)
        self.assertEqual(gcd(0, 5), 5)
    
    def test_lcm(self):
        """测试最小公倍数"""
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(3, 5), 15)
        self.assertEqual(lcm(12, 8), 24)
        self.assertEqual(lcm(0, 5), 0)


class TestStatistics(unittest.TestCase):
    """测试统计函数"""
    
    def setUp(self):
        self.data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.data_odd = [1, 2, 3, 4, 5]
    
    def test_mean(self):
        """测试均值"""
        self.assertEqual(mean(self.data), 5.5)
        self.assertEqual(mean([1, 2, 3]), 2.0)
    
    def test_median(self):
        """测试中位数"""
        self.assertEqual(median(self.data), 5.5)
        self.assertEqual(median(self.data_odd), 3)
        self.assertEqual(median([1, 2, 3, 4]), 2.5)
    
    def test_mode(self):
        """测试众数"""
        self.assertEqual(mode([1, 2, 2, 3, 3, 3]), [3])
        self.assertEqual(sorted(mode([1, 1, 2, 2, 3])), [1, 2])
    
    def test_variance(self):
        """测试方差"""
        # 总体方差
        self.assertAlmostEqual(variance([1, 2, 3, 4, 5], population=True), 2.0)
        # 样本方差
        self.assertAlmostEqual(variance([1, 2, 3, 4, 5], population=False), 2.5)
    
    def test_std_dev(self):
        """测试标准差"""
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        # 总体标准差
        self.assertAlmostEqual(std_dev(data, population=True), 2.0, places=5)
    
    def test_covariance(self):
        """测试协方差"""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        self.assertAlmostEqual(covariance(x, y, population=True), 4.0)
    
    def test_correlation(self):
        """测试相关系数"""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        # 完全正相关
        self.assertAlmostEqual(correlation(x, y), 1.0, places=5)
        # 完全负相关
        self.assertAlmostEqual(correlation(x, [10, 8, 6, 4, 2]), -1.0, places=5)
    
    def test_percentile(self):
        """测试百分位数"""
        data = list(range(1, 101))
        self.assertEqual(percentile(data, 0), 1)
        self.assertEqual(percentile(data, 100), 100)
        self.assertAlmostEqual(percentile(data, 50), 50.5, places=1)
    
    def test_quartiles(self):
        """测试四分位数"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        q1, q2, q3 = quartiles(data)
        self.assertAlmostEqual(q1, 3.25, places=1)
        self.assertAlmostEqual(q2, 5.5, places=1)
        self.assertAlmostEqual(q3, 7.75, places=1)
    
    def test_iqr(self):
        """测试四分位距"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        iqr_val = iqr(data)
        self.assertAlmostEqual(iqr_val, 4.5, places=1)
    
    def test_describe(self):
        """测试描述性统计"""
        stats = describe([1, 2, 3, 4, 5])
        self.assertEqual(stats['count'], 5)
        self.assertEqual(stats['mean'], 3.0)
        self.assertEqual(stats['min'], 1)
        self.assertEqual(stats['max'], 5)


class TestNormalDistribution(unittest.TestCase):
    """测试正态分布"""
    
    def test_normal_pdf(self):
        """测试正态分布 PDF"""
        # 标准正态分布在 x=0 处
        self.assertAlmostEqual(normal_pdf(0, 0, 1), 1/math.sqrt(2*math.pi), places=5)
        # 对称性
        self.assertAlmostEqual(normal_pdf(1), normal_pdf(-1), places=5)
    
    def test_normal_cdf(self):
        """测试正态分布 CDF"""
        # 标准正态分布的性质
        self.assertAlmostEqual(normal_cdf(0), 0.5, places=5)
        self.assertAlmostEqual(normal_cdf(1.96), 0.975, places=2)
        self.assertAlmostEqual(normal_cdf(-1.96), 0.025, places=2)
    
    def test_normal_inv(self):
        """测试正态分布逆 CDF"""
        # 标准正态分布的分位数
        self.assertAlmostEqual(normal_inv(0.5), 0, places=5)
        self.assertAlmostEqual(normal_inv(0.975), 1.96, places=2)
        self.assertAlmostEqual(normal_inv(0.025), -1.96, places=2)
    
    def test_normal_roundtrip(self):
        """测试正态分布 CDF 和逆 CDF 的往返"""
        for p in [0.1, 0.25, 0.5, 0.75, 0.9]:
            x = normal_inv(p)
            self.assertAlmostEqual(normal_cdf(x), p, places=3)


class TestDiscreteDistributions(unittest.TestCase):
    """测试离散分布"""
    
    def test_binomial_pmf(self):
        """测试二项分布 PMF"""
        # 验证总和为 1
        n, p = 10, 0.5
        total = sum(binomial_pmf(k, n, p) for k in range(n + 1))
        self.assertAlmostEqual(total, 1.0, places=5)
        # 已知值
        self.assertAlmostEqual(binomial_pmf(5, 10, 0.5), 0.246, places=2)
    
    def test_binomial_cdf(self):
        """测试二项分布 CDF"""
        # CDF 最终应为 1
        self.assertAlmostEqual(binomial_cdf(10, 10, 0.5), 1.0, places=5)
    
    def test_poisson_pmf(self):
        """测试泊松分布 PMF"""
        # 验证总和接近 1
        lam = 3.0
        total = sum(poisson_pmf(k, lam) for k in range(100))
        self.assertAlmostEqual(total, 1.0, places=5)
        # 已知值
        self.assertAlmostEqual(poisson_pmf(0, 1), math.exp(-1), places=5)
    
    def test_poisson_cdf(self):
        """测试泊松分布 CDF"""
        self.assertAlmostEqual(poisson_cdf(10, 3), 0.9997, places=3)
    
    def test_geometric_pmf(self):
        """测试几何分布 PMF"""
        p = 0.3
        # 验证总和接近 1
        total = sum(geometric_pmf(k, p) for k in range(1, 1000))
        self.assertAlmostEqual(total, 1.0, places=5)
    
    def test_geometric_cdf(self):
        """测试几何分布 CDF"""
        self.assertAlmostEqual(geometric_cdf(1, 0.5), 0.5, places=5)
        self.assertAlmostEqual(geometric_cdf(2, 0.5), 0.75, places=5)
    
    def test_hypergeometric_pmf(self):
        """测试超几何分布 PMF"""
        # 经典例子：从52张牌中抽5张，恰好2张红桃
        pmf = hypergeometric_pmf(2, 52, 13, 5)
        self.assertTrue(0 < pmf < 1)


class TestContinuousDistributions(unittest.TestCase):
    """测试连续分布"""
    
    def test_exponential_pdf(self):
        """测试指数分布 PDF"""
        # 在 x=0 处
        self.assertEqual(exponential_pdf(0, 1), 1.0)
        # 负值应为 0
        self.assertEqual(exponential_pdf(-1, 1), 0.0)
    
    def test_exponential_cdf(self):
        """测试指数分布 CDF"""
        # 指数分布的特殊性质
        self.assertAlmostEqual(exponential_cdf(0, 1), 0.0, places=5)
        self.assertAlmostEqual(exponential_cdf(1, 1), 1 - math.exp(-1), places=5)


class TestBayes(unittest.TestCase):
    """测试贝叶斯定理"""
    
    def test_conditional_probability(self):
        """测试条件概率"""
        p = conditional_probability(0.3, 0.5)
        self.assertEqual(p, 0.6)
    
    def test_bayes_theorem(self):
        """测试贝叶斯定理"""
        # 医学测试示例
        p_disease = 0.01
        p_positive_given_disease = 0.99
        p_positive_given_healthy = 0.05
        p_positive = p_positive_given_disease * p_disease + \
                     p_positive_given_healthy * (1 - p_disease)
        
        result = bayes_theorem(p_positive_given_disease, p_disease, p_positive)
        # 结果应该在合理范围内
        self.assertTrue(0 < result < 1)
    
    def test_bayes_theorem_multiple(self):
        """测试多假设贝叶斯"""
        # 三个假设的例子
        hypotheses = [(0.6, 0.3), (0.3, 0.5), (0.1, 0.2)]
        result = bayes_theorem_multiple(0.5, 0.3, hypotheses)
        self.assertTrue(0 < result < 1)


class TestSampling(unittest.TestCase):
    """测试采样函数"""
    
    def test_weighted_choice(self):
        """测试加权选择"""
        items = ['a', 'b', 'c']
        weights = [1, 2, 7]
        
        # 多次测试统计
        counts = {item: 0 for item in items}
        random.seed(42)
        for _ in range(10000):
            result = weighted_choice(items, weights)
            counts[result] += 1
        
        # 检查大致比例
        self.assertTrue(counts['c'] > counts['b'] > counts['a'])
    
    def test_sample_without_replacement(self):
        """测试无放回抽样"""
        population = list(range(100))
        sample = sample_without_replacement(population, 10)
        
        self.assertEqual(len(sample), 10)
        self.assertEqual(len(set(sample)), 10)  # 无重复
    
    def test_rejection_sampling(self):
        """测试拒绝采样"""
        # 从标准正态分布采样
        samples = rejection_sampling(
            lambda x: math.exp(-x*x/2) / math.sqrt(2*math.pi),
            -5, 5, 0.5, n_samples=1000
        )
        
        self.assertEqual(len(samples), 1000)
        # 样本应该在合理范围内
        self.assertTrue(-5 < mean(samples) < 5)


class TestStatisticalTests(unittest.TestCase):
    """测试统计检验"""
    
    def test_z_score(self):
        """测试 Z 分数"""
        self.assertEqual(z_score(100, 100, 15), 0)
        self.assertEqual(z_score(115, 100, 15), 1)
        self.assertEqual(z_score(85, 100, 15), -1)
    
    def test_z_test(self):
        """测试 Z 检验"""
        # 样本均值显著高于总体均值
        z, p = z_test(110, 100, 15, 100)
        self.assertTrue(z > 0)
        self.assertTrue(0 < p < 1)
    
    def test_confidence_interval(self):
        """测试置信区间"""
        lower, upper = confidence_interval(100, 15, 100, 0.95)
        self.assertTrue(lower < 100 < upper)
        # 99% 区间应更宽
        lower_99, upper_99 = confidence_interval(100, 15, 100, 0.99)
        self.assertTrue((upper_99 - lower_99) > (upper - lower))


class TestInformationTheory(unittest.TestCase):
    """测试信息论函数"""
    
    def test_entropy(self):
        """测试熵"""
        # 公平硬币的熵
        h = entropy([0.5, 0.5])
        self.assertAlmostEqual(h, 1.0, places=5)
        
        # 确定性事件的熵为 0
        h = entropy([1.0, 0.0])
        self.assertAlmostEqual(h, 0.0, places=5)
        
        # 更多不确定性 -> 更高熵
        h1 = entropy([0.9, 0.1])
        h2 = entropy([0.5, 0.5])
        self.assertTrue(h1 < h2)
    
    def test_kl_divergence(self):
        """测试 KL 散度"""
        p = [0.5, 0.5]
        q = [0.5, 0.5]
        # 相同分布的 KL 散度为 0
        self.assertAlmostEqual(kl_divergence(p, q), 0.0, places=5)
        
        # KL 散度非对称
        p = [0.8, 0.2]
        q = [0.5, 0.5]
        kl1 = kl_divergence(p, q)
        kl2 = kl_divergence(q, p)
        self.assertNotAlmostEqual(kl1, kl2, places=5)
    
    def test_mutual_information(self):
        """测试互信息"""
        # 独立变量的互信息为 0
        joint = [[0.25, 0.25], [0.25, 0.25]]
        mi = mutual_information(joint)
        self.assertAlmostEqual(mi, 0.0, places=5)
        
        # 完全相关的变量互信息 = 熵
        joint = [[0.5, 0], [0, 0.5]]
        mi = mutual_information(joint)
        self.assertAlmostEqual(mi, 1.0, places=5)


class TestUtilityFunctions(unittest.TestCase):
    """测试实用工具函数"""
    
    def test_probability_of_at_least_one(self):
        """测试至少一个发生的概率"""
        # 两个独立事件，各 50% 概率
        p = probability_of_at_least_one([0.5, 0.5])
        self.assertAlmostEqual(p, 0.75, places=5)
        
        # 空列表
        self.assertEqual(probability_of_at_least_one([]), 0.0)
        
        # 必然事件
        self.assertEqual(probability_of_at_least_one([1.0]), 1.0)
    
    def test_probability_of_all(self):
        """测试全部发生的概率"""
        # 两个独立事件
        p = probability_of_all([0.5, 0.5])
        self.assertAlmostEqual(p, 0.25, places=5)
        
        # 空列表
        self.assertEqual(probability_of_all([]), 0.0)
        
        # 必然事件
        self.assertEqual(probability_of_all([1.0, 1.0]), 1.0)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_data(self):
        """测试空数据"""
        with self.assertRaises(ValueError):
            mean([])
        with self.assertRaises(ValueError):
            median([])
        with self.assertRaises(ValueError):
            variance([])
    
    def test_invalid_probabilities(self):
        """测试无效概率"""
        with self.assertRaises(ValueError):
            binomial_pmf(5, 10, 1.5)  # p > 1
        with self.assertRaises(ValueError):
            binomial_pmf(5, 10, -0.1)  # p < 0
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            normal_pdf(0, 0, -1)  # 负标准差
        with self.assertRaises(ValueError):
            confidence_interval(100, -15, 100)  # 负标准差


if __name__ == '__main__':
    unittest.main(verbosity=2)