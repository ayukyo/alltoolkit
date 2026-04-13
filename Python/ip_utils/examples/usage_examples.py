#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - IP Address Utilities Examples
===========================================
Demonstration of ip_utils module capabilities.

Run: python examples/usage_examples.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # IPv4 functions
    validate_ipv4, ipv4_to_int, int_to_ipv4, get_ipv4_class,
    is_private_ipv4, is_loopback_ipv4, is_link_local_ipv4,
    is_multicast_ipv4, is_reserved_ipv4, get_ipv4_info,
    
    # Subnet functions
    cidr_to_mask, mask_to_cidr, get_subnet_info, ip_in_subnet,
    get_all_hosts_in_subnet, split_subnet,
    
    # IPv6 functions
    validate_ipv6, expand_ipv6, compress_ipv6, ipv6_to_int, int_to_ipv6,
    is_private_ipv6, is_loopback_ipv6, is_link_local_ipv6,
    is_multicast_ipv6, get_ipv6_info,
    
    # General functions
    validate_ip, get_ip_version, compare_ips, sort_ips, parse_cidr,
    is_public_ip, get_local_ip_ranges
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def demo_ipv4_validation():
    """Demonstrate IPv4 validation."""
    print_section("IPv4 Validation")
    
    test_ips = [
        '192.168.1.1',
        '10.0.0.1',
        '256.1.1.1',    # Invalid
        '1.2.3',        # Invalid
        '127.0.0.1',
        '8.8.8.8',
    ]
    
    for ip in test_ips:
        result = "✓ Valid" if validate_ipv4(ip) else "✗ Invalid"
        print(f"  {ip:20s} → {result}")


def demo_ipv4_conversion():
    """Demonstrate IPv4 conversion."""
    print_section("IPv4 Conversion")
    
    test_ips = ['192.168.1.1', '10.0.0.1', '127.0.0.1', '8.8.8.8']
    
    print("\n  IPv4 → Integer → IPv4:")
    for ip in test_ips:
        num = ipv4_to_int(ip)
        back = int_to_ipv4(num)
        binary = format(num, '032b')
        print(f"  {ip:15s} → {num:12d} → {back:15s}")
        print(f"    Binary: {binary[:8]}.{binary[8:16]}.{binary[16:24]}.{binary[24:32]}")


def demo_ipv4_classification():
    """Demonstrate IPv4 classification."""
    print_section("IPv4 Classification")
    
    test_ips = [
        ('192.168.1.1', 'Private LAN'),
        ('10.0.0.1', 'Private LAN (Class A)'),
        ('172.16.0.1', 'Private LAN (Class B)'),
        ('127.0.0.1', 'Loopback'),
        ('169.254.1.1', 'Link-local'),
        ('224.0.0.1', 'Multicast'),
        ('192.0.2.1', 'TEST-NET (Reserved)'),
        ('8.8.8.8', 'Public DNS'),
        ('1.1.1.1', 'Public DNS'),
    ]
    
    print(f"\n  {'IP Address':<18} {'Class':<6} {'Private':<8} {'Loopback':<9} {'LinkLocal':<10} {'Public':<8}")
    print("  " + "-"*65)
    
    for ip, desc in test_ips:
        cls = get_ipv4_class(ip)
        priv = "✓" if is_private_ipv4(ip) else ""
        loop = "✓" if is_loopback_ipv4(ip) else ""
        link = "✓" if is_link_local_ipv4(ip) else ""
        pub = "✓" if is_public_ip(ip) else ""
        
        print(f"  {ip:<18} {cls:<6} {priv:<8} {loop:<9} {link:<10} {pub:<8}")


def demo_ipv4_info():
    """Demonstrate IPv4 info dataclass."""
    print_section("IPv4 Info Details")
    
    info = get_ipv4_info('192.168.1.100')
    
    print(f"""
  Address:        {info.address}
  Integer:        {info.integer}
  Binary:         {info.binary}
  Address Class:  {info.address_class}
  
  Classification:
    Private:      {'Yes' if info.is_private else 'No'}
    Loopback:     {'Yes' if info.is_loopback else 'No'}
    Link-Local:   {'Yes' if info.is_link_local else 'No'}
    Multicast:    {'Yes' if info.is_multicast else 'No'}
    Reserved:     {'Yes' if info.is_reserved else 'No'}
""")


