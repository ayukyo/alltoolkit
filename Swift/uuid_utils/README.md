# UUID Utilities (Swift)

通用 UUID 工具类，提供 UUID 生成、验证、解析和格式转换功能。

## 功能特性

- ✅ **UUID v4 生成** - 随机 UUID，符合 RFC 4122 标准
- ✅ **UUID v5 生成** - 基于命名空间的确定性 UUID（SHA-1）
- ✅ **UUID v7 生成** - 基于时间戳的可排序 UUID
- ✅ **UUID 验证** - 严格模式和宽松模式
- ✅ **格式转换** - 连字符添加/移除、大小写转换
- ✅ **版本检测** - 自动识别 UUID 版本
- ✅ **时间戳提取** - 从 UUID v7 提取生成时间
- ✅ **文本提取** - 从任意文本中提取 UUID
- ✅ **短 UUID** - Base62 编码的紧凑 UUID
- ✅ **零依赖** - 仅使用 Swift 标准库和 Foundation

## 安装

将 `mod.swift` 文件添加到您的 Swift 项目中即可。

```swift
// 直接复制到项目中
// 或使用 Swift Package Manager
```

## 快速开始

```swift
import Foundation

// 基本生成
let uuid = UUIDUtils.generate()
// 输出: "550e8400e29b41d4a716446655440000" (32字符，无连字符)

// 带格式生成
let uuidWithHyphens = UUIDUtils.generate(withHyphens: true, uppercase: false)
// 输出: "550e8400-e29b-41d4-a716-446655440000"

// 大写格式
let uuidUpper = UUIDUtils.generate(withHyphens: true, uppercase: true)
// 输出: "550E8400-E29B-41D4-A716-446655440000"
```

## API 文档

### UUID 生成

```swift
// 生成随机 UUID (v4)
let uuid = UUIDUtils.generate()  // 无连字符，32字符
let uuid = UUIDUtils.generate(withHyphens: true)  // 标准格式，36字符
let uuid = UUIDUtils.generate(withHyphens: true, uppercase: true)  // 大写

// 批量生成
let uuids = UUIDUtils.generate(count: 10)

// UUID v7 (基于时间戳，可排序)
let v7 = UUIDUtils.generateV7()
// 提取时间戳
if let timestamp = UUIDUtils.extractTimestamp(fromV7: v7) {
    print("Generated at: \(timestamp)")
}

// UUID v5 (基于命名空间，确定性)
let v5 = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "example.com")
// 使用预定义命名空间
let dnsUUID = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "example.com")
let urlUUID = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceURL, name: "https://example.com")
```

### UUID 验证

```swift
// 严格验证（需要标准格式）
UUIDUtils.isValid("550e8400-e29b-41d4-a716-446655440000")  // true
UUIDUtils.isValid("550e8400e29b41d4a716446655440000")    // false (无连字符)

// 宽松验证（支持无连字符格式）
UUIDUtils.isValidLoose("550e8400e29b41d4a716446655440000")  // true

// 解析 UUID
let uuid = UUIDUtils.parse("550e8400-e29b-41d4-a716-446655440000")
let uuidLoose = UUIDUtils.parseLoose("550e8400e29b41d4a716446655440000")
```

### 版本检测

```swift
let uuid = UUID().uuidString
let v7 = UUIDUtils.generateV7()

// 获取版本号
UUIDUtils.getVersion(uuid)  // 4
UUIDUtils.getVersion(v7)   // 7

// 快速检测
UUIDUtils.isV4(uuid)  // true
UUIDUtils.isV7(v7)    // true
```

### 格式转换

```swift
// 添加/移除连字符
UUIDUtils.addHyphens("550e8400e29b41d4a716446655440000")
// 返回: "550e8400-e29b-41d4-a716-446655440000"

UUIDUtils.removeHyphens("550e8400-e29b-41d4-a716-446655440000")
// 返回: "550e8400e29b41d4a716446655440000"

// 大小写转换
UUIDUtils.toUppercase("550e8400-e29b-41d4-a716-446655440000")
// 返回: "550E8400-E29B-41D4-A716-446655440000"

UUIDUtils.toLowercase("550E8400-E29B-41D4-A716-446655440000")
// 返回: "550e8400-e29b-41d4-a716-446655440000"
```

### 文本提取

```swift
let text = "User ID: 550e8400-e29b-41d4-a716-446655440000, Order: 6fa459ea-ee8a-3ca4-894e-db77e160355e"

// 提取所有 UUID
let uuids = UUIDUtils.extract(from: text)
// 返回: ["550e8400-e29b-41d4-a716-446655440000", "6fa459ea-ee8a-3ca4-894e-db77e160355e"]

// 提取第一个
let first = UUIDUtils.extractFirst(from: text)
// 返回: "550e8400-e29b-41d4-a716-446655440000"
```

### 比较

```swift
// 相等比较（忽略大小写和连字符）
UUIDUtils.areEqual("550e8400-e29b-41d4-a716-446655440000", 
                   "550E8400E29B41D4A716446655440000")  // true

// 排序比较
UUIDUtils.compare("00000000-0000-0000-0000-000000000001",
                  "00000000-0000-0000-0000-000000000002")
// 返回: .orderedAscending
```

### 短 UUID

```swift
// Base62 编码短 UUID (约22字符)
let short = UUIDUtils.generateShort()

// 指定长度
let short8 = UUIDUtils.generateShort(length: 8)
```

### Nil UUID

```swift
// 获取 Nil UUID
let nilUUID = UUIDUtils.nilUUID()  // "00000000-0000-0000-0000-000000000000"

// 检查是否为 Nil UUID
UUIDUtils.isNil(nilUUID)  // true
```

### String 扩展

```swift
// String 扩展提供便捷方法
let text = "550e8400-e29b-41d4-a716-446655440000"

text.isValidUUID      // true
text.uuidValue        // UUID?
text.uuidSimplified   // "550e8400e29b41d4a716446655440000"

let compact = "550e8400e29b41d4a716446655440000"
compact.isValidUUIDLoose  // true
compact.uuidFormatted     // "550e8400-e29b-41d4-a716-446655440000"
```

## 预定义命名空间

UUID v5 需要命名空间，提供了以下预定义命名空间：

```swift
UUIDUtils.namespaceDNS   // 6ba7b810-9dad-11d1-80b4-00c04fd430c8
UUIDUtils.namespaceURL   // 6ba7b811-9dad-11d1-80b4-00c04fd430c8
UUIDUtils.namespaceOID   // 6ba7b812-9dad-11d1-80b4-00c04fd430c8
UUIDUtils.namespaceX500  // 6ba7b814-9dad-11d1-80b4-00c04fd430c8
```

## 系统要求

- iOS 13.0+ / macOS 10.15+ / watchOS 6.0+ / tvOS 13.0+
- Swift 5.0+

## 测试覆盖率

- 基本生成: ✅
- UUID v7: ✅
- UUID v5: ✅
- 验证: ✅
- 版本检测: ✅
- 格式转换: ✅
- 文本提取: ✅
- 比较: ✅
- 时间戳提取: ✅
- 短 UUID: ✅
- Nil UUID: ✅
- String 扩展: ✅
- 性能测试: ✅

## 许可证

MIT License

## 作者

AllToolkit