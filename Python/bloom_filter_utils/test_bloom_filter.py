"""
布隆过滤器工具集测试 (Bloom Filter Utils Tests)

测试覆盖：
- 布隆过滤器基础操作
- 计数布隆过滤器
- 可扩展布隆过滤器
- 可删除布隆过滤器
- 参数计算
- 序列化/反序列化
- 边界情况
"""

import math
import pytest
from bloom_filter import (
    BloomFilter,
    CountingBloomFilter,
    ScalableBloomFilter,
    DeletableBloomFilter,
    BloomFilterBuilder,
    BloomFilterStats,
    optimal_num_bits,
    optimal_num_hashes,
    estimate_false_positive_rate,
    create_bloom_filter,
    create_optimal_bloom_filter,
)


class TestOptimalParameters:
    """测试最优参数计算"""
    
    def test_optimal_num_bits_basic(self):
        """基础位数组大小计算"""
        m = optimal_num_bits(1000, 0.01)
        # m = -n * ln(p) / (ln(2)^2)
        expected = math.ceil(-1000 * math.log(0.01) / (math.log(2) ** 2))
        assert m == expected
    
    def test_optimal_num_bits_zero_capacity(self):
        """零容量返回1"""
        assert optimal_num_bits(0, 0.01) == 1
    
    def test_optimal_num_bits_invalid_error_rate(self):
        """无效假阳性率处理"""
        assert optimal_num_bits(1000, 0) == optimal_num_bits(1000, 1e-10)
        assert optimal_num_bits(1000, 1) == 1
    
    def test_optimal_num_hashes_basic(self):
        """基础哈希函数数量计算"""
        k = optimal_num_hashes(9585, 1000)  # 典型值
        # k = (m / n) * ln(2)
        expected = max(1, round((9585 / 1000) * math.log(2)))
        assert k == expected
    
    def test_optimal_num_hashes_zero_capacity(self):
        """零容量返回1"""
        assert optimal_num_hashes(1000, 0) == 1
        assert optimal_num_hashes(0, 1000) == 1
    
    def test_estimate_false_positive_rate_empty(self):
        """空过滤器假阳性率为0"""
        rate = estimate_false_positive_rate(1000, 0, 7)
        assert rate == 0.0
    
    def test_estimate_false_positive_rate_basic(self):
        """基础假阳性率计算"""
        rate = estimate_false_positive_rate(9585, 1000, 7)
        assert 0 < rate < 0.02  # 应该接近设计假阳性率
    
    def test_estimate_false_positive_rate_invalid(self):
        """无效参数处理"""
        assert estimate_false_positive_rate(0, 100, 7) == 1.0
        assert estimate_false_positive_rate(1000, 100, 0) == 1.0


