"""
CIDR Utils - CIDR 子网计算工具
无外部依赖，纯 Python 实现 IPv4/IPv6 CIDR 计算

功能：
- 解析 CIDR 表示法
- 计算子网范围（起始/结束 IP）
- 计算可用主机数
- 检查 IP 是否在子网内
- 转换子网掩码格式
- 子网划分
- 超网合并
"""

from typing import Union, List, Tuple, Optional
import struct
import socket


class CIDRError(Exception):
    """CIDR 相关错误"""
    pass


class IPAddress:
    """IP 地址类，支持 IPv4 和 IPv6"""
    
    def __init__(self, address: Union[str, int, 'IPAddress'], version: Optional[int] = None):
        """
        初始化 IP 地址
        
        Args:
            address: IP 地址字符串、整数或 IPAddress 对象
            version: IP 版本 (4 或 6)，仅当 address 为整数时需要
        """
        if isinstance(address, IPAddress):
            self._value = address._value
            self._version = address._version
        elif isinstance(address, int):
            self._version = version or 4
            self._value = address
        else:
            self._version, self._value = self._parse_string(str(address))
    
    def _parse_string(self, addr: str) -> Tuple[int, int]:
        """解析 IP 地址字符串"""
        # 判断 IPv4 还是 IPv6
        if ':' in addr:
            # IPv6
            try:
                packed = socket.inet_pton(socket.AF_INET6, addr)
                value = int.from_bytes(packed, 'big')
                return 6, value
            except socket.error:
                raise CIDRError(f"无效的 IPv6 地址: {addr}")
        else:
            # IPv4
            try:
                packed = socket.inet_pton(socket.AF_INET, addr)
                value = int.from_bytes(packed, 'big')
                return 4, value
            except socket.error:
                raise CIDRError(f"无效的 IPv4 地址: {addr}")
    
    @property
    def version(self) -> int:
        """IP 版本"""
        return self._version
    
    @property
    def value(self) -> int:
        """整数值表示"""
        return self._value
    
    @property
    def max_value(self) -> int:
        """该版本 IP 的最大值"""
        return (1 << 32) - 1 if self._version == 4 else (1 << 128) - 1
    
    @property
    def bit_length(self) -> int:
        """该版本 IP 的位数"""
        return 32 if self._version == 4 else 128
    
    def __str__(self) -> str:
        """转换为字符串表示"""
        if self._version == 4:
            return socket.inet_ntop(socket.AF_INET, self._value.to_bytes(4, 'big'))
        else:
            return socket.inet_ntop(socket.AF_INET6, self._value.to_bytes(16, 'big'))
    
    def __repr__(self) -> str:
        return f"IPAddress('{self}')"
    
    def __int__(self) -> int:
        return self._value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, IPAddress):
            return self._version == other._version and self._value == other._value
        return False
    
    def __lt__(self, other) -> bool:
        if isinstance(other, IPAddress):
            if self._version != other._version:
                raise CIDRError("无法比较不同版本的 IP 地址")
            return self._value < other._value
        return NotImplemented
    
    def __le__(self, other) -> bool:
        return self == other or self < other
    
    def __gt__(self, other) -> bool:
        if isinstance(other, IPAddress):
            return other < self
        return NotImplemented
    
    def __ge__(self, other) -> bool:
        return self == other or self > other
    
    def __hash__(self) -> int:
        return hash((self._version, self._value))
    
    def __and__(self, other) -> 'IPAddress':
        if isinstance(other, IPAddress):
            if self._version != other._version:
                raise CIDRError("无法对不同版本的 IP 地址进行位运算")
            return IPAddress(self._value & other._value, self._version)
        elif isinstance(other, int):
            return IPAddress(self._value & other, self._version)
        return NotImplemented
    
    def __or__(self, other) -> 'IPAddress':
        if isinstance(other, IPAddress):
            if self._version != other._version:
                raise CIDRError("无法对不同版本的 IP 地址进行位运算")
            return IPAddress(self._value | other._value, self._version)
        elif isinstance(other, int):
            return IPAddress(self._value | other, self._version)
        return NotImplemented
    
    def __invert__(self) -> 'IPAddress':
        """按位取反"""
        return IPAddress(self.max_value ^ self._value, self._version)
    
    def __add__(self, other) -> 'IPAddress':
        if isinstance(other, int):
            return IPAddress(self._value + other, self._version)
        return NotImplemented
    
    def __sub__(self, other) -> Union['IPAddress', int]:
        if isinstance(other, int):
            return IPAddress(self._value - other, self._version)
        elif isinstance(other, IPAddress):
            if self._version != other._version:
                raise CIDRError("无法计算不同版本 IP 地址的差值")
            return self._value - other._value
        return NotImplemented


