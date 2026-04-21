"""
Netmask Utilities 核心模块

实现IPv4/IPv6地址和子网的计算功能。
"""

from typing import Optional, List, Tuple, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod


class IPAddress(ABC):
    """IP地址抽象基类"""
    
    _address: int
    _version: int
    
    @property
    def version(self) -> int:
        """IP版本 (4 或 6)"""
        return self._version
    
    @property
    def address(self) -> int:
        """整数形式的IP地址"""
        return self._address
    
    @abstractmethod
    def __str__(self) -> str:
        """字符串表示"""
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        pass
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, IPAddress):
            return False
        return self._address == other._address and self._version == other._version
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, IPAddress):
            return NotImplemented
        if self._version != other._version:
            raise ValueError("Cannot compare IPv4 and IPv6 addresses")
        return self._address < other._address
    
    def __le__(self, other) -> bool:
        return self == other or self < other
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, IPAddress):
            return NotImplemented
        return other < self
    
    def __ge__(self, other) -> bool:
        return self == other or self > other
    
    def __hash__(self) -> int:
        return hash((self._address, self._version))
    
    def __int__(self) -> int:
        return self._address


class IPv4Address(IPAddress):
    """IPv4地址类"""
    
    MAX_VALUE = (1 << 32) - 1
    
    def __init__(self, address: Union[str, int]):
        """
        初始化IPv4地址
        
        Args:
            address: IP地址字符串 (如 "192.168.1.1") 或整数
        """
        self._version = 4
        
        if isinstance(address, int):
            if not 0 <= address <= self.MAX_VALUE:
                raise ValueError(f"Invalid IPv4 integer: {address}")
            self._address = address
        else:
            self._address = self._parse_str(address)
    
    def _parse_str(self, address: str) -> int:
        """解析字符串形式的IP地址"""
        parts = address.strip().split(".")
        if len(parts) != 4:
            raise ValueError(f"Invalid IPv4 address: {address}")
        
        result = 0
        for i, part in enumerate(parts):
            try:
                octet = int(part)
                if not 0 <= octet <= 255:
                    raise ValueError(f"Invalid octet value: {octet}")
                result |= (octet << (24 - i * 8))
            except ValueError:
                raise ValueError(f"Invalid IPv4 address: {address}")
        
        return result
    
    def __str__(self) -> str:
        octets = []
        for i in range(4):
            octets.append(str((self._address >> (24 - i * 8)) & 0xFF))
        return ".".join(octets)
    
    def __repr__(self) -> str:
        return f"IPv4Address('{self}')"


class IPv6Address(IPAddress):
    """IPv6地址类"""
    
    MAX_VALUE = (1 << 128) - 1
    
    def __init__(self, address: Union[str, int]):
        """
        初始化IPv6地址
        
        Args:
            address: IP地址字符串 (如 "2001:db8::1") 或整数
        """
        self._version = 6
        
        if isinstance(address, int):
            if not 0 <= address <= self.MAX_VALUE:
                raise ValueError(f"Invalid IPv6 integer: {address}")
            self._address = address
        else:
            self._address = self._parse_str(address)
    
    def _parse_str(self, address: str) -> int:
        """解析字符串形式的IPv6地址"""
        addr = address.strip()
        
        # 处理 :: 缩写
        if "::" in addr:
            if addr.count("::") > 1:
                raise ValueError(f"Invalid IPv6 address: {address}")
            
            left, right = addr.split("::")
            left_parts = left.split(":") if left else []
            right_parts = right.split(":") if right else []
            
            missing = 8 - len(left_parts) - len(right_parts)
            if missing < 0:
                raise ValueError(f"Invalid IPv6 address: {address}")
            
            parts = left_parts + ["0"] * missing + right_parts
        else:
            parts = addr.split(":")
            if len(parts) != 8:
                raise ValueError(f"Invalid IPv6 address: {address}")
        
        result = 0
        for i, part in enumerate(parts):
            if not part:
                part = "0"
            try:
                hextet = int(part, 16)
                if not 0 <= hextet <= 0xFFFF:
                    raise ValueError(f"Invalid hextet value: {part}")
                result |= (hextet << (112 - i * 16))
            except ValueError:
                raise ValueError(f"Invalid IPv6 address: {address}")
        
        return result
    
    def __str__(self) -> str:
        hextets = []
        for i in range(8):
            hextets.append(format((self._address >> (112 - i * 16)) & 0xFFFF, 'x'))
        
        # 找到最长的连续零序列进行压缩
        best_start = -1
        best_len = 0
        current_start = -1
        current_len = 0
        
        for i, h in enumerate(hextets):
            if h == "0":
                if current_start == -1:
                    current_start = i
                current_len += 1
            else:
                if current_len > best_len:
                    best_start = current_start
                    best_len = current_len
                current_start = -1
                current_len = 0
        
        if current_len > best_len:
            best_start = current_start
            best_len = current_len
        
        if best_len >= 2:
            left = ":".join(hextets[:best_start])
            right = ":".join(hextets[best_start + best_len:])
            
            if not left and not right:
                return "::"
            elif not left:
                return f"::{right}"
            elif not right:
                return f"{left}::"
            else:
                return f"{left}::{right}"
        
        return ":".join(hextets)
    
    def __repr__(self) -> str:
        return f"IPv6Address('{self}')"


