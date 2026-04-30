"""
Golomb Coding Utilities - 使用示例

本文件展示 Golomb/Rice 编码工具的多种使用场景。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    BitWriter, BitReader,
    GolombCoding, RiceCoding,
    DeltaGolombCompressor,
    GolombRiceCoder,
    compress_sorted_integers, decompress_sorted_integers,
    optimal_parameter,
)


def example_1_basic_golomb():
    """
    示例 1: 基本 Golomb 编码
    
    Golomb 编码将整数 N 编码为：
    - 商 q = floor(N / M)，使用一元编码
    - 余数 r = N mod M，使用截断二进制编码
    """
    print("=== 示例 1: 基本 Golomb 编码 ===")
    
    m = 10  # 参数 M
    coder = GolombCoding(m)
    
    print(f"\n参数 M = {m}")
    print(f"M 不是 2 的幂，使用截断二进制编码")
    
    values = [0, 7, 10, 23, 100, 500]
    print(f"\n编码值: {values}")
    
    print("\n详细编码:")
    print("-" * 40)
    for value in values:
        q, r = coder.encode(value)
        decoded = coder.decode(q, r)
        print(f"值 {value:4d} -> 商={q}, 余={r} -> 解码={decoded}")
    
    print("\n序列编码测试:")
    encoded = coder.encode_sequence(values)
    decoded = coder.decode_sequence(encoded, len(values))
    print(f"编码后: {len(encoded)} 字节")
    print(f"解码验证: {decoded == values}")


def example_2_rice_coding():
    """
    示例 2: Rice 编码
    
    Rice 编码是 Golomb 编码的特例，当 M 是 2 的幂时。
    余数使用固定长度二进制编码，更高效。
    """
    print("\n=== 示例 2: Rice 编码 ===")
    
    k = 4  # M = 2^k = 16
    rice = RiceCoding(k)
    
    print(f"\n参数 k = {k}, M = {rice.m}")
    print(f"M 是 2 的幂，使用 Rice 编码优化")
    
    values = [0, 15, 16, 31, 32, 100, 200, 500, 1000]
    
    print(f"\n编码值: {values}")
    
    encoded = rice.encode_sequence(values)
    decoded = rice.decode_sequence(encoded, len(values))
    
    print(f"编码后: {len(encoded)} 字节")
    print(f"解码验证: {decoded == values}")
    
    # 计算 Gamma 编码对比 (Gamma 编码要求值 >= 1)
    print("\n与 Gamma 编码对比:")
    writer = BitWriter()
    for v in values:
        if v >= 1:
            writer.write_gamma(v)
        else:
            writer.write_bits(0, 1)  # 0 用单比特表示
    gamma_encoded = writer.flush()
    print(f"Gamma 编码: {len(gamma_encoded)} 字节")
    print(f"Rice 编码: {len(encoded)} 字节")
    print(f"Rice 节省: {len(gamma_encoded) - len(encoded)} 字节")


def example_3_optimal_parameter():
    """
    示例 3: 自动计算最优参数
    
    对于几何分布数据，可自动计算最优 M 或 k。
    """
    print("\n=== 示例 3: 自动计算最优参数 ===")
    
    # 小值序列
    small_values = list(range(1, 51))
    m_small = GolombCoding.optimal_m(small_values)
    k_small = RiceCoding.optimal_k(small_values)
    
    print(f"\n小值序列 (1-50):")
    print(f"推荐 M = {m_small}")
    print(f"推荐 k = {k_small} (M = {1 << k_small})")
    
    # 中值序列
    medium_values = list(range(50, 200, 10))
    m_medium = GolombCoding.optimal_m(medium_values)
    k_medium = RiceCoding.optimal_k(medium_values)
    
    print(f"\n中值序列 (50-190):")
    print(f"推荐 M = {m_medium}")
    print(f"推荐 k = {k_medium} (M = {1 << k_medium})")
    
    # 大值序列
    large_values = [100, 500, 1000, 5000, 10000]
    m_large = GolombCoding.optimal_m(large_values)
    k_large = RiceCoding.optimal_k(large_values)
    
    print(f"\n大值序列:")
    print(f"推荐 M = {m_large}")
    print(f"推荐 k = {k_large} (M = {1 << k_large})")
    
    # 分析报告
    print("\n=== 分析报告 ===")
    analysis = GolombRiceCoder.analyze(list(range(1, 101)))
    print(f"数据数量: {analysis['count']}")
    print(f"最小值: {analysis['min']}")
    print(f"最大值: {analysis['max']}")
    print(f"平均值: {analysis['mean']:.2f}")
    print(f"推荐类型: {analysis['recommended_type']}")
    print(f"Golomb 大小: {analysis['golomb_size']} 字节")
    print(f"Rice 大小: {analysis['rice_size']} 字节")


def example_4_delta_golomb_compression():
    """
    示例 4: Delta + Golomb 压缩
    
    专门用于有序整数序列的压缩，广泛应用于：
    - 搜索引擎倒排索引
    - 数据库索引
    - 时间戳序列
    """
    print("\n=== 示例 4: Delta + Golomb 压缩 ===")
    
    compressor = DeltaGolombCompressor()
    
    # 场景 1: 密集文档 ID 列表 (倒排索引)
    print("\n场景 1: 倒排索引文档 ID 列表")
    doc_ids = [1, 2, 3, 5, 8, 9, 10, 15, 18, 20, 23, 25, 28, 30, 35, 40]
    
    compressed = compressor.compress(doc_ids)
    decompressed = compressor.decompress(compressed)
    
    print(f"原始 ID: {doc_ids[:10]}...")
    print(f"原始大小: {len(doc_ids) * 4} 字节")
    print(f"压缩后: {len(compressed)} 字节")
    print(f"压缩比: {compressor.get_compression_ratio(doc_ids):.2f}x")
    print(f"解压验证: {decompressed == doc_ids}")
    
    # 场景 2: 时间戳序列
    print("\n场景 2: 时间戳序列 (秒级)")
    timestamps = [
        1704067200,  # 2024-01-01 00:00:00
        1704067260,  # +60 秒
        1704067320,
        1704067380,
        1704067500,
        1704067800,
        1704068100,
    ]
    
    compressed = compressor.compress(timestamps)
    decompressed = compressor.decompress(compressed)
    
    print(f"时间戳数量: {len(timestamps)}")
    print(f"压缩后: {len(compressed)} 字节")
    print(f"压缩比: {compressor.get_compression_ratio(timestamps):.2f}x")
    
    # 场景 3: 长序列压缩
    print("\n场景 3: 10000 个连续整数")
    long_sequence = list(range(1, 10001))
    
    compressed = compressor.compress(long_sequence)
    decompressed = compressor.decompress(compressed)
    
    print(f"原始大小: {len(long_sequence) * 4} 字节 (40 KB)")
    print(f"压缩后: {len(compressed)} 字节 ({len(compressed) / 1024:.1f} KB)")
    print(f"压缩比: {compressor.get_compression_ratio(long_sequence):.2f}x")
    print(f"解压验证: {decompressed == long_sequence}")


def example_5_bitstream_operations():
    """
    示例 5: 比特流操作
    
    直接使用 BitWriter/BitReader 进行底层比特操作。
    """
    print("\n=== 示例 5: 比特流操作 ===")
    
    writer = BitWriter()
    
    print("\n写入各种数据:")
    
    # 单比特
    writer.write_bit(1)
    print("写入比特: 1")
    
    # 多比特整数
    writer.write_bits(42, 6)  # 42 = 101010 (6 位)
    print("写入 6 位: 42 (101010)")
    
    # 一元编码
    writer.write_unary(5)  # 000001
    print("写入一元: 5 (000001)")
    
    # Gamma 编码
    writer.write_gamma(10)  # 10 = 1010
    print("写入 Gamma: 10")
    
    writer.write_gamma(50)
    print("写入 Gamma: 50")
    
    data = writer.flush()
    print(f"\n总字节数: {len(data)}")
    print(f"十六进制: {data.hex()}")
    
    # 读取
    print("\n读取数据:")
    reader = BitReader(data)
    
    bit = reader.read_bit()
    print(f"读取比特: {bit}")
    
    bits_6 = reader.read_bits(6)
    print(f"读取 6 位: {bits_6}")
    
    unary = reader.read_unary()
    print(f"读取一元: {unary}")
    
    gamma1 = reader.read_gamma()
    print(f"读取 Gamma: {gamma1}")
    
    gamma2 = reader.read_gamma()
    print(f"读取 Gamma: {gamma2}")


def example_6_smart_encoding():
    """
    示例 6: 智能编码
    
    自动选择最佳编码方式和参数。
    """
    print("\n=== 示例 6: 智能编码 ===")
    
    # 测试不同类型的数据
    datasets = {
        '密集序列': list(range(1, 101)),
        '稀疏序列': [1, 100, 1000, 5000, 10000],
        '混合序列': [1, 2, 3, 10, 50, 100, 500, 1000],
        '小值序列': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    }
    
    for name, values in datasets.items():
        print(f"\n{name}: {values[:5]}...")
        
        encoded, metadata = GolombRiceCoder.encode_optimal(values)
        decoded = GolombRiceCoder.decode(encoded, metadata)
        
        print(f"编码类型: {metadata['type']}")
        if metadata['type'] == 'rice':
            print(f"参数 k = {metadata['k']}, M = {metadata['m']}")
        else:
            print(f"参数 M = {metadata['m']}")
        print(f"编码后: {len(encoded)} 字节")
        print(f"解码验证: {decoded == values}")


def example_7_inverted_index_simulation():
    """
    示例 7: 搜索引擎倒排索引模拟
    
    模拟搜索引擎中倒排列表的压缩存储。
    """
    print("\n=== 示例 7: 搜索引擎倒排索引模拟 ===")
    
    # 模拟多个词项的倒排列表
    inverted_lists = {
        'python': [1, 2, 5, 10, 15, 20, 23, 25, 28, 30, 35, 40, 45, 50],
        'java': [3, 8, 12, 18, 22, 27, 33, 38, 44, 49, 55, 60],
        'coding': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        'algorithm': [100, 150, 200, 250, 300, 350, 400],
    }
    
    print("\n词项倒排列表压缩:")
    print("-" * 50)
    
    total_original = 0
    total_compressed = 0
    
    for term, doc_ids in inverted_lists.items():
        compressor = DeltaGolombCompressor()
        compressed = compressor.compress(doc_ids)
        
        original_size = len(doc_ids) * 4
        ratio = compressor.get_compression_ratio(doc_ids)
        
        total_original += original_size
        total_compressed += len(compressed)
        
        print(f"{term:12s}: {len(doc_ids):3d} docs, "
              f"{original_size:4d}B -> {len(compressed):3d}B, "
              f"ratio={ratio:.2f}x")
    
    print("-" * 50)
    print(f"总计: {total_original}B -> {total_compressed}B, "
          f"ratio={total_original/total_compressed:.2f}x")


def example_8_custom_m_parameter():
    """
    示例 8: 自定义 M 参数
    
    根据特定需求设置自定义 M 参数。
    """
    print("\n=== 示例 8: 自定义 M 参数 ===")
    
    # 相同数据，不同 M 参数的压缩效果对比
    values = list(range(1, 101))
    
    print(f"\n数据: 1 到 100")
    print("\n不同 M 参数对比:")
    print("-" * 40)
    
    for m in [2, 4, 8, 16, 32, 64]:
        compressor = DeltaGolombCompressor(m=m)
        compressed = compressor.compress(values)
        ratio = compressor.get_compression_ratio(values)
        
        print(f"M = {m:3d}: {len(compressed):3d} 字节, ratio={ratio:.2f}x")
    
    # 自动选择最优
    optimal_m = optimal_parameter(values)
    compressor = DeltaGolombCompressor(m=optimal_m)
    compressed = compressor.compress(values)
    ratio = compressor.get_compression_ratio(values)
    
    print(f"\n最优 M = {optimal_m}: {len(compressed):3d} 字节, ratio={ratio:.2f}x")


def example_9_convenience_functions():
    """
    示例 9: 便捷函数使用
    
    使用简化的便捷函数进行快速操作。
    """
    print("\n=== 示例 9: 便捷函数使用 ===")
    
    from mod import golomb_encode, golomb_decode, rice_encode, rice_decode
    
    # Golomb 编码便捷函数
    print("\nGolomb 编码便捷函数:")
    value = 25
    m = 10
    q, r = golomb_encode(value, m)
    decoded = golomb_decode(q, r, m)
    print(f"值 {value} (M={m}): q={q}, r={r}, decoded={decoded}")
    
    # Rice 编码便捷函数
    print("\nRice 编码便捷函数:")
    value = 25
    k = 3  # M = 8
    q, r = rice_encode(value, k)
    decoded = rice_decode(q, r, k)
    print(f"值 {value} (k={k}): q={q}, r={r}, decoded={decoded}")
    
    # 序列压缩便捷函数
    print("\n序列压缩便捷函数:")
    values = [1, 10, 50, 100, 500]
    
    compressed = compress_sorted_integers(values)
    decompressed = decompress_sorted_integers(compressed)
    
    print(f"原始: {values}")
    print(f"压缩后: {len(compressed)} 字节")
    print(f"解压后: {decompressed}")


def main():
    """运行所有示例"""
    examples = [
        example_1_basic_golomb,
        example_2_rice_coding,
        example_3_optimal_parameter,
        example_4_delta_golomb_compression,
        example_5_bitstream_operations,
        example_6_smart_encoding,
        example_7_inverted_index_simulation,
        example_8_custom_m_parameter,
        example_9_convenience_functions,
    ]
    
    for example in examples:
        example()
        print("\n" + "=" * 60)
    
    print("\n所有示例完成!")


if __name__ == "__main__":
    main()