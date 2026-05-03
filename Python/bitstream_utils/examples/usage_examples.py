"""
Bitstream Utils 使用示例

演示位流工具的各种用法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from bitstream_utils.mod import (
    BitReader, BitWriter, BitArray,
    count_bits, count_set_bits, reverse_bits,
    encode_varint, decode_varint,
    gray_encode, gray_decode
)


def example_basic_read_write():
    """基本读写示例"""
    print("\n" + "=" * 50)
    print("示例1: 基本读写操作")
    print("=" * 50)
    
    # 创建写入器
    writer = BitWriter()
    
    # 写入各种数据
    writer.write_bits(0b1010, 4)      # 写入4位
    writer.write_byte(0xAB)          # 写入1字节
    writer.write_uint16_be(0x1234)   # 写入16位大端
    writer.write_uint32_le(0xDEADBEEF)  # 写入32位小端
    writer.write_bool(True)          # 写入布尔值
    writer.write_varint(150)         # 写入变长整数
    
    # 获取数据
    data = writer.get_bytes()
    print(f"写入数据: {data.hex()}")
    print(f"总位数: {writer.bit_length}")
    
    # 读取数据
    reader = BitReader(data)
    print(f"\n读取结果:")
    print(f"  4位: {bin(reader.read_bits(4))}")
    print(f"  1字节: {hex(reader.read_byte())}")
    print(f"  16位大端: {hex(reader.read_uint16_be())}")
    print(f"  32位小端: {hex(reader.read_uint32_le())}")
    print(f"  布尔值: {reader.read_bool()}")
    print(f"  Varint: {reader.read_varint()}")


def example_varint_encoding():
    """Varint编码示例"""
    print("\n" + "=" * 50)
    print("示例2: 变长整数编码")
    print("=" * 50)
    
    values = [0, 1, 127, 128, 255, 256, 16384, 100000, 1000000]
    
    print(f"{'值':<12} {'编码字节':<20} {'字节数':<8}")
    print("-" * 42)
    
    for value in values:
        encoded = encode_varint(value)
        print(f"{value:<12} {encoded.hex():<20} {len(encoded):<8}")
    
    # 解码示例
    print("\n解码示例:")
    data = encode_varint(150)
    value, consumed = decode_varint(data)
    print(f"数据 {data.hex()} 解码为 {value}, 消耗 {consumed} 字节")


def example_elias_codes():
    """Elias编码示例"""
    print("\n" + "=" * 50)
    print("示例3: Elias编码（Gamma和Delta）")
    print("=" * 50)
    
    # Gamma编码 - 适合小整数
    print("Gamma编码:")
    writer = BitWriter()
    for i in [1, 2, 3, 4, 5, 10, 20]:
        writer.write_gamma(i)
    data = writer.get_bytes()
    print(f"编码 [1,2,3,4,5,10,20] 使用 {len(data)} 字节")
    
    # 读取验证
    reader = BitReader(data)
    decoded = [reader.read_gamma() for _ in range(7)]
    print(f"解码结果: {decoded}")
    
    # Delta编码 - 适合较大整数
    print("\nDelta编码:")
    writer = BitWriter()
    for i in [1, 10, 100, 1000]:
        writer.write_delta(i)
    data = writer.get_bytes()
    print(f"编码 [1,10,100,1000] 使用 {len(data)} 字节")
    
    reader = BitReader(data)
    decoded = [reader.read_delta() for _ in range(4)]
    print(f"解码结果: {decoded}")


def example_bit_array():
    """位数组示例"""
    print("\n" + "=" * 50)
    print("示例4: 位数组操作")
    print("=" * 50)
    
    # 创建位数组
    arr = BitArray(32)
    
    # 设置一些位
    arr.set(0)
    arr.set(5)
    arr.set(10)
    arr.set(31)
    
    print(f"位数组大小: {len(arr)}")
    print(f"设置的位数: {arr.count_set()}")
    print(f"第一个设置位: {arr.find_first_set()}")
    print(f"第一个清除位: {arr.find_first_clear()}")
    
    # 打印所有位
    bits = [str(arr[i]) for i in range(32)]
    print(f"位内容: {''.join(bits[:16])}")
    print(f"        {''.join(bits[16:])}")
    
    # 序列化
    data = arr.to_bytes()
    print(f"序列化为字节: {data.hex()}")


def example_bit_operations():
    """位操作函数示例"""
    print("\n" + "=" * 50)
    print("示例5: 位操作函数")
    print("=" * 50)
    
    value = 0b10110010
    
    print(f"原值: {bin(value)}")
    print(f"1的个数: {count_set_bits(value)}")
    print(f"所需位数: {count_bits(value)}")
    
    # 反转位
    reversed_val = reverse_bits(value, 8)
    print(f"反转后: {bin(reversed_val)}")
    
    # 循环移位
    rotated = rotate_left(value, 3, 8)
    print(f"循环左移3位: {bin(rotated)}")
    
    # 单个位操作
    print(f"第3位的值: {get_bit(value, 3)}")
    print(f"设置第0位: {bin(set_bit(value, 0))}")
    print(f"清除第1位: {bin(clear_bit(value, 1))}")
    print(f"翻转第0位: {bin(toggle_bit(value, 0))}")


def example_gray_code():
    """格雷码示例"""
    print("\n" + "=" * 50)
    print("示例6: 格雷码转换")
    print("=" * 50)
    
    print("二进制 -> 格雷码 -> 二进制")
    print("-" * 35)
    for i in range(16):
        gray = gray_encode(i)
        decoded = gray_decode(gray)
        print(f"{i:2d} ({bin(i)[2:].zfill(4)}) -> {bin(gray)[2:].zfill(4)} -> {decoded}")


def example_network_protocol():
    """模拟网络协议解析"""
    print("\n" + "=" * 50)
    print("示例7: 模拟网络协议解析")
    print("=" * 50)
    
    # 模拟一个简单的数据包
    # 格式: 版本(2位) | 类型(4位) | 标志(2位) | 序列号(16位) | 变长数据
    
    writer = BitWriter()
    
    # 写入头部
    writer.write_bits(2, 2)        # 版本 = 2
    writer.write_bits(10, 4)       # 类型 = 10
    writer.write_bits(0b11, 2)     # 标志 = ACK+URGENT
    writer.write_uint16_be(12345)  # 序列号
    
    # 写入变长数据
    payload = b"Hello, World!"
    writer.write_varint(len(payload))
    writer.write_bytes(payload)
    
    # 对齐
    writer.align_to_byte()
    
    data = writer.get_bytes()
    print(f"数据包: {data.hex()}")
    print(f"大小: {len(data)} 字节")
    
    # 解析
    reader = BitReader(data)
    version = reader.read_bits(2)
    msg_type = reader.read_bits(4)
    flags = reader.read_bits(2)
    seq = reader.read_uint16_be()
    payload_len = reader.read_varint()
    payload_data = reader.read_bytes(payload_len)
    
    print(f"\n解析结果:")
    print(f"  版本: {version}")
    print(f"  类型: {msg_type}")
    print(f"  标志: {bin(flags)}")
    print(f"  序列号: {seq}")
    print(f"  载荷长度: {payload_len}")
    print(f"  载荷数据: {payload_data}")


def example_compression_technique():
    """模拟压缩技术"""
    print("\n" + "=" * 50)
    print("示例8: 位级数据压缩")
    print("=" * 50)
    
    # 对比不同编码方式的效率
    test_data = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]  # 斐波那契数列
    
    # 固定32位编码
    writer32 = BitWriter()
    for v in test_data:
        writer32.write_bits(v, 32)
    size_fixed32 = len(writer32.get_bytes())
    
    # 固定16位编码
    writer16 = BitWriter()
    for v in test_data:
        writer16.write_bits(v, 16)
    size_fixed16 = len(writer16.get_bytes())
    
    # Varint编码
    writer_var = BitWriter()
    for v in test_data:
        writer_var.write_varint(v)
    size_varint = len(writer_var.get_bytes())
    
    # Gamma编码
    writer_gamma = BitWriter()
    for v in test_data:
        writer_gamma.write_gamma(v)
    size_gamma = len(writer_gamma.get_bytes())
    
    # Delta编码
    writer_delta = BitWriter()
    for v in test_data:
        writer_delta.write_delta(v)
    size_delta = len(writer_delta.get_bytes())
    
    print(f"编码数据: {test_data}")
    print(f"\n编码方式对比:")
    print(f"  固定32位: {size_fixed32} 字节")
    print(f"  固定16位: {size_fixed16} 字节")
    print(f"  Varint:   {size_varint} 字节")
    print(f"  Gamma:    {size_gamma} 字节")
    print(f"  Delta:    {size_delta} 字节")
    
    # 计算压缩率
    print(f"\n相比固定32位:")
    print(f"  Varint压缩率: {(1 - size_varint/size_fixed32) * 100:.1f}%")
    print(f"  Gamma压缩率:  {(1 - size_gamma/size_fixed32) * 100:.1f}%")
    print(f"  Delta压缩率:  {(1 - size_delta/size_fixed32) * 100:.1f}%")


def main():
    """运行所有示例"""
    print("\n" + "=" * 50)
    print("Bitstream Utils 使用示例集")
    print("=" * 50)
    
    example_basic_read_write()
    example_varint_encoding()
    example_elias_codes()
    example_bit_array()
    example_bit_operations()
    example_gray_code()
    example_network_protocol()
    example_compression_technique()
    
    print("\n" + "=" * 50)
    print("所有示例执行完毕!")
    print("=" * 50)


if __name__ == "__main__":
    main()