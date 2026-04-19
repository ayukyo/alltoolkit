"""
布隆过滤器工具集示例 (Bloom Filter Examples)

演示布隆过滤器的各种使用场景
"""

from bloom_filter import (
    BloomFilter,
    CountingBloomFilter,
    ScalableBloomFilter,
    DeletableBloomFilter,
    BloomFilterBuilder,
    optimal_num_bits,
    optimal_num_hashes,
    estimate_false_positive_rate,
    create_bloom_filter,
    create_optimal_bloom_filter,
)


def example_basic_usage():
    """
    示例 1: 基础用法
    演示布隆过滤器的基本操作
    """
    print("=" * 60)
    print("示例 1: 基础用法")
    print("=" * 60)
    
    # 创建布隆过滤器
    bf = BloomFilter(capacity=10000, error_rate=0.01)
    
    # 添加元素
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    for word in words:
        bf.add(word)
    
    print(f"已添加 {len(bf)} 个元素")
    
    # 检查元素是否存在
    print(f"\n检查元素:")
    test_words = ["apple", "banana", "grape", "kiwi"]
    for word in test_words:
        result = "可能存在" if word in bf else "不存在"
        print(f"  {word}: {result}")
    
    # 获取统计信息
    stats = bf.stats()
    print(f"\n统计信息:")
    print(f"  容量: {stats.capacity}")
    print(f"  设计假阳性率: {stats.error_rate:.4%}")
    print(f"  位数组大小: {stats.size_bits:,} bits ({stats.size_bits / 8 / 1024:.2f} KB)")
    print(f"  哈希函数数量: {stats.num_hashes}")
    print(f"  已添加元素: {stats.num_elements}")
    print(f"  填充率: {stats.fill_ratio:.2%}")
    print(f"  估算假阳性率: {stats.estimated_error_rate:.4%}")


def example_cache_penetration():
    """
    示例 2: 缓存穿透防护
    使用布隆过滤器防止恶意查询穿透到数据库
    """
    print("\n" + "=" * 60)
    print("示例 2: 缓存穿透防护")
    print("=" * 60)
    
    # 模拟已有用户 ID
    existing_users = {f"user_{i}" for i in range(1, 10001)}
    
    # 创建布隆过滤器存储已存在用户
    bf = BloomFilter(capacity=10000, error_rate=0.01)
    for user_id in existing_users:
        bf.add(user_id)
    
    print(f"布隆过滤器已加载 {len(existing_users)} 个用户ID")
    
    # 模拟查询
    queries = ["user_1", "user_100", "user_99999", "user_5000", "user_100001"]
    
    print(f"\n查询结果:")
    for query in queries:
        if query not in bf:
            # 布隆过滤器确定不存在，直接返回
            print(f"  {query}: 不存在（被布隆过滤器拦截）")
        else:
            # 可能存在，需要查缓存/数据库
            actually_exists = query in existing_users
            status = "存在" if actually_exists else "假阳性（需要实际查询）"
            print(f"  {query}: 可能存在 -> {status}")
    
    # 统计拦截效果
    malicious_queries = [f"malicious_{i}" for i in range(1000)]
    blocked = sum(1 for q in malicious_queries if q not in bf)
    
    print(f"\n恶意查询拦截统计:")
    print(f"  总查询: 1000")
    print(f"  被拦截: {blocked}")
    print(f"  拦截率: {blocked / 1000:.2%}")


def example_url_deduplication():
    """
    示例 3: URL 去重
    爬虫中使用布隆过滤器去重 URL
    """
    print("\n" + "=" * 60)
    print("示例 3: URL 去重（爬虫场景）")
    print("=" * 60)
    
    # 创建 URL 去重过滤器
    url_filter = BloomFilter(capacity=100000, error_rate=0.001)
    
    # 模拟爬取的 URL
    visited_urls = [
        "https://example.com/page/1",
        "https://example.com/page/2",
        "https://example.com/page/3",
        "https://example.com/category/tech",
        "https://example.com/category/news",
    ]
    
    for url in visited_urls:
        url_filter.add(url)
    
    print(f"已访问 {len(url_filter)} 个 URL")
    
    # 模拟新发现的 URL
    new_urls = [
        "https://example.com/page/1",      # 已访问
        "https://example.com/page/4",      # 新 URL
        "https://example.com/page/2",      # 已访问
        "https://example.com/article/1",   # 新 URL
    ]
    
    print(f"\n处理新发现的 URL:")
    unique_count = 0
    for url in new_urls:
        if url in url_filter:
            print(f"  [跳过] {url}（已访问）")
        else:
            print(f"  [添加] {url}（新 URL）")
            url_filter.add(url)
            unique_count += 1
    
    print(f"\n新增 URL 数量: {unique_count}")
    print(f"布隆过滤器统计:")
    stats = url_filter.stats()
    print(f"  位数组: {stats.size_bits / 8 / 1024:.2f} KB")
    print(f"  填充率: {stats.fill_ratio:.2%}")