class CIDR:
    """CIDR 表示法类"""
    
    def __init__(self, cidr: Union[str, Tuple[Union[str, IPAddress, int], int]]):
        """
        初始化 CIDR
        
        Args:
            cidr: CIDR 字符串 (如 '192.168.1.0/24') 或 (IP, 前缀长度) 元组
        """
        if isinstance(cidr, str):
            self._network, self._prefix = self._parse_cidr_string(cidr)
            self._validate_prefix()
        elif isinstance(cidr, tuple):
            ip, prefix = cidr
            self._network = IPAddress(ip)
            self._prefix = prefix
            self._validate_prefix()
        else:
            raise CIDRError(f"无效的 CIDR 参数: {cidr}")
        
        # 计算网络地址
        self._network_address = self._calculate_network_address()
    
    def _parse_cidr_string(self, cidr: str) -> Tuple[IPAddress, int]:
        """解析 CIDR 字符串"""
        if '/' not in cidr:
            raise CIDRError(f"无效的 CIDR 格式: {cidr}")
        
        parts = cidr.split('/')
        if len(parts) != 2:
            raise CIDRError(f"无效的 CIDR 格式: {cidr}")
        
        ip_str, prefix_str = parts
        try:
            prefix = int(prefix_str)
        except ValueError:
            raise CIDRError(f"无效的前缀长度: {prefix_str}")
        
        return IPAddress(ip_str), prefix
    
    def _validate_prefix(self):
        """验证前缀长度"""
        max_prefix = self._network.bit_length
        if not 0 <= self._prefix <= max_prefix:
            raise CIDRError(f"前缀长度必须在 0-{max_prefix} 之间，当前: {self._prefix}")
    
    def _calculate_network_address(self) -> IPAddress:
        """计算网络地址"""
        mask = self.netmask_value
        return self._network & mask
    
    @property
    def version(self) -> int:
        """IP 版本"""
        return self._network.version
    
    @property
    def prefix(self) -> int:
        """前缀长度"""
        return self._prefix
    
    @property
    def bit_length(self) -> int:
        """IP 位数"""
        return self._network.bit_length
    
    @property
    def netmask_value(self) -> int:
        """子网掩码整数值"""
        if self._prefix == 0:
            return 0
        if self._prefix == self.bit_length:
            return (1 << self.bit_length) - 1
        # 创建连续的前缀位，然后左移到正确位置
        return ((1 << self._prefix) - 1) << (self.bit_length - self._prefix)
    
    @property
    def netmask(self) -> IPAddress:
        """子网掩码"""
        return IPAddress(self.netmask_value, self.version)
    
    @property
    def wildcard_value(self) -> int:
        """通配符掩码整数值"""
        host_bits = self.bit_length - self._prefix
        if host_bits == 0:
            return 0
        return (1 << host_bits) - 1
    
    @property
    def wildcard(self) -> IPAddress:
        """通配符掩码（主机掩码）"""
        return IPAddress(self.wildcard_value, self.version)
    
    @property
    def network_address(self) -> IPAddress:
        """网络地址"""
        return self._network_address
    
    @property
    def broadcast_address(self) -> IPAddress:
        """广播地址"""
        return self._network_address | self.wildcard
    
    @property
    def first_host(self) -> Optional[IPAddress]:
        """第一个可用主机地址"""
        if self._prefix >= self.bit_length - 1:
            # /31 或 /32 (IPv4) 或 /127 或 /128 (IPv6) 没有可用主机
            return None
        return self._network_address + 1
    
    @property
    def last_host(self) -> Optional[IPAddress]:
        """最后一个可用主机地址"""
        if self._prefix >= self.bit_length - 1:
            return None
        return self.broadcast_address - 1
    
    @property
    def num_addresses(self) -> int:
        """地址总数"""
        return 1 << (self.bit_length - self._prefix)
    
    @property
    def num_hosts(self) -> int:
        """可用主机数"""
        if self._prefix >= self.bit_length - 1:
            return 0
        return max(0, self.num_addresses - 2)
    
    def __str__(self) -> str:
        return f"{self._network_address}/{self._prefix}"
    
    def __repr__(self) -> str:
        return f"CIDR('{self}')"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, CIDR):
            return self._network_address == other._network_address and self._prefix == other._prefix
        return False
    
    def __hash__(self) -> int:
        return hash((self._network_address, self._prefix))
    
    def __contains__(self, ip: Union[str, IPAddress]) -> bool:
        """检查 IP 是否在子网内"""
        ip_addr = IPAddress(ip) if isinstance(ip, str) else ip
        if ip_addr.version != self.version:
            return False
        return self._network_address <= ip_addr <= self.broadcast_address
    
    def contains(self, ip: Union[str, IPAddress]) -> bool:
        """检查 IP 是否在子网内"""
        return ip in self
    
    def overlaps(self, other: 'CIDR') -> bool:
        """检查两个子网是否有重叠"""
        if self.version != other.version:
            return False
        return (self._network_address <= other.broadcast_address and 
                other._network_address <= self.broadcast_address)
    
    def is_subnet_of(self, other: 'CIDR') -> bool:
        """检查是否是另一个 CIDR 的子网"""
        if self.version != other.version:
            return False
        return self._network_address >= other._network_address and self.broadcast_address <= other.broadcast_address
    
    def is_supernet_of(self, other: 'CIDR') -> bool:
        """检查是否是另一个 CIDR 的超网"""
        return other.is_subnet_of(self)
    
    def subnet(self, new_prefix: int) -> List['CIDR']:
        """
        划分子网
        
        Args:
            new_prefix: 新的前缀长度（必须大于当前前缀）
        
        Returns:
            子网列表
        """
        if new_prefix <= self._prefix:
            raise CIDRError(f"新前缀长度必须大于 {self._prefix}")
        if new_prefix > self.bit_length:
            raise CIDRError(f"新前缀长度不能超过 {self.bit_length}")
        
        num_subnets = 1 << (new_prefix - self._prefix)
        subnets = []
        current = self._network_address
        
        for _ in range(num_subnets):
            subnets.append(CIDR((current, new_prefix)))
            current = current + (1 << (self.bit_length - new_prefix))
        
        return subnets
    
    def hosts(self) -> List[IPAddress]:
        """返回所有可用主机地址"""
        if self.num_hosts == 0:
            return []
        
        hosts = []
        current = self.first_host
        last = self.last_host
        
        while current <= last:
            hosts.append(current)
            current = current + 1
        
        return hosts
    
    def to_range(self) -> Tuple[IPAddress, IPAddress]:
        """返回 IP 范围（网络地址，广播地址）"""
        return (self._network_address, self.broadcast_address)
    
    def info(self) -> dict:
        """返回详细信息字典"""
        return {
            'cidr': str(self),
            'version': self.version,
            'network_address': str(self._network_address),
            'broadcast_address': str(self.broadcast_address),
            'netmask': str(self.netmask),
            'wildcard': str(self.wildcard),
            'first_host': str(self.first_host) if self.first_host else None,
            'last_host': str(self.last_host) if self.last_host else None,
            'num_addresses': self.num_addresses,
            'num_hosts': self.num_hosts,
            'prefix_length': self._prefix
        }


