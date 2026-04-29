"""
Elias 编码工具使用示例

本示例展示如何使用 Elias 编码工具进行整数编码和解码。
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # Gamma 编码
    elias_gamma_encode, elias_gamma_decode,
    elias_gamma_encode_sequence, elias_gamma_decode_sequence,
    # Delta 编码
    elias_delta_encode, elias_delta_decode,
    elias_delta_encode_sequence, elias_delta_decode_sequence,
    # Omega 编码
    elias_omega_encode, elias_omega_decode,
    elias_omega_encode_sequence, elias_omega_decode_sequence,
    # 工具函数
    compare_encodings, optimal_encode, get_encoding_stats,
    EliasEncoder, EliasDecoder
)


def basic_gamma_example():
    """Elias Gamma 基础示例"""
    print("=" * 50)
    print("Elias Gamma 编码示例")
    print("=" * 50)
    
    # 编码单个数字
    numbers = [1, 2, 3, 4, 5, 8, 16, 32, 100]
    
    print("\n单个数字编码:")
    for n in numbers:
        encoded = elias_gamma_encode(n)
        decoded = elias_gamma_decode(encoded)
        print(f"  {n} -> '{encoded}' (长度: {len(encoded)}) -> {decoded}")
    
    # 编码序列
    print("\n序列编码:")
    sequence = [1, 2, 3, 5, 8, 13, 21, 34]
    encoded = elias_gamma_encode_sequence(sequence)
    decoded = elias_gamma_decode_sequence(encoded, len(sequence))
    print(f"  输入: {sequence}")
    print(f"  编码: '{encoded}'")
    print(f"  解码: {decoded}")
    print(f"  总位数: {len(encoded)}")


def basic_delta_example():
    """Elias Delta 基础示例"""
    print("\n" + "=" * 50)
    print("Elias Delta 编码示例")
    print("=" * 50)
    
    numbers = [1, 2, 3, 4, 5, 8, 16, 32, 100]
    
    print("\n单个数字编码:")
    for n in numbers:
        encoded = elias_delta_encode(n)
        decoded = elias_delta_decode(encoded)
        print(f"  {n} -> '{encoded}' (长度: {len(encoded)}) -> {decoded}")
    
    print("\n序列编码:")
    sequence = [1, 10, 100, 1000]
    encoded = elias_delta_encode_sequence(sequence)
    decoded = elias_delta_decode_sequence(encoded, len(sequence))
    print(f"  输入: {sequence}")
    print(f"  编码: '{encoded}'")
    print(f"  解码: {decoded}")
    print(f"  总位数: {len(encoded)}")


def basic_omega_example():
    """Elias Omega 基础示例"""
    print("\n" + "=" * 50)
    print("Elias Omega 编码示例")
    print("=" * 50)
    
    numbers = [1, 2, 3, 4, 5, 8, 16, 32, 100]
    
    print("\n单个数字编码:")
    for n in numbers:
        encoded = elias_omega_encode(n)
        decoded = elias_omega_decode(encoded)
        print(f"  {n} -> '{encoded}' (长度: {len(encoded)}) -> {decoded}")
    
    print("\n序列编码:")
    sequence = [1, 2, 4, 8, 16, 32, 64, 128]
    encoded = elias_omega_encode_sequence(sequence)
    decoded = elias_omega_decode_sequence(encoded, len(sequence))
    print(f"  输入: {sequence}")
    print(f"  编码: '{encoded}'")
    print(f"  解码: {decoded}")
    print(f"  总位数: {len(encoded)}")


def comparison_example():
    """编码比较示例"""
    print("\n" + "=" * 50)
    print("编码效率比较")
    print("=" * 50)
    
    numbers = [1, 2, 3, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000]
    
    print("\n各编码长度比较:")
    print(f"{'数字':>8} | {'二进制':>6} | {'Gamma':>6} | {'Delta':>6} | {'Omega':>6} | {'最优':>6}")
    print("-" * 55)
    
    for n in numbers:
        result = compare_encodings(n)
        print(f"{result['number']:>8} | {result['binary_length']:>6} | "
              f"{result['gamma']['length']:>6} | {result['delta']['length']:>6} | "
              f"{result['omega']['length']:>6} | {result['recommendation']:>6}")
    
    # 自动选择最优编码
    print("\n自动选择最优编码:")
    result, method = optimal_encode(1000)
    print(f"  1000 使用 {method} 编码: '{result[:20]}...' (长度: {len(result)})")


def statistics_example():
    """统计信息示例"""
    print("\n" + "=" * 50)
    print("编码统计信息")
    print("=" * 50)
    
    # 小数字序列
    small_numbers = list(range(1, 51))
    stats = get_encoding_stats(small_numbers)
    
    print(f"\n序列 [1..50] 统计:")
    print(f"  数量: {stats['count']}")
    print(f"  最小值: {stats['min']}")
    print(f"  最大值: {stats['max']}")
    print(f"  平均值: {stats['average']:.2f}")
    print(f"  普通二进制位数: {stats['binary_bits']}")
    print(f"  Gamma 编码位数: {stats['gamma_bits']}")
    print(f"  Delta 编码位数: {stats['delta_bits']}")
    print(f"  Omega 编码位数: {stats['omega_bits']}")
    print(f"  最佳方法: {stats['best_method']}")
    
    # 大数字序列
    large_numbers = list(range(1000, 1051))
    stats = get_encoding_stats(large_numbers)
    
    print(f"\n序列 [1000..1050] 统计:")
    print(f"  数量: {stats['count']}")
    print(f"  普通二进制位数: {stats['binary_bits']}")
    print(f"  Gamma 编码位数: {stats['gamma_bits']}")
    print(f"  Delta 编码位数: {stats['delta_bits']}")
    print(f"  Omega 编码位数: {stats['omega_bits']}")
    print(f"  最佳方法: {stats['best_method']}")


def bytes_format_example():
    """字节格式示例"""
    print("\n" + "=" * 50)
    print("字节格式编码")
    print("=" * 50)
    
    # 编码为字节
    numbers = [1, 2, 3, 5, 8, 13]
    
    print("\nGamma 编码为字节:")
    encoded = elias_gamma_encode_sequence(numbers, as_bytes=True)
    print(f"  输入: {numbers}")
    print(f"  字节数据: {encoded.hex()}")
    print(f"  字节长度: {len(encoded)} bytes")
    
    decoded = elias_gamma_decode_sequence(encoded, len(numbers))
    print(f"  解码结果: {decoded}")
    
    print("\nDelta 编码为字节:")
    encoded = elias_delta_encode_sequence(numbers, as_bytes=True)
    print(f"  字节数据: {encoded.hex()}")
    decoded = elias_delta_decode_sequence(encoded, len(numbers))
    print(f"  解码结果: {decoded}")


def stream_encoder_example():
    """流式编解码示例"""
    print("\n" + "=" * 50)
    print("流式编解码器")
    print("=" * 50)
    
    # 创建编码器
    encoder = EliasEncoder(method='delta')
    
    # 逐个添加数字
    encoder.encode(1)
    encoder.encode(100)
    encoder.encode(1000)
    
    print(f"\n已编码 {encoder.count} 个数字")
    print(f"总位数: {encoder.bit_length}")
    
    # 获取编码结果
    result = encoder.get_result()
    print(f"编码结果: '{result}'")
    
    # 创建解码器
    decoder = EliasDecoder(result, method='delta')
    
    # 逐个解码
    print("\n逐个解码:")
    while decoder.has_more:
        n = decoder.decode()
        print(f"  解码第 {decoder.decoded_count} 个: {n}")
    
    # 批量编码
    print("\n批量编码:")
    encoder2 = EliasEncoder(method='omega')
    encoder2.encode_all([1, 2, 4, 8, 16, 32])
    result2 = encoder2.get_result(as_bytes=True)
    
    decoder2 = EliasDecoder(result2, method='omega')
    decoded_all = decoder2.decode_all()
    print(f"  输入: [1, 2, 4, 8, 16, 32]")
    print(f"  解码全部: {decoded_all}")
    
    # 解码指定数量
    decoder3 = EliasDecoder(result2, method='omega')
    first_three = decoder3.decode_count(3)
    print(f"  解码前 3 个: {first_three}")


def real_world_example():
    """实际应用示例"""
    print("\n" + "=" * 50)
    print("实际应用场景")
    print("=" * 50)
    
    # 搜索引擎索引压缩示例
    print("\n1. 搜索引擎倒排索引压缩:")
    # 假设这是文档 ID 列表（通常是有序且可以差分编码）
    doc_ids = [1, 5, 12, 25, 37, 50, 78, 100, 150, 200]
    
    # 计算差分（实际应用中通常使用差分编码）
    gaps = [doc_ids[0]]
    for i in range(1, len(doc_ids)):
        gaps.append(doc_ids[i] - doc_ids[i-1])
    
    print(f"  文档 ID: {doc_ids}")
    print(f"  差分值: {gaps}")
    
    # 编码差分值
    delta_encoded = elias_delta_encode_sequence(gaps)
    print(f"  Delta 编码位数: {len(delta_encoded)}")
    
    # 与原始编码对比
    original_bits = sum(d.bit_length() for d in doc_ids)
    print(f"  原始二进制位数: {original_bits}")
    print(f"  压缩率: {(1 - len(delta_encoded)/original_bits)*100:.1f}%")
    
    # 数据传输示例
    print("\n2. 网络数据传输:")
    # 假设需要传输一组配置参数
    config_values = [1, 10, 50, 200, 500, 1000]
    
    encoded_bytes = elias_delta_encode_sequence(config_values, as_bytes=True)
    print(f"  配置值: {config_values}")
    print(f"  编码后字节: {encoded_bytes.hex()}")
    print(f"  传输大小: {len(encoded_bytes)} bytes")
    
    decoded = elias_delta_decode_sequence(encoded_bytes, len(config_values))
    print(f"  接收端解码: {decoded}")


def main():
    """运行所有示例"""
    basic_gamma_example()
    basic_delta_example()
    basic_omega_example()
    comparison_example()
    statistics_example()
    bytes_format_example()
    stream_encoder_example()
    real_world_example()
    
    print("\n" + "=" * 50)
    print("示例运行完成")
    print("=" * 50)


if __name__ == '__main__':
    main()