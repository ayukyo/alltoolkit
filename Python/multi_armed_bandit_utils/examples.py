"""
Multi-Armed Bandit 使用示例

本示例展示如何使用多臂老虎机算法解决实际问题：
1. A/B 测试优化
2. 推荐系统
3. 广告投放
4. 在线学习
"""

import random
from typing import List, Dict
from mod import (
    BanditAlgorithm,
    EpsilonGreedyBandit,
    UCB1Bandit,
    ThompsonSamplingBandit,
    SoftmaxBandit,
    ExponentialWeightBandit,
    create_bandit,
    BanditExperiment,
    quick_ab_test
)


def example_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("示例 1: 基本使用")
    print("=" * 60)
    
    # 创建一个简单的 Epsilon-Greedy bandit
    bandit = EpsilonGreedyBandit(
        arm_names=["选项A", "选项B", "选项C"],
        epsilon=0.1  # 10% 的时间探索
    )
    
    # 模拟 100 轮选择和奖励
    for i in range(100):
        # 选择一个臂
        arm = bandit.select()
        
        # 模拟奖励（假设各选项有不同的真实奖励概率）
        true_rewards = {"选项A": 0.3, "选项B": 0.7, "选项C": 0.5}
        reward = 1.0 if random.random() < true_rewards[arm] else 0.0
        
        # 更新 bandit
        bandit.update(arm, reward, is_binary=True)
    
    # 查看结果
    print(f"\n累计奖励: {bandit.cumulative_reward}")
    print(f"发现的最优选项: {bandit.get_best_arm()}")
    print("\n各选项统计:")
    for name, stats in bandit.get_all_stats().items():
        print(f"  {name}: 点击率 {stats['average_reward']:.2%}, "
              f"选择次数 {stats['pull_count']}")


def example_ab_testing():
    """A/B 测试示例"""
    print("\n" + "=" * 60)
    print("示例 2: A/B 测试优化")
    print("=" * 60)
    
    # 假设我们有三个网页设计版本
    variants = ["control", "variant_A", "variant_B"]
    
    # 创建 Thompson Sampling bandit（适合 A/B 测试）
    bandit = ThompsonSamplingBandit(variants, is_binary=True)
    
    # 模拟真实转化率
    true_conversion_rates = {
        "control": 0.10,
        "variant_A": 0.15,
        "variant_B": 0.08,
    }
    
    visits = 1000
    conversions = 0
    
    for _ in range(visits):
        # Bandit 选择展示哪个版本
        variant = bandit.select()
        
        # 模拟用户转化
        converted = random.random() < true_conversion_rates[variant]
        bandit.update(variant, 1.0 if converted else 0.0, is_binary=True)
        
        if converted:
            conversions += 1
    
    print(f"\n总访问: {visits}")
    print(f"总转化: {conversions}")
    print(f"转化率: {conversions/visits:.2%}")
    print(f"\n最佳版本: {bandit.get_best_arm()}")
    
    print("\n各版本详细数据:")
    for name, stats in bandit.get_all_stats().items():
        print(f"  {name}:")
        print(f"    - 展示次数: {stats['pull_count']}")
        print(f"    - 转化率: {stats['average_reward']:.2%}")
        print(f"    - 展示比例: {stats['selection_rate']:.2%}")


def example_recommendation_system():
    """推荐系统示例"""
    print("\n" + "=" * 60)
    print("示例 3: 推荐系统 - 内容推荐")
    print("=" * 60)
    
    # 假设有多个内容类别可以推荐
    content_categories = [
        "科技新闻",
        "娱乐八卦",
        "体育赛事",
        "财经资讯",
        "健康养生"
    ]
    
    # 使用 UCB1 算法
    bandit = UCB1Bandit(content_categories)
    
    # 模拟不同用户的点击偏好（用户对各类内容的兴趣不同）
    user_interests = {
        "科技新闻": 0.6,
        "娱乐八卦": 0.4,
        "体育赛事": 0.5,
        "财经资讯": 0.3,
        "健康养生": 0.2,
    }
    
    # 模拟 500 次推荐
    clicks = 0
    recommendations = {cat: 0 for cat in content_categories}
    
    for _ in range(500):
        # 选择推荐内容
        category = bandit.select()
        recommendations[category] += 1
        
        # 模拟用户点击
        clicked = random.random() < user_interests[category]
        bandit.update(category, 1.0 if clicked else 0.0)
        
        if clicked:
            clicks += 1
    
    print(f"\n总推荐: 500")
    print(f"总点击: {clicks}")
    print(f"点击率: {clicks/500:.2%}")
    
    print("\n推荐分布:")
    for cat, count in sorted(recommendations.items(), 
                            key=lambda x: x[1], reverse=True):
        avg_reward = bandit.arms[cat].average_reward
        print(f"  {cat}: 推荐 {count} 次, 点击率 {avg_reward:.2%}")


