"""
Bloom Filter Utils 使用示例

演示布隆过滤器的各种使用场景：
1. 基础用法
2. 去重应用
3. 缓存过滤
4. URL 去重
5. 数据库查询优化
6. 序列化和持久化
7. 不同哈希函数对比
8. 可扩展过滤器
9. 计数过滤器
"""

import time
import random
import string
from typing import List, Set

from bloom_filter_utils import (
    BloomFilter,
    ScalableBloomFilter,
    ScalableBloomFilterConfig,
    CountingBloomFilter,
    BitArray,
    optimal_size,
    false_positive_rate,
    estimate_memory_usage,
    compare_hash_functions,
    BloomFilterBuilder,
    from_iterable,
)


def example_basic_usage():
    """示例 1: 基础用法"""
    print("\n" + "="*60)
    print("示例 1: BloomFilter 基础用法")
    print("="*60)
    
    # 创建布隆过滤器（预期 1000 元素，假阳性率 1%）
    bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
    
    print(f"过滤器配置: {bf}")
    print(f"位数组大小: {bf.size} 位 ({bf.size // 8} 字节)")
    print(f"哈希函数数量: {bf.hash_count}")
    
    # 添加元素
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    for item in items:
        bf.add(item)
    
    print(f"\n已添加 {len(bf)} 个元素")
    
    # 查询元素
    print("\n查询结果:")
    test_items = ["apple", "banana", "grape", "kiwi"]
    for item in test_items:
        result = item in bf
        expected = item in items
        status = "✓" if result == expected or (result and expected) else "✗"
        print(f"  '{item}': {result} (期望: {expected}) {status}")
    
    # 查看统计信息
    stats = bf.get_stats()
    print(f"\n统计信息:")
    print(f"  已设置位数: {stats.set_bits}")
    print(f"  填充率: {stats.fill_ratio:.2%}")
    print(f"  估计假阳性率: {stats.estimated_fp_rate:.4%}")


