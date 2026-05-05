"""
Bayesian Estimator Utils 使用示例

展示贝叶斯估计器在各种场景下的应用。
"""

import sys
import os

# 添加 Python 目录到路径
python_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, python_dir)

# 导入模块（添加 bayesian_estimator_utils 目录）
module_dir = os.path.join(python_dir, 'bayesian_estimator_utils')
sys.path.insert(0, module_dir)

from mod import (
    BetaDistribution,
    NormalDistribution,
    PoissonDistribution,
    BayesianEstimator,
    BayesianAverage,
    NaiveBayesClassifier,
    ABTestBayesian,
    beta_estimate,
    normal_estimate,
    poisson_estimate,
    create_classifier,
    create_ab_test,
    create_bayesian_average,
)


def example_beta_distribution():
    """示例1: Beta 分布用于概率估计"""
    print("\n" + "=" * 50)
    print("示例1: Beta 分布 - 概率估计")
    print("=" * 50)
    
    # 场景: 网站转化率估计
    # 观测: 1000 次访问，100 次转化
    
    print("\n场景: 电商网站转化率分析")
    print("-" * 40)
    
    # 使用 Beta 分布估计转化率
    bd = BetaDistribution(alpha=101, beta=901)  # 1 + 100, 1 + 900
    
    print(f"观测数据: 1000 次访问，100 次转化")
    print(f"\n贝叶斯估计结果:")
    print(f"  估计转化率: {bd.mean:.3f} ({bd.mean:.1%})")
    print(f"  标准差: {bd.std_dev:.4f}")
    print(f"  95% 可信区间: [{bd.credible_interval(0.95)[0]:.3f}, {bd.credible_interval(0.95)[1]:.3f}]")
    
    # 添加更多观测
    print(f"\n更新: 又有 50 次转化，450 次未转化")
    bd_updated = bd.update(50, 450)
    print(f"  新估计: {bd_updated.mean:.3f} ({bd_updated.mean:.1%})")
    
    # 概率超过某个阈值的计算
    threshold = 0.1
    prob_above = 1 - bd.cdf_approx(threshold)
    print(f"\n转化率超过 {threshold:.1%} 的概率: ~{prob_above:.1%}")
    
    # 采样示例
    samples = bd.sample(10)
    print(f"10 个随机样本: {[f'{s:.3f}' for s in samples[:5]]}")


def example_ab_test():
    """示例2: 贝叶斯 A/B 测试"""
    print("\n" + "=" * 50)
    print("示例2: 贝叶斯 A/B 测试")
    print("=" * 50)
    
    print("\n场景: 两个网页设计的转化率对比")
    print("-" * 40)
    
    ab = create_ab_test()
    
    # 版本 A: 1000 次访问，80 次转化
    # 版本 B: 1000 次访问，100 次转化
    ab.add_result('A', successes=80, failures=920)
    ab.add_result('B', successes=100, failures=900)
    
    print(f"版本 A: 1000 次访问 → 80 次转化 (8%)")
    print(f"版本 B: 1000 次访问 → 100 次转化 (10%)")
    
    print(f"\n贝叶斯分析结果:")
    print(f"  A 的估计率: {ab.get_rate_estimate('A'):.1%}")
    print(f"  B 的估计率: {ab.get_rate_estimate('B'):.1%}")
    
    # B 比 A 好的概率
    prob_b_better = ab.probability_b_better(n_samples=10000)
    print(f"\n  B 比 A 好的概率: {prob_b_better:.1%}")
    
    # 期望损失
    loss_if_choose_a = ab.expected_loss('A', 'B', n_samples=10000)
    loss_if_choose_b = ab.expected_loss('B', 'A', n_samples=10000)
    
    print(f"\n  选择 A 的期望损失: {loss_if_choose_a:.3f}")
    print(f"  选择 B 的期望损失: {loss_if_choose_b:.3f}")
    
    # 推荐决策
    rec = ab.recommend(threshold=0.90)
    print(f"\n决策建议:")
    print(f"  推荐: {rec['recommendation'] or '继续测试'}")
    print(f"  置信度: {rec['confidence']:.1%}")
    
    # 如果置信度不够高，建议继续测试
    if rec['confidence'] < 0.90:
        print(f"  提示: 置信度不足 90%，建议继续收集数据")
    
    # 更多数据后的分析
    print("\n增加数据后的分析:")
    ab2 = create_ab_test()
    ab2.add_result('A', successes=800, failures=9200)
    ab2.add_result('B', successes=1000, failures=9000)
    
    prob_b_better2 = ab2.probability_b_better()
    print(f"  A: 10000 次访问 → 800 转化 (8%)")
    print(f"  B: 10000 次访问 → 1000 转化 (10%)")
    print(f"  B 比 A 好的概率: {prob_b_better2:.1%}")
    
    rec2 = ab2.recommend()
    print(f"  推荐: {rec2['recommendation']} (置信度: {rec2['confidence']:.1%})")


