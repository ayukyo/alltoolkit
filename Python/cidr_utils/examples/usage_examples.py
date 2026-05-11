"""
CIDR Utils 使用示例
演示各种 CIDR 计算和网络操作功能
"""

import os
import sys

# 础保能找到模块
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# 尝试多种导入方式
try:
    from cidr_utils.mod import (
        CIDR,
        IPAddress,
        parse_cidr,
        ip_to_int,
        int_to_ip,
        prefix_to_netmask,
        netmask_to_prefix,
        is_valid_cidr,
        is_valid_ip,
        ip_in_cidr,
        get_ip_version,
        subnet_cidr,
        calculate_host_range,
        get_all_hosts,
        cidr_to_range,
        range_to_cidr,
        wildcard_to_cidr,
        get_network_class,
        is_private_ip,
        is_loopback_ip,
        is_multicast_ip,
        is_link_local_ip,
    )
except ImportError:
    # 直接从 mod 导入
    sys.path.insert(0, os.path.join(parent_dir, 'cidr_utils'))
    from mod import (
        CIDR,
        IPAddress,
        parse_cidr,
        ip_to_int,
        int_to_ip,
        prefix_to_netmask,
        netmask_to_prefix,
        is_valid_cidr,
        is_valid_ip,
        ip_in_cidr,
        get_ip_version,
        subnet_cidr,
        calculate_host_range,
        get_all_hosts,
        cidr_to_range,
        range_to_cidr,
        wildcard_to_cidr,
        get_network_class,
        is_private_ip,
        is_loopback_ip,
        is_multicast_ip,
        is_link_local_ip,
    )


def example_1_basic_cidr():
    """示例 1：基本 CIDR 信息"""
    print("\n=== 示例 1：基本 CIDR 信息 ===")
    
    cidr = CIDR('192.168.1.0/24')
    
    print(f"CIDR: {cidr}")
    print(f"网络地址: {cidr.network_address}")
    print(f"广播地址: {cidr.broadcast_address}")
    print(f"子网掩码: {cidr.netmask}")
    print(f"通配符掩码: {cidr.wildcard}")
    print(f"第一个主机: {cidr.first_host}")
    print(f"最后一个主机: {cidr.last_host}")
    print(f"总地址数: {cidr.num_addresses}")
    print(f"可用主机数: {cidr.num_hosts}")
    print(f"IP 版本: IPv{cidr.version}")


def example_2_ip_operations():
    """示例 2：IP 地址操作"""
    print("\n=== 示例 2：IP 地址操作 ===")
    
    # 创建 IP 地址
    ip1 = IPAddress('192.168.1.1')
    ip2 = IPAddress('192.168.1.100')
    
    print(f"IP1: {ip1}")
    print(f"IP2: {ip2}")
    
    # 比较操作
    print(f"IP1 < IP2: {ip1 < ip2}")
    print(f"IP1 整数值: {int(ip1)}")
    
    # 加减操作
    print(f"IP1 + 10: {ip1 + 10}")
    print(f"IP2 - 50: {ip2 - 50}")
    
    # 位运算
    mask = IPAddress('255.255.255.0')
    print(f"IP1 & 掩码: {ip1 & mask} (网络地址)")


def example_3_ip_in_subnet():
    """示例 3：检查 IP 是否在子网内"""
    print("\n=== 示例 3：检查 IP 是否在子网内 ===")
    
    cidr = CIDR('192.168.1.0/24')
    
    test_ips = [
        '192.168.1.1',
        '192.168.1.255',
        '192.168.2.1',
        '10.0.0.1',
    ]
    
    print(f"子网: {cidr}")
    for ip in test_ips:
        result = '✓ 在子网内' if ip in cidr else '✗ 不在子网内'
        print(f"  {ip}: {result}")


def example_4_subnet_division():
    """示例 4：子网划分"""
    print("\n=== 示例 4：子网划分 ===")
    
    original = CIDR('192.168.1.0/24')
    print(f"原始网络: {original}")
    
    # 划分为 4 个 /26 子网
    subnets = original.subnet(26)
    print(f"\n划分为 /26 子网 ({len(subnets)} 个):")
    
    for subnet in subnets:
        print(f"  {subnet} -> 主机范围: {subnet.first_host} - {subnet.last_host}")


