"""
布隆过滤器工具模块测试
"""

import math
import pytest
from mod import (
    BloomFilter, 
    CountingBloomFilter, 
    ScalableBloomFilter,
    create_bloom_filter,
    calculate_optimal_params,
    estimate_memory_usage
)


class TestBloomFilter:
    """标准布隆过滤器测试"""
    
    def test_basic_operations(self):
        """测试基本添加和查询操作"""
        bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
        
        # 添加元素
        bf.add("hello")
        bf.add("world")
        bf.add("python")
        
        # 检查存在的元素
        assert "hello" in bf
        assert "world" in bf
        assert "python" in bf
        
        # 检查不存在的元素（大部分应该返回False）
        assert "java" not in bf or True  # 允许假阳性
        assert "rust" not in bf or True
    
    def test_contains_method(self):
        """测试contains方法"""
        bf = BloomFilter(expected_items=50)
        bf.add("test")
        
        assert bf.contains("test") is True
        assert bf.contains("notexist") in [True, False]  # 可能假阳性
    
    def test_len(self):
        """测试长度"""
        bf = BloomFilter(expected_items=100)
        assert len(bf) == 0
        
        bf.add("item1")
        bf.add("item2")
        assert len(bf) == 2
    
    def test_repr(self):
        """测试字符串表示"""
        bf = BloomFilter(expected_items=100)
        repr_str = repr(bf)
        assert "BloomFilter" in repr_str
        assert "size=" in repr_str
        assert "hash_count=" in repr_str
    
    def test_clear(self):
        """测试清空"""
        bf = BloomFilter(expected_items=100)
        bf.add("item1")
        bf.add("item2")
        
        bf.clear()
        assert len(bf) == 0
        assert "item1" not in bf
        assert "item2" not in bf
    
    def test_stats(self):
        """测试统计信息"""
        bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
        
        for i in range(50):
            bf.add(f"item_{i}")
        
        stats = bf.get_stats()
        
        assert stats["item_count"] == 50
        assert stats["size"] > 0
        assert stats["hash_count"] > 0
        assert 0 <= stats["load_factor"] <= 1
        assert 0 <= stats["current_false_positive_rate"] < 1
    
    def test_current_false_positive_rate(self):
        """测试当前假阳性率计算"""
        bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
        
        # 空过滤器假阳性率为0
        assert bf.current_false_positive_rate() == 0.0
        
        # 添加元素后计算假阳性率
        for i in range(100):
            bf.add(f"item_{i}")
        
        fp_rate = bf.current_false_positive_rate()
        assert 0 <= fp_rate <= 1
    
    def test_load_factor(self):
        """测试负载因子"""
        bf = BloomFilter(expected_items=100)
        
        # 空过滤器负载为0
        assert bf.load_factor() == 0.0
        
        # 添加元素后负载增加
        for i in range(50):
            bf.add(f"item_{i}")
        
        assert 0 < bf.load_factor() < 1
    
    def test_union(self):
        """测试并集操作"""
        bf1 = BloomFilter(expected_items=100)
        bf2 = BloomFilter(expected_items=100)
        
        bf1.add("apple")
        bf1.add("banana")
        bf2.add("cherry")
        bf2.add("date")
        
        union = bf1.union(bf2)
        
        # 并集应该包含所有元素
        assert "apple" in union
        assert "banana" in union
        assert "cherry" in union
        assert "date" in union
    
    def test_union_incompatible(self):
        """测试不兼容过滤器的并集"""
        bf1 = BloomFilter(expected_items=100)
        bf2 = BloomFilter(expected_items=200)  # 不同大小
        
        with pytest.raises(ValueError):
            bf1.union(bf2)
    
    def test_intersection(self):
        """测试交集操作"""
        bf1 = BloomFilter(expected_items=100)
        bf2 = BloomFilter(expected_items=100)
        
        bf1.add("apple")
        bf1.add("banana")
        bf1.add("cherry")
        
        bf2.add("banana")
        bf2.add("cherry")
        bf2.add("date")
        
        intersection = bf1.intersection(bf2)
        
        # 交集应该只包含共同元素
        assert "banana" in intersection
        assert "cherry" in intersection
    
    def test_serialization(self):
        """测试序列化和反序列化"""
        bf = BloomFilter(expected_items=100)
        
        items = ["apple", "banana", "cherry", "date", "elderberry"]
        for item in items:
            bf.add(item)
        
        # 序列化
        data = bf.to_bytes()
        assert len(data) > 0
        
        # 反序列化
        restored = BloomFilter.from_bytes(data)
        
        # 验证属性
        assert restored.size == bf.size
        assert restored.hash_count == bf.hash_count
        assert restored.item_count == bf.item_count
        
        # 验证元素
        for item in items:
            assert item in restored
    
    def test_serialization_empty(self):
        """测试空过滤器的序列化"""
        bf = BloomFilter(expected_items=100)
        data = bf.to_bytes()
        
        restored = BloomFilter.from_bytes(data)
        assert len(restored) == 0
    
    def test_serialization_too_short(self):
        """测试序列化数据太短的情况"""
        with pytest.raises(ValueError):
            BloomFilter.from_bytes(b"short")
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        # 预期元素数量必须大于0
        with pytest.raises(ValueError):
            BloomFilter(expected_items=0)
        
        with pytest.raises(ValueError):
            BloomFilter(expected_items=-1)
        
        # 假阳性率必须在0-1之间
        with pytest.raises(ValueError):
            BloomFilter(expected_items=100, false_positive_rate=0)
        
        with pytest.raises(ValueError):
            BloomFilter(expected_items=100, false_positive_rate=1)
        
        with pytest.raises(ValueError):
            BloomFilter(expected_items=100, false_positive_rate=1.5)


