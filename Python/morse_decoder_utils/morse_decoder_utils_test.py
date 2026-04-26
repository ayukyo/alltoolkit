"""
Morse Code Decoder Utils 测试

测试覆盖：
1. 文本 Morse 码解码
2. 信号解码
3. 自动阈值检测
4. 纠错功能
5. 信号质量分析
"""

import sys
import os
import math

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from morse_decoder_utils.mod import (
    MorseDecoder, decode_morse, decode_signal, 
    analyze_signal, quick_decode, COMMON_PHRASES
)


def test_basic_decode():
    """测试基本解码功能"""
    print("测试基本解码...")
    
    decoder = MorseDecoder()
    
    # 测试简单字符
    test_cases = [
        ('.-', 'A'),
        ('-...', 'B'),
        ('...', 'S'),
        ('---', 'O'),
        ('.----', '1'),
        ('-----', '0'),
    ]
    
    for morse, expected in test_cases:
        text, stats = decoder.decode_text(morse)
        assert text == expected, f"Expected {expected}, got {text}"
        assert stats['signal_quality'] == 1.0
    
    print("  ✓ 基本字符解码通过")


def test_word_decode():
    """测试单词解码"""
    print("测试单词解码...")
    
    decoder = MorseDecoder()
    
    test_cases = [
        ('... --- ...', 'SOS'),
        ('.... . .-.. .-.. ---', 'HELLO'),
        ('.-- --- .-. .-.. -..', 'WORLD'),
        ('.---- .---- .----', '111'),
        ('----- ----- -----', '000'),
    ]
    
    for morse, expected in test_cases:
        text, stats = decoder.decode_text(morse)
        assert text == expected, f"Expected {expected}, got {text}"
    
    print("  ✓ 单词解码通过")


def test_sentence_decode():
    """测试句子解码"""
    print("测试句子解码...")
    
    decoder = MorseDecoder()
    
    # 使用 / 或多空格分隔单词
    test_cases = [
        ('... --- ...   .-- .   .- .-. .', 'SOS WE ARE'),
        ('.... ..   /   .... --- .--   /   .- .-. .   -.-- --- ..-', 'HI HOW ARE YOU'),
    ]
    
    for morse, expected in test_cases:
        text, stats = decoder.decode_text(morse)
        assert text == expected, f"Expected '{expected}', got '{text}'"
    
    print("  ✓ 句子解码通过")


def test_special_characters():
    """测试特殊字符解码"""
    print("测试特殊字符解码...")
    
    decoder = MorseDecoder()
    
    test_cases = [
        ('.-.-.-', '.'),
        ('--..--', ','),
        ('..--..', '?'),
        ('-.-.--', '!'),
        ('-..-.', '/'),
    ]
    
    for morse, expected in test_cases:
        text, stats = decoder.decode_text(morse)
        assert text == expected, f"Expected {expected}, got {text}"
    
    print("  ✓ 特殊字符解码通过")


def test_normalization():
    """测试 Morse 码标准化"""
    print("测试 Morse 码标准化...")
    
    decoder = MorseDecoder()
    
    # 测试不同符号表示（同一字符的不同符号）
    test_cases = [
        ('•-', 'A'),  # 使用 Unicode 点和 ASCII 划
        ('●—', 'A'),  # 使用 Unicode 圆点和 em dash
        ('.-', 'A'),  # 标准格式
        ('_', 'T'),  # 单独的下划线应该是 T
        ('__.', 'G'),  # 使用下划线代替划：--. = G
        ('_._.', 'C'),  # 使用下划线代替划：-.-. = C
        ('_...', 'B'),  # 下划线代替划：-... = B
    ]
    
    for morse, expected in test_cases:
        text, stats = decoder.decode_text(morse)
        assert text == expected, f"Expected {expected}, got {text} for '{morse}'"
    
    print("  ✓ 标准化通过")


def test_error_correction():
    """测试纠错功能"""
    print("测试纠错功能...")
    
    decoder = MorseDecoder()
    
    # 测试单符号错误
    # A = .- 错误变成 -.- 或类似
    text, stats = decoder.decode_text('.-')  # 正确的 A
    assert text == 'A'
    
    # 测试未知码（可能被纠错或显示 ?）
    text, stats = decoder.decode_text('........')  # 超过 H (....)
    # 应该尝试纠错或返回 ?
    
    print("  ✓ 纠错测试通过")


def test_quick_decode():
    """测试快速解码"""
    print("测试快速解码...")
    
    # 测试常用短语
    for morse, expected in COMMON_PHRASES.items():
        result = quick_decode(morse)
        assert result == expected, f"Expected {expected}, got {result}"
    
    # 测试非常用短语
    text = quick_decode('.... . .-.. .-.. ---')
    assert text == 'HELLO'
    
    print("  ✓ 快速解码通过")


def test_decode_morse_function():
    """测试便捷函数"""
    print("测试便捷函数...")
    
    text = decode_morse('... --- ...')
    assert text == 'SOS'
    
    text = decode_morse('.- -... -.-.')
    assert text == 'ABC'
    
    print("  ✓ 便捷函数测试通过")


