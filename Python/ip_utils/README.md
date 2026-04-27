# Ip Utils


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


## 功能

### 类

- **IPv4Info**: IPv4 address information container
- **SubnetInfo**: Subnet information container
- **IPv6Info**: IPv6 address information container

### 函数

- **validate_ipv4(ip**) - Validate an IPv4 address.
- **ipv4_to_int(ip**) - Convert IPv4 address to integer.
- **int_to_ipv4(num**) - Convert integer to IPv4 address.
- **get_ipv4_class(ip**) - Get the class of an IPv4 address (A, B, C, D, E).
- **is_private_ipv4(ip**) - Check if IPv4 address is private (RFC 1918).
- **is_loopback_ipv4(ip**) - Check if IPv4 address is a loopback address (127.x.x.x).
- **is_link_local_ipv4(ip**) - Check if IPv4 address is link-local (169.254.x.x).
- **is_multicast_ipv4(ip**) - Check if IPv4 address is multicast (224.0.0.0 - 239.255.255.255).
- **is_reserved_ipv4(ip**) - Check if IPv4 address is reserved.
- **get_ipv4_info(ip**) - Get comprehensive information about an IPv4 address.

... 共 33 个函数

## 使用示例

```python
from mod import validate_ipv4

# 使用 validate_ipv4
result = validate_ipv4()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
