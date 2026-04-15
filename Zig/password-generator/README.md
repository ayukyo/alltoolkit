# Password Generator - Zig

一个功能完整的密码生成器模块，使用纯 Zig 实现，无外部依赖。

## 特性

- 🔐 **密码生成** - 可配置长度和字符集
- 🔢 **PIN 码生成** - 纯数字验证码
- 📝 **短语密码** - 易记的单词组合密码
- 📊 **强度分析** - 密码安全评分和熵计算
- 🔍 **模式检测** - 识别常见弱密码模式
- 🎲 **加密安全** - 使用 `std.crypto.random` 生成

## 快速开始

```zig
const std = @import("std");
const password_generator = @import("password-generator");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    // 生成默认密码 (16位，字母+数字)
    const password = try password_generator.generate(allocator, .{});
    defer allocator.free(password);
    std.debug.print("Password: {s}\n", .{password});
}
```

## API 文档

### 生成密码

```zig
const options = password_generator.PasswordOptions{
    .length = 20,                    // 密码长度
    .include_lowercase = true,       // 包含小写字母
    .include_uppercase = true,       // 包含大写字母
    .include_digits = true,          // 包含数字
    .include_symbols = true,         // 包含符号
    .exclude_similar = false,        // 排除相似字符 (i, l, 1, L, o, O, 0)
    .custom_charset = null,          // 自定义字符集
};

const password = try password_generator.generate(allocator, options);
```

### 生成多个密码

```zig
const passwords = try password_generator.generateMultiple(allocator, 5, .{
    .length = 12,
    .include_symbols = true,
});
defer {
    for (passwords) |pwd| allocator.free(pwd);
    allocator.free(passwords);
}
```

### 生成 PIN 码

```zig
const pin = try password_generator.generatePin(allocator, 6);
defer allocator.free(pin);
// 输出: "384729"
```

### 生成短语密码

```zig
const passphrase = try password_generator.generatePassphrase(allocator, 4, "-");
defer allocator.free(passphrase);
// 输出: "forest-eagle-river-tiger"
```

### 分析密码强度

```zig
const analysis = password_generator.analyze("MyP@ssw0rd!2024");

std.debug.print("Score: {}/100\n", .{analysis.score});
std.debug.print("Rating: {s}\n", .{analysis.rating});
std.debug.print("Entropy: {d:.2} bits\n", .{analysis.entropy});
std.debug.print("Has lowercase: {}\n", .{analysis.has_lowercase});
std.debug.print("Has uppercase: {}\n", .{analysis.has_uppercase});
std.debug.print("Has digits: {}\n", .{analysis.has_digits});
std.debug.print("Has symbols: {}\n", .{analysis.has_symbols});
```

### 检测常见模式

```zig
const has_pattern = password_generator.hasCommonPatterns("abc123");
// 返回 true (存在连续字符)
```

## 字符集常量

```zig
const CharSets = password_generator.CharSets;

CharSets.lowercase  // "abcdefghijklmnopqrstuvwxyz"
CharSets.uppercase  // "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CharSets.digits     // "0123456789"
CharSets.symbols    // "!@#$%^&*()_+-=[]{}|;:,.<>?"
CharSets.similar    // "il1Lo0O"
```

## 密码强度评分

| 评分范围 | 等级 |
|---------|------|
| 80-100  | Very Strong |
| 60-79   | Strong |
| 40-59   | Moderate |
| 20-39   | Weak |
| 0-19    | Very Weak |

评分依据:
- 长度 (最多 40 分): 6-8字符 24分, 12+字符 32分, 16+字符 40分
- 多样性 (最多 40 分): 每种字符类型 10 分
- 熵值加成 (最多 20 分): 基于信息熵计算

## 构建

```bash
# 构建库
zig build

# 运行测试
zig build test

# 运行示例
zig build run
```

## 依赖

- Zig 0.11.0+
- 标准库 (`std.crypto.random`)

## 许可证

MIT License