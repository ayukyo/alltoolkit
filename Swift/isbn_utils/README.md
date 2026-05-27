# ISBN Utils - ISBN 验证与转换工具

[![Swift](https://img.shields.io/badge/Swift-5.5+-orange.svg)](https://swift.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-green.svg)]()

Swift 实现的 ISBN-10/ISBN-13 验证、转换和生成工具库。纯标准库实现，零外部依赖。

## 功能特性

- ✅ **ISBN-10 验证** - 支持标准数字和 X 校验位
- ✅ **ISBN-13 验证** - 支持 978/979 前缀
- ✅ **校验位计算** - 自动计算 ISBN-10 和 ISBN-13 校验位
- ✅ **格式转换** - ISBN-10 ↔ ISBN-13 双向转换
- ✅ **文本提取** - 从任意文本中提取 ISBN
- ✅ **格式化显示** - 添加连字符的标准显示格式
- ✅ **随机生成** - 生成有效的测试用 ISBN
- ✅ **String 扩展** - 便捷的 `.isValidISBN` 和 `.formattedISBN` 属性

## 安装

将 `mod.swift` 文件添加到您的 Swift 项目中即可。

## 快速开始

### 验证 ISBN

```swift
// 验证任意 ISBN
let result = ISBNUtils.validate("978-0-13-235088-4")

switch result {
case .success(let isbn):
    print("有效 ISBN: \(isbn.formatted)")
    print("类型: \(isbn.type)")  // .isbn10 或 .isbn13
case .failure(let error):
    print("无效: \(error.localizedDescription)")
}
```

### 校验位计算

```swift
// 计算 ISBN-10 校验位（可能返回 0-9 或 X）
let check10 = ISBNUtils.calculateISBN10CheckDigit("030640615")  // "2"

// 计算 ISBN-13 校验位（返回 0-9）
let check13 = ISBNUtils.calculateISBN13CheckDigit("978030640615")  // "7"
```

### 格式转换

```swift
// ISBN-10 → ISBN-13
if case .success(let isbn13) = ISBNUtils.toISBN13("0306406152") {
    print("ISBN-13: \(isbn13)")  // "9780306406157"
}

// ISBN-13 → ISBN-10（仅限 978 前缀）
if case .success(let isbn10) = ISBNUtils.toISBN10("9780306406157") {
    print("ISBN-10: \(isbn10)")  // "0306406152"
}
```

### 从文本提取

```swift
let text = """
推荐书籍:
1. Clean Code - ISBN: 978-0-13-235088-4
2. 设计模式 - 0-201-63361-2
"""

let isbns = ISBNUtils.extract(from: text)
for isbn in isbns {
    print("\(isbn.formatted) (\(isbn.type))")
}
```

### 格式化显示

```swift
// 添加标准连字符
ISBNUtils.formatISBN10("0306406152")   // "0-30640-615-2"
ISBNUtils.formatISBN13("9780306406157") // "978-030640615-7"
```

### 随机生成（测试用）

```swift
let randomISBN13 = ISBNUtils.generateRandomISBN13()
let randomISBN10 = ISBNUtils.generateRandomISBN10()
```

### String 扩展

```swift
let isbn = "9780306406157"

if isbn.isValidISBN {
    print(isbn.formattedISBN)  // "978-030640615-7"
}
```

## API 参考

### ISBNUtils

| 方法 | 说明 |
|------|------|
| `validate(_:)` | 验证 ISBN 字符串，返回 `Result<ISBN, ISBNError>` |
| `validateISBN10(_:)` | 验证 ISBN-10 |
| `validateISBN13(_:)` | 验证 ISBN-13 |
| `calculateISBN10CheckDigit(_:)` | 计算 ISBN-10 校验位 |
| `calculateISBN13CheckDigit(_:)` | 计算 ISBN-13 校验位 |
| `toISBN13(_:)` | 将 ISBN-10 转换为 ISBN-13 |
| `toISBN10(_:)` | 将 ISBN-13 转换为 ISBN-10 |
| `extract(from:)` | 从文本中提取所有 ISBN |
| `formatISBN10(_:)` | 格式化 ISBN-10 显示 |
| `formatISBN13(_:)` | 格式化 ISBN-13 显示 |
| `generateRandomISBN10()` | 生成随机有效 ISBN-10 |
| `generateRandomISBN13()` | 生成随机有效 ISBN-13 |

### ISBN 枚举

```swift
public enum ISBN {
    case isbn10(String)
    case isbn13(String)
    
    var digits: String      // 纯数字字符串
    var type: ISBNType      // .isbn10 或 .isbn13
    var formatted: String   // 格式化显示
}
```

### ISBNError 错误类型

```swift
public enum ISBNError: Error {
    case invalidFormat                    // 无效格式
    case invalidCheckDigit(expected, actual) // 校验位错误
    case invalidLength                    // 长度错误
    case conversionError                  // 转换错误
}
```

## 文件结构

```
Swift/isbn_utils/
├── mod.swift              # 主模块（核心实现）
├── isbn_utils_test.swift  # 单元测试
├── examples/
│   └── usage_examples.swift  # 使用示例
└── README.md
```

## 运行测试

```bash
cd Swift/isbn_utils
swift isbn_utils_test.swift
```

## 运行示例

```bash
cd Swift/isbn_utils
swift examples/usage_examples.swift
```

## 注意事项

1. **ISBN-10 到 ISBN-13**: 总是成功，会添加 978 前缀
2. **ISBN-13 到 ISBN-10**: 仅适用于 978 前缀的 ISBN-13，979 前缀会返回转换错误
3. **校验位 X**: 仅适用于 ISBN-10，代表数值 10
4. **输入容错**: 自动忽略空格、连字符等非数字字符

## 算法说明

### ISBN-10 校验算法

```
校验位 = (11 - (d1*10 + d2*9 + ... + d9*2) mod 11) mod 11
```
如果结果为 10，则校验位为 X。

### ISBN-13 校验算法

```
校验位 = (10 - (d1*1 + d2*3 + d3*1 + d4*3 + ...) mod 10) mod 10
```
权重交替为 1 和 3。

## License

MIT License