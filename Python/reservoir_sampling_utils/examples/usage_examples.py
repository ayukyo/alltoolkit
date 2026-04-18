"""
Reservoir Sampling Utils - 使用示例

展示水库采样在各种场景下的应用。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    ReservoirSampler,
    FastReservoirSampler,
    WeightedReservoirSampler,
    ReservoirSamplerWithReplacement,
    reservoir_sample,
    weighted_sample,
    stratified_reservoir_sample,
    two_pass_reservoir_sample,
    analyze_sample_distribution
)
import random


def example_basic_sampling():
    """基本采样示例"""
    print("=" * 50)
    print("示例 1: 基本水库采样")
    print("=" * 50)
    
    # 从数据流中采样 5 个元素
    sampler = ReservoirSampler(5, seed=42)
    
    # 模拟数据流
    for i in range(100):
        sampler.add(i)
    
    sample = sampler.sample()
    print(f"从 1-100 中采样 5 个: {sample}")
    print(f"处理了 {sampler.count} 个元素")
    print()


def example_streaming_data():
    """流式数据处理示例"""
    print("=" * 50)
    print("示例 2: 流式数据处理")
    print("=" * 50)
    
    # 模拟从文件或网络读取数据流
    def data_stream():
        """模拟数据流生成器"""
        for i in range(10000):
            yield f"item_{i}"
    
    sampler = ReservoirSampler(10, seed=123)
    sampler.add_all(data_stream())
    
    sample = sampler.sample()
    print(f"从 10000 条记录中采样 10 条:")
    for item in sample:
        print(f"  - {item}")
    print()


def example_weighted_sampling():
    """加权采样示例"""
    print("=" * 50)
    print("示例 3: 加权水库采样")
    print("=" * 50)
    
    # 商品推荐场景：高评分商品有更高概率被选中
    products = [
        ("优质商品A", 10.0),
        ("普通商品B", 5.0),
        ("低评分商品C", 1.0),
        ("热销商品D", 20.0),
        ("冷门商品E", 0.5),
    ]
    
    sampler = WeightedReservoirSampler(3, seed=42)
    for product, weight in products:
        sampler.add(product, weight)
    
    sample = sampler.sample()
    print("加权采样结果（高权重商品更可能被选中）:")
    for item in sample:
        print(f"  - {item}")
    print()


def example_stratified_sampling():
    """分层采样示例"""
    print("=" * 50)
    print("示例 4: 分层水库采样")
    print("=" * 50)
    
    # 用户数据：按年龄分层
    users = [
        ("用户1", 15), ("用户2", 17),  # 青少年
        ("用户3", 25), ("用户4", 30), ("用户5", 28),  # 青年
        ("用户6", 45), ("用户7", 50), ("用户8", 55),  # 中年
        ("用户9", 70), ("用户10", 75),  # 老年
    ]
    
    def age_group(user):
        """年龄分组函数"""
        _, age = user
        if age < 20:
            return "青少年"
        elif age < 40:
            return "青年"
        elif age < 60:
            return "中年"
        else:
            return "老年"
    
    result = stratified_reservoir_sample(
        iter(users),
        k=2,  # 每层采样 2 个
        strata_func=age_group,
        seed=42
    )
    
    print("分层采样结果:")
    for group, samples in sorted(result.items()):
        print(f"  {group}: {[s[0] for s in samples]}")
    print()


def example_fast_sampler():
    """高效采样器示例"""
    print("=" * 50)
    print("示例 5: 高效水库采样 (Algorithm L)")
    print("=" * 50)
    
    # 大数据集场景
    sampler = FastReservoirSampler(100, seed=42)
    
    # 模拟大数据流
    for i in range(1000000):
        sampler.add(i)
        if i % 100000 == 0:
            print(f"  已处理 {i:,} 条记录...")
    
    sample = sampler.sample()
    print(f"\n采样完成，共处理 {sampler.count:,} 条记录")
    print(f"样本大小: {len(sample)}")
    print(f"样本范围: {min(sample)} ~ {max(sample)}")
    print()


def example_with_replacement():
    """有放回采样示例"""
    print("=" * 50)
    print("示例 6: 有放回水库采样")
    print("=" * 50)
    
    # 抽奖场景：每个位置独立抽取，可能有重复中奖
    participants = ["Alice", "Bob", "Charlie", "David", "Eve"]
    
    sampler = ReservoirSamplerWithReplacement(3, seed=42)
    sampler.add_all(iter(participants))
    
    sample = sampler.sample()
    print("有放回抽奖结果（可能重复）:")
    for i, winner in enumerate(sample, 1):
        print(f"  第 {i} 名: {winner}")
    print()


def example_distribution_analysis():
    """分布分析示例"""
    print("=" * 50)
    print("示例 7: 采样结果分布分析")
    print("=" * 50)
    
    # 多次采样并分析分布
    all_samples = []
    for seed in range(10):
        sample = reservoir_sample(range(100), 10, seed=seed)
        all_samples.extend(sample)
    
    result = analyze_sample_distribution(all_samples)
    
    print(f"总采样次数: 10")
    print(f"每次采样大小: 10")
    print(f"总样本数: {result['total']}")
    print(f"唯一元素数: {result['unique']}")
    print(f"重复元素数: {result['duplicates']}")
    print(f"重复率: {result['duplicate_ratio']:.2%}")
    print()


def example_convenience_functions():
    """便捷函数示例"""
    print("=" * 50)
    print("示例 8: 便捷函数")
    print("=" * 50)
    
    # 快速采样
    sample = reservoir_sample(range(1000), 5, seed=42)
    print(f"reservoir_sample: {sample}")
    
    # 快速加权采样
    weighted_items = [("A", 1.0), ("B", 2.0), ("C", 3.0), ("D", 4.0)]
    sample = weighted_sample(iter(weighted_items), 2, seed=42)
    print(f"weighted_sample: {sample}")
    
    # 两遍扫描采样
    items = list(range(100))
    sample = two_pass_reservoir_sample(items, 5, seed=42)
    print(f"two_pass_reservoir_sample: {sample}")
    print()


def example_real_world_log_sampling():
    """真实场景：日志采样"""
    print("=" * 50)
    print("示例 9: 日志采样场景")
    print("=" * 50)
    
    # 模拟日志流
    def log_stream(n=10000):
        for i in range(n):
            level = random.choice(["INFO", "WARN", "ERROR"])
            yield f"[{level}] Log entry {i}"
    
    # 采样保留所有 ERROR，对其他日志采样
    error_logs = []
    sampler = ReservoirSampler(50, seed=42)
    
    for log in log_stream():
        if "[ERROR]" in log:
            error_logs.append(log)
        else:
            sampler.add(log)
    
    print(f"ERROR 日志数: {len(error_logs)}")
    print(f"其他日志采样数: {len(sampler.sample())}")
    print(f"采样器处理的总数: {sampler.count}")
    print()


def example_real_world_user_sampling():
    """真实场景：用户行为采样"""
    print("=" * 50)
    print("示例 10: 用户行为采样场景")
    print("=" * 50)
    
    # 模拟用户行为数据
    user_actions = [
        ("user_001", "click", 1.0),
        ("user_001", "view", 1.0),
        ("user_002", "purchase", 10.0),  # 购买行为权重高
        ("user_003", "click", 1.0),
        ("user_004", "signup", 5.0),
        ("user_005", "purchase", 10.0),
        ("user_006", "view", 1.0),
        ("user_007", "click", 1.0),
        ("user_008", "purchase", 10.0),
        ("user_009", "view", 1.0),
    ]
    
    # 加权采样：重要行为更可能被保留
    sampler = WeightedReservoirSampler(5, seed=42)
    for user, action, weight in user_actions:
        sampler.add(f"{user}:{action}", weight)
    
    sample = sampler.sample()
    print("加权采样结果（购买行为权重高）:")
    for item in sample:
        print(f"  - {item}")
    print()


def main():
    """运行所有示例"""
    example_basic_sampling()
    example_streaming_data()
    example_weighted_sampling()
    example_stratified_sampling()
    example_fast_sampler()
    example_with_replacement()
    example_distribution_analysis()
    example_convenience_functions()
    example_real_world_log_sampling()
    example_real_world_user_sampling()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()