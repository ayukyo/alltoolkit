# IP 子网计算器 (IP Calculator Utils)

Go 语言实现的 IP 地址和子网计算工具库，零外部依赖，支持 IPv4 和 IPv6。

## 功能特性

- **CIDR 解析**: 解析 CIDR 表示法，获取完整子网信息
- **子网范围计算**: 计算网络地址、广播地址、可用 IP 范围
- **IP 范围检测**: 判断 IP 地址是否在指定子网内
- **子网掩码转换**: 前缀长度与子网掩码互转
- **子网划分**: 计算子网划分方案
- **IP 地址比较**: 比较 IP 地址大小
- **IP 地址转换**: IP 地址与整数互转
- **IPv6 支持**: 完整支持 IPv6 地址处理
- **端口处理**: 端口范围解析和验证
- **IP 分类**: IPv4 地址 A/B/C/D/E 类别判断

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/ip_calculator_utils
```

## 快速开始

### 解析 CIDR 获取子网信息

```go
package main

import (
    "fmt"
    ipcalc "github.com/ayukyo/alltoolkit/Go/ip_calculator_utils"
)

func main() {
    info, err := ipcalc.GetSubnetInfo("192.168.1.0/24")
    if err != nil {
        panic(err)
    }

    fmt.Printf("网络地址: %s\n", info.NetworkAddress)
    fmt.Printf("广播地址: %s\n", info.BroadcastAddr)
    fmt.Printf("第一个可用IP: %s\n", info.FirstUsable)
    fmt.Printf("最后一个可用IP: %s\n", info.LastUsable)
    fmt.Printf("子网掩码: %s\n", info.SubnetMask)
    fmt.Printf("通配符掩码: %s\n", info.WildcardMask)
    fmt.Printf("前缀长度: %d\n", info.PrefixLength)
    fmt.Printf("总IP数量: %d\n", info.TotalHosts)
    fmt.Printf("可用IP数量: %d\n", info.UsableHosts)
    fmt.Printf("私有地址: %v\n", info.IsPrivate)
}
```

### 检查 IP 是否在子网内

```go
// 单个子网检查
inRange, err := ipcalc.IPInRange("192.168.1.100", "192.168.1.0/24")
// inRange = true

// 多个子网检查
cidrs := []string{"10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"}
inRange, match, _ := ipcalc.IPInMultipleRanges("192.168.1.1", cidrs)
// inRange = true, match = "192.168.0.0/16"
```

### 子网掩码转换

```go
// 前缀长度 -> 子网掩码
mask, _ := ipcalc.SubnetToMask(24, false)  // "255.255.255.0"
mask, _ := ipcalc.SubnetToMask(16, false) // "255.255.0.0"

// 子网掩码 -> 前缀长度
prefix, _ := ipcalc.MaskToPrefixLength("255.255.255.0") // 24
```

### 子网划分

```go
// 将 /24 划分为 /26 子网
subnets, _ := ipcalc.CalculateSubnets("192.168.1.0/24", 26)
for i, subnet := range subnets {
    fmt.Printf("子网 %d: %s - %s (%d IPs)\n", i+1, subnet.Start, subnet.End, subnet.Count)
}

// 获取 CIDR 表示
cidrs, _ := ipcalc.SplitCIDRByMask("192.168.1.0/24", 26)
// ["192.168.1.0/26", "192.168.1.64/26", "192.168.1.128/26", "192.168.1.192/26"]
```

### IP 地址转换

```go
// IP -> 整数
n, _ := ipcalc.IPToInt("192.168.1.1") // 3232235777

// 整数 -> IP
ip, _ := ipcalc.IntToIP(3232235777) // "192.168.1.1"
```

### IP 地址比较

```go
result, _ := ipcalc.CompareIPs("192.168.1.1", "192.168.1.2")
// result = -1 (第一个小于第二个)
```

### IP 地址验证和分类

```go
// 验证 IP 地址
valid, version := ipcalc.ValidateIP("192.168.1.1")
// valid = true, version = 4