@dataclass
class Subnet:
    """
    子网类
    
    Attributes:
        network: 网络地址
        prefix: 前缀长度 (CIDR表示法中的数字)
    """
    network: IPAddress
    prefix: int
    
    def __init__(self, cidr: str):
        """
        从CIDR表示法初始化子网
        
        Args:
            cidr: CIDR表示法 (如 "192.168.1.0/24" 或 "2001:db8::/32")
        """
        network, prefix = parse_cidr(cidr)
        self.network = network
        self.prefix = prefix
        
        # 验证前缀长度
        max_prefix = 32 if self.network.version == 4 else 128
        if not 0 <= prefix <= max_prefix:
            raise ValueError(f"Invalid prefix length: {prefix}")
    
    @property
    def version(self) -> int:
        """IP版本"""
        return self.network.version
    
    @property
    def max_prefix(self) -> int:
        """最大前缀长度"""
        return 32 if self.version == 4 else 128
    
    @property
    def mask(self) -> IPAddress:
        """子网掩码"""
        return int_to_ip(cidr_to_mask(self.prefix, self.version), self.version)
    
    @property
    def host_mask(self) -> IPAddress:
        """主机掩码 (反掩码)"""
        mask_int = cidr_to_mask(self.prefix, self.version)
        max_val = IPv4Address.MAX_VALUE if self.version == 4 else IPv6Address.MAX_VALUE
        return int_to_ip(max_val ^ mask_int, self.version)
    
    @property
    def broadcast(self) -> IPAddress:
        """广播地址"""
        if self.version == 4:
            if self.prefix == 32:
                return self.network
            if self.prefix == 31:
                # /31 子网是点对点链路，没有广播地址
                return int_to_ip(int(self.network) + 1, 4)
            return get_broadcast_address(str(self.network), self.prefix)
        else:
            if self.prefix == 128:
                return self.network
            return get_broadcast_address(str(self.network), self.prefix)
    
    @property
    def first_host(self) -> Optional[IPAddress]:
        """第一个可用主机地址"""
        if self.version == 4 and self.prefix >= 31:
            return None
        if self.version == 6 and self.prefix == 128:
            return None
        return get_first_host(str(self.network), self.prefix)
    
    @property
    def last_host(self) -> Optional[IPAddress]:
        """最后一个可用主机地址"""
        if self.version == 4 and self.prefix >= 31:
            return None
        if self.version == 6 and self.prefix == 128:
            return None
        return get_last_host(str(self.network), self.prefix)
    
    @property
    def host_count(self) -> int:
        """可用主机数量"""
        return get_host_count(self.prefix, self.version)
    
    def contains(self, ip: Union[str, IPAddress]) -> bool:
        """
        检查IP地址是否在子网内
        
        Args:
            ip: IP地址 (字符串或IPAddress对象)
        
        Returns:
            是否在子网内
        """
        if isinstance(ip, str):
            ip = IPv4Address(ip) if self.version == 4 else IPv6Address(ip)
        
        if ip.version != self.version:
            return False
        
        return is_ip_in_subnet(str(ip), str(self.network), self.prefix)
    
    def __contains__(self, ip: Union[str, IPAddress]) -> bool:
        return self.contains(ip)
    
    def __str__(self) -> str:
        return f"{self.network}/{self.prefix}"
    
    def __repr__(self) -> str:
        return f"Subnet('{self}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Subnet):
            return False
        return self.network == other.network and self.prefix == other.prefix
    
    def __hash__(self) -> int:
        return hash((self.network, self.prefix))


