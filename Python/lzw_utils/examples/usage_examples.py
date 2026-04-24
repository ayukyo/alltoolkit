"""
LZW 工具库使用示例

本示例展示 LZW (Lempel-Ziv-Welch) 压缩算法的各种使用场景。
LZW 是一种基于字典的无损压缩算法，广泛用于 GIF、TIFF、PDF 等格式。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from lzw_utils.mod import (
    compress, decompress,
    compress_string, decompress_string,
    compress_to_hex, decompress_from_hex,
    get_compression_ratio, get_compression_stats,
    compress_stream,
    compress_gif, decompress_gif,
    LZWEncoder, LZWDecoder
)


def example_basic_compression():
    """基本压缩示例"""
    print("=" * 60)
    print("示例 1: 基本压缩和解压缩")
    print("=" * 60)
    
    # 原始数据
    original = b"TOBEORNOTTOBEORTOBEORNOTTOBEORNOTTOBEORTOBEORNOT"
    print(f"原始数据: {original}")
    print(f"原始大小: {len(original)} 字节")
    
    # 压缩
    compressed = compress(original)
    print(f"\n压缩后: {compressed.hex()}")
    print(f"压缩后大小: {len(compressed)} 字节")
    
    # 解压缩
    decompressed = decompress(compressed)
    print(f"\n解压后: {decompressed}")
    print(f"验证: {'成功' if decompressed == original else '失败'}")
    
    # 压缩率
    ratio = get_compression_ratio(original, compressed)
    print(f"压缩率: {ratio:.2%}")
    print(f"节省: {(1 - ratio) * 100:.1f}%\n")


def example_string_compression():
    """字符串压缩示例"""
    print("=" * 60)
    print("示例 2: 字符串压缩")
    print("=" * 60)
    
    texts = [
        "Hello, World! 你好，世界！🌍",
        "这是一段中文文本，用于测试 LZW 压缩算法的效果。" * 10,
        "The quick brown fox jumps over the lazy dog. " * 20,
    ]
    
    for text in texts:
        compressed = compress_string(text)
        decompressed = decompress_string(compressed)
        
        original_size = len(text.encode('utf-8'))
        ratio = len(compressed) / original_size if original_size > 0 else 0
        
        print(f"文本: '{text[:30]}...'")
        print(f"  原始: {original_size} 字节 -> 压缩后: {len(compressed)} 字节")
        print(f"  压缩率: {ratio:.2%}")
        print(f"  验证: {'成功' if decompressed == text else '失败'}\n")


def example_hex_format():
    """十六进制格式示例"""
    print("=" * 60)
    print("示例 3: 十六进制格式压缩")
    print("=" * 60)
    
    # 适用于需要在文本环境中传输压缩数据的场景
    data = b"Repeated patterns are easy to compress: ABABABABABABABABABAB"
    
    # 压缩为十六进制字符串
    hex_string = compress_to_hex(data)
    print(f"原始数据: {data}")
    print(f"十六进制: {hex_string}")
    
    # 从十六进制字符串解压
    restored = decompress_from_hex(hex_string)
    print(f"解压后: {restored}")
    print(f"验证: {'成功' if restored == data else '失败'}\n")


def example_streaming():
    """流式压缩示例"""
    print("=" * 60)
    print("示例 4: 流式压缩（大数据处理）")
    print("=" * 60)
    
    # 模拟大文件
    large_data = b"This is a line of text that will be repeated.\n" * 10000
    print(f"模拟大文件: {len(large_data) / 1024:.2f} KB")
    
    # 流式压缩
    compressed_chunks = []
    for chunk in compress_stream(large_data, chunk_size=4096):
        compressed_chunks.append(chunk)
    
    compressed = b''.join(compressed_chunks)
    print(f"压缩后: {len(compressed) / 1024:.2f} KB")
    
    # 统计
    stats = get_compression_stats(large_data, compressed)
    print(f"压缩率: {stats['ratio']:.2%}")
    print(f"节省空间: {stats['saved_bytes'] / 1024:.2f} KB")
    
    # 验证
    decompressed = decompress(compressed)
    print(f"验证: {'成功' if decompressed == large_data else '失败'}\n")


def example_encoder_decoder():
    """编码器和解码器类示例"""
    print("=" * 60)
    print("示例 5: 使用编码器和解码器类")
    print("=" * 60)
    
    # 创建编码器
    encoder = LZWEncoder(min_code_size=9, max_code_size=16)
    
    # 分块编码
    chunks = [b"First chunk. ", b"Second chunk. ", b"Third chunk."]
    for chunk in chunks:
        encoder.update(chunk)
    
    compressed = encoder.finish()
    print(f"分块编码完成，压缩后大小: {len(compressed)} 字节")
    
    # 创建解码器
    decoder = LZWDecoder(min_code_size=9, max_code_size=16)
    
    # 解码
    decompressed = decoder.update(compressed)
    original = b''.join(chunks)
    
    print(f"原始: {original}")
    print(f"解压: {decompressed}")
    print(f"验证: {'成功' if decompressed == original else '失败'}\n")


def example_gif_compression():
    """GIF 格式压缩示例"""
    print("=" * 60)
    print("示例 6: GIF 格式兼容压缩")
    print("=" * 60)
    
    # 模拟 GIF 图像数据（像素索引）
    # 假设是一个简单的调色板图像
    pixel_data = bytes([
        0, 0, 0, 1, 1, 1, 2, 2, 2,
        0, 0, 0, 1, 1, 1, 2, 2, 2,
        0, 0, 0, 1, 1, 1, 2, 2, 2,
    ] * 10)
    
    print(f"GIF 像素数据: {len(pixel_data)} 字节")
    
    # GIF 格式压缩
    compressed = compress_gif(pixel_data, min_code_size=8)
    print(f"GIF 压缩后: {len(compressed)} 字节")
    
    # 解压
    decompressed = decompress_gif(compressed, min_code_size=8)
    print(f"解压后: {len(decompressed)} 字节")
    print(f"验证: {'成功' if decompressed == pixel_data else '失败'}\n")


def example_compression_analysis():
    """压缩分析示例"""
    print("=" * 60)
    print("示例 7: 压缩效果分析")
    print("=" * 60)
    
    # 不同类型的数据
    datasets = {
        "高度重复": b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "中等重复": b"ABABABABABABABABABABABABABABABAB",
        "低重复": bytes(range(256)),
        "英文文本": b"The quick brown fox jumps over the lazy dog. " * 5,
        "混合内容": b"Hello World! " * 10 + bytes(range(50)),
    }
    
    print(f"{'数据类型':<12} {'原始大小':>10} {'压缩大小':>10} {'压缩率':>10} {'效果':>8}")
    print("-" * 54)
    
    for name, data in datasets.items():
        compressed = compress(data)
        stats = get_compression_stats(data, compressed)
        
        effect = "优秀" if stats['ratio'] < 0.5 else "良好" if stats['ratio'] < 1 else "膨胀"
        
        print(f"{name:<12} {stats['original_size']:>10} {stats['compressed_size']:>10} "
              f"{stats['ratio']:>10.2%} {effect:>8}")
    
    print()


def example_file_compression():
    """文件压缩模拟示例"""
    print("=" * 60)
    print("示例 8: 模拟文件压缩")
    print("=" * 60)
    
    # 模拟不同类型的文件内容
    file_types = {
        "log文件": b"2024-04-24 10:00:01 INFO: Application started\n" * 100,
        "CSV数据": b"id,name,value\n1,item1,100\n2,item2,200\n" * 50,
        "配置文件": b"[section]\nkey=value\nsetting=true\n" * 30,
        "源代码": b"def hello():\n    print('Hello, World!')\n" * 20,
    }
    
    total_original = 0
    total_compressed = 0
    
    for file_type, content in file_types.items():
        compressed = compress(content)
        ratio = get_compression_ratio(content, compressed)
        
        total_original += len(content)
        total_compressed += len(compressed)
        
        print(f"{file_type}:")
        print(f"  原始: {len(content):>6} 字节")
        print(f"  压缩: {len(compressed):>6} 字节")
        print(f"  压缩率: {ratio:.2%}")
        print(f"  节省: {(1 - ratio) * 100:.1f}%\n")
    
    overall_ratio = total_compressed / total_original if total_original > 0 else 0
    print(f"总体压缩率: {overall_ratio:.2%}")
    print(f"总节省: {(1 - overall_ratio) * 100:.1f}%\n")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("LZW 工具库使用示例")
    print("=" * 60 + "\n")
    
    example_basic_compression()
    example_string_compression()
    example_hex_format()
    example_streaming()
    example_encoder_decoder()
    example_gif_compression()
    example_compression_analysis()
    example_file_compression()
    
    print("=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()