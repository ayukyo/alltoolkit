"""
LZ77 Utils - 使用示例

展示 LZ77 压缩算法的各种使用场景。
"""

import sys
sys.path.insert(0, '..')
from mod import (
    LZ77Token,
    LZ77Encoder,
    LZ77Decoder,
    LZ77Compressor,
    StreamingLZ77Encoder,
    lz77_encode,
    lz77_decode,
    lz77_decode_to_string,
    lz77_compress,
    analyze_lz77,
    compare_presets,
)


def example_basic_compression():
    """基础压缩示例"""
    print("=" * 50)
    print("示例 1: 基础压缩")
    print("=" * 50)
    
    compressor = LZ77Compressor()
    
    # 压缩重复数据
    data = "hellohellohellohellohello"
    result = compressor.compress(data)
    
    print(f"\n原始数据: {data}")
    print(f"原始大小: {result.original_size} 字节")
    print(f"压缩后大小: {result.compressed_size} 字节")
    print(f"压缩率: {result.compression_ratio:.2f}x")
    print(f"空间节省: {result.space_saving:.1f}%")
    print(f"\n令牌详情:")
    print(f"  总令牌数: {result.total_tokens}")
    print(f"  字面量数: {result.literal_count}")
    print(f"  匹配数: {result.match_count}")
    
    # 显示部分令牌
    print(f"\n前 10 个令牌:")
    for i, token in enumerate(result.tokens[:10]):
        if token.is_literal:
            print(f"  [{i}] 字面量: {repr(chr(token.value) if isinstance(token.value, int) else token.value)}")
        else:
            print(f"  [{i}] 匹配: offset={token.offset}, length={token.length}")
    
    # 解压验证
    decoded = compressor.decompress_to_string(result.tokens)
    print(f"\n解压结果: {decoded}")
    print(f"数据完整性: {decoded == data}")


def example_presets():
    """预设配置示例"""
    print("\n" + "=" * 50)
    print("示例 2: 预设配置对比")
    print("=" * 50)
    
    # 测试数据 - 较长的重复文本
    data = "The quick brown fox jumps over the lazy dog. " * 20
    
    print(f"\n原始数据: {len(data)} 字节")
    print(f"数据片段: {data[:50]}...")
    
    # 使用不同预设
    presets = {
        'fast': LZ77Compressor.fast(),
        'balanced': LZ77Compressor.balanced(),
        'maximum': LZ77Compressor.maximum(),
    }
    
    print(f"\n各预设压缩效果:")
    print("-" * 40)
    
    for name, compressor in presets.items():
        result = compressor.compress(data)
        print(f"{name:10s}: 压缩率={result.compression_ratio:.2f}x, "
              f"节省={result.space_saving:.1f}%, "
              f"匹配={result.match_count}")


def example_analysis():
    """压缩分析示例"""
    print("\n" + "=" * 50)
    print("示例 3: 压缩特性分析")
    print("=" * 50)
    
    # 不同类型的数据
    datasets = {
        '重复数据': "aaaa" * 50,
        '周期数据': "abcdabcdabcd" * 20,
        '文本数据': "Python is a great programming language. Python is great! " * 10,
        '混合数据': "abc123abc123xyz789xyz789" * 15,
    }
    
    for name, data in datasets.items():
        print(f"\n{name} ({len(data)} 字节):")
        print("-" * 30)
        
        analysis = analyze_lz77(data)
        
        print(f"  压缩率: {analysis['compression_ratio']:.2f}x")
        print(f"  空间节省: {analysis['space_saving']:.1f}%")
        print(f"  最大匹配长度: {analysis['max_match_length']}")
        print(f"  平均匹配长度: {analysis['avg_match_length']:.2f}")
        
        # 匹配长度分布
        dist = analysis['match_lengths_distribution']
        if dist:
            top_lengths = sorted(dist.items(), key=lambda x: x[1], reverse=True)[:5]
            print(f"  匹配长度分布 (top 5): {dict(top_lengths)}")


def example_streaming():
    """流式处理示例"""
    print("\n" + "=" * 50)
    print("示例 4: 流式处理")
    print("=" * 50)
    
    encoder = StreamingLZ77Encoder(window_size=100, min_match_length=3)
    decoder = LZ77Decoder()
    
    # 模拟分块输入
    chunks = [
        "abcdefgh",
        "abcdefgh",  # 重复，应产生匹配
        "12345678",
        "abcdefgh",  # 再次重复
    ]
    
    all_tokens = []
    
    print(f"\n流式输入:")
    for i, chunk in enumerate(chunks):
        tokens = encoder.feed(chunk)
        all_tokens.extend(tokens)
        print(f"  块 {i+1}: '{chunk}' -> {len(tokens)} 个令牌")
    
    # 刷新剩余
    remaining = encoder.flush()
    all_tokens.extend(remaining)
    print(f"  刷新剩余: {len(remaining)} 个令牌")
    
    # 解码验证
    decoded = decoder.decode(all_tokens)
    full_data = "".join(chunks)
    
    print(f"\n总令牌数: {len(all_tokens)}")
    print(f"解码结果: {decoded.decode('utf-8')[:50]}...")
    print(f"数据完整性: {decoded.decode('utf-8') == full_data}")