class TestBloomFilterBasic:
    """测试布隆过滤器基础功能"""
    
    def test_init(self):
        """测试初始化"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        assert bf.capacity == 1000
        assert bf.error_rate == 0.01
        assert bf.size_bits > 0
        assert bf.num_hashes > 0
        assert bf.is_empty
        assert len(bf) == 0
    
    def test_init_invalid_capacity(self):
        """无效容量抛出异常"""
        with pytest.raises(ValueError):
            BloomFilter(capacity=0, error_rate=0.01)
        with pytest.raises(ValueError):
            BloomFilter(capacity=-1, error_rate=0.01)
    
    def test_init_invalid_error_rate(self):
        """无效假阳性率抛出异常"""
        with pytest.raises(ValueError):
            BloomFilter(capacity=1000, error_rate=0)
        with pytest.raises(ValueError):
            BloomFilter(capacity=1000, error_rate=1)
        with pytest.raises(ValueError):
            BloomFilter(capacity=1000, error_rate=-0.1)
    
    def test_add_and_contains_string(self):
        """添加和检查字符串"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        bf.add("hello")
        bf.add("world")
        
        assert "hello" in bf
        assert "world" in bf
        assert "foo" not in bf
        assert len(bf) == 2
    
    def test_add_and_contains_bytes(self):
        """添加和检查字节"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        bf.add(b"hello")
        bf.add(b"world")
        
        assert b"hello" in bf
        assert b"world" in bf
        assert b"foo" not in bf
    
    def test_add_and_contains_integers(self):
        """添加和检查整数"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        bf.add(1)
        bf.add(2)
        bf.add(3)
        
        assert 1 in bf
        assert 2 in bf
        assert 3 in bf
        assert 4 not in bf
    
    def test_add_and_contains_various_types(self):
        """添加和检查各种类型"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        bf.add("string")
        bf.add(123)
        bf.add(45.67)
        bf.add((1, 2, 3))
        bf.add([1, 2, 3])  # 列表会被转为字符串
    
    def test_contains_method(self):
        """contains 方法"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        bf.add("test")
        
        assert bf.contains("test")
        assert not bf.contains("not_test")
    
    def test_might_contain_method(self):
        """might_contain 方法"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        bf.add("test")
        
        assert bf.might_contain("test")
        assert not bf.might_contain("not_test")
    
    def test_update_batch(self):
        """批量添加"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        items = ["a", "b", "c", "d", "e"]
        bf.update(items)
        
        assert len(bf) == 5
        for item in items:
            assert item in bf
    
    def test_update_set(self):
        """批量添加集合"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        items = {"apple", "banana", "cherry"}
        bf.update(items)
        
        assert len(bf) == 3
    
    def test_clear(self):
        """清空过滤器"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        bf.add("test1")
        bf.add("test2")
        assert len(bf) == 2
        
        bf.clear()
        
        assert len(bf) == 0
        assert bf.is_empty
        assert "test1" not in bf
    
    def test_copy(self):
        """复制过滤器"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        bf.add("test")
        
        bf_copy = bf.copy()
        
        assert len(bf_copy) == 1
        assert "test" in bf_copy
        
        # 修改副本不影响原对象
        bf_copy.add("new")
        assert "new" in bf_copy
        assert "new" not in bf


class TestBloomFilterStats:
    """测试统计信息"""
    
    def test_stats(self):
        """统计信息"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        for i in range(100):
            bf.add(f"item_{i}")
        
        stats = bf.stats()
        
        assert stats.capacity == 1000
        assert stats.error_rate == 0.01
        assert stats.num_elements == 100
        assert 0 <= stats.fill_ratio <= 1
        assert 0 <= stats.estimated_error_rate <= 1
    
    def test_fill_ratio(self):
        """填充率"""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        
        # 空过滤器填充率为 0
        assert bf.fill_ratio == 0.0
        
        # 添加元素后填充率增加
        for i in range(100):
            bf.add(f"item_{i}")
        
        assert bf.fill_ratio > 0


class TestBloomFilterUnion:
    """测试并集操作"""
    
    def test_union_basic(self):
        """基础并集"""
        bf1 = BloomFilter(capacity=1000, error_rate=0.01)
        bf2 = BloomFilter(capacity=1000, error_rate=0.01)
        
        bf1.add("a")
        bf1.add("b")
        
        bf2.add("c")
        bf2.add("d")
        
        union = bf1.union(bf2)
        
        assert "a" in union
        assert "b" in union
        assert "c" in union
        assert "d" in union
    
    def test_union_same_element(self):
        """相同元素并集"""
        bf1 = BloomFilter(capacity=1000, error_rate=0.01)
        bf2 = BloomFilter(capacity=1000, error_rate=0.01)
        
        bf1.add("a")
        bf2.add("a")
        
        union = bf1.union(bf2)
        
        assert "a" in union
    
    def test_union_different_size_error(self):
        """不同大小抛出异常"""
        bf1 = BloomFilter(capacity=1000, error_rate=0.01)
        bf2 = BloomFilter(capacity=2000, error_rate=0.01)
        
        with pytest.raises(ValueError):
            bf1.union(bf2)
    
    def test_intersect_approx(self):
        """近似交集"""
        bf1 = BloomFilter(capacity=1000, error_rate=0.01)
        bf2 = BloomFilter(capacity=1000, error_rate=0.01)
        
        bf1.add("a")
        bf1.add("b")
        bf1.add("common")
        
        bf2.add("c")
        bf2.add("d")
        bf2.add("common")
        
        intersect = bf1.intersect_approx(bf2)
        
        # "common" 应该在交集中
        assert "common" in intersect