// 获取 IP 类别
class, _ := ipcalc.GetIPClass("192.168.1.1") // "C"
```

### 端口范围解析

```go
// 单端口
start, end, _ := ipcalc.ParsePortRange("80") // 80, 80

// 端口范围
start, end, _ := ipcalc.ParsePortRange("80-443") // 80, 443

// 端口验证
valid := ipcalc.ValidatePort(80) // true
valid := ipcalc.ValidatePort(0)  // false
```

### IPv6 支持

```go
// IPv6 CIDR 解析
info, _ := ipcalc.GetSubnetInfo("2001:db8::/32")

// IPv6 范围检查
inRange, _ := ipcalc.IPInRange("2001:db8::1", "2001:db8::/32") // true
```

## API 参考

### SubnetInfo 结构体

```go
type SubnetInfo struct {
    NetworkAddress string   // 网络地址
    BroadcastAddr   string   // 广播地址 (IPv4 only)
    FirstUsable     string   // 第一个可用IP
    LastUsable      string   // 最后一个可用IP
    SubnetMask      string   // 子网掩码
    WildcardMask    string   // 通配符掩码
    PrefixLength    int      // 前缀长度
    TotalHosts      uint64   // 总IP数量
    UsableHosts     uint64   // 可用IP数量
    IPVersion       int      // IP版本 (4 or 6)
    IsPrivate       bool     // 是否私有地址
    IsLoopback      bool     // 是否回环地址
    ReservedIPs     []string // 保留的IP地址
}
```

### 主要函数

| 函数 | 说明 |
|------|------|
| `ParseCIDR(cidr string)` | 解析 CIDR 表示法 |
| `GetSubnetInfo(cidr string)` | 获取子网详细信息 |
| `IPInRange(ip, cidr string)` | 检查 IP 是否在子网内 |
| `IPInMultipleRanges(ip string, cidrs []string)` | 检查 IP 是否在多个子网内 |
| `SubnetToMask(prefixLen int, ipv6 bool)` | 前缀长度转子网掩码 |
| `MaskToPrefixLength(mask string)` | 子网掩码转前缀长度 |
| `CalculateSubnets(cidr string, newPrefixLen int)` | 计算子网划分 |
| `SplitCIDRByMask(cidr string, newMask int)` | 按掩码划分子网 |
| `GetIPsInRange(cidr string, limit int)` | 获取子网内 IP 列表 |
| `ValidateIP(ip string)` | 验证 IP 地址 |
| `GetIPClass(ip string)` | 获取 IPv4 类别 |
| `CompareIPs(ip1, ip2 string)` | 比较两个 IP 地址 |
| `IPToInt(ip string)` | IP 转整数 |
| `IntToIP(n uint64)` | 整数转 IPv4 |
| `FormatIPWithCIDR(ip string, prefixLen int)` | 格式化 IP/CIDR |
| `ParsePortRange(portRange string)` | 解析端口范围 |
| `ValidatePort(port int)` | 验证端口 |

## 运行示例

```bash
cd examples
go run main.go
```

## 运行测试

```bash
go test -v
```

## 基准测试

```bash
go test -bench=.
```

## 错误处理

所有函数返回的错误可以使用 `errors.Is()` 进行判断：

```go
import "errors"

result, err := ipcalc.GetSubnetInfo("invalid")
if errors.Is(err, ipcalc.ErrInvalidCIDR) {
    // 处理无效 CIDR
}
```

支持的错误类型：
- `ErrInvalidCIDR`: 无效的 CIDR 表示法
- `ErrInvalidIP`: 无效的 IP 地址
- `ErrInvalidSubnetMask`: 无效的子网掩码
- `ErrIPVersionMismatch`: IP 版本不匹配

## 许可证

MIT License