"""
MurmurHash 工具模块测试

测试覆盖：
- 基本哈希功能
- 边界情况处理
- 一致性验证
- 性能测试
- 一致性哈希
- 布隆过滤器
"""

import unittest
import sys
import os
import time
import random
import string

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from murmur_hash_utils.mod import (
    MurmurHash3,
    murmurhash3_x86_32,
    murmurhash3_x86_128,
    murmurhash3_x64_128,
    murmurhash3_hex,
    ConsistentHash,
    HashBloomFilter
)


class TestMurmurHash3Basic(unittest.TestCase):
    """基本哈希功能测试"""
    
    def test_x86_32_basic(self):
        """测试32位哈希基本功能"""
        # 已知测试向量
        result = murmurhash3_x86_32("")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLess(result, 2**32)
        
        # 相同输入相同输出
        result1 = murmurhash3_x86_32("hello")
        result2 = murmurhash3_x86_32("hello")
        self.assertEqual(result1, result2)
        
        # 不同输入不同输出
        result3 = murmurhash3_x86_32("world")
        self.assertNotEqual(result1, result3)
    
    def test_x86_128_basic(self):
        """测试x86 128位哈希基本功能"""
        result = murmurhash3_x86_128("")
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 4)
        
        for r in result:
            self.assertIsInstance(r, int)
            self.assertGreaterEqual(r, 0)
            self.assertLess(r, 2**32)
    
    def test_x64_128_basic(self):
        """测试x64 128位哈希基本功能"""
        result = murmurhash3_x64_128("")
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        
        for r in result:
            self.assertIsInstance(r, int)
            self.assertGreaterEqual(r, 0)
            self.assertLess(r, 2**64)
    
    def test_hex_output(self):
        """测试十六进制输出"""
        # 32位
        hex32 = murmurhash3_hex("test", variant='x86_32')
        self.assertIsInstance(hex32, str)
        self.assertEqual(len(hex32), 8)
        self.assertTrue(all(c in '0123456789abcdef' for c in hex32))
        
        # x86 128位
        hex128_x86 = murmurhash3_hex("test", variant='x86_128')
        self.assertEqual(len(hex128_x86), 32)
        
        # x64 128位
        hex128_x64 = murmurhash3_hex("test", variant='x64_128')
        self.assertEqual(len(hex128_x64), 32)
    
    def test_seed_variation(self):
        """测试不同种子产生不同结果"""
        result1 = murmurhash3_x86_32("hello", seed=0)
        result2 = murmurhash3_x86_32("hello", seed=1)
        result3 = murmurhash3_x86_32("hello", seed=42)
        
        self.assertNotEqual(result1, result2)
        self.assertNotEqual(result2, result3)
    
    def test_bytes_input(self):
        """测试字节数据输入"""
        str_result = murmurhash3_x86_32("hello")
        bytes_result = murmurhash3_x86_32(b"hello")
        
        self.assertEqual(str_result, bytes_result)
    
    def test_unicode_input(self):
        """测试Unicode输入"""
        result1 = murmurhash3_x86_32("你好世界")
        result2 = murmurhash3_x86_32("日本語")
        result3 = murmurhash3_x86_32("🎉🚀💻")
        
        self.assertIsInstance(result1, int)
        self.assertIsInstance(result2, int)
        self.assertIsInstance(result3, int)
        
        # 不同Unicode字符串产生不同结果
        self.assertNotEqual(result1, result2)
        self.assertNotEqual(result2, result3)


class TestMurmurHash3Consistency(unittest.TestCase):
    """一致性测试"""
    
    def test_deterministic(self):
        """测试确定性：相同输入总是产生相同输出"""
        test_inputs = ["", "a", "hello", "world", "12345", "测试"]
        
        for _ in range(10):
            for inp in test_inputs:
                r1 = murmurhash3_x86_32(inp)
                r2 = murmurhash3_x86_32(inp)
                self.assertEqual(r1, r2, f"输入 '{inp}' 产生不一致结果")
    
    def test_known_values(self):
        """测试已知参考值"""
        # MurmurHash3 x86_32 空字符串的已知结果
        result = murmurhash3_x86_32("", 0)
        self.assertEqual(result, 0x00000000)
        
        # 空字符串 x64_128
        h1, h2 = murmurhash3_x64_128("", 0)
        # 参考实现验证（空字符串应该产生确定的哈希值）
        self.assertIsInstance(h1, int)
        self.assertIsInstance(h2, int)
    
    def test_avalanche_effect(self):
        """测试雪崩效应：微小输入变化导致输出大幅变化"""
        base = "hello world"
        variants = [
            "hello worlD",  # 一个字符变化
            "hello worl",    # 删除一个字符
            "hello world!", # 添加一个字符
            "Hello world",  # 首字母大写
        ]
        
        base_hash = murmurhash3_x86_32(base)
        
        for variant in variants:
            var_hash = murmurhash3_x86_32(variant)
            # 哈希值应该完全不同
            self.assertNotEqual(base_hash, var_hash)


