"""
MurmurHash 基本使用示例

演示 MurmurHash 的各种用法：
- 基本哈希计算
- 不同变体选择
- 一致性哈希
- 布隆过滤器
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from murmur_hash_utils.mod import (
    murmurhash3_x86_32,
    murmurhash3_x86_128,
    murmurhash3_x64_128,
    murmurhash3_hex,
    ConsistentHash,
    HashBloomFilter
)


def demo_basic_hashing():
    """基本哈希计算示例"""
    print("=" * 60)
    print("1. 基本哈希计算")
    print("=" * 60)
    
    # 测试数据
    test_data = [
        "hello world",
        "MurmurHash3",
        "一致性哈希算法",
        "12345",
        "",
        "a" * 1000,  # 长字符串
    ]
    
    for data in test_data:
        h32 = murmurhash3_x86_32(data)
        h128 = murmurhash3_hex(data, variant='x64_128')
        
        display = data[:30] + "..." if len(data) > 30 else data
        print(f"'{display}':")
        print(f"  32位: {h32:10d} (0x{h32:08x})")
        print(f"  128位: {h128}")
        print()


def demo_seed_variation():
    """种子变化示例"""
    print("=" * 60)
    print("2. 使用不同种子值")
    print("=" * 60)
    
    data = "hello world"
    seeds = [0, 1, 42, 100, 999]
    
    print(f"输入: '{data}'")
    print()
    
    for seed in seeds:
        h = murmurhash3_x86_32(data, seed=seed)
        print(f"  种子 {seed:3d}: 0x{h:08x}")
    
    print("\n说明: 不同种子值产生完全不同的哈希结果")
    print("用途: 可以用种子值创建多个独立的哈希函数")


def demo_consistent_hashing():
    """一致性哈希示例"""
    print("\n" + "=" * 60)
    print("3. 一致性哈希 - 分布式系统路由")
    print("=" * 60)
    
    # 创建一致性哈希环
    servers = ['server1', 'server2', 'server3', 'server4', 'server5']
    ch = ConsistentHash(servers, virtual_nodes=150)
    
    print(f"服务器节点: {servers}")
    print(f"虚拟节点数: 150/物理节点")
    print()
    
    # 路由测试
    keys = ['user:1001', 'user:1002', 'data:abc', 'session:xyz', 'file:123']
    
    print("键路由结果:")
    for key in keys:
        server = ch.get_node(key)
        print(f"  '{key}' -> {server}")
    
    # 数据分布统计
    print("\n数据分布统计 (10000个键):")
    distribution = {s: 0 for s in servers}
    
    for i in range(10000):
        key = f"key_{i}"
        server = ch.get_node(key)
        distribution[server] += 1
    
    for server, count in sorted(distribution.items()):
        bar = "█" * (count // 50)
        print(f"  {server}: {count:4d} {bar}")
    
    # 添加节点演示
    print("\n添加新节点 'server6':")
    ch.add_node('server6')
    
    # 检查迁移
    unchanged = 0
    for i in range(1000):
        key = f"key_{i}"
        new_server = ch.get_node(key)
        # 原服务器
        ch.remove_node('server6')
        old_server = ch.get_node(key)
        ch.add_node('server6')
        
        if new_server == old_server or new_server != 'server6':
            unchanged += 1
    
    print(f"  约 {unchanged/10:.0f}% 的键保持原有路由")
    
    # 获取多节点（用于复制）
    print("\n获取多个节点（用于数据复制）:")
    replicas = ch.get_nodes('important:file', count=3)
    print(f"  'important:file' -> {replicas}")


def demo_bloom_filter():
    """布隆过滤器示例"""
    print("\n" + "=" * 60)
    print("4. 布隆过滤器 - 快速成员检测")
    print("=" * 60)
    
    # 创建布隆过滤器
    expected_items = 10000
    false_positive_rate = 0.01
    
    bf = HashBloomFilter(expected_items, false_positive_rate)
    
    print(f"预期元素数: {expected_items}")
    print(f"假阳性率: {false_positive_rate}")
    print(f"位数组大小: {bf.size}")
    print(f"哈希函数数: {bf.hash_count}")
    print()
    
    # 添加元素
    words = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    
    print("添加元素:")
    for word in words:
        bf.add(word)
        print(f"  + '{word}'")
    
    print(f"\n当前元素数: {len(bf)}")
    
    # 查询测试
    test_words = ['apple', 'grape', 'banana', 'mango', 'cherry']
    
    print("\n查询测试:")
    for word in test_words:
        exists = word in bf
        status = "✓ 存在" if exists else "✗ 不存在"
        actual = "（已添加）" if word in words else "（未添加）"
        print(f"  '{word}': {status} {actual}")
    
    # 假阳性测试
    print("\n假阳性率测试:")
    bf_test = HashBloomFilter(1000, 0.01)
    
    # 添加1000个元素
    for i in range(1000):
        bf_test.add(f"item_{i}")
    
    # 测试10000个不存在的元素
    false_positives = 0
    test_count = 10000
    
    for i in range(1000, 1000 + test_count):
        if bf_test.might_contain(f"item_{i}"):
            false_positives += 1
    
    actual_rate = false_positives / test_count
    print(f"  测试元素数: {test_count}")
    print(f"  假阳性数: {false_positives}")
    print(f"  实际假阳性率: {actual_rate:.4%}")


def demo_url_shortener():
    """URL缩短服务示例"""
    print("\n" + "=" * 60)
    print("5. 应用示例：URL缩短服务")
    print("=" * 60)
    
    class URLShortener:
        """基于MurmurHash的URL缩短服务"""
        
        def __init__(self):
            self.urls = {}  # hash -> url
            self.charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        def shorten(self, url: str) -> str:
            """缩短URL"""
            # 使用128位哈希
            h = murmurhash3_x86_32(url)
            
            # 转换为base62
            code = self._to_base62(h)
            
            # 如果冲突，使用不同种子
            original_h = h
            seed = 0
            while code in self.urls and self.urls[code] != url:
                seed += 1
                h = murmurhash3_x86_32(url, seed=seed)
                code = self._to_base62(h)
                if seed > 100:
                    raise Exception("无法找到可用短码")
            
            self.urls[code] = url
            return code
        
        def _to_base62(self, num: int) -> str:
            """转换为base62字符串"""
            if num == 0:
                return self.charset[0]
            
            result = []
            for _ in range(6):  # 6位短码
                result.append(self.charset[num % 62])
                num //= 62
            
            return ''.join(reversed(result))
        
        def expand(self, code: str) -> str:
            """展开短码"""
            return self.urls.get(code, None)
    
    # 使用示例
    shortener = URLShortener()
    
    urls = [
        "https://www.example.com/very/long/url/that/needs/shortening",
        "https://github.com/user/repo/issues/12345",
        "https://docs.python.org/3/library/functions.html",
    ]
    
    print("URL缩短:")
    for url in urls:
        short = shortener.shorten(url)
        print(f"  {url[:50]}...")
        print(f"    -> {short}")
    
    print("\nURL展开:")
    for url in urls:
        short = shortener.shorten(url)
        expanded = shortener.expand(short)
        match = "✓" if expanded == url else "✗"
        print(f"  {short} -> {expanded[:40]}... {match}")


def demo_deduplication():
    """数据去重示例"""
    print("\n" + "=" * 60)
    print("6. 应用示例：数据去重")
    print("=" * 60)
    
    class Deduplicator:
        """基于布隆过滤器的数据去重"""
        
        def __init__(self, expected_items: int = 100000):
            self.seen = HashBloomFilter(expected_items, 0.001)
            self.count = 0
            self.duplicates = 0
        
        def process(self, item: str) -> bool:
            """处理项目，返回是否为新项目"""
            if item in self.seen:
                self.duplicates += 1
                return False
            
            self.seen.add(item)
            self.count += 1
            return True
        
        def stats(self):
            """返回统计信息"""
            return {
                'total': self.count + self.duplicates,
                'unique': self.count,
                'duplicates': self.duplicates,
            }
    
    # 模拟数据流
    dedup = Deduplicator(1000)
    
    import random
    random.seed(42)
    
    data_stream = [f"user_{random.randint(1, 500)}" for _ in range(1000)]
    
    print(f"处理 {len(data_stream)} 条数据...")
    
    for item in data_stream:
        is_new = dedup.process(item)
    
    stats = dedup.stats()
    print(f"\n统计结果:")
    print(f"  总数据量: {stats['total']}")
    print(f"  唯一数据: {stats['unique']}")
    print(f"  重复数据: {stats['duplicates']}")


def main():
    """运行所有示例"""
    demo_basic_hashing()
    demo_seed_variation()
    demo_consistent_hashing()
    demo_bloom_filter()
    demo_url_shortener()
    demo_deduplication()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()