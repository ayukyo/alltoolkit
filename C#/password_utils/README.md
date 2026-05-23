# PasswordUtils - C# 密码工具模块

全面的密码强度检查、生成和分析工具。零外部依赖，仅使用 .NET 标准库。

## 功能特性

### 🔒 密码强度分析
- 基于熵的强度计算
- 字符集分析（大小写、数字、特殊字符）
- 破解时间估算
- 智能改进建议
- 键盘模式检测（如 qwerty）
- 重复字符检测
- 顺序字符检测（如 abc、123）

### 🔐 密码生成
- 自定义长度
- 字符类型选择（大小写、数字、特殊字符）
- 排除易混淆字符（如 l, 1, I, O, 0）
- 自定义字符集
- 批量生成
- 安全随机（使用 `RandomNumberGenerator`）

### 📝 密码短语生成
- 基于单词的易记密码
- 自定义单词数量
- 自定义分隔符
- 大写选项
- 随机数字插入

### ✅ 策略验证
- 最小长度要求
- 字符类型要求
- 可自定义策略
- 详细错误信息

### 🔍 其他功能
- 常见密码检测
- 熵值计算
- 密码评分（1-5）
- 常见密码黑名单

## 文件结构

```
C#/password_utils/
├── PasswordUtils.cs          # 主模块（核心实现）
├── PasswordUtilsTest.cs      # 测试套件
├── README.md                 # 本文档
└── examples/
    └── UsageExample.cs       # 使用示例
```

## 快速开始

### 编译

```bash
# 编译主模块
csc -target:library -out:PasswordUtils.dll PasswordUtils.cs

# 编译并运行测试
csc -out:PasswordUtilsTest.exe PasswordUtils.cs PasswordUtilsTest.cs
./PasswordUtilsTest.exe

# 编译并运行示例
csc -out:UsageExample.exe PasswordUtils.cs examples/UsageExample.cs
./UsageExample.exe
```

### 使用 .NET CLI

```bash
# 创建项目
dotnet new classlib -n PasswordUtils

# 复制 PasswordUtils.cs 到项目
# 添加测试项目
dotnet new xunit -n PasswordUtils.Tests

# 运行
dotnet run
```

## API 文档

### PasswordUtils.AnalyzeStrength(password)

分析密码强度，返回详细信息。

```csharp
var analysis = PasswordUtils.AnalyzeStrength("MyP@ssw0rd!");

Console.WriteLine($"强度: {analysis.Strength}");        // VeryStrong
Console.WriteLine($"得分: {analysis.Score}/100");       // 85
Console.WriteLine($"熵值: {analysis.Entropy} bits");   // 76.5
Console.WriteLine($"破解时间: {analysis.CrackTimeDisplay}"); // Centuries+
Console.WriteLine($"包含小写: {analysis.HasLowercase}"); // true
Console.WriteLine($"包含大写: {analysis.HasUppercase}"); // true
Console.WriteLine($"包含数字: {analysis.HasDigits}");   // true
Console.WriteLine($"包含特殊: {analysis.HasSpecialChars}"); // true

foreach (var suggestion in analysis.Suggestions)
{
    Console.WriteLine($"建议: {suggestion}");
}
```

### PasswordUtils.Generate(options)

生成安全随机密码。

```csharp
// 默认生成（16字符，包含所有字符类型）
var password = PasswordUtils.Generate();

// 自定义选项
var options = new PasswordOptions
{
    Length = 24,
    IncludeLowercase = true,
    IncludeUppercase = true,
    IncludeDigits = true,
    IncludeSpecialChars = true,
    ExcludeAmbiguous = true  // 排除 l, 1, I, O, 0
};
var strongPassword = PasswordUtils.Generate(options);

// 仅数字（PIN码）
var pin = PasswordUtils.Generate(new PasswordOptions
{
    Length = 6,
    IncludeLowercase = false,
    IncludeUppercase = false,
    IncludeDigits = true,
    IncludeSpecialChars = false
});

// 自定义字符集
var hex = PasswordUtils.Generate(new PasswordOptions
{
    Length = 16,
    CustomChars = "0123456789ABCDEF"
});
```

### PasswordUtils.GenerateMultiple(count, options)