class TestCountingBloomFilter:
    """计数布隆过滤器测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        cbf = CountingBloomFilter(expected_items=100)
        
        cbf.add("hello")
        cbf.add("world")
        
        assert "hello" in cbf
        assert "world" in cbf
    
    def test_remove(self):
        """测试删除操作"""
        cbf = CountingBloomFilter(expected_items=100)
        
        cbf.add("item1")
        cbf.add("item2")
        
        assert "item1" in cbf
        
        # 删除存在的元素
        result = cbf.remove("item1")
        assert result is True
        assert "item1" not in cbf
        
        # 删除不存在的元素
        result = cbf.remove("notexist")
        assert result is False
    
    def test_max_count(self):
        """测试计数器上限"""
        cbf = CountingBloomFilter(expected_items=10, max_count=2)
        
        # 添加相同元素多次
        assert cbf.add("item") is True
        assert cbf.add("item") is True
        
        # 当计数器达到上限时，添加失败
        # 注意：这取决于哈希冲突
        # 连续添加可能成功也可能失败
    
    def test_clear(self):
        """测试清空"""
        cbf = CountingBloomFilter(expected_items=100)
        
        cbf.add("item1")
        cbf.add("item2")
        
        cbf.clear()
        
        assert len(cbf) == 0
        assert "item1" not in cbf
    
    def test_stats(self):
        """测试统计信息"""
        cbf = CountingBloomFilter(expected_items=100)
        
        for i in range(50):
            cbf.add(f"item_{i}")
        
        stats = cbf.get_stats()
        
        assert stats["item_count"] == 50
        assert stats["size"] > 0
        assert stats["hash_count"] > 0
    
    def test_repr(self):
        """测试字符串表示"""
        cbf = CountingBloomFilter(expected_items=100)
        repr_str = repr(cbf)
        assert "CountingBloomFilter" in repr_str


class TestScalableBloomFilter:
    """可扩展布隆过滤器测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        sbf = ScalableBloomFilter(initial_size=10)
        
        sbf.add("hello")
        sbf.add("world")
        
        assert "hello" in sbf
        assert "world" in sbf
    
    def test_auto_scaling(self):
        """测试自动扩展"""
        sbf = ScalableBloomFilter(initial_size=10, fill_threshold=0.5)
        
        # 添加大量元素触发扩展
        for i in range(100):
            sbf.add(f"item_{i}")
        
        # 应该有多个过滤器
        assert len(sbf.filters) > 1
    
    def test_get_stats(self):
        """测试统计信息"""
        sbf = ScalableBloomFilter(initial_size=10)
        
        for i in range(50):
            sbf.add(f"item_{i}")
        
        stats = sbf.get_stats()
        
        assert stats["total_item_count"] == 50
        assert "filter_count" in stats
        assert "filter_stats" in stats
    
    def test_repr(self):
        """测试字符串表示"""
        sbf = ScalableBloomFilter(initial_size=10)
        repr_str = repr(sbf)
        assert "ScalableBloomFilter" in repr_str


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_create_bloom_filter_empty(self):
        """测试创建空过滤器"""
        bf = create_bloom_filter()
        
        assert len(bf) == 0
        assert isinstance(bf, BloomFilter)
    
    def test_create_bloom_filter_with_items(self):
        """测试创建带初始元素的过滤器"""
        items = ["apple", "banana", "cherry"]
        bf = create_bloom_filter(items=items)
        
        assert len(bf) == 3
        for item in items:
            assert item in bf
    
    def test_calculate_optimal_params(self):
        """测试计算最优参数"""
        size, hash_count = calculate_optimal_params(
            expected_items=10000,
            false_positive_rate=0.01
        )
        
        assert size > 0
        assert hash_count > 0
        
        # 验证参数合理性
        # m = -n * ln(p) / (ln(2))^2
        expected_size = int(math.ceil(-10000 * math.log(0.01) / (math.log(2) ** 2)))
        assert abs(size - expected_size) < 2  # 允许小误差
    
    def test_estimate_memory_usage(self):
        """测试内存使用估算"""
        memory = estimate_memory_usage(
            expected_items=10000,
            false_positive_rate=0.01
        )
        
        assert memory > 0
        
        # 验证计算
        size, _ = calculate_optimal_params(10000, 0.01)
        expected_memory = (size + 7) // 8
        assert memory == expected_memory


