"""
字节操作工具模块使用示例

展示各种字节操作功能的实际应用场景。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from byte_utils.mod import ByteUtils


def example_endian_conversion():
    """示例：字节序转换（网络协议解析）"""
    print("\n" + "=" * 60)
    print("示例：字节序转换（网络协议解析）")
    print("=" * 60)
    
    # 模拟网络数据包（大端序）
    # 格式: 源端口(2字节), 目标端口(2字节), 序列号(4字节), 确认号(4字节)
    packet = b'\x00\x50\x00\x51\x12\x34\x56\x78\x87\x65\x43\x21'
    
    # 解析大端序字段
    src_port = ByteUtils.from_big_endian(packet[0:2])
    dst_port = ByteUtils.from_big_endian(packet[2:4])
    seq_num = ByteUtils.from_big_endian(packet[4:8])
    ack_num = ByteUtils.from_big_endian(packet[8:12])
    
    print(f"源端口: {src_port}")
    print(f"目标端口: {dst_port}")
    print(f"序列号: 0x{seq_num:08X}")
    print(f"确认号: 0x{ack_num:08X}")
    
    # 小端序常见于 x86 架构
    value = 0xDEADBEEF
    le_bytes = ByteUtils.to_little_endian(value, 4)
    print(f"\n值 0x{value:08X} 的小端序: {le_bytes.hex()}")
    
    # 大端序常见于网络协议
    be_bytes = ByteUtils.to_big_endian(value, 4)
    print(f"值 0x{value:08X} 的大端序: {be_bytes.hex()}")


def example_bit_manipulation():
    """示例：位操作（标志位管理）"""
    print("\n" + "=" * 60)
    print("示例：位操作（标志位管理）")
    print("=" * 60)
    
    # 模拟文件权限标志
    # 位: 0=执行, 1=写, 2=读
    # 格式: R W X
    
    # 创建用户权限
    user_perms = 0
    
    # 添加读权限
    user_perms = ByteUtils.set_bit(user_perms, 2)
    print(f"添加读权限后: {bin(user_perms)} (值: {user_perms})")
    
    # 添加写权限
    user_perms = ByteUtils.set_bit(user_perms, 1)
    print(f"添加写权限后: {bin(user_perms)} (值: {user_perms})")
    
    # 测试权限
    can_read = ByteUtils.test_bit(user_perms, 2)
    can_write = ByteUtils.test_bit(user_perms, 1)
    can_execute = ByteUtils.test_bit(user_perms, 0)
    print(f"\n权限检查:")
    print(f"  读: {'是' if can_read else '否'}")
    print(f"  写: {'是' if can_write else '否'}")
    print(f"  执行: {'是' if can_execute else '否'}")
    
    # 移除写权限
    user_perms = ByteUtils.clear_bit(user_perms, 1)
    print(f"\n移除写权限后: {bin(user_perms)}")
    
    # 翻转执行权限
    user_perms = ByteUtils.toggle_bit(user_perms, 0)
    print(f"翻转执行权限后: {bin(user_perms)}")
    
    # 提取权限组（模拟 3 位一组）
    full_perms = 0b111101100  # rwxrwxrwx
    owner = ByteUtils.get_bits(full_perms, 6, 3)
    group = ByteUtils.get_bits(full_perms, 3, 3)
    others = ByteUtils.get_bits(full_perms, 0, 3)
    print(f"\n完整权限 0b{full_perms:09b}:")
    print(f"  所有者: {bin(owner)} (rwx: {'r' if owner & 4 else '-'}{'w' if owner & 2 else '-'}{'x' if owner & 1 else '-'})")
    print(f"  组: {bin(group)} (rwx: {'r' if group & 4 else '-'}{'w' if group & 2 else '-'}{'x' if group & 1 else '-'})")
    print(f"  其他: {bin(others)} (rwx: {'r' if others & 4 else '-'}{'w' if others & 2 else '-'}{'x' if others & 1 else '-'})")


def example_hex_operations():
    """示例：十六进制操作（调试和分析）"""
    print("\n" + "=" * 60)
    print("示例：十六进制操作（调试和分析）")
    print("=" * 60)
    
    # 原始字节数据
    data = b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64'
    
    # 转换为十六进制字符串（调试用）
    hex_str = ByteUtils.to_hex(data, uppercase=True, separator=' ')
    print(f"原始数据: {data}")
    print(f"十六进制: {hex_str}")
    
    # 从十六进制恢复
    restored = ByteUtils.from_hex(hex_str)
    print(f"恢复数据: {restored}")
    
    # 验证十六进制字符串
    test_strings = ['deadbeef', 'DEADBEEF', 'hello', '12 34 56', '']
    print("\n十六进制验证:")
    for s in test_strings:
        is_valid = ByteUtils.is_hex(s)
        print(f"  '{s}': {'有效' if is_valid else '无效'}")


def example_data_packing():
    """示例：数据打包（协议构建）"""
    print("\n" + "=" * 60)
    print("示例：数据打包（协议构建）")
    print("=" * 60)
    
    # 构建一个简单的协议消息
    # 格式: 魔数(4字节) | 版本(1字节) | 类型(1字节) | 长度(2字节) | 数据
    
    magic = 0x89504E47  # PNG 魔数的一部分
    version = 1
    msg_type = 2
    payload = b'Hello, World!'
    
    # 构建消息头
    header = ByteUtils.concat(
        ByteUtils.to_big_endian(magic, 4),  # 魔数（大端序）
        bytes([version]),                     # 版本
        bytes([msg_type]),                    # 类型
        ByteUtils.to_big_endian(len(payload), 2)  # 长度
    )
    
    # 完整消息
    message = ByteUtils.concat(header, payload)
    
    print(f"消息头: {ByteUtils.to_hex(header, uppercase=True, separator=' ')}")
    print(f"载荷: {payload}")
    print(f"完整消息 ({len(message)} 字节): {ByteUtils.to_hex(message[:20], uppercase=True, separator=' ')}...")
    
    # 对齐到 16 字节边界
    aligned = ByteUtils.align_to_boundary(message, 16)
    print(f"对齐后 ({len(aligned)} 字节)")
    
    # 解析消息
    parsed_magic = ByteUtils.from_big_endian(aligned[0:4])
    parsed_version = aligned[4]
    parsed_type = aligned[5]
    parsed_length = ByteUtils.from_big_endian(aligned[6:8])
    parsed_payload = aligned[8:8+parsed_length]
    
    print("\n解析结果:")
    print(f"  魔数: 0x{parsed_magic:08X}")
    print(f"  版本: {parsed_version}")
    print(f"  类型: {parsed_type}")
    print(f"  长度: {parsed_length}")
    print(f"  载荷: {parsed_payload}")


def example_simple_encryption():
    """示例：简单 XOR 加密"""
    print("\n" + "=" * 60)
    print("示例：简单 XOR 加密")
    print("=" * 60)
    
    # 原始数据
    plaintext = b"Secret message: The password is 12345!"
    key = b"MySecretKey123!"
    
    # XOR 加密
    ciphertext = ByteUtils.xor_bytes(plaintext, key)
    print(f"原始: {plaintext}")
    print(f"密钥: {key}")
    print(f"密文: {ByteUtils.to_hex(ciphertext, separator=' ')}")
    
    # XOR 解密
    decrypted = ByteUtils.xor_bytes(ciphertext, key)
    print(f"解密: {decrypted}")
    
    # 验证
    assert decrypted == plaintext, "解密失败"
    print("✓ 加密/解密验证成功")


def example_checksums():
    """示例：校验和计算"""
    print("\n" + "=" * 60)
    print("示例：校验和计算")
    print("=" * 60)
    
    data = b"Hello, World!"
    
    # 各种校验和
    checksum_8 = ByteUtils.checksum_8bit(data)
    xor_sum = ByteUtils.checksum_xor(data)
    fletcher16 = ByteUtils.checksum_fletcher16(data)
    crc8 = ByteUtils.crc8(data)
    
    print(f"数据: {data}")
    print(f"\n校验结果:")
    print(f"  8位校验和: 0x{checksum_8:02X}")
    print(f"  XOR校验和: 0x{xor_sum:02X}")
    print(f"  Fletcher-16: 0x{fletcher16:04X}")
    print(f"  CRC-8: 0x{crc8:02X}")
    
    # 演示错误检测
    corrupted = data[:-1] + bytes([data[-1] ^ 0x01])  # 翻转最后一位
    crc8_corrupted = ByteUtils.crc8(corrupted)
    
    print(f"\n损坏数据: {corrupted}")
    print(f"  原始 CRC-8: 0x{crc8:02X}")
    print(f"  损坏 CRC-8: 0x{crc8_corrupted:02X}")
    print(f"  错误检测: {'检测到' if crc8 != crc8_corrupted else '未检测到'}")


def example_pattern_matching():
    """示例：字节模式匹配"""
    print("\n" + "=" * 60)
    print("示例：字节模式匹配")
    print("=" * 60)
    
    # 在二进制数据中查找模式
    data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10'
    
    # 查找 PNG 签名
    png_sig = b'\x89PNG'
    pos = ByteUtils.find_pattern(data, png_sig)
    print(f"PNG 签名位置: {pos}")
    
    # 查找 IHDR 块
    ihdr = b'IHDR'
    pos = ByteUtils.find_pattern(data, ihdr)
    print(f"IHDR 块位置: {pos}")
    
    # 使用通配符模式匹配
    # 查找模式: \x00\x00\x00?? (\x00\x00\x00 后跟任意两字节)
    patterns = ByteUtils.find_pattern_with_wildcard(data, '000000??')
    print(f"通配符模式 '000000??' 匹配位置: {patterns}")
    
    # 查找所有 \x00 出现位置
    zeros = ByteUtils.find_all_patterns(data, b'\x00')
    print(f"所有 \\x00 位置: {zeros}")
    
    # 替换模式
    modified = ByteUtils.replace_pattern(data, b'IHDR', b'tEXt')
    print(f"替换后 IHDR -> tEXt: {modified[:20]}")


def example_entropy_analysis():
    """示例：熵分析（数据压缩评估）"""
    print("\n" + "=" * 60)
    print("示例：熵分析（数据压缩评估）")
    print("=" * 60)
    
    # 不同类型的数据
    uniform_data = b'\x00' * 100  # 全零，熵 = 0
    random_like = bytes(range(256)) * 1  # 遍历所有字节值
    text_data = b"Hello, World! " * 10  # 重复文本
    
    # 计算熵
    entropy_uniform = ByteUtils.entropy(uniform_data)
    entropy_random = ByteUtils.entropy(random_like)
    entropy_text = ByteUtils.entropy(text_data)
    
    print(f"均匀数据熵: {entropy_uniform:.2f} (压缩潜力最高)")
    print(f"随机数据熵: {entropy_random:.2f} (压缩潜力最低)")
    print(f"文本数据熵: {entropy_text:.2f} (中等压缩潜力)")
    
    # 字节频率分析
    freq = ByteUtils.byte_frequency(text_data[:20])
    print(f"\n文本数据前20字节的频率分布:")
    for byte_val, count in sorted(freq.items(), key=lambda x: -x[1])[:5]:
        char = chr(byte_val) if 32 <= byte_val < 127 else '?'
        print(f"  0x{byte_val:02X} ('{char}'): {count} 次")


def example_byte_manipulation():
    """示例：字节操作实用技巧"""
    print("\n" + "=" * 60)
    print("示例：字节操作实用技巧")
    print("=" * 60)
    
    # 位反转（某些算法需要）
    value = 0b10110001
    reversed_val = ByteUtils.reverse_bits(value, 8)
    print(f"位反转: 0b{value:08b} -> 0b{reversed_val:08b}")
    
    # 循环移位（加密和哈希算法）
    value = 0b10110001
    rot_left = ByteUtils.rotate_left(value, 3, 8)
    rot_right = ByteUtils.rotate_right(value, 3, 8)
    print(f"循环左移3位: 0b{value:08b} -> 0b{rot_left:08b}")
    print(f"循环右移3位: 0b{value:08b} -> 0b{rot_right:08b}")
    
    # 字节序交换（跨平台数据交换）
    data = b'\x12\x34\x56\x78'
    swapped = ByteUtils.swap_endian(data)
    print(f"字节序交换: {data.hex()} -> {swapped.hex()}")
    
    # 查找重复模式
    data = b'\xAB\xCD\xAB\xCD\xAB\xCD\xEF\xEF\xEF'
    patterns = ByteUtils.find_repeating_patterns(data, min_length=2)
    print(f"\n重复模式分析:")
    for pattern, positions in patterns:
        print(f"  {pattern.hex()}: 位置 {positions}")


def main():
    """运行所有示例"""
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  字节操作工具模块 - 使用示例".center(56) + "  ║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    
    example_endian_conversion()
    example_bit_manipulation()
    example_hex_operations()
    example_data_packing()
    example_simple_encryption()
    example_checksums()
    example_pattern_matching()
    example_entropy_analysis()
    example_byte_manipulation()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()