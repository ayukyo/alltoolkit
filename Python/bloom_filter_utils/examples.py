"""
Bloom Filter Utils 使用示例

展示布隆过滤器的各种使用场景
"""

from mod import (
    BloomFilter,
    ScalableBloomFilter,
    CountingBloomFilter,
    estimate_size
)


def example_basic_usage():
    """基本使用示例"""
    print("=" * 50)
    print("示例 1: 基本使用")
    print("=" * 50)
    
    # 创建一个预期存储 10000 个元素，误判率 1% 的布隆过滤器
    bf = BloomFilter(expected_items=10000, false_positive_rate=0.01)
    
    # 添加元素
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    for item in items:
        bf.add(item)
        print(f"添加: {item}")
    
    print(f"\n过滤器状态: {bf}")
    
    # 检查元素是否存在
    test_items = ["apple", "grape", "banana", "kiwi"]
    print("\n检查元素:")
    for item in test_items:
        result = "可能存在" if item in bf else "不存在"
        print(f"  {item}: {result}")


def example_url_deduplication():
    """URL 去重示例"""
    print("\n" + "=" * 50)
    print("示例 2: URL 去重（爬虫场景）")
    print("=" * 50)
    
    # 创建 URL 过滤器
    url_filter = BloomFilter(expected_items=100000, false_positive_rate=0.001)
    
    # 模拟爬虫发现的 URL
    visited_urls = [
        "https://example.com/page/1",
        "https://example.com/page/2",
        "https://example.com/page/3",
    ]
    
    new_urls = [
        "https://example.com/page/1",  # 已访问
        "https://example.com/page/4",  # 新 URL
        "https://example.com/page/5",  # 新 URL
        "https://example.com/page/2",  # 已访问
    ]
    
    # 标记已访问
    for url in visited_urls:
        url_filter.add(url)
    
    # 过滤新 URL
    to_crawl = []
    for url in new_urls:
        if url in url_filter:
            print(f"跳过（已访问）: {url}")
        else:
            print(f"加入队列: {url}")
            to_crawl.append(url)
    
    print(f"\n需要爬取的 URL 数量: {len(to_crawl)}")
    print(f"节省请求: {len(new_urls) - len(to_crawl)}")


def example_cache_protection():
    """缓存穿透防护示例"""
    print("\n" + "=" * 50)
    print("示例 3: 缓存穿透防护")
    print("=" * 50)
    
    # 模拟缓存层
    cache = {"user:1": "Alice", "user:2": "Bob"}
    
    # 布隆过滤器存储所有有效 key
    valid_keys = BloomFilter(expected_items=10000, false_positive_rate=0.01)
    for key in cache:
        valid_keys.add(key)
    
    def get_user(user_id):
        """模拟获取用户"""
        key = f"user:{user_id}"
        
        # 先检查布隆过滤器
        if key not in valid_keys:
            print(f"用户 {user_id}: 布隆过滤器拦截（一定不存在）")
            return None
        
        # 检查缓存
        if key in cache:
            print(f"用户 {user_id}: 缓存命中")
            return cache[key]
        
        # 假设从数据库查询
        print(f"用户 {user_id}: 缓存未命中，查询数据库")
        return None
    
    # 测试
    get_user(1)   # 存在，缓存命中
    get_user(2)   # 存在，缓存命中
    get_user(999) # 不存在，被布隆过滤器拦截
    get_user(3)   # 可能触发假阳性


def example_spam_filter():
    """垃圾邮件过滤示例"""
    print("\n" + "=" * 50)
    print("示例 4: 垃圾邮件关键词过滤")
    print("=" * 50)
    
    # 创建垃圾关键词过滤器
    spam_filter = BloomFilter(expected_items=1000, false_positive_rate=0.001)
    
    # 常见垃圾关键词
    spam_keywords = [
        "免费", "中奖", "优惠", "点击领取", "限时",
        "urgent", "winner", "click here", "free money"
    ]
    
    for keyword in spam_keywords:
        spam_filter.add(keyword.lower())
    
    emails = [
        "Hello, how are you?",
        "恭喜您中奖了！点击领取大奖",
        "Meeting reminder for tomorrow",
        "FREE MONEY - CLICK HERE NOW!!!",
        "项目进度更新",
    ]
    
    def is_spam(content):
        """检查是否为垃圾邮件"""
        content_lower = content.lower()
        for keyword in spam_keywords:
            if keyword.lower() in content_lower:
                if keyword.lower() in spam_filter:
                    return True
        return False
    
    print("邮件过滤结果:")
    for email in emails:
        status = "垃圾邮件" if is_spam(email) else "正常邮件"
        print(f"  [{status}] {email[:40]}...")


