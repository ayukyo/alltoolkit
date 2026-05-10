"""
布隆过滤器使用示例

演示各种使用场景和功能
"""

import sys
sys.path.insert(0, '..')
from mod import (
    BloomFilter,
    CountingBloomFilter,
    ScalableBloomFilter,
    create_bloom_filter,
    calculate_optimal_params,
    estimate_memory_usage
)


def example_basic_usage():
    """基本使用示例"""
    print("=" * 50)
    print("基本使用示例")
    print("=" * 50)
    
    # 创建布隆过滤器
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    
    print(f"\n创建过滤器: {bf}")
    print(f"位数组大小: {bf.size}")
    print(f"哈希函数数量: {bf.hash_count}")
    
    # 添加元素
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    for word in words:
        bf.add(word)
    
    print(f"\n添加了 {len(words)} 个元素")
    
    # 查询元素
    print("\n查询结果:")
    test_words = ["apple", "grape", "banana", "kiwi", "cherry"]
    for word in test_words:
        result = word in bf
        status = "✓ 存在" if result else "✗ 不存在"
        print(f"  '{word}': {status}")
    
    print(f"\n当前假阳性率: {bf.current_false_positive_rate():.6f}")
    print(f"负载因子: {bf.load_factor():.4f}")


def example_cache_penetration():
    """缓存穿透防护示例"""
    print("\n" + "=" * 50)
    print("缓存穿透防护示例")
    print("=" * 50)
    
    # 模拟场景：防止恶意请求查询不存在的数据
    print("\n场景：数据库中只有部分ID存在，需要快速过滤无效请求")
    
    # 创建布隆过滤器存储所有有效ID
    bf = BloomFilter(expected_items=10000, false_positive_rate=0.001)
    
    # 添加有效ID
    valid_ids = [f"USER_{i:05d}" for i in range(100, 200)]  # USER_00100 到 USER_00199
    for id in valid_ids:
        bf.add(id)
    
    print(f"已添加 {len(valid_ids)} 个有效用户ID")
    
    # 模拟请求
    requests = [
        "USER_00100",  # 存在
        "USER_00500",  # 不存在
        "USER_00150",  # 存在
        "USER_00999",  # 不存在
    ]
    
    print("\n处理请求:")
    for request_id in requests:
        if request_id in bf:
            # 可能存在，需要查数据库
            print(f"  {request_id}: 可能存在 → 查询数据库")
        else:
            # 一定不存在，直接拒绝
            print(f"  {request_id}: 一定不存在 → 直接拒绝（避免无效数据库查询）")
    
    print(f"\n优点：")
    print("  1. 快速过滤无效请求，减少数据库压力")
    print("  2. 内存占用小，适合存储大量数据")
    print("  3. 少量假阳性可接受（只是多查一次数据库）")


def example_url_deduplication():
    """URL去重示例"""
    print("\n" + "=" * 50)
    print("URL去重示例（网络爬虫场景）")
    print("=" * 50)
    
    # 创建布隆过滤器
    bf = BloomFilter(expected_items=100000, false_positive_rate=0.01)
    
    # 已爬取的URL
    crawled_urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/category/tech",
    ]
    
    for url in crawled_urls:
        bf.add(url)
    
    print(f"已爬取 {len(crawled_urls)} 个URL")
    
    # 新发现的URL
    new_urls = [
        "https://example.com/page1",      # 已爬取
        "https://example.com/page3",      # 新URL
        "https://example.com/category/tech",  # 已爬取
        "https://example.com/about",      # 新URL
    ]
    
    print("\n处理新发现的URL:")
    to_crawl = []
    for url in new_urls:
        if url in bf:
            print(f"  {url}: 已爬取，跳过")
        else:
            print(f"  {url}: 新URL，加入爬取队列")
            to_crawl.append(url)
            bf.add(url)  # 添加到过滤器
    
    print(f"\n需要爬取: {len(to_crawl)} 个新URL")


def example_counting_bloom_filter():
    """计数布隆过滤器示例"""
    print("\n" + "=" * 50)
    print("计数布隆过滤器示例（支持删除）")
    print("=" * 50)
    
    cbf = CountingBloomFilter(expected_items=100, false_positive_rate=0.01)
    
    # 添加元素
    items = ["active_user_1", "active_user_2", "active_user_3"]
    for item in items:
        cbf.add(item)
    
    print(f"添加了 {len(items)} 个活跃用户")
    print(f"统计信息: {cbf.get_stats()}")
    
    # 检查元素
    print("\n检查元素:")
    for item in items + ["inactive_user"]:
        status = "存在" if item in cbf else "不存在"
        print(f"  {item}: {status}")
    
    # 删除元素
    print("\n删除 'active_user_2'...")
    result = cbf.remove("active_user_2")
    print(f"删除结果: {'成功' if result else '失败'}")
    
    print("\n删除后检查:")
    for item in items:
        status = "存在" if item in cbf else "不存在"
        print(f"  {item}: {status}")
    
    print("\n应用场景：")
    print("  1. 动态用户在线状态")
    print("  2. 实时黑名单/白名单")
    print("  3. 需要频繁增删元素的场景")


