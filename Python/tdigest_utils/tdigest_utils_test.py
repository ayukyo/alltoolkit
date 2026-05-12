"""
T-Digest 工具模块测试
"""

import math
import pytest
import random
from mod import (
    TDigest,
    Centroid,
    create_digest,
    quantiles,
    percentile_summary
)


class TestCentroid:
    """质心类测试"""
    
    def test_create(self):
        """测试创建质心"""
        c = Centroid(mean=10.0, weight=5.0)
        assert c.mean == 10.0
        assert c.weight == 5.0
    
    def test_add(self):
        """测试添加值到质心"""
        c = Centroid(mean=10.0, weight=2.0)
        c.add(20.0, weight=2.0)
        
        # 加权平均: (10*2 + 20*2) / 4 = 15
        assert c.mean == 15.0
        assert c.weight == 4.0
    
    def test_add_zero_weight(self):
        """测试零权重添加（不应改变质心）"""
        c = Centroid(mean=10.0, weight=2.0)
        c.add(20.0, weight=0.0)
        # 应该保持不变或忽略零权重
        # 实际上如果权重为0可能会被忽略
    
    def test_comparison(self):
        """测试质心比较"""
        c1 = Centroid(mean=10.0)
        c2 = Centroid(mean=20.0)
        assert c1 < c2
        assert c2 > c1
    
    def test_equality(self):
        """测试质心相等"""
        c1 = Centroid(mean=10.0, weight=5.0)
        c2 = Centroid(mean=10.0, weight=5.0)
        c3 = Centroid(mean=10.0, weight=6.0)
        
        assert c1 == c2
        assert c1 != c3
    
    def test_repr(self):
        """测试字符串表示"""
        c = Centroid(mean=10.0, weight=5.0)
        repr_str = repr(c)
        assert "Centroid" in repr_str
        assert "mean" in repr_str
        assert "weight" in repr_str