def example_serialization():
    """序列化示例"""
    print("\n" + "=" * 50)
    print("示例 5: 序列化与持久化")
    print("=" * 50)
    
    # 创建过滤器并添加数据
    bf = BloomFilter(1000, 0.01)
    items = [f"user_{i}" for i in range(100)]
    for item in items:
        bf.add(item)
    
    # 序列化
    data = bf.serialize()
    print(f"序列化数据大小: {len(data)} bytes")
    
    # 模拟保存到文件
    # with open("filter.bin", "wb") as f:
    #     f.write(data)
    
    # 反序列化
    bf_restored = BloomFilter.deserialize(data)
    
    # 验证
    print("\n验证恢复的过滤器:")
    test_items = ["user_1", "user_50", "user_999"]
    for item in test_items:
        original = item in bf
        restored = item in bf_restored
        status = "✓" if original == restored else "✗"
        print(f"  {status} {item}: 原始={original}, 恢复={restored}")


def example_counting_filter():
    """计数布隆过滤器示例"""
    print("\n" + "=" * 50)
    print("示例 6: 计数布隆过滤器（支持删除）")
    print("=" * 50)
    
    cbf = CountingBloomFilter(expected_items=1000)
    
    # 添加活跃用户
    active_users = ["alice", "bob", "charlie"]
    for user in active_users:
        cbf.add(user)
        print(f"添加用户: {user}")
    
    print(f"\n当前用户数: {len(cbf)}")
    
    # 检查用户状态
    test_users = ["alice", "david", "bob"]
    for user in test_users:
        status = "活跃" if user in cbf else "非活跃"
        print(f"  {user}: {status}")
    
    # 用户离开
    print("\n用户 bob 离开...")
    cbf.remove("bob")
    
    # 再次检查
    print("\n更新后状态:")
    for user in test_users:
        status = "活跃" if user in cbf else "非活跃"
        print(f"  {user}: {status}")


def example_scalable_filter():
    """可扩展布隆过滤器示例"""
    print("\n" + "=" * 50)
    print("示例 7: 可扩展布隆过滤器")
    print("=" * 50)
    
    # 创建可扩展过滤器
    sbf = ScalableBloomFilter(initial_capacity=100, false_positive_rate=0.01)
    
    # 添加大量数据（超过初始容量）
    print("添加 1000 个元素...")
    for i in range(1000):
        sbf.add(f"data_{i}")
    
    print(f"总元素数: {len(sbf)}")
    print(f"层数: {len(sbf._filters)}")
    
    # 验证所有元素
    found = sum(1 for i in range(1000) if f"data_{i}" in sbf)
    print(f"找到元素: {found}/1000")
    
    # 验证不存在的元素
    not_found = sum(1 for i in range(1000, 2000) if f"data_{i}" in sbf)
    print(f"误判（不存在但报告存在）: {not_found}/1000")


def example_resource_estimation():
    """资源估算示例"""
    print("\n" + "=" * 50)
    print("示例 8: 资源需求估算")
    print("=" * 50)
    
    scenarios = [
        (10000, 0.01, "小型应用"),
        (100000, 0.01, "中型应用"),
        (1000000, 0.01, "大型应用"),
        (10000000, 0.001, "大规模系统"),
        (100000000, 0.001, "超大规模"),
    ]
    
    print(f"{'场景':<12} {'元素数':<12} {'误判率':<8} {'内存(MB)':<10} {'哈希函数':<8}")
    print("-" * 55)
    
    for n, p, name in scenarios:
        info = estimate_size(n, p)
        print(f"{name:<12} {n:<12,} {p:<8.3f} {info['mb']:<10.2f} {info['hash_functions']:<8}")


def example_set_operations():
    """集合操作示例"""
    print("\n" + "=" * 50)
    print("示例 9: 集合操作（并集/交集）")
    print("=" * 50)
    
    # 创建两个过滤器
    bf1 = BloomFilter(100, 0.01)
    bf2 = BloomFilter(100, 0.01)
    
    # 第一个集合
    set1 = ["apple", "banana", "cherry"]
    for item in set1:
        bf1.add(item)
    print(f"集合 1: {set1}")
    
    # 第二个集合
    set2 = ["banana", "cherry", "date", "elderberry"]
    for item in set2:
        bf2.add(item)
    print(f"集合 2: {set2}")
    
    # 并集
    union = bf1.union(bf2)
    print(f"\n并集测试:")
    for item in ["apple", "banana", "cherry", "date", "elderberry"]:
        in_union = item in union
        print(f"  {item}: {'存在' if in_union else '不存在'}")
    
    # 交集
    intersection = bf1.intersection(bf2)
    print(f"\n交集测试:")
    for item in ["apple", "banana", "cherry", "date", "elderberry"]:
        in_inter = item in intersection
        print(f"  {item}: {'存在' if in_inter else '不存在'}")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_url_deduplication()
    example_cache_protection()
    example_spam_filter()
    example_serialization()
    example_counting_filter()
    example_scalable_filter()
    example_resource_estimation()
    example_set_operations()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()