def example_5_prefix_netmask_conversion():
    """示例 5：前缀长度与子网掩码转换"""
    print("\n=== 示例 5：前缀长度与子网掩码转换 ===")
    
    # 前缀转掩码
    prefixes = [8, 16, 20, 24, 28, 32]
    print("前缀长度 -> 子网掩码:")
    for prefix in prefixes:
        netmask = prefix_to_netmask(prefix)
        print(f"  /{prefix} -> {netmask}")
    
    # 掩码转前缀
    netmasks = ['255.0.0.0', '255.255.0.0', '255.255.255.0', '255.255.255.128']
    print("\n子网掩码 -> 前缀长度:")
    for netmask in netmasks:
        prefix = netmask_to_prefix(netmask)
        print(f"  {netmask} -> /{prefix}")


def example_6_range_to_cidr():
    """示例 6：IP 范围转 CIDR"""
    print("\n=== 示例 6：IP 范围转 CIDR ===")
    
    # 单个连续范围
    cidrs = range_to_cidr('192.168.1.0', '192.168.1.255')
    print(f"192.168.1.0 - 192.168.1.255:")
    for cidr in cidrs:
        print(f"  {cidr}")
    
    # 跨越多个子网的范围
    cidrs = range_to_cidr('192.168.0.0', '192.168.3.255')
    print(f"\n192.168.0.0 - 192.168.3.255:")
    for cidr in cidrs:
        print(f"  {cidr}")


def example_7_ip_classification():
    """示例 7：IP 地址分类"""
    print("\n=== 示例 7：IP 地址分类 ===")
    
    test_ips = [
        ('10.0.0.1', '私有 IP'),
        ('172.16.0.1', '私有 IP'),
        ('192.168.1.1', '私有 IP'),
        ('127.0.0.1', '环回地址'),
        ('224.0.0.1', '组播地址'),
        ('169.254.1.1', '链路本地'),
        ('8.8.8.8', '公网 IP'),
        ('1.1.1.1', '公网 IP'),
    ]
    
    for ip, expected in test_ips:
        classifications = []
        if is_private_ip(ip):
            classifications.append('私有')
        if is_loopback_ip(ip):
            classifications.append('环回')
        if is_multicast_ip(ip):
            classifications.append('组播')
        if is_link_local_ip(ip):
            classifications.append('链路本地')
        
        if not classifications:
            classifications.append('公网')
        
        result = '、'.join(classifications)
        print(f"  {ip}: {result} ({expected})")


def example_8_network_class():
    """示例 8：网络类别"""
    print("\n=== 示例 8：IPv4 网络类别 ===")
    
    test_ips = [
        '10.0.0.1',
        '128.0.0.1',
        '172.16.0.1',
        '192.168.1.1',
        '224.0.0.1',
        '240.0.0.1',
    ]
    
    for ip in test_ips:
        class_type = get_network_class(ip)
        print(f"  {ip}: 类别 {class_type}")


def example_9_ipv6_support():
    """示例 9：IPv6 支持"""
    print("\n=== 示例 9：IPv6 支持 ===")
    
    # IPv6 CIDR
    cidr = CIDR('2001:db8::/32')
    print(f"IPv6 CIDR: {cidr}")
    print(f"网络地址: {cidr.network_address}")
    print(f"总地址数: {cidr.num_addresses} (约 {cidr.num_addresses:.2e})")
    
    # IPv6 地址操作
    ip1 = IPAddress('2001:db8::1')
    ip2 = IPAddress('2001:db8::ffff')
    print(f"\nIPv6 IP1: {ip1}")
    print(f"IPv6 IP2: {ip2}")
    print(f"IP1 < IP2: {ip1 < ip2}")
    
    # IPv6 地址类型检查
    test_ipv6 = [
        ('fc00::1', 'ULA 私有'),
        ('fe80::1', '链路本地'),
        ('::1', '环回'),
        ('ff00::1', '组播'),
    ]
    
    print("\nIPv6 地址类型:")
    for ip, expected in test_ipv6:
        classifications = []
        if is_private_ip(ip):
            classifications.append('私有')
        if is_loopback_ip(ip):
            classifications.append('环回')
        if is_multicast_ip(ip):
            classifications.append('组播')
        if is_link_local_ip(ip):
            classifications.append('链路本地')
        
        result = '、'.join(classifications) if classifications else '公网'
        print(f"  {ip}: {result} ({expected})")