def example_deduplication():
    """示例 2: 数据去重"""
    print("\n" + "="*60)
    print("示例 2: 使用布隆过滤器进行数据去重")
    print("="*60)
    
    # 模拟大规模数据流
    bf = BloomFilter(expected_elements=10000, false_positive_rate=0.01)
    
    # 模拟的数据（有重复）
    all_data = [f"user_{i % 500}" for i in range(10000)]  # 500 个不同用户，重复 20 次
    
    seen_count = 0
    unique_estimates = 0
    
    for user in all_data:
        if user in bf:
            seen_count += 1
        else:
            bf.add(user)
            unique_estimates += 1
    
    print(f"总数据量: {len(all_data)}")
    print(f"识别为重复: {seen_count}")
    print(f"识别为新元素: {unique_estimates}")
    print(f"实际不同元素: 500")
    print(f"过滤器大小: {bf.size // 8} 字节")
    
    # 如果用 Set 存储，需要多少内存？
    actual_set = set(all_data)
    print(f"\n对比：如果用 Set 存储:")
    print(f"  Set 元素数量: {len(actual_set)}")
    print(f"  估算内存使用: ~{len(actual_set) * 50 // 1024} KB (Python 字符串对象)")
    print(f"  布隆过滤器: ~{bf.size // 8 // 1024} KB")
    
    saving = (len(actual_set) * 50 - bf.size // 8) / 1024
    print(f"  内存节省: ~{saving:.1f} KB ({saving / (len(actual_set) * 50 / 1024) * 100:.1f}%)")


def example_cache_filtering():
    """示例 3: 缓存穿透防护"""
    print("\n" + "="*60)
    print("示例 3: 使用布隆过滤器防止缓存穿透")
    print("="*60)
    
    # 模拟场景：缓存层使用布隆过滤器记录已缓存的键
    cache_bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
    
    # 已缓存的键
    cached_keys = [f"product_{i}" for i in range(100, 200)]  # 产品 ID 100-199
    for key in cached_keys:
        cache_bf.add(key)
    
    # 模拟请求
    requests = [
        "product_100",  # 已缓存
        "product_150",  # 已缓存
        "product_999",  # 不存在，但布隆过滤器可能误判
        "product_1000", # 不存在
        "product_200",  # 已缓存
    ]
    
    print("请求处理流程:")
    for request in requests:
        if request in cache_bf:
            # 可能已缓存，尝试从缓存获取
            if request in cached_keys:
                print(f"  {request}: ✓ 在布隆过滤器 → 查缓存 → 找到")
            else:
                print(f"  {request}: ✓ 在布隆过滤器 → 查缓存 → 未找到（假阳性）")
        else:
            # 肯定不在缓存中，直接跳过缓存查询
            print(f"  {request}: ✗ 不在布隆过滤器 → 直接查询数据库（节省缓存查询）")
    
    print("\n优势：")
    print("  - 对于肯定不在缓存中的请求，跳过缓存查询，直接查数据库")
    print("  - 减少无效的缓存查询压力")
    print("  - 当数据库返回空结果时，仍需谨慎处理（可能有假阳性）")


def example_url_deduplication():
    """示例 4: URL 去重（爬虫应用）"""
    print("\n" + "="*60)
    print("示例 4: URL 去重 - 网络爬虫应用")
    print("="*60)
    
    # 使用可扩展布隆过滤器，因为 URL 数量未知
    sbf = ScalableBloomFilter(
        initial_capacity=1000,
        false_positive_rate=0.001,  # 更低的假阳性率
        growth_factor=2.0,
    )
    
    # 模拟爬虫发现的 URL
    base_urls = [
        "https://example.com/page/1",
        "https://example.com/page/2",
        "https://example.com/category/news",
        "https://example.com/category/sports",
        "https://example.com/article/123",
    ]
    
    # 爬虫过程
    visited_count = 0
    skipped_count = 0
    
    print("爬虫 URL 处理:")
    
    # 第一轮爬取
    for url in base_urls:
        if url in sbf:
            print(f"  [跳过] {url} (已访问)")
            skipped_count += 1
        else:
            sbf.add(url)
            print(f"  [访问] {url}")
            visited_count += 1
    
    # 模拟第二轮（有些重复 URL）
    more_urls = [
        "https://example.com/page/1",  # 重复
        "https://example.com/page/3",  # 新的
        "https://example.com/article/123",  # 重复
        "https://example.com/article/456",  # 新的
    ]
    
    print("\n第二轮爬取:")
    for url in more_urls:
        if url in sbf:
            print(f"  [跳过] {url} (已访问)")
            skipped_count += 1
        else:
            sbf.add(url)
            print(f"  [访问] {url}")
            visited_count += 1
    
    stats = sbf.get_stats()
    print(f"\n爬虫统计:")
    print(f"  已访问 URL: {visited_count}")
    print(f"  跳过 URL: {skipped_count}")
    print(f"  内部过滤器数量: {stats['filter_count']}")
    print(f"  总存储大小: {stats['total_size_bytes'] // 1024} KB")


def example_database_query_optimization():
    """示例 5: 数据库查询优化"""
    print("\n" + "="*60)
    print("示例 5: 数据库查询优化")
    print("="*60)
    
    # 场景：判断某个用户 ID 是否存在于用户表中
    # 使用布隆过滤器快速判断，避免不必要的数据库查询
    
    # 模拟用户表（10000 用户）
    existing_users = set(range(10000))
    
    # 创建布隆过滤器
    bf = BloomFilter(expected_elements=10000, false_positive_rate=0.01)
    for user_id in existing_users:
        bf.add(f"user_{user_id}")
    
    # 模拟查询请求
    query_ids = [
        500,    # 存在
        9999,   # 存在（最后一个）
        10000,  # 不存在
        50000,  # 不存在
        7500,   # 存在
    ]
    
    db_queries_saved = 0
    db_queries_needed = 0
    
    print("查询处理:")
    for uid in query_ids:
        key = f"user_{uid}"
        if key in bf:
            # 可能存在，需要查询数据库确认
            db_queries_needed += 1
            if uid in existing_users:
                print(f"  user_{uid}: 可能存在 → 查数据库 → 找到")
            else:
                print(f"  user_{uid}: 可能存在 → 查数据库 → 未找到（假阳性）")
        else:
            # 肯定不存在，跳过数据库查询
            db_queries_saved += 1
            print(f"  user_{uid}: 不存在 → 跳过数据库查询")
    
    print(f"\n性能统计:")
    print(f"  数据库查询次数: {db_queries_needed}")
    print(f"  节省的查询次数: {db_queries_saved}")
    print(f"  查询节省率: {db_queries_saved / len(query_ids) * 100:.1f}%")
    print(f"\n布隆过滤器内存使用: {bf.size // 8 // 1024} KB")
    print(f"如果用 Set 存储 10000 个字符串: ~500 KB")
    print(f"内存节省: ~{500 - bf.size // 8 // 1024} KB")


def example_serialization():
    """示例 6: 序列化和持久化"""
    print("\n" + "="*60)
    print("示例 6: 序列化和持久化")
    print("="*60)
    
    # 创建并填充布隆过滤器
    bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
    items = [f"item_{i}" for i in range(500)]
    for item in items:
        bf.add(item)
    
    # 序列化为字节
    data = bf.to_bytes()
    print(f"原始过滤器: {bf}")
    print(f"序列化数据大小: {len(data)} 字节")
    
    # 反序列化
    bf_restored = BloomFilter.from_bytes(data)
    print(f"恢复的过滤器: {bf_restored}")
    
    # 验证所有元素都在恢复的过滤器中
    missing = sum(1 for item in items if item not in bf_restored)
    print(f"验证: 所有 {len(items)} 个元素都在恢复的过滤器中")
    print(f"缺失元素: {missing} (应该是 0)")
    
    # 保存到文件示例
    print("\n文件操作示例:")
    print("  bf.save('bloom_filter.dat')  # 保存")
    print("  bf = BloomFilter.load('bloom_filter.dat')  # 加载")
    
    # 对比不同大小
    print("\n不同配置的序列化大小:")
    configs = [
        (1000, 0.1),
        (1000, 0.01),
        (1000, 0.001),
        (10000, 0.01),
        (100000, 0.01),
    ]
    
    for n, fp in configs:
        temp_bf = BloomFilter(expected_elements=n, false_positive_rate=fp)
        size = len(temp_bf.to_bytes())
        print(f"  n={n}, fp={fp}: {size} 字节 ({size / 1024:.1f} KB)")


def example_hash_comparison():
    """示例 7: 不同哈希函数对比"""
    print("\n" + "="*60)
    print("示例 7: 不同哈希函数性能对比")
    print("="*60)
    
    # 准备测试数据
    items = [f"item_{i}" for i in range(1000)]
    queries = [f"item_{i}" for i in range(2000)]  # 包含一些不在集合中的
    
    print(f"测试配置: {len(items)} 元素, {len(queries)} 查询")
    
    results = compare_hash_functions(items, queries, 1000)
    
    print("\n各哈希函数性能:")
    print(f"{'哈希函数':<10} {'添加(ms)':<12} {'查询(ms)':<12} {'平均添加(μs)':<15} {'平均查询(μs)':<15} {'假阳性率':<10}")
    print("-" * 74)
    
    for name, data in results.items():
        print(f"{name:<10} {data['add_time_ms']:<12.3f} {data['query_time_ms']:<12.3f} "
              f"{data['avg_add_us']:<15.3f} {data['avg_query_us']:<15.3f} "
              f"{data['actual_fp_rate']:<10.4f}")
    
    # 找出最快的
    fastest_add = min(results.items(), key=lambda x: x[1]['add_time_ms'])
    fastest_query = min(results.items(), key=lambda x: x[1]['query_time_ms'])
    
    print(f"\n添加最快: {fastest_add[0]}")
    print(f"查询最快: {fastest_query[0]}")


def example_scalable_filter():
    """示例 8: 可扩展布隆过滤器"""
    print("\n" + "="*60)
    print("示例 8: 可扩展布隆过滤器")
    print("="*60)
    
    # 创建可扩展过滤器（初始容量小，测试扩容）
    config = ScalableBloomFilterConfig(
        initial_capacity=100,
        false_positive_rate=0.01,
        growth_factor=2.0,
        fp_rate_factor=0.8,
    )
    
    sbf = ScalableBloomFilter(config=config)
    
    print(f"初始状态: {sbf}")
    
    # 逐步添加元素，观察扩容
    milestones = [50, 100, 200, 400, 800]
    
    for target in milestones:
        current = len(sbf)
        while len(sbf) < target:
            sbf.add(f"item_{len(sbf)}")
        
        stats = sbf.get_stats()
        print(f"\n添加到 {len(sbf)} 个元素后:")
        print(f"  内部过滤器数量: {stats['filter_count']}")
        print(f"  总存储大小: {stats['total_size_bytes']} 字节")
        print(f"  估计假阳性率: {stats['estimated_fp_rate']:.6f}")
    
    # 验证所有元素都在
    print(f"\n验证: 随机检查 100 个元素")
    checks = random.sample(range(800), 100)
    missing = sum(1 for i in checks if f"item_{i}" not in sbf)
    print(f"  缺失元素: {missing} (应该是 0，无假阴性)")


def example_counting_filter():
    """示例 9: 计数布隆过滤器"""
    print("\n" + "="*60)
    print("示例 9: 计数布隆过滤器（支持删除）")
    print("="*60)
    
    # 创建计数布隆过滤器
    cbf = CountingBloomFilter(
        expected_elements=100,
        false_positive_rate=0.01,
        counter_bits=4,  # 4 位计数器，每个位置最大计数 15
    )
    
    print(f"配置: {cbf}")
    
    # 添加元素（包括重复）
    items_with_counts = {
        "apple": 3,
        "banana": 2,
        "cherry": 1,
        "date": 4,
    }
    
    print("\n添加元素:")
    for item, count in items_with_counts.items():
        for _ in range(count):
            cbf.add(item)
        print(f"  '{item}' 添加 {count} 次, 当前计数估计: {cbf.count(item)}")
    
    # 删除操作
    print("\n删除 'apple' 一次:")
    cbf.remove("apple")
    print(f"  'apple' 当前计数估计: {cbf.count(item)}")
    print(f"  'apple' 是否可能存在: {'apple' in cbf}")
    
    # 删除所有
    print("\n删除 'apple' 所有剩余:")
    while "apple" in cbf:
        cbf.remove("apple")
    print(f"  'apple' 当前计数估计: {cbf.count('apple')}")
    print(f"  'apple' 是否可能存在: {'apple' in cbf}")
    
    # 统计信息
    stats = cbf.get_stats()
    print(f"\n统计信息:")
    print(f"  总添加元素数: {len(cbf)}")
    print(f"  非零计数器: {stats['non_zero_counters']}")
    print(f"  计数器位数: {stats['counter_bits']}")
    print(f"  最大计数值: {stats['max_count']}")


def example_builder_pattern():
    """示例 10: 构建器模式"""
    print("\n" + "="*60)
    print("示例 10: 使用构建器模式创建布隆过滤器")
    print("="*60)
    
    # 使用流畅 API 构建
    bf = (BloomFilterBuilder()
          .expected_elements(1000)
          .false_positive_rate(0.01)
          .with_hash('murmur')
          .build())
    
    print(f"构建的过滤器: {bf}")
    
    # 带初始元素的构建
    items = ["red", "green", "blue", "yellow", "purple"]
    
    bf2 = (BloomFilterBuilder()
           .with_items(items)
           .false_positive_rate(0.001)
           .build())
    
    print(f"\n带初始元素的过滤器: {bf2}")
    print(f"验证所有元素:")
    for item in items:
        print(f"  '{item}': {item in bf2}")


def example_memory_estimation():
    """示例 11: 内存使用估算"""
    print("\n" + "="*60)
    print("示例 11: 内存使用估算")
    print("="*60)
    
    print("不同规模和假阳性率的内存需求:")
    print(f"{'元素数量':<15} {'假阳性率':<12} {'位数':<10} {'字节':<10} {'KB':<8} {'MB':<8} {'哈希数':<8}")
    print("-" * 73)
    
    configs = [
        (1000, 0.1),
        (1000, 0.01),
        (1000, 0.001),
        (10000, 0.01),
        (100000, 0.01),
        (1000000, 0.01),
        (1000000, 0.001),
    ]
    
    for n, fp in configs:
        stats = estimate_memory_usage(n, fp)
        print(f"{n:<15} {fp:<12} {stats['bits_needed']:<10} {stats['bytes_needed']:<10} "
              f"{stats['kilobytes']:<8.1f} {stats['megabytes']:<8.3f} {stats['hash_functions']:<8}")
    
    print("\n关键观察:")
    print("  - 假阳性率越低，所需空间越大")
    print("  - 元素数量越大，所需空间越大")
    print("  - 空间与元素数量线性相关")
    print("  - 空间与 log(1/p) 线性相关")


def example_optimal_calculation():
    """示例 12: 最优参数计算"""
    print("\n" + "="*60)
    print("示例 12: 最优参数计算")
    print("="*60)
    
    print("给定元素数量和假阳性率，计算最优配置:")
    
    scenarios = [
        (1000, 0.1),
        (1000, 0.01),
        (1000, 0.001),
        (10000, 0.01),
        (100000, 0.01),
    ]
    
    print(f"\n{'元素数量':<12} {'假阳性率':<12} {'位数(m)':<10} {'哈希数(k)':<10} {'实际假阳性率':<15}")
    print("-" * 59)
    
    for n, target_fp in scenarios:
        m, k = optimal_size(n, target_fp)
        actual_fp = false_positive_rate(n, m, k)
        bits_per_element = m / n
        
        print(f"{n:<12} {target_fp:<12} {m:<10} {k:<10} {actual_fp:<15.6f}")
        print(f"  → 每元素需要 {bits_per_element:.1f} 位")


def example_bitarray_operations():
    """示例 13: BitArray 直接操作"""
    print("\n" + "="*60)
    print("示例 13: BitArray 直接操作")
    print("="*60)
    
    # 创建位数组
    ba = BitArray(100)
    
    print(f"创建位数组: {ba}")
    
    # 设置一些位
    positions = [0, 10, 25, 50, 75, 99]
    for pos in positions:
        ba.set(pos)
    
    print(f"设置位位置: {positions}")
    print(f"已设置位数: {ba.count_set_bits()}")
    
    # 检查特定位置
    print("\n检查各位置:")
    test_positions = [0, 1, 10, 11, 50, 99, 100]
    for pos in test_positions:
        try:
            value = ba[pos]
            print(f"  位置 {pos}: {value}")
        except IndexError as e:
            print(f"  位置 {pos}: IndexError (越界)")
    
    # 翻转位
    print("\n翻转位置 10:")
    old = ba[10]
    ba.toggle(10)
    new = ba[10]
    print(f"  原值: {old}, 新值: {new}")
    
    # 清除所有位
    print("\n清除所有位:")
    ba.clear_all()
    print(f"  已设置位数: {ba.count_set_bits()}")


def example_real_world_scenario():
    """示例 14: 真实场景 - 垃圾邮件过滤"""
    print("\n" + "="*60)
    print("示例 14: 真实场景 - 垃圾邮件关键词过滤")
    print("="*60)
    
    # 模拟垃圾邮件关键词库
    spam_keywords = [
        "FREE MONEY", "CLICK HERE", "WIN NOW", "URGENT", "ACT NOW",
        "LIMITED TIME", "CONGRATULATIONS", "YOU WON", "CASH PRIZE",
        "NO RISK", "GUARANTEED", "DOUBLE YOUR", "MILLION DOLLARS",
    ]
    
    # 创建布隆过滤器存储关键词
    bf = BloomFilter(expected_elements=len(spam_keywords), false_positive_rate=0.01)
    for keyword in spam_keywords:
        bf.add(keyword.lower())
    
    print(f"垃圾邮件关键词库: {len(spam_keywords)} 个")
    print(f"过滤器大小: {bf.size // 8} 字节")
    
    # 测试邮件内容
    emails = [
        "Hello, this is a legitimate email about your project.",
        "FREE MONEY! Click here to claim your prize now!",
        "Meeting scheduled for tomorrow at 3 PM.",
        "URGENT: Your account needs immediate attention.",
        "Thanks for your help with the presentation.",
    ]
    
    print("\n邮件检测:")
    for email in emails:
        # 检查是否包含垃圾关键词
        found_keywords = []
        for word in email.lower().split():
            # 检查单词和组合
            if word in bf:
                found_keywords.append(word)
        
        # 更精确的短语检查
        for keyword in spam_keywords:
            if keyword.lower() in email.lower():
                found_keywords.append(keyword)
        
        status = "🚫 可能垃圾邮件" if found_keywords else "✓ 正常邮件"
        print(f"  '{email[:50]}...'")
        print(f"    → {status} (关键词: {found_keywords[:3] if found_keywords else '无'}")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "="*60)
    print("Bloom Filter Utils - 完整示例演示")
    print("="*60)
    
    example_basic_usage()
    example_deduplication()
    example_cache_filtering()
    example_url_deduplication()
    example_database_query_optimization()
    example_serialization()
    example_hash_comparison()
    example_scalable_filter()
    example_counting_filter()
    example_builder_pattern()
    example_memory_estimation()
    example_optimal_calculation()
    example_bitarray_operations()
    example_real_world_scenario()
    
    print("\n" + "="*60)
    print("所有示例完成！")
    print("="*60)


if __name__ == "__main__":
    # 可以运行单个示例或所有示例
    import sys
    
    if len(sys.argv) > 1:
        # 运行指定示例
        example_name = sys.argv[1]
        example_func = globals().get(f"example_{example_name}")
        if example_func:
            example_func()
        else:
            print(f"未找到示例: {example_name}")
            print("可用示例: basic_usage, deduplication, cache_filtering, url_deduplication, ...")
    else:
        # 运行所有示例
        run_all_examples()