def example_counting_bloom_filter():
    """
    示例 4: 计数布隆过滤器
    支持删除操作的布隆过滤器
    """
    print("\n" + "=" * 60)
    print("示例 4: 计数布隆过滤器")
    print("=" * 60)
    
    # 创建计数布隆过滤器
    cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
    
    # 添加元素
    elements = ["active_user_1", "active_user_2", "active_user_3"]
    for elem in elements:
        cbf.add(elem)
    
    print(f"已添加 {len(cbf)} 个元素")
    
    # 检查存在性
    print(f"\n检查存在性:")
    for elem in elements:
        print(f"  {elem}: {'存在' if elem in cbf else '不存在'}")
    
    # 删除元素
    print(f"\n删除 active_user_2...")
    cbf.remove("active_user_2")
    
    print(f"\n删除后检查:")
    for elem in elements:
        exists = elem in cbf
        print(f"  {elem}: {'存在' if exists else '不存在'}")
    
    # 计数器特性：同一元素可多次添加
    print(f"\n多次添加同一元素:")
    for _ in range(3):
        cbf.add("frequent_user")
    print(f"  'frequent_user' 添加了 3 次")
    
    # 删除一次后仍存在
    cbf.remove("frequent_user")
    print(f"  删除 1 次后: {'存在' if 'frequent_user' in cbf else '不存在'}")


def example_scalable_bloom_filter():
    """
    示例 5: 可扩展布隆过滤器
    自动扩容，支持无限元素
    """
    print("\n" + "=" * 60)
    print("示例 5: 可扩展布隆过滤器")
    print("=" * 60)
    
    # 创建小初始容量的可扩展过滤器
    sbf = ScalableBloomFilter(
        initial_capacity=100,
        error_rate=0.01,
        growth_factor=2.0,
    )
    
    print(f"初始状态: {sbf}")
    
    # 添加超过初始容量的元素
    print(f"\n添加 1000 个元素...")
    for i in range(1000):
        sbf.add(f"item_{i}")
    
    print(f"添加后状态: {sbf}")
    print(f"  过滤器数量: {sbf.num_filters}")
    print(f"  总位数: {sbf.total_bits:,}")
    print(f"  估算假阳性率: {sbf.estimated_error_rate():.4%}")
    
    # 验证所有元素
    missing = sum(1 for i in range(1000) if f"item_{i}" not in sbf)
    print(f"\n验证: 1000 个元素中 {1000 - missing} 个可查询到（无假阴性）")


def example_deletable_bloom_filter():
    """
    示例 6: 可删除布隆过滤器
    使用指纹支持精确删除
    """
    print("\n" + "=" * 60)
    print("示例 6: 可删除布隆过滤器")
    print("=" * 60)
    
    # 创建可删除布隆过滤器
    dbf = DeletableBloomFilter(capacity=1000, error_rate=0.01)
    
    # 添加元素
    items = ["session_1", "session_2", "session_3"]
    for item in items:
        dbf.add(item)
    
    print(f"已添加 {len(dbf)} 个会话")
    
    # 模拟会话过期
    print(f"\n会话 session_2 过期，删除...")
    dbf.remove("session_2")
    
    print(f"\n当前会话:")
    for item in items:
        exists = item in dbf
        status = "活跃" if exists else "已过期"
        print(f"  {item}: {status}")


def example_builder_pattern():
    """
    示例 7: 构建器模式
    使用流畅 API 创建布隆过滤器
    """
    print("\n" + "=" * 60)
    print("示例 7: 构建器模式")
    print("=" * 60)
    
    # 标准布隆过滤器
    bf = (BloomFilterBuilder()
          .with_capacity(10000)
          .with_error_rate(0.001)
          .build())
    
    print(f"标准过滤器: {bf}")
    
    # 带初始元素的过滤器
    whitelist_bf = (BloomFilterBuilder()
                   .with_capacity(100)
                   .with_error_rate(0.01)
                   .with_items(["allowed_1", "allowed_2", "allowed_3"])
                   .build())
    
    print(f"带初始元素的过滤器: {whitelist_bf}")
    
    # 计数布隆过滤器
    cbf = (BloomFilterBuilder()
           .with_capacity(5000)
           .with_error_rate(0.005)
           .as_counting()
           .build())
    
    print(f"计数过滤器: {cbf}")
    
    # 可扩展布隆过滤器
    sbf = (BloomFilterBuilder()
           .with_capacity(1000)
           .with_error_rate(0.01)
           .as_scalable()
           .build())
    
    print(f"可扩展过滤器: {sbf}")
    
    # 可删除布隆过滤器
    dbf = (BloomFilterBuilder()
           .with_capacity(2000)
           .with_error_rate(0.01)
           .as_deletable()
           .build())
    
    print(f"可删除过滤器: {dbf}")


