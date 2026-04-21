#!/usr/bin/env python3
"""
Netmask Utilities 使用示例

展示常用功能的完整示例代码。
"""

from netmask_utils import (
    # 类
    IPv4Address, IPv6Address, Subnet,
    # 函数
    is_valid_ipv4, is_valid_ipv6, is_valid_ip,
    ip_to_int, int_to_ip,
    cidr_to_mask, mask_to_cidr,
    parse_cidr,
    get_network_address, get_broadcast_address,
    get_first_host, get_last_host,
    get_host_count, get_host_range,
    is_ip_in_subnet,
    split_subnet, merge_subnets,
    find_smallest_subnet,
    list_available_ips,
)


def example_ip_validation():
    """IP地址验证示例"""
    print("=" * 50)
    print("IP地址验证")
    print("=" * 50)
    
    # IPv4验证
    test_ips = [
        "192.168.1.1",
        "255.255.255.255",
        "0.0.0.0",
        "256.1.1.1",  # 无效
        "1.1.1",      # 无效
    ]
    
    for ip in test_ips:
        valid = is_valid_ipv4(ip)
        print(f"  {ip}: {'✓ 有效' if valid else '✗ 无效'}")
    
    print()
    
    # IPv6验证
    test_ipv6 = [
        "2001:db8::1",
        "::1",
        "::",
        "fe80::1",
        "gggg::1",  # 无效
    ]
    
    for ip in test_ipv6:
        valid = is_valid_ipv6(ip)
        print(f"  {ip}: {'✓ 有效' if valid else '✗ 无效'}")
    
    print()


def example_ip_conversion():
    """IP地址转换示例"""
    print("=" * 50)
    print("IP地址转换")
    print("=" * 50)
    
    # 字符串 <-> 整数转换
    ip = "192.168.1.100"
    ip_int = ip_to_int(ip)
    print(f"  {ip} → 整数: {ip_int}")
    print(f"  {ip_int} → IP: {int_to_ip(ip_int)}")
    
    print()
    
    # 特殊地址
    special = [
        ("0.0.0.0", "最小地址"),
        ("255.255.255.255", "最大地址"),
        ("127.0.0.1", "回环地址"),
        ("192.168.1.1", "私有地址"),
    ]
    
    for addr, desc in special:
        num = ip_to_int(addr)
        print(f"  {addr} ({desc}): {num}")
    
    print()


def example_cidr_operations():
    """CIDR操作示例"""
    print("=" * 50)
    print("CIDR操作")
    print("=" * 50)
    
    # CIDR转掩码
    prefixes = [8, 16, 24, 25, 30, 32]
    print("  CIDR前缀 → 子网掩码:")
    for p in prefixes:
        mask = cidr_to_mask(p, 4)
        mask_ip = int_to_ip(mask, 4)
        print(f"    /{p} → {mask_ip} (0x{mask:08X})")
    
    print()
    
    # 掩码转CIDR
    masks = ["255.0.0.0", "255.255.0.0", "255.255.255.0", "255.255.255.252"]
    print("  子网掩码 → CIDR前缀:")
    for mask in masks:
        prefix = mask_to_cidr(mask, 4)
        print(f"    {mask} → /{prefix}")
    
    print()


def example_subnet_operations():
    """子网操作示例"""
    print("=" * 50)
    print("子网操作")
    print("=" * 50)
    
    # 创建子网
    subnet = Subnet("192.168.1.0/24")
    print(f"  子网: {subnet}")
    print(f"    网络地址: {subnet.network}")
    print(f"    子网掩码: {subnet.mask}")
    print(f"    广播地址: {subnet.broadcast}")
    print(f"    可用主机: {subnet.first_host} - {subnet.last_host}")
    print(f"    主机数量: {subnet.host_count}")
    
    print()
    
    # 检查IP是否在子网内
    test_ips = ["192.168.1.1", "192.168.1.100", "192.168.2.1", "10.0.0.1"]
    print("  IP地址检查:")
    for ip in test_ips:
        in_subnet = subnet.contains(ip)
        print(f"    {ip}: {'✓ 在子网内' if in_subnet else '✗ 不在子网内'}")
    
    print()
    
    # 小型子网示例
    small_subnet = Subnet("192.168.1.0/30")
    print(f"  小型子网示例: {small_subnet}")
    print(f"    主机数量: {small_subnet.host_count}")
    print(f"    主机范围: {small_subnet.first_host} - {small_subnet.last_host}")
    
    print()


