"""
LZW 工具库测试套件

测试覆盖：
- 基本压缩和解压缩
- 字符串压缩
- 十六进制格式
- 流式处理
- GIF 格式兼容
- 边界情况
- 压缩率统计
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lzw_utils.mod import (
    compress, decompress,
    compress_string, decompress_string,
    compress_to_hex, decompress_from_hex,
    get_compression_ratio, get_compression_stats,
    compress_stream,
    compress_gif, decompress_gif,
    LZWEncoder, LZWDecoder
)


def test_basic_compress_decompress():
    """测试基本压缩和解压缩"""
    print("测试基本压缩和解压缩...")
    
    test_cases = [
        b"TOBEORNOTTOBEORTOBEORNOT",
        b"ABABABABABABABAB",
        b"AAAAAAAAAA",
        b"Hello, World!",
        b"The quick brown fox jumps over the lazy dog",
        b"",  # 空数据
        b"A",  # 单字节
    ]
    
    for data in test_cases:
        compressed = compress(data)
        decompressed = decompress(compressed)
        assert decompressed == data, f"解压缩失败: {data}"
        
        if data:
            print(f"  ✓ '{data[:20]}...' ({len(data)} -> {len(compressed)} 字节)")
        else:
            print(f"  ✓ 空数据处理正确")
    
    print("基本压缩测试通过！\n")


def test_string_compress():
    """测试字符串压缩"""
    print("测试字符串压缩...")
    
    test_strings = [
        "Hello, World!",
        "你好，世界！🌍",
        "日本語テスト",
        "A" * 1000,
        "重复的文本重复的文本重复的文本" * 50,
    ]
    
    for text in test_strings:
        compressed = compress_string(text)
        decompressed = decompress_string(compressed)
        assert decompressed == text, f"字符串解压缩失败: {text[:20]}"
        
        ratio = get_compression_ratio(text.encode('utf-8'), compressed)
        print(f"  ✓ '{text[:20]}...' 压缩率: {ratio:.2%}")
    
    print("字符串压缩测试通过！\n")


def test_hex_format():
    """测试十六进制格式"""
    print("测试十六进制格式...")
    
    test_data = b"TOBEORNOTTOBEORTOBEORNOT"
    
    hex_str = compress_to_hex(test_data)
    assert isinstance(hex_str, str), "十六进制输出应为字符串"
    assert all(c in '0123456789abcdef' for c in hex_str), "应只包含十六进制字符"
    
    decompressed = decompress_from_hex(hex_str)
    assert decompressed == test_data, "十六进制解压缩失败"
    
    print(f"  ✓ 原始数据: {test_data}")
    print(f"  ✓ 十六进制: {hex_str}")
    print(f"  ✓ 解压后: {decompressed}")
    print("十六进制格式测试通过！\n")


def test_compression_ratio():
    """测试压缩率计算"""
    print("测试压缩率计算...")
    
    # 重复数据应该压缩效果好
    repetitive = b"ABABABABAB" * 100
    compressed_rep = compress(repetitive)
    ratio_rep = get_compression_ratio(repetitive, compressed_rep)
    
    # 随机数据压缩效果应该较差
    random_like = bytes(range(256)) * 4
    compressed_rand = compress(random_like)
    ratio_rand = get_compression_ratio(random_like, compressed_rand)
    
    print(f"  重复数据压缩率: {ratio_rep:.2%} (越好)")
    print(f"  随机数据压缩率: {ratio_rand:.2%} (较差)")
    
    assert ratio_rep < ratio_rand, "重复数据应该压缩得更好"
    
    # 测试统计信息
    stats = get_compression_stats(repetitive, compressed_rep)
    print(f"  统计信息: {stats}")
    
    assert stats['original_size'] == len(repetitive)
    assert stats['compressed_size'] == len(compressed_rep)
    assert stats['is_efficient'] == (stats['ratio'] < 1)
    
    print("压缩率测试通过！\n")


def test_streaming():
    """测试流式压缩"""
    print("测试流式压缩...")
    
    # 大数据测试
    large_data = b"Hello, World! This is a test of streaming compression. " * 1000
    
    # 流式压缩
    chunks = list(compress_stream(large_data, chunk_size=1024))
    compressed = b''.join(chunks)
    
    # 解压验证
    decompressed = decompress(compressed)
    assert decompressed == large_data, "流式压缩数据不匹配"
    
    print(f"  ✓ 流式压缩: {len(large_data)} -> {len(compressed)} 字节")
    print("流式压缩测试通过！\n")


def test_encoder_decoder_classes():
    """测试编码器和解码器类"""
    print("测试编码器和解码器类...")
    
    # 测试编码器
    encoder = LZWEncoder()
    encoder.update(b"Hello, ")
    encoder.update(b"World!")
    compressed = encoder.finish()
    
    # 测试解码器
    decoder = LZWDecoder()
    decompressed = decoder.update(compressed)
    
    assert decompressed == b"Hello, World!", "编码器/解码器类测试失败"
    print(f"  ✓ 编码器和解码器工作正常")
    
    # 测试自定义参数
    encoder2 = LZWEncoder(min_code_size=10, max_code_size=14)
    test_data = b"Custom parameters test"
    encoder2.update(test_data)
    compressed2 = encoder2.finish()
    
    decoder2 = LZWDecoder(min_code_size=10, max_code_size=14)
    decompressed2 = decoder2.update(compressed2)
    
    assert decompressed2 == test_data, "自定义参数测试失败"
    print(f"  ✓ 自定义参数工作正常")
    
    print("编码器/解码器类测试通过！\n")


def test_gif_format():
    """测试 GIF 格式兼容"""
    print("测试 GIF 格式兼容...")
    
    # GIF 格式是特殊的 LZW 变体，主要用于图像压缩
    # 使用较小范围的像素值进行测试
    test_cases = [
        b"\x00\x01\x00\x01\x00\x01",  # 简单像素数据
        b"\x00\x01\x02" * 50,  # 小范围重复
        b"\xFF" * 100,  # 单一像素
        b"\x00\x01\x02\x03\x04\x05\x06\x07" * 10,  # 8色图像
    ]
    
    for data in test_cases:
        compressed = compress_gif(data)
        decompressed = decompress_gif(compressed)
        assert decompressed == data, f"GIF 解压缩失败: {data[:20]}"
        print(f"  ✓ GIF 格式: {len(data)} -> {len(compressed)} 字节")
    
    print("GIF 格式测试通过！\n")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 空数据
    assert compress(b"") == b"", "空数据应该返回空"
    assert decompress(b"") == b"", "空解压应该返回空"
    
    # 单字节
    single = b"A"
    assert decompress(compress(single)) == single
    
    # 最大字典压力（大量不同序列）
    unique = bytes(range(256)) * 10
    compressed_unique = compress(unique)
    assert decompress(compressed_unique) == unique
    print(f"  ✓ 高熵数据: {len(unique)} -> {len(compressed_unique)} 字节")
    
    # 二进制数据
    binary = bytes([0, 1, 2, 255, 254, 253] * 100)
    assert decompress(compress(binary)) == binary
    print(f"  ✓ 二进制数据处理正确")
    
    # Unicode
    unicode_data = "🎉🎊🎁🎂🎈🎪🎨🎭🎵🎶".encode('utf-8')
    assert decompress(compress(unicode_data)) == unicode_data
    print(f"  ✓ Unicode 数据处理正确")
    
    print("边界情况测试通过！\n")


def test_large_data():
    """测试大数据"""
    print("测试大数据处理...")
    
    # 1MB 数据
    large = (b"This is a test sentence for LZW compression. " * 20000)[:1024 * 1024]
    compressed = compress(large)
    decompressed = decompress(compressed)
    
    assert decompressed == large, "大数据解压缩失败"
    
    stats = get_compression_stats(large, compressed)
    print(f"  原始大小: {stats['original_size'] / 1024:.2f} KB")
    print(f"  压缩后: {stats['compressed_size'] / 1024:.2f} KB")
    print(f"  压缩率: {stats['ratio']:.2%}")
    print(f"  节省: {stats['saved_percent']:.1f}%")
    
    assert decompressed == large
    print("大数据测试通过！\n")


def test_repetitive_patterns():
    """测试重复模式"""
    print("测试重复模式压缩效果...")
    
    patterns = [
        (b"A" * 1000, "全相同"),
        (b"AB" * 500, "AB 交替"),
        (b"ABC" * 333, "ABC 循环"),
        (b"ABCD" * 250, "ABCD 循环"),
        (b"ABCDEFGH" * 125, "8字节循环"),
    ]
    
    best_ratio = 1.0
    best_pattern = ""
    
    for data, name in patterns:
        compressed = compress(data)
        ratio = get_compression_ratio(data, compressed)
        
        if ratio < best_ratio:
            best_ratio = ratio
            best_pattern = name
        
        print(f"  {name}: {ratio:.2%} ({len(data)} -> {len(compressed)} 字节)")
    
    print(f"  最佳: {best_pattern} ({best_ratio:.2%})")
    print("重复模式测试通过！\n")


def test_compression_quality():
    """测试压缩质量"""
    print("测试压缩质量...")
    
    # 各种类型的数据
    test_cases = {
        "英文文本": b"The quick brown fox jumps over the lazy dog. " * 100,
        "重复模式": b"ABCABCABCABCABCABCABCABCABCABCABC" * 50,
        "高度压缩": b"X" * 10000,
        "低压缩": bytes(range(256)) * 40,
    }
    
    total_original = 0
    total_compressed = 0
    
    for name, data in test_cases.items():
        compressed = compress(data)
        ratio = get_compression_ratio(data, compressed)
        
        total_original += len(data)
        total_compressed += len(compressed)
        
        status = "✓ 高效" if ratio < 1 else "✗ 膨胀"
        print(f"  {name}: {ratio:.2%} {status}")
    
    overall = total_compressed / total_original if total_original > 0 else 0
    print(f"  总体压缩率: {overall:.2%}")
    print("压缩质量测试完成！\n")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("LZW 工具库测试套件")
    print("=" * 60 + "\n")
    
    tests = [
        test_basic_compress_decompress,
        test_string_compress,
        test_hex_format,
        test_compression_ratio,
        test_streaming,
        test_encoder_decoder_classes,
        test_gif_format,
        test_edge_cases,
        test_large_data,
        test_repetitive_patterns,
        test_compression_quality,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ 测试失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ 测试错误: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)