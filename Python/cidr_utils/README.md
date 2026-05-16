# CIDR Utils - CIDR 子网计算工具

IPv4/IPv6 CIDR 表示法解析与计算工具，零外部依赖。

## 功能特性

- **CIDR 解析**: 解析 CIDR 表示法（如 `192.168.1.0/24`）
- **子网计算**: 网络地址、广播地址、可用主机数
- **IP 检查**: 判断 IP 是否在子网内
- **掩码转换**: 前缀长度与子网掩码互转
- **子网划分**: 将大网段划分为多个子网
- **超网合并**: 合并相邻 CIDR 块
- **特殊地址**: 私有地址、环回地址、组播地址识别

## 快速开始

```python
from cidr_utils.mod import (
    parse_cidr,
    ip_in_cidr,
    prefix_to_netmask,
    netmask_to_prefix,
    CIDR,
)

# 解析 CIDR
network = parse_cidr("192.168.1.0/24")

# 子网信息
print(f"网络地址: {network.network_address}")
print(f"广播地址: {network.broadcast_address}")
print(f"子网掩码: {network.netmask}")
print(f"可用主机数: {network.num_hosts}")

# 检查 IP 是否在子网内
if ip_in_cidr("192.168.1.100", "192.168.1.0/24"):
    print("IP 在子网内")

# 前缀转掩码
mask = prefix_to_netmask(24)  # "255.255.255.0"

# 掩码转前缀
prefix = netmask_to_prefix("255.255.255.0")  # 24
```

## 核心类

### CIDR - CIDR 表示法

```python
from cidr_utils.mod import CIDR

network = CIDR("192.168.1.0/24")

# 基本信息
print(f"版本: {network.version}")  # 4
print(f"前缀: {network.prefix}")  # 24
print(f"地址总数: {network.num_addresses}")  # 256
print(f"可用主机: {network.num_hosts}")  # 254

# 地址范围
print(f"网络地址: {network.network_address}")  # 192.168.1.0
print(f"广播地址: {network.broadcast_address}")  # 192.168.1.255
print(f"首主机: {network.first_host}")  # 192.168.1.1
print(f"末主机: {network.last_host}")  # 192.168.1.254

# 子网掩码
print(f"子网掩码: {network.netmask}")  # 255.255.255.0
print(f"通配符掩码: {network.wildcard}")  # 0.0.0.255

# 检查 IP
if "192.168.1.50" in network:
    print("IP 在子网内")

# 获取详细信息
info = network.info()
```

### IPAddress - IP 地址

```python
from cidr_utils.mod import IPAddress

ip = IPAddress("192.168.1.1")

print(f"版本: {ip.version}")  # 4
print(f"整数值: {int(ip)}")  # 3232235777

# 比较
ip1 = IPAddress("192.168.1.1")
ip2 = IPAddress("192.168.1.2")
print(ip1 < ip2)  # True

# 位运算
mask = IPAddress("255.255.255.0")
network = ip1 & mask  # 192.168.1.0
```

## 子网划分

```python
# 将 /24 划分为 4 个 /26
subnets = network.subnet(26)
for subnet in subnets:
    print(f"{subnet}")

# 输出:
# 192.168.1.0/26
# 192.168.1.64/26
# 192.168.1.128/26
# 192.168.1.192/26
```

## IP 范围转 CIDR

```python
from cidr_utils.mod import range_to_cidr

# 将 IP 范围转换为最优 CIDR 列表
cidrs = range_to_cidr("192.168.1.0", "192.168.1.255")
for cidr in cidrs:
    print(cidr)  # 192.168.1.0/24

# 更复杂的范围
cidrs = range_to_cidr("192.168.1.64", "192.168.1.127")
# 192.168.1.64/26
```

## 特殊地址检查

```python
from cidr_utils.mod import (
    is_private_ip,
    is_loopback_ip,
    is_multicast_ip,
    is_link_local_ip,
    get_network_class,
)

# 私有地址
is_private_ip("192.168.1.1")  # True
is_private_ip("10.0.0.1")  # True
is_private_ip("8.8.8.8")  # False

# 环回地址
is_loopback_ip("127.0.0.1")  # True

# 组播地址
is_multicast_ip("224.0.0.1")  # True

# 链路本地
is_link_local_ip("169.254.1.1")  # True

# 网络类别
get_network_class("10.0.0.1")  # 'A'
get_network_class("172.16.0.1")  # 'B'
get_network_class("192.168.1.1")  # 'C'
```

## IPv6 支持

```python
# IPv6 CIDR
network = CIDR("2001:db8::/32")

print(f"网络地址: {network.network_address}")
print(f"地址总数: {network.num_addresses}")  # 2^96

# IPv6 地址检查
ip_in_cidr("2001:db8::1", "2001:db8::/32")  # True
```

## 常用函数

| 函数 | 说明 |
|------|------|
| `parse_cidr(cidr)` | 解析 CIDR 字符串 |
| `ip_in_cidr(ip, cidr)` | 检查 IP 是否在 CIDR 内 |
| `prefix_to_netmask(prefix)` | 前缀转子网掩码 |
| `netmask_to_prefix(mask)` | 子网掩码转前缀 |
| `cidr_to_range(cidr)` | CIDR 转 IP 范围 |
| `range_to_cidr(start, end)` | IP 范围转 CIDR 列表 |
| `subnet_cidr(cidr, new_prefix)` | 划分子网 |
| `merge_cidrs(cidrs)` | 合并相邻 CIDR |

## 测试覆盖

- CIDR 解析（IPv4/IPv6）
- 子网计算
- IP 地址位运算
- 子网划分
- IP 范围转换
- 特殊地址识别
- 边界值处理

## 许可证

MIT License