def example_subnet_split():
    """子网划分示例"""
    print("=" * 50)
    print("子网划分")
    print("=" * 50)
    
    # 将/24划分为4个/26
    original = "192.168.1.0/24"
    new_prefix = 26
    subnets = split_subnet(original, new_prefix)
    
    print(f"  划分 {original} 为 /{new_prefix} 子网:")
    for i, s in enumerate(subnets, 1):
        print(f"    {i}. {s}")
        print(f"       范围: {s.first_host} - {s.last_host} ({s.host_count}主机)")
    
    print()
    
    # 划分/24为2个/25
    subnets = split_subnet("10.0.0.0/24", 25)
    print(f"  划分 10.0.0.0/24 为 /25 子网:")
    for s in subnets:
        print(f"    {s}")
    
    print()


def example_subnet_merge():
    """子网合并示例"""
    print("=" * 50)
    print("子网合并")
    print("=" * 50)
    
    # 合并两个/25为一个/24
    subnets_to_merge = ["192.168.1.0/25", "192.168.1.128/25"]
    result = merge_subnets(subnets_to_merge)
    
    print(f"  合并 {subnets_to_merge}")
    if result:
        print(f"    结果: {result}")
    else:
        print("    无法合并")
    
    print()
    
    # 合并四个/26
    subnets_to_merge = [
        "10.0.0.0/26",
        "10.0.0.64/26",
        "10.0.0.128/26",
        "10.0.0.192/26"
    ]
    result = merge_subnets(subnets_to_merge)
    
    print(f"  合并四个/26子网:")
    if result:
        print(f"    结果: {result}")
    
    print()
    
    # 无法合并的情况
    invalid_merge = ["192.168.1.0/24", "192.168.2.0/25"]
    result = merge_subnets(invalid_merge)
    print(f"  尝试合并不兼容子网: {invalid_merge}")
    print(f"    结果: {'无法合并' if result is None else result}")
    
    print()


def example_find_smallest_subnet():
    """查找最小子网示例"""
    print("=" * 50)
    print("查找最小子网")
    print("=" * 50)
    
    # 示例1：两个IP - 找到最小子网（/25可以覆盖192.168.1.1到192.168.1.127）
    ips = ["192.168.1.1", "192.168.1.100"]
    result = find_smallest_subnet(ips)
    print(f"  IP列表: {ips}")
    print(f"  最小子网: {result}")  # 192.168.1.0/25
    
    print()
    
    # 示例2：不同网段 - 需要/22才能覆盖
    ips = ["192.168.1.1", "192.168.2.1"]
    result = find_smallest_subnet(ips)
    print(f"  IP列表: {ips}")
    print(f"  最小子网: {result}")  # 192.168.0.0/22
    
    print()
    
    # 示例3：多个IP
    ips = ["10.0.1.1", "10.0.1.50", "10.0.2.100", "10.0.3.200"]
    result = find_smallest_subnet(ips)
    print(f"  IP列表: {ips}")
    print(f"  最小子网: {result}")
    
    print()


def example_list_ips():
    """列出子网IP示例"""
    print("=" * 50)
    print("列出子网内所有IP")
    print("=" * 50)
    
    # /30子网
    cidr = "192.168.1.0/30"
    ips = list_available_ips(cidr)
    print(f"  {cidr} 可用IP:")
    for ip in ips:
        print(f"    {ip}")
    
    print()
    
    # 包含网络和广播地址
    ips = list_available_ips(cidr, include_network=True, include_broadcast=True)
    print(f"  {cidr} 所有IP (含网络和广播):")
    for ip in ips:
        print(f"    {ip}")
    
    print()
    
    # /29子网
    cidr = "10.0.0.0/29"
    ips = list_available_ips(cidr)
    print(f"  {cidr} 可用IP:")
    print(f"    {', '.join(str(ip) for ip in ips)}")
    
    print()