def example_ad_placement():
    """广告投放优化示例"""
    print("\n" + "=" * 60)
    print("示例 4: 广告投放优化")
    print("=" * 60)
    
    # 多个广告位
    ad_slots = [
        "顶部横幅",
        "侧边栏",
        "内容中插入",
        "底部横幅",
        "弹窗"
    ]
    
    # 使用 Softmax 算法，温度随时间递减
    bandit = SoftmaxBandit(
        ad_slots,
        temperature=1.0,
        temperature_decay=0.995,
        min_temperature=0.1
    )
    
    # 各广告位的真实点击率
    true_ctrs = {
        "顶部横幅": 0.05,
        "侧边栏": 0.02,
        "内容中插入": 0.08,  # 最佳
        "底部横幅": 0.01,
        "弹窗": 0.03,
    }
    
    impressions = 2000
    total_clicks = 0
    revenue_per_click = 0.5  # 每次点击收入 $0.5
    
    for _ in range(impressions):
        slot = bandit.select()
        clicked = random.random() < true_ctrs[slot]
        bandit.update(slot, 1.0 if clicked else 0.0)
        
        if clicked:
            total_clicks += 1
    
    print(f"\n总展示: {impressions}")
    print(f"总点击: {total_clicks}")
    print(f"总收益: ${total_clicks * revenue_per_click:.2f}")
    print(f"整体 CTR: {total_clicks/impressions:.2%}")
    print(f"最优广告位: {bandit.get_best_arm()}")


def example_compare_algorithms():
    """比较不同算法"""
    print("\n" + "=" * 60)
    print("示例 5: 算法比较实验")
    print("=" * 60)
    
    # 真实奖励概率
    true_rewards = {
        "臂1": 0.2,
        "臂2": 0.5,
        "臂3": 0.8,  # 最佳
        "臂4": 0.4,
    }
    
    # 创建实验
    experiment = BanditExperiment(
        arm_names=list(true_rewards.keys()),
        true_rewards=true_rewards,
        algorithms=list(BanditAlgorithm)
    )
    
    # 运行实验
    results = experiment.run(rounds=2000, verbose=False)
    
    # 获取排名
    ranking = experiment.get_ranking()
    
    print("\n算法性能排名:")
    print("-" * 50)
    print(f"{'排名':<4} {'算法':<25} {'累计奖励':<12} {'最优臂'}")
    print("-" * 50)
    
    for i, (algo, data) in enumerate(ranking, 1):
        print(f"{i:<4} {algo:<25} {data['cumulative_reward']:<12.1f} "
              f"{data['best_arm_found']}")