def demo_subnet_operations():
    """Demonstrate subnet operations."""
    print_section("Subnet Operations")
    
    # CIDR to Mask
    print("\n  CIDR → Subnet Mask:")
    for prefix in [8, 16, 20, 24, 25, 28, 30, 32]:
        mask = cidr_to_mask(prefix)
        print(f"    /{prefix:<2} → {mask}")
    
    # Mask to CIDR
    print("\n  Subnet Mask → CIDR:")
    masks = ['255.0.0.0', '255.255.0.0', '255.255.255.0', '255.255.255.128', '255.255.255.252']
    for mask in masks:
        prefix = mask_to_cidr(mask)
        print(f"    {mask} → /{prefix}")
    
    # Subnet Info
    print("\n  Subnet Information for 192.168.1.0/24:")
    info = get_subnet_info('192.168.1.0/24')
    print(f"""
    Network Address:   {info.network_address}
    Broadcast Address:  {info.broadcast_address}
    First Usable:       {info.first_usable}
    Last Usable:        {info.last_usable}
    Subnet Mask:        {info.subnet_mask}
    CIDR Prefix:        /{info.cidr_prefix}
    Total Hosts:        {info.total_hosts:,}
    Usable Hosts:       {info.usable_hosts:,}
    Wildcard Mask:      {info.wildcard_mask}
""")
    
    # IP in subnet check
    print("  IP in Subnet Check:")
    test_cases = [
        ('192.168.1.100', '192.168.1.0/24'),
        ('192.168.2.1', '192.168.1.0/24'),
        ('10.0.0.5', '10.0.0.0/8'),
        ('172.16.5.10', '172.16.0.0/12'),
    ]
    for ip, subnet in test_cases:
        result = "✓ In subnet" if ip_in_subnet(ip, subnet) else "✗ Not in subnet"
        print(f"    {ip:15s} in {subnet:20s} → {result}")
    
    # Split subnet
    print("\n  Split Subnet 192.168.1.0/24 into /26:")
    subnets = split_subnet('192.168.1.0/24', None, 26)
    for subnet in subnets:
        info = get_subnet_info(subnet)
        print(f"    {subnet:20s} → {info.usable_hosts} usable hosts")


def demo_subnet_hosts():
    """Demonstrate getting all hosts in a subnet."""
    print_section("Subnet Host Enumeration")
    
    print("\n  Hosts in 192.168.1.0/30:")
    hosts = get_all_hosts_in_subnet('192.168.1.0/30')
    for host in hosts:
        print(f"    {host}")
    
    print("\n  Hosts in 10.0.0.0/29:")
    hosts = get_all_hosts_in_subnet('10.0.0.0/29')
    for host in hosts:
        print(f"    {host}")


def demo_ipv6_validation():
    """Demonstrate IPv6 validation."""
    print_section("IPv6 Validation")
    
    test_ips = [
        '::1',
        '::',
        '2001:db8::1',
        '2001:0db8:0000:0000:0000:0000:0000:0001',
        'fe80::1',
        'ff02::1',
        'fd00::1',
        'invalid::ip',
        '2001::db8::1',  # Invalid (double ::)
    ]
    
    for ip in test_ips:
        result = "✓ Valid" if validate_ipv6(ip) else "✗ Invalid"
        print(f"  {ip:45s} → {result}")


def demo_ipv6_conversion():
    """Demonstrate IPv6 conversion."""
    print_section("IPv6 Conversion")
    
    test_ips = ['::1', '2001:db8::1', 'fe80::1', 'ff02::1']
    
    print("\n  IPv6 → Expanded → Compressed:")
    for ip in test_ips:
        expanded = expand_ipv6(ip)
        compressed = compress_ipv6(expanded)
        print(f"  {ip:20s}")
        print(f"    Expanded:  {expanded}")
        print(f"    Compressed: {compressed}")
    
    print("\n  IPv6 → Integer → IPv6:")
    test_values = [('::', 0), ('::1', 1), ('::2', 2)]
    for ip, expected in test_values:
        num = ipv6_to_int(ip)
        back = int_to_ipv6(num)
        print(f"  {ip:10s} → {num:39d} → {back}")


def demo_ipv6_classification():
    """Demonstrate IPv6 classification."""
    print_section("IPv6 Classification")
    
    test_ips = [
        ('::1', 'Loopback'),
        ('fe80::1', 'Link-Local'),
        ('ff02::1', 'Multicast'),
        ('fd00::1', 'Private (ULA)'),
        ('2001:db8::1', 'Documentation'),
    ]
    
    print(f"\n  {'IPv6 Address':<30} {'Loopback':<9} {'LinkLocal':<10} {'Multicast':<10} {'Private':<8}")
    print("  " + "-"*75)
    
    for ip, desc in test_ips:
        loop = "✓" if is_loopback_ipv6(ip) else ""
        link = "✓" if is_link_local_ipv6(ip) else ""
        mcast = "✓" if is_multicast_ipv6(ip) else ""
        priv = "✓" if is_private_ipv6(ip) else ""
        
        print(f"  {ip:<30} {loop:<9} {link:<10} {mcast:<10} {priv:<8}")