def example_bayesian_average():
    """示例3: 贝叶斯平均评分系统"""
    print("\n" + "=" * 50)
    print("示例3: 贝叶斯平均 - 评分系统")
    print("=" * 50)
    
    print("\n场景: 电影评分排名系统")
    print("-" * 40)
    
    # 设置: 全局平均 3.5，先验权重 25（相当于至少 25 个评分）
    ba = create_bayesian_average(global_mean=3.5, prior_weight=25)
    
    # 添加电影评分
    movies = {
        "经典大片": [5, 5, 5, 4, 5, 5, 4, 5, 5, 4,  # 100 个评分
                    5, 4, 5, 5, 4, 5, 5, 5, 4, 5,
                    5, 5, 4, 5, 5, 5, 5, 4, 5, 5,
                    5, 5, 5, 4, 5, 5, 5, 4, 5, 5,
                    5, 5, 4, 5, 5, 5, 5, 5, 4, 5,
                    5, 4, 5, 5, 5, 4, 5, 5, 5, 5,
                    5, 5, 5, 4, 5, 5, 4, 5, 5, 5,
                    5, 4, 5, 5, 5, 5, 4, 5, 5, 5,
                    5, 5, 5, 4, 5, 5, 5, 5, 4, 5,
                    5, 5, 4, 5, 5, 5, 5, 5, 4, 5],
        "新上映电影": [5, 5],  # 只有 2 个评分
        "冷门佳作": [4, 4, 5, 5, 4, 5],  # 6 个评分
        "争议电影": [1, 5, 1, 5, 1, 5, 1, 5],  # 极端评分
    }
    
    for movie, ratings in movies.items():
        ba.add_item(movie, ratings)
    
    print("\n评分对比:")
    print(f"{'电影':<15} {'评分数':<10} {'普通平均':<10} {'贝叶斯平均':<10}")
    print("-" * 50)
    
    for movie in ba.get_all_items():
        avg = ba.get_average(movie)
        bayes_avg = ba.get_bayesian_average(movie)
        count = ba.get_item_count(movie)
        print(f"{movie:<15} {count:<10} {avg:.2f}       {bayes_avg:.2f}")
    
    # 贝叶斯排名
    print("\n贝叶斯平均排名:")
    for rank, (movie, score) in enumerate(ba.rank_items(), 1):
        print(f"  #{rank}: {movie} ({score:.2f})")
    
    # 普通平均排名对比
    print("\n普通平均排名:")
    for rank, (movie, score) in enumerate(ba.rank_items(use_bayesian=False), 1):
        print(f"  #{rank}: {movie} ({score:.2f})")
    
    print("\n说明:")
    print("  - 新上映电影只有 2 个评分，贝叶斯平均向全局平均收缩")
    print("  - 经典大片评分数量多，贝叶斯平均接近实际平均")
    print("  - 贝叶斯平均避免了小样本极端评分的问题")