def example_quick_ab_test():
    """快速 A/B 测试"""
    print("\n" + "=" * 60)
    print("示例 6: 快速 A/B 测试分析")
    print("=" * 60)
    
    # 假设我们已经收集了一些 A/B 测试数据
    historical_data = {
        "control": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
        "treatment_A": [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        "treatment_B": [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    }
    
    result = quick_ab_test(
        variant_names=["control", "treatment_A", "treatment_B"],
        rewards=historical_data,
        algorithm=BanditAlgorithm.THOMPSON_SAMPLING
    )
    
    print(f"\n使用算法: {result['algorithm']}")
    print(f"最优版本: {result['best_variant']}")
    print(f"累计奖励: {result['cumulative_reward']}")
    
    print("\n详细分析:")
    for name, stats in result['variant_stats'].items():
        print(f"  {name}:")
        print(f"    - 样本数: {stats['pull_count']}")
        print(f"    - 成功率: {stats['average_reward']:.2%}")


def example_dynamic_pricing():
    """动态定价示例"""
    print("\n" + "=" * 60)
    print("示例 7: 动态定价优化")
    print("=" * 60)
    
    # 不同价格点
    prices = ["$9.99", "$12.99", "$14.99", "$19.99"]
    
    # 使用 Thompson Sampling（适合二值结果）
    bandit = ThompsonSamplingBandit(prices, is_binary=True)
    
    # 各价格点的真实转化率（价格越高，转化越低，但利润更高）
    conversion_rates = {
        "$9.99": 0.15,
        "$12.99": 0.12,
        "$14.99": 0.08,
        "$19.99": 0.04,
    }
    
    # 利润计算
    profit_map = {
        "$9.99": 9.99 * 0.3,
        "$12.99": 12.99 * 0.3,
        "$14.99": 14.99 * 0.3,
        "$19.99": 19.99 * 0.3,
    }
    
    customers = 500
    total_profit = 0
    
    for _ in range(customers):
        price = bandit.select()
        purchased = random.random() < conversion_rates[price]
        bandit.update(price, 1.0 if purchased else 0.0, is_binary=True)
        
        if purchased:
            total_profit += profit_map[price]
    
    print(f"\n顾客数: {customers}")
    print(f"总利润: ${total_profit:.2f}")
    print(f"平均利润: ${total_profit/customers:.2f} 每顾客")
    print(f"最优定价: {bandit.get_best_arm()}")


def example_factory_function():
    """工厂函数使用示例"""
    print("\n" + "=" * 60)
    print("示例 8: 工厂函数创建 Bandit")
    print("=" * 60)
    
    arms = ["A", "B", "C"]
    
    # 创建不同类型的 bandit
    for algo in BanditAlgorithm:
        bandit = create_bandit(
            algo, 
            arms,
            # 根据算法类型传递不同参数
            epsilon=0.1 if algo == BanditAlgorithm.EPSILON_GREEDY else None,
            temperature=0.5 if algo == BanditAlgorithm.SOFTMAX else None,
        )
        
        # 简单测试
        selected = bandit.select()
        bandit.update(selected, random.random())
        
        print(f"{algo.value}: 选择了 {selected}")


def example_contextual_warning():
    """算法选择指南"""
    print("\n" + "=" * 60)
    print("算法选择指南")
    print("=" * 60)
    
    guide = """
    ┌─────────────────────────────────────────────────────────────┐
    │                     算法选择建议                            │
    ├─────────────────────────────────────────────────────────────┤
    │ Epsilon-Greedy:                                            │
    │   - 简单易懂，适合入门                                      │
    │   - 适合需要完全控制探索概率的场景                          │
    │                                                             │
    │ UCB1:                                                       │
    │   - 自动平衡探索与利用                                      │
    │   - 适合统计意义重要的场景                                  │
    │   - 有理论保证的遗憾上界                                    │
    │                                                             │
    │ Thompson Sampling:                                          │
    │   - 最适合 A/B 测试和二值奖励                               │
    │   - 自然地处理不确定性                                      │
    │   - 实践中表现优异                                          │
    │                                                             │
    │ Softmax:                                                    │
    │   - 输出概率分布，可解释性强                                │
    │   - 温度参数控制探索程度                                    │
    │   - 适合需要概率输出的场景                                  │
    │                                                             │
    │ Exponential-weight (EXP3):                                  │
    │   - 适合对抗性环境（对手可能改变奖励）                      │
    │   - 适合非平稳（时变）奖励                                  │
    └─────────────────────────────────────────────────────────────┘
    """
    print(guide)


if __name__ == "__main__":
    random.seed(42)  # 为了可重复的结果
    
    example_basic_usage()
    example_ab_testing()
    example_recommendation_system()
    example_ad_placement()
    example_compare_algorithms()
    example_quick_ab_test()
    example_dynamic_pricing()
    example_factory_function()
    example_contextual_warning()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)