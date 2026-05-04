"""
MAC Address Utilities 使用示例

展示如何使用 MAC 地址处理工具
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mac_address_utils.mod import (
    validate,
    normalize,
    to_colon_format,
    to_hyphen_format,
    to_dot_format,
    to_no_separator_format,
    get_oui,
    lookup_vendor,
    is_multicast,
    is_unicast,
    is_broadcast,
    is_locally_administered,
    is_globally_unique,
    generate_random,
    generate_random_multicast,
    increment,
    decrement,
    compare,
    is_equal,
    get_type_info,
    parse,
    from_bytes,
    from_integer,
    to_integer,
    generate_range,
    get_ip_multicast_mac,
    get_ipv6_multicast_mac,
    mask_mac,
    list_vendors,
)


def example_basic_validation():
    """基本验证示例"""
    print("=== MAC 地址验证示例 ===")
    
    mac_addresses = [
        "00:11:22:33:44:55",      # 冒号格式
        "00-11-22-33-44-55",      # 连字符格式
        "001122334455",           # 无分隔符
        "0011.2233.4455",         # Cisco点号格式
        "invalid_mac",            # 无效
        "00:11:22",               # 太短
        "GG:HH:II:JJ:KK:LL",      # 无效字符
    ]
    
    for mac in mac_addresses:
        valid = validate(mac)
        print(f"  {mac}: {valid}")
    
    print()


def example_format_conversion():
    """格式转换示例"""
    print("=== MAC 地址格式转换示例 ===")
    
    mac = "00-11-22-33-44-55"
    
    print(f"  输入: {mac}")
    print(f"  冒号格式: {to_colon_format(mac)}")
    print(f"  连字符格式: {to_hyphen_format(mac)}")
    print(f"  Cisco点号格式: {to_dot_format(mac)}")
    print(f"  无分隔符格式: {to_no_separator_format(mac)}")
    print()


def example_vendor_lookup():
    """厂商查询示例"""
    print("=== MAC 地址厂商查询示例 ===")
    
    mac_addresses = [
        "00:03:93:AB:CD:EF",  # Apple
        "00:0D:3A:12:34:56",  # Microsoft
        "00:0C:29:DE:AD:BE",  # VMware
        "52:54:00:11:22:33",  # QEMU/KVM
        "D8:1C:79:AB:CD:EF",  # Google
        "DE:AD:BE:EF:CA:FE",  # 未知厂商
    ]
    
    for mac in mac_addresses:
        vendor = lookup_vendor(mac)
        print(f"  {mac} -> {vendor if vendor else '未知厂商'}")
    
    print(f"\n  支持的厂商列表: {', '.join(list_vendors()[:10])}...")
    print()


def example_address_types():
    """地址类型判断示例"""
    print("=== MAC 地址类型判断示例 ===")
    
    mac_addresses = [
        ("00:11:22:33:44:55", "普通单播"),
        ("01:00:5E:00:00:01", "IPv4多播"),
        ("33:33:FF:00:00:01", "IPv6多播"),
        ("FF:FF:FF:FF:FF:FF", "广播地址"),
        ("02:11:22:33:44:55", "本地管理"),
    ]
    
    for mac, desc in mac_addresses:
        info = get_type_info(mac)
        print(f"  {mac} ({desc}):")
        print(f"    多播: {info['is_multicast']}, 单播: {info['is_unicast']}")
        print(f"    广播: {info['is_broadcast']}")
        print(f"    本地管理: {info['is_locally_administered']}, 全局唯一: {info['is_globally_unique']}")
    
    print()


def example_random_generation():
    """随机生成示例"""
    print("=== MAC 地址随机生成示例 ===")
    
    # 生成随机 MAC
    print("  随机MAC地址:")
    for i in range(3):
        mac = generate_random()
        print(f"    {mac}")
    
    # 使用指定厂商 OUI
    print("\n  使用Apple OUI:")
    for i in range(3):
        mac = generate_random(vendor="Apple")
        print(f"    {mac} (厂商: {lookup_vendor(mac)})")
    
    # 生成本地管理地址
    print("\n  本地管理地址:")
    for i in range(3):
        mac = generate_random(locally_administered=True)
        print(f"    {mac} (本地管理: {is_locally_administered(mac)})")
    
    # 生成多播地址
    print("\n  多播MAC地址:")
    for i in range(3):
        mac = generate_random_multicast()
        print(f"    {mac} (多播: {is_multicast(mac)})")
    
    print()


def example_arithmetic_operations():
    """算术运算示例"""
    print("=== MAC 地址算术运算示例 ===")
    
    mac = "00:11:22:33:44:50"
    
    print(f"  起始MAC: {mac}")
    print(f"  递增1: {increment(mac)}")
    print(f"  递增10: {increment(mac, 10)}")
    print(f"  递减1: {decrement(mac)}")
    print(f"  递减5: {decrement(mac, 5)}")
    
    # 生成范围
    print(f"\n  生成连续5个MAC:")
    macs = generate_range(mac, 5)
    for i, m in enumerate(macs):
        print(f"    {i}: {m}")
    
    # 进位示例
    mac = "00:11:22:33:44:FE"
    print(f"\n  进位示例:")
    print(f"    {mac} -> 递增2 -> {increment(mac, 2)}")
    
    print()


def example_comparison():
    """比较示例"""
    print("=== MAC 地址比较示例 ===")
    
    mac1 = "00:11:22:33:44:55"
    mac2 = "00:11:22:33:44:56"
    mac3 = "00:11:22:33:44:55"
    
    print(f"  比较 {mac1} 和 {mac2}: {compare(mac1, mac2)}")
    print(f"  比较 {mac1} 和 {mac3}: {compare(mac1, mac3)}")
    print(f"  比较 {mac2} 和 {mac1}: {compare(mac2, mac1)}")
    
    # 不同格式比较
    mac4 = "00-11-22-33-44-55"
    mac5 = "001122334455"
    print(f"\n  不同格式比较:")
    print(f"    {mac1} == {mac4}: {is_equal(mac1, mac4)}")
    print(f"    {mac1} == {mac5}: {is_equal(mac1, mac5)}")
    
    print()


def example_integer_conversion():
    """整数转换示例"""
    print("=== MAC 地址整数转换示例 ===")
    
    mac = "00:11:22:33:44:55"
    value = to_integer(mac)
    
    print(f"  MAC: {mac}")
    print(f"  整数值: {value}")
    print(f"  十六进制: 0x{value:X}")
    
    # 从整数创建
    new_mac = from_integer(value)
    print(f"  从整数恢复: {new_mac}")
    
    # 边界值
    print(f"\n  最小MAC: {from_integer(0)}")
    print(f"  最大MAC: {from_integer(0xFFFFFFFFFFFF)}")
    
    print()


def example_parse_and_build():
    """解析和构建示例"""
    print("=== MAC 地址解析和构建示例 ===")
    
    mac = "00:11:22:33:44:55"
    bytes_tuple = parse(mac)
    
    print(f"  MAC: {mac}")
    print(f"  解析为字节: {bytes_tuple}")
    
    # 从字节构建
    new_mac = from_bytes(*bytes_tuple)
    print(f"  从字节构建: {new_mac}")
    
    print()


def example_ip_multicast():
    """IP 多播 MAC 地址示例"""
    print("=== IP多播MAC地址转换示例 ===")
    
    # IPv4 多播
    ipv4_multicasts = [
        "224.0.0.1",       # 所有主机
        "224.0.0.2",       # 所有路由器
        "239.255.255.250", # SSDP
        "239.0.0.100",     # 自定义
    ]
    
    print("  IPv4多播地址:")
    for ip in ipv4_multicasts:
        mac = get_ip_multicast_mac(ip)
        print(f"    {ip} -> {mac}")
    
    # IPv6 多播
    ipv6_multicasts = [
        "ff02::1",         # 所有节点
        "ff02::2",         # 所有路由器
        "ff02::1:ff00:0",  # 需求节点多播
    ]
    
    print("\n  IPv6多播地址:")
    for ip in ipv6_multicasts:
        mac = get_ipv6_multicast_mac(ip)
        print(f"    {ip} -> {mac}")
    
    print()


def example_privacy_masking():
    """隐私遮蔽示例"""
    print("=== MAC 地址隐私遮蔽示例 ===")
    
    mac = "00:11:22:33:44:55"
    
    print(f"  原始MAC: {mac}")
    print(f"  默认遮蔽: {mask_mac(mac)}")
    print(f"  自定义遮蔽字符(X): {mask_mac(mac, 'X')}")
    print(f"  自定义遮蔽字符(?): {mask_mac(mac, '?')}")
    
    print()


def example_network_device_inventory():
    """网络设备资产示例"""
    print("=== 网络设备资产应用示例 ===")
    
    devices = [
        {"name": "Web服务器1", "mac": "00:03:93:AA:BB:CC"},
        {"name": "数据库服务器", "mac": "00:0D:3A:DD:EE:FF"},
        {"name": "虚拟机1", "mac": "00:0C:29:11:22:33"},
        {"name": "测试设备", "mac": "02:11:22:33:44:55"},
    ]
    
    print("  设备资产信息:")
    for device in devices:
        mac = device["mac"]
        vendor = lookup_vendor(mac) or "未知"
        info = get_type_info(mac)
        masked = mask_mac(mac)
        
        print(f"\n  {device['name']}:")
        print(f"    MAC: {masked}")
        print(f"    厂商: {vendor}")
        print(f"    类型: {'本地管理' if info['is_locally_administered'] else '全局唯一'}")
    
    print()


def example_vlan_mac_pool():
    """VLAN MAC 地址池示例"""
    print("=== VLAN MAC 地址池示例 ===")
    
    # 为 VLAN 100 生成 MAC 地址池
    base_mac = "00:01:64:00:00:01"
    vlan_macs = generate_range(base_mac, 20)
    
    print(f"  VLAN 100 MAC地址池 (基于 {base_mac}):")
    for i, mac in enumerate(vlan_macs[:10]):
        print(f"    端口{i}: {mac}")
    print(f"    ... (共 {len(vlan_macs)} 个地址)")
    
    print()


def main():
    """运行所有示例"""
    print()
    print("=" * 60)
    print("MAC Address Utilities 使用示例")
    print("=" * 60)
    print()
    
    example_basic_validation()
    example_format_conversion()
    example_vendor_lookup()
    example_address_types()
    example_random_generation()
    example_arithmetic_operations()
    example_comparison()
    example_integer_conversion()
    example_parse_and_build()
    example_ip_multicast()
    example_privacy_masking()
    example_network_device_inventory()
    example_vlan_mac_pool()
    
    print("=" * 60)
    print("示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()