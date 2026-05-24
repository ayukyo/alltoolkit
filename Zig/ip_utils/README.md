# IP Utils - IPv4 地址工具模块

零依赖的 IPv4 地址处理工具，使用 Zig 语言实现。

## 功能特性

### IPv4 地址操作
- ✅ 字符串解析和验证
- ✅ 与 32 位整数互相转换
- ✅ 地址类型判断（私有、回环、多播、公网等）
- ✅ IP 地址遍历（下一个/上一个）

### 子网计算
- ✅ CIDR 表示法解析（如 `192.168.1.0/24`）
- ✅ 子网掩码转换
- ✅ 广播地址计算
- ✅ 可用主机数计算
- ✅ IP 归属判断

### IP 范围
- ✅ 范围创建和验证
- ✅ IP 数量计算
- ✅ 范围内 IP 检查

## 使用方法

```zig
const ip_utils = @import("mod.zig");

// 解析 IPv4 地址
const ip = try ip_utils.IPv4.parse("192.168.1.1");

// 地址类型判断
if (ip.isPrivate()) {
    // 私有地址
}
if (ip.isLoopback()) {
    // 回环地址
}
if (ip.isPublic()) {
    // 公网地址
}

// 子网计算
const subnet = try ip_utils.Subnet.fromCIDR("192.168.1.0/24");
const broadcast = subnet.broadcastAddress();
const host_count = subnet.mask.usableHostCount(); // 254

// 检查 IP 是否在子网内
if (subnet.contains(ip)) {
    // IP 在子网内
}

// IP 范围
const range = ip_utils.IPRange.init(
    try ip_utils.IPv4.parse("192.168.1.1"),
    try ip_utils.IPv4.parse("192.168.1.100")
);
const count = range.count(); // 100
```

## 运行测试

```bash
zig test mod.zig
```

## 运行示例

```bash
zig run example.zig
```

## API 参考

### IPv4 结构体

| 方法 | 描述 |
|------|------|
| `parse(str)` | 从字符串解析 IPv4 地址 |
| `toU32()` | 转换为 32 位无符号整数 |
| `fromU32(value)` | 从 32 位整数创建 IPv4 |
| `toString(buf)` | 转换为字符串格式 |
| `isPrivate()` | 是否为私有地址 |
| `isLoopback()` | 是否为回环地址 |
| `isLinkLocal()` | 是否为本地链路地址 |
| `isMulticast()` | 是否为多播地址 |
| `isBroadcast()` | 是否为广播地址 |
| `isReserved()` | 是否为保留地址 |
| `isPublic()` | 是否为公网地址 |

### SubnetMask 结构体

| 方法 | 描述 |
|------|------|
| `fromPrefix(len)` | 从 CIDR 前缀长度创建 |
| `fromIPv4(ip)` | 从 IPv4 地址创建 |
| `toIPv4()` | 转换为 IPv4 格式的掩码 |
| `hostBits()` | 获取主机位数 |
| `hostCount()` | 获取主机总数 |
| `usableHostCount()` | 获取可用主机数 |

### Subnet 结构体

| 方法 | 描述 |
|------|------|
| `fromCIDR(cidr)` | 从 CIDR 字符串创建 |
| `broadcastAddress()` | 获取广播地址 |
| `firstHost()` | 获取第一个可用主机 |
| `lastHost()` | 获取最后一个可用主机 |
| `contains(ip)` | 检查 IP 是否在子网内 |

### IPRange 结构体

| 方法 | 描述 |
|------|------|
| `init(start, end)` | 创建 IP 范围 |
| `contains(ip)` | 检查 IP 是否在范围内 |
| `count()` | 获取范围内的 IP 数量 |

### 工具函数

| 函数 | 描述 |
|------|------|
| `isValidIPv4(str)` | 验证 IPv4 地址字符串 |
| `isValidCIDR(cidr)` | 验证 CIDR 表示法 |
| `ipDistance(a, b)` | 计算两个 IP 之间的距离 |
| `nextIP(ip)` | 获取下一个 IP 地址 |
| `prevIP(ip)` | 获取上一个 IP 地址 |

## 支持的地址类型

- **私有地址**: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
- **回环地址**: 127.0.0.0/8
- **本地链路地址**: 169.254.0.0/16
- **多播地址**: 224.0.0.0/4
- **保留地址**: 0.0.0.0/8, 240.0.0.0/4, CGNAT 等
- **公网地址**: 除上述之外的所有地址