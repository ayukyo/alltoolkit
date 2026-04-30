# Base64 Utils - Lua Base64 编码/解码工具库

零外部依赖的纯 Lua Base64 工具库，支持标准 Base64 和 URL 安全格式。

## 功能特性

- **标准 Base64 编码/解码** - 符合 RFC 4648 规范
- **URL 安全格式** - 无 padding，使用 `-` 和 `_` 替代 `+` 和 `/`
- **Base64 验证** - 检查字符串是否为有效的 Base64 格式
- **编码统计** - 获取编码后的开销、大小等信息
- **表格编解码** - 将 Lua 表格编码为 Base64 JSON 格式

## 文件结构

```
base64_utils/
├── mod.lua              # 主模块文件
├── base64_utils_test.lua # 测试文件
├── README.md            # 说明文档
└── examples/
    └── usage_examples.lua # 使用示例
```

## API 参考

### 编码函数

#### `base64_utils.encode(data, urlsafe)`
将字符串编码为 Base64 格式。

- `data` - 要编码的字符串
- `urlsafe` - 是否使用 URL 安全格式（可选，默认 false）
- 返回：Base64 编码字符串

```lua
local encoded = base64.encode("Hello World")
-- 结果: "SGVsbG8gV29ybGQ="
```

#### `base64_utils.encode_urlsafe(data)`
编码为 URL 安全的 Base64 格式（无 padding）。

```lua
local encoded = base64.encode_urlsafe("Hello World")
-- 结果: "SGVsbG8gV29ybGQ"
```

### 解码函数

#### `base64_utils.decode(encoded, urlsafe)`
解码 Base64 字符串。

- `encoded` - Base64 编码的字符串
- `urlsafe` - 是否为 URL 安全格式（可选，自动检测）
- 返回：解码后的原始数据, 错误信息（如有）

```lua
local decoded, err = base64.decode("SGVsbG8gV29ybGQ=")
-- decoded = "Hello World", err = nil
```

#### `base64_utils.decode_urlsafe(encoded)`
解码 URL 安全的 Base64 字符串。

```lua
local decoded, err = base64.decode_urlsafe("SGVsbG8gV29ybGQ")
-- decoded = "Hello World"
```

### 验证函数

#### `base64_utils.is_valid(str, urlsafe)`
验证字符串是否为有效的 Base64 格式。

```lua
local valid = base64.is_valid("SGVsbG8gV29ybGQ=")
-- valid = true

local valid = base64.is_valid("SGVs###G8=")
-- valid = false
```

### 统计函数

#### `base64_utils.get_encode_stats(data, urlsafe)`
获取编码统计信息。

返回表格包含：
- `original_size` - 原始数据大小
- `encoded_size` - 编码后大小
- `overhead_bytes` - 编码开销字节数
- `overhead_percent` - 编码开销百分比
- `padding_count` - padding 数量
- `is_urlsafe` - 是否使用 URL 安全格式

```lua
local stats = base64.get_encode_stats("Hello")
-- stats.original_size = 5
-- stats.encoded_size = 8
-- stats.padding_count = 1
```

### 表格编解码

#### `base64_utils.encode_table(tbl)`
将 Lua 表格编码为 Base64 JSON 格式。

```lua
local config = { name = "test", value = 123 }
local encoded, err = base64.encode_table(config)
-- encoded = Base64 编码的 JSON 字符串
```

#### `base64_utils.decode_table(encoded)`
解码 Base64 JSON 为 Lua 表格。

```lua
local tbl, err = base64.decode_table(encoded)
-- tbl = { name = "test", value = 123 }
```

## 使用示例

```lua
local base64 = require("mod")

-- 基本编解码
local encoded = base64.encode("你好世界")
local decoded, _ = base64.decode(encoded)
print(decoded)  -- 输出: 你好世界

-- URL 安全格式（适合 URL 参数）
local url_encoded = base64.encode_urlsafe("user@example.com")
print(url_encoded)  -- 无 padding，可直接用于 URL

-- 表格编解码（可用于简单 Token）
local token_data = { user = "alice", time = os.time() }
local token = base64.encode_table(token_data)
print("Token: " .. token)
```

## 测试

运行测试：

```bash
cd Lua/base64_utils
lua base64_utils_test.lua
```

测试覆盖：
- RFC 4648 标准测试向量
- 中文编码
- URL 安全格式
- 二进制数据
- 边界情况
- 错误处理

## 特点

- **零外部依赖** - 纯 Lua 实现，无需任何库
- **完整测试** - 35+ 测试用例覆盖各种场景
- **错误处理** - 所有函数都有参数验证和错误返回
- **灵活解码** - 自动检测 URL 安全格式，自动处理空白字符
- **表格支持** - 内置 JSON 序列化/解析（零依赖）

## 适用场景

- Web API 数据编码
- URL 参数传输
- 简单认证 Token
- 配置文件编码存储
- 二进制数据文本化