# ============ 工具函数 ============

def is_valid_ipv4(address: str) -> bool:
    """
    验证IPv4地址是否有效
    
    Args:
        address: IP地址字符串
    
    Returns:
        是否为有效IPv4地址
    
    Example:
        >>> is_valid_ipv4("192.168.1.1")
        True
        >>> is_valid_ipv4("256.1.1.1")
        False
    """
    try:
        IPv4Address(address)
        return True
    except ValueError:
        return False


def is_valid_ipv6(address: str) -> bool:
    """
    验证IPv6地址是否有效
    
    Args:
        address: IP地址字符串
    
    Returns:
        是否为有效IPv6地址
    
    Example:
        >>> is_valid_ipv6("2001:db8::1")
        True
        >>> is_valid_ipv6("gggg::1")
        False
    """
    try:
        IPv6Address(address)
        return True
    except ValueError:
        return False


def is_valid_ip(address: str) -> Tuple[bool, Optional[int]]:
    """
    验证IP地址是否有效
    
    Args:
        address: IP地址字符串
    
    Returns:
        (是否有效, IP版本) 元组
    
    Example:
        >>> is_valid_ip("192.168.1.1")
        (True, 4)
        >>> is_valid_ip("2001:db8::1")
        (True, 6)
    """
    if is_valid_ipv4(address):
        return True, 4
    if is_valid_ipv6(address):
        return True, 6
    return False, None


def ip_to_int(address: str) -> int:
    """
    将IP地址转换为整数
    
    Args:
        address: IP地址字符串
    
    Returns:
        整数形式的IP地址
    
    Example:
        >>> ip_to_int("192.168.1.1")
        3232235777
    """
    valid, version = is_valid_ip(address)
    if not valid:
        raise ValueError(f"Invalid IP address: {address}")
    
    if version == 4:
        return int(IPv4Address(address))
    else:
        return int(IPv6Address(address))


def int_to_ip(value: int, version: int = 4) -> IPAddress:
    """
    将整数转换为IP地址
    
    Args:
        value: 整数值
        version: IP版本 (4 或 6)
    
    Returns:
        IPAddress对象
    
    Example:
        >>> str(int_to_ip(3232235777, 4))
        '192.168.1.1'
    """
    if version == 4:
        return IPv4Address(value)
    else:
        return IPv6Address(value)


def cidr_to_mask(prefix: int, version: int = 4) -> int:
    """
    将CIDR前缀长度转换为子网掩码
    
    Args:
        prefix: 前缀长度 (0-32 for IPv4, 0-128 for IPv6)
        version: IP版本
    
    Returns:
        整数形式的子网掩码
    
    Example:
        >>> hex(cidr_to_mask(24, 4))
        '0xffffff00'
        >>> cidr_to_mask(24, 4)
        4294967040
    """
    max_prefix = 32 if version == 4 else 128
    max_value = IPv4Address.MAX_VALUE if version == 4 else IPv6Address.MAX_VALUE
    
    if not 0 <= prefix <= max_prefix:
        raise ValueError(f"Invalid prefix length: {prefix}")
    
    if prefix == 0:
        return 0
    
    # 计算掩码：prefix个1后面跟着(max_prefix - prefix)个0
    return max_value ^ ((1 << (max_prefix - prefix)) - 1)


def mask_to_cidr(mask: Union[str, int], version: int = 4) -> int:
    """
    将子网掩码转换为CIDR前缀长度
    
    Args:
        mask: 子网掩码 (字符串或整数)
        version: IP版本
    
    Returns:
        前缀长度
    
    Example:
        >>> mask_to_cidr("255.255.255.0", 4)
        24
        >>> mask_to_cidr(0xFFFFFF00, 4)
        24
    """
    if isinstance(mask, str):
        mask_int = ip_to_int(mask)
    else:
        mask_int = mask
    
    max_prefix = 32 if version == 4 else 128
    
    # 验证是否为有效掩码
    # 有效掩码必须是连续的1后面跟着连续的0
    inverted = (~mask_int) & (IPv4Address.MAX_VALUE if version == 4 else IPv6Address.MAX_VALUE)
    
    # 检查inverted是否为(2^n - 1)的形式
    if inverted != 0 and (inverted + 1) & inverted != 0:
        raise ValueError(f"Invalid subnet mask: {mask}")
    
    # 计算前缀长度
    return max_prefix - bin(inverted).count('1')


