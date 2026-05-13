# ISBN Utils - 国际标准书号工具集

[![Kotlin](https://img.shields.io/badge/Kotlin-1.9+-7F52FF.svg)](https://kotlinlang.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

纯 Kotlin 实现的 ISBN（国际标准书号）工具集，无外部依赖。

## 功能特性

- ✅ **ISBN-10 验证** - 完整的校验位验证
- ✅ **ISBN-13 验证** - 支持 978 和 979 前缀
- ✅ **ISBN-10 ⇄ ISBN-13 转换** - 双向转换（979 前缀 ISBN-13 仅支持转为 ISBN-10）
- ✅ **ISBN 解析** - 提取前缀、注册组、出版者、校验位等信息
- ✅ **格式化输出** - 标准 ISBN 格式化显示
- ✅ **批量验证** - 高效处理大量 ISBN
- ✅ **文本提取** - 从文本中自动提取有效 ISBN
- ✅ **随机生成** - 生成有效的测试用 ISBN
- ✅ **等价性比较** - 判断不同格式的 ISBN 是否代表同一本书
- ✅ **扩展函数** - Kotlin 风格的扩展函数 API

## 快速开始

### 基本验证

```kotlin
import isbn_utils.ISBNUtils
import isbn_utils.isValidISBN

// 验证 ISBN
val isValid1 = ISBNUtils.validate("0-306-40615-2")    // true (ISBN-10)
val isValid2 = ISBNUtils.validate("978-0-306-40615-7") // true (ISBN-13)
val isValid3 = ISBNUtils.validate("123-456-789-X")     // false

// 使用扩展函数
val isValid = "9787115212105".isValidISBN()
```

### 类型检测

```kotlin
import isbn_utils.ISBNUtils
import isbn_utils.ISBNType

val type1 = ISBNUtils.detectType("0306406152")      // ISBNType.ISBN_10
val type2 = ISBNUtils.detectType("9780306406157")   // ISBNType.ISBN_13
val type3 = ISBNUtils.detectType("12345")           // ISBNType.INVALID
```

### ISBN 转换

```kotlin
// ISBN-10 转 ISBN-13
val isbn13 = ISBNUtils.convertToISBN13("0306406152")
// -> "9780306406157"

// ISBN-13 转 ISBN-10（仅支持 978 前缀）
val isbn10 = ISBNUtils.convertToISBN10("9780306406157")
// -> "0306406152"

// 979 前缀的 ISBN-13 无法转为 ISBN-10
val cannotConvert = ISBNUtils.convertToISBN10("9791091146135")
// -> null
```

### 格式化

```kotlin
import isbn_utils.formatISBN

// 格式化 ISBN
val formatted1 = ISBNUtils.format("0306406152")
// -> "0-30640-615-2"

val formatted2 = ISBNUtils.format("9780306406157")
// -> "978-0-30640-615-7"

// 使用扩展函数
val formatted = "9787115212105".formatISBN()
```

### 解析详细信息

```kotlin
val info = ISBNUtils.parse("9787115212105")

println(info.isValid)           // true
println(info.type)               // ISBNType.ISBN_13
println(info.formatted)          // "978-7-11521-210-5"
println(info.prefix)             // "978"
println(info.registrationGroup)  // "7" (中国)
println(info.checkDigit)         // '5'
println(info.isbn10)             // "7115212107"
println(info.isbn13)             // "9787115212105"
```

### 批量验证

```kotlin
val isbns = listOf(
    "0306406152",     // 有效
    "9780306406157",  // 有效
    "1234567890",     // 无效
    "0471958697"      // 有效
)

val results = ISBNUtils.validateBatch(isbns)
// { "0306406152"=true, "9780306406157"=true, "1234567890"=false, "0471958697"=true }
```

### 从文本提取

```kotlin
val text = """
    推荐书籍：
    1. 《代码大全》ISBN: 978-7-115-21210-5
    2. 《编程珠玑》ISBN-10: 0-201-03336-1
"""

val extracted = ISBNUtils.extractFromText(text)
// ["9787115212105", "0201033361"]
```

### 等价性比较

```kotlin
// 同一本书的不同格式
val same = ISBNUtils.areEquivalent("0306406152", "9780306406157")  // true

// 不同的书
val different = ISBNUtils.areEquivalent("0306406152", "0471958697")  // false
```

### 生成随机 ISBN

```kotlin
// 生成随机有效的 ISBN
val randomISBN10 = ISBNUtils.generateRandomISBN10()
val randomISBN13 = ISBNUtils.generateRandomISBN13()

println(randomISBN10)  // 如: "123456789X"
println(randomISBN13)  // 如: "9781234567890"
```

### 校验位计算

```kotlin
// 计算 ISBN-10 校验位
val check10 = ISBNUtils.calculateISBN10CheckDigit("030640615")
// -> '2'

// 计算 ISBN-13 校验位
val check13 = ISBNUtils.calculateISBN13CheckDigit("978030640615")
// -> '7'
```

### 获取摘要

```kotlin
val summary = ISBNUtils.getSummary("9787115212105")
// 输出:
// ISBN 信息:
//   类型: ISBN-13
//   原始: 9787115212105
//   格式化: 978-7-11521-210-5
//   GS1 前缀: 978
//   注册组: 7 (中国)
//   出版者代码: 11521
//   校验位: 5
//   ISBN-10: 7115212107
//   ISBN-13: 9787115212105
```

## API 参考

### 主要方法

| 方法 | 描述 |
|------|------|
| `validate(isbn: String): Boolean` | 验证 ISBN（自动检测类型） |
| `validateISBN10(isbn: String): Boolean` | 验证 ISBN-10 |
| `validateISBN13(isbn: String): Boolean` | 验证 ISBN-13 |
| `detectType(isbn: String): ISBNType` | 检测 ISBN 类型 |
| `format(isbn: String): String` | 格式化 ISBN |
| `parse(isbn: String): ISBNInfo` | 解析 ISBN 详细信息 |
| `convertToISBN10(isbn13: String): String?` | ISBN-13 转 ISBN-10 |
| `convertToISBN13(isbn10: String): String?` | ISBN-10 转 ISBN-13 |
| `cleanISBN(isbn: String): String` | 清理 ISBN（移除分隔符） |
| `validateBatch(isbns: List<String>): Map<String, Boolean>` | 批量验证 |
| `extractFromText(text: String): List<String>` | 从文本提取 ISBN |
| `areEquivalent(isbn1: String, isbn2: String): Boolean` | 等价性比较 |
| `generateRandomISBN10(): String` | 生成随机 ISBN-10 |
| `generateRandomISBN13(): String` | 生成随机 ISBN-13 |
| `calculateISBN10CheckDigit(isbn9: String): Char` | 计算 ISBN-10 校验位 |
| `calculateISBN13CheckDigit(isbn12: String): Char` | 计算 ISBN-13 校验位 |
| `getSummary(isbn: String): String` | 获取 ISBN 摘要 |

### 扩展函数

```kotlin
// 快速验证
fun String.isValidISBN(): Boolean

// 快速格式化
fun String.formatISBN(): String

// 快速解析
fun String.parseISBN(): ISBNInfo
```

## 数据类

### ISBNType

```kotlin
enum class ISBNType {
    ISBN_10,   // 10 位 ISBN
    ISBN_13,   // 13 位 ISBN
    INVALID    // 无效 ISBN
}
```

### ISBNInfo

```kotlin
data class ISBNInfo(
    val type: ISBNType,           // ISBN 类型
    val original: String,         // 原始输入
    val formatted: String,        // 格式化后
    val isValid: Boolean,         // 是否有效
    val prefix: String?,          // GS1 前缀 (978/979)
    val registrationGroup: String?, // 注册组代码
    val registrant: String?,      // 出版者代码
    val publication: String?,     // 出版物代码
    val checkDigit: Char?,        // 校验位
    val isbn10: String?,          // ISBN-10 格式
    val isbn13: String?          // ISBN-13 格式
)
```

## 校验位算法

### ISBN-10

校验位计算使用模 11 加权算法：

```
sum = d₁×10 + d₂×9 + d₃×8 + d₄×7 + d₅×6 + d₆×5 + d₇×4 + d₈×3 + d₉×2
checkDigit = (11 - (sum % 11)) % 11
```

如果校验位为 10，则用 'X' 表示。

### ISBN-13

校验位计算使用模 10 加权算法：

```
sum = d₁×1 + d₂×3 + d₃×1 + d₄×3 + d₅×1 + d₆×3 + d₇×1 + d₈×3 + d₉×1 + d₁₀×3 + d₁₁×1 + d₁₂×3
checkDigit = (10 - (sum % 10)) % 10
```

## 支持的注册组

工具内置了常见国家和地区的注册组代码，包括：

- 英语区（0, 1）
- 法语区（2）
- 德语区（3）
- 日本（4）
- 俄语区（5）
- 中国（7）
- 以及其他 100+ 个国家/地区

## 常见用途

### 图书库存管理

```kotlin
// 检查 ISBN 有效性并标准化
val normalizedISBN = if (isbn.isValidISBN()) {
    ISBNUtils.convertToISBN13(ISBNUtils.cleanISBN(isbn))
} else {
    null
}
```

### 数据清洗

```kotlin
// 从杂乱数据中提取并验证 ISBN
val cleanISBNS = rawTexts
    .flatMap { ISBNUtils.extractFromText(it) }
    .distinct()
    .filter { ISBNUtils.validate(it) }
```

### 去重检测

```kotlin
// 使用 ISBN-13 作为唯一标识
val uniqueBooks = books
    .groupBy { ISBNUtils.convertToISBN13(it.isbn) ?: it.isbn }
    .values
```

## 性能

- 验证操作：O(n)，n 为 ISBN 长度
- 转换操作：O(n)
- 批量验证：使用关联映射优化，O(m)，m 为 ISBN 数量

## 测试

运行测试：

```bash
kotlinc -script ISBNUtilsTest.kt
```

或使用 Gradle：

```bash
./gradlew test
```

## 许可证

MIT License

## 相关标准

- [ISO 2108](https://www.iso.org/standard/36563.html) - ISBN 国际标准
- [ISBN 用户手册](https://www.isbn-international.org/content/isbn-users-manual)