# netmask_utils

网络子网计算工具 - 零外部依赖的纯Python实现。

## 功能

- **IP地址验证与解析**
  - IPv4/IPv6地址验证
  - 字符串与整数转换
  - IPv6地址压缩

- **CIDR操作**
  - CIDR前缀与子网掩码互转
  - 网络地址/广播地址计算
  - 主机范围计算

- **子网操作**
  - 子网创建与解析
  - IP地址包含检查
  - 子网划分
  - 子网合并
  - 最小子网查找

## 快速开始

```python
from netmask_utils import (
    IPv4Address, IPv6Address, Subnet,
    is_valid_ipv4, is_valid_ipv6,
    parse_cidr, split_subnet, merge_subnets,
    find_smallest_subnet, list_available_ips,
)

# IP地址验证
is_valid_ipv4("192.168.1.1")  # True
is_valid_ipv6("2001:db8::1")   # True

# 创建子网
subnet = Subnet("192.168.1.0/24")
print(subnet.network)        # 192.168.1.0
print(subnet.broadcast)      # 192.168.1.255
print(subnet.first_host)     # 192.168.1.1
print(subnet.last_host)      # 192.168.1.254
print(subnet.host_count)     # 254

# 检查IP是否在子网内
"192.168.1.100" in subnet    # True
"192.168.2.1" in subnet      # False

# 子网划分
subnets = split_subnet("192.168.1.0/24", 26)
# ['192.168.1.0/26', '192.168.1.64/26', '192.168.1.128/26', '192.168.1.192/26']

# 子网合并
result = merge_subnets(["192.168.1.0/25", "192.168.1.128/25"])
# Subnet('192.168.1.0/24')

# 查找包含所有IP的最小子网
subnet = find_smallest_subnet(["192.168.1.10", "192.168.1.200"])
# Subnet('192.168.1.0/24')

# 列出子网内所有IP
ips = list_available_ips("192.168.1.0/30")
# [IPv4Address('192.168.1.1'), IPv4Address('192.168.1.2')]
```

## API参考

### 类

#### `IPv4Address`
IPv4地址类，支持比较、哈希、整数转换。

```python
ip = IPv4Address("192.168.1.1")
ip = IPv4Address(3232235777)  # 从整数创建

str(ip)      # "192.168.1.1"
int(ip)      # 3232235777
ip.version   # 4
```

#### `IPv6Address`
IPv6地址类，支持地址压缩。

```python
ip = IPv6Address("2001:db8::1")
str(ip)      # "2001:db8::1"
ip.version   # 6
```

#### `Subnet`
子网类，包含完整的子网信息。

```python
subnet = Subnet("192.168.1.0/24")

subnet.network     # 网络地址
subnet.prefix      # 前缀长度
subnet.mask        # 子网掩码
subnet.broadcast   # 广播地址
subnet.first_host  # 第一个可用主机
subnet.last_host   # 最后一个可用主机
subnet.host_count  # 可用主机数量

subnet.contains(ip)    # 检查IP是否在子网内
ip in subnet           # 使用in操作符
```

### 函数

#### IP验证
```python
is_valid_ipv4(address) -> bool
is_valid_ipv6(address) -> bool
is_valid_ip(address) -> Tuple[bool, Optional[int]]  # (是否有效, 版本)
```

#### IP转换
```python
ip_to_int(address) -> int
int_to_ip(value, version=4) -> IPAddress
```

#### CIDR操作
```python
cidr_to_mask(prefix, version=4) -> int      # CIDR转掩码
mask_to_cidr(mask, version=4) -> int         # 掩码转CIDR
parse_cidr(cidr) -> Tuple[IPAddress, int]    # 解析CIDR
```

#### 网络计算
```python
get_network_address(address, prefix) -> IPAddress
get_broadcast_address(address, prefix) -> IPAddress
get_first_host(address, prefix) -> IPAddress
get_last_host(address, prefix) -> IPAddress
get_host_count(prefix, version=4) -> int
get_host_range(address, prefix) -> Tuple[IPAddress, IPAddress]
is_ip_in_subnet(ip, network, prefix) -> bool
```

#### 子网操作
```python
split_subnet(cidr, new_prefix) -> List[Subnet]
merge_subnets(cidrs) -> Optional[Subnet]
find_smallest_subnet(ips) -> Optional[Subnet]
list_available_ips(cidr, include_network=False, include_broadcast=False) -> List[IPAddress]
```

## 运行测试

```bash
cd Python/netmask_utils
python -m pytest test_netmask.py -v
```

## 运行示例

```bash
cd Python/netmask_utils
python examples.py
```

## 特点

- ✅ 零外部依赖
- ✅ 支持IPv4和IPv6
- ✅ 完整的类型注解
- ✅ 详细的文档字符串
- ✅ 全面的单元测试
- ✅ 丰富的使用示例

## 适用场景

- 网络配置工具
- IP地址管理系统
- 子网规划与优化
- 网络安全工具
- 自动化运维脚本

## License

MIT