def parse_cidr(cidr: str) -> Tuple[IPAddress, int]:
    """
    解析CIDR表示法
    
    Args:
        cidr: CIDR字符串 (如 "192.168.1.0/24")
    
    Returns:
        (网络地址, 前缀长度) 元组
    
    Example:
        >>> net, prefix = parse_cidr("192.168.1.0/24")
        >>> str(net), prefix
        ('192.168.1.0', 24)
    """
    if "/" not in cidr:
        raise ValueError(f"Invalid CIDR notation: {cidr}")
    
    address_part, prefix_part = cidr.rsplit("/", 1)
    
    valid, version = is_valid_ip(address_part)
    if not valid:
        raise ValueError(f"Invalid IP address in CIDR: {address_part}")
    
    try:
        prefix = int(prefix_part)
    except ValueError:
        raise ValueError(f"Invalid prefix length: {prefix_part}")
    
    max_prefix = 32 if version == 4 else 128
    if not 0 <= prefix <= max_prefix:
        raise ValueError(f"Invalid prefix length: {prefix}")
    
    ip_class = IPv4Address if version == 4 else IPv6Address
    return ip_class(address_part), prefix


def get_network_address(address: str, prefix: int) -> IPAddress:
    """
    计算网络地址
    
    Args:
        address: IP地址
        prefix: 前缀长度
    
    Returns:
        网络地址
    
    Example:
        >>> str(get_network_address("192.168.1.100", 24))
        '192.168.1.0'
    """
    valid, version = is_valid_ip(address)
    if not valid:
        raise ValueError(f"Invalid IP address: {address}")
    
    max_prefix = 32 if version == 4 else 128
    if not 0 <= prefix <= max_prefix:
        raise ValueError(f"Invalid prefix length: {prefix}")
    
    ip_int = ip_to_int(address)
    mask_int = cidr_to_mask(prefix, version)
    
    return int_to_ip(ip_int & mask_int, version)


def get_broadcast_address(address: str, prefix: int) -> IPAddress:
    """
    计算广播地址 (仅适用于IPv4)
    
    Args:
        address: 网络地址或网络内的任意IP
        prefix: 前缀长度
    
    Returns:
        广播地址
    
    Example:
        >>> str(get_broadcast_address("192.168.1.0", 24))
        '192.168.1.255'
    """
    valid, version = is_valid_ip(address)
    if not valid:
        raise ValueError(f"Invalid IP address: {address}")
    
    max_prefix = 32 if version == 4 else 128
    if not 0 <= prefix <= max_prefix:
        raise ValueError(f"Invalid prefix length: {prefix}")
    
    ip_int = ip_to_int(address)
    mask_int = cidr_to_mask(prefix, version)
    max_value = IPv4Address.MAX_VALUE if version == 4 else IPv6Address.MAX_VALUE
    
    return int_to_ip((ip_int & mask_int) | (max_value ^ mask_int), version)


def get_first_host(address: str, prefix: int) -> IPAddress:
    """
    获取第一个可用主机地址
    
    Args:
        address: 网络地址
        prefix: 前缀长度
    
    Returns:
        第一个可用主机地址
    
    Example:
        >>> str(get_first_host("192.168.1.0", 24))
        '192.168.1.1'
    """
    network = get_network_address(address, prefix)
    return int_to_ip(int(network) + 1, network.version)


def get_last_host(address: str, prefix: int) -> IPAddress:
    """
    获取最后一个可用主机地址
    
    Args:
        address: 网络地址
        prefix: 前缀长度
    
    Returns:
        最后一个可用主机地址
    
    Example:
        >>> str(get_last_host("192.168.1.0", 24))
        '192.168.1.254'
    """
    broadcast = get_broadcast_address(address, prefix)
    return int_to_ip(int(broadcast) - 1, broadcast.version)


