"""
RLE Utilities 使用示例

演示游程编码工具的各种使用场景。
"""

import os
import sys

# 添加模块目录到路径
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module_dir)

from mod import (
    RLEEncoder, RLEDecoder, RLE, RLERun,
    StreamingRLEEncoder,
    rle_encode, rle_decode, rle_compress, rle_decompress
)


def example_basic_encoding():
    """基本编码示例"""
    print("=" * 50)
    print("基本编码示例")
    print("=" * 50)
    
    # 简单字符串编码
    text = "AAABBBCCCCDD"
    print(f"\n原文: {text}")
    
    # 使用便捷函数
    encoded = rle_encode(text)
    print(f"编码: {encoded}")
    
    decoded = rle_decode(encoded)
    print(f"解码: {decoded}")
    
    # 验证
    assert decoded == text, "编解码不一致！"
    print("✓ 编解码验证通过")


def example_compact_format():
    """紧凑格式示例"""
    print("\n" + "=" * 50)
    print("紧凑格式示例")
    print("=" * 50)
    
    texts = [
        "AAAAAABBBBBBCCCCCC",
        "AABCCDDEEEFFF",
        "ABCDEF",  # 无重复
        "AAAAAAAAAAAAAAAAAAA",  # 19个A
    ]
    
    for text in texts:
        compact = rle_compress(text)
        original = rle_decompress(compact)
        ratio = len(text) / len(compact) if len(compact) > 0 else 0
        
        print(f"\n原文: {text}")
        print(f"紧凑: {compact}")
        print(f"压缩比: {ratio:.2f}x")
        assert original == text


def example_bytes_encoding():
    """字节编码示例"""
    print("\n" + "=" * 50)
    print("字节编码示例")
    print("=" * 50)
    
    # 模拟图像数据（大量重复像素）
    image_data = bytes([0] * 100 + [255] * 50 + [128] * 75)
    print(f"\n原始数据长度: {len(image_data)} 字节")
    
    # 编码
    encoded = RLE.encode_bytes(image_data)
    print(f"编码后长度: {len(encoded)} 字节")
    print(f"编码数据 (hex): {encoded.hex()}")
    
    # 解码
    decoded = RLE.decode_bytes(encoded)
    print(f"解码后长度: {len(decoded)} 字节")
    
    # 验证
    assert decoded == image_data
    print("✓ 字节编解码验证通过")
    
    # 压缩效果
    ratio = len(image_data) / len(encoded)
    print(f"压缩比: {ratio:.2f}x")


def example_encoder_decoder():
    """编码器/解码器类示例"""
    print("\n" + "=" * 50)
    print("编码器/解码器类示例")
    print("=" * 50)
    
    # 创建编码器（自定义最小游程长度）
    encoder = RLEEncoder(min_run_length=3)
    
    text = "AABBCCCCCDDDDEEEEEE"
    print(f"\n原文: {text}")
    print(f"最小游程长度: 3")
    
    # 获取游程列表
    runs = encoder.encode_string(text)
    print(f"\n游程列表:")
    for run in runs:
        print(f"  {run}")
    
    # 紧凑编码（只压缩游程 >= 3 的）
    compact = encoder.encode_compact(text)
    print(f"\n紧凑编码: {compact}")
    
    # 解码
    decoder = RLEDecoder()
    decoded = decoder.decode_compact(compact)
    print(f"解码结果: {decoded}")


def example_streaming():
    """流式编码示例"""
    print("\n" + "=" * 50)
    print("流式编码示例")
    print("=" * 50)
    
    encoder = StreamingRLEEncoder()
    
    # 模拟流式数据输入
    chunks = ["AAA", "AAB", "BBB", "BCC", "CC"]
    
    print("\n分块输入:")
    all_completed = []
    
    for chunk in chunks:
        completed = encoder.feed(chunk)
        print(f"  输入 '{chunk}' -> 完成 {len(completed)} 个游程")
        all_completed.extend(completed)
    
    # 刷新最后的游程
    last_run = encoder.flush()
    if last_run:
        all_completed.append(last_run)
        print(f"  刷新 -> 最后游程: {last_run}")
    
    print(f"\n所有游程:")
    for run in all_completed:
        print(f"  {run}")
    
    # 验证
    expected = "AAAAABBBBBCCCC"  # 5A + 5B + 4C
    actual = "".join(run.value * run.count for run in all_completed)
    assert actual == expected, f"期望 {expected}, 实际 {actual}"
    print(f"✓ 流式编码验证通过: {actual}")


