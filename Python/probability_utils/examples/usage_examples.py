"""
probability_utils 使用示例

本文件演示概率计算工具的常见应用场景：
1. 组合数学问题
2. 描述性统计分析
3. 概率分布计算
4. 贝叶斯推断
5. 统计检验
6. 信息论应用
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # 基础数学
    factorial, permutation, combination, gcd, lcm,
    # 统计函数
    mean, median, mode, variance, std_dev, describe,
    covariance, correlation, percentile, quartiles, iqr,
    skewness, kurtosis,
    # 概率分布
    normal_pdf, normal_cdf, normal_inv,
    binomial_pmf, binomial_cdf,
    poisson_pmf, poisson_cdf,
    exponential_pdf, exponential_cdf,
    geometric_pmf, geometric_cdf,
    hypergeometric_pmf,
    negative_binomial_pmf,
    # 贝叶斯
    conditional_probability, bayes_theorem,
    # 随机采样
    weighted_choice, sample_without_replacement,
    # 统计检验
    z_score, z_test, confidence_interval,
    # 信息论
    entropy, kl_divergence, mutual_information,
    # 实用工具
    probability_of_at_least_one, probability_of_all
)


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def example_combinatorics():
    """组合数学示例"""
    print_section("组合数学")
    
    # 彩票中奖概率
    print("\n【彩票中奖概率】")
    # 假设彩票从 49 个号码中选 6 个
    total_tickets = combination(49, 6)
    print(f"从 49 个号码中选 6 个的组合数: {total_tickets:,}")
    print(f"中头奖的概率: 1 / {total_tickets:,} = {1/total_tickets:.10f}")
    
    # 排列问题
    print("\n【排列问题】")
    print(f"10 个人站成一排的方法数: {permutation(10, 10):,}")
    print(f"10 个人中选 3 个人排队的方法数: {permutation(10, 3):,}")
    
    # 阶乘应用
    print("\n【阶乘应用】")
    print(f"52 张牌的排列方式: 52! = {factorial(52):,}")
    
    # GCD/LCM
    print("\n【最大公约数与最小公倍数】")
    print(f"gcd(48, 18) = {gcd(48, 18)}")
    print(f"lcm(12, 18) = {lcm(12, 18)}")


def example_descriptive_stats():
    """描述性统计示例"""
    print_section("描述性统计")
    
    # 学生成绩数据
    scores = [78, 85, 92, 88, 76, 95, 89, 72, 83, 91, 87, 79, 84, 90, 82]
    
    print("\n【学生成绩分析】")
    print(f"数据: {scores}")
    
    stats = describe(scores)
    print(f"\n统计摘要:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    # 四分位数分析
    q1, q2, q3 = quartiles(scores)
    print(f"\n四分位数分析:")
    print(f"  Q1 (25%): {q1:.2f}")
    print(f"  Q2 (50%): {q2:.2f}")
    print(f"  Q3 (75%): {q3:.2f}")
    print(f"  IQR: {iqr(scores):.2f}")
    
    # 相关性分析
    print("\n【相关性分析】")
    study_hours = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    test_scores = [60, 65, 70, 75, 80, 82, 85, 88, 92, 95]
    
    corr = correlation(study_hours, test_scores)
    print(f"学习时长与考试成绩的相关系数: {corr:.4f}")
    
    cov = covariance(study_hours, test_scores)
    print(f"协方差: {cov:.2f}")


def example_probability_distributions():
    """概率分布示例"""
    print_section("概率分布")
    
    # 正态分布
    print("\n【正态分布】")
    mu, sigma = 100, 15  # IQ 分数
    print(f"IQ 分布 (μ={mu}, σ={sigma}):")
    print(f"  P(X < 85) = {normal_cdf(85, mu, sigma):.4f}")
    print(f"  P(X > 130) = {1 - normal_cdf(130, mu, sigma):.4f}")
    print(f"  P(90 < X < 110) = {normal_cdf(110, mu, sigma) - normal_cdf(90, mu, sigma):.4f}")
    print(f"  95% 分位点: {normal_inv(0.95, mu, sigma):.2f}")
    print(f"  99% 分位点: {normal_inv(0.99, mu, sigma):.2f}")
    
    # 二项分布
    print("\n【二项分布】")
    n, p = 20, 0.6  # 20 道题，每题 60% 正确率
    print(f"考试问题 (n={n}, p={p}):")
    print(f"  恰好答对 12 题的概率: {binomial_pmf(12, n, p):.4f}")
    print(f"  至少答对 15 题的概率: {1 - binomial_cdf(14, n, p):.4f}")
    print(f"  答对 10 题或更少的概率: {binomial_cdf(10, n, p):.4f}")
    
    # 泊松分布
    print("\n【泊松分布】")
    lam = 5  # 平均每小时 5 个顾客
    print(f"客服中心 (λ={lam} 顾客/小时):")
    print(f"  一小时内恰好 3 个顾客的概率: {poisson_pmf(3, lam):.4f}")
    print(f"  一小时内 0-5 个顾客的概率: {poisson_cdf(5, lam):.4f}")
    print(f"  一小时内超过 8 个顾客的概率: {1 - poisson_cdf(8, lam):.4f}")
    
    # 指数分布
    print("\n【指数分布】")
    lam = 0.5  # 平均等待 2 小时
    print(f"设备故障 (λ={lam}, 平均故障间隔 {1/lam} 小时):")
    print(f"  1 小时内发生故障的概率: {exponential_cdf(1, lam):.4f}")
    print(f"  4 小时内发生故障的概率: {exponential_cdf(4, lam):.4f}")
    print(f"  超过 6 小时才故障的概率: {1 - exponential_cdf(6, lam):.4f}")
    
    # 几何分布
    print("\n【几何分布】")
    p = 0.3  # 成功概率 30%
    print(f"销售转化 (p={p}):")
    print(f"  第 1 次就成功的概率: {geometric_pmf(1, p):.4f}")
    print(f"  第 3 次才成功的概率: {geometric_pmf(3, p):.4f}")
    print(f"  5 次内成功的概率: {geometric_cdf(5, p):.4f}")
    
    # 超几何分布
    print("\n【超几何分布】")
    # 从 52 张牌中抽 5 张
    hearts = hypergeometric_pmf(2, 52, 13, 5)
    print(f"从 52 张牌中抽 5 张:")
    print(f"  恰好 2 张红桃的概率: {hearts:.4f}")
    
    # 负二项分布
    print("\n【负二项分布】")
    r, p = 3, 0.4  # 要得到 3 次成功
    print(f"游戏掉落 (r={r}, p={p}):")
    print(f"  恰好 5 次获得 3 个掉落物的概率: {negative_binomial_pmf(5, r, p):.4f}")
    print(f"  恰好 10 次获得 3 个掉落物的概率: {negative_binomial_pmf(10, r, p):.4f}")


def example_bayesian_inference():
    """贝叶斯推断示例"""
    print_section("贝叶斯推断")
    
    # 医学诊断示例
    print("\n【医学诊断 - 罕见疾病检测】")
    prevalence = 0.001  # 患病率 0.1%
    sensitivity = 0.99  # 灵敏度 99%
    specificity = 0.95  # 特异度 95%
    
    print(f"患病率: {prevalence:.1%}")
    print(f"检测灵敏度 (真阳性率): {sensitivity:.1%}")
    print(f"检测特异度: {specificity:.1%}")
    
    # 计算 P(阳性)
    p_positive = sensitivity * prevalence + (1 - specificity) * (1 - prevalence)
    
    # 贝叶斯定理
    p_disease_given_positive = bayes_theorem(sensitivity, prevalence, p_positive)
    
    print(f"\nP(测试阳性): {p_positive:.4f}")
    print(f"P(患病 | 测试阳性): {p_disease_given_positive:.2%}")
    print("\n解读: 即使测试为阳性，实际患病的概率只有约 2%，")
    print("      这是因为疾病非常罕见。需要进一步确认。")
    
    # 垃圾邮件过滤示例
    print("\n【垃圾邮件过滤】")
    p_spam = 0.3  # 30% 的邮件是垃圾邮件
    p_word_spam = 0.8  # 垃圾邮件中包含某词的概率
    p_word_ham = 0.1   # 正常邮件中包含该词的概率
    
    p_word = p_word_spam * p_spam + p_word_ham * (1 - p_spam)
    p_spam_given_word = bayes_theorem(p_word_spam, p_spam, p_word)
    
    print(f"P(垃圾邮件): {p_spam:.1%}")
    print(f"P(词 | 垃圾邮件): {p_word_spam:.1%}")
    print(f"P(词 | 正常邮件): {p_word_ham:.1%}")
    print(f"\n如果邮件包含该词，是垃圾邮件的概率: {p_spam_given_word:.2%}")
    
    # 条件概率示例
    print("\n【条件概率】")
    p_a_and_b = 0.12
    p_b = 0.3
    p_a_given_b = conditional_probability(p_a_and_b, p_b)
    print(f"P(A ∩ B) = {p_a_and_b}")
    print(f"P(B) = {p_b}")
    print(f"P(A | B) = P(A ∩ B) / P(B) = {p_a_given_b:.2f}")


def example_statistical_tests():
    """统计检验示例"""
    print_section("统计检验")
    
    # Z 检验
    print("\n【Z 检验 - 产品质量】")
    population_mean = 100  # 标准均值
    population_std = 15
    sample_mean = 108
    sample_size = 50
    
    z, p = z_test(sample_mean, population_mean, population_std, sample_size)
    
    print(f"总体均值: {population_mean}")
    print(f"总体标准差: {population_std}")
    print(f"样本均值: {sample_mean}")
    print(f"样本大小: {sample_size}")
    print(f"\nZ 统计量: {z:.4f}")
    print(f"P 值 (双尾): {p:.4f}")
    
    if p < 0.05:
        print("结论: 样本均值与总体均值存在显著差异 (p < 0.05)")
    else:
        print("结论: 样本均值与总体均值无显著差异 (p >= 0.05)")
    
    # 置信区间
    print("\n【置信区间】")
    sample_mean = 50
    sample_std = 8
    sample_size = 25
    
    for confidence in [0.90, 0.95, 0.99]:
        lower, upper = confidence_interval(sample_mean, sample_std, sample_size, confidence)
        print(f"{confidence:.0%} 置信区间: [{lower:.2f}, {upper:.2f}]")
    
    # Z 分数
    print("\n【Z 分数 - 标准化比较】")
    scores = [
        ("数学", 85, 70, 10),
        ("英语", 78, 75, 8),
        ("物理", 92, 68, 15),
    ]
    
    print("各科成绩标准化比较:")
    for subject, score, mean_val, std_val in scores:
        z_val = z_score(score, mean_val, std_val)
        print(f"  {subject}: {score}分, Z={z_val:.2f}")


def example_information_theory():
    """信息论示例"""
    print_section("信息论")
    
    # 熵
    print("\n【信息熵】")
    print("衡量不确定性/信息量:")
    
    distributions = [
        ("公平硬币", [0.5, 0.5]),
        ("偏倚硬币 (90/10)", [0.9, 0.1]),
        ("极端偏倚 (99/1)", [0.99, 0.01]),
        ("确定性", [1.0, 0.0]),
        ("公平骰子", [1/6]*6),
    ]
    
    for name, probs in distributions:
        h = entropy(probs)
        print(f"  {name}: H = {h:.4f} 比特")
    
    print("\n解释: 不确定性越大，熵越高；确定性事件熵为 0")
    
    # KL 散度
    print("\n【KL 散度 - 分布距离】")
    p = [0.5, 0.5]
    q1 = [0.5, 0.5]
    q2 = [0.7, 0.3]
    q3 = [0.9, 0.1]
    
    print(f"真实分布 P = {p}")
    print(f"  D_KL(P||Q={q1}) = {kl_divergence(p, q1):.4f}")
    print(f"  D_KL(P||Q={q2}) = {kl_divergence(p, q2):.4f}")
    print(f"  D_KL(P||Q={q3}) = {kl_divergence(p, q3):.4f}")
    
    # 互信息
    print("\n【互信息 - 变量相关性】")
    
    # 独立
    joint_independent = [[0.25, 0.25], [0.25, 0.25]]
    print(f"独立变量: I(X;Y) = {mutual_information(joint_independent):.4f}")
    
    # 完全相关
    joint_correlated = [[0.5, 0], [0, 0.5]]
    print(f"完全相关: I(X;Y) = {mutual_information(joint_correlated):.4f}")
    
    # 部分相关
    joint_partial = [[0.3, 0.2], [0.2, 0.3]]
    print(f"部分相关: I(X;Y) = {mutual_information(joint_partial):.4f}")


def example_utility():
    """实用工具示例"""
    print_section("实用概率计算")
    
    # 至少一个发生的概率
    print("\n【至少一个发生的概率】")
    probs = [0.3, 0.4, 0.5]
    p_at_least_one = probability_of_at_least_one(probs)
    print(f"独立事件概率: {probs}")
    print(f"至少一个发生的概率: {p_at_least_one:.4f}")
    print(f"计算: 1 - (1-0.3)(1-0.4)(1-0.5) = 1 - 0.21 = 0.79")
    
    # 全部发生的概率
    print("\n【全部发生的概率】")
    p_all = probability_of_all(probs)
    print(f"全部发生的概率: {p_all:.4f}")
    print(f"计算: 0.3 × 0.4 × 0.5 = 0.06")
    
    # 加权随机选择
    print("\n【加权随机选择】")
    import random
    random.seed(42)
    
    items = ['A', 'B', 'C', 'D']
    weights = [10, 30, 40, 20]
    
    print(f"选项: {items}")
    print(f"权重: {weights}")
    
    # 模拟 1000 次选择
    counts = {item: 0 for item in items}
    for _ in range(1000):
        choice = weighted_choice(items, weights)
        counts[choice] += 1
    
    print("\n1000 次选择结果:")
    for item in items:
        expected = weights[items.index(item)] / sum(weights) * 100
        actual = counts[item] / 10
        print(f"  {item}: {counts[item]} 次 ({actual:.1f}%), 期望 {expected:.1f}%")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("  Probability Utils - 概率计算工具使用示例")
    print("=" * 60)
    
    example_combinatorics()
    example_descriptive_stats()
    example_probability_distributions()
    example_bayesian_inference()
    example_statistical_tests()
    example_information_theory()
    example_utility()
    
    print("\n" + "=" * 60)
    print("  示例运行完成！")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()