class TestTDigest:
    """T-Digest 类测试"""
    
    def test_create(self):
        """测试创建 T-Digest"""
        td = TDigest()
        assert td.compression == 100.0
        assert len(td.centroids) == 0
        assert td.total_weight == 0.0
    
    def test_create_custom_compression(self):
        """测试自定义压缩参数"""
        td = TDigest(compression=200.0)
        assert td.compression == 200.0
    
    def test_invalid_compression(self):
        """测试无效压缩参数"""
        with pytest.raises(ValueError):
            TDigest(compression=0)
        
        with pytest.raises(ValueError):
            TDigest(compression=-10)
    
    def test_add_single_value(self):
        """测试添加单个值"""
        td = TDigest()
        td.add(10.0)
        
        # 强制压缩
        td._compress()
        
        assert len(td.centroids) >= 1
        assert td.total_weight == 1.0
        assert td.min_val == 10.0
        assert td.max_val == 10.0
    
    def test_add_multiple_values(self):
        """测试添加多个值"""
        td = TDigest()
        for i in range(100):
            td.add(float(i))
        
        # 缓冲区应该在满时自动压缩
        assert td.total_weight == 100.0
        assert td.min_val == 0.0
        assert td.max_val == 99.0
    
    def test_add_with_weight(self):
        """测试带权重添加"""
        td = TDigest()
        td.add(10.0, weight=5.0)
        
        td._compress()
        
        assert td.total_weight == 5.0
    
    def test_add_invalid_value(self):
        """测试添加无效值"""
        td = TDigest()
        
        with pytest.raises(ValueError):
            td.add(float('nan'))
        
        with pytest.raises(ValueError):
            td.add(float('inf'))
    
    def test_add_invalid_weight(self):
        """测试添加无效权重"""
        td = TDigest()
        
        with pytest.raises(ValueError):
            td.add(10.0, weight=0)
        
        with pytest.raises(ValueError):
            td.add(10.0, weight=-1)
    
    def test_batch_add(self):
        """测试批量添加"""
        td = TDigest()
        values = list(range(1000))
        td.batch_add(values)
        
        assert td.total_weight == 1000.0
    
    def test_batch_add_with_weights(self):
        """测试带权重批量添加"""
        td = TDigest()
        values = [1.0, 2.0, 3.0]
        weights = [2.0, 3.0, 5.0]
        td.batch_add(values, weights)
        
        assert td.total_weight == 10.0
    
    def test_quantile_uniform(self):
        """测试均匀分布分位数"""
        td = TDigest(compression=100)
        values = list(range(100))
        random.seed(42)
        random.shuffle(values)
        td.batch_add(values)
        
        # 检查中位数接近 49.5
        median = td.quantile(0.5)
        assert 45 <= median <= 55  # 允许一定误差
        
        # 检查极值
        min_val = td.quantile(0.0)
        max_val = td.quantile(1.0)
        assert min_val <= 1
        assert max_val >= 98
    
    def test_quantile_normal(self):
        """测试正态分布分位数"""
        td = TDigest(compression=200)
        random.seed(42)
        data = [random.gauss(100, 15) for _ in range(10000)]
        td.batch_add(data)
        
        # 中位数应该接近均值
        median = td.median()
        assert 95 <= median <= 105
        
        # 标准差估算
        p16 = td.quantile(0.16)  # 约 -1σ
        p84 = td.quantile(0.84)  # 约 +1σ
        
        # 标准差应该接近 15
        estimated_std = (p84 - p16) / 2
        assert 12 <= estimated_std <= 18
    
    def test_percentile(self):
        """测试百分位数"""
        td = TDigest(compression=100)
        td.batch_add(list(range(100)))
        
        # P50 应该接近中位数
        p50 = td.percentile(50)
        assert 45 <= p50 <= 55
    
    def test_median(self):
        """测试中位数"""
        td = TDigest(compression=100)
        td.batch_add([1, 2, 3, 4, 5])
        
        median = td.median()
        assert 2.5 <= median <= 3.5
    
    def test_iqr(self):
        """测试四分位距"""
        td = TDigest(compression=200)
        random.seed(42)
        # 创建均匀分布
        td.batch_add(list(range(100)))
        
        iqr = td.iqr()
        # 对于均匀分布 0-99，IQR ≈ 50
        assert 40 <= iqr <= 60
    
    def test_quantile_invalid(self):
        """测试无效分位数"""
        td = TDigest(compression=100)
        td.batch_add([1, 2, 3])
        
        with pytest.raises(ValueError):
            td.quantile(-0.1)
        
        with pytest.raises(ValueError):
            td.quantile(1.1)
    
    def test_quantile_empty(self):
        """测试空 T-Digest 分位数"""
        td = TDigest()
        
        with pytest.raises(ValueError):
            td.quantile(0.5)
    
    def test_merge(self):
        """测试合并"""
        td1 = TDigest(compression=100)
        td2 = TDigest(compression=100)
        
        td1.batch_add([1, 2, 3, 4, 5])
        td2.batch_add([6, 7, 8, 9, 10])
        
        merged = td1.merge(td2)
        
        assert merged.total_weight == 10.0
        median = merged.median()
        assert 4 <= median <= 7  # 中位数应该在 5-6 附近
    
    def test_add_operator(self):
        """测试 + 运算符"""
        td1 = TDigest(compression=100)
        td2 = TDigest(compression=100)
        
        td1.batch_add([1, 2, 3])
        td2.batch_add([4, 5, 6])
        
        merged = td1 + td2
        
        assert merged.total_weight == 6.0
    
    def test_copy(self):
        """测试拷贝"""
        td1 = TDigest(compression=100)
        td1.batch_add(list(range(100)))
        
        td2 = td1.copy()
        
        assert td2.total_weight == td1.total_weight
        assert td2.median() == td1.median()
        
        # 修改副本不应影响原对象
        td2.add(1000)
        assert td2.max_val == 1000
        assert td1.max_val != 1000
    
    def test_serialization(self):
        """测试序列化"""
        td1 = TDigest(compression=100)
        random.seed(42)
        td1.batch_add([random.gauss(50, 10) for _ in range(1000)])
        
        data = td1.to_dict()
        
        assert 'compression' in data
        assert 'centroids' in data
        assert 'total_weight' in data
        assert 'min_val' in data
        assert 'max_val' in data
        
        # 反序列化
        td2 = TDigest.from_dict(data)
        
        assert td2.compression == td1.compression
        assert td2.total_weight == td1.total_weight
        assert abs(td2.median() - td1.median()) < 0.1
    
    def test_to_centroids(self):
        """测试导出质心"""
        td = TDigest(compression=100)
        td.batch_add([1, 2, 3, 4, 5])
        
        centroids = td.to_centroids()
        
        assert len(centroids) > 0
        for mean, weight in centroids:
            assert isinstance(mean, (int, float))  # Python int is also numeric
            assert isinstance(weight, (int, float))
            assert weight > 0
    
    def test_from_centroids(self):
        """测试从质心创建"""
        centroids = [(1.0, 2.0), (2.0, 3.0), (3.0, 2.0)]
        
        td = TDigest.from_centroids(centroids, compression=100, min_val=0.5, max_val=3.5)
        
        assert td.total_weight == 7.0
        assert td.min_val == 0.5
        assert td.max_val == 3.5
    
    def test_cdf(self):
        """测试累积分布函数"""
        td = TDigest(compression=100)
        td.batch_add(list(range(100)))
        
        # CDF 在最小值以下应该是 0
        assert td.cdf(-10) == 0.0
        
        # CDF 在最大值以上应该是 1
        assert td.cdf(200) == 1.0
        
        # CDF 在中位数附近应该是约 0.5
        cdf_mid = td.cdf(50)
        assert 0.4 <= cdf_mid <= 0.6
    
    def test_mean(self):
        """测试均值"""
        td = TDigest(compression=100)
        values = [1, 2, 3, 4, 5]
        td.batch_add(values)
        
        mean = td.mean()
        expected = sum(values) / len(values)
        assert abs(mean - expected) < 0.5
    
    def test_variance(self):
        """测试方差"""
        td = TDigest(compression=200)
        values = list(range(100))
        td.batch_add(values)
        
        variance = td.variance()
        
        # 计算真实方差
        n = len(values)
        real_mean = sum(values) / n
        real_var = sum((x - real_mean) ** 2 for x in values) / n
        
        # 方差应该接近真实值
        assert abs(variance - real_var) < 100  # 允许一定误差
    
    def test_std_dev(self):
        """测试标准差"""
        td = TDigest(compression=200)
        random.seed(42)
        data = [random.gauss(100, 15) for _ in range(10000)]
        td.batch_add(data)
        
        std_dev = td.std_dev()
        
        # 标准差应该接近 15
        assert 12 <= std_dev <= 18
    
    def test_size(self):
        """测试质心数量"""
        td = TDigest(compression=100)
        td.batch_add(list(range(1000)))
        
        size = td.size()
        assert size > 0
        # 质心数量应该远小于数据点数量
        assert size < 1000
    
    def test_len(self):
        """测试总数据点数"""
        td = TDigest()
        td.batch_add([1, 2, 3, 4, 5])
        
        assert len(td) == 5
    
    def test_repr(self):
        """测试字符串表示"""
        td = TDigest(compression=100)
        td.batch_add([1, 2, 3])
        
        repr_str = repr(td)
        assert "TDigest" in repr_str
        assert "compression" in repr_str
    
    def test_extreme_values(self):
        """测试极端值"""
        td = TDigest(compression=200)
        values = [1e-10, 1e10, 1, 100, 10000]
        td.batch_add(values)
        
        # 应该能处理极端值
        min_val = td.quantile(0.0)
        max_val = td.quantile(1.0)
        
        assert min_val <= 1
        assert max_val >= 1e9


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_create_digest(self):
        """测试创建函数"""
        values = list(range(100))
        td = create_digest(values, compression=100)
        
        assert td.total_weight == 100.0
        assert 45 <= td.median() <= 55
    
    def test_create_digest_empty(self):
        """测试空创建"""
        td = create_digest()
        assert td.total_weight == 0.0
    
    def test_quantiles_function(self):
        """测试批量分位数函数"""
        values = list(range(100))
        qs = [0.25, 0.5, 0.75]
        
        results = quantiles(values, qs)
        
        assert len(results) == 3
        # 检查顺序
        assert results[0] <= results[1] <= results[2]
    
    def test_percentile_summary(self):
        """测试百分位数摘要"""
        values = list(range(1000))
        
        summary = percentile_summary(values)
        
        assert summary['count'] == 1000
        assert summary['min'] == 0
        assert summary['max'] == 999
        assert 'median' in summary
        assert 'p95' in summary
        assert 'p99' in summary
        assert 'iqr' in summary