def parse_cidr(cidr: str) -> CIDR:
    """
    解析 CIDR 字符串
    
    Args:
        cidr: CIDR 字符串 (如 '192.168.1.0/24')
    
    Returns:
        CIDR 对象
    """
    return CIDR(cidr)


def ip_to_int(ip: str) -> int:
    """
    将 IP 地址转换为整数
    
    Args:
        ip: IP 地址字符串
    
    Returns:
        整数值
    """
    return int(IPAddress(ip))


def int_to_ip(value: int, version: int = 4) -> str:
    """
    将整数转换为 IP 地址
    
    Args:
        value: 整数值
        version: IP 版本 (4 或 6)
    
    Returns:
        IP 地址字符串
    """
    return str(IPAddress(value, version))


def prefix_to_netmask(prefix: int, version: int = 4) -> str:
    """
    将前缀长度转换为子网掩码
    
    Args:
        prefix: 前缀长度
        version: IP 版本 (4 或 6)
    
    Returns:
        子网掩码字符串
    """
    bit_length = 32 if version == 4 else 128
    if not 0 <= prefix <= bit_length:
        raise CIDRError(f"前缀长度必须在 0-{bit_length} 之间")
    
    if prefix == 0:
        mask_value = 0
    elif prefix == bit_length:
        mask_value = (1 << bit_length) - 1
    else:
        mask_value = ((1 << prefix) - 1) << (bit_length - prefix)
    
    return str(IPAddress(mask_value, version))