def example_scalable_bloom_filter():
    """可扩展布隆过滤器示例"""
    print("\n" + "=" * 50)
    print("可扩展布隆过滤器示例")
    print("=" * 50)
    
    sbf = ScalableBloomFilter(
        initial_size=100,
        growth_factor=2.0,
        false_positive_rate=0.01,
        fill_threshold=0.6
    )
    
    print(f"初始配置: 大小=100, 增长因子=2.0, 阈值=0.6")
    
    # 添加大量元素
    print("\n添加1000个元素...")
    for i in range(1000):
        sbf.add(f"item_{i}")
    
    stats = sbf.get_stats()
    print(f"\n最终状态:")
    print(f"  过滤器数量: {stats['filter_count']}")
    print(f"  总元素数: {stats['total_item_count']}")
    print(f"  当前容量: {stats['current_capacity']}")
    
    print("\n应用场景：")
    print("  1. 数据量不确定的场景")
    print("  2. 数据持续增长")
    print("  3. 避免预先估计容量不准确的问题")


def example_serialization():
    """序列化示例"""
    print("\n" + "=" * 50)
    print("序列化示例（持久化存储）")
    print("=" * 50)
    
    # 创建并填充过滤器
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    
    for i in range(500):
        bf.add(f"item_{i}")
    
    print(f"原始过滤器: {bf}")
    
    # 序列化
    data = bf.to_bytes()
    print(f"\n序列化大小: {len(data)} 字节")
    print(f"平均每个元素: {len(data) / 500:.2f} 字节")
    
    # 反序列化
    restored = BloomFilter.from_bytes(data)
    print(f"\n恢复的过滤器: {restored}")
    
    # 验证
    test_items = ["item_0", "item_100", "item_499", "item_500"]
    print("\n验证数据完整性:")
    for item in test_items:
        original = item in bf
        after = item in restored
        status = "✓" if original == after else "✗"
        print(f"  {item}: 原始={original}, 恢复后={after} {status}")


def example_optimal_params():
    """最优参数计算示例"""
    print("\n" + "=" * 50)
    print("最优参数计算示例")
    print("=" * 50)
    
    scenarios = [
        (1000, 0.01, "小规模高精度"),
        (10000, 0.01, "中规模标准"),
        (100000, 0.001, "大规模高精度"),
        (1000000, 0.01, "百万级标准"),
    ]
    
    print("\n不同场景下的最优参数:")
    print("-" * 70)
    print(f"{'场景':<20} {'元素数':<12} {'假阳性率':<12} {'位数组大小':<15} {'哈希数':<8} {'内存(KB)':<10}")
    print("-" * 70)
    
    for n, p, desc in scenarios:
        size, hash_count = calculate_optimal_params(n, p)
        memory = estimate_memory_usage(n, p)
        print(f"{desc:<20} {n:<12} {p:<12.4f} {size:<15} {hash_count:<8} {memory/1024:<10.2f}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 50)
    print("便捷函数示例")
    print("=" * 50)
    
    # 使用便捷函数创建过滤器
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    bf = create_bloom_filter(items=items, expected_items=100, false_positive_rate=0.01)
    
    print(f"使用 create_bloom_filter 创建过滤器")
    print(f"已添加元素: {items}")
    print(f"过滤器信息: {bf}")
    
    # 检查
    print("\n检查元素:")
    for item in items + ["fig", "grape"]:
        status = "✓" if item in bf else "✗"
        print(f"  {item}: {status}")


def example_false_positive_analysis():
    """假阳性分析示例"""
    print("\n" + "=" * 50)
    print("假阳性率分析示例")
    print("=" * 50)
    
    import random
    
    # 创建过滤器
    n = 10000  # 元素数量
    p = 0.01   # 目标假阳性率
    
    bf = BloomFilter(expected_items=n, false_positive_rate=p)
    
    # 添加元素
    items = set(f"item_{i}" for i in range(n))
    for item in items:
        bf.add(item)
    
    # 测试假阳性
    test_items = set(f"test_{i}" for i in range(n))
    false_positives = sum(1 for item in test_items if item in bf)
    actual_fp_rate = false_positives / n
    
    print(f"\n配置:")
    print(f"  预期元素数: {n}")
    print(f"  目标假阳性率: {p}")
    
    print(f"\n实际测量:")
    print(f"  理论假阳性率: {bf.current_false_positive_rate():.6f}")
    print(f"  实际假阳性率: {actual_fp_rate:.6f}")
    print(f"  假阳性数量: {false_positives}/{n}")
    
    # 验证无假阴性
    false_negatives = sum(1 for item in items if item not in bf)
    print(f"\n假阴性数量: {false_negatives} (应该为0)")
    
    print("\n结论:")
    print("  ✓ 布隆过滤器保证无假阴性")
    print("  ✓ 实际假阳性率接近理论值")
    print("  ✓ 适合用于快速初步筛选")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_cache_penetration()
    example_url_deduplication()
    example_counting_bloom_filter()
    example_scalable_bloom_filter()
    example_serialization()
    example_optimal_params()
    example_convenience_functions()
    example_false_positive_analysis()
    
    print("\n" + "=" * 50)
    print("所有示例完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()