"""
Netmask Utilities - 网络子网计算工具

提供IP地址和子网的计算与验证功能：
- CIDR解析与计算
- IPv4/IPv6地址验证
- 子网掩码转换
- 网络地址/广播地址计算
- IP范围计算
- 子网包含检查
- 子网划分与合并

零外部依赖，纯Python实现。
"""

from .core import (
    IPAddress,
    IPv4Address,
    IPv6Address,
    Subnet,
    cidr_to_mask,
    mask_to_cidr,
    ip_to_int,
    int_to_ip,
    is_valid_ipv4,
    is_valid_ipv6,
    is_valid_ip,
    parse_cidr,
    get_network_address,
    get_broadcast_address,
    get_first_host,
    get_last_host,
    get_host_count,
    get_host_range,
    is_ip_in_subnet,
    split_subnet,
    merge_subnets,
    find_smallest_subnet,
    list_available_ips,
)

__version__ = "1.0.0"
__all__ = [
    # Classes
    "IPAddress",
    "IPv4Address",
    "IPv6Address",
    "Subnet",
    # Functions
    "cidr_to_mask",
    "mask_to_cidr",
    "ip_to_int",
    "int_to_ip",
    "is_valid_ipv4",
    "is_valid_ipv6",
    "is_valid_ip",
    "parse_cidr",
    "get_network_address",
    "get_broadcast_address",
    "get_first_host",
    "get_last_host",
    "get_host_count",
    "get_host_range",
    "is_ip_in_subnet",
    "split_subnet",
    "merge_subnets",
    "find_smallest_subnet",
    "list_available_ips",
]