"""
Morse Code Decoder Utils 使用示例

演示：
1. 基本 Morse 码解码
2. 不同格式的 Morse 码
3. 信号解码
4. 信号质量分析
5. 常用短语快速解码
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


def example_basic_decode():
    """示例1：基本 Morse 码解码"""
    print("=" * 50)
    print("示例1：基本 Morse 码解码")
    print("=" * 50)
    
    # 简单字符
    print("\n单字符解码:")
    print(f"  .- → {decode_morse('.-')}")
    print(f"  -... → {decode_morse('-...')}")
    print(f"  --- → {decode_morse('---')}")
    
    # 单词
    print("\n单词解码:")
    print(f"  ... --- ... → {decode_morse('... --- ...')}")
    print(f"  .... . .-.. .-.. --- → {decode_morse('.... . .-.. .-.. ---')}")
    
    # 句子
    print("\n句子解码:")
    morse = "... --- ...   .-- .   .- .-. .   .... . .-. ."
    print(f"  {morse}")
    print(f"  → {decode_morse(morse)}")


def example_different_formats():
    """示例2：不同格式的 Morse 码"""
    print("\n" + "=" * 50)
    print("示例2：不同格式的 Morse 码")
    print("=" * 50)
    
    decoder = MorseDecoder()
    
    # 标准格式
    print("\n标准格式 (点和划):")
    morse = '.- -... -.-.'
    text, stats = decoder.decode_text(morse)
    print(f"  {morse} → {text}")
    
    # 使用 Unicode 符号
    print("\nUnicode 符号:")
    morse = '•− −••• −•−•'
    text, stats = decoder.decode_text(morse)
    print(f"  {morse} → {text}")
    
    # 使用下划线
    print("\n使用下划线代替划:")
    morse = '. _ _ . .'
    text, stats = decoder.decode_text(morse)
    print(f"  {morse} → {text}")
    
    # 不同分隔符
    print("\n使用不同分隔符:")
    morse = '.-/.../---'
    text, stats = decoder.decode_text(morse, char_sep='/')
    print(f"  {morse} → {text}")


def example_decoder_class():
    """示例3：使用 MorseDecoder 类"""
    print("\n" + "=" * 50)
    print("示例3：使用 MorseDecoder 类")
    print("=" * 50)
    
    decoder = MorseDecoder()
    
    # 解码并获取统计信息
    morse = "... --- ...   .-- .   .... .- ...- .   .-   .--. .-. --- -... .-.. . --"
    text, stats = decoder.decode_text(morse)
    
    print(f"\nMorse 码: {morse}")
    print(f"解码结果: {text}")
    print(f"\n统计信息:")
    print(f"  解码字符数: {stats['decoded_chars']}")
    print(f"  未知字符数: {stats['unknown_chars']}")
    print(f"  信号质量: {stats['signal_quality']:.2%}")


def example_signal_decode():
    """示例4：从信号解码"""
    print("\n" + "=" * 50)
    print("示例4：从信号解码")
    print("=" * 50)
    
    # 生成一个简单的 Morse 信号：HI
    # H = .... (4个点)
    # I = .. (2个点)
    
    sample_rate = 1000  # 1kHz 采样率
    unit_time = 0.1     # 100ms 单位时间
    unit_samples = int(unit_time * sample_rate)  # 100 samples
    
    signal = []
    
    # H = ....
    for _ in range(4):
        signal.extend([1.0] * unit_samples)  # 点
        signal.extend([0.0] * unit_samples)  # 间隙
    
    # 字符间隙（已有1个单位，再加2个）
    signal.extend([0.0] * unit_samples * 2)
    
    # I = ..
    for _ in range(2):
        signal.extend([1.0] * unit_samples)
        signal.extend([0.0] * unit_samples)
    
    # 解码
    text, stats = decode_signal(signal, sample_rate)
    
    print(f"\n生成的信号:")
    print(f"  采样率: {sample_rate} Hz")
    print(f"  单位时间: {unit_time * 1000} ms")
    print(f"  信号长度: {len(signal)} 样本 ({len(signal)/sample_rate:.2f}s)")
    print(f"\n解码结果: {text}")
    print(f"\n详细统计:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")


def example_signal_quality():
    """示例5：信号质量分析"""
    print("\n" + "=" * 50)
    print("示例5：信号质量分析")
    print("=" * 50)
    
    # 生成高质量信号
    print("\n高质量信号:")
    good_signal = []
    for _ in range(10):
        good_signal.extend([0.1] * 50)   # 低电平
        good_signal.extend([0.9] * 50)   # 高电平
    
    result = analyze_signal(good_signal, 1000)
    print(f"  质量: {result['quality']:.2%}")
    print(f"  信噪比估计: {result['snr_estimate']:.2f}")
    print(f"  稳定性: {result['stability']:.2%}")
    print(f"  阈值: {result['threshold']:.3f}")
    
    # 生成噪声信号
    print("\n噪声信号:")
    import random
    random.seed(123)
    noisy_signal = [0.3 + random.random() * 0.4 for _ in range(1000)]
    
    result = analyze_signal(noisy_signal, 1000)
    print(f"  质量: {result['quality']:.2%}")
    print(f"  信噪比估计: {result['snr_estimate']:.2f}")
    print(f"  稳定性: {result['stability']:.2%}")
    
    # 生成有噪声的真实信号
    print("\n有噪声的 Morse 信号 (SOS):")
    noisy_morse = []
    unit = 50
    for _ in range(3):  # S = ...
        noisy_morse.extend([0.8 + random.random() * 0.15 for _ in range(unit)])
        noisy_morse.extend([0.1 + random.random() * 0.15 for _ in range(unit)])
    noisy_morse.extend([random.random() * 0.2 for _ in range(unit * 2)])  # 字符间隙
    for _ in range(3):  # O = ---
        noisy_morse.extend([0.8 + random.random() * 0.15 for _ in range(unit * 3)])
        noisy_morse.extend([0.1 + random.random() * 0.15 for _ in range(unit)])
    noisy_morse.extend([random.random() * 0.2 for _ in range(unit * 2)])  # 字符间隙
    for _ in range(3):  # S = ...
        noisy_morse.extend([0.8 + random.random() * 0.15 for _ in range(unit)])
        noisy_morse.extend([0.1 + random.random() * 0.15 for _ in range(unit)])
    
    result = analyze_signal(noisy_morse, 1000)
    print(f"  质量: {result['quality']:.2%}")
    print(f"  信噪比估计: {result['snr_estimate']:.2f}")
    
    text, _ = decode_signal(noisy_morse, 1000)
    print(f"  解码结果: {text}")


def example_quick_decode():
    """示例6：快速解码常用短语"""
    print("\n" + "=" * 50)
    print("示例6：快速解码常用短语")
    print("=" * 50)
    
    print("\n内置常用短语:")
    for morse, text in list(COMMON_PHRASES.items())[:5]:
        print(f"  {morse} → {text}")
    
    print("\n使用 quick_decode:")
    print(f"  quick_decode('... --- ...') → {quick_decode('... --- ...')}")
    print(f"  quick_decode('.- .-.. .-..') → {quick_decode('.- .-.. .-..')}")
    print(f"  quick_decode('.... . .-.. .--.') → {quick_decode('.... . .-.. .--.')}")


def example_special_chars():
    """示例7：特殊字符解码"""
    print("\n" + "=" * 50)
    print("示例7：特殊字符解码")
    print("=" * 50)
    
    special_chars = [
        ('.-.-.-', '.'),
        ('--..--', ','),
        ('..--..', '?'),
        ('-.-.--', '!'),
        ('-..-.', '/'),
        ('-.--.', '('),
        ('-.--.-', ')'),
        ('.--.-.', '@'),
        ('...-..-', '$'),
    ]
    
    print("\n特殊字符:")
    for morse, char in special_chars:
        decoded = decode_morse(morse)
        print(f"  {morse} → {decoded} (期望: {char})")
    
    # 带特殊字符的句子
    print("\n带特殊字符的句子:")
    morse = '.. ...   ..- ... .--. .-.. --- .- -.. .. -. --.   .- -   ... --- ... .-.-.-'
    print(f"  {morse}")
    print(f"  → {decode_morse(morse)}")


def example_numbers():
    """示例8：数字解码"""
    print("\n" + "=" * 50)
    print("示例8：数字解码")
    print("=" * 50)
    
    # 数字 0-9
    numbers = [
        ('-----', '0'),
        ('.----', '1'),
        ('..---', '2'),
        ('...--', '3'),
        ('....-', '4'),
        ('.....', '5'),
        ('-....', '6'),
        ('--...', '7'),
        ('---..', '8'),
        ('----.', '9'),
    ]
    
    print("\n数字 0-9:")
    for morse, expected in numbers:
        decoded = decode_morse(morse)
        status = '✓' if decoded == expected else '✗'
        print(f"  {morse} → {decoded} {status}")
    
    # 电话号码
    print("\n电话号码:")
    morse = '.---- ..--- ...-- ....- ..... -.... --... ---.. ----.'
    print(f"  {morse}")
    print(f"  → {decode_morse(morse)}")


def example_real_world():
    """示例9：实际应用场景"""
    print("\n" + "=" * 50)
    print("示例9：实际应用场景")
    print("=" * 50)
    
    decoder = MorseDecoder()
    
    # 场景1：解码来自无线电的消息
    print("\n场景1：无线电接收消息")
    radio_message = "--. --- --- -..   -- --- .-. -. .. -. --.   . ...- . .-. -.-- -... --- -.. -.--"
    text, stats = decoder.decode_text(radio_message)
    print(f"  收到: {radio_message}")
    print(f"  解码: {text}")
    print(f"  质量: {stats['signal_quality']:.0%}")
    
    # 场景2：求救信号
    print("\n场景2：紧急求救信号")
    sos_signal = "... --- ..."
    print(f"  信号: {sos_signal}")
    print(f"  解码: {quick_decode(sos_signal)}")
    
    # 场景3：确认收到
    print("\n场景3：确认收到")
    confirmation = ".-.   ---   .---"  # R O K
    text, _ = decoder.decode_text(confirmation)
    print(f"  收到: {confirmation}")
    print(f"  解码: {text}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Morse Code Decoder Utils 使用示例")
    print("=" * 60)
    
    example_basic_decode()
    example_different_formats()
    example_decoder_class()
    example_signal_decode()
    example_signal_quality()
    example_quick_decode()
    example_special_chars()
    example_numbers()
    example_real_world()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()