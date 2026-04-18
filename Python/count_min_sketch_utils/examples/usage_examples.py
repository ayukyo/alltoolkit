"""
Count-Min Sketch 工具使用示例

本文件展示了 Count-Min Sketch 的各种使用场景：
1. 基本频率统计
2. 网络流量分析
3. 热点检测
4. Top-K 元素追踪
5. 流式数据处理
6. 合并多个数据源
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from count_min_sketch_utils.mod import (
    CountMinSketch,
    CountMinSketchBuilder,
    TopKTracker,
    create_optimal_sketch,
    frequency_analysis
)
import random
import time


def example_01_basic_usage():
    """示例 1: 基本频率统计"""
    print("=" * 60)
    print("示例 1: 基本频率统计")
    print("=" * 60)
    
    # 创建 Count-Min Sketch
    cms = CountMinSketch(width=1000, depth=5)
    
    # 模拟数据流
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    
    for word in words:
        cms.add(word)
    
    # 查询频率
    print(f"\n频率统计:")
    print(f"  apple: {cms.estimate('apple')} 次")
    print(f"  banana: {cms.estimate('banana')} 次")
    print(f"  cherry: {cms.estimate('cherry')} 次")
    print(f"  grape: {cms.estimate('grape')} 次 (不存在)")
    
    print(f"\n总计数: {cms.total_count}")
    print(f"内存使用: {cms.memory_usage} 字节")


def example_02_network_traffic_analysis():
    """示例 2: 网络流量分析"""
    print("\n" + "=" * 60)
    print("示例 2: 网络流量分析 - IP 频率统计")
    print("=" * 60)
    
    # 创建较大容量的 sketch
    cms = CountMinSketch(width=10000, depth=7)
    
    # 模拟网络流量 - 某些 IP 更频繁
    hot_ips = [f"192.168.1.{i}" for i in range(10)]
    normal_ips = [f"10.0.0.{i}" for i in range(100)]
    
    # 热点 IP 访问更多
    for ip in hot_ips:
        count = random.randint(500, 1000)
        cms.add(ip, count)
    
    # 普通 IP 访问较少
    for ip in normal_ips:
        count = random.randint(1, 50)
        cms.add(ip, count)
    
    # 检测热点 IP（频率 > 5%）
    all_ips = hot_ips + normal_ips
    threshold = 0.05
    heavy_hitters = cms.check_heavy_hitters(all_ips, threshold)
    
    print(f"\n检测到 {len(heavy_hitters)} 个热点 IP (频率 > {threshold*100}%):")
    for ip, count in heavy_hitters[:10]:
        print(f"  {ip}: ~{count} 次访问")
    
    print(f"\n总流量: {cms.total_count}")
    print(f"误差范围: ±{cms.estimate_error():.2f}")


def example_03_hot_hashtag_detection():
    """示例 3: 热门话题标签检测"""
    print("\n" + "=" * 60)
    print("示例 3: 社交媒体热门话题检测")
    print("=" * 60)
    
    # 使用 TopKTracker 追踪热门标签
    tracker = TopKTracker(k=10, sketch_width=5000, sketch_depth=5)
    
    # 模拟社交媒体标签流
    hashtags = [
        "#AI", "#科技", "#AI", "#创新", "#AI", "#科技",
        "#健康", "#生活", "#AI", "#科技", "#创新",
        "#体育", "#足球", "#体育", "#足球", "#体育",
        "#AI", "#科技", "#健康", "#生活", "#创新",
        "#AI", "#科技", "#AI", "#创新", "#AI",
    ]
    
    # 随机打乱并添加更多数据
    random.shuffle(hashtags)
    for tag in hashtags * 10:
        tracker.add(tag)
    
    # 获取 Top-10 标签
    top_hashtags = tracker.get_top_k()
    
    print(f"\n热门话题 Top-{len(top_hashtags)}:")
    for i, (tag, count) in enumerate(top_hashtags, 1):
        bar = "█" * min(count // 10, 20)
        print(f"  {i:2}. {tag:<10} {count:>5} 次 {bar}")


def example_04_builder_pattern():
    """示例 4: 使用 Builder 创建最优参数"""
    print("\n" + "=" * 60)
    print("示例 4: 根据需求自动计算最优参数")
    print("=" * 60)
    
    # 场景：需要高精度统计
    print("\n场景 1: 高精度统计 (误差 < 0.1%, 置信度 99%)")
    builder1 = CountMinSketchBuilder()
    builder1.with_error_rate(0.001).with_confidence(0.99)
    cms1 = builder1.build()
    print(f"  参数: width={cms1.width}, depth={cms1.depth}")
    print(f"  内存: {cms1.memory_usage / 1024:.2f} KB")
    
    # 场景：快速统计，允许较大误差
    print("\n场景 2: 快速统计 (误差 < 5%, 置信度 90%)")
    builder2 = CountMinSketchBuilder()
    builder2.with_error_rate(0.05).with_confidence(0.90)
    cms2 = builder2.build()
    print(f"  参数: width={cms2.width}, depth={cms2.depth}")
    print(f"  内存: {cms2.memory_usage / 1024:.2f} KB")
    
    # 场景：均衡配置
    print("\n场景 3: 均衡配置 (误差 < 1%, 置信度 95%)")
    cms3 = create_optimal_sketch(expected_items=1000000)
    print(f"  参数: width={cms3.width}, depth={cms3.depth}")


def example_05_stream_processing():
    """示例 5: 流式数据处理"""
    print("\n" + "=" * 60)
    print("示例 5: 流式数据实时处理")
    print("=" * 60)
    
    cms = CountMinSketch(width=5000, depth=5)
    tracker = TopKTracker(k=5, sketch_width=5000, sketch_depth=5)
    
    # 模拟实时数据流
    events = ["click", "view", "click", "purchase", "view", 
              "click", "view", "click", "view", "purchase"]
    
    print("\n实时处理中...")
    batch_size = 1000
    for batch_num in range(3):
        # 模拟一批数据
        for _ in range(batch_size):
            event = random.choice(events)
            weight = random.randint(1, 5)
            cms.add(event, weight)
            tracker.add(event, weight)
        
        # 输出当前状态
        print(f"\n批次 {batch_num + 1} 处理完成:")
        print(f"  总事件数: {cms.total_count}")
        print(f"  Top-5 事件:")
        for event, count in tracker.get_top_k():
            print(f"    - {event}: ~{count}")


def example_06_merge_data_sources():
    """示例 6: 合并多个数据源"""
    print("\n" + "=" * 60)
    print("示例 6: 合并多个数据源")
    print("=" * 60)
    
    # 模拟多个数据源
    source1 = CountMinSketch(width=100, depth=5, seed=42)
    source2 = CountMinSketch(width=100, depth=5, seed=42)
    source3 = CountMinSketch(width=100, depth=5, seed=42)
    
    # 数据源 1: 用户点击
    source1.add("product_A", 100)
    source1.add("product_B", 50)
    
    # 数据源 2: 用户购买
    source2.add("product_A", 30)
    source2.add("product_C", 20)
    
    # 数据源 3: 用户收藏
    source3.add("product_A", 40)
    source3.add("product_B", 10)
    source3.add("product_D", 15)
    
    # 合并数据源
    merged = source1.merge(source2).merge(source3)
    
    print("\n各数据源统计:")
    print(f"  数据源 1 (点击): {source1.total_count} 次操作")
    print(f"  数据源 2 (购买): {source2.total_count} 次操作")
    print(f"  数据源 3 (收藏): {source3.total_count} 次操作")
    
    print("\n合并后统计:")
    print(f"  总操作数: {merged.total_count}")
    print(f"  product_A: ~{merged.estimate('product_A')}")
    print(f"  product_B: ~{merged.estimate('product_B')}")
    print(f"  product_C: ~{merged.estimate('product_C')}")
    print(f"  product_D: ~{merged.estimate('product_D')}")


def example_07_serialization():
    """示例 7: 序列化和持久化"""
    print("\n" + "=" * 60)
    print("示例 7: 序列化与持久化")
    print("=" * 60)
    
    # 创建并填充数据
    cms = CountMinSketch(width=100, depth=5)
    for i in range(100):
        cms.add(f"item_{i % 10}")
    
    # 序列化为 JSON
    json_str = cms.to_json()
    print(f"\n序列化为 JSON ({len(json_str)} 字符):")
    print(f"  {json_str[:100]}...")
    
    # 从 JSON 恢复
    restored = CountMinSketch.from_json(json_str)
    
    print("\n恢复后验证:")
    for i in range(10):
        item = f"item_{i}"
        print(f"  {item}: 原始={cms.estimate(item)}, 恢复={restored.estimate(item)}")
    
    print(f"\n总计数: 原始={cms.total_count}, 恢复={restored.total_count}")


def example_08_frequency_analysis():
    """示例 8: 一站式频率分析"""
    print("\n" + "=" * 60)
    print("示例 8: 一站式频率分析")
    print("=" * 60)
    
    # 模拟用户行为数据
    actions = []
    users = [f"user_{i}" for i in range(100)]
    action_types = ["login", "view", "click", "purchase", "logout"]
    weights = [1, 10, 5, 1, 1]  # 不同行为的相对频率
    
    for _ in range(1000):
        action = random.choices(action_types, weights=weights)[0]
        user = random.choice(users)
        actions.append(f"{user}:{action}")
    
    # 进行频率分析
    result = frequency_analysis(
        actions,
        width=1000,
        depth=5,
        threshold=0.05,  # 检测高频行为
        top_k=5           # 获取 Top-5
    )
    
    print(f"\n分析结果:")
    print(f"  总操作数: {result['total_count']}")
    print(f"  唯一组合: {result['unique_count']}")
    print(f"  误差范围: ±{result['error_bound']:.2f}")
    
    if 'heavy_hitters' in result:
        print(f"\n  高频操作 (>{result['total_count'] * 0.05} 次):")
        for item, count in result['heavy_hitters'][:5]:
            print(f"    - {item}: {count}")
    
    if 'top_k' in result:
        print(f"\n  Top-5 操作:")
        for item, count in result['top_k']:
            print(f"    - {item}: {count}")


def example_09_accuracy_comparison():
    """示例 9: 准确性与参数关系"""
    print("\n" + "=" * 60)
    print("示例 9: 参数对准确性的影响")
    print("=" * 60)
    
    # 准备测试数据
    true_counts = {}
    for i in range(100):
        item = f"item_{i}"
        count = random.randint(1, 100)
        true_counts[item] = count
    
    # 测试不同参数
    configs = [
        ("低精度", 100, 3),
        ("中精度", 1000, 5),
        ("高精度", 5000, 7),
    ]
    
    print("\n准确性对比:")
    for name, width, depth in configs:
        cms = CountMinSketch(width=width, depth=depth)
        
        # 添加数据
        for item, count in true_counts.items():
            cms.add(item, count)
        
        # 计算误差
        errors = []
        for item, true_count in true_counts.items():
            estimated = cms.estimate(item)
            error = abs(estimated - true_count) / true_count * 100
            errors.append(error)
        
        avg_error = sum(errors) / len(errors)
        max_error = max(errors)
        
        print(f"\n  {name} (width={width}, depth={depth}):")
        print(f"    内存: {cms.memory_usage / 1024:.2f} KB")
        print(f"    平均误差: {avg_error:.2f}%")
        print(f"    最大误差: {max_error:.2f}%")


def example_10_performance():
    """示例 10: 性能测试"""
    print("\n" + "=" * 60)
    print("示例 10: 性能测试")
    print("=" * 60)
    
    cms = CountMinSketch(width=10000, depth=5)
    
    # 测试添加性能
    n = 100000
    start = time.time()
    for i in range(n):
        cms.add(f"item_{i}")
    add_time = time.time() - start
    
    print(f"\n添加 {n:,} 个元素:")
    print(f"  耗时: {add_time:.3f} 秒")
    print(f"  速率: {n / add_time:,.0f} 操作/秒")
    
    # 测试查询性能
    start = time.time()
    for i in range(n):
        cms.estimate(f"item_{i}")
    query_time = time.time() - start
    
    print(f"\n查询 {n:,} 次:")
    print(f"  耗时: {query_time:.3f} 秒")
    print(f"  速率: {n / query_time:,.0f} 操作/秒")
    
    print(f"\n内存使用: {cms.memory_usage / 1024:.2f} KB")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Count-Min Sketch 工具使用示例")
    print("=" * 60)
    
    examples = [
        example_01_basic_usage,
        example_02_network_traffic_analysis,
        example_03_hot_hashtag_detection,
        example_04_builder_pattern,
        example_05_stream_processing,
        example_06_merge_data_sources,
        example_07_serialization,
        example_08_frequency_analysis,
        example_09_accuracy_comparison,
        example_10_performance,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n示例执行出错: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例执行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()