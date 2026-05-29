# Credit Card Utils

信用卡验证、格式化和识别工具库。

## 功能特性

- ✅ **卡类型识别** - 自动识别 Visa、MasterCard、Amex、Discover、JCB、Diners Club、UnionPay、Maestro
- ✅ **Luhn 算法验证** - 完整实现 Luhn 校验和算法
- ✅ **格式化** - 自动根据卡类型格式化卡号（Visa 4-4-4-4，Amex 4-6-5）
- ✅ **脱敏处理** - 安全显示卡号，支持自定义可见位数
- ✅ **发卡行识别** - 根据 IIN/BIN 识别发卡机构
- ✅ **有效期验证** - 检查卡片是否过期
- ✅ **CVV 验证** - 根据卡类型验证 CVV 长度
- ✅ **测试卡号生成** - 生成有效测试卡号
- ✅ **零外部依赖** - 纯 Swift 实现

## 使用方法

### 1. 卡类型识别

```swift
let type = CreditCardUtils.detectCardType("4242424242424242")
// type == .visa

let type2 = CreditCardUtils.detectCardType("5555555555554444")
// type2 == .mastercard
```

### 2. 验证卡号

```swift
// 简单验证
if CreditCardUtils.isValid("4242424242424242") {
    print("Valid card!")
}

// 详细验证
let result = CreditCardUtils.validate("4242424242424241")
if !result.isValid {
    for error in result.errors {
        print(error.rawValue) // "Card number fails Luhn checksum validation"
    }
}

// 完整验证（含有效期和 CVV）
let fullResult = CreditCardUtils.validateFull(
    cardNumber: "4242424242424242",
    expiryMonth: 12,
    expiryYear: 2025,
    cvv: "123"
)
```

### 3. 格式化卡号

```swift
// 自动格式化
let formatted = CreditCardUtils.format("4242424242424242")
// "4242-4242-4242-4242"

// Amex 使用不同格式
let amex = CreditCardUtils.format("378282246310005")
// "3782-822463-10005"

// 自定义分隔符
let withSpaces = CreditCardUtils.format("4242424242424242", separator: " ")
// "4242 4242 4242 4242"
```

### 4. 脱敏处理

```swift
// 默认脱敏（显示前6后4）
let masked = CreditCardUtils.mask("4242424242424242")
// "424242****4242"

// 自定义可见范围
let custom = CreditCardUtils.mask("4242424242424242", visiblePrefix: 4, visibleSuffix: 4)
// "4242********4242"

// 仅显示后4位
let last4 = CreditCardUtils.mask("4242424242424242", visiblePrefix: 0, visibleSuffix: 4)
// "************4242"

// 获取后4位
let digits = CreditCardUtils.lastFour("4242424242424242")
// "4242"
```

### 5. 完整分析

```swift
let info = CreditCardUtils.analyze("4242424242424242")
// info.type == .visa
// info.isValid == true
// info.formattedNumber == "4242-4242-4242-4242"
// info.maskedNumber == "424242****4242"
// info.lastFourDigits == "4242"
// info.issuer == "Visa"
```

### 6. Luhn 算法

```swift
// 验证 Luhn 校验
if CreditCardUtils.luhnCheck("4242424242424242") {
    print("Passes Luhn check!")
}

// 生成校验位
let checksum = CreditCardUtils.generateLuhnChecksum("424242424242424")
// checksum == 2
```

### 7. 有效期验证

```swift
let expiry = CreditCardUtils.validateExpiry(month: 12, year: 2025)
if expiry.isValid {
    print("Card not expired")
}

// 含过期状态分析
let info = CreditCardUtils.analyzeWithExpiry("4242424242424242", expiryMonth: 12, expiryYear: 2025)
// info.isExpired == false
```

### 8. CVV 验证

```swift
// Visa/MasterCard 需要 3 位 CVV
let visaCVV = CreditCardUtils.validateCVV(cvv: "123", for: .visa)
// valid

// Amex 需要 4 位 CVV
let amexCVV = CreditCardUtils.validateCVV(cvv: "1234", for: .amex)
// valid
```

### 9. String 扩展

```swift
let card = "4242424242424242"

card.isValidCreditCard     // true
card.creditCardType        // .visa
card.formattedCreditCard   // "4242-4242-4242-4242"
card.maskedCreditCard      // "424242****4242"
```

### 10. 测试卡号生成

```swift
// 生成有效测试卡号
let testVisa = CreditCardUtils.generateTestNumber(for: .visa)
let testAmex = CreditCardUtils.generateTestNumber(for: .amex)
let testMC = CreditCardUtils.generateTestNumber(for: .mastercard)
```

## 支持的卡类型

| 卡类型 | IIN 范围 | 卡号长度 | CVV 长度 |
|--------|----------|----------|----------|
| Visa | 4 | 13-16 | 3 |
| MasterCard | 51-55, 2221-2720 | 16 | 3 |
| American Express | 34, 37 | 15 | 4 |
| Discover | 6011, 644-649, 65 | 16-19 | 3 |
| JCB | 3528-3589 | 16 | 3 |
| Diners Club | 300-305, 36-38 | 14-19 | 3 |
| UnionPay | 62, 81 | 16-19 | 3 |
| Maestro | 5018, 5020, 5038, etc. | 12-19 | 3 |

## 文件结构

```
credit_card_utils/
├── credit_card_utils.swift        # 主模块
├── credit_card_utils_tests.swift  # 单元测试
├── examples.swift                 # 使用示例
└── README.md                      # 说明文档
```

## 测试

```bash
# 使用 Swift 测试
swift test

# 或运行示例
swift run examples.swift
```

## 注意事项

⚠️ **安全提示**：
- 本库仅用于格式化和验证，不存储或传输卡号
- 生产环境应使用 PCI DSS 认证的服务处理支付
- 测试卡号仅用于开发测试，不可用于真实交易

## 许可证

MIT License