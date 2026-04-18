#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - IP Address Utilities Module
=========================================
A comprehensive IP address processing utility module for Python with zero external dependencies.

Features:
    - IPv4 and IPv6 address validation
    - IP address parsing and conversion (string <-> integer)
    - Subnet calculation (CIDR notation support)
    - IP address range checking
    - Private/reserved IP detection
    - IP address comparison and sorting
    - Network utilities (broadcast, first/last usable, etc.)

Author: AllToolkit Contributors
License: MIT
"""

import re
from typing import Union, Tuple, List, Optional
from dataclasses import dataclass


# ============================================================================
# Constants
# ============================================================================

# IPv4 private address ranges (RFC 1918)
IPV4_PRIVATE_RANGES = [
    ('10.0.0.0', '10.255.255.255'),
    ('172.16.0.0', '172.31.255.255'),
    ('192.168.0.0', '192.168.255.255'),
]

# IPv4 loopback range
IPV4_LOOPBACK_RANGE = ('127.0.0.0', '127.255.255.255')

# IPv4 link-local range (RFC 3927)
IPV4_LINK_LOCAL_RANGE = ('169.254.0.0', '169.254.255.255')

# IPv4 multicast range (RFC 5771)
IPV4_MULTICAST_RANGE = ('224.0.0.0', '239.255.255.255')

# IPv4 reserved ranges
IPV4_RESERVED_RANGES = [
    ('0.0.0.0', '0.255.255.255'),      # "This network"
    ('192.0.0.0', '192.0.0.255'),       # IANA IPv4 Special Purpose
    ('192.0.2.0', '192.0.2.255'),       # TEST-NET-1
    ('198.51.100.0', '198.51.100.255'), # TEST-NET-2
    ('203.0.113.0', '203.0.113.255'),   # TEST-NET-3
    ('224.0.0.0', '255.255.255.255'),   # Multicast and future use
]

# IPv6 private address ranges
IPV6_PRIVATE_PREFIX = 'fc00::/7'  # ULA (RFC 4193)
IPV6_LINK_LOCAL_PREFIX = 'fe80::/10'
IPV6_LOOPBACK = '::1'
IPV6_MULTICAST_PREFIX = 'ff00::/8'


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class IPv4Info:
    """IPv4 address information container."""
    address: str
    integer: int
    binary: str
    is_private: bool
    is_loopback: bool
    is_link_local: bool
    is_multicast: bool
    is_reserved: bool
    address_class: str


@dataclass
class SubnetInfo:
    """Subnet information container."""
    network_address: str
    broadcast_address: str
    first_usable: str
    last_usable: str
    subnet_mask: str
    cidr_prefix: int
    total_hosts: int
    usable_hosts: int
    wildcard_mask: str


@dataclass
class IPv6Info:
    """IPv6 address information container."""
    address: str
    compressed: str
    expanded: str
    integer: int
    is_private: bool
    is_loopback: bool
    is_link_local: bool
    is_multicast: bool


# ============================================================================
# IPv4 Utilities
# ============================================================================

# Pre-compiled regex for IPv4 validation - faster than splitting
_IPV4_PATTERN = re.compile(
    r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
)

def validate_ipv4(ip: str) -> bool:
    """
    Validate an IPv4 address.
    
    Args:
        ip: IPv4 address string (e.g., '192.168.1.1')
    
    Returns:
        True if valid IPv4 address, False otherwise
    
    Examples:
        >>> validate_ipv4('192.168.1.1')
        True
        >>> validate_ipv4('256.1.1.1')
        False
        >>> validate_ipv4('')
        False
        >>> validate_ipv4(None)
        False
    
    Note:
        优化版本：
        - 预编译正则提高性能
        - 快速长度检查避免不必要解析
        - 优化八位组验证减少函数调用
        - 边界处理：空值、非字符串、前导零、过长输入
    """
    # 边界处理：空值和非字符串类型
    if ip is None or not isinstance(ip, str):
        return False
    
    # 快速检查：空字符串或过长
    # 最长有效IP: '255.255.255.255' = 15字符，最短: '0.0.0.0' = 7字符
    if len(ip) < 7 or len(ip) > 15:
        return False
    
    # 快速检查：必须包含恰好3个点
    dot_count = ip.count('.')
    if dot_count != 3:
        return False
    
    match = _IPV4_PATTERN.match(ip)
    if not match:
        return False
    
    # 优化：使用直接索引访问而非循环
    # Validate each octet range and leading zeros
    for i in range(1, 5):
        part = match.group(i)
        part_len = len(part)
        
        # 边界处理：防止非ASCII字符干扰
        # 快速检查：仅数字字符
        if not part.isdigit():
            return False
        
        # 快速检查：前导零（单字符零是合法的）
        if part_len > 1 and part[0] == '0':
            return False
        
        # 快速范围检查：使用字符比较避免 int 转换开销
        # 255 是最大值，可以用字符比较快速判断
        if part_len == 3:
            # 三个字符的八位组：必须 <= 255
            # 快速检查：如果第一个字符 > 2，则一定 > 255
            if part[0] > '2':
                return False
            # 如果第一个字符是 '2'，需要检查后两位
            if part[0] == '2':
                if part[1] > '5':
                    return False
                if part[1] == '5' and part[2] > '5':
                    return False
        # 1-2字符的八位组一定在有效范围内（已通过前导零检查）
    
    return True


def ipv4_to_int(ip: str) -> int:
    """
    Convert IPv4 address to integer.
    
    Args:
        ip: Valid IPv4 address string
    
    Returns:
        Integer representation of the IP address
    
    Raises:
        ValueError: If invalid IPv4 address
    
    Examples:
        >>> ipv4_to_int('192.168.1.1')
        3232235777
        >>> ipv4_to_int('0.0.0.0')
        0
    """
    if not validate_ipv4(ip):
        raise ValueError(f"Invalid IPv4 address: {ip}")
    
    parts = [int(x) for x in ip.split('.')]
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]


def int_to_ipv4(num: int) -> str:
    """
    Convert integer to IPv4 address.
    
    Args:
        num: Integer representation of IPv4 address (0 to 2^32-1)
    
    Returns:
        IPv4 address string
    
    Raises:
        ValueError: If integer is out of valid range
    
    Examples:
        >>> int_to_ipv4(3232235777)
        '192.168.1.1'
        >>> int_to_ipv4(0)
        '0.0.0.0'
    """
    if num < 0 or num > 0xFFFFFFFF:
        raise ValueError(f"Integer out of IPv4 range: {num}")
    
    return '.'.join([
        str((num >> 24) & 0xFF),
        str((num >> 16) & 0xFF),
        str((num >> 8) & 0xFF),
        str(num & 0xFF)
    ])


def get_ipv4_class(ip: str) -> str:
    """
    Get the class of an IPv4 address (A, B, C, D, E).
    
    Note: Classful networking is deprecated but still useful for categorization.
    
    Args:
        ip: Valid IPv4 address string
    
    Returns:
        Address class ('A', 'B', 'C', 'D', 'E', or 'Unknown')
    
    Examples:
        >>> get_ipv4_class('10.0.0.1')
        'A'
        >>> get_ipv4_class('172.16.0.1')
        'B'
        >>> get_ipv4_class('192.168.1.1')
        'C'
    """
    if not validate_ipv4(ip):
        return 'Unknown'
    
    first_octet = int(ip.split('.')[0])
    
    # Class A: 0-127 (0 is reserved, 127 is loopback, but still Class A range)
    if 0 <= first_octet <= 127:
        return 'A'
    elif 128 <= first_octet <= 191:
        return 'B'
    elif 192 <= first_octet <= 223:
        return 'C'
    elif 224 <= first_octet <= 239:
        return 'D'  # Multicast
    elif 240 <= first_octet <= 255:
        return 'E'  # Reserved
    else:
        return 'Unknown'


def is_private_ipv4(ip: str) -> bool:
    """
    Check if IPv4 address is private (RFC 1918).
    
    Args:
        ip: IPv4 address string
    
    Returns:
        True if private, False otherwise
    
    Examples:
        >>> is_private_ipv4('192.168.1.1')
        True
        >>> is_private_ipv4('8.8.8.8')
        False
    """
    if not validate_ipv4(ip):
        return False
    
    ip_int = ipv4_to_int(ip)
    
    for start, end in IPV4_PRIVATE_RANGES:
        start_int = ipv4_to_int(start)
        end_int = ipv4_to_int(end)
        if start_int <= ip_int <= end_int:
            return True
    
    return False


def is_loopback_ipv4(ip: str) -> bool:
    """
    Check if IPv4 address is a loopback address (127.x.x.x).
    
    Args:
        ip: IPv4 address string
    
    Returns:
        True if loopback, False otherwise
    
    Examples:
        >>> is_loopback_ipv4('127.0.0.1')
        True
        >>> is_loopback_ipv4('192.168.1.1')
        False
    """
    if not validate_ipv4(ip):
        return False
    
    first_octet = int(ip.split('.')[0])
    return first_octet == 127


def is_link_local_ipv4(ip: str) -> bool:
    """
    Check if IPv4 address is link-local (169.254.x.x).
    
    Args:
        ip: IPv4 address string
    
    Returns:
        True if link-local, False otherwise
    
    Examples:
        >>> is_link_local_ipv4('169.254.1.1')
        True
        >>> is_link_local_ipv4('192.168.1.1')
        False
    """
    if not validate_ipv4(ip):
        return False
    
    parts = [int(x) for x in ip.split('.')]
    return parts[0] == 169 and parts[1] == 254


def is_multicast_ipv4(ip: str) -> bool:
    """
    Check if IPv4 address is multicast (224.0.0.0 - 239.255.255.255).
    
    Args:
        ip: IPv4 address string
    
    Returns:
        True if multicast, False otherwise
    
    Examples:
        >>> is_multicast_ipv4('224.0.0.1')
        True
        >>> is_multicast_ipv4('192.168.1.1')
        False
    """
    if not validate_ipv4(ip):
        return False
    
    first_octet = int(ip.split('.')[0])
    return 224 <= first_octet <= 239


def is_reserved_ipv4(ip: str) -> bool:
    """
    Check if IPv4 address is reserved.
    
    Args:
        ip: IPv4 address string
    
    Returns:
        True if reserved, False otherwise
    
    Examples:
        >>> is_reserved_ipv4('192.0.2.1')  # TEST-NET-1
        True
        >>> is_reserved_ipv4('8.8.8.8')
        False
    """
    if not validate_ipv4(ip):
        return False
    
    ip_int = ipv4_to_int(ip)
    
    for start, end in IPV4_RESERVED_RANGES:
        start_int = ipv4_to_int(start)
        end_int = ipv4_to_int(end)
        if start_int <= ip_int <= end_int:
            return True
    
    return False


def get_ipv4_info(ip: str) -> IPv4Info:
    """
    Get comprehensive information about an IPv4 address.
    
    Args:
        ip: IPv4 address string
    
    Returns:
        IPv4Info object with address details
    
    Raises:
        ValueError: If invalid IPv4 address
    
    Examples:
        >>> info = get_ipv4_info('192.168.1.1')
        >>> info.is_private
        True
        >>> info.address_class
        'C'
    """
    if not validate_ipv4(ip):
        raise ValueError(f"Invalid IPv4 address: {ip}")
    
    ip_int = ipv4_to_int(ip)
    binary = format(ip_int, '032b')
    
    return IPv4Info(
        address=ip,
        integer=ip_int,
        binary='.'.join([binary[i:i+8] for i in range(0, 32, 8)]),
        is_private=is_private_ipv4(ip),
        is_loopback=is_loopback_ipv4(ip),
        is_link_local=is_link_local_ipv4(ip),
        is_multicast=is_multicast_ipv4(ip),
        is_reserved=is_reserved_ipv4(ip),
        address_class=get_ipv4_class(ip)
    )


# ============================================================================
# Subnet Utilities
# ============================================================================

def cidr_to_mask(prefix: int) -> str:
    """
    Convert CIDR prefix to subnet mask.
    
    Args:
        prefix: CIDR prefix (0-32)
    
    Returns:
        Subnet mask string
    
    Raises:
        ValueError: If prefix is out of range
    
    Examples:
        >>> cidr_to_mask(24)
        '255.255.255.0'
        >>> cidr_to_mask(16)
        '255.255.0.0'
    """
    if prefix < 0 or prefix > 32:
        raise ValueError(f"Invalid CIDR prefix: {prefix}")
    
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return int_to_ipv4(mask)


def mask_to_cidr(mask: str) -> int:
    """
    Convert subnet mask to CIDR prefix.
    
    Args:
        mask: Subnet mask string (e.g., '255.255.255.0')
    
    Returns:
        CIDR prefix (0-32)
    
    Raises:
        ValueError: If invalid subnet mask
    
    Examples:
        >>> mask_to_cidr('255.255.255.0')
        24
        >>> mask_to_cidr('255.255.0.0')
        16
    """
    if not validate_ipv4(mask):
        raise ValueError(f"Invalid subnet mask: {mask}")
    
    mask_int = ipv4_to_int(mask)
    
    # Validate that mask is contiguous
    if mask_int == 0:
        return 0
    
    # Count leading 1s
    binary = bin(mask_int)[2:].zfill(32)
    if '01' in binary:  # Non-contiguous mask
        raise ValueError(f"Invalid subnet mask (non-contiguous): {mask}")
    
    return binary.count('1')


def get_subnet_info(network: str, prefix: Optional[int] = None) -> SubnetInfo:
    """
    Get detailed information about a subnet.
    
    Args:
        network: Network address or CIDR notation (e.g., '192.168.1.0/24')
        prefix: Optional CIDR prefix (if not included in network)
    
    Returns:
        SubnetInfo object with subnet details
    
    Raises:
        ValueError: If invalid network or prefix
    
    Examples:
        >>> info = get_subnet_info('192.168.1.0/24')
        >>> info.usable_hosts
        254
        >>> info.broadcast_address
        '192.168.1.255'
    """
    # Parse CIDR notation if provided
    if '/' in network:
        addr, prefix_str = network.split('/')
        prefix = int(prefix_str)
    elif prefix is None:
        raise ValueError("CIDR prefix required (either in network or as separate argument)")
    else:
        addr = network
    
    if not validate_ipv4(addr):
        raise ValueError(f"Invalid network address: {addr}")
    
    if prefix < 0 or prefix > 32:
        raise ValueError(f"Invalid CIDR prefix: {prefix}")
    
    addr_int = ipv4_to_int(addr)
    mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    
    # Calculate network address (ensure it's the actual network address)
    network_int = addr_int & mask_int
    
    # Calculate broadcast address
    broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)
    
    # Calculate first and last usable addresses
    if prefix == 32:
        first_usable_int = network_int
        last_usable_int = network_int
        usable_hosts = 1
        total_hosts = 1
    elif prefix == 31:
        # /31 networks have 2 addresses, both usable (RFC 3021)
        first_usable_int = network_int
        last_usable_int = broadcast_int
        usable_hosts = 2
        total_hosts = 2
    else:
        first_usable_int = network_int + 1
        last_usable_int = broadcast_int - 1
        total_hosts = 2 ** (32 - prefix)
        usable_hosts = total_hosts - 2  # Subtract network and broadcast
    
    # Calculate wildcard mask
    wildcard_int = ~mask_int & 0xFFFFFFFF
    
    return SubnetInfo(
        network_address=int_to_ipv4(network_int),
        broadcast_address=int_to_ipv4(broadcast_int),
        first_usable=int_to_ipv4(first_usable_int),
        last_usable=int_to_ipv4(last_usable_int),
        subnet_mask=cidr_to_mask(prefix),
        cidr_prefix=prefix,
        total_hosts=total_hosts,
        usable_hosts=max(0, usable_hosts),
        wildcard_mask=int_to_ipv4(wildcard_int)
    )


def ip_in_subnet(ip: str, network: str, prefix: Optional[int] = None) -> bool:
    """
    Check if an IP address is within a subnet.
    
    Args:
        ip: IPv4 address to check
        network: Network address or CIDR notation
        prefix: Optional CIDR prefix
    
    Returns:
        True if IP is in subnet, False otherwise
    
    Examples:
        >>> ip_in_subnet('192.168.1.100', '192.168.1.0/24')
        True
        >>> ip_in_subnet('192.168.2.1', '192.168.1.0/24')
        False
    """
    if not validate_ipv4(ip):
        return False
    
    # Parse CIDR notation
    if '/' in network:
        addr, prefix_str = network.split('/')
        prefix = int(prefix_str)
    elif prefix is None:
        raise ValueError("CIDR prefix required")
    else:
        addr = network
    
    if not validate_ipv4(addr):
        return False
    
    ip_int = ipv4_to_int(ip)
    network_int = ipv4_to_int(addr)
    mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    
    return (ip_int & mask_int) == (network_int & mask_int)


def get_all_hosts_in_subnet(network: str, prefix: Optional[int] = None) -> List[str]:
    """
    Get all usable host addresses in a subnet.
    
    Args:
        network: Network address or CIDR notation
        prefix: Optional CIDR prefix
    
    Returns:
        List of all usable IP addresses in the subnet
    
    Examples:
        >>> get_all_hosts_in_subnet('192.168.1.0/30')
        ['192.168.1.1', '192.168.1.2']
    """
    info = get_subnet_info(network, prefix)
    
    # For large subnets, limit the output
    if info.total_hosts > 256:
        raise ValueError(f"Subnet too large ({info.total_hosts} hosts). Use ip_in_subnet() for checking.")
    
    hosts = []
    for i in range(info.usable_hosts):
        hosts.append(int_to_ipv4(ipv4_to_int(info.first_usable) + i))
    
    return hosts


def split_subnet(network: str, prefix: int, new_prefix: int) -> List[str]:
    """
    Split a subnet into smaller subnets.
    
    Args:
        network: Network address or CIDR notation
        prefix: Original CIDR prefix (if not in network string)
        new_prefix: New CIDR prefix for split subnets
    
    Returns:
        List of new subnet CIDR notations
    
    Examples:
        >>> split_subnet('192.168.1.0/24', None, 26)
        ['192.168.1.0/26', '192.168.1.64/26', '192.168.1.128/26', '192.168.1.192/26']
    """
    info = get_subnet_info(network, prefix)
    
    if new_prefix < info.cidr_prefix:
        raise ValueError(f"New prefix ({new_prefix}) must be larger than original ({info.cidr_prefix})")
    
    if new_prefix > 32:
        raise ValueError(f"Invalid new prefix: {new_prefix}")
    
    num_subnets = 2 ** (new_prefix - info.cidr_prefix)
    network_int = ipv4_to_int(info.network_address)
    new_mask_int = (0xFFFFFFFF << (32 - new_prefix)) & 0xFFFFFFFF
    subnet_size = 2 ** (32 - new_prefix)
    
    subnets = []
    for i in range(num_subnets):
        subnet_int = network_int + (i * subnet_size)
        subnets.append(f"{int_to_ipv4(subnet_int)}/{new_prefix}")
    
    return subnets


# ============================================================================
# IPv6 Utilities
# ============================================================================

def validate_ipv6(ip: str) -> bool:
    """
    Validate an IPv6 address.
    
    Args:
        ip: IPv6 address string
    
    Returns:
        True if valid IPv6 address, False otherwise
    
    Examples:
        >>> validate_ipv6('2001:db8::1')
        True
        >>> validate_ipv6('::1')
        True
        >>> validate_ipv6('invalid')
        False
    """
    # Remove any brackets (for IPv6 addresses in URLs)
    ip = ip.strip('[]')
    
    # Handle :: compression
    if '::' in ip:
        # Only one :: allowed
        if ip.count('::') > 1:
            return False
        
        # Check for triple colon (:::) which is invalid
        if ':::' in ip:
            return False
        
        # Split by ::
        parts = ip.split('::')
        left = parts[0].split(':') if parts[0] else []
        right = parts[1].split(':') if parts[1] else []
        
        # Remove empty strings
        left = [p for p in left if p]
        right = [p for p in right if p]
        
        # Total groups should be <= 7 (one :: represents at least 1 empty group)
        if len(left) + len(right) > 7:
            return False
        
        all_parts = left + right
    else:
        all_parts = ip.split(':')
        if len(all_parts) != 8:
            return False
    
    # Validate each part
    for part in all_parts:
        if not part:
            continue
        if len(part) > 4:
            return False
        try:
            int(part, 16)
        except ValueError:
            return False
    
    return True


def expand_ipv6(ip: str) -> str:
    """
    Expand IPv6 address to full form (8 groups of 4 hex digits).
    
    Args:
        ip: IPv6 address string
    
    Returns:
        Fully expanded IPv6 address
    
    Raises:
        ValueError: If invalid IPv6 address
    
    Examples:
        >>> expand_ipv6('2001:db8::1')
        '2001:0db8:0000:0000:0000:0000:0000:0001'
        >>> expand_ipv6('::1')
        '0000:0000:0000:0000:0000:0000:0000:0001'
    """
    if not validate_ipv6(ip):
        raise ValueError(f"Invalid IPv6 address: {ip}")
    
    # Remove brackets
    ip = ip.strip('[]')
    
    # Handle :: compression
    if '::' in ip:
        parts = ip.split('::')
        left = parts[0].split(':') if parts[0] else []
        right = parts[1].split(':') if parts[1] else []
        
        # Remove empty strings from split (due to trailing/leading colons)
        left = [p for p in left if p]
        right = [p for p in right if p]
        
        # Calculate number of zeros to insert to get 8 groups total
        num_zeros = 8 - len(left) - len(right)
        all_parts = left + ['0000'] * num_zeros + right
    else:
        all_parts = ip.split(':')
    
    # Ensure we have exactly 8 parts
    if len(all_parts) != 8:
        raise ValueError(f"Invalid IPv6 address (expected 8 groups): {ip}")
    
    # Pad each part to 4 characters
    return ':'.join([p.zfill(4) for p in all_parts])


def compress_ipv6(ip: str) -> str:
    """
    Compress IPv6 address to shortest form.
    
    Args:
        ip: IPv6 address string
    
    Returns:
        Compressed IPv6 address
    
    Raises:
        ValueError: If invalid IPv6 address
    
    Examples:
        >>> compress_ipv6('2001:0db8:0000:0000:0000:0000:0000:0001')
        '2001:db8::1'
        >>> compress_ipv6('0000:0000:0000:0000:0000:0000:0000:0001')
        '::1'
    """
    if not validate_ipv6(ip):
        raise ValueError(f"Invalid IPv6 address: {ip}")
    
    # Remove brackets
    ip = ip.strip('[]')
    
    # Expand first to get consistent format
    expanded = expand_ipv6(ip)
    parts = expanded.split(':')
    
    # Find longest sequence of zeros
    max_zero_start = -1
    max_zero_len = 0
    current_zero_start = -1
    current_zero_len = 0
    
    for i, part in enumerate(parts):
        if part == '0000':
            if current_zero_start == -1:
                current_zero_start = i
            current_zero_len += 1
        else:
            if current_zero_len > max_zero_len:
                max_zero_start = current_zero_start
                max_zero_len = current_zero_len
            current_zero_start = -1
            current_zero_len = 0
    
    # Check last sequence
    if current_zero_len > max_zero_len:
        max_zero_start = current_zero_start
        max_zero_len = current_zero_len
    
    # Only compress if sequence is >= 2 zeros
    if max_zero_len >= 2:
        # Remove leading zeros from each part
        parts = [p.lstrip('0') or '0' for p in parts]
        
        left = parts[:max_zero_start]
        right = parts[max_zero_start + max_zero_len:]
        
        if not left and not right:
            return '::'
        elif not left:
            return '::' + ':'.join(right)
        elif not right:
            return ':'.join(left) + '::'
        else:
            return ':'.join(left) + '::' + ':'.join(right)
    else:
        # No compression possible, just remove leading zeros
        return ':'.join([p.lstrip('0') or '0' for p in parts])


def ipv6_to_int(ip: str) -> int:
    """
    Convert IPv6 address to integer.
    
    Args:
        ip: IPv6 address string
    
    Returns:
        Integer representation of the IPv6 address
    
    Raises:
        ValueError: If invalid IPv6 address
    
    Examples:
        >>> ipv6_to_int('::1')
        1
    """
    if not validate_ipv6(ip):
        raise ValueError(f"Invalid IPv6 address: {ip}")
    
    expanded = expand_ipv6(ip)
    return int(expanded.replace(':', ''), 16)


def int_to_ipv6(num: int) -> str:
    """
    Convert integer to IPv6 address.
    
    Args:
        num: Integer representation of IPv6 address
    
    Returns:
        Compressed IPv6 address string
    
    Raises:
        ValueError: If integer is out of valid range
    
    Examples:
        >>> int_to_ipv6(1)
        '::1'
    """
    if num < 0 or num > 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:
        raise ValueError(f"Integer out of IPv6 range: {num}")
    
    hex_str = format(num, '032x')
    parts = [hex_str[i:i+4] for i in range(0, 32, 4)]
    expanded = ':'.join(parts)
    
    return compress_ipv6(expanded)


def is_private_ipv6(ip: str) -> bool:
    """
    Check if IPv6 address is private (ULA - Unique Local Address).
    
    Args:
        ip: IPv6 address string
    
    Returns:
        True if private ULA address, False otherwise
    
    Examples:
        >>> is_private_ipv6('fd00::1')
        True
        >>> is_private_ipv6('2001:db8::1')
        False
    """
    if not validate_ipv6(ip):
        return False
    
    expanded = expand_ipv6(ip)
    first_two = expanded[:4].lower()
    
    # ULA range: fc00::/7 (fc00::/8 and fd00::/8)
    return first_two.startswith('fc') or first_two.startswith('fd')


def is_loopback_ipv6(ip: str) -> bool:
    """
    Check if IPv6 address is loopback (::1).
    
    Args:
        ip: IPv6 address string
    
    Returns:
        True if loopback, False otherwise
    
    Examples:
        >>> is_loopback_ipv6('::1')
        True
        >>> is_loopback_ipv6('2001:db8::1')
        False
    """
    if not validate_ipv6(ip):
        return False
    
    return compress_ipv6(ip) == '::1'


def is_link_local_ipv6(ip: str) -> bool:
    """
    Check if IPv6 address is link-local (fe80::/10).
    
    Args:
        ip: IPv6 address string
    
    Returns:
        True if link-local, False otherwise
    
    Examples:
        >>> is_link_local_ipv6('fe80::1')
        True
        >>> is_link_local_ipv6('2001:db8::1')
        False
    """
    if not validate_ipv6(ip):
        return False
    
    expanded = expand_ipv6(ip).lower()
    return expanded.startswith('fe8') or expanded.startswith('fe9') or \
           expanded.startswith('fea') or expanded.startswith('feb')


def is_multicast_ipv6(ip: str) -> bool:
    """
    Check if IPv6 address is multicast (ff00::/8).
    
    Args:
        ip: IPv6 address string
    
    Returns:
        True if multicast, False otherwise
    
    Examples:
        >>> is_multicast_ipv6('ff02::1')
        True
        >>> is_multicast_ipv6('2001:db8::1')
        False
    """
    if not validate_ipv6(ip):
        return False
    
    expanded = expand_ipv6(ip).lower()
    return expanded.startswith('ff')


def get_ipv6_info(ip: str) -> IPv6Info:
    """
    Get comprehensive information about an IPv6 address.
    
    Args:
        ip: IPv6 address string
    
    Returns:
        IPv6Info object with address details
    
    Raises:
        ValueError: If invalid IPv6 address
    
    Examples:
        >>> info = get_ipv6_info('2001:db8::1')
        >>> info.is_private
        False
    """
    if not validate_ipv6(ip):
        raise ValueError(f"Invalid IPv6 address: {ip}")
    
    compressed = compress_ipv6(ip)
    expanded = expand_ipv6(ip)
    
    return IPv6Info(
        address=ip.strip('[]'),
        compressed=compressed,
        expanded=expanded,
        integer=ipv6_to_int(ip),
        is_private=is_private_ipv6(ip),
        is_loopback=is_loopback_ipv6(ip),
        is_link_local=is_link_local_ipv6(ip),
        is_multicast=is_multicast_ipv6(ip)
    )


# ============================================================================
# General IP Utilities
# ============================================================================

def validate_ip(ip: str) -> bool:
    """
    Validate an IP address (IPv4 or IPv6).
    
    Args:
        ip: IP address string
    
    Returns:
        True if valid IP address (v4 or v6), False otherwise
    
    Examples:
        >>> validate_ip('192.168.1.1')
        True
        >>> validate_ip('2001:db8::1')
        True
        >>> validate_ip('invalid')
        False
    """
    return validate_ipv4(ip) or validate_ipv6(ip)


def get_ip_version(ip: str) -> int:
    """
    Get the IP version (4 or 6).
    
    Args:
        ip: IP address string
    
    Returns:
        4 for IPv4, 6 for IPv6, 0 for invalid
    
    Examples:
        >>> get_ip_version('192.168.1.1')
        4
        >>> get_ip_version('2001:db8::1')
        6
        >>> get_ip_version('invalid')
        0
    """
    if validate_ipv4(ip):
        return 4
    elif validate_ipv6(ip):
        return 6
    else:
        return 0


def compare_ips(ip1: str, ip2: str) -> int:
    """
    Compare two IP addresses.
    
    Args:
        ip1: First IP address
        ip2: Second IP address
    
    Returns:
        -1 if ip1 < ip2, 0 if equal, 1 if ip1 > ip2
    
    Raises:
        ValueError: If IPs are different versions or invalid
    
    Examples:
        >>> compare_ips('192.168.1.1', '192.168.1.2')
        -1
        >>> compare_ips('::1', '::2')
        -1
    """
    v1 = get_ip_version(ip1)
    v2 = get_ip_version(ip2)
    
    if v1 == 0 or v2 == 0:
        raise ValueError("Invalid IP address")
    
    if v1 != v2:
        raise ValueError("Cannot compare IPv4 and IPv6 addresses")
    
    if v1 == 4:
        int1 = ipv4_to_int(ip1)
        int2 = ipv4_to_int(ip2)
    else:
        int1 = ipv6_to_int(ip1)
        int2 = ipv6_to_int(ip2)
    
    if int1 < int2:
        return -1
    elif int1 > int2:
        return 1
    else:
        return 0


def sort_ips(ips: List[str]) -> List[str]:
    """
    Sort IP addresses in ascending order.
    
    Args:
        ips: List of IP addresses
    
    Returns:
        Sorted list of IP addresses
    
    Raises:
        ValueError: If any IP is invalid or mixed versions
    
    Examples:
        >>> sort_ips(['192.168.1.2', '192.168.1.1', '192.168.1.3'])
        ['192.168.1.1', '192.168.1.2', '192.168.1.3']
    """
    if not ips:
        return []
    
    # Determine version from first IP
    version = get_ip_version(ips[0])
    if version == 0:
        raise ValueError(f"Invalid IP address: {ips[0]}")
    
    # Create sortable tuples
    def sort_key(ip):
        v = get_ip_version(ip)
        if v != version:
            raise ValueError(f"Mixed IP versions not allowed: {ip} (expected IPv{version})")
        if version == 4:
            return ipv4_to_int(ip)
        else:
            return ipv6_to_int(ip)
    
    return sorted(ips, key=sort_key)


def parse_cidr(cidr: str) -> Tuple[str, int]:
    """
    Parse CIDR notation into address and prefix.
    
    Args:
        cidr: CIDR notation string (e.g., '192.168.1.0/24')
    
    Returns:
        Tuple of (address, prefix)
    
    Raises:
        ValueError: If invalid CIDR notation
    
    Examples:
        >>> parse_cidr('192.168.1.0/24')
        ('192.168.1.0', 24)
        >>> parse_cidr('2001:db8::/32')
        ('2001:db8::', 32)
    """
    if '/' not in cidr:
        raise ValueError(f"Invalid CIDR notation (missing /): {cidr}")
    
    parts = cidr.split('/')
    if len(parts) != 2:
        raise ValueError(f"Invalid CIDR notation: {cidr}")
    
    address, prefix_str = parts
    prefix = int(prefix_str)
    
    version = get_ip_version(address)
    if version == 0:
        raise ValueError(f"Invalid IP address in CIDR: {address}")
    
    max_prefix = 32 if version == 4 else 128
    if prefix < 0 or prefix > max_prefix:
        raise ValueError(f"Invalid prefix for IPv{version}: {prefix}")
    
    return address, prefix


# ============================================================================
# Convenience Functions
# ============================================================================

def get_local_ip_ranges() -> List[Tuple[str, str]]:
    """
    Get list of local/private IP ranges.
    
    Returns:
        List of (start, end) tuples for private IPv4 ranges
    
    Examples:
        >>> ranges = get_local_ip_ranges()
        >>> len(ranges)
        3
    """
    return IPV4_PRIVATE_RANGES.copy()


def is_public_ip(ip: str) -> bool:
    """
    Check if an IP address is public (not private, loopback, link-local, or multicast).
    
    Args:
        ip: IP address string
    
    Returns:
        True if public IP, False otherwise
    
    Examples:
        >>> is_public_ip('8.8.8.8')
        True
        >>> is_public_ip('192.168.1.1')
        False
    """
    if validate_ipv4(ip):
        return not (is_private_ipv4(ip) or is_loopback_ipv4(ip) or 
                    is_link_local_ipv4(ip) or is_multicast_ipv4(ip) or 
                    is_reserved_ipv4(ip))
    elif validate_ipv6(ip):
        return not (is_private_ipv6(ip) or is_loopback_ipv6(ip) or
                    is_link_local_ipv6(ip) or is_multicast_ipv6(ip))
    return False


if __name__ == '__main__':
    # Quick demo
    print("=== IPv4 Examples ===")
    print(f"validate_ipv4('192.168.1.1'): {validate_ipv4('192.168.1.1')}")
    print(f"ipv4_to_int('192.168.1.1'): {ipv4_to_int('192.168.1.1')}")
    print(f"is_private_ipv4('192.168.1.1'): {is_private_ipv4('192.168.1.1')}")
    
    print("\n=== Subnet Examples ===")
    subnet = get_subnet_info('192.168.1.0/24')
    print(f"Subnet: {subnet.network_address}/{subnet.cidr_prefix}")
    print(f"Broadcast: {subnet.broadcast_address}")
    print(f"Usable hosts: {subnet.usable_hosts}")
    
    print("\n=== IPv6 Examples ===")
    print(f"validate_ipv6('2001:db8::1'): {validate_ipv6('2001:db8::1')}")
    print(f"expand_ipv6('::1'): {expand_ipv6('::1')}")
    print(f"compress_ipv6('2001:0db8:0000:0000:0000:0000:0000:0001'): {compress_ipv6('2001:0db8:0000:0000:0000:0000:0000:0001')}")