def netmask_to_prefix(netmask: str) -> int:
    """
    将子网掩码转换为前缀长度
    
    Args:
        netmask: 子网掩码字符串
    
    Returns:
        前缀长度
    """
    ip = IPAddress(netmask)
    value = ip.value
    
    # 计算连续 1 的位数
    if value == 0:
        return 0
    
    if value == ip.max_value:
        return ip.bit_length
    
    # 使用更安全的方法计算前缀
    count = 0
    bit_len = ip.bit_length
    while count < bit_len and (value & (1 << (bit_len - 1 - count))):
        count += 1
    
    # 验证是否是有效的子网掩码
    if count == 0:
        raise CIDRError(f"无效的子网掩码: {netmask}")
    
    expected = ((1 << count) - 1) << (bit_len - count)
    if value != expected:
        raise CIDRError(f"无效的子网掩码: {netmask}")
    
    return count


def is_valid_cidr(cidr: str) -> bool:
    """
    检查 CIDR 字符串是否有效
    
    Args:
        cidr: CIDR 字符串
    
    Returns:
        是否有效
    """
    try:
        CIDR(cidr)
        return True
    except CIDRError:
        return False


def is_valid_ip(ip: str) -> bool:
    """
    检查 IP 地址是否有效
    
    Args:
        ip: IP 地址字符串
    
    Returns:
        是否有效
    """
    try:
        IPAddress(ip)
        return True
    except CIDRError:
        return False


def ip_in_cidr(ip: str, cidr: str) -> bool:
    """
    检查 IP 是否在 CIDR 范围内
    
    Args:
        ip: IP 地址字符串
        cidr: CIDR 字符串
    
    Returns:
        是否在范围内
    """
    network = CIDR(cidr)
    return ip in network


def get_ip_version(ip: str) -> int:
    """
    获取 IP 版本
    
    Args:
        ip: IP 地址字符串
    
    Returns:
        IP 版本 (4 或 6)
    """
    return IPAddress(ip).version


def subnet_cidr(cidr: str, new_prefix: int) -> List[CIDR]:
    """
    划分 CIDR 子网
    
    Args:
        cidr: 原 CIDR 字符串
        new_prefix: 新的前缀长度
    
    Returns:
        子网 CIDR 列表
    """
    network = CIDR(cidr)
    return network.subnet(new_prefix)