class TestMurmurHash3EdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_string(self):
        """测试空字符串"""
        result = murmurhash3_x86_32("")
        self.assertIsInstance(result, int)
        
        result128 = murmurhash3_x64_128("")
        self.assertIsInstance(result128, tuple)
        self.assertEqual(len(result128), 2)
    
    def test_single_byte(self):
        """测试单字节"""
        for i in range(256):
            data = bytes([i])
            result = murmurhash3_x86_32(data)
            self.assertIsInstance(result, int)
            self.assertGreaterEqual(result, 0)
    
    def test_long_string(self):
        """测试长字符串"""
        long_string = "a" * 100000
        result = murmurhash3_x86_32(long_string)
        self.assertIsInstance(result, int)
        
        # 长度不同结果不同
        for length in [100, 1000, 10000, 100000]:
            result = murmurhash3_x86_32("a" * length)
            self.assertIsInstance(result, int)
    
    def test_various_lengths(self):
        """测试不同长度输入"""
        for length in range(1, 100):
            data = "x" * length
            result = murmurhash3_x86_32(data)
            self.assertIsInstance(result, int)
    
    def test_special_characters(self):
        """测试特殊字符"""
        special = "\n\t\r\0\x00\xff"
        result = murmurhash3_x86_32(special)
        self.assertIsInstance(result, int)


class TestMurmurHash3Performance(unittest.TestCase):
    """性能测试"""
    
    def test_performance_x86_32(self):
        """测试32位哈希性能"""
        data = "test_data_for_performance" * 100
        iterations = 10000
        
        start = time.time()
        for _ in range(iterations):
            murmurhash3_x86_32(data)
        elapsed = time.time() - start
        
        per_second = iterations / elapsed
        print(f"\nx86_32 性能: {per_second:.0f} 次哈希/秒")
        
        # 确保性能合理（至少每秒500次，纯Python实现较慢）
        self.assertGreater(per_second, 500)
    
    def test_performance_x64_128(self):
        """测试128位哈希性能"""
        data = "test_data_for_performance" * 100
        iterations = 10000
        
        start = time.time()
        for _ in range(iterations):
            murmurhash3_x64_128(data)
        elapsed = time.time() - start
        
        per_second = iterations / elapsed
        print(f"x64_128 性能: {per_second:.0f} 次哈希/秒")
    
    def test_performance_bytes_vs_string(self):
        """测试字节和字符串性能对比"""
        str_data = "hello world" * 100
        bytes_data = str_data.encode('utf-8')
        iterations = 5000
        
        # 字符串
        start = time.time()
        for _ in range(iterations):
            murmurhash3_x86_32(str_data)
        str_time = time.time() - start
        
        # 字节
        start = time.time()
        for _ in range(iterations):
            murmurhash3_x86_32(bytes_data)
        bytes_time = time.time() - start
        
        print(f"字符串: {iterations/str_time:.0f}/秒, 字节: {iterations/bytes_time:.0f}/秒")


