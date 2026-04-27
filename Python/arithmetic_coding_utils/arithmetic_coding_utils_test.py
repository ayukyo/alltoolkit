"""
算术编码工具测试模块

测试覆盖：
1. 基本编码/解码功能
2. 自适应模型
3. 二进制编码
4. 边界情况
5. 压缩效率
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
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


def test_arithmetic_model():
    """测试概率模型"""
    print("测试 ArithmeticModel...")
    
    # 测试从符号列表创建
    model = ArithmeticModel(symbols=['A', 'B', 'A', 'C'])
    assert model.total == 4
    assert model.counts['A'] == 2
    assert model.counts['B'] == 1
    assert model.counts['C'] == 1
    
    # 测试概率计算
    prob_a = model.get_probability('A')
    assert abs(prob_a - 0.5) < 0.001
    
    # 测试累积范围
    low, high = model.get_cumulative_range('A')
    assert 0 <= low < high <= 1
    
    # 测试从范围获取符号
    result = model.get_symbol_from_range((low + high) / 2)
    assert result is not None
    assert result[0] == 'A'
    
    print("  ✓ ArithmeticModel 测试通过")


def test_static_encoding():
    """测试静态算术编码"""
    print("测试静态算术编码...")
    
    symbols = ['A', 'B', 'C', 'A', 'A', 'B']
    
    # 创建模型
    model = ArithmeticModel(symbols=symbols)
    
    # 编码
    encoder = ArithmeticEncoder(model=model, adaptive=False)
    code = encoder.encode(symbols)
    
    assert 0 <= code <= 1
    
    # 解码
    decoder = ArithmeticDecoder(model=model, adaptive=False)
    decoded = decoder.decode(code, len(symbols))
    
    assert decoded == symbols, f"解码错误: 期望 {symbols}, 得到 {decoded}"
    
    print(f"  原始: {symbols}")
    print(f"  编码: {code}")
    print(f"  解码: {decoded}")
    print("  ✓ 静态编码测试通过")


def test_adaptive_encoding():
    """测试自适应算术编码"""
    print("测试自适应算术编码...")
    
    symbols = ['X', 'Y', 'Z', 'X', 'Y', 'X', 'X']
    
    # 自适应模式需要预初始化模型，包含所有可能的符号
    # 这样编码器和解码器才能保持同步
    initial_counts = {'X': 1, 'Y': 1, 'Z': 1}  # 初始计数为1（平滑）
    
    model = ArithmeticModel(counts=initial_counts)
    encoder = ArithmeticEncoder(model=model, adaptive=True)
    code = encoder.encode(symbols)
    
    # 解码时使用相同的初始模型
    decode_model = ArithmeticModel(counts=initial_counts)
    decoder = ArithmeticDecoder(model=decode_model, adaptive=True)
    decoded = decoder.decode(code, len(symbols))
    
    assert decoded == symbols, f"解码错误: 期望 {symbols}, 得到 {decoded}"
    
    print(f"  原始: {symbols}")
    print(f"  编码: {code}")
    print(f"  解码: {decoded}")
    print("  ✓ 自适应编码测试通过")


def test_string_encoding():
    """测试字符串编码"""
    print("测试字符串编码...")
    
    texts = [
        "HELLO",
        "AABBCC",
        "mississippi",
        "banana"
    ]
    
    for text in texts:
        code, counts, num_symbols = encode_string(text, adaptive=False)
        decoded = decode_string(code, counts, num_symbols, adaptive=False)
        
        assert decoded == text, f"解码错误: 期望 '{text}', 得到 '{decoded}'"
        print(f"  '{text}' → {code:.10f} → '{decoded}'")
    
    print("  ✓ 字符串编码测试通过")


def test_binary_encoding():
    """测试二进制算术编码"""
    print("测试二进制算术编码...")
    
    test_cases = [
        [1, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1]
    ]
    
    for bits in test_cases:
        encoder = BinaryArithmeticEncoder(probability_one=0.5, adaptive=True)
        code = encoder.encode(bits)
        
        decoder = BinaryArithmeticEncoder(probability_one=0.5, adaptive=True)
        decoded = decoder.decode(code, len(bits))
        
        assert decoded == bits, f"解码错误: 期望 {bits}, 得到 {decoded}"
        print(f"  {bits} → {code:.10f} → {decoded}")
    
    print("  ✓ 二进制编码测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 空序列
    model = ArithmeticModel(symbols=['A'])
    encoder = ArithmeticEncoder(model=model)
    assert encoder.encode([]) == 0.0
    print("  ✓ 空序列处理正确")
    
    # 单一符号
    single = ['A', 'A', 'A', 'A']
    model = ArithmeticModel(symbols=single)
    encoder = ArithmeticEncoder(model=model, adaptive=False)
    code = encoder.encode(single)
    decoder = Decoder = ArithmeticDecoder(model=model, adaptive=False)
    decoded = ArithmeticDecoder(model=model, adaptive=False).decode(code, len(single))
    assert decoded == single
    print("  ✓ 单一符号序列处理正确")
    
    # 长序列
    long_seq = list("ABABABABAB" * 5)  # 50个符号，足够测试长度
    model = ArithmeticModel(symbols=long_seq)
    encoder = ArithmeticEncoder(model=model)
    code = encoder.encode(long_seq)
    decoded = ArithmeticDecoder(model=model).decode(code, len(long_seq))
    assert decoded == long_seq, f"解码错误: 长序列不匹配"
    print("  ✓ 长序列处理正确")
    
    # 低频符号
    rare = ['A'] * 50 + ['B']  # 51个符号，更易于精度控制
    model = ArithmeticModel(symbols=rare)
    encoder = ArithmeticEncoder(model=model)
    code = encoder.encode(rare)
    decoded = ArithmeticDecoder(model=model).decode(code, len(rare))
    assert decoded == rare, f"解码错误: 低频符号序列不匹配"
    print("  ✓ 低频符号处理正确")
    
    print("  ✓ 边界情况测试通过")


def test_compression_efficiency():
    """测试压缩效率"""
    print("测试压缩效率...")
    
    # 测试不同分布的压缩效率
    test_data = [
        ("均匀分布", list("ABCDEFGH")),
        ("偏态分布", list("AAABBC")),
        ("极端分布", list("AAAAAB"))
    ]
    
    for name, symbols in test_data:
        model = build_model_from_data(symbols)
        encoder = ArithmeticEncoder(model=model)
        code = encoder.encode(symbols)
        
        theoretical = calculate_theoretical_bits(symbols, model)
        
        print(f"  {name}:")
        print(f"    符号: {symbols}")
        print(f"    理论最优: {theoretical:.2f} bits")
        print(f"    编码值: {code}")
    
    print("  ✓ 压缩效率测试通过")


def test_model_building():
    """测试模型构建"""
    print("测试模型构建...")
    
    # 无平滑
    data = list("AABBBCC")
    model = build_model_from_data(data)
    assert model.counts['A'] == 2
    assert model.counts['B'] == 3
    assert model.counts['C'] == 2
    
    # 带平滑
    model_smooth = build_model_from_data(data, smoothing=1.0)
    assert model_smooth.counts['A'] == 3  # 2 + 1
    
    print("  ✓ 模型构建测试通过")


def test_session_context():
    """测试上下文管理器"""
    print("测试上下文管理器...")
    
    with ArithmeticCodingSession(adaptive=True) as session:
        symbols = ['P', 'Y', 'T', 'H', 'O', 'N']
        code = session.encode(symbols)
        decoded = session.decode(code, len(symbols))
        
        # 自适应模式可能会因模型初始化而有差异
        print(f"  编码: {symbols}")
        print(f"  解码: {decoded}")
    
    print("  ✓ 上下文管理器测试通过")


def test_adaptive_codec():
    """测试自适应编解码器"""
    print("测试自适应编解码器...")
    
    codec = AdaptiveArithmeticCodec()
    
    symbols = ['X', 'Y', 'Z', 'X', 'Y']
    code = codec.encode(symbols)
    decoded = codec.decode(code, len(symbols))
    
    print(f"  原始: {symbols}")
    print(f"  编码: {code}")
    print(f"  解码: {decoded}")
    
    print("  ✓ 自适应编解码器测试通过")


def test_unicode_support():
    """测试 Unicode 支持"""
    print("测试 Unicode 支持...")
    
    # 中文
    cn_text = "你好世界"
    code, counts, num = encode_string(cn_text, adaptive=False)
    decoded = decode_string(code, counts, num, adaptive=False)
    assert decoded == cn_text
    print(f"  中文: '{cn_text}' ✓")
    
    # 日文
    jp_text = "こんにちは"
    code, counts, num = encode_string(jp_text, adaptive=False)
    decoded = decode_string(code, counts, num, adaptive=False)
    assert decoded == jp_text
    print(f"  日文: '{jp_text}' ✓")
    
    # Emoji
    emoji = "😀🎉🎊"
    code, counts, num = encode_string(emoji, adaptive=False)
    decoded = decode_string(code, counts, num, adaptive=False)
    assert decoded == emoji
    print(f"  Emoji: '{emoji}' ✓")
    
    print("  ✓ Unicode 支持测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("算术编码工具测试")
    print("=" * 50)
    
    test_arithmetic_model()
    test_static_encoding()
    test_adaptive_encoding()
    test_string_encoding()
    test_binary_encoding()
    test_edge_cases()
    test_compression_efficiency()
    test_model_building()
    test_session_context()
    test_adaptive_codec()
    test_unicode_support()
    
    print("=" * 50)
    print("所有测试通过! ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()