def example_analysis():
    """数据分析示例"""
    print("\n" + "=" * 50)
    print("数据分析示例")
    print("=" * 50)
    
    datasets = [
        ("高度可压缩", "A" * 100 + "B" * 100),
        ("低压缩性", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("混合数据", "AAABBCDDDDEEEFFG"),
        ("交替数据", "ABABABABABAB"),
    ]
    
    for name, data in datasets:
        analysis = RLE.analyze(data)
        print(f"\n{name}:")
        print(f"  数据长度: {len(data)}")
        print(f"  游程数量: {analysis['total_runs']}")
        print(f"  最大游程: {analysis['max_run_length']}")
        print(f"  平均游程: {analysis['avg_run_length']}")
        print(f"  压缩潜力: {analysis['compression_potential']:.2%}")


def example_image_compression():
    """图像压缩模拟示例"""
    print("\n" + "=" * 50)
    print("图像压缩模拟示例")
    print("=" * 50)
    
    # 模拟简单的 8 位灰度图像数据
    # 假设是一行 100 个像素
    image_row = bytes([0, 0, 0, 0, 0,  # 5个黑色像素
                       255, 255, 255,  # 3个白色
                       128, 128, 128, 128,  # 4个灰色
                       0, 0,  # 2个黑色
                       255, 255, 255, 255, 255,  # 5个白色
                       64, 64, 64,  # 3个深灰
                       192, 192])  # 2个浅灰
    
    print(f"原始行数据长度: {len(image_row)} 字节")
    
    # 编码
    encoded = RLE.encode_bytes(image_row)
    print(f"编码后长度: {len(encoded)} 字节")
    
    # 计算压缩效果
    compression_ratio = len(image_row) / len(encoded)
    space_saved = (1 - len(encoded) / len(image_row)) * 100
    
    print(f"压缩比: {compression_ratio:.2f}x")
    print(f"节省空间: {space_saved:.1f}%")
    
    # 解码验证
    decoded = RLE.decode_bytes(encoded)
    assert decoded == image_row
    print("✓ 图像数据编解码验证通过")


def example_log_compression():
    """日志压缩示例"""
    print("\n" + "=" * 50)
    print("日志压缩示例")
    print("=" * 50)
    
    # 模拟重复日志条目
    log_lines = "ERROR: Connection failed\n" * 50 + "INFO: Retrying...\n" * 20
    
    print(f"原始日志大小: {len(log_lines)} 字节")
    
    # 编码（作为字节）
    log_bytes = log_lines.encode('utf-8')
    encoded = RLE.encode_bytes(log_bytes)
    
    print(f"编码后大小: {len(encoded)} 字节")
    print(f"压缩比: {len(log_bytes) / len(encoded):.2f}x")
    
    # 解码
    decoded = RLE.decode_bytes(encoded)
    decoded_text = decoded.decode('utf-8')
    assert decoded_text == log_lines
    print("✓ 日志编解码验证通过")


def example_unicode():
    """Unicode 字符串示例"""
    print("\n" + "=" * 50)
    print("Unicode 字符串示例")
    print("=" * 50)
    
    # 中文
    chinese = "你好你好你好世界世界"
    encoded = rle_encode(chinese)
    decoded = rle_decode(encoded)
    print(f"中文: {chinese} -> {encoded} -> {decoded}")
    assert decoded == chinese
    
    # Emoji
    emojis = "😀😀😀🎉🎉🎊🎊🎊🎊"
    encoded = rle_encode(emojis)
    decoded = rle_decode(encoded)
    print(f"Emoji: {emojis} -> {encoded}")
    assert decoded == emojis
    
    print("✓ Unicode 编解码验证通过")


def example_compress_ratio():
    """压缩比计算示例"""
    print("\n" + "=" * 50)
    print("压缩比计算示例")
    print("=" * 50)
    
    test_cases = [
        ("全相同", "A" * 100),
        ("高度重复", "AAAAABBBBBCCCCC" * 10),
        ("无重复", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("随机混合", "AABBCCDDEEAABBCCDD"),
    ]
    
    print("\n压缩效果对比:")
    print("-" * 60)
    print(f"{'类型':<12} {'原始长度':<10} {'编码长度':<10} {'压缩比':<10}")
    print("-" * 60)
    
    for name, data in test_cases:
        encoded = rle_compress(data)
        ratio = RLE.compress_ratio(data, encoded)
        print(f"{name:<12} {len(data):<10} {len(encoded):<10} {ratio:<10.2f}x")


def main():
    """运行所有示例"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  RLE Utilities 使用示例".center(56) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    
    example_basic_encoding()
    example_compact_format()
    example_bytes_encoding()
    example_encoder_decoder()
    example_streaming()
    example_analysis()
    example_image_compression()
    example_log_compression()
    example_unicode()
    example_compress_ratio()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()