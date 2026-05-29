# SemVer Utilities (Swift)

语义版本控制工具类，提供版本解析、比较、验证和操作功能。完全符合 Semantic Versioning 2.0.0 规范。

## 功能特性

- ✅ **版本解析** - 支持完整 SemVer 格式和宽松解析
- ✅ **版本验证** - 严格和宽松模式验证
- ✅ **版本比较** - 支持预发布版本的完整比较逻辑
- ✅ **版本排序** - 对版本列表进行排序
- ✅ **范围检查** - 检查版本是否在指定范围内
- ✅ **约束满足** - 支持多种约束格式（^, ~, >=, <, x 范围）
- ✅ **版本递增** - 主版本、次版本、补丁版本递增
- ✅ **版本提取** - 从文本中提取版本号
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

// 解析版本
let version = SemVerUtils.parse("1.2.3")
print(version?.fullVersion)  // "1.2.3"

// 比较版本
let result = SemVerUtils.compare("1.0.0", "2.0.0")
// .orderedAscending (1.0.0 < 2.0.0)

// 检查约束
let satisfies = SemVerUtils.satisfies("1.5.0", constraint: "^1.0.0")
// true
```

## API 文档

### 版本解析

```swift
// 标准解析
let v1 = SemVerUtils.parse("1.2.3")
let v2 = SemVerUtils.parse("v1.2.3")  // 支持 v 前缀
let v3 = SemVerUtils.parse("1.2.3-alpha")  // 预发布版本
let v4 = SemVerUtils.parse("1.2.3+build.123")  // 构建元数据
let v5 = SemVerUtils.parse("1.2.3-beta.1+build.456")  // 完整格式

// 宽松解析（支持不完整版本）
let v6 = SemVerUtils.parseLoose("1")  // 解析为 1.0.0
let v7 = SemVerUtils.parseLoose("1.2")  // 解析为 1.2.0
```

### SemVer 结构体

```swift
let v = SemVerUtils.parse("1.2.3-beta+build")!

v.major            // 1
v.minor            // 2
v.patch            // 3
v.prerelease       // "beta"
v.buildMetadata    // "build"
v.isStable         // false
v.isPrerelease     // true
v.coreVersion      // "1.2.3"
v.fullVersion      // "1.2.3-beta+build"
```

### 版本验证

```swift
// 严格验证（需要完整版本）
SemVerUtils.isValid("1.2.3")        // true
SemVerUtils.isValid("1")            // false

// 宽松验证
SemVerUtils.isValidLoose("1")       // true
SemVerUtils.isValidLoose("1.2")     // true
```

### 版本比较

```swift
// 比较结果
SemVerUtils.compare("1.0.0", "2.0.0")  // .orderedAscending
SemVerUtils.compare("2.0.0", "1.0.0")  // .orderedDescending
SemVerUtils.compare("1.0.0", "1.0.0")  // .orderedSame

// 比较方法
SemVerUtils.isGreater("2.0.0", than: "1.0.0")   // true
SemVerUtils.isLess("1.0.0", than: "2.0.0")      // true
SemVerUtils.isGreaterOrEqual("1.0.0", to: "1.0.0")  // true
SemVerUtils.isEqual("1.0.0", "1.0.0")           // true

// 预发布版本比较
SemVerUtils.compare("1.0.0-alpha", "1.0.0")  // .orderedAscending (预发布 < 正式)
SemVerUtils.compare("1.0.0-alpha", "1.0.0-beta")  // .orderedAscending
```

### 版本排序

```swift
let versions = ["3.0.0", "1.0.0", "2.0.0"]

// 排序为 SemVer 对象
let sorted = SemVerUtils.sort(versions)
// [SemVer(1.0.0), SemVer(2.0.0), SemVer(3.0.0)]

// 排序为字符串
let sortedStrings = SemVerUtils.sortStrings(versions)
// ["1.0.0", "2.0.0", "3.0.0"]

// 获取最新/最旧版本
let latest = SemVerUtils.latest(versions)   // SemVer(3.0.0)
let oldest = SemVerUtils.oldest(versions)   // SemVer(1.0.0)
```

### 版本范围

```swift
// 范围检查
SemVerUtils.isInRange("1.5.0", min: "1.0.0", max: "2.0.0")  // true
SemVerUtils.isInRange("0.9.0", min: "1.0.0", max: "2.0.0")  // false
```

### 约束满足

支持以下约束格式：

```swift
// 精确匹配
SemVerUtils.satisfies("1.2.3", constraint: "1.2.3")  // true

// 比较操作符
SemVerUtils.satisfies("1.5.0", constraint: ">=1.0.0")  // true
SemVerUtils.satisfies("0.9.0", constraint: "<1.0.0")   // true
SemVerUtils.satisfies("1.0.0", constraint: "<=1.0.0")  // true
SemVerUtils.satisfies("1.0.1", constraint: ">1.0.0")   // true

