"""
Base62 Utilities 测试

测试 Base62 编解码的各项功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base62_utils.mod import (
    Base62Encoder,
    DEFAULT_CHARSET,
    URL_FRIENDLY_CHARSET,
    REVERSED_CHARSET,
    encode,
    decode,
    encode_bytes,
    decode_bytes,
    encode_uuid,
    decode_uuid,
    encode_snowflake,
    decode_snowflake,
    generate_short_id,
    generate_time_based_id,
    is_valid,
    encode_url_friendly,
    decode_url_friendly,
)


class TestBase62Encoder:
    """Base62Encoder 测试"""
    
    def test_encode_int_zero(self):
        """测试编码零"""
        encoder = Base62Encoder()
        assert encoder.encode_int(0) == '0'
        print("✓ encode_int(0) = '0'")
    
    def test_encode_int_positive(self):
        """测试编码正整数"""
        encoder = Base62Encoder()
        
        # 单字符
        assert encoder.encode_int(10) == 'A'
        assert encoder.encode_int(35) == 'Z'
        assert encoder.encode_int(36) == 'a'
        assert encoder.encode_int(61) == 'z'
        
        # 多字符
        assert encoder.encode_int(62) == '10'
        assert encoder.encode_int(123) == '1z'
        
        print("✓ encode_int 正整数编码正确")
    
    def test_encode_int_negative(self):
        """测试编码负数应抛出异常"""
        encoder = Base62Encoder()
        try:
            encoder.encode_int(-1)
            assert False, "应抛出 ValueError"
        except ValueError:
            print("✓ encode_int(-1) 抛出 ValueError")
    
    def test_decode_int(self):
        """测试解码整数"""
        encoder = Base62Encoder()
        
        assert encoder.decode_int('0') == 0
        assert encoder.decode_int('A') == 10
        assert encoder.decode_int('Z') == 35
        assert encoder.decode_int('a') == 36
        assert encoder.decode_int('z') == 61
        assert encoder.decode_int('10') == 62
        assert encoder.decode_int('1z') == 123
        
        print("✓ decode_int 解码正确")
    
    def test_encode_decode_roundtrip(self):
        """测试编解码往返"""
        encoder = Base62Encoder()
        
        test_numbers = [
            0, 1, 10, 61, 62, 100, 1000, 10000,
            12345678, 987654321, 
            12345678901234567890,
        ]
        
        for num in test_numbers:
            encoded = encoder.encode_int(num)
            decoded = encoder.decode_int(encoded)
            assert decoded == num, f"往返失败: {num} -> {encoded} -> {decoded}"
        
        print(f"✓ 编解码往返测试通过 ({len(test_numbers)} 个数字)")
    
    def test_encode_bytes(self):
        """测试字节流编码"""
        encoder = Base62Encoder()
        
        test_data = [
            b'\x00',
            b'hello',
            b'Hello, World!',
            bytes(range(256)),  # 所有可能的字节值
        ]
        
        for data in test_data:
            encoded = encoder.encode_bytes(data)
            decoded = encoder.decode_bytes(encoded, len(data))
            assert decoded == data, f"字节流编解码失败: {data} -> {encoded} -> {decoded}"
        
        # 空字节流特殊处理
        encoded_empty = encoder.encode_bytes(b'')
        assert encoded_empty == '0'
        
        print("✓ 字节流编解码测试通过")
    
    def test_encode_uuid(self):
        """测试 UUID 编码"""
        encoder = Base62Encoder()
        
        test_uuids = [
            "550e8400-e29b-41d4-a716-446655440000",
            "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            "00000000-0000-0000-0000-000000000000",
            "ffffffff-ffff-ffff-ffff-ffffffffffff",
        ]
        
        for uuid in test_uuids:
            encoded = encoder.encode_uuid(uuid)
            decoded = encoder.decode_uuid(encoded)
            # 移除连字符后比较
            assert decoded.replace('-', '') == uuid.replace('-', '')
            # UUID 编码长度取决于值，最大22字符
            assert len(encoded) <= 22
        
        print(f"✓ UUID 编码测试通过 ({len(test_uuids)} 个 UUID)")
    
    def test_encode_snowflake(self):
        """测试雪花 ID 编码"""
        encoder = Base62Encoder()
        
        test_ids = [
            0,
            1,
            123456789,
            1234567890123456789,
            9223372036854775807,  # max int64
        ]
        
        for snowflake in test_ids:
            encoded = encoder.encode_snowflake(snowflake)
            decoded = encoder.decode_snowflake(encoded)
            assert decoded == snowflake
        
        print(f"✓ 雪花 ID 编码测试通过 ({len(test_ids)} 个 ID)")
    
    def test_generate_short_id(self):
        """测试短 ID 生成"""
        encoder = Base62Encoder()
        
        # 测试长度
        for length in [1, 4, 8, 16, 32]:
            id1 = encoder.generate_short_id(length)
            assert len(id1) == length
        
        # 测试唯一性
        ids = set(encoder.generate_short_id(8) for _ in range(1000))
        assert len(ids) == 1000, "生成的 ID 存在重复"
        
        print("✓ 短 ID 生成测试通过")
    
    def test_generate_time_based_id(self):
        """测试基于时间的 ID 生成"""
        encoder = Base62Encoder()
        
        # 测试长度
        for length in [6, 8, 12, 16]:
            id1 = encoder.generate_time_based_id(length)
            assert len(id1) == length
        
        # 测试唯一性
        ids = set(encoder.generate_time_based_id(12) for _ in range(100))
        assert len(ids) == 100, "生成的 ID 存在重复"
        
        print("✓ 基于时间的 ID 生成测试通过")
    
    def test_encode_with_prefix(self):
        """测试带前缀编码"""
        encoder = Base62Encoder()
        
        prefixed = encoder.encode_with_prefix(12345, "user_")
        # 验证格式正确 (user_ + base62编码)
        assert prefixed.startswith("user_")
        
        # 解码时指定前缀
        prefix, num = encoder.decode_with_prefix(prefixed, "user_")
        assert prefix == "user_"
        assert num == 12345
        
        # 自动提取前缀
        prefix2, num2 = encoder.decode_with_prefix(prefixed)
        assert prefix2 == "user_"
        assert num2 == 12345
        
        # 测试无前缀
        prefixed = encoder.encode_with_prefix(12345, "")
        assert prefixed == encode(12345)
        
        print("✓ 带前缀编码测试通过")
    
    def test_is_valid(self):
        """测试有效性检查"""
        encoder = Base62Encoder()
        
        assert encoder.is_valid("abc123XYZ") == True
        assert encoder.is_valid("0AZaz") == True
        assert encoder.is_valid("") == True  # 空字符串有效 (解码为0)
        assert encoder.is_valid("hello!") == False  # 包含非法字符
        assert encoder.is_valid("test-string") == False  # 包含非法字符
        assert encoder.is_valid("test_string") == False  # 包含非法字符
        
        print("✓ 有效性检查测试通过")
    
    def test_custom_charset(self):
        """测试自定义字符集"""
        # URL 友好字符集
        encoder = Base62Encoder(URL_FRIENDLY_CHARSET)
        
        # 编码结果应该不同
        num = 123456789
        encoded_default = Base62Encoder().encode_int(num)
        encoded_url = encoder.encode_int(num)
        
        # 位置应该不同（字符集顺序不同）
        # 但解码结果相同
        assert encoder.decode_int(encoded_url) == num
        
        print("✓ 自定义字符集测试通过")
    
    def test_invalid_charset(self):
        """测试无效字符集"""
        # 长度不对
        try:
            Base62Encoder("abc")
            assert False, "应抛出 ValueError"
        except ValueError:
            pass
        
        # 包含重复字符
        try:
            Base62Encoder("a" * 62)
            assert False, "应抛出 ValueError"
        except ValueError:
            pass
        
        print("✓ 无效字符集测试通过")
    
    def test_invalid_decode(self):
        """测试无效解码"""
        encoder = Base62Encoder()
        
        try:
            encoder.decode_int("hello!")  # 包含非法字符
            assert False, "应抛出 ValueError"
        except ValueError:
            pass
        
        print("✓ 无效解码测试通过")


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_encode_decode(self):
        """测试便捷编解码函数"""
        num = 123456789
        encoded = encode(num)
        decoded = decode(encoded)
        assert decoded == num
        print("✓ encode/decode 便捷函数测试通过")
    
    def test_encode_decode_bytes(self):
        """测试字节流便捷函数"""
        data = b"Hello, World!"
        encoded = encode_bytes(data)
        decoded = decode_bytes(encoded)
        assert decoded == data
        print("✓ encode_bytes/decode_bytes 便捷函数测试通过")
    
    def test_encode_decode_uuid(self):
        """测试 UUID 便捷函数"""
        uuid = "550e8400-e29b-41d4-a716-446655440000"
        encoded = encode_uuid(uuid)
        decoded = decode_uuid(encoded)
        assert decoded.replace('-', '') == uuid.replace('-', '')
        print("✓ encode_uuid/decode_uuid 便捷函数测试通过")
    
    def test_encode_decode_snowflake(self):
        """测试雪花 ID 便捷函数"""
        snowflake = 1234567890123456789
        encoded = encode_snowflake(snowflake)
        decoded = decode_snowflake(encoded)
        assert decoded == snowflake
        print("✓ encode_snowflake/decode_snowflake 便捷函数测试通过")
    
    def test_generate_functions(self):
        """测试生成函数"""
        id1 = generate_short_id(8)
        assert len(id1) == 8
        
        id2 = generate_time_based_id(12)
        assert len(id2) == 12
        
        assert is_valid(id1)
        assert is_valid(id2)
        
        print("✓ generate_short_id/generate_time_based_id 便捷函数测试通过")
    
    def test_url_friendly_functions(self):
        """测试 URL 友好函数"""
        num = 123456789
        encoded = encode_url_friendly(num)
        decoded = decode_url_friendly(encoded)
        assert decoded == num
        print("✓ encode_url_friendly/decode_url_friendly 便捷函数测试通过")


class TestPerformance:
    """性能测试"""
    
    def test_large_numbers(self):
        """测试大数编解码"""
        encoder = Base62Encoder()
        
        large_num = 10 ** 100  # googol
        encoded = encoder.encode_int(large_num)
        decoded = encoder.decode_int(encoded)
        assert decoded == large_num
        
        print(f"✓ 大数编解码测试通过 ({len(encoded)} 字符)")
    
    def test_batch_encoding(self):
        """测试批量编码性能"""
        encoder = Base62Encoder()
        
        import time
        start = time.time()
        
        for i in range(10000):
            encoder.encode_int(i)
        
        elapsed = time.time() - start
        print(f"✓ 批量编码测试通过 (10000 次编码耗时 {elapsed:.3f}s)")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Base62 Utilities 测试")
    print("=" * 60)
    
    # 编码器测试
    encoder_tests = TestBase62Encoder()
    print("\n[TestBase62Encoder]")
    encoder_tests.test_encode_int_zero()
    encoder_tests.test_encode_int_positive()
    encoder_tests.test_encode_int_negative()
    encoder_tests.test_decode_int()
    encoder_tests.test_encode_decode_roundtrip()
    encoder_tests.test_encode_bytes()
    encoder_tests.test_encode_uuid()
    encoder_tests.test_encode_snowflake()
    encoder_tests.test_generate_short_id()
    encoder_tests.test_generate_time_based_id()
    encoder_tests.test_encode_with_prefix()
    encoder_tests.test_is_valid()
    encoder_tests.test_custom_charset()
    encoder_tests.test_invalid_charset()
    encoder_tests.test_invalid_decode()
    
    # 便捷函数测试
    convenience_tests = TestConvenienceFunctions()
    print("\n[TestConvenienceFunctions]")
    convenience_tests.test_encode_decode()
    convenience_tests.test_encode_decode_bytes()
    convenience_tests.test_encode_decode_uuid()
    convenience_tests.test_encode_decode_snowflake()
    convenience_tests.test_generate_functions()
    convenience_tests.test_url_friendly_functions()
    
    # 性能测试
    perf_tests = TestPerformance()
    print("\n[TestPerformance]")
    perf_tests.test_large_numbers()
    perf_tests.test_batch_encoding()
    
    print("\n" + "=" * 60)
    print("所有测试通过! ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()