def merge_cidrs(cidrs: List[str]) -> List[CIDR]:
    """
    合并相邻的 CIDR 块（超网合并）
    
    Args:
        cidrs: CIDR 字符串列表
    
    Returns:
        合并后的 CIDR 列表
    """
    if not cidrs:
        return []
    
    # 解析并排序
    networks = [CIDR(c) for c in cidrs]
    
    # 检查版本一致性
    versions = set(n.version for n in networks)
    if len(versions) > 1:
        raise CIDRError("无法合并不同版本的 IP 地址")
    
    # 按网络地址排序
    networks.sort(key=lambda n: (int(n.network_address), n.prefix))
    
    # 合并相邻块
    merged = []
    current = networks[0]
    
    for network in networks[1:]:
        # 检查是否可以合并
        if (current.prefix == network.prefix and 
            int(current.network_address) + current.num_addresses == int(network.network_address)):
            # 尝试合并为更大的块
            if current.prefix > 0:
                # 检查是否可以形成超网
                super_prefix = current.prefix - 1
                super_netmask = ((1 << current.bit_length) - 1) << (current.bit_length - super_prefix)
                if int(current.network_address) & super_netmask == int(current.network_address):
                    # 可以合并
                    current = CIDR((current.network_address, super_prefix))
                else:
                    merged.append(current)
                    current = network
            else:
                merged.append(current)
                current = network
        else:
            merged.append(current)
            current = network
    
    merged.append(current)
    return merged


def calculate_host_range(cidr: str) -> Tuple[str, str]:
    """
    计算主机范围
    
    Args:
        cidr: CIDR 字符串
    
    Returns:
        (起始 IP, 结束 IP) 元组
    """
    network = CIDR(cidr)
    first = network.first_host
    last = network.last_host
    
    if first is None or last is None:
        return (str(network.network_address), str(network.broadcast_address))
    
    return (str(first), str(last))


def get_all_hosts(cidr: str) -> List[str]:
    """
    获取所有主机地址
    
    Args:
        cidr: CIDR 字符串
    
    Returns:
        主机地址字符串列表
    """
    network = CIDR(cidr)
    return [str(ip) for ip in network.hosts()]


def cidr_to_range(cidr: str) -> Tuple[str, str]:
    """
    将 CIDR 转换为 IP 范围
    
    Args:
        cidr: CIDR 字符串
    
    Returns:
        (网络地址, 广播地址) 元组
    """
    network = CIDR(cidr)
    start, end = network.to_range()
    return (str(start), str(end))


def range_to_cidr(start_ip: str, end_ip: str) -> List[CIDR]:
    """
    将 IP 范围转换为 CIDR 列表
    
    Args:
        start_ip: 起始 IP
        end_ip: 结束 IP
    
    Returns:
        CIDR 列表
    """
    start = IPAddress(start_ip)
    end = IPAddress(end_ip)
    
    if start.version != end.version:
        raise CIDRError("起始 IP 和结束 IP 版本必须相同")
    
    if start > end:
        raise CIDRError("起始 IP 不能大于结束 IP")
    
    bit_length = start.bit_length
    cidrs = []
    current = start.value
    end_value = end.value
    
    while current <= end_value:
        # 找到能覆盖的最大块（从最大的块开始尝试）
        # 最大块的条件：块起始地址能被块大小整除，且块不超过 end
        
        # 计算当前地址能对齐的最大块大小（基于地址的低位零位数）
        if current == 0:
            max_align_bits = bit_length
        else:
            # 计算低位有多少个零（决定能对齐的最大块）
            max_align_bits = 0
            temp = current
            while max_align_bits < bit_length and (temp & 1) == 0:
                max_align_bits += 1
                temp >>= 1
        
        # 从最大对齐块开始，逐步减小，直到找到能放入范围的块
        for align_bits in range(max_align_bits, -1, -1):
            block_size = 1 << align_bits
            if current + block_size - 1 <= end_value:
                prefix = bit_length - align_bits
                cidrs.append(CIDR((IPAddress(current, start.version), prefix)))
                current += block_size
                break
    
    return cidrs