def example_tokens():
    """令牌操作示例"""
    print("\n" + "=" * 50)
    print("示例 5: 令牌操作")
    print("=" * 50)
    
    # 手动创建令牌序列
    print("\n手动构建令牌:")
    
    # 构建编码 "abcab"
    tokens = [
        LZ77Token.literal(ord('a')),  # 'a'
        LZ77Token.literal(ord('b')),  # 'b'
        LZ77Token.literal(ord('c')),  # 'c'
        LZ77Token.match(offset=3, length=2),  # 匹配 'ab' (回溯3，长度2)
    ]
    
    print("令牌序列:")
    for token in tokens:
        print(f"  {token}")
    
    # 解码
    decoder = LZ77Decoder()
    decoded = decoder.decode(tokens)
    print(f"\n解码结果: {decoded.decode('utf-8')}")
    
    # 令牌属性测试
    print("\n令牌属性测试:")
    literal = LZ77Token.literal(65)
    match = LZ77Token.match(10, 5)
    
    print(f"  字面量: is_literal={literal.is_literal}, is_match={literal.is_match}")
    print(f"  匹配: is_literal={match.is_literal}, is_match={match.is_match}")


def example_bytes_data():
    """字节数据处理示例"""
    print("\n" + "=" * 50)
    print("示例 6: 字节数据处理")
    print("=" * 50)
    
    compressor = LZ77Compressor()
    
    # 二进制数据
    binary_data = bytes([0, 1, 2, 3, 0, 1, 2, 3, 255, 254, 255, 254])
    
    print(f"\n原始字节: {binary_data.hex()}")
    print(f"长度: {len(binary_data)} 字节")
    
    result = compressor.compress(binary_data)
    
    print(f"压缩率: {result.compression_ratio:.2f}x")
    print(f"匹配数: {result.match_count}")
    
    # 解压
    decoded = compressor.decompress(result.tokens)
    print(f"\n解压字节: {decoded.hex()}")
    print(f"数据完整性: {decoded == binary_data}")


def example_roundtrip():
    """往返验证示例"""
    print("\n" + "=" * 50)
    print("示例 7: 往返验证")
    print("=" * 50)
    
    compressor = LZ77Compressor.balanced()
    
    # 各种测试数据
    test_cases = [
        "简单字符串",
        "aaaa" * 25,
        "abcdabcdabcd" * 10,
        "你好世界你好世界你好世界",
        "Mixed 内容 mixed 内容 Mixed!",
    ]
    
    print("\n验证结果:")
    print("-" * 40)
    
    for data in test_cases:
        result, success = compressor.roundtrip(data)
        status = "✓ 成功" if success else "✗ 失败"
        print(f"  {data[:30]:30s} -> {status}, 压缩率={result.compression_ratio:.2f}x")


def example_compare_all_presets():
    """全面预设对比示例"""
    print("\n" + "=" * 50)
    print("示例 8: 预设全面对比")
    print("=" * 50)
    
    # 较大数据集
    data = "This is a sample text that will be compressed. " * 50
    
    comparison = compare_presets(data)
    
    print(f"\n数据: {len(data)} 字节")
    print(f"片段: {data[:60]}...")
    
    print("\n预设对比结果:")
    print("-" * 60)
    
    # 按压缩率排序
    sorted_presets = sorted(
        comparison.items(),
        key=lambda x: x[1]['compression_ratio'],
        reverse=True
    )
    
    for preset, stats in sorted_presets:
        print(f"{preset:10s}: "
              f"压缩率={stats['compression_ratio']:6.2f}x, "
              f"节省={stats['space_saving']:5.1f}%, "
              f"令牌={stats['total_tokens']:4d}, "
              f"匹配={stats['match_count']:4d}")


def main():
    """运行所有示例"""
    example_basic_compression()
    example_presets()
    example_analysis()
    example_streaming()
    example_tokens()
    example_bytes_data()
    example_roundtrip()
    example_compare_all_presets()
    
    print("\n" + "=" * 50)
    print("所有示例完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()