class TestBloomFilterSerialization:
    """测试序列化"""
    
    def test_to_bytes_and_from_bytes(self):
        """序列化和反序列化"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        items = ["hello", "world", "foo", "bar"]
        for item in items:
            bf.add(item)
        
        # 序列化
        data = bf.to_bytes()
        assert isinstance(data, bytes)
        assert len(data) > 0
        
        # 反序列化
        bf2 = BloomFilter.from_bytes(data)
        
        assert bf2.capacity == bf.capacity
        assert bf2.error_rate == bf.error_rate
        assert bf2.num_hashes == bf.num_hashes
        assert bf2.size_bits == bf.size_bits
        assert len(bf2) == len(bf)
        
        # 验证元素
        for item in items:
            assert item in bf2
    
    def test_serialization_preserves_filter_state(self):
        """序列化保持过滤器状态"""
        bf = BloomFilter(capacity=10000, error_rate=0.001)
        
        for i in range(1000):
            bf.add(f"item_{i}")
        
        data = bf.to_bytes()
        bf2 = BloomFilter.from_bytes(data)
        
        assert bf2.fill_ratio == bf.fill_ratio
    
    def test_from_bytes_invalid_data(self):
        """无效数据反序列化"""
        with pytest.raises(ValueError):
            BloomFilter.from_bytes(b"invalid")


class TestCountingBloomFilter:
    """测试计数布隆过滤器"""
    
    def test_init(self):
        """测试初始化"""
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        assert len(cbf) == 0
    
    def test_add_and_contains(self):
        """添加和检查"""
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        
        cbf.add("hello")
        assert "hello" in cbf
        assert len(cbf) == 1
    
    def test_remove(self):
        """删除元素"""
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        
        cbf.add("hello")
        assert "hello" in cbf
        
        result = cbf.remove("hello")
        assert result is True
        assert "hello" not in cbf
        assert len(cbf) == 0
    
    def test_remove_nonexistent(self):
        """删除不存在的元素"""
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        
        result = cbf.remove("nonexistent")
        assert result is False
    
    def test_add_multiple_remove(self):
        """多次添加和删除"""
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        
        # 同一元素添加多次
        cbf.add("test")
        cbf.add("test")
        
        # 删除一次后仍存在
        cbf.remove("test")
        assert "test" in cbf
        
        # 再次删除后不存在
        cbf.remove("test")
        assert "test" not in cbf
    
    def test_clear(self):
        """清空计数布隆过滤器"""
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        
        cbf.add("a")
        cbf.add("b")
        cbf.add("c")
        
        cbf.clear()
        
        assert len(cbf) == 0
        assert "a" not in cbf
    
    def test_stats(self):
        """统计信息"""
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        
        for i in range(100):
            cbf.add(f"item_{i}")
        
        stats = cbf.stats()
        
        assert stats.capacity == 1000
        assert stats.num_elements == 100
    
    def test_counter_overflow(self):
        """计数器溢出"""
        # 4位计数器最大值15
        cbf = CountingBloomFilter(capacity=10, error_rate=0.1, counter_bits=4)
        
        # 添加同一元素16次，第16次应该失败
        for i in range(15):
            assert cbf.add("test") is True
        
        # 计数器已满
        assert cbf.add("test") is False


class TestScalableBloomFilter:
    """测试可扩展布隆过滤器"""
    
    def test_init(self):
        """测试初始化"""
        sbf = ScalableBloomFilter(initial_capacity=100, error_rate=0.01)
        assert sbf.num_filters == 1
        assert len(sbf) == 0
    
    def test_add_and_contains(self):
        """添加和检查"""
        sbf = ScalableBloomFilter(initial_capacity=100, error_rate=0.01)
        
        sbf.add("hello")
        assert "hello" in sbf
        assert len(sbf) == 1
    
    def test_auto_scaling(self):
        """自动扩容"""
        sbf = ScalableBloomFilter(initial_capacity=10, error_rate=0.01)
        
        # 添加超过初始容量的元素
        for i in range(100):
            sbf.add(f"item_{i}")
        
        # 应该扩容
        assert sbf.num_filters > 1
        assert len(sbf) == 100
        
        # 所有元素应该仍可查询
        for i in range(100):
            assert f"item_{i}" in sbf
    
    def test_deduplication(self):
        """重复元素会重复计数（不做去重检查）"""
        sbf = ScalableBloomFilter(initial_capacity=100, error_rate=0.01)
        
        sbf.add("test")
        sbf.add("test")  # 重复添加
        
        # ScalableBloomFilter 不做去重检查，所以计数会增加
        assert len(sbf) == 2
        assert "test" in sbf
    
    def test_clear(self):
        """清空"""
        sbf = ScalableBloomFilter(initial_capacity=100, error_rate=0.01)
        
        for i in range(50):
            sbf.add(f"item_{i}")
        
        sbf.clear()
        
        assert len(sbf) == 0
        assert sbf.num_filters == 1  # 重置为单个过滤器
    
    def test_total_bits(self):
        """总位数统计"""
        sbf = ScalableBloomFilter(initial_capacity=10, error_rate=0.01)
        
        for i in range(100):
            sbf.add(f"item_{i}")
        
        total = sbf.total_bits
        assert total > 0
    
    def test_estimated_error_rate(self):
        """估算假阳性率"""
        sbf = ScalableBloomFilter(initial_capacity=100, error_rate=0.01)
        
        for i in range(1000):
            sbf.add(f"item_{i}")
        
        rate = sbf.estimated_error_rate()
        assert 0 < rate < 1


class TestDeletableBloomFilter:
    """测试可删除布隆过滤器"""
    
    def test_init(self):
        """测试初始化"""
        dbf = DeletableBloomFilter(capacity=1000, error_rate=0.01)
        assert len(dbf) == 0
    
    def test_add_and_contains(self):
        """添加和检查"""
        dbf = DeletableBloomFilter(capacity=1000, error_rate=0.01)
        
        dbf.add("hello")
        assert "hello" in dbf
        assert len(dbf) == 1
    
    def test_remove(self):
        """删除元素"""
        dbf = DeletableBloomFilter(capacity=1000, error_rate=0.01)
        
        dbf.add("hello")
        assert "hello" in dbf
        
        result = dbf.remove("hello")
        assert result is True
        assert "hello" not in dbf
        assert len(dbf) == 0
    
    def test_remove_nonexistent(self):
        """删除不存在的元素"""
        dbf = DeletableBloomFilter(capacity=1000, error_rate=0.01)
        
        result = dbf.remove("nonexistent")
        assert result is False
    
    def test_clear(self):
        """清空"""
        dbf = DeletableBloomFilter(capacity=1000, error_rate=0.01)
        
        dbf.add("a")
        dbf.add("b")
        
        dbf.clear()
        
        assert len(dbf) == 0


class TestBloomFilterBuilder:
    """测试构建器"""
    
    def test_build_standard(self):
        """构建标准布隆过滤器"""
        bf = BloomFilterBuilder() \
            .with_capacity(1000) \
            .with_error_rate(0.01) \
            .build()
        
        assert isinstance(bf, BloomFilter)
        assert bf.capacity == 1000
        assert bf.error_rate == 0.01
    
    def test_build_with_items(self):
        """带初始元素构建"""
        items = ["a", "b", "c"]
        bf = BloomFilterBuilder() \
            .with_capacity(1000) \
            .with_items(items) \
            .build()
        
        assert len(bf) == 3
        for item in items:
            assert item in bf
    
    def test_build_counting(self):
        """构建计数布隆过滤器"""
        cbf = BloomFilterBuilder() \
            .with_capacity(1000) \
            .as_counting() \
            .build()
        
        assert isinstance(cbf, CountingBloomFilter)
    
    def test_build_scalable(self):
        """构建可扩展布隆过滤器"""
        sbf = BloomFilterBuilder() \
            .with_capacity(1000) \
            .as_scalable() \
            .build()
        
        assert isinstance(sbf, ScalableBloomFilter)
    
    def test_build_deletable(self):
        """构建可删除布隆过滤器"""
        dbf = BloomFilterBuilder() \
            .with_capacity(1000) \
            .as_deletable() \
            .build()
        
        assert isinstance(dbf, DeletableBloomFilter)
    
    def test_build_custom_parameters(self):
        """自定义参数构建"""
        bf = BloomFilterBuilder() \
            .with_capacity(5000) \
            .with_error_rate(0.001) \
            .with_num_hashes(10) \
            .with_size_bits(50000) \
            .build()
        
        assert bf.capacity == 5000
        assert bf.num_hashes == 10
        assert bf.size_bits == 50000


class TestConvenienceFunctions:
    """测试便捷函数"""
    
    def test_create_bloom_filter(self):
        """创建布隆过滤器"""
        bf = create_bloom_filter(1000, 0.01)
        
        assert isinstance(bf, BloomFilter)
        assert bf.capacity == 1000
        assert bf.error_rate == 0.01
    
    def test_create_optimal_bloom_filter(self):
        """创建最优布隆过滤器"""
        bf = create_optimal_bloom_filter(1000, acceptable_false_positives=1)
        
        assert isinstance(bf, BloomFilter)
        # 假阳性率应该接近 1/1000
        assert bf.error_rate <= 0.001
    
    def test_create_optimal_bloom_filter_invalid(self):
        """无效参数"""
        with pytest.raises(ValueError):
            create_optimal_bloom_filter(0)


class TestBloomFilterFalsePositiveRate:
    """测试假阳性率"""
    
    def test_no_false_negatives(self):
        """无假阴性"""
        bf = BloomFilter(capacity=10000, error_rate=0.01)
        
        items = [f"item_{i}" for i in range(1000)]
        for item in items:
            bf.add(item)
        
        # 所有已添加元素必须能查到
        for item in items:
            assert item in bf, f"False negative for {item}"
    
    def test_false_positive_rate_approximate(self):
        """假阳性率接近设计值"""
        capacity = 10000
        error_rate = 0.01
        
        bf = BloomFilter(capacity=capacity, error_rate=error_rate)
        
        # 添加元素
        for i in range(capacity):
            bf.add(f"item_{i}")
        
        # 测试假阳性
        false_positives = 0
        test_count = 10000
        
        for i in range(test_count):
            test_item = f"not_item_{i}"
            if test_item in bf:
                false_positives += 1
        
        actual_rate = false_positives / test_count
        
        # 假阳性率应该在设计值附近（允许一定误差）
        # 通常实际假阳性率会低于设计值
        assert actual_rate < error_rate * 3, f"False positive rate too high: {actual_rate}"


class TestUnicodeSupport:
    """测试 Unicode 支持"""
    
    def test_chinese(self):
        """中文字符"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        items = ["你好", "世界", "测试", "布隆过滤器"]
        for item in items:
            bf.add(item)
        
        for item in items:
            assert item in bf
    
    def test_emoji(self):
        """Emoji 支持"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        items = ["🎉", "🎊", "🎁", "🌟", "💻"]
        for item in items:
            bf.add(item)
        
        for item in items:
            assert item in bf
    
    def test_mixed_unicode(self):
        """混合 Unicode"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        items = ["Hello", "世界", "🌍", "123", "日本語"]
        for item in items:
            bf.add(item)
        
        for item in items:
            assert item in bf