def wildcard_to_cidr(network_ip: str, wildcard: str) -> CIDR:
    """
    通过网络地址和通配符掩码创建 CIDR
    
    Args:
        network_ip: 网络 IP 地址
        wildcard: 通配符掩码
    
    Returns:
        CIDR 对象
    """
    network = IPAddress(network_ip)
    wc = IPAddress(wildcard)
    
    if network.version != wc.version:
        raise CIDRError("网络地址和通配符掩码版本必须相同")
    
    # 通配符掩码的反码就是子网掩码
    netmask = ~wc
    
    # 计算前缀长度
    prefix = netmask_to_prefix(str(netmask))
    
    return CIDR((network, prefix))


def get_network_class(ip: str) -> str:
    """
    获取 IPv4 地址的网络类别 (A/B/C/D/E)
    
    Args:
        ip: IPv4 地址字符串
    
    Returns:
        网络类别 (A/B/C/D/E) 或 'Unknown'
    """
    addr = IPAddress(ip)
    if addr.version != 4:
        raise CIDRError("网络类别仅适用于 IPv4")
    
    first_byte = (addr.value >> 24) & 0xFF
    
    if first_byte < 128:
        return 'A'
    elif first_byte < 192:
        return 'B'
    elif first_byte < 224:
        return 'C'
    elif first_byte < 240:
        return 'D'  # 组播
    else:
        return 'E'  # 保留


def is_private_ip(ip: str) -> bool:
    """
    检查是否为私有 IP 地址
    
    Args:
        ip: IP 地址字符串
    
    Returns:
        是否为私有地址
    """
    addr = IPAddress(ip)
    
    if addr.version == 4:
        # IPv4 私有地址范围
        private_cidrs = [
            '10.0.0.0/8',
            '172.16.0.0/12',
            '192.168.0.0/16'
        ]
    else:
        # IPv6 私有地址范围
        private_cidrs = [
            'fc00::/7',   # ULA
            'fe80::/10',  # Link-local
        ]
    
    return any(addr in CIDR(c) for c in private_cidrs)


def is_loopback_ip(ip: str) -> bool:
    """
    检查是否为环回地址
    
    Args:
        ip: IP 地址字符串
    
    Returns:
        是否为环回地址
    """
    addr = IPAddress(ip)
    
    if addr.version == 4:
        return addr in CIDR('127.0.0.0/8')
    else:
        return addr in CIDR('::1/128')


def is_multicast_ip(ip: str) -> bool:
    """
    检查是否为组播地址
    
    Args:
        ip: IP 地址字符串
    
    Returns:
        是否为组播地址
    """
    addr = IPAddress(ip)
    
    if addr.version == 4:
        return addr in CIDR('224.0.0.0/4')
    else:
        return addr in CIDR('ff00::/8')


def is_link_local_ip(ip: str) -> bool:
    """
    检查是否为链路本地地址
    
    Args:
        ip: IP 地址字符串
    
    Returns:
        是否为链路本地地址
    """
    addr = IPAddress(ip)
    
    if addr.version == 4:
        return addr in CIDR('169.254.0.0/16')
    else:
        return addr in CIDR('fe80::/10')


# 导出公共 API
__all__ = [
    'CIDRError',
    'IPAddress',
    'CIDR',
    'parse_cidr',
    'ip_to_int',
    'int_to_ip',
    'prefix_to_netmask',
    'netmask_to_prefix',
    'is_valid_cidr',
    'is_valid_ip',
    'ip_in_cidr',
    'get_ip_version',
    'subnet_cidr',
    'merge_cidrs',
    'calculate_host_range',
    'get_all_hosts',
    'cidr_to_range',
    'range_to_cidr',
    'wildcard_to_cidr',
    'get_network_class',
    'is_private_ip',
    'is_loopback_ip',
    'is_multicast_ip',
    'is_link_local_ip',
]