批量生成密码。

```csharp
var passwords = PasswordUtils.GenerateMultiple(10, new PasswordOptions { Length = 12 });
foreach (var pwd in passwords)
{
    Console.WriteLine(pwd);
}
```

### PasswordUtils.GeneratePassphrase(...)

生成易记的密码短语。

```csharp
// 默认（4个单词，用 - 分隔）
var phrase = PasswordUtils.GeneratePassphrase();
// 输出示例: apple-dragon-elephant-sunset

// 5个单词，空格分隔
var phrase = PasswordUtils.GeneratePassphrase(5, " ");

// 大写 + 随机数字
var phrase = PasswordUtils.GeneratePassphrase(4, "-", capitalize: true, includeNumber: true);
// 输出示例: Apple3-Dragon-Elephant-Sunset
```

### PasswordUtils.IsCommonPassword(password)

检查是否为常见弱密码。

```csharp
PasswordUtils.IsCommonPassword("password");      // true
PasswordUtils.IsCommonPassword("123456");        // true
PasswordUtils.IsCommonPassword("qwerty");        // true
PasswordUtils.IsCommonPassword("MyUn!queP@ss");  // false
```

### PasswordUtils.ValidatePolicy(password, ...)

验证密码是否符合策略要求。

```csharp
var (isValid, errors) = PasswordUtils.ValidatePolicy(
    "Pass1",
    minLength: 8,
    requireLowercase: true,
    requireUppercase: true,
    requireDigit: true,
    requireSpecial: true
);

if (!isValid)
{
    foreach (var error in errors)
    {
        Console.WriteLine(error);
    }
}
```

### PasswordUtils.CalculateEntropy(password)

计算密码熵值（单位：比特）。

```csharp
var entropy = PasswordUtils.CalculateEntropy("Password1!");
Console.WriteLine($"熵值: {entropy:F2} bits");
// 熵值: 52.00 bits
```

### PasswordUtils.RatePassword(password)

返回密码评分（1-5）。

```csharp
var rating = PasswordUtils.RatePassword("MyP@ssw0rd!");
Console.WriteLine($"评分: {rating}/5");  // 5/5
```

### PasswordUtils.GetStrengthLabel(password)

获取人类可读的强度标签。

```csharp
var label = PasswordUtils.GetStrengthLabel("password");
Console.WriteLine(label);  // "VeryWeak"
```

## 强度等级

| 等级 | 分数范围 | 描述 |
|------|----------|------|
| VeryWeak | 0-19 | 极弱，立即被破解 |
| Weak | 20-39 | 弱，几秒到几分钟被破解 |
| Fair | 40-59 | 一般，几小时到几天被破解 |
| Strong | 60-79 | 强，需要数月到数年 |
| VeryStrong | 80-100 | 极强，需要数十年以上 |

## 安全说明

- 使用 `RandomNumberGenerator` 生成密码，这是密码学安全的随机数生成器
- 不存储任何密码
- 常见密码列表来自公开的弱密码数据库
- 熵值计算考虑了字符集多样性

## 测试覆盖

- 强度分析测试
- 密码生成测试
- 密码短语测试
- 策略验证测试
- 熵值计算测试
- 边界情况测试
- Unicode 支持

## 示例输出

```
=== Password Strength Analysis ===

Password: MyStr0ng!Pass#2024
  Strength:     VeryStrong
  Score:        92/100
  Entropy:      121.97 bits
  Crack Time:   Centuries+
  Character Set:
    - Lowercase: ✓ Yes
    - Uppercase: ✓ Yes
    - Digits:    ✓ Yes
    - Special:   ✓ Yes

=== Password Generation ===

Default Password (16 chars):
   xK9#mP2$nL5@qR8&
   aB3!cD4@eF5#gH6$
   ...

Passphrase (4 words):
   apple-dragon-elephant-sunset
   harbor-jungle-kitchen-lemon
   ...
```

## 许可证

MIT License - 自由使用、修改和分发。

## 作者

AllToolkit 自动化开发

## 更新日志

- 2026-05-24: 初始版本发布
  - 密码强度分析
  - 密码生成
  - 密码短语生成
  - 策略验证
  - 常见密码检测
  - 熵值计算