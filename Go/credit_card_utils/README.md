# Credit Card Utils (Go)

信用卡工具模块，提供信用卡号验证、类型识别、格式化和测试卡号生成功能。零外部依赖，仅使用 Go 标准库。

## 功能特性

- **Luhn 算法验证** - 验证信用卡号的有效性
- **卡类型识别** - 支持 Visa、Mastercard、Amex、Discover、JCB、Diners Club、UnionPay、Maestro
- **卡号格式化** - 标准格式和自定义分组
- **卡号掩码** - 安全显示卡号
- **CVV 验证** - 根据卡类型验证 CVV 长度
- **有效期验证** - 验证和解析有效期
- **测试卡号生成** - 生成通过 Luhn 检查的测试卡号
- **IIN 解析** - 获取发卡行识别号
- **完整验证** - 一次性验证卡号、CVV 和有效期

## 快速开始

```go
package main

import (
    "fmt"
    creditcard "github.com/ayukyo/alltoolkit/Go/credit_card_utils"
)

func main() {
    // 验证卡号
    isValid := creditcard.LuhnCheck("4111111111111111")
    fmt.Println("Valid:", isValid) // true

    // 识别卡类型
    cardType := creditcard.IdentifyCardType("4111111111111111")
    fmt.Println("Type:", cardType) // Visa

    // 格式化卡号
    formatted := creditcard.FormatCardNumber("4111111111111111")
    fmt.Println("Formatted:", formatted) // "4111 1111 1111 1111"

    // 获取卡信息
    info := creditcard.GetCardInfo("4111111111111111")
    fmt.Printf("Type: %s, CVV Length: %d\n", info.Type, info.CVVLength)
}
```

## API 文档

### Luhn 算法

```go
// 验证卡号是否通过 Luhn 检查
LuhnCheck(number string) bool

// 计算 Luhn 校验位
CalculateLuhnDigit(number string) int
```

### 卡号处理

```go
// 清理卡号（移除非数字字符）
CleanCardNumber(number string) string

// 格式化卡号（4位一组）
FormatCardNumber(number string) string

// 自定义格式化
FormatCardNumberCustom(number string, groups []int) string

// 掩码卡号
MaskCardNumber(number string, showFirst, showLast int) string
MaskCardNumberDefault(number string) string // 显示前4后4
```

### 卡类型识别

```go
// 识别卡类型
IdentifyCardType(number string) CardType

// 获取详细信息
GetCardInfo(number string) CardInfo

// 检查卡号是否有效（Luhn + 长度）
IsValidCardNumber(number string) bool

// 获取预期长度
GetExpectedLengths(cardType CardType) []int

// 获取 CVV 长度
GetCVVLength(cardType CardType) int
```

### CVV 验证

```go
// 验证 CVV
IsValidCVV(cvv string, cardType CardType) bool
IsValidCVVForNumber(cvv, number string) bool
```

### 有效期验证

```go
// 解析有效期
ParseExpiryDate(expiry string) (year, month int, err error)

// 验证有效期
IsValidExpiryDate(expiry string) bool

// 检查是否过期
IsExpired(expiry string) bool

// 格式化有效期
FormatExpiryDate(expiry string) string
```

### 测试卡号生成

```go
// 生成测试卡号
GenerateTestCardNumber(cardType CardType) string

// 生成完整测试卡（卡号、CVV、有效期）
GenerateTestCard(cardType CardType) (number, cvv, expiry string)
```

### 完整验证

```go
// 验证卡号、CVV、有效期
ValidateCard(number, cvv, expiry string) ValidationResult
```

## 支持的卡类型

| 卡类型 | 前缀 | 长度 | CVV长度 |
|--------|------|------|---------|
| Visa | 4 | 13, 16, 19 | 3 |
| Mastercard | 51-55, 2221-2720 | 16 | 3 |
| American Express | 34, 37 | 15 | 4 |
| Discover | 6011, 65, 644-649 | 16, 19 | 3 |
| JCB | 35 | 16 | 3 |
| Diners Club | 300-305, 36, 38-39 | 14, 16, 19 | 3 |
| UnionPay | 62, 81 | 16-19 | 3 |
| Maestro | 5018, 5020, 5038, etc. | 12-19 | 3 |

## 示例

运行示例：

```bash
cd examples
go run main.go
```

## 测试

```bash
go test -v
```

## 注意事项

⚠️ **重要**: 
- 此模块仅用于验证卡号格式，不能验证卡号是否真实存在或可用
- 生成的测试卡号仅用于开发和测试，不可用于实际交易
- 生产环境支付处理应使用专业支付网关（如 Stripe、PayPal 等）

## 许可证

MIT License