def demo_general_utilities():
    """Demonstrate general IP utilities."""
    print_section("General IP Utilities")
    
    # IP version detection
    print("\n  IP Version Detection:")
    test_ips = ['192.168.1.1', '10.0.0.1', '::1', '2001:db8::1', 'invalid']
    for ip in test_ips:
        version = get_ip_version(ip)
        v_str = f"IPv{version}" if version else "Invalid"
        print(f"    {ip:20s} → {v_str}")
    
    # IP comparison
    print("\n  IP Comparison:")
    comparisons = [
        ('192.168.1.1', '192.168.1.2'),
        ('10.0.0.2', '10.0.0.1'),
        ('::1', '::2'),
    ]
    for ip1, ip2 in comparisons:
        result = compare_ips(ip1, ip2)
        cmp_str = "<" if result < 0 else ">" if result > 0 else "=="
        print(f"    {ip1} {cmp_str} {ip2}")
    
    # IP sorting
    print("\n  IP Sorting:")
    ips = ['192.168.1.3', '10.0.0.1', '192.168.1.1', '172.16.0.1', '192.168.1.2']
    sorted_ips = sort_ips(ips)
    print(f"    Original: {ips}")
    print(f"    Sorted:   {sorted_ips}")
    
    # CIDR parsing
    print("\n  CIDR Parsing:")
    cidrs = ['192.168.1.0/24', '10.0.0.0/8', '2001:db8::/32']
    for cidr in cidrs:
        addr, prefix = parse_cidr(cidr)
        print(f"    {cidr:20s} → Address: {addr}, Prefix: {prefix}")
    
    # Public IP check
    print("\n  Public IP Check:")
    test_ips = ['8.8.8.8', '1.1.1.1', '192.168.1.1', '10.0.0.1', '127.0.0.1']
    for ip in test_ips:
        is_pub = is_public_ip(ip)
        print(f"    {ip:15s} → {'Public' if is_pub else 'Private/Reserved'}")
    
    # Local IP ranges
    print("\n  Local/Private IP Ranges (RFC 1918):")
    for start, end in get_local_ip_ranges():
        print(f"    {start} - {end}")


def demo_practical_use_cases():
    """Demonstrate practical use cases."""
    print_section("Practical Use Cases")
    
    # Network planning
    print("\n  Network Planning Example:")
    print("  Need to subnet 10.0.0.0/24 into 4 equal subnets:\n")
    
    subnets = split_subnet('10.0.0.0/24', None, 26)
    for subnet in subnets:
        info = get_subnet_info(subnet)
        print(f"    {subnet}")
        print(f"      Range: {info.first_usable} - {info.last_usable}")
        print(f"      Usable hosts: {info.usable_hosts}")
    
    # Security check
    print("\n  Security Check - Identify private IPs:")
    server_ips = [
        '192.168.1.10',    # Internal server
        '10.0.0.5',        # Internal database
        '203.0.113.50',    # Public web server
        '172.16.0.100',    # Internal API
        '8.8.8.8',         # External DNS
    ]
    
    print("\n  Server IP Classification:")
    for ip in server_ips:
        info = get_ipv4_info(ip)
        status = "INTERNAL" if info.is_private else "PUBLIC"
        print(f"    {ip:15s} → {status:8s} (Class {info.address_class})")
    
    # IP range analysis
    print("\n  IP Range Analysis:")
    print("  Checking if IPs belong to the same /24 subnet:\n")
    
    subnet = '192.168.1.0/24'
    ips_to_check = ['192.168.1.1', '192.168.1.100', '192.168.2.1', '10.0.0.1']
    
    for ip in ips_to_check:
        in_subnet = ip_in_subnet(ip, subnet)
        status = "✓ Same subnet" if in_subnet else "✗ Different subnet"
        print(f"    {ip:15s} in {subnet} → {status}")


def main():
    """Run all demonstrations."""
    print("\n" + "="*60)
    print("  AllToolkit - IP Address Utilities Demo")
    print("="*60)
    
    # IPv4 demos
    demo_ipv4_validation()
    demo_ipv4_conversion()
    demo_ipv4_classification()
    demo_ipv4_info()
    
    # Subnet demos
    demo_subnet_operations()
    demo_subnet_hosts()
    
    # IPv6 demos
    demo_ipv6_validation()
    demo_ipv6_conversion()
    demo_ipv6_classification()
    
    # General utilities
    demo_general_utilities()
    
    # Practical examples
    demo_practical_use_cases()
    
    print("\n" + "="*60)
    print("  Demo Complete!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()