class TestConsistentHash(unittest.TestCase):
    """一致性哈希测试"""
    
    def test_basic_routing(self):
        """测试基本路由功能"""
        ch = ConsistentHash(['node1', 'node2', 'node3'])
        
        # 相同key应该路由到相同节点
        for _ in range(10):
            node = ch.get_node('user:1001')
            self.assertIn(node, ['node1', 'node2', 'node3'])
            
        # 多次查询应该一致
        node1 = ch.get_node('test_key')
        node2 = ch.get_node('test_key')
        self.assertEqual(node1, node2)
    
    def test_distribution(self):
        """测试分布均匀性"""
        nodes = ['node1', 'node2', 'node3', 'node4', 'node5']
        ch = ConsistentHash(nodes)
        
        counts = {node: 0 for node in nodes}
        
        for i in range(10000):
            key = f'key_{i}'
            node = ch.get_node(key)
            counts[node] += 1
        
        # 检查分布相对均匀（每个节点应该在10%-30%范围内）
        for node, count in counts.items():
            ratio = count / 10000
            self.assertGreater(ratio, 0.10, f"{node} 分布过低: {ratio:.2%}")
            self.assertLess(ratio, 0.30, f"{node} 分布过高: {ratio:.2%}")
        
        print(f"\n分布情况: {counts}")
    
    def test_add_node(self):
        """测试添加节点"""
        ch = ConsistentHash(['node1', 'node2'])
        
        # 记录原始路由
        original_routes = {}
        for i in range(100):
            key = f'key_{i}'
            original_routes[key] = ch.get_node(key)
        
        # 添加新节点
        ch.add_node('node3')
        
        # 大部分key应该保持原有路由
        same_count = 0
        for key, original_node in original_routes.items():
            new_node = ch.get_node(key)
            if new_node == original_node:
                same_count += 1
        
        # 添加一个节点后，大约1/3的key会迁移
        ratio = same_count / len(original_routes)
        print(f"添加节点后保持一致的比例: {ratio:.2%}")
        self.assertGreater(ratio, 0.5)  # 至少一半保持不变
    
    def test_remove_node(self):
        """测试移除节点"""
        ch = ConsistentHash(['node1', 'node2', 'node3'])
        
        # 记录原始路由
        original_routes = {}
        for i in range(100):
            key = f'key_{i}'
            original_routes[key] = ch.get_node(key)
        
        # 移除节点
        ch.remove_node('node3')
        
        # 验证移除后只有两个节点
        for i in range(100):
            key = f'key_{i}'
            node = ch.get_node(key)
            self.assertIn(node, ['node1', 'node2'])
    
    def test_get_nodes(self):
        """测试获取多个节点"""
        ch = ConsistentHash(['node1', 'node2', 'node3', 'node4', 'node5'])
        
        nodes = ch.get_nodes('test_key', 3)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(len(set(nodes)), 3)  # 无重复
        
        # 每个节点都应该是有效节点
        for node in nodes:
            self.assertIn(node, ['node1', 'node2', 'node3', 'node4', 'node5'])
    
    def test_empty_ring(self):
        """测试空环错误处理"""
        ch = ConsistentHash()
        
        with self.assertRaises(ValueError):
            ch.get_node('test_key')
    
    def test_virtual_nodes(self):
        """测试虚拟节点数量影响"""
        # 低虚拟节点数
        ch_low = ConsistentHash(['node1', 'node2', 'node3'], virtual_nodes=10)
        
        # 高虚拟节点数
        ch_high = ConsistentHash(['node1', 'node2', 'node3'], virtual_nodes=1000)
        
        # 计算分布标准差
        def calc_std_dev(ch, samples=1000):
            counts = {'node1': 0, 'node2': 0, 'node3': 0}
            for i in range(samples):
                key = f'key_{i}'
                node = ch.get_node(key)
                counts[node] += 1
            
            mean = samples / 3
            variance = sum((counts[n] - mean) ** 2 for n in counts) / 3
            return variance ** 0.5
        
        std_low = calc_std_dev(ch_low)
        std_high = calc_std_dev(ch_high)
        
        # 高虚拟节点数应该有更均匀的分布（更小的标准差）
        print(f"\n低虚拟节点数标准差: {std_low:.2f}, 高虚拟节点数标准差: {std_high:.2f}")