def get_host_count(prefix: int, version: int = 4) -> int:
    """
    计算可用主机数量
    
    Args:
        prefix: 前缀长度
        version: IP版本
    
    Returns:
        可用主机数量 (IPv4扣除网络地址和广播地址)
    
    Example:
        >>> get_host_count(24, 4)
        254
        >>> get_host_count(30, 4)
        2
    """
    max_prefix = 32 if version == 4 else 128
    if not 0 <= prefix <= max_prefix:
        raise ValueError(f"Invalid prefix length: {prefix}")
    
    host_bits = max_prefix - prefix
    total = 2 ** host_bits
    
    if version == 4:
        if prefix == 32:
            return 1  # 单主机
        elif prefix == 31:
            return 2  # 点对点链路
        else:
            return max(0, total - 2)  # 扣除网络地址和广播地址
    else:
        # IPv6没有广播地址的概念
        if prefix == 128:
            return 1
        return total - 1  # 扣除子网路由器任播地址习惯


def get_host_range(address: str, prefix: int) -> Optional[Tuple[IPAddress, IPAddress]]:
    """
    获取主机地址范围
    
    Args:
        address: 网络地址
        prefix: 前缀长度
    
    Returns:
        (第一个主机, 最后一个主机) 元组，或None（对于/32和/128）
    
    Example:
        >>> first, last = get_host_range("192.168.1.0", 24)
        >>> str(first), str(last)
        ('192.168.1.1', '192.168.1.254')
    """
    valid, version = is_valid_ip(address)
    if not valid:
        raise ValueError(f"Invalid IP address: {address}")
    
    max_prefix = 32 if version == 4 else 128
    
    if prefix == max_prefix:
        return None
    
    if version == 4 and prefix == 31:
        # /31 点对点链路
        network = get_network_address(address, prefix)
        return (network, int_to_ip(int(network) + 1, 4))
    
    return (get_first_host(address, prefix), get_last_host(address, prefix))


def is_ip_in_subnet(ip: str, network: str, prefix: int) -> bool:
    """
    检查IP地址是否在指定子网内
    
    Args:
        ip: 要检查的IP地址
        network: 网络地址
        prefix: 前缀长度
    
    Returns:
        是否在子网内
    
    Example:
        >>> is_ip_in_subnet("192.168.1.100", "192.168.1.0", 24)
        True
        >>> is_ip_in_subnet("192.168.2.1", "192.168.1.0", 24)
        False
    """
    valid, ip_version = is_valid_ip(ip)
    if not valid:
        raise ValueError(f"Invalid IP address: {ip}")
    
    valid, net_version = is_valid_ip(network)
    if not valid:
        raise ValueError(f"Invalid network address: {network}")
    
    if ip_version != net_version:
        return False
    
    ip_int = ip_to_int(ip)
    net_int = ip_to_int(network)
    mask_int = cidr_to_mask(prefix, ip_version)
    
    return (ip_int & mask_int) == (net_int & mask_int)


def split_subnet(cidr: str, new_prefix: int) -> List[Subnet]:
    """
    将子网划分为更小的子网
    
    Args:
        cidr: 原子网的CIDR表示
        new_prefix: 新的前缀长度 (必须大于原前缀)
    
    Returns:
        子网列表
    
    Example:
        >>> subnets = split_subnet("192.168.1.0/24", 26)
        >>> [str(s) for s in subnets]
        ['192.168.1.0/26', '192.168.1.64/26', '192.168.1.128/26', '192.168.1.192/26']
    """
    subnet = Subnet(cidr)
    
    if new_prefix <= subnet.prefix:
        raise ValueError(f"New prefix must be larger than {subnet.prefix}")
    
    max_prefix = subnet.max_prefix
    if new_prefix > max_prefix:
        raise ValueError(f"New prefix cannot exceed {max_prefix}")
    
    # 计算需要划分的子网数量
    num_subnets = 2 ** (new_prefix - subnet.prefix)
    
    # 计算每个新子网的大小
    subnet_size = 2 ** (max_prefix - new_prefix)
    
    base = int(subnet.network)
    result = []
    
    ip_class = IPv4Address if subnet.version == 4 else IPv6Address
    
    for i in range(num_subnets):
        new_network = base + (i * subnet_size)
        result.append(Subnet(f"{ip_class(new_network)}/{new_prefix}"))
    
    return result


