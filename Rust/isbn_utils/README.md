# ISBN Utils

ISBN-10 和 ISBN-13 工具库，用于验证、生成、格式化和转换 ISBN 编码。

## 功能特性

- ✅ 验证 ISBN-10 和 ISBN-13
- ✅ 生成随机有效 ISBN
- ✅ 格式化 ISBN（添加连字符）
- ✅ ISBN-10 与 ISBN-13 互相转换
- ✅ 零外部依赖（纯 Rust 实现）

## 安装

在 `Cargo.toml` 中添加：

```toml
[dependencies]
isbn_utils = { path = "." }
```

## 使用方法

### 验证 ISBN

```rust
use isbn_utils::validate;

// 验证 ISBN-10
let isbn = validate("0-306-40615-2").unwrap();
assert!(isbn.is_valid());

// 验证 ISBN-13
let isbn = validate("978-0-306-40615-7").unwrap();
assert!(isbn.is_valid());

// 支持 X 校验位
let isbn = validate("0-8044-2957-X").unwrap();
assert!(isbn.is_valid());
```

### 格式化 ISBN

```rust
use isbn_utils::validate;

let isbn = validate("0306406152").unwrap();
println!("{}", isbn.format()); // 输出: 0-3064-0615-2
```

### ISBN-10 与 ISBN-13 转换

```rust
use isbn_utils::validate;

// ISBN-10 转 ISBN-13
let isbn10 = validate("0306406152").unwrap();
let isbn13 = isbn10.to_isbn13();
println!("{}", isbn13); // 输出: 9780306406157

// ISBN-13 转 ISBN-10（仅限 978 前缀）
let isbn13 = validate("9780306406157").unwrap();
let isbn10 = isbn13.to_isbn10().unwrap();
println!("{}", isbn10); // 输出: 0306406152
```

### 生成随机 ISBN

```rust
use isbn_utils::{generate_isbn10, generate_isbn13};

let isbn10 = generate_isbn10();
println!("Random ISBN-10: {}", isbn10);

let isbn13 = generate_isbn13();
println!("Random ISBN-13: {}", isbn13);
```

### 使用 ISBN10 和 ISBN13 类型

```rust
use isbn_utils::{ISBN10, ISBN13};
use std::str::FromStr;

// 直接创建
let isbn10 = ISBN10::from_str("0306406152").unwrap();
let isbn13 = ISBN13::from_str("9780306406157").unwrap();

// 检查注册组
println!("Registration group: {}", isbn10.registration_group());
```

## 运行示例

```bash
cargo run --example basic_usage
```

## 运行测试

```bash
cargo test
```

## API 参考

### `validate(s: &str) -> Result<ISBN, ISBNError>`

验证并解析 ISBN 字符串。

### `generate_isbn10() -> ISBN10`

生成随机有效的 ISBN-10。

### `generate_isbn13() -> ISBN13`

生成随机有效的 ISBN-13（978 前缀）。

### `ISBN`

枚举类型，可以是 `ISBN10` 或 `ISBN13`。

### `ISBN10`

- `is_valid()` - 检查有效性
- `digits()` - 获取数字字符串
- `format()` - 格式化输出
- `to_isbn13()` - 转换为 ISBN-13
- `registration_group()` - 获取注册组信息

### `ISBN13`

- `is_valid()` - 检查有效性
- `digits()` - 获取数字字符串
- `format()` - 格式化输出
- `to_isbn10()` - 转换为 ISBN-10（仅 978 前缀）
- `prefix()` - 获取前缀（978 或 979）
- `registration_group()` - 获取注册组信息

## 校验算法

### ISBN-10 校验

使用加权和模 11 算法：
```
checksum = (11 - (Σ digit_i * (10-i)) mod 11) mod 11
```
如果校验位为 10，则用 'X' 表示。

### ISBN-13 校验

使用 GS1 模 10 算法：
```
checksum = (10 - (Σ weight_i * digit_i) mod 10) mod 10
```
其中奇数位权重为 1，偶数位权重为 3。

## 许可证

MIT License