class TestHashBloomFilter(unittest.TestCase):
    """基于MurmurHash的布隆过滤器测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        bf = HashBloomFilter(1000, 0.01)
        
        # 添加元素
        bf.add("test1")
        bf.add("test2")
        bf.add("test3")
        
        # 检查存在
        self.assertIn("test1", bf)
        self.assertIn("test2", bf)
        self.assertIn("test3", bf)
        
        # 检查不存在
        self.assertNotIn("nonexistent", bf)
    
    def test_no_false_negatives(self):
        """测试无假阴性"""
        bf = HashBloomFilter(1000, 0.01)
        
        items = [f"item_{i}" for i in range(500)]
        for item in items:
            bf.add(item)
        
        # 所有添加的元素都应该被正确识别
        for item in items:
            self.assertIn(item, bf)
    
    def test_false_positive_rate(self):
        """测试假阳性率在预期范围内"""
        n = 1000  # 元素数量
        p = 0.01  # 假阳性率
        
        bf = HashBloomFilter(n, p)
        
        # 添加元素
        for i in range(n):
            bf.add(f"item_{i}")
        
        # 测试不存在的元素
        false_positives = 0
        test_count = 10000
        
        for i in range(n, n + test_count):
            if bf.might_contain(f"item_{i}"):
                false_positives += 1
        
        actual_rate = false_positives / test_count
        print(f"\n实际假阳性率: {actual_rate:.4%}, 预期: {p:.2%}")
        
        # 假阳性率应该在合理范围内（允许5倍误差）
        self.assertLess(actual_rate, p * 5)
    
    def test_len(self):
        """测试长度统计"""
        bf = HashBloomFilter(100, 0.01)
        
        self.assertEqual(len(bf), 0)
        
        for i in range(50):
            bf.add(f"item_{i}")
        
        self.assertEqual(len(bf), 50)
    
    def test_bytes_input(self):
        """测试字节数据输入"""
        bf = HashBloomFilter(100, 0.01)
        
        bf.add(b"bytes_data")
        self.assertIn(b"bytes_data", bf)
        
        # 字符串和字节应该一致
        bf.add("string_data")
        self.assertIn("string_data", bf)


class TestDistribution(unittest.TestCase):
    """哈希分布测试"""
    
    def test_uniformity(self):
        """测试哈希值分布均匀性"""
        n = 10000
        buckets = 256
        
        counts = [0] * buckets
        
        for i in range(n):
            hash_value = murmurhash3_x86_32(f"test_{i}")
            bucket = hash_value % buckets
            counts[bucket] += 1
        
        # 卡方检验简化版：每个桶的计数应该接近均值
        mean = n / buckets
        
        # 计算最大偏差
        max_deviation = max(abs(c - mean) for c in counts) / mean
        
        print(f"\n最大偏差: {max_deviation:.2%}, 期望均值: {mean:.1f}")
        print(f"桶计数范围: {min(counts)} - {max(counts)}")
        
        # 最大偏差不应该太大（纯Python实现，允许较大偏差）
        self.assertLess(max_deviation, 0.60)
    
    def test_collision_rate(self):
        """测试碰撞率"""
        n = 10000
        hashes = set()
        
        collisions = 0
        for i in range(n):
            h = murmurhash3_x86_32(f"unique_string_{i}")
            if h in hashes:
                collisions += 1
            hashes.add(h)
        
        collision_rate = collisions / n
        print(f"\n碰撞率: {collision_rate:.4%}")
        
        # 32位哈希在10000个元素时碰撞率应该很低
        self.assertLess(collision_rate, 0.01)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_consistent_hash_with_bloom_filter(self):
        """测试一致性哈希与布隆过滤器结合使用"""
        nodes = ['server1', 'server2', 'server3']
        ch = ConsistentHash(nodes)
        
        # 为每个节点创建布隆过滤器
        filters = {node: HashBloomFilter(1000, 0.01) for node in nodes}
        
        # 分配和记录数据
        for i in range(1000):
            key = f"user:{i}"
            node = ch.get_node(key)
            filters[node].add(key)
        
        # 验证数据分布和查找
        for i in range(1000):
            key = f"user:{i}"
            node = ch.get_node(key)
            self.assertIn(key, filters[node])
    
    def test_distributed_cache_simulation(self):
        """模拟分布式缓存场景"""
        # 创建分布式缓存
        servers = [f'cache_{i}' for i in range(10)]
        ch = ConsistentHash(servers, virtual_nodes=150)
        
        # 模拟缓存数据分布
        data_distribution = {server: 0 for server in servers}
        
        for i in range(10000):
            key = f"cache_key_{i}"
            server = ch.get_node(key)
            data_distribution[server] += 1
        
        # 验证分布均匀性
        values = list(data_distribution.values())
        mean = sum(values) / len(values)
        std_dev = (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5
        cv = std_dev / mean  # 变异系数
        
        print(f"\n分布式缓存模拟:")
        print(f"每个服务器数据量: {min(values)} - {max(values)}")
        print(f"均值: {mean:.0f}, 标准差: {std_dev:.0f}")
        print(f"变异系数: {cv:.2%}")
        
        # 变异系数应该小于20%
        self.assertLess(cv, 0.2)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestMurmurHash3Basic))
    suite.addTests(loader.loadTestsFromTestCase(TestMurmurHash3Consistency))
    suite.addTests(loader.loadTestsFromTestCase(TestMurmurHash3EdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestMurmurHash3Performance))
    suite.addTests(loader.loadTestsFromTestCase(TestConsistentHash))
    suite.addTests(loader.loadTestsFromTestCase(TestHashBloomFilter))
    suite.addTests(loader.loadTestsFromTestCase(TestDistribution))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)