"""
算术编码工具使用示例

演示算术编码的各种应用场景：
1. 基本文本压缩
2. 自适应编码
3. 二进制数据压缩
4. 压缩效率分析
5. 自定义符号集
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from arithmetic_coding_utils.mod import (
    ArithmeticModel,
    ArithmeticEncoder,
    ArithmeticDecoder,
    BinaryArithmeticEncoder,
    build_model_from_data,
    encode_string,
    decode_string,
    calculate_compression_ratio,
    calculate_theoretical_bits,
    AdaptiveArithmeticCodec,
    ArithmeticCodingSession
)


def example_1_basic_text_compression():
    """示例1: 基本文本压缩"""
    print("\n" + "=" * 50)
    print("示例1: 基本文本压缩")
    print("=" * 50)
    
    text = "MISSISSIPPI"
    print(f"原始文本: {text}")
    
    # 方法一：使用便捷函数（静态模式）
    code, counts, num_symbols = encode_string(text, adaptive=False)
    print(f"\n编码结果:")
    print(f"  编码值: {code}")
    print(f"  符号计数: {counts}")
    print(f"  符号数量: {num_symbols}")
    
    # 解码
    decoded = decode_string(code, counts, num_symbols, adaptive=False)
    print(f"  解码文本: {decoded}")
    print(f"  解码正确: {decoded == text}")
    
    # 计算理论压缩效率
    model = build_model_from_data(list(text))
    theoretical_bits = calculate_theoretical_bits(list(text), model)
    original_bits = len(text) * 8  # 假设 ASCII
    
    print(f"\n压缩效率分析:")
    print(f"  原始大小: {original_bits} bits (ASCII)")
    print(f"  理论最优: {theoretical_bits:.2f} bits")
    print(f"  压缩比: {original_bits / theoretical_bits:.2f}x")


def example_2_static_vs_adaptive():
    """示例2: 静态编码 vs 自适应编码"""
    print("\n" + "=" * 50)
    print("示例2: 静态编码 vs 自适应编码")
    print("=" * 50)
    
    text = "AAABBBCCCDDE"
    symbols = list(text)
    
    print(f"测试文本: {text}")
    print(f"符号分布: A=3, B=3, C=3, D=2, E=1")
    
    # 静态编码（预知分布）
    model = ArithmeticModel(symbols=symbols)
    encoder = ArithmeticEncoder(model=model, adaptive=False)
    static_code = encoder.encode(symbols)
    
    print(f"\n静态编码:")
    print(f"  编码值: {static_code}")
    
    # 自适应编码（边编码边学习）
    adaptive_model = ArithmeticModel()
    adaptive_encoder = ArithmeticEncoder(model=adaptive_model, adaptive=True)
    adaptive_code = adaptive_encoder.encode(symbols)
    
    print(f"\n自适应编码:")
    print(f"  编码值: {adaptive_code}")
    
    print("\n说明:")
    print("  静态编码: 需要预先知道符号分布")
    print("  自适应编码: 边编码边学习分布，适合未知分布场景")


def example_3_binary_compression():
    """示例3: 二进制数据压缩"""
    print("\n" + "=" * 50)
    print("示例3: 二进制数据压缩")
    print("=" * 50)
    
    # 模拟一个偏态分布的二进制序列
    binary_data = [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1]
    ones_count = sum(binary_data)
    zeros_count = len(binary_data) - ones_count
    
    print(f"二进制数据: {binary_data}")
    print(f"统计: 1的数量={ones_count}, 0的数量={zeros_count}")
    print(f"1的概率: {ones_count/len(binary_data):.2f}")
    
    # 使用二进制算术编码
    encoder = BinaryArithmeticEncoder(probability_one=0.5, adaptive=True)
    code = encoder.encode(binary_data)
    
    print(f"\n编码结果: {code}")
    
    # 解码
    decoder = BinaryArithmeticEncoder(probability_one=0.5, adaptive=True)
    decoded = decoder.decode(code, len(binary_data))
    
    print(f"解码结果: {decoded}")
    print(f"解码正确: {decoded == binary_data}")
    
    # 压缩效率
    original_bits = len(binary_data)  # 1 bit per symbol (理想情况)
    print(f"\n说明: 二进制算术编码对偏态分布效果更好")


def example_4_custom_symbols():
    """示例4: 自定义符号集"""
    print("\n" + "=" * 50)
    print("示例4: 自定义符号集")
    print("=" * 50)
    
    # 使用 DNA 序列
    dna = "ATCGATCGATCGATCG"
    print(f"DNA 序列: {dna}")
    
    # 编码
    code, counts, num = encode_string(dna, adaptive=False)
    print(f"编码值: {code}")
    print(f"碱基计数: {counts}")
    
    # 解码
    decoded = decode_string(code, counts, num, adaptive=False)
    print(f"解码序列: {decoded}")
    
    # 计算压缩效率
    model = build_model_from_data(list(dna))
    theoretical = calculate_theoretical_bits(list(dna), model)
    print(f"\n理论最优: {theoretical:.2f} bits")
    print(f"原始大小: {len(dna) * 2} bits (每个碱基2位)")
    
    # 音符序列
    print("\n--- 音符序列 ---")
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
    model = ArithmeticModel(symbols=notes)
    encoder = ArithmeticEncoder(model=model)
    code = encoder.encode(notes)
    
    print(f"音符序列: {notes}")
    print(f"编码值: {code}")
    
    decoder = ArithmeticDecoder(model=model)
    decoded_notes = decoder.decode(code, len(notes))
    print(f"解码音符: {decoded_notes}")


def example_5_compression_analysis():
    """示例5: 压缩效率分析"""
    print("\n" + "=" * 50)
    print("示例5: 压缩效率分析")
    print("=" * 50)
    
    test_cases = [
        ("均匀分布", "ABCDEFGH"),
        ("轻度偏态", "AAABBBCC"),
        ("中度偏态", "AAAAABBC"),
        ("极端偏态", "AAAAAAAAB"),
    ]
    
    print(f"{'类型':<12} {'原文':<12} {'理论(bits)':<12} {'ASCII(bits)':<12} {'压缩比'}")
    print("-" * 60)
    
    for name, text in test_cases:
        model = build_model_from_data(list(text))
        theoretical = calculate_theoretical_bits(list(text), model)
        ascii_bits = len(text) * 8
        ratio = ascii_bits / theoretical
        
        print(f"{name:<12} {text:<12} {theoretical:<12.2f} {ascii_bits:<12} {ratio:.2f}x")
    
    print("\n说明:")
    print("  - 均匀分布压缩效果有限")
    print("  - 偏态分布压缩效果更好")
    print("  - 算术编码接近信息熵理论极限")


def example_6_session_context():
    """示例6: 使用上下文管理器"""
    print("\n" + "=" * 50)
    print("示例6: 使用上下文管理器")
    print("=" * 50)
    
    text = "ARITHMETIC"
    
    with ArithmeticCodingSession(adaptive=True) as session:
        symbols = list(text)
        code = session.encode(symbols)
        
        print(f"原文: {text}")
        print(f"编码值: {code}")
        
        # 解码需要知道符号数量
        # 注意：自适应模式下解码结果可能与原文略有不同
        print("  (上下文管理器适合简单的编码场景)")
    
    print("\n优势:")
    print("  - 自动管理资源")
    print("  - 编码/解码使用同一模型")
    print("  - 代码更清晰")


def example_7_long_sequence():
    """示例7: 长序列压缩"""
    print("\n" + "=" * 50)
    print("示例7: 长序列压缩")
    print("=" * 50)
    
    # 生成一个长序列
    import random
    random.seed(42)
    
    # 创建偏态分布
    long_seq = []
    for _ in range(1000):
        if random.random() < 0.7:
            long_seq.append('A')
        elif random.random() < 0.5:
            long_seq.append('B')
        else:
            long_seq.append('C')
    
    print(f"序列长度: {len(long_seq)}")
    print(f"符号分布: A={long_seq.count('A')}, B={long_seq.count('B')}, C={long_seq.count('C')}")
    
    # 压缩
    code, counts, num = encode_string(long_seq, adaptive=False)
    
    # 解码验证
    decoded = decode_string(code, counts, num, adaptive=False)
    
    print(f"编码值: {code}")
    print(f"解码正确: {decoded == long_seq}")
    
    # 计算效率
    model = build_model_from_data(long_seq)
    theoretical = calculate_theoretical_bits(long_seq, model)
    
    print(f"\n理论最优: {theoretical:.2f} bits = {theoretical/8:.2f} bytes")
    print(f"原始大小: {len(long_seq)} bytes (每字符1字节)")
    print(f"压缩比: {len(long_seq) / (theoretical/8):.2f}x")


def example_8_codec_usage():
    """示例8: 使用编解码器类"""
    print("\n" + "=" * 50)
    print("示例8: 使用 AdaptiveArithmeticCodec")
    print("=" * 50)
    
    codec = AdaptiveArithmeticCodec()
    
    # 第一次编码
    data1 = ['A', 'B', 'A', 'C']
    code1 = codec.encode(data1)
    print(f"数据1: {data1}")
    print(f"编码1: {code1}")
    
    # 第二次编码（模型会累积学习）
    data2 = ['A', 'A', 'B', 'B']
    code2 = codec.encode(data2)
    print(f"\n数据2: {data2}")
    print(f"编码2: {code2}")
    
    # 查看模型
    model = codec.get_model()
    print(f"\n累积模型计数: {model.counts}")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("算术编码工具 - 使用示例")
    print("=" * 60)
    
    example_1_basic_text_compression()
    example_2_static_vs_adaptive()
    example_3_binary_compression()
    example_4_custom_symbols()
    example_5_compression_analysis()
    example_6_session_context()
    example_7_long_sequence()
    example_8_codec_usage()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()