"""
Bloom Filter Utils 使用示例

本文件展示布隆过滤器的各种使用场景和最佳实践。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    BloomFilter,
    ScalableBloomFilter,
    CountingBloomFilter,
    create_filter,
    create_scalable_filter,
    create_counting_filter
)


def example_basic_usage():
    """基础用法示例"""
    print("=" * 60)
    print("1. 基础用法")
    print("=" * 60)
    
    # 创建布隆过滤器
    bf = BloomFilter(capacity=10000, error_rate=0.01)
    print(f"创建过滤器: {bf}")
    
    # 添加元素
    usernames = ["alice", "bob", "charlie", "david", "eve"]
    for name in usernames:
        bf.add(name)
    
    print(f"\n添加了 {len(bf)} 个用户名")
    
    # 检查元素
    print("\n检查用户名是否存在:")
    for name in ["alice", "bob", "frank", "grace"]:
        exists = name in bf
        print(f"  '{name}': {'可能存在 ✓' if exists else '一定不存在 ✗'}")
    
    # 获取统计信息
    stats = bf.get_stats()
    print(f"\n统计信息:")
    print(f"  容量: {stats.capacity}")
    print(f"  位数组: {stats.num_bits:,} bits")
    print(f"  哈希函数: {stats.num_hashes}")
    print(f"  元素数: {stats.num_elements}")
    print(f"  填充率: {stats.fill_ratio:.2%}")
    print(f"  当前错误率: {stats.current_error_rate:.4%}")


def example_cache_penetration():
    """缓存穿透防护示例"""
    print("\n" + "=" * 60)
    print("2. 缓存穿透防护")
    print("=" * 60)
    
    # 模拟缓存穿透场景
    class CacheWithBloomFilter:
        """使用布隆过滤器防止缓存穿透的缓存"""
        
        def __init__(self):
            self.cache = {}
            self.bloom = BloomFilter(capacity=100000, error_rate=0.01)
            self.hit_count = 0
            self.miss_count = 0
            self.blocked_count = 0
        
        def set(self, key: str, value):
            """设置缓存"""
            self.cache[key] = value
            self.bloom.add(key)
        
        def get(self, key: str):
            """获取缓存"""
            # 先检查布隆过滤器
            if key not in self.bloom:
                self.blocked_count += 1
                return None  # 一定不存在，直接返回
            
            # 可能在缓存中
            if key in self.cache:
                self.hit_count += 1
                return self.cache[key]
            
            self.miss_count += 1
            return None
    
    # 使用示例
    cache = CacheWithBloomFilter()
    
    # 添加一些有效数据
    valid_keys = ["user:1", "user:2", "user:3", "product:100", "product:200"]
    for key in valid_keys:
        cache.set(key, f"value_of_{key}")
    
    print(f"缓存初始化完成，添加了 {len(valid_keys)} 个有效键")
    
    # 模拟查询
    test_keys = ["user:1", "user:999", "product:100", "attack:1", "attack:2", "attack:3"]
    print("\n查询结果:")
    for key in test_keys:
        result = cache.get(key)
        status = "命中" if result else "未命中"
        print(f"  {key}: {status}")
    
    print(f"\n统计:")
    print(f"  缓存命中: {cache.hit_count}")
    print(f"  缓存未命中: {cache.miss_count}")
    print(f"  布隆过滤拦截: {cache.blocked_count}")
    print(f"  节省数据库查询: {cache.blocked_count} 次")


def example_url_deduplication():
    """URL去重示例（爬虫场景）"""
    print("\n" + "=" * 60)
    print("3. 网页爬虫 URL 去重")
    print("=" * 60)
    
    class CrawlerURLFilter:
        """爬虫 URL 过滤器"""
        
        def __init__(self, expected_urls: int = 1000000):
            self.seen = BloomFilter(capacity=expected_urls, error_rate=0.001)
            self.count = 0
        
        def is_new(self, url: str) -> bool:
            """检查 URL 是否是新发现的"""
            if url in self.seen:
                return False
            self.seen.add(url)
            self.count += 1
            return True
    
    crawler = CrawlerURLFilter()
    
    # 模拟爬虫发现 URL
    discovered_urls = [
        "https://example.com/page/1",
        "https://example.com/page/2",
        "https://example.com/page/3",
        "https://example.com/page/1",  # 重复
        "https://example.com/page/2",  # 重复
        "https://example.com/page/4",
    ]
    
    print("URL 去重结果:")
    new_count = 0
    for url in discovered_urls:
        is_new = crawler.is_new(url)
        if is_new:
            new_count += 1
        status = "新发现 ✓" if is_new else "已存在 (跳过)"
        print(f"  {url[:40]}: {status}")
    
    print(f"\n统计:")
    print(f"  发现 URL: {len(discovered_urls)}")
    print(f"  新 URL: {new_count}")
    print(f"  重复: {len(discovered_urls) - new_count}")
    
    stats = crawler.seen.get_stats()
    print(f"  内存占用约: {stats.num_bits / 8 / 1024:.2f} KB")
    print(f"  (相比 Set 存储 URL 字符串，节省大量内存)")


def example_scalable_filter():
    """可扩展布隆过滤器示例"""
    print("\n" + "=" * 60)
    print("4. 可扩展布隆过滤器")
    print("=" * 60)
    
    # 当元素数量不确定时使用
    sbf = ScalableBloomFilter(initial_capacity=100, error_rate=0.01)
    
    print("添加元素（超过初始容量会自动扩展）:\n")
    
    for i in range(500):
        sbf.add(f"dynamic_item_{i}")
        
        # 打印扩展信息
        if i in [99, 199, 299, 399, 499]:
            stats = sbf.get_stats()
            print(f"  添加 {i+1} 个元素后:")
            print(f"    层数: {stats['num_layers']}")
            print(f"    总元素: {stats['total_elements']}")
    
    print(f"\n最终统计:")
    stats = sbf.get_stats()
    print(f"  总元素: {stats['total_elements']}")
    print(f"  层数: {stats['num_layers']}")
    
    print("\n各层详情:")
    for layer in stats['layers']:
        print(f"  层 {layer['layer']}: 容量={layer['capacity']}, "
              f"元素={layer['elements']}, 填充率={layer['fill_ratio']:.1%}")


def example_counting_filter():
    """计数布隆过滤器示例（支持删除）"""
    print("\n" + "=" * 60)
    print("5. 计数布隆过滤器（支持删除）")
    print("=" * 60)
    
    # 需要删除元素时使用
    cbf = CountingBloomFilter(capacity=100, error_rate=0.01)
    
    # 添加在线用户
    online_users = ["user_1", "user_2", "user_3", "user_4", "user_5"]
    print("添加在线用户:")
    for user in online_users:
        cbf.add(user)
        print(f"  + {user}")
    
    print(f"\n当前在线: {len(cbf)} 人")
    
    # 用户下线
    print("\n用户下线:")
    for user in ["user_2", "user_4"]:
        cbf.remove(user)
        print(f"  - {user}")
    
    print(f"\n当前在线: {len(cbf)} 人")
    
    # 检查状态
    print("\n检查用户状态:")
    for user in ["user_1", "user_2", "user_3", "user_4", "user_5", "user_999"]:
        status = "在线 ✓" if user in cbf else "离线 ✗"
        print(f"  {user}: {status}")


def example_serialization():
    """序列化和持久化示例"""
    print("\n" + "=" * 60)
    print("6. 序列化与持久化")
    print("=" * 60)
    
    # 创建并填充
    bf = BloomFilter(capacity=1000, error_rate=0.01)
    items = ["important_data_1", "important_data_2", "important_data_3"]
    
    for item in items:
        bf.add(item)
    
    print(f"原始过滤器: {bf}")
    
    # 序列化为字节
    data = bf.to_bytes()
    print(f"\n序列化后大小: {len(data)} bytes")
    
    # 模拟存储和加载
    print("模拟保存到文件/数据库...")
    
    # 反序列化
    bf_restored = BloomFilter.from_bytes(data)
    print(f"恢复后过滤器: {bf_restored}")
    
    # 验证数据完整性
    print("\n验证数据完整性:")
    all_present = all(item in bf_restored for item in items)
    print(f"  所有原始数据都存在: {all_present} ✓")


def example_false_positive_demonstration():
    """假阳性演示"""
    print("\n" + "=" * 60)
    print("7. 假阳性率演示")
    print("=" * 60)
    
    capacity = 1000
    error_rate = 0.05  # 5% 错误率，更易观察
    
    bf = BloomFilter(capacity=capacity, error_rate=error_rate)
    
    # 添加元素
    for i in range(capacity):
        bf.add(f"element_{i}")
    
    print(f"参数: 容量={capacity}, 目标错误率={error_rate}")
    print(f"实际: 位数={bf.num_bits}, 哈希函数={bf.num_hashes}")
    
    # 测试假阳性
    false_positives = 0
    test_count = 10000
    
    for i in range(capacity, capacity + test_count):
        # 这些元素绝对没有被添加过
        if f"element_{i}" in bf:
            false_positives += 1
    
    actual_rate = false_positives / test_count
    
    print(f"\n假阳性测试 ({test_count} 次查询):")
    print(f"  假阳性次数: {false_positives}")
    print(f"  实际错误率: {actual_rate:.2%}")
    print(f"  目标错误率: {error_rate:.2%}")
    print(f"  误差: {abs(actual_rate - error_rate):.2%}")
    
    # 注意：实际错误率可能略高于目标，因为参数是基于理论最优值


def example_spam_filter():
    """垃圾邮件过滤示例"""
    print("\n" + "=" * 60)
    print("8. 垃圾邮件特征过滤")
    print("=" * 60)
    
    class SpamFilter:
        """基于布隆过滤器的垃圾邮件特征检测"""
        
        def __init__(self):
            self.known_spam = BloomFilter(capacity=100000, error_rate=0.001)
            self.spam_phrases = BloomFilter(capacity=10000, error_rate=0.001)
            self._load_spam_data()
        
        def _load_spam_data(self):
            """加载垃圾邮件数据"""
            # 模拟加载已知的垃圾邮件发送者
            spammers = ["spammer1@bad.com", "spammer2@evil.com", "promo@spam.org"]
            for spammer in spammers:
                self.known_spam.add(spammer.lower())
            
            # 模拟加载垃圾邮件特征短语
            phrases = [
                "click here now",
                "act immediately",
                "congratulations you won",
                "limited time offer",
                "free money"
            ]
            for phrase in phrases:
                self.spam_phrases.add(phrase.lower())
        
        def check_email(self, sender: str, content: str) -> dict:
            """检查邮件是否可能是垃圾邮件"""
            result = {
                "is_spam": False,
                "reasons": []
            }
            
            # 检查发送者
            if sender.lower() in self.known_spam:
                result["is_spam"] = True
                result["reasons"].append("已知垃圾邮件发送者")
            
            # 检查内容特征
            content_lower = content.lower()
            if content_lower in self.spam_phrases:
                result["is_spam"] = True
                result["reasons"].append("包含垃圾邮件特征短语")
            
            return result
    
    # 使用示例
    spam_filter = SpamFilter()
    
    emails = [
        {
            "sender": "spammer1@bad.com",
            "content": "Hello, this is a normal email."
        },
        {
            "sender": "friend@gmail.com",
            "content": "click here now for free money!!!"
        },
        {
            "sender": "legitimate@company.com",
            "content": "Your order has been shipped."
        }
    ]
    
    print("邮件检测结果:")
    for email in emails:
        result = spam_filter.check_email(email["sender"], email["content"])
        status = "垃圾邮件 ⚠️" if result["is_spam"] else "正常邮件 ✓"
        print(f"\n  发送者: {email['sender']}")
        print(f"  状态: {status}")
        if result["reasons"]:
            print(f"  原因: {', '.join(result['reasons'])}")


def example_password_checker():
    """弱密码检查示例"""
    print("\n" + "=" * 60)
    print("9. 弱密码检测")
    print("=" * 60)
    
    class WeakPasswordChecker:
        """弱密码检查器"""
        
        def __init__(self):
            self.weak_passwords = BloomFilter(capacity=100000, error_rate=0.0001)
            self._load_weak_passwords()
        
        def _load_weak_passwords(self):
            """加载常见弱密码"""
            # 示例弱密码列表
            weak = [
                "password", "123456", "qwerty", "admin", "letmein",
                "welcome", "monkey", "dragon", "master", "login",
                "abc123", "111111", "password123", "admin123"
            ]
            for pwd in weak:
                self.weak_passwords.add(pwd.lower())
        
        def is_weak(self, password: str) -> bool:
            """检查密码是否可能是弱密码"""
            return password.lower() in self.weak_passwords
        
        def check_strength(self, password: str) -> dict:
            """检查密码强度"""
            result = {
                "password": "*" * len(password),
                "is_weak": self.is_weak(password),
                "length": len(password),
                "recommendations": []
            }
            
            if result["is_weak"]:
                result["recommendations"].append("这是一个常见的弱密码")
            
            if len(password) < 8:
                result["recommendations"].append("密码长度至少应为8个字符")
            
            if password.isnumeric():
                result["recommendations"].append("避免使用纯数字密码")
            
            if password.isalpha():
                result["recommendations"].append("建议添加数字和特殊字符")
            
            if not result["recommendations"]:
                result["recommendations"].append("密码强度良好")
            
            return result
    
    checker = WeakPasswordChecker()
    
    test_passwords = ["password", "MyStr0ng!Pass", "123456", "hello", "SecureP@ss2024"]
    
    print("密码强度检查结果:")
    for pwd in test_passwords:
        result = checker.check_strength(pwd)
        status = "弱 ⚠️" if result["is_weak"] else "良好 ✓"
        print(f"\n  密码: {result['password']}")
        print(f"  状态: {status}")
        print(f"  建议: {result['recommendations'][0]}")


def example_comparison_with_set():
    """与 Set 内存对比示例"""
    print("\n" + "=" * 60)
    print("10. 内存占用对比")
    print("=" * 60)
    
    import sys
    
    # 测试数据量
    n = 100000
    
    # 使用 Set
    s = set()
    for i in range(n):
        s.add(f"item_{i}")
    set_size = sys.getsizeof(s) + sum(sys.getsizeof(x) for x in list(s)[:100]) * n / 100  # 估算
    
    # 使用 BloomFilter
    bf = BloomFilter(capacity=n, error_rate=0.01)
    for i in range(n):
        bf.add(f"item_{i}")
    bf_size = bf.num_bits / 8  # 位数组字节大小
    
    print(f"存储 {n:,} 个元素的内存对比:\n")
    print(f"  Python Set:")
    print(f"    估算大小: {set_size / 1024 / 1024:.2f} MB")
    print(f"    精确查找: 是")
    
    print(f"\n  BloomFilter:")
    print(f"    位数组大小: {bf_size / 1024 / 1024:.2f} MB")
    print(f"    节省: {(1 - bf_size / set_size) * 100:.1f}%")
    print(f"    可能假阳性: 是 (约 {bf.error_rate:.2%})")
    
    print(f"\n结论:")
    print(f"  - 布隆过滤器节省约 {(1 - bf_size / set_size) * 100:.0f}% 内存")
    print(f"  - 适合允许少量假阳性的场景")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_cache_penetration()
    example_url_deduplication()
    example_scalable_filter()
    example_counting_filter()
    example_serialization()
    example_false_positive_demonstration()
    example_spam_filter()
    example_password_checker()
    example_comparison_with_set()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()