def example_ipv6_operations():
    """IPv6操作示例"""
    print("=" * 50)
    print("IPv6操作")
    print("=" * 50)
    
    # IPv6地址验证和转换
    ipv6 = "2001:db8::1"
    ip = IPv6Address(ipv6)
    print(f"  IPv6地址: {ip}")
    print(f"    整数形式: {int(ip)}")
    
    print()
    
    # IPv6子网
    subnet = Subnet("2001:db8::/32")
    print(f"  IPv6子网: {subnet}")
    print(f"    前缀长度: {subnet.prefix}")
    print(f"    包含 2001:db8:1::1: {subnet.contains('2001:db8:1::1')}")
    print(f"    包含 2001:db9::1: {subnet.contains('2001:db9::1')}")
    
    print()
    
    # IPv6地址压缩
    addresses = [
        "2001:0db8:0000:0000:0000:0000:0000:0001",
        "fe80:0000:0000:0000:0000:0000:0000:0001",
        "0000:0000:0000:0000:0000:0000:0000:0001",
    ]
    print("  IPv6地址压缩:")
    for addr in addresses:
        compressed = IPv6Address(addr)
        print(f"    {addr}")
        print(f"      → {compressed}")
    
    print()


def example_ip_address_class():
    """IPAddress类使用示例"""
    print("=" * 50)
    print("IPAddress类")
    print("=" * 50)
    
    # 创建IP地址
    ip1 = IPv4Address("192.168.1.1")
    ip2 = IPv4Address("192.168.1.100")
    ip3 = IPv4Address("192.168.1.1")
    
    print(f"  IP地址比较:")
    print(f"    {ip1} == {ip3}: {ip1 == ip3}")
    print(f"    {ip1} < {ip2}: {ip1 < ip2}")
    print(f"    {ip1} > {ip2}: {ip1 > ip2}")
    
    print()
    
    # 排序IP地址
    ips = [
        IPv4Address("10.0.0.1"),
        IPv4Address("192.168.1.1"),
        IPv4Address("172.16.0.1"),
        IPv4Address("10.0.0.2"),
    ]
    sorted_ips = sorted(ips)
    print(f"  排序IP地址:")
    for ip in sorted_ips:
        print(f"    {ip}")
    
    print()
    
    # 用作字典键
    ip_dict = {
        IPv4Address("192.168.1.1"): "网关",
        IPv4Address("192.168.1.100"): "服务器",
        IPv4Address("192.168.1.200"): "打印机",
    }
    print(f"  作为字典键:")
    for ip, desc in ip_dict.items():
        print(f"    {ip}: {desc}")
    
    print()


def example_network_calculations():
    """网络计算综合示例"""
    print("=" * 50)
    print("网络计算综合示例")
    print("=" * 50)
    
    # 场景：给定一个IP和前缀，计算所有信息
    ip = "192.168.100.50"
    prefix = 26
    
    network = get_network_address(ip, prefix)
    broadcast = get_broadcast_address(ip, prefix)
    first_host = get_first_host(ip, prefix)
    last_host = get_last_host(ip, prefix)
    host_count = get_host_count(prefix, 4)
    host_range = get_host_range(ip, prefix)
    
    print(f"  IP: {ip}/{prefix}")
    print(f"    网络地址: {network}")
    print(f"    广播地址: {broadcast}")
    print(f"    第一个主机: {first_host}")
    print(f"    最后一个主机: {last_host}")
    print(f"    主机数量: {host_count}")
    print(f"    主机范围: {host_range[0]} - {host_range[1]}")
    
    print()
    
    # 子网掩码二进制表示
    mask_int = cidr_to_mask(prefix, 4)
    mask_binary = bin(mask_int)[2:].zfill(32)
    mask_formatted = '.'.join([mask_binary[i:i+8] for i in range(0, 32, 8)])
    print(f"    子网掩码二进制: {mask_formatted}")
    
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 50)
    print("Netmask Utilities 使用示例")
    print("=" * 50 + "\n")
    
    example_ip_validation()
    example_ip_conversion()
    example_cidr_operations()
    example_subnet_operations()
    example_subnet_split()
    example_subnet_merge()
    example_find_smallest_subnet()
    example_list_ips()
    example_ipv6_operations()
    example_ip_address_class()
    example_network_calculations()
    
    print("=" * 50)
    print("示例运行完成")
    print("=" * 50)


if __name__ == "__main__":
    main()