def example_serialization():
    """
    示例 8: 序列化和持久化
    保存和加载布隆过滤器
    """
    print("\n" + "=" * 60)
    print("示例 8: 序列化和持久化")
    print("=" * 60)
    
    # 创建并填充过滤器
    bf = BloomFilter(capacity=1000, error_rate=0.01)
    
    for i in range(100):
        bf.add(f"item_{i}")
    
    print(f"原始过滤器: {bf}")
    
    # 序列化为字节
    data = bf.to_bytes()
    print(f"\n序列化后大小: {len(data)} bytes")
    
    # 反序列化
    bf_restored = BloomFilter.from_bytes(data)
    print(f"恢复后的过滤器: {bf_restored}")
    
    # 验证数据完整性
    missing = sum(1 for i in range(100) if f"item_{i}" not in bf_restored)
    print(f"\n数据完整性验证: {100 - missing}/100 元素可查询")
    
    # 模拟保存到文件
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.bloom') as f:
        f.write(data)
        filepath = f.name
    
    print(f"已保存到: {filepath}")
    
    # 从文件加载
    with open(filepath, 'rb') as f:
        loaded_data = f.read()
    
    bf_loaded = BloomFilter.from_bytes(loaded_data)
    print(f"从文件加载: {bf_loaded}")
    
    # 清理
    import os
    os.unlink(filepath)


def example_optimal_parameters():
    """
    示例 9: 最优参数计算
    了解如何选择最优参数
    """
    print("\n" + "=" * 60)
    print("示例 9: 最优参数计算")
    print("=" * 60)
    
    # 不同场景的参数计算
    scenarios = [
        ("小型黑名单", 1000, 0.01),
        ("中型用户ID", 100000, 0.01),
        ("大型URL集合", 10000000, 0.001),
        ("海量数据", 100000000, 0.0001),
    ]
    
    print(f"\n{'场景':<15} {'元素数':>12} {'假阳性率':>10} {'位数组大小':>15} {'内存(KB)':>12} {'哈希数':>6}")
    print("-" * 75)
    
    for name, n, p in scenarios:
        m = optimal_num_bits(n, p)
        k = optimal_num_hashes(m, n)
        size_kb = m / 8 / 1024
        
        print(f"{name:<15} {n:>12,} {p:>10.4%} {m:>15,} {size_kb:>12.2f} {k:>6}")
    
    # 使用最优参数创建
    print(f"\n使用最优参数创建过滤器:")
    bf = create_optimal_bloom_filter(
        expected_items=10000,
        acceptable_false_positives=10,  # 可接受 10 个假阳性
    )
    print(f"  {bf}")


def example_union_operation():
    """
    示例 10: 并集操作
    合并两个布隆过滤器
    """
    print("\n" + "=" * 60)
    print("示例 10: 并集操作")
    print("=" * 60)
    
    # 创建两个过滤器
    bf1 = BloomFilter(capacity=1000, error_rate=0.01)
    bf2 = BloomFilter(capacity=1000, error_rate=0.01)
    
    # 分别添加元素
    set1 = ["apple", "banana", "cherry"]
    set2 = ["date", "elderberry", "fig"]
    
    for item in set1:
        bf1.add(item)
    for item in set2:
        bf2.add(item)
    
    print(f"过滤器1: {set1}")
    print(f"过滤器2: {set2}")
    
    # 计算并集
    union = bf1.union(bf2)
    
    print(f"\n并集后的过滤器统计:")
    stats = union.stats()
    print(f"  元素数: {stats.num_elements}")
    
    # 验证并集
    all_items = set1 + set2
    print(f"\n验证并集:")
    for item in all_items:
        exists = item in union
        print(f"  {item}: {'存在' if exists else '不存在'}")


def example_email_spam_filter():
    """
    示例 11: 垃圾邮件过滤器
    黑名单检测
    """
    print("\n" + "=" * 60)
    print("示例 11: 垃圾邮件黑名单")
    print("=" * 60)
    
    # 已知垃圾邮件发送者
    spammers = [
        "spam@example.com",
        "phishing@fake.com",
        "scam@malicious.org",
        "promo@spam.net",
        "newsletter@junk.com",
    ]
    
    # 创建黑名单过滤器
    blacklist = BloomFilter(capacity=10000, error_rate=0.001)
    for spammer in spammers:
        blacklist.add(spammer.lower())  # 统一小写
    
    print(f"已加载 {len(spammers)} 个垃圾邮件发送者到黑名单")
    
    # 检查邮件
    test_emails = [
        "spam@example.com",
        "legitimate@company.com",
        "PHISHING@FAKE.COM",  # 大小写测试
        "newuser@website.com",
        "promo@spam.net",
    ]
    
    print(f"\n邮件检查结果:")
    for email in test_emails:
        normalized = email.lower()
        if normalized in blacklist:
            status = "⚠️ 拦截（疑似垃圾邮件）"
        else:
            status = "✅ 放行"
        print(f"  {email}: {status}")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_cache_penetration()
    example_url_deduplication()
    example_counting_bloom_filter()
    example_scalable_bloom_filter()
    example_deletable_bloom_filter()
    example_builder_pattern()
    example_serialization()
    example_optimal_parameters()
    example_union_operation()
    example_email_spam_filter()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()