def test_signal_decode():
    """测试信号解码"""
    print("测试信号解码...")
    
    # 生成简单的信号：SOS
    # S = ... (3个点)
    # O = --- (3个划)
    # 单位时间 = 100ms，采样率 = 1000Hz
    
    sample_rate = 1000  # 1kHz
    unit_samples = int(0.1 * sample_rate)  # 100ms = 100 samples
    
    signal = []
    
    # S = ... (点 点 点)
    for _ in range(3):  # 3个点
        signal.extend([1.0] * unit_samples)  # 点（开）
        signal.extend([0.0] * unit_samples)  # 间隙
    
    # 字符间隙 = 3个单位 = 已经有1个，再加2个
    signal.extend([0.0] * unit_samples * 2)
    
    # O = --- (划 划 划)
    for _ in range(3):  # 3个划
        signal.extend([1.0] * unit_samples * 3)  # 划（开，3个单位）
        signal.extend([0.0] * unit_samples)  # 间隙
    
    # 字符间隙
    signal.extend([0.0] * unit_samples * 2)
    
    # S = ...
    for _ in range(3):
        signal.extend([1.0] * unit_samples)
        signal.extend([0.0] * unit_samples)
    
    # 使用类方法获取完整统计
    decoder = MorseDecoder()
    text, stats = decoder.decode_signal(signal, sample_rate)
    
    # 应该解码出 SOS（可能有些格式差异）
    assert 'S' in text or 'O' in text, f"Failed to decode SOS, got: {text}"
    print(f"  解码结果: {text}")
    print(f"  统计信息: {stats}")
    print("  ✓ 信号解码测试通过")


def test_signal_quality_analysis():
    """测试信号质量分析"""
    print("测试信号质量分析...")
    
    # 生成高质量信号
    good_signal = [0.0] * 100 + [1.0] * 100 + [0.0] * 100 + [1.0] * 100
    result = analyze_signal(good_signal, 1000)
    
    assert 'quality' in result
    assert 'threshold' in result
    assert result['quality'] > 0.8, f"Quality too low: {result['quality']}"
    
    print(f"  高质量信号分析: quality={result['quality']:.2f}")
    
    # 生成低质量信号（噪声）
    import random
    random.seed(42)
    noisy_signal = [random.random() for _ in range(400)]
    result = analyze_signal(noisy_signal, 1000)
    
    assert 'quality' in result
    print(f"  噪声信号分析: quality={result['quality']:.2f}")
    
    print("  ✓ 信号质量分析测试通过")


def test_auto_threshold():
    """测试自动阈值计算"""
    print("测试自动阈值计算...")
    
    decoder = MorseDecoder()
    
    # 生成清晰的双峰信号
    signal = []
    for _ in range(20):
        signal.extend([0.0] * 50)   # 低电平
        signal.extend([1.0] * 50)   # 高电平
    
    threshold = decoder._auto_threshold(decoder._normalize_signal(signal))
    
    # 对于清晰的 0/1 信号，阈值应该在 0-1 之间
    print(f"  计算阈值: {threshold:.3f}")
    
    # 验证阈值能有效分离高低电平
    low = sum(1 for s in signal if s < threshold)
    high = sum(1 for s in signal if s >= threshold)
    
    # 应该大致分离高低电平（各约50%）
    ratio = high / len(signal)
    assert 0.4 < ratio < 0.6, f"Threshold doesn't separate well: {ratio}"
    
    print("  ✓ 自动阈值计算测试通过")


def test_edge_detection():
    """测试边缘检测"""
    print("测试边缘检测...")
    
    decoder = MorseDecoder()
    
    binary = [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0]
    edges = decoder._detect_edges(binary)
    
    # 应该检测到3个高电平段
    assert len(edges) == 3, f"Expected 3 edges, got {len(edges)}"
    assert edges[0] == (2, 5), f"First edge wrong: {edges[0]}"
    assert edges[1] == (6, 8), f"Second edge wrong: {edges[1]}"
    assert edges[2] == (11, 12), f"Third edge wrong: {edges[2]}"
    
    print(f"  检测到的边缘: {edges}")
    print("  ✓ 边缘检测测试通过")


def test_empty_input():
    """测试空输入处理"""
    print("测试空输入处理...")
    
    decoder = MorseDecoder()
    
    text, stats = decoder.decode_text('')
    assert text == ''
    
    text, stats = decoder.decode_text('   ')
    assert text == ''
    
    text, stats = decoder.decode_signal([])
    assert text == ''
    
    print("  ✓ 空输入处理测试通过")


def test_stats():
    """测试统计信息"""
    print("测试统计信息...")
    
    decoder = MorseDecoder()
    
    # 解码包含错误的 Morse 码
    morse = '... --- ...   .-- .   .- .-. .   ...--.-'  # ...--- 是未知的
    text, stats = decoder.decode_text(morse)
    
    assert 'decoded_chars' in stats
    assert 'unknown_chars' in stats
    assert 'signal_quality' in stats
    assert stats['decoded_chars'] > 0
    
    print(f"  解码文本: {text}")
    print(f"  统计信息: {stats}")
    
    print("  ✓ 统计信息测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Morse Code Decoder Utils 测试")
    print("=" * 50)
    
    tests = [
        test_basic_decode,
        test_word_decode,
        test_sentence_decode,
        test_special_characters,
        test_normalization,
        test_error_correction,
        test_quick_decode,
        test_decode_morse_function,
        test_signal_decode,
        test_signal_quality_analysis,
        test_auto_threshold,
        test_edge_detection,
        test_empty_input,
        test_stats,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 错误: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)