def merge_subnets(cidrs: List[str]) -> Optional[Subnet]:
    """
    尝试合并多个子网
    
    Args:
        cidrs: CIDR字符串列表
    
    Returns:
        合并后的子网，如果无法合并则返回None
    
    Example:
        >>> merged = merge_subnets(["192.168.1.0/25", "192.168.1.128/25"])
        >>> str(merged)
        '192.168.1.0/24'
    """
    if not cidrs:
        return None
    
    subnets = [Subnet(cidr) for cidr in cidrs]
    
    # 检查所有子网是否同一版本
    versions = set(s.version for s in subnets)
    if len(versions) != 1:
        return None
    
    version = versions.pop()
    max_prefix = 32 if version == 4 else 128
    
    # 检查所有子网是否相同前缀
    prefixes = set(s.prefix for s in subnets)
    if len(prefixes) != 1:
        return None
    
    prefix = prefixes.pop()
    
    # 子网数量必须是2的幂
    if len(subnets) & (len(subnets) - 1) != 0:
        return None
    
    # 计算新前缀
    new_prefix = prefix - (len(subnets) - 1).bit_length()
    if new_prefix < 0:
        return None
    
    # 获取最小网络地址
    min_addr = min(int(s.network) for s in subnets)
    
    # 检查网络地址是否对齐
    subnet_size = 2 ** (max_prefix - new_prefix)
    if min_addr % subnet_size != 0:
        return None
    
    # 检查所有子网是否在预期范围内
    ip_class = IPv4Address if version == 4 else IPv6Address
    expected_networks = set()
    for i in range(len(subnets)):
        expected_networks.add(min_addr + i * (subnet_size // len(subnets)))
    
    actual_networks = set(int(s.network) for s in subnets)
    if expected_networks != actual_networks:
        return None
    
    return Subnet(f"{ip_class(min_addr)}/{new_prefix}")


def find_smallest_subnet(ips: List[str]) -> Optional[Subnet]:
    """
    找到能包含所有IP地址的最小子网
    
    Args:
        ips: IP地址列表
    
    Returns:
        最小子网，如果无法计算则返回None
    
    Example:
        >>> subnet = find_smallest_subnet(["192.168.1.1", "192.168.1.100"])
        >>> str(subnet)
        '192.168.1.0/24'
    """
    if not ips:
        return None
    
    # 验证所有IP
    parsed = []
    version = None
    for ip in ips:
        valid, v = is_valid_ip(ip)
        if not valid:
            return None
        if version is None:
            version = v
        elif version != v:
            return None
        parsed.append(ip_to_int(ip))
    
    if version is None:
        return None
    
    max_prefix = 32 if version == 4 else 128
    min_ip = min(parsed)
    max_ip = max(parsed)
    
    # 找到能覆盖范围的最小前缀
    for prefix in range(max_prefix, -1, -1):
        mask = cidr_to_mask(prefix, version)
        if (min_ip & mask) == (max_ip & mask):
            ip_class = IPv4Address if version == 4 else IPv6Address
            return Subnet(f"{ip_class(min_ip & mask)}/{prefix}")
    
    # 理论上不会到达这里
    return None


def list_available_ips(cidr: str, include_network: bool = False, 
                       include_broadcast: bool = False) -> List[IPAddress]:
    """
    列出子网内所有IP地址
    
    注意：对于大子网（如/8）会消耗大量内存，慎用
    
    Args:
        cidr: CIDR表示法
        include_network: 是否包含网络地址
        include_broadcast: 是否包含广播地址
    
    Returns:
        IP地址列表
    
    Example:
        >>> ips = list_available_ips("192.168.1.0/30")
        >>> [str(ip) for ip in ips]
        ['192.168.1.1', '192.168.1.2']
    """
    subnet = Subnet(cidr)
    
    # 安全限制：防止生成过多IP
    if subnet.version == 4 and subnet.prefix < 20:
        raise ValueError(f"Subnet too large to list all IPs (/{subnet.prefix})")
    if subnet.version == 6 and subnet.prefix < 120:
        raise ValueError(f"IPv6 subnet too large to list all IPs (/{subnet.prefix})")
    
    network = int(subnet.network)
    broadcast = int(subnet.broadcast)
    
    start = network + (0 if include_network else 1)
    end = broadcast + (1 if include_broadcast else 0)
    
    if subnet.version == 4:
        if subnet.prefix == 31:
            # /31 点对点链路
            return [IPv4Address(network), IPv4Address(network + 1)]
        if subnet.prefix == 32:
            return [IPv4Address(network)]
    
    ip_class = IPv4Address if subnet.version == 4 else IPv6Address
    return [ip_class(i) for i in range(start, end)]