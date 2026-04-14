# env_utils - Rust 环境变量工具库

一个零外部依赖的 Rust 环境变量管理工具库。

## 功能特性

- 📁 从 `.env` 文件加载环境变量
- 🔢 支持多种类型解析：String, i32, i64, u32, u64, usize, f32, f64, bool
- ✅ 支持默认值
- ⚠️ 验证必需的环境变量
- 📋 解析列表类型（逗号分隔）
- 🗺️ 解析键值对映射
- 🛠️ 设置和删除环境变量
- 📚 获取所有环境变量

## 安装

将以下内容添加到 `Cargo.toml`:

```toml
[dependencies.env_utils]
path = "./env_utils"
```

或者直接复制 `mod.rs` 到你的项目中。

## 快速开始

```rust
use env_utils::{get_env, get_env_or, require_env, load_dotenv, set_env, has_env};

fn main() {
    // 从 .env 文件加载
    load_dotenv().ok();
    
    // 获取字符串
    let host: String = get_env_or("HOST", "localhost".to_string());
    
    // 获取数字
    let port: u16 = get_env_or("PORT", 3000);
    
    // 获取布尔值
    let debug: bool = get_env_or("DEBUG", false);
    
    // 获取必需的环境变量
    let db_url: String = require_env("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    
    // 检查是否存在
    if has_env("API_KEY") {
        println!("API Key is configured");
    }
    
    // 设置环境变量
    set_env("APP_ENV", "production");
}
```

## API 参考

### 加载 .env 文件

```rust
// 从当前目录加载 .env
load_dotenv()?;

// 从指定路径加载
load_dotenv_from_path("/path/to/.env")?;
```

`.env` 文件格式：
```env
# 注释
DATABASE_URL=postgres://localhost/mydb
PORT=8080
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 获取环境变量

```rust
// 获取可选值
let value: Option<String> = get_env("KEY");

// 获取带默认值
let port: u16 = get_env_or("PORT", 3000);
let host: String = get_env_or("HOST", "localhost".to_string());

// 获取必需值（失败返回错误）
let url: String = require_env("DATABASE_URL")?;
```

### 类型转换

支持的类型：
- `String` - 字符串
- `i32`, `i64` - 有符号整数
- `u32`, `u64`, `usize` - 无符号整数
- `f32`, `f64` - 浮点数
- `bool` - 布尔值（支持 "true", "false", "1", "0", "yes", "no", "on", "off"）

```rust
let timeout: u64 = get_env_or("TIMEOUT", 30);
let rate: f64 = get_env_or("RATE", 0.5);
let enabled: bool = get_env_or("FEATURE_ENABLED", false);
```

### 列表和映射

```rust
// 解析逗号分隔列表
// ALLOWED_HOSTS=localhost,127.0.0.1,example.com
let hosts: Vec<String> = get_env_list("ALLOWED_HOSTS").unwrap_or_default();

// 解析键值对映射
// CONFIG=debug=true,timeout=30,retries=3
let config: HashMap<String, String> = get_env_map("CONFIG").unwrap_or_default();
```

### 验证和设置

```rust
// 验证必需的环境变量
let missing = validate_required(&["DATABASE_URL", "API_KEY", "SECRET_KEY"]);
if !missing.is_empty() {
    panic!("Missing required env vars: {:?}", missing);
}

// 设置环境变量
set_env("APP_ENV", "production");

// 删除环境变量
remove_env("TEMP_VAR");

// 检查是否存在
if has_env("FEATURE_FLAG") {
    // ...
}

// 获取所有环境变量
let all_env: HashMap<String, String> = get_all_env();
```

## 错误处理

```rust
use env_utils::{require_env, EnvError};

match require_env::<String>("DATABASE_URL") {
    Ok(url) => println!("Database URL: {}", url),
    Err(EnvError::NotFound(key)) => eprintln!("Variable {} not found", key),
    Err(EnvError::ParseError { key, value, expected_type }) => {
        eprintln!("Failed to parse '{}' as {} for key {}", value, expected_type, key);
    }
    Err(EnvError::DotEnvError(msg)) => eprintln!("DotEnv error: {}", msg),
}
```

## 示例

查看 `examples/` 目录获取更多示例：

- `basic.rs` - 基本用法
- `dotenv.rs` - .env 文件加载
- `validation.rs` - 环境变量验证

## 许可证

MIT License