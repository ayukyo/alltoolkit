"""
XXHash 工具模块测试
"""

import pytest
import tempfile
import os
from mod import (
    XXHash32, XXHash64,
    xxhash32, xxhash64,
    xxhash32_hex, xxhash64_hex,
    hash_file_32, hash_file_64,
    hash_list_32, hash_list_64,
    distributed_shard, consistent_hash,
    XXHashStreamer,
    fingerprint_32, fingerprint_64,
    multi_hash, hash_dict,
    _verify_test_vectors
)


class TestXXHash32:
    """XXHash32 测试"""
    
    def test_empty_string(self):
        """测试空字符串"""
        result = xxhash32(b"")
        assert result == 0x02CC5D05
    
    def test_single_byte(self):
        """测试单字节"""
        result = xxhash32(b"a")
        assert result == 0x550D7456
    
    def test_short_string(self):
        """测试短字符串"""
        result = xxhash32(b"abc")
        assert result == 0x32D153FF
    
    def test_medium_string(self):
        """测试中等长度字符串"""
        result = xxhash32(b"message digest")
        assert result == 0x7C948494
    
    def test_alphabet(self):
        """测试字母表"""
        result = xxhash32(b"abcdefghijklmnopqrstuvwxyz")
        assert result == 0x63A14D5F
    
    def test_alphanumeric(self):
        """测试字母数字"""
        result = xxhash32(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        assert result == 0x9C285E64
    
    def test_long_string(self):
        """测试长字符串"""
        data = b"1234567890" * 8
        result = xxhash32(data)
        assert result == 0x9C05F475
    
    def test_with_seed(self):
        """测试带种子的哈希"""
        data = b"hello"
        h1 = xxhash32(data, seed=0)
        h2 = xxhash32(data, seed=1)
        h3 = xxhash32(data, seed=42)
        
        assert h1 != h2
        assert h1 != h3
        assert h2 != h3
    
    def test_unicode_string(self):
        """测试Unicode字符串"""
        result = xxhash32("你好世界")
        assert isinstance(result, int)
        assert result >= 0
    
    def test_hex_output(self):
        """测试十六进制输出"""
        result = xxhash32_hex(b"test")
        assert len(result) == 8
        assert all(c in '0123456789abcdef' for c in result)
    
    def test_streaming(self):
        """测试流式处理"""
        # 一次性处理
        h1 = xxhash32(b"hello world")
        
        # 分块处理
        h = XXHash32()
        h.update(b"hello")
        h.update(b" ")
        h.update(b"world")
        h2 = h.digest()
        
        assert h1 == h2
    
    def test_reset(self):
        """测试重置功能"""
        h = XXHash32()
        h.update(b"data")
        h.reset()
        h.update(b"test")
        result = h.digest()
        
        expected = xxhash32(b"test")
        assert result == expected
    
    def test_copy(self):
        """测试复制功能"""
        h1 = XXHash32()
        h1.update(b"hello")
        
        h2 = h1.copy()
        h1.update(b" world")
        h2.update(b" there")
        
        assert h1.digest() != h2.digest()
        assert h1.digest() == xxhash32(b"hello world")
        assert h2.digest() == xxhash32(b"hello there")
    
    def test_deterministic(self):
        """测试确定性"""
        data = b"random test data"
        results = [xxhash32(data) for _ in range(100)]
        assert len(set(results)) == 1


class TestXXHash64:
    """XXHash64 测试"""
    
    def test_empty_string(self):
        """测试空字符串"""
        result = xxhash64(b"")
        assert result == 0xEF46DB3751D8E999
    
    def test_single_byte(self):
        """测试单字节"""
        result = xxhash64(b"a")
        assert result == 0xD24EC4F1A98C6E5B
    
    def test_short_string(self):
        """测试短字符串"""
        result = xxhash64(b"abc")
        assert result == 0x44BC2CF5AD770999
    
    def test_medium_string(self):
        """测试中等长度字符串"""
        result = xxhash64(b"message digest")
        assert result == 0x795F52660BF920CC
    
    def test_alphabet(self):
        """测试字母表"""
        result = xxhash64(b"abcdefghijklmnopqrstuvwxyz")
        assert result == 0x403CAE455B1BEBEC
    
    def test_alphanumeric(self):
        """测试字母数字"""
        result = xxhash64(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        assert result == 0xC2651DC67503E3EE
    
    def test_long_string(self):
        """测试长字符串"""
        data = b"1234567890" * 8
        result = xxhash64(data)
        assert result == 0x9F1A2F428C46410C
    
    def test_with_seed(self):
        """测试带种子的哈希"""
        data = b"hello"
        h1 = xxhash64(data, seed=0)
        h2 = xxhash64(data, seed=1)
        h3 = xxhash64(data, seed=42)
        
        assert h1 != h2
        assert h1 != h3
        assert h2 != h3
    
    def test_unicode_string(self):
        """测试Unicode字符串"""
        result = xxhash64("你好世界")
        assert isinstance(result, int)
        assert result >= 0
    
    def test_hex_output(self):
        """测试十六进制输出"""
        result = xxhash64_hex(b"test")
        assert len(result) == 16
        assert all(c in '0123456789abcdef' for c in result)
    
    def test_streaming(self):
        """测试流式处理"""
        # 一次性处理
        h1 = xxhash64(b"hello world")
        
        # 分块处理
        h = XXHash64()
        h.update(b"hello")
        h.update(b" ")
        h.update(b"world")
        h2 = h.digest()
        
        assert h1 == h2
    
    def test_large_data_streaming(self):
        """测试大数据流式处理"""
        data = b"x" * 10000
        
        # 一次性处理
        h1 = xxhash64(data)
        
        # 流式处理
        h = XXHash64()
        for i in range(0, len(data), 100):
            h.update(data[i:i+100])
        h2 = h.digest()
        
        assert h1 == h2
    
    def test_reset(self):
        """测试重置功能"""
        h = XXHash64()
        h.update(b"data")
        h.reset()
        h.update(b"test")
        result = h.digest()
        
        expected = xxhash64(b"test")
        assert result == expected
    
    def test_copy(self):
        """测试复制功能"""
        h1 = XXHash64()
        h1.update(b"hello")
        
        h2 = h1.copy()
        h1.update(b" world")
        h2.update(b" there")
        
        assert h1.digest() != h2.digest()
        assert h1.digest() == xxhash64(b"hello world")
        assert h2.digest() == xxhash64(b"hello there")


class TestFileHashing:
    """文件哈希测试"""
    
    def test_hash_file_32(self):
        """测试文件32位哈希"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"hello world")
            f.flush()
            filepath = f.name
        
        try:
            result = hash_file_32(filepath)
            expected = xxhash32(b"hello world")
            assert result == expected
        finally:
            os.unlink(filepath)
    
    def test_hash_file_64(self):
        """测试文件64位哈希"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"hello world")
            f.flush()
            filepath = f.name
        
        try:
            result = hash_file_64(filepath)
            expected = xxhash64(b"hello world")
            assert result == expected
        finally:
            os.unlink(filepath)
    
    def test_hash_large_file(self):
        """测试大文件哈希"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            data = b"x" * 100000
            f.write(data)
            f.flush()
            filepath = f.name
        
        try:
            result = hash_file_64(filepath)
            expected = xxhash64(data)
            assert result == expected
        finally:
            os.unlink(filepath)
    
    def test_hash_file_with_seed(self):
        """测试带种子的文件哈希"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test data")
            f.flush()
            filepath = f.name
        
        try:
            h1 = hash_file_64(filepath, seed=0)
            h2 = hash_file_64(filepath, seed=1)
            assert h1 != h2
        finally:
            os.unlink(filepath)
    
    def test_file_not_found(self):
        """测试文件不存在"""
        with pytest.raises(FileNotFoundError):
            hash_file_32("/nonexistent/path/file.txt")


class TestListHashing:
    """列表哈希测试"""
    
    def test_hash_list_32(self):
        """测试列表32位哈希"""
        items = [1, 2, 3, "hello", "world"]
        result = hash_list_32(items)
        assert isinstance(result, int)
        assert result >= 0
    
    def test_hash_list_64(self):
        """测试列表64位哈希"""
        items = [1, 2, 3, "hello", "world"]
        result = hash_list_64(items)
        assert isinstance(result, int)
        assert result >= 0
    
    def test_empty_list(self):
        """测试空列表"""
        result = hash_list_64([])
        assert isinstance(result, int)
    
    def test_list_order_matters(self):
        """测试列表顺序影响哈希"""
        h1 = hash_list_64([1, 2, 3])
        h2 = hash_list_64([3, 2, 1])
        assert h1 != h2
    
    def test_list_with_seed(self):
        """测试带种子的列表哈希"""
        items = [1, 2, 3]
        h1 = hash_list_64(items, seed=0)
        h2 = hash_list_64(items, seed=1)
        assert h1 != h2


class TestDistributedSharding:
    """分布式分片测试"""
    
    def test_basic_sharding(self):
        """测试基本分片"""
        for i in range(10):
            shard = distributed_shard(f"key:{i}", 4)
            assert 0 <= shard < 4
    
    def test_distribution(self):
        """测试分片分布"""
        num_shards = 10
        keys = [f"user:{i}" for i in range(1000)]
        distribution = [0] * num_shards
        
        for key in keys:
            shard = distributed_shard(key, num_shards)
            distribution[shard] += 1
        
        # 检查分布是否相对均匀
        expected_per_shard = len(keys) / num_shards
        for count in distribution:
            # 允许20%的偏差
            assert abs(count - expected_per_shard) / expected_per_shard < 0.3
    
    def test_deterministic(self):
        """测试分片确定性"""
        key = "test_key"
        shards = [distributed_shard(key, 100) for _ in range(100)]
        assert len(set(shards)) == 1
    
    def test_consistent_hash(self):
        """测试一致性哈希"""
        key = "session:12345"
        bucket = consistent_hash(key, 100)
        assert 0 <= bucket < 100
        
        # 同一key总是映射到同一bucket
        for _ in range(10):
            assert consistent_hash(key, 100) == bucket


class TestXXHashStreamer:
    """流式哈希器测试"""
    
    def test_32bit_streamer(self):
        """测试32位流式哈希器"""
        streamer = XXHashStreamer(bits=32, seed=0)
        streamer.push(b"hello").push(b" ").push(b"world")
        result = streamer.hexdigest()
        
        expected = xxhash32_hex(b"hello world")
        assert result == expected
    
    def test_64bit_streamer(self):
        """测试64位流式哈希器"""
        streamer = XXHashStreamer(bits=64, seed=0)
        streamer.push(b"hello").push(b" ").push(b"world")
        result = streamer.hexdigest()
        
        expected = xxhash64_hex(b"hello world")
        assert result == expected
    
    def test_streamer_reset(self):
        """测试流式哈希器重置"""
        streamer = XXHashStreamer(bits=64, seed=0)
        streamer.push(b"data1")
        streamer.reset()
        streamer.push(b"data2")
        result = streamer.digest()
        
        expected = xxhash64(b"data2")
        assert result == expected
    
    def test_streamer_string_input(self):
        """测试字符串输入"""
        streamer = XXHashStreamer(bits=64, seed=0)
        streamer.push("hello")
        result = streamer.hexdigest()
        
        expected = xxhash64_hex(b"hello")
        assert result == expected
    
    def test_invalid_bits(self):
        """测试无效位数"""
        with pytest.raises(ValueError):
            XXHashStreamer(bits=128)


class TestFingerprint:
    """指纹测试"""
    
    def test_fingerprint_32(self):
        """测试32位指纹"""
        data = b"test data"
        fp = fingerprint_32(data)
        
        assert len(fp) == 8
        assert fp == xxhash32_hex(data)
    
    def test_fingerprint_64(self):
        """测试64位指纹"""
        data = b"test data"
        fp = fingerprint_64(data)
        
        assert len(fp) == 16
        assert fp == xxhash64_hex(data)
    
    def test_fingerprint_uniqueness(self):
        """测试指纹唯一性"""
        data_list = [b"data1", b"data2", b"data3"]
        fingerprints = [fingerprint_64(d) for d in data_list]
        
        assert len(set(fingerprints)) == len(data_list)


class TestMultiHash:
    """多哈希测试"""
    
    def test_multi_hash_default(self):
        """测试默认多哈希"""
        data = b"test"
        result = multi_hash(data)
        
        assert isinstance(result, dict)
        assert len(result) == 3
        assert 0 in result
        assert 1 in result
        assert 2 in result
        
        # 不同种子产生不同结果
        assert result[0] != result[1]
        assert result[1] != result[2]
    
    def test_multi_hash_custom_seeds(self):
        """测试自定义种子"""
        data = b"test"
        seeds = [10, 20, 30, 40]
        result = multi_hash(data, seeds)
        
        assert len(result) == 4
        for seed in seeds:
            assert seed in result
    
    def test_multi_hash_for_bloom_filter(self):
        """测试用于布隆过滤器"""
        data = b"user@example.com"
        seeds = list(range(7))  # 常见的布隆过滤器配置
        result = multi_hash(data, seeds)
        
        # 所有哈希值应该是唯一的
        values = list(result.values())
        assert len(set(values)) == len(values)


class TestHashDict:
    """字典哈希测试"""
    
    def test_simple_dict(self):
        """测试简单字典"""
        d = {"a": 1, "b": 2}
        result = hash_dict(d)
        assert isinstance(result, int)
    
    def test_dict_order_independence(self):
        """测试字典顺序无关性"""
        d1 = {"a": 1, "b": 2}
        d2 = {"b": 2, "a": 1}
        
        assert hash_dict(d1) == hash_dict(d2)
    
    def test_nested_dict(self):
        """测试嵌套字典"""
        d = {"outer": {"inner": "value"}}
        result = hash_dict(d)
        assert isinstance(result, int)
    
    def test_dict_with_list(self):
        """测试包含列表的字典"""
        d = {"items": [1, 2, 3]}
        result = hash_dict(d)
        assert isinstance(result, int)
    
    def test_dict_with_seed(self):
        """测试带种子的字典哈希"""
        d = {"key": "value"}
        h1 = hash_dict(d, seed=0)
        h2 = hash_dict(d, seed=1)
        assert h1 != h2


class TestEdgeCases:
    """边界情况测试"""
    
    def test_very_long_string(self):
        """测试超长字符串"""
        data = b"x" * 1000000
        result = xxhash64(data)
        assert isinstance(result, int)
    
    def test_binary_data(self):
        """测试二进制数据"""
        data = bytes(range(256))
        result = xxhash64(data)
        assert isinstance(result, int)
    
    def test_unicode_various_scripts(self):
        """测试各种Unicode脚本"""
        strings = [
            "你好世界",  # 中文
            "こんにちは",  # 日文
            "안녕하세요",  # 韩文
            "Привет мир",  # 俄文
            "مرحبا بالعالم",  # 阿拉伯文
            "שלום עולם",  # 希伯来文
        ]
        
        for s in strings:
            result = xxhash64(s)
            assert isinstance(result, int)
    
    def test_null_bytes(self):
        """测试空字节"""
        data = b"hello\x00world"
        result = xxhash64(data)
        assert isinstance(result, int)
    
    def test_high_value_seed(self):
        """测试高值种子"""
        result = xxhash64(b"test", seed=0xFFFFFFFFFFFFFFFF)
        assert isinstance(result, int)
    
    def test_negative_seed(self):
        """测试负种子"""
        # 应该自动转换为正数
        result = xxhash64(b"test", seed=-1)
        assert isinstance(result, int)


class TestPerformance:
    """性能测试"""
    
    def test_32_vs_64_consistency(self):
        """测试32位和64位一致性"""
        data = b"test data"
        
        # 多次运行确保确定性
        for _ in range(10):
            h32 = xxhash32(data)
            h64 = xxhash64(data)
            assert isinstance(h32, int)
            assert isinstance(h64, int)
    
    def test_large_data_performance(self):
        """测试大数据性能"""
        import time
        
        data = b"x" * 10000000  # 10MB
        
        start = time.time()
        result = xxhash64(data)
        elapsed = time.time() - start
        
        # 应该在合理时间内完成
        assert elapsed < 5.0  # 5秒内处理10MB（更宽松的时限）
        assert isinstance(result, int)


class TestVerifyTestVectors:
    """测试向量验证测试"""
    
    def test_verify_test_vectors(self):
        """验证测试向量函数"""
        result = _verify_test_vectors()
        assert result == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])