// 脱字符约束 (^) - 允许次版本和补丁变更
SemVerUtils.satisfies("1.5.0", constraint: "^1.0.0")   // true
SemVerUtils.satisfies("2.0.0", constraint: "^1.0.0")   // false
SemVerUtils.satisfies("0.2.5", constraint: "^0.2.3")   // true (0.x 只允许补丁变更)

// 波浪号约束 (~) - 只允许补丁变更
SemVerUtils.satisfies("1.2.9", constraint: "~1.2.3")   // true
SemVerUtils.satisfies("1.3.0", constraint: "~1.2.3")   // false

// X 范围
SemVerUtils.satisfies("1.5.0", constraint: "1.x")      // true
SemVerUtils.satisfies("1.2.5", constraint: "1.2.x")    // true
SemVerUtils.satisfies("1.2.5", constraint: "1.2.*")    // true
```

### 版本递增

```swift
// 递增主版本
SemVerUtils.incrementMajor("1.2.3")  // SemVer(2.0.0)

// 递增次版本
SemVerUtils.incrementMinor("1.2.3")  // SemVer(1.3.0)

// 递增补丁版本
SemVerUtils.incrementPatch("1.2.3")  // SemVer(1.2.4)

// 设置预发布标识符
SemVerUtils.setPrerelease("1.2.3", prerelease: "beta.1")  // SemVer(1.2.3-beta.1)

// 移除预发布标识符
SemVerUtils.removePrerelease("1.2.3-beta")  // SemVer(1.2.3)
```

### 版本差异

```swift
let diff = SemVerUtils.diff("1.0.0", "2.0.0")
// .major (主版本更新)

let diff2 = SemVerUtils.diff("1.0.0", "1.1.0")
// .minor (次版本更新)

let diff3 = SemVerUtils.diff("1.0.0", "1.0.1")
// .patch (补丁更新)

let diff4 = SemVerUtils.diff("1.0.0-alpha", "1.0.0-beta")
// .prerelease (预发布变化)
```

### 版本提取

```swift
let text = "We use v1.2.3 and v2.0.0-beta in production"

// 提取所有版本
let versions = SemVerUtils.extract(from: text)
// [SemVer(1.2.3), SemVer(2.0.0-beta)]

// 提取第一个版本
let first = SemVerUtils.extractFirst(from: text)
// SemVer(1.2.3)
```

### 工厂方法

```swift
// 创建初始版本
let v1 = SemVerUtils.initial()  // SemVer(0.0.1)

// 创建零版本
let v2 = SemVerUtils.zero()     // SemVer(0.0.0)

// 快速创建版本
let v3 = SemVerUtils.version(1)        // SemVer(1.0.0)
let v4 = SemVerUtils.version(1, 2)     // SemVer(1.2.0)
let v5 = SemVerUtils.version(1, 2, 3)  // SemVer(1.2.3)
```

### String 扩展

```swift
// 解析扩展
let v = "1.2.3".semver          // SemVer?
let vLoose = "1".semverLoose    // SemVer?

// 验证扩展
"1.2.3".isValidSemVer           // true

// 约束检查扩展
"1.5.0".satisfiesSemVer(">=1.0.0")  // true?
```

### Array 扩展

```swift
let versions = ["3.0.0", "1.0.0", "2.0.0"]

// 排序扩展
versions.sortedSemVer           // ["1.0.0", "2.0.0", "3.0.0"]

// 最新/最旧扩展
versions.latestSemVer           // SemVer(3.0.0)
versions.oldestSemVer           // SemVer(1.0.0)
```

## SemVer 比较规则

遵循 SemVer 2.0.0 规范：

1. **主版本比较**: 1.0.0 < 2.0.0 < 3.0.0
2. **次版本比较**: 1.1.0 < 1.2.0 < 1.3.0
3. **补丁比较**: 1.0.1 < 1.0.2 < 1.0.3
4. **预发布优先级低**: 1.0.0-alpha < 1.0.0
5. **预发布标识符比较**:
   - 数值标识符按数值比较: alpha.1 < alpha.2
   - 字符标识符按字母顺序: alpha < beta
   - 数值标识符低于字符串标识符: alpha.1 < alpha.beta

## Codable 支持

SemVer 支持 JSON 编解码：

```swift
let v = SemVerUtils.parse("1.2.3-beta")!
let encoder = JSONEncoder()
let data = encoder.encode(v)

let decoder = JSONDecoder()
let decoded = decoder.decode(SemVer.self, from: data)
```

## 系统要求

- iOS 13.0+ / macOS 10.15+ / watchOS 6.0+ / tvOS 13.0+
- Swift 5.0+

## 测试覆盖率

- 版本解析: ✅
- 版本验证: ✅
- 版本比较: ✅
- 预发布比较: ✅
- 版本排序: ✅
- 范围检查: ✅
- 约束满足: ✅
- 版本递增: ✅
- 版本差异: ✅
- 版本提取: ✅
- 工厂方法: ✅
- String 扩展: ✅
- Array 扩展: ✅
- Codable: ✅
- Hashable: ✅
- 性能测试: ✅

## 许可证

MIT License

## 作者

AllToolkit