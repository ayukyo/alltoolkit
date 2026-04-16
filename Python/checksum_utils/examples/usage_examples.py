"""
checksum_utils 使用示例

演示各种校验和计算方法的使用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from checksum_utils.mod import (
    CRC32, CRC64, Adler32, Fletcher, InternetChecksum, SimpleChecksum,
    ChecksumCalculator, crc32, crc64, adler32, fletcher16, fletcher32,
    fletcher64, internet_checksum
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 50)
    print("基本用法示例")
    print("=" * 50)
    
    data = "Hello, World!"
    
    print(f"\n测试数据: {data!r}")
    print(f"CRC32:     {ChecksumCalculator.to_hex(crc32(data), 8)}")
    print(f"CRC64:     {ChecksumCalculator.to_hex(crc64(data), 16)}")
    print(f"Adler32:   {ChecksumCalculator.to_hex(adler32(data), 8)}")
    print(f"Fletcher-16: {fletcher16(data)}")
    print(f"Fletcher-32: {ChecksumCalculator.to_hex(fletcher32(data), 8)}")
    print(f"Internet:  {ChecksumCalculator.to_hex(internet_checksum(data), 4)}")
    print(f"Sum8:      {ChecksumCalculator.sum8(data)}")
    print(f"XOR8:      {ChecksumCalculator.xor8(data)}")
    print(f"LRC:       {ChecksumCalculator.lrc(data)}")


def example_data_integrity():
    """数据完整性验证示例"""
    print("\n" + "=" * 50)
    print("数据完整性验证示例")
    print("=" * 50)
    
    # 模拟数据传输
    original_data = "重要数据: 用户ID=12345, 金额=1000.00"
    
    # 发送方计算校验和
    checksum = crc32(original_data)
    print(f"\n原始数据: {original_data}")
    print(f"CRC32 校验和: {ChecksumCalculator.to_hex(checksum, 8)}")
    
    # 模拟传输过程
    transmitted_data = original_data
    transmitted_checksum = checksum
    
    # 接收方验证
    received_checksum = crc32(transmitted_data)
    if received_checksum == transmitted_checksum:
        print("✓ 数据完整性验证通过!")
    else:
        print("✗ 数据完整性验证失败!")
    
    # 模拟数据损坏
    corrupted_data = original_data.replace("1000.00", "1000.01")
    corrupted_checksum = crc32(corrupted_data)
    print(f"\n损坏数据: {corrupted_data}")
    print(f"新 CRC32: {ChecksumCalculator.to_hex(corrupted_checksum, 8)}")
    if corrupted_checksum == transmitted_checksum:
        print("✓ 数据完整性验证通过!")
    else:
        print("✗ 数据完整性验证失败! 数据已损坏")


def example_file_verification():
    """文件校验示例"""
    print("\n" + "=" * 50)
    print("文件校验示例")
    print("=" * 50)
    
    import tempfile
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("这是一个测试文件的内容。\n" * 100)
        filepath = f.name
    
    try:
        # 计算文件校验和
        crc32_value = CRC32.calculate_file(filepath)
        crc64_value = CRC64.calculate_file(filepath)
        adler32_value = Adler32.calculate_file(filepath)
        
        print(f"\n文件: {filepath}")
        print(f"CRC32:   {ChecksumCalculator.to_hex(crc32_value, 8)}")
        print(f"CRC64:   {ChecksumCalculator.to_hex(crc64_value, 16)}")
        print(f"Adler32: {ChecksumCalculator.to_hex(adler32_value, 8)}")
        
        print("\n这些值可用于验证文件是否被修改。")
    finally:
        os.unlink(filepath)


def example_network_protocol():
    """网络协议校验示例"""
    print("\n" + "=" * 50)
    print("网络协议校验示例 (IP/TCP/UDP)")
    print("=" * 50)
    
    # 模拟 IP 头部
    ip_header = bytes([
        0x45, 0x00, 0x00, 0x3C,  # Version, IHL, TOS, Total Length
        0x00, 0x00, 0x00, 0x00,  # ID, Flags, Fragment Offset
        0x40, 0x01, 0x00, 0x00,  # TTL, Protocol, Header Checksum (placeholder)
        0xC0, 0xA8, 0x01, 0x01,  # Source IP: 192.168.1.1
        0xC0, 0xA8, 0x01, 0x02,  # Dest IP: 192.168.1.2
    ])
    
    # 计算 IP 头部校验和
    checksum = InternetChecksum.calculate(ip_header)
    
    print(f"\nIP 头部: {ip_header.hex()}")
    print(f"IP 头部校验和: {ChecksumCalculator.to_hex(checksum, 4)}")
    
    # 验证校验和
    # 在实际 IP 头部中，校验和字段应该包含计算出的值
    # 验证时，整个头部（包含校验和）的结果应该是 0xFFFF
    verified = InternetChecksum.verify(ip_header, checksum)
    print(f"验证结果: {'✓ 通过' if verified else '✗ 失败'}")


def example_incremental_calculation():
    """增量计算示例"""
    print("\n" + "=" * 50)
    print("增量计算示例")
    print("=" * 50)
    
    # 分块处理大数据
    chunks = [
        b"第一块数据 ",
        b"第二块数据 ",
        b"第三块数据 ",
        b"第四块数据"
    ]
    
    # CRC32 增量计算
    crc = 0
    for i, chunk in enumerate(chunks, 1):
        crc = CRC32.calculate(chunk, crc)
        print(f"块 {i} CRC32 增量值: {ChecksumCalculator.to_hex(crc, 8)}")
    
    # 与整体计算比较
    full_data = b"".join(chunks)
    full_crc = CRC32.calculate(full_data)
    print(f"\n最终 CRC32: {ChecksumCalculator.to_hex(crc, 8)}")
    print(f"整体 CRC32: {ChecksumCalculator.to_hex(full_crc, 8)}")
    print(f"结果一致: {'✓ 是' if crc == full_crc else '✗ 否'}")


def example_all_checksums():
    """计算所有校验和示例"""
    print("\n" + "=" * 50)
    print("一次性计算所有校验和")
    print("=" * 50)
    
    data = "测试数据 Test Data 12345"
    result = ChecksumCalculator.calculate_all(data)
    
    print(f"\n数据: {data!r}")
    print("\n所有校验和结果:")
    for name, value in result.items():
        if isinstance(value, int):
            print(f"  {name}: {value}")
        else:
            print(f"  {name}: {value}")


def example_protocol_validation():
    """协议数据验证示例"""
    print("\n" + "=" * 50)
    print("协议数据验证示例")
    print("=" * 50)
    
    # 模拟 Modbus RTU LRC 校验
    def calculate_modbus_lrc(data: bytes) -> int:
        """计算 Modbus LRC"""
        return SimpleChecksum.lrc(data)
    
    # Modbus 请求示例: 地址 01, 功能码 03, 寄存器地址 0000, 寄存器数量 000A
    request = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x0A])
    lrc = calculate_modbus_lrc(request)
    
    print(f"\nModbus RTU 请求: {request.hex().upper()}")
    print(f"LRC 校验和: {ChecksumCalculator.to_hex(lrc, 2)}")
    print(f"完整帧: {(request + bytes([lrc])).hex().upper()}")


def example_performance_comparison():
    """性能比较示例"""
    print("\n" + "=" * 50)
    print("不同校验和算法特点比较")
    print("=" * 50)
    
    print("""
算法         | 位宽  | 速度   | 错误检测能力 | 典型应用
-------------|-------|--------|-------------|------------------
CRC32        | 32位  | 中等   | 高          | ZIP, PNG, Ethernet
CRC64        | 64位  | 中等   | 非常高      | ISO 3309, 数据存储
Adler32      | 32位  | 快     | 中等        | zlib, PNG
Fletcher-16  | 16位  | 快     | 中等        | 通信协议
Fletcher-32  | 32位  | 快     | 中等        | 通信协议
Internet     | 16位  | 快     | 低          | IP, TCP, UDP
Sum8/XOR8    | 8位   | 非常快 | 低          | 简单校验
LRC          | 8位   | 快     | 低          | Modbus RTU
""")


if __name__ == '__main__':
    example_basic_usage()
    example_data_integrity()
    example_file_verification()
    example_network_protocol()
    example_incremental_calculation()
    example_all_checksums()
    example_protocol_validation()
    example_performance_comparison()
    
    print("\n" + "=" * 50)
    print("示例完成!")
    print("=" * 50)