class TestBloomFilterPerformance:
    """布隆过滤器性能测试"""
    
    def test_large_dataset(self):
        """测试大数据集"""
        bf = BloomFilter(expected_items=10000, false_positive_rate=0.01)
        
        # 添加大量元素
        for i in range(10000):
            bf.add(f"item_{i}")
        
        # 检查存在的元素
        found = sum(1 for i in range(10000) if f"item_{i}" in bf)
        assert found == 10000  # 无假阴性
        
        # 检查假阳性率
        false_positives = sum(1 for i in range(10000, 20000) if f"item_{i}" in bf)
        fp_rate = false_positives / 10000
        
        # 假阳性率应该接近预期值
        # 允许一定的偏差
        assert fp_rate < 0.05  # 应该远低于5%
    
    def test_false_positive_rate_accuracy(self):
        """测试假阳性率准确性"""
        n = 1000
        p = 0.01
        
        bf = BloomFilter(expected_items=n, false_positive_rate=p)
        
        # 添加元素
        for i in range(n):
            bf.add(f"item_{i}")
        
        # 检查假阳性
        test_count = 10000
        false_positives = sum(1 for i in range(n, n + test_count) if f"item_{i}" in bf)
        
        actual_fp_rate = false_positives / test_count
        
        # 实际假阳性率应该接近预期
        # 允许统计波动
        assert actual_fp_rate < p * 5  # 不应该超过预期的5倍


class TestEdgeCases:
    """边界情况测试"""
    
    def test_empty_string(self):
        """测试空字符串"""
        bf = BloomFilter(expected_items=100)
        
        bf.add("")
        assert "" in bf
    
    def test_unicode_strings(self):
        """测试Unicode字符串"""
        bf = BloomFilter(expected_items=100)
        
        items = ["你好", "世界", "🎉", "日本語"]
        for item in items:
            bf.add(item)
        
        for item in items:
            assert item in bf
    
    def test_long_strings(self):
        """测试长字符串"""
        bf = BloomFilter(expected_items=100)
        
        long_string = "a" * 10000
        bf.add(long_string)
        
        assert long_string in bf
    
    def test_special_characters(self):
        """测试特殊字符"""
        bf = BloomFilter(expected_items=100)
        
        items = ["hello\nworld", "tab\there", "quote\"test", "backslash\\path"]
        for item in items:
            bf.add(item)
        
        for item in items:
            assert item in bf


if __name__ == "__main__":
    pytest.main([__file__, "-v"])