class TestEdgeCases:
    """测试边界情况"""
    
    def test_single_element(self):
        """单个元素"""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        
        bf.add("only_one")
        
        assert "only_one" in bf
        assert "not_one" not in bf
        assert len(bf) == 1
    
    def test_empty_filter(self):
        """空过滤器"""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        
        assert bf.is_empty
        assert len(bf) == 0
        assert "anything" not in bf
    
    def test_very_small_error_rate(self):
        """极小假阳性率"""
        bf = BloomFilter(capacity=100, error_rate=0.0001)
        
        for i in range(100):
            bf.add(f"item_{i}")
        
        # 无假阴性
        for i in range(100):
            assert f"item_{i}" in bf
    
    def test_large_capacity(self):
        """大容量"""
        bf = BloomFilter(capacity=1000000, error_rate=0.01)
        
        # 添加少量元素
        for i in range(100):
            bf.add(f"item_{i}")
        
        for i in range(100):
            assert f"item_{i}" in bf
    
    def test_same_element_multiple_times(self):
        """同一元素多次添加"""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        
        for _ in range(100):
            bf.add("same")
        
        assert "same" in bf
        # 计数会增加，但元素只有一个
        assert len(bf) == 100


class TestRepr:
    """测试字符串表示"""
    
    def test_bloom_filter_repr(self):
        """BloomFilter repr"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        repr_str = repr(bf)
        
        assert "BloomFilter" in repr_str
        assert "capacity=1000" in repr_str
        assert "error_rate=0.01" in repr_str
    
    def test_bloom_filter_stats_repr(self):
        """BloomFilterStats repr"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        stats = bf.stats()
        repr_str = repr(stats)
        
        assert "BloomFilterStats" in repr_str
        assert "capacity" in repr_str
    
    def test_counting_bloom_filter_repr(self):
        """CountingBloomFilter repr"""
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        repr_str = repr(cbf)
        
        assert "CountingBloomFilter" in repr_str
    
    def test_scalable_bloom_filter_repr(self):
        """ScalableBloomFilter repr"""
        sbf = ScalableBloomFilter(initial_capacity=100, error_rate=0.01)
        repr_str = repr(sbf)
        
        assert "ScalableBloomFilter" in repr_str
    
    def test_deletable_bloom_filter_repr(self):
        """DeletableBloomFilter repr"""
        dbf = DeletableBloomFilter(capacity=1000, error_rate=0.01)
        repr_str = repr(dbf)
        
        assert "DeletableBloomFilter" in repr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])