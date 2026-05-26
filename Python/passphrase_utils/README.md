# Passphrase Utils - 密码短语生成工具

生成安全且易于记忆的密码短语。零外部依赖，纯 Python 标准库实现。

## 功能特性

- **安全随机**: 使用 `secrets` 模块确保密码学安全的随机性
- **多种分隔符**: 支持空格、连字符、下划线、点号或无分隔符
- **大小写控制**: 支持小写、大写、首字母大写、随机大小写、交替大小写
- **增强选项**: 可添加随机数字和特殊字符
- **熵值计算**: 自动计算密码短语的熵值（安全性指标）
- **破解时间估算**: 估算暴力破解所需时间
- **强度分析**: 分析现有密码短语的强度
- **内置单词列表**: 提供常用英语单词列表和 Diceware 标准列表

## 安装

无需安装，直接导入使用：

```python
from passphrase_utils.mod import PassphraseGenerator, generate_passphrase
```

## 快速开始

### 基本用法

```python
from passphrase_utils.mod import generate_passphrase

# 生成默认的 4 词密码短语
phrase = generate_passphrase()
print(phrase)  # 例如: "correct-horse-battery-staple"

# 指定单词数量和分隔符
phrase = generate_passphrase(word_count=5, separator=" ")
print(phrase)  # 例如: "apple banana cherry date elderberry"
```

### 使用 PassphraseGenerator 类

```python
from passphrase_utils.mod import PassphraseGenerator, Separator, WordCase

gen = PassphraseGenerator()

# 生成带增强的密码短语
result = gen.generate(
    word_count=4,
    separator=Separator.HYPHEN,
    word_case=WordCase.CAPITALIZE,
    include_numbers=True,
    include_special=True
)

print(f"密码短语: {result.passphrase}")
print(f"单词列表: {result.words}")
print(f"熵值: {result.entropy_bits} bits")
```

### Diceware 风格

```python
from passphrase_utils.mod import generate_diceware

# 使用 Diceware 方法生成密码短语
phrase = generate_diceware(word_count=5)
print(phrase)  # 例如: "abandon ability able about above"
```

### 分析密码短语强度

```python
from passphrase_utils.mod import passphrase_strength

analysis = passphrase_strength("correct-horse-battery-staple")
print(f"强度: {analysis['strength']}")
print(f"熵值: {analysis['entropy_bits']} bits")
print(f"预估破解时间: {analysis['estimated_crack_time']}")
```

## API 参考

### PassphraseGenerator

```python
class PassphraseGenerator:
    def __init__(
        self,
        wordlist: Optional[List[str]] = None,
        wordlist_name: str = "builtin"
    ):
        """初始化生成器"""

    def generate(
        self,
        word_count: int = 4,
        separator: Separator = Separator.HYPHEN,
        word_case: WordCase = WordCase.LOWER,
        min_word_length: int = 3,
        max_word_length: int = 10,
        include_numbers: bool = False,
        include_special: bool = False,
        special_chars: str = "!@#$%^&*"
    ) -> PassphraseResult:
        """生成密码短语"""

    def calculate_entropy(
        self,
        word_count: int,
        wordlist_size: Optional[int] = None
    ) -> float:
        """计算熵值"""

    def estimate_crack_time(
        self,
        entropy_bits: float,
        guesses_per_second: float = 1e12
    ) -> str:
        """估算破解时间"""

    def analyze_passphrase(self, passphrase: str) -> dict:
        """分析密码短语强度"""
```

### Separator 枚举

| 值 | 描述 |
|---|---|
| `SPACE` | 空格分隔 |
| `HYPHEN` | 连字符分隔 (默认) |
| `UNDERSCORE` | 下划线分隔 |
| `DOT` | 点号分隔 |
| `NONE` | 无分隔符 |
| `RANDOM` | 随机选择分隔符 |

### WordCase 枚举

| 值 | 描述 |
|---|---|
| `LOWER` | 全部小写 (默认) |
| `UPPER` | 全部大写 |
| `CAPITALIZE` | 首字母大写 |
| `RANDOM` | 随机大小写 |
| `ALTERNATE` | 交替大小写 |

### PassphraseResult

```python
@dataclass
class PassphraseResult:
    passphrase: str      # 生成的密码短语
    words: List[str]      # 组成的单词列表
    entropy_bits: float   # 熵值（比特）
    separator: str        # 使用的分隔符
    word_count: int       # 单词数量
    wordlist_name: str    # 使用的单词列表名称
```

## 熵值参考

| 熵值范围 | 强度 | 破解时间估计 |
|---------|------|-------------|
| < 28 bits | 非常弱 | 瞬间 |
| 28-35 bits | 弱 | 几分钟到几小时 |
| 36-59 bits | 中等 | 数天到数年 |
| 60-79 bits | 强 | 数年到数百年 |
| >= 80 bits | 非常强 | 实际上不可破解 |

### 推荐配置

- **一般用途**: 4-5 个单词，熵值约 50-65 bits
- **重要账户**: 5-6 个单词，熵值约 65-80 bits
- **高安全性**: 7+ 个单词，熵值 > 90 bits

## 示例

### 生成多个候选

```python
gen = PassphraseGenerator()
results = gen.generate_multiple(5)

for i, r in enumerate(1, 1):
    print(f"{i}. {r.passphrase} ({r.entropy_bits} bits)")
```

### 使用自定义单词列表

```python
custom_words = ["苹果", "香蕉", "樱桃", "日期", "浆果"]
gen = PassphraseGenerator(wordlist=custom_words, wordlist_name="fruits")
result = gen.generate(word_count=3)
print(result.passphrase)  # 例如: "苹果-香蕉-樱桃"
```

### 完整示例

```python
from passphrase_utils.mod import PassphraseGenerator, Separator, WordCase

gen = PassphraseGenerator()

# 生成一个强密码短语
result = gen.generate(
    word_count=5,
    separator=Separator.HYPHEN,
    word_case=WordCase.CAPITALIZE,
    include_numbers=True,
    include_special=True
)

print(f"密码短语: {result.passphrase}")
print(f"单词: {result.words}")
print(f"熵值: {result.entropy_bits} bits")
print(f"破解时间: {gen.estimate_crack_time(result.entropy_bits)}")
```

## 安全说明

1. **随机性**: 使用 Python 的 `secrets` 模块，提供密码学安全的随机数生成
2. **单词列表**: 内置的单词列表经过筛选，避免了容易混淆的单词
3. **熵值**: 建议密码短语的熵值不低于 50 bits
4. **存储**: 生成的密码短语应使用密码管理器安全存储

## 测试

```bash
python passphrase_utils_test.py
```

## 许可证

MIT License