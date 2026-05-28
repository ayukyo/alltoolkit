# credit_card_utils

零外部依赖的信用卡工具库，提供完整的信用卡号验证、品牌识别和格式化功能。

## 功能特性

- ✅ **Luhn 算法验证** - 完整的 Luhn 校验算法实现
- ✅ **卡品牌识别** - 支持 10+ 种主流信用卡品牌
- ✅ **卡号格式化** - 按品牌标准格式化显示
- ✅ **卡号掩码** - 安全隐藏敏感信息
- ✅ **BIN/IIN 提取** - 获取银行卡识别码
- ✅ **有效期验证** - MM/YY 或 MM/YYYY 格式
- ✅ **CVV 验证** - 按品牌验证安全码长度
- ✅ **测试卡号检测** - 识别常用测试卡号
- ✅ **测试卡号生成** - 生成符合 Luhn 的测试卡号

## 支持的卡品牌

| 品牌 | 前缀 | 卡号长度 |
|------|------|----------|
| Visa | 4 | 13, 16, 19 |
| MasterCard | 51-55, 2221-2720 | 16 |
| American Express | 34, 37 | 15 |
| Discover | 6011, 622126-622925, 644-649, 65 | 16-19 |
| JCB | 3528-3589 | 16 |
| Diners Club | 300-305, 36, 38, 39 | 14 |
| UnionPay (银联) | 62 | 16-19 |
| Maestro | 5018, 5020, 5038, 5893, 6304, 6759, 6761-6763 | 12-19 |
| Elo | 特定 BIN | 16 |
| Mir (俄罗斯) | 2200-2204 | 16 |

## 使用方法

### 基本验证

```rust
use credit_card_utils::*;

// 创建信用卡实例
let card = CreditCard::new("4111111111111111");

// 获取基本信息
println!("品牌: {}", card.brand());      // Visa
println!("有效: {}", card.is_valid());    // true
println!("长度: {}", card.length());      // 16

// 格式化显示
println!("格式化: {}", card.format());    // 4111 1111 1111 1111

// 掩码处理
println!("掩码(后4位): {}", card.mask_last4());  // ************1111
println!("掩码(中间): {}", card.mask_middle());  // 4111********1111

// 获取 BIN
println!("BIN: {}", card.bin().unwrap()); // 411111

// 检测测试卡
if card.is_test_card() {
    println!("警告: 这是一个测试卡号!");
}
```

### 详细验证

```rust
use credit_card_utils::*;

// 使用验证器获取详细结果
let result = CreditCardValidator::validate("4111111111111111");

println!("有效: {}", result.valid);
println!("品牌: {}", result.brand);
println!("格式化: {}", result.formatted);

if !result.errors.is_empty() {
    println!("错误: {:?}", result.errors);
}

if !result.warnings.is_empty() {
    println!("警告: {:?}", result.warnings);
}
```

### 有效期和 CVV 验证

```rust
use credit_card_utils::*;

// 验证有效期
let valid = CreditCardValidator::validate_expiry("12/25");
println!("有效期: {}", valid); // true

// 验证 CVV (Visa 需要 3 位，Amex 需要 4 位)
let cvv_valid = CreditCardValidator::validate_cvv("123", CardBrand::Visa);
println!("CVV 有效: {}", cvv_valid); // true

let amex_cvv = CreditCardValidator::validate_cvv("1234", CardBrand::Amex);
println!("Amex CVV 有效: {}", amex_cvv); // true
```

### Luhn 算法

```rust
use credit_card_utils::*;

// 单独执行 Luhn 校验
let valid = CreditCardValidator::check_luhn("4111111111111111");
println!("Luhn 有效: {}", valid); // true
```

### 生成测试卡号

```rust
use credit_card_utils::*;

// 生成符合 Luhn 的测试卡号
let visa = CreditCardGenerator::generate_visa();
let mc = CreditCardGenerator::generate_mastercard();
let amex = CreditCardGenerator::generate_amex();
let discover = CreditCardGenerator::generate_discover();

println!("Visa: {}", visa);
println!("MasterCard: {}", mc);
println!("Amex: {}", amex);
println!("Discover: {}", discover);
```

### 卡品牌检测

```rust
use credit_card_utils::*;

// 单独检测卡品牌
let brand = CreditCardValidator::detect_brand("4111111111111111");
println!("品牌: {}", brand); // Visa
```

## API 参考

### CreditCard

主要信用卡结构体，提供卡号验证和格式化功能。

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `new(number: &str)` | `Self` | 创建实例，自动清理格式 |
| `number()` | `&str` | 获取纯净卡号 |
| `brand()` | `CardBrand` | 获取卡品牌 |
| `is_valid()` | `bool` | 检查是否有效 |
| `length()` | `usize` | 获取卡号长度 |
| `format()` | `String` | 格式化显示 |
| `mask_last4()` | `String` | 掩码后4位 |
| `mask_middle()` | `String` | 掩码中间 |
| `bin()` | `Option<&str>` | 获取 BIN/IIN |
| `is_test_card()` | `bool` | 检测测试卡 |

### CreditCardValidator

验证器，提供详细验证结果。

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `validate(number: &str)` | `ValidationResult` | 完整验证 |
| `check_luhn(number: &str)` | `bool` | Luhn 校验 |
| `detect_brand(number: &str)` | `CardBrand` | 品牌检测 |
| `validate_expiry(expiry: &str)` | `bool` | 有效期验证 |
| `validate_cvv(cvv: &str, brand: CardBrand)` | `bool` | CVV 验证 |

### CreditCardGenerator

测试卡号生成器（仅用于测试）。

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `generate_visa()` | `String` | 生成 Visa 测试卡 |
| `generate_mastercard()` | `String` | 生成 MasterCard 测试卡 |
| `generate_amex()` | `String` | 生成 Amex 测试卡 |
| `generate_discover()` | `String` | 生成 Discover 测试卡 |

### CardBrand

信用卡品牌枚举。

```rust
pub enum CardBrand {
    Visa,
    MasterCard,
    Amex,
    Discover,
    Jcb,
    DinersClub,
    UnionPay,
    Maestro,
    Elo,
    Mir,
    Unknown,
}
```

## 运行示例

```bash
cd Rust/credit_card_utils
cargo run --example demo
```

## 运行测试

```bash
cd Rust/credit_card_utils
cargo test
```

## 安全提示

⚠️ **重要**: 此库仅用于卡号格式验证，不处理实际支付或存储敏感数据。

- 永远不要在不安全的环境中记录或传输完整卡号
- 生产环境请使用 PCI DSS 认证的支付处理服务
- 测试卡号仅用于开发环境

## 许可证

MIT License