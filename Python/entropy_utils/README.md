# Entropy Utils 📊

信息熵和密码熵分析工具模块，提供各种熵计算和密码强度分析功能。

## 功能特性

- **香农熵** - 计算字符串、字节和列表的信息熵
- **密码熵分析** - 评估密码强度和安全性
- **数据压缩评估** - 评估数据的可压缩性
- **字符集分析** - 分析密码使用的字符类型
- **密码建议** - 基于熵分析生成改进建议
- **零外部依赖** - 纯 Python 实现

## 快速开始

```python
from entropy_utils import (
    shannon_entropy, analyze_password, entropy_report
)

# 计算字符串熵
text = "hello"
entropy = shannon_entropy(text)
print(f"熵值: {entropy:.2f} bits/字符")  # ~2.32

# 分析密码强度
result = analyze_password("P@ssw0rd!")
print(result.entropy)           # 熵值
print(result.strength_level)    # 'medium', 'strong', etc.
print(result.crack_time)        # 破解时间估算

# 完整报告
report = entropy_report("MyP@ssw0rd123")
print(report)
```

## 香农熵

### 基本用法

```python
from entropy_utils import shannon_entropy

# 字符串熵
print(shannon_entropy("aaaaaa"))    # 低熵：全相同字符
# 0.00

print(shannon_entropy("abcdef"))    # 高熵：完全随机
# ~2.58

print(shannon_entropy("aaaaaaaa"))  # 非常低熵
# 0.00

# 字节熵
data = b'\x00\x01\x02\x03'
print(shannon_entropy(data))

# 列表熵
items = [1, 1, 1, 2, 2, 3]
print(shannon_entropy(items))
```

### 熵值解释

| 熵值范围 | 含义 | 示例 |
|---------|------|------|
| 0-2 | 非常低 | "aaaaaa", "123456" |
| 2-3 | 低 | "password", "abc123" |
| 3-4 | 中等 | "Pass123", "hello" |
| 4+ | 高 | "P@ssw0rd!", "x#9kL" |

## 密码分析

### analyze_password

```python
from entropy_utils import analyze_password

result = analyze_password("P@ssw0rd!")

print(result.password)        # 'P@ssw0rd!' (掩码显示)
print(result.entropy)         # 47.5
print(result.length)          # 9
print(result.strength_level)  # 'strong'
print(result.crack_time)      # 'centuries'
print(result.char_classes)    # {'upper', 'lower', 'digit', 'special'}
```

### 强度等级

```python
from entropy_utils import analyze_password

passwords = [
    "123456",
    "password",
    "P@ssw0rd",
    "Str0ng!P@ssw0rd#2024",
]

for pwd in passwords:
    result = analyze_password(pwd)
    print(f"{pwd}: {result.strength_level} ({result.entropy:.1f} bits)")
```

输出：
```
123456: very_weak (13.5 bits)
password: weak (32.8 bits)
P@ssw0rd: medium (47.2 bits)
Str0ng!P@ssw0rd#2024: very_strong (95.6 bits)
```

### 字符集分析

```python
from entropy_utils import analyze_password

result = analyze_password("Hello123!")

print(result.has_upper)    # True
print(result.has_lower)    # True
print(result.has_digit)    # True
print(result.has_special)  # True
print(result.char_count)   # {'upper': 1, 'lower': 4, 'digit': 3, 'special': 1}
```

### 破解时间估算

```python
from entropy_utils import analyze_password

result = analyze_password("Str0ng!P@ss")
print(result.crack_time)  # '2 hours' / '3 centuries' 等

# 按攻击场景
print(result.crack_time_online)   # 在线攻击（1K/s）
print(result.crack_time_offline)   # 离线攻击（10B/s）
```

### 改进建议

```python
from entropy_utils import analyze_password

result = analyze_password("password")

for suggestion in result.suggestions:
    print(suggestion)
# 'Add uppercase letters'
# 'Add digits'
# 'Add special characters'
# 'Increase length'
```

## 完整熵报告

```python
from entropy_utils import entropy_report

report = entropy_report("MyP@ssw0rd123")

# 报告包含：
print(report['shannon_entropy'])    # 香农熵
print(report['per_char_entropy'])  # 每字符熵
print(report['unique_chars'])      # 唯一字符数
print(report['password_analysis'])  # 密码分析结果
print(report['compression_ratio'])  # 估算压缩比
print(report['recommendations'])   # 改进建议
```

## EntropyUtils 类

```python
from entropy_utils import EntropyUtils

utils = EntropyUtils()

# 计算自定义数据集的熵
data = [1, 2, 3, 1, 2, 1]
print(utils.calculate(data))

# 批量分析
passwords = ["123456", "password", "P@ssw0rd"]
for pwd in passwords:
    result = utils.analyze(pwd)
    print(f"{pwd}: {result.strength_level}")
```

## DataEntropyAnalyzer

```python
from entropy_utils import DataEntropyAnalyzer

analyzer = DataEntropyAnalyzer()

# 分析文件熵
# result = analyzer.analyze_file("data.bin")

# 分析数据流
data = b'\x00\x01\x02\x03' * 1000
result = analyzer.analyze_bytes(data)
print(result['entropy'])           # 熵值
print(result['is_compressible'])   # 是否可压缩
print(result['estimated_ratio'])    # 压缩比估算
```

## 密码强度判定标准

| 等级 | 熵值范围 | 安全性 |
|------|----------|--------|
| very_weak | < 28 bits | 极易被破解 |
| weak | 28-35 bits | 容易被破解 |
| fair | 35-50 bits | 中等强度 |
| medium | 50-60 bits | 较好 |
| strong | 60-80 bits | 强 |
| very_strong | 80+ bits | 非常强 |

## 最佳实践

```python
from entropy_utils import analyze_password

# 检查密码强度
def validate_password(password: str) -> bool:
    result = analyze_password(password)
    return result.strength_level in ('strong', 'very_strong')

# 生成建议
def suggest_improvements(password: str) -> list:
    result = analyze_password(password)
    return result.suggestions
```

## 主要函数

| 函数 | 说明 |
|------|------|
| `shannon_entropy(data)` | 计算香农熵 |
| `analyze_password(password)` | 分析密码强度 |
| `entropy_report(data)` | 生成完整熵报告 |
| `EntropyUtils.calculate()` | 通用熵计算 |

## 测试

```bash
python -m pytest Python/entropy_utils/ -v
```

## 许可证

MIT License