def example_naive_bayes_classifier():
    """示例4: 朴素贝叶斯文本分类"""
    print("\n" + "=" * 50)
    print("示例4: 朴素贝叶斯 - 文本分类")
    print("=" * 50)
    
    print("\n场景: 邮件垃圾分类")
    print("-" * 40)
    
    clf = create_classifier(smoothing=1.0)
    
    # 训练数据（使用词频）
    spam_words = [
        ["free", "money", "click", "now", "offer"],
        ["limited", "time", "act", "fast", "discount"],
        ["buy", "cheap", "deal", "save", "cash"],
        ["subscribe", "urgent", "prize", "winner", "claim"],
    ]
    
    normal_words = [
        ["meeting", "schedule", "project", "team", "update"],
        ["hello", "thanks", "regards", "question", "help"],
        ["report", "analysis", "data", "summary", "review"],
        ["document", "file", "attached", "please", "find"],
    ]
    
    for words in spam_words:
        clf.train("spam", words)
    
    for words in normal_words:
        clf.train("normal", words)
    
    print(f"训练完成: {clf._total_docs} 个样本")
    print(f"词汇表大小: {clf.get_vocab_size()}")
    
    # 测试分类
    test_emails = [
        ["free", "offer", "click", "limited"],
        ["meeting", "schedule", "team", "project"],
        ["buy", "cheap", "discount", "save"],
        ["hello", "question", "help", "thanks"],
        ["urgent", "prize", "winner", "claim"],
    ]
    
    print("\n分类测试:")
    for i, words in enumerate(test_emails, 1):
        probs = clf.predict(words)
        label = clf.predict_label(words)
        print(f"  邮件 {i}: {words}")
        print(f"    分类: {label} (spam={probs['spam']:.2f}, normal={probs['normal']:.2f})")
    
    # 重要特征分析
    print("\n各类别最重要的特征:")
    for cls in clf.get_classes():
        top_features = clf.get_top_features(cls, top_n=5)
        print(f"  {cls}: {[f'{f}({p:.2f})' for f, p in top_features]}")
    
    # 混合特征示例（词频 + 连续特征）
    print("\n混合特征分类示例:")
    print("-" * 40)
    
    clf2 = create_classifier()
    
    # 邮件特征：词频 + 链接数量 + 文件大小
    clf2.train("spam", {"free": 3, "click": 2, "links": 5, "attachments": 2.5})
    clf2.train("spam", {"money": 2, "urgent": 1, "links": 8, "attachments": 1.0})
    clf2.train("normal", {"meeting": 1, "project": 2, "links": 1, "attachments": 5.0})
    clf2.train("normal", {"hello": 1, "document": 2, "links": 0, "attachments": 10.0})
    
    # 预测
    test_features = {"free": 1, "click": 1, "links": 6, "attachments": 2}
    probs = clf2.predict(test_features)
    label = clf2.predict_label(test_features)
    
    print(f"测试邮件特征: {test_features}")
    print(f"分类: {label} (spam={probs['spam']:.2f}, normal={probs['normal']:.2f})")


def example_normal_estimation():
    """示例5: 正态分布参数估计"""
    print("\n" + "=" * 50)
    print("示例5: 正态分布估计 - 测量数据分析")
    print("=" * 50)
    
    print("\n场景: 产品质量测量")
    print("-" * 40)
    
    # 测量数据（产品尺寸）
    measurements = [
        25.1, 25.3, 24.9, 25.0, 25.2,
        25.1, 24.8, 25.4, 25.0, 25.2,
        25.3, 24.9, 25.1, 25.0, 25.2,
    ]
    
    result = normal_estimate(measurements, 0.95)
    
    print(f"测量数据: {len(measurements)} 个样本")
    print(f"原始数据: {measurements[:5]} ...")
    
    print(f"\n贝叶斯估计:")
    print(f"  均值估计: {result.estimate:.2f} mm")
    print(f"  95% 可信区间: [{result.lower_bound:.2f}, {result.upper_bound:.2f}] mm")
    
    # 分布对象
    nd = result.distribution
    print(f"\n分布参数:")
    print(f"  μ = {nd.mu:.2f}")
    print(f"  σ = {nd.sigma:.3f}")
    
    # 新测量更新
    estimator = BayesianEstimator()
    estimator.update_normal(measurements)
    
    print("\n增量更新:")
    new_measurements = [25.5, 25.6, 25.3]
    estimator.update_normal(new_measurements)
    
    new_result = estimator.normal_estimate(0.95)
    print(f"  添加 3 个新测量后:")
    print(f"  新均值: {new_result.estimate:.2f} mm")
    print(f"  新可信区间: [{new_result.lower_bound:.2f}, {new_result.upper_bound:.2f}] mm")
    
    # 概率计算
    print(f"\n概率计算:")
    prob_within_spec = nd.cdf(25.5) - nd.cdf(24.5)
    print(f"  在规格 [24.5, 25.5] 范围内的概率: {prob_within_spec:.1%}")