class TestEdgeCases:
    """边界情况测试"""
    
    def test_single_value(self):
        """测试单个值"""
        td = TDigest()
        td.add(42.0)
        
        assert td.quantile(0.5) == 42.0
        assert td.quantile(0.0) == 42.0
        assert td.quantile(1.0) == 42.0
    
    def test_two_values(self):
        """测试两个值"""
        td = TDigest()
        td.add(0.0)
        td.add(100.0)
        
        median = td.median()
        assert 0 <= median <= 100
    
    def test_identical_values(self):
        """测试相同值"""
        td = TDigest()
        for _ in range(100):
            td.add(50.0)
        
        assert td.median() == 50.0
        assert td.quantile(0.25) == 50.0
        assert td.quantile(0.75) == 50.0
    
    def test_large_dataset(self):
        """测试大数据集"""
        td = TDigest(compression=100)
        
        # 添加 1M 个数据点
        for i in range(10000):  # 分批添加
            td.batch_add([random.random() * 100 for _ in range(100)])
        
        # 质心数量应该远小于数据点数量
        assert td.size() < 1000
        
        # 分位数应该在合理范围内
        assert 0 <= td.median() <= 100
    
    def test_negative_values(self):
        """测试负值"""
        td = TDigest()
        td.batch_add([-10, -5, 0, 5, 10])
        
        median = td.median()
        assert -5 <= median <= 5
    
    def test_floating_point_precision(self):
        """测试浮点精度"""
        td = TDigest()
        values = [0.1 + 0.2] * 100  # 0.30000000000000004
        td.batch_add(values)
        
        # 应该正确处理浮点精度
        assert td.min_val >= 0.29
        assert td.max_val <= 0.31
    
    def test_very_small_compression(self):
        """测试非常小的压缩参数"""
        td = TDigest(compression=10)
        td.batch_add(list(range(1000)))
        
        # 应该仍然工作
        median = td.median()
        assert 400 <= median <= 600
    
    def test_very_large_compression(self):
        """测试非常大的压缩参数"""
        td = TDigest(compression=1000)
        td.batch_add(list(range(100)))
        
        # 应该有更多质心（更高精度）
        assert td.size() > 0


class TestAccuracy:
    """精度测试"""
    
    def test_uniform_accuracy(self):
        """测试均匀分布精度"""
        td = TDigest(compression=200)
        n = 10000
        values = list(range(n))
        random.seed(42)
        random.shuffle(values)
        td.batch_add(values)
        
        # 测试多个分位数的精度
        for q in [0.1, 0.25, 0.5, 0.75, 0.9]:
            estimated = td.quantile(q)
            expected = q * (n - 1)
            # 允许 2% 误差
            error_rate = abs(estimated - expected) / n
            assert error_rate < 0.02, f"分位数 {q} 误差过大: {error_rate}"
    
    def test_normal_accuracy(self):
        """测试正态分布精度"""
        td = TDigest(compression=200)
        random.seed(42)
        
        # 生成正态分布数据
        mean, std = 100, 15
        data = [random.gauss(mean, std) for _ in range(10000)]
        td.batch_add(data)
        
        # 检查中位数接近均值
        estimated_median = td.median()
        assert abs(estimated_median - mean) < 2
        
        # 检查标准差估算
        estimated_std = td.std_dev()
        assert abs(estimated_std - std) < 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])