# MAC Address Utilities

MAC 地址处理工具模块，零依赖实现。

## 功能

- **验证**：验证 MAC 地址格式有效性
- **格式转换**：冒号、连字符、点号(Cisco)、无分隔符格式互转
- **厂商查询**：基于 OUI 数据库查询厂商名称
- **地址类型判断**：多播/单播/广播/本地管理/全局唯一
- **随机生成**：随机 MAC、指定厂商、本地管理、多播地址
- **算术运算**：递增、递减、范围生成
- **比较**：MAC 地址比较和相等判断
- **整数转换**：MAC 与 48 位整数互转
- **IP多播**：IPv4/IPv6 多播地址转 MAC 多播地址
- **隐私遮蔽**：部分遮蔽 MAC 地址用于显示

## 使用方法

```python
from mac_address_utils.mod import (
    validate, normalize, lookup_vendor, 
    generate_random, is_multicast, mask_mac
)

# 验证
valid = validate("00:11:22:33:44:55")  # True

# 标准化
mac = normalize("00-11-22-33-44-55")  # "00:11:22:33:44:55"

# 厂商查询
vendor = lookup_vendor("00:03:93:AB:CD:EF")  # "Apple"

# 类型判断
is_mc = is_multicast("01:00:5E:00:00:01")  # True

# 随机生成
random_mac = generate_random(vendor="Apple")

# 隐私遮蔽
masked = mask_mac("00:11:22:33:44:55")  # "00:11:22:**:**:**"
```

## 支持的厂商

内置 OUI 数据库包含以下厂商：

- Apple
- Microsoft
- Google
- Samsung
- Cisco
- Intel
- Dell
- HP
- Huawei
- TP-Link
- Netgear
- Xiaomi
- VMware
- Parallels
- VirtualBox
- QEMU/KVM

更多厂商可通过 `list_vendors()` 查看。

## 格式支持

- 冒号格式：`00:11:22:33:44:55`
- 连字符格式：`00-11-22-33-44-55`
- Cisco点号格式：`0011.2233.4455`
- 无分隔符格式：`001122334455`

## 测试

```bash
python mac_address_utils/mac_address_utils_test.py
```

## 示例

```bash
python mac_address_utils/examples/usage_examples.py
```

## 文件结构

```
mac_address_utils/
├── mod.py              # 主模块
├── mac_address_utils_test.py  # 测试
├── README.md           # 文档
└── examples/
    └── usage_examples.py  # 使用示例
```

## API 参考

### 验证与标准化

| 函数 | 说明 |
|------|------|
| `validate(mac)` | 验证 MAC 格式有效性 |
| `normalize(mac)` | 标准化为冒号格式 |

### 格式转换

| 函数 | 说明 |
|------|------|
| `to_colon_format(mac)` | 冒号格式 |
| `to_hyphen_format(mac)` | 连字符格式 |
| `to_dot_format(mac)` | Cisco点号格式 |
| `to_no_separator_format(mac)` | 无分隔符 |

### 厂商查询

| 函数 | 说明 |
|------|------|
| `get_oui(mac)` | 获取 OUI (前24位) |
| `lookup_vendor(mac)` | 查询厂商名称 |
| `list_vendors()` | 列出所有支持的厂商 |

### 地址类型

| 函数 | 说明 |
|------|------|
| `is_multicast(mac)` | 是否多播 |
| `is_unicast(mac)` | 是否单播 |
| `is_broadcast(mac)` | 是否广播 |
| `is_locally_administered(mac)` | 是否本地管理 |
| `is_globally_unique(mac)` | 是否全局唯一 |
| `get_type_info(mac)` | 获取类型信息字典 |

### 随机生成

| 函数 | 说明 |
|------|------|
| `generate_random()` | 随机 MAC |
| `generate_random(vendor="Apple")` | 指定厂商 OUI |
| `generate_random(locally_administered=True)` | 本地管理地址 |
| `generate_random_multicast()` | 随机多播地址 |

### 算术运算

| 函数 | 说明 |
|------|------|
| `increment(mac, count)` | 递增 |
| `decrement(mac, count)` | 递减 |
| `generate_range(start, count)` | 生成连续范围 |

### 比较与转换

| 函数 | 说明 |
|------|------|
| `compare(mac1, mac2)` | 比较 (-1/0/1) |
| `is_equal(mac1, mac2)` | 相等判断 |
| `parse(mac)` | 解析为字节元组 |
| `from_bytes(b1..b6)` | 从字节构建 |
| `to_integer(mac)` | 转48位整数 |
| `from_integer(value)` | 从整数构建 |

### IP 多播

| 函数 | 说明 |
|------|------|
| `get_ip_multicast_mac(ip)` | IPv4 多播转 MAC |
| `get_ipv6_multicast_mac(ip)` | IPv6 多播转 MAC |

### 其他

| 函数 | 说明 |
|------|------|
| `mask_mac(mac, char)` | 遮蔽部分内容 |

## 版本

1.0.0

## 许可证

MIT