def example_10_wildcard_mask():
    """示例 10：通配符掩码"""
    print("\n=== 示例 10：通配符掩码转换 ===")
    
    # 从网络地址和通配符掩码创建 CIDR
    cidr = wildcard_to_cidr('192.168.1.0', '0.0.0.255')
    print(f"网络: 192.168.1.0, 通配符: 0.0.0.255")
    print(f"结果 CIDR: {cidr}")
    
    cidr = wildcard_to_cidr('10.0.0.0', '0.255.255.255')
    print(f"\n网络: 10.0.0.0, 通配符: 0.255.255.255")
    print(f"结果 CIDR: {cidr}")


def example_11_host_list():
    """示例 11：获取主机列表"""
    print("\n=== 示例 11：获取主机列表 ===")
    
    # 小型网络 - 显示所有主机
    cidr = CIDR('192.168.1.0/28')  # 16 地址, 14 主机
    hosts = cidr.hosts()
    
    print(f"网络 {cidr} 的所有主机 ({len(hosts)} 个):")
    print(f"  {', '.join(str(h) for h in hosts)}")
    
    # 大型网络 - 只显示范围
    cidr_large = CIDR('192.168.0.0/22')  # 1024 地址
    print(f"\n大型网络 {cidr_large}:")
    print(f"  主机数: {cidr_large.num_hosts}")
    print(f"  范围: {cidr_large.first_host} - {cidr_large.last_host}")


def example_12_cidr_info_dict():
    """示例 12：CIDR 信息字典"""
    print("\n=== 示例 12：获取完整信息 ===")
    
    cidr = CIDR('10.0.0.0/8')
    info = cidr.info()
    
    print(f"CIDR {cidr} 详细信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")


def example_13_validation():
    """示例 13：验证函数"""
    print("\n=== 示例 13：验证函数 ===")
    
    # 验证 CIDR
    test_cidrs = [
        '192.168.1.0/24',
        '10.0.0.0/8',
        'invalid',
        '192.168.1.0/33',
    ]
    
    print("CIDR 验证:")
    for cidr in test_cidrs:
        result = '✓ 有效' if is_valid_cidr(cidr) else '✗ 无效'
        print(f"  {cidr}: {result}")
    
    # 验证 IP
    test_ips = [
        '192.168.1.1',
        '255.255.255.255',
        '2001:db8::1',
        '256.1.1.1',
        'invalid',
    ]
    
    print("\nIP 验证:")
    for ip in test_ips:
        result = '✓ 有效' if is_valid_ip(ip) else '✗ 无效'
        print(f"  {ip}: {result}")


def example_14_common_networks():
    """示例 14：常见网络分析"""
    print("\n=== 示例 14：常见网络分析 ===")
    
    common_cidrs = [
        '10.0.0.0/8',       # A 类私有
        '172.16.0.0/12',    # B 类私有
        '192.168.0.0/16',   # C 类私有
        '127.0.0.0/8',      # 环回
        '224.0.0.0/4',      # 组播
        '0.0.0.0/0',        # 全网
    ]
    
    for cidr_str in common_cidrs:
        cidr = CIDR(cidr_str)
        print(f"\n{cidr_str}:")
        print(f"  网络地址: {cidr.network_address}")
        print(f"  广播地址: {cidr.broadcast_address}")
        print(f"  掩码: {cidr.netmask}")
        print(f"  地址数: {cidr.num_addresses}")
        print(f"  主机数: {cidr.num_hosts}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("CIDR Utils 使用示例")
    print("=" * 60)
    
    example_1_basic_cidr()
    example_2_ip_operations()
    example_3_ip_in_subnet()
    example_4_subnet_division()
    example_5_prefix_netmask_conversion()
    example_6_range_to_cidr()
    example_7_ip_classification()
    example_8_network_class()
    example_9_ipv6_support()
    example_10_wildcard_mask()
    example_11_host_list()
    example_12_cidr_info_dict()
    example_13_validation()
    example_14_common_networks()
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()