def example_poisson_estimation():
    """示例6: 泊松分布计数估计"""
    print("\n" + "=" * 50)
    print("示例6: 泊松分布估计 - 流量分析")
    print("=" * 50)
    
    print("\n场景: 网站每小时访问量估计")
    print("-" * 40)
    
    # 每小时访问量数据
    hourly_visits = [45, 52, 48, 55, 49, 51, 47, 53, 50, 48, 56, 44]
    
    result = poisson_estimate(hourly_visits)
    
    print(f"观测数据: 12 小时的访问量")
    print(f"数据: {hourly_visits}")
    
    print(f"\n贝叶斯估计:")
    print(f"  λ 估计: {result.estimate:.1f} 次/小时")
    print(f"  95% 可信区间: [{result.lower_bound:.1f}, {result.upper_bound:.1f}]")
    
    # 泊松分布对象
    pd = result.distribution
    
    print(f"\n概率计算:")
    print(f"  P(X ≥ 60) = {1 - pd.cdf(59):.2%}")
    print(f"  P(X ≤ 40) = {pd.cdf(40):.2%}")
    
    # 概率质量函数示例
    print(f"\n概率质量函数示例:")
    for k in [40, 50, 60]:
        print(f"  P(X = {k}) = {pd.pmf(k):.3f}")
    
    # 采样
    samples = pd.sample(10)
    print(f"\n10 个随机样本: {samples}")


def example_online_learning():
    """示例7: 在线贝叶斯学习"""
    print("\n" + "=" * 50)
    print("示例7: 在线贝叶斯学习")
    print("=" * 50)
    
    print("\n场景: 实时概率更新")
    print("-" * 40)
    
    estimator = BayesianEstimator()
    
    print("模拟实时数据流:")
    print("  初始状态: 均匀先验 (α=1, β=1)")
    
    # 模拟数据流
    data_stream = [
        (1, 0),  # 成功
        (1, 0),
        (0, 1),  # 失败
        (1, 0),
        (1, 0),
        (0, 1),
        (1, 0),
        (1, 0),
    ]
    
    total_success = 0
    total_failure = 0
    
    for i, (s, f) in enumerate(data_stream):
        estimator.update_beta(s, f)
        total_success += s
        total_failure += f
        
        print(f"\n  步骤 {i+1}: 成功={s}, 失败={f}")
        print(f"    累计: {total_success} 成功, {total_failure} 失败")
        print(f"    估计概率: {estimator.beta_mean():.3f}")
        print(f"    95% CI: [{estimator.beta_credible_interval(0.95)[0]:.3f}, "
              f"{estimator.beta_credible_interval(0.95)[1]:.3f}]")
    
    print("\n最终估计:")
    final = estimator.beta_estimate(0.95)
    print(f"  估计: {final.estimate:.3f}")
    print(f"  可信区间: [{final.lower_bound:.3f}, {final.upper_bound:.3f}]")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Bayesian Estimator Utils - 使用示例")
    print("=" * 60)
    
    example_beta_distribution()
    example_ab_test()
    example_bayesian_average()
    example_naive_bayes_classifier()
    example_normal_estimation()
    example_poisson_estimation()
    example_online_learning()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()