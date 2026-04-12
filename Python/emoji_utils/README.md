# Emoji Utils 🎭

**Python 表情符号处理工具库**

零依赖、生产就绪的表情符号提取、分析、转换和操作工具。

---

## ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **全面支持** - 覆盖所有 Unicode 表情符号范围
- **智能分析** - 自动分类、统计、密度计算
- **Unicode 转换** - 表情符号与 Unicode 互相转换
- **肤色处理** - 支持肤色变体检测和移除
- **文本转换** - 表情符号与文本描述互转
- **位置追踪** - 获取表情符号在文本中的精确位置
- **安全反转** - 反转文本时保持表情符号完整

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 或者从 AllToolkit 克隆
git clone https://github.com/ayukyo/alltoolkit.git
cd alltoolkit/Python/emoji_utils
```

---

## 🚀 快速开始

### 基本使用

```python
from emoji_utils.mod import EmojiUtils

utils = EmojiUtils()

# 提取表情符号
text = "Hello 👋 World 🌍!"
emojis = utils.extract_emojis(text)
print(emojis)  # ['👋', '🌍']

# 计数
count = utils.count_emojis(text)
print(count)  # 2

# 检测
has_emoji = utils.has_emoji(text)
print(has_emoji)  # True

# 移除
clean = utils.remove_emojis(text)
print(clean)  # "Hello World!"
```

### 模块级函数

```python
from emoji_utils.mod import (
    extract_emojis,
    count_emojis,
    has_emoji,
    remove_emojis,
    analyze,
)

text = "Great! 👏👏👏"

# 直接使用
emojis = extract_emojis(text)      # ['🏻', '👏', '👏']
count = count_emojis(text)         # 3
exists = has_emoji(text)           # True
clean = remove_emojis(text)        # "Great!"
```

---

## 📖 API 参考

### EmojiUtils 类

#### 提取与计数

| 方法 | 描述 | 返回 |
|------|------|------|
| `extract_emojis(text)` | 提取所有表情符号 | `List[str]` |
| `count_emojis(text)` | 计数表情符号总数 | `int` |
| `get_unique_emojis(text)` | 获取唯一表情符号集合 | `Set[str]` |
| `get_emoji_counts(text)` | 获取每个表情符号的计数 | `Dict[str, int]` |

#### 检测与判断

| 方法 | 描述 | 返回 |
|------|------|------|
| `has_emoji(text)` | 检查文本是否包含表情符号 | `bool` |
| `is_emoji(char)` | 检查字符是否为表情符号 | `bool` |

#### 移除与替换

| 方法 | 描述 | 返回 |
|------|------|------|
| `remove_emojis(text, strip_whitespace=True)` | 移除所有表情符号 | `str` |
| `replace_emojis(text, replacement='')` | 替换表情符号为指定字符串 | `str` |

#### 分析

| 方法 | 描述 | 返回 |
|------|------|------|
| `analyze(text)` | 全面分析文本中的表情符号 | `EmojiAnalysis` |
| `get_emoji_info(emoji)` | 获取单个表情符号的详细信息 | `EmojiInfo` |
| `get_emoji_positions(text)` | 获取表情符号的位置 | `List[Tuple[int, int, str]]` |

#### Unicode 转换

| 方法 | 描述 | 返回 |
|------|------|------|
| `to_unicode_escape(emoji)` | 转换为 Unicode 转义序列 | `str` |
| `from_unicode_escape(unicode_str)` | 从 Unicode 转义序列转换 | `str` |

#### 肤色处理

| 方法 | 描述 | 返回 |
|------|------|------|
| `strip_skin_tone(emoji)` | 移除肤色修饰符 | `str` |
| `get_skin_tone_variants(emoji)` | 获取所有肤色变体 | `Dict[str, str]` |

#### 文本转换

| 方法 | 描述 | 返回 |
|------|------|------|
| `emoji_to_text(emoji, use_shortcodes=False)` | 转换为文本描述 | `str` |
| `text_to_emoji(text)` | 从文本转换为表情符号 | `Optional[str]` |

#### 分类与过滤

| 方法 | 描述 | 返回 |
|------|------|------|
| `filter_by_category(text, category)` | 按类别过滤表情符号 | `List[str]` |

#### 其他

| 方法 | 描述 | 返回 |
|------|------|------|
| `reverse(text)` | 反转文本（保持表情符号完整） | `str` |

---

## 📊 数据结构

### EmojiInfo

表情符号详细信息：

```python
@dataclass
class EmojiInfo:
    char: str              # 表情符号字符
    unicode: str           # Unicode 编码
    name: str              # Unicode 名称
    category: EmojiCategory  # 类别
    skin_tone: Optional[str]  # 肤色
    is_variant: bool       # 是否为变体
    codepoints: List[str]  # 码点列表
```

### EmojiAnalysis

分析结果：

```python
@dataclass
class EmojiAnalysis:
    text: str              # 原始文本
    total_emojis: int      # 表情符号总数
    unique_emojis: int     # 唯一表情符号数
    emojis: List[str]      # 所有表情符号列表
    emoji_info: List[EmojiInfo]  # 详细信息
    emoji_counts: Dict[str, int]  # 计数
    categories: Dict[str, int]    # 类别统计
    emoji_density: float   # 密度百分比
```

### EmojiCategory

表情符号类别：

```python
class EmojiCategory(Enum):
    SMILEY = "smiley"      # 笑脸/表情
    PERSON = "person"      # 人物
    ANIMAL = "animal"      # 动物
    FOOD = "food"          # 食物
    TRAVEL = "travel"      # 旅行/地点
    ACTIVITY = "activity"  # 活动
    OBJECT = "object"      # 物品
    SYMBOL = "symbol"      # 符号
    FLAG = "flag"          # 旗帜
    NATURE = "nature"      # 自然
    UNKNOWN = "unknown"    # 未知
```

---

## 💡 使用示例

### 1. 社交媒体分析

```python
from emoji_utils.mod import EmojiUtils, EmojiCategory

utils = EmojiUtils()

posts = [
    "Love this! ❤️❤️❤️",
    "Great service 👍",
    "Amazing! 🎉🎉🎉",
]

for post in posts:
    analysis = utils.analyze(post)
    print(f"Post: {post}")
    print(f"  Emojis: {analysis.total_emojis}")
    print(f"  Density: {analysis.emoji_density}%")
    print(f"  Categories: {analysis.categories}")
```

### 2. 内容过滤

```python
from emoji_utils.mod import remove_emojis, has_emoji

messages = [
    "Hello! 👋",
    "Check this! 🔥",
    "Plain text",
]

for msg in messages:
    if has_emoji(msg):
        clean = remove_emojis(msg)
        print(f"Filtered: {clean}")
```

### 3. 表情符号统计

```python
from emoji_utils.mod import EmojiUtils

utils = EmojiUtils()
text = "😀😃😄😀😁😀😆😅😂"

analysis = utils.analyze(text)
print(f"Total: {analysis.total_emojis}")
print(f"Unique: {analysis.unique_emojis}")
print(f"Most used: {max(analysis.emoji_counts.items(), key=lambda x: x[1])}")
```

### 4. Unicode 转换

```python
from emoji_utils.mod import to_unicode_escape, from_unicode_escape

# 表情符号 → Unicode
unicode_str = to_unicode_escape("😀")
print(unicode_str)  # U+1F600

# Unicode → 表情符号
emoji = from_unicode_escape("U+1F600")
print(emoji)  # 😀
```

### 5. 肤色处理

```python
from emoji_utils.mod import EmojiUtils

utils = EmojiUtils()

# 获取肤色变体
base = "👋"
variants = utils.get_skin_tone_variants(base)
for tone, variant in variants.items():
    print(f"{tone}: {variant}")

# 移除肤色
emoji_with_tone = "👋🏽"
base_emoji = utils.strip_skin_tone(emoji_with_tone)
print(f"{emoji_with_tone} → {base_emoji}")
```

### 6. 安全反转文本

```python
from emoji_utils.mod import reverse

text = "Hello 👋 World 🌍"
reversed_text = reverse(text)
print(f"'{text}' → '{reversed_text}'")
# 输出：'🌍👋 olleH' (表情符号保持完整)
```

---

## 🧪 测试

运行测试套件：

```bash
cd /path/to/AllToolkit/Python/emoji_utils
python emoji_utils_test.py
```

测试覆盖：

- ✅ 基本提取和计数
- ✅ 检测和判断
- ✅ 移除和替换
- ✅ Unicode 转换
- ✅ 肤色处理
- ✅ 文本转换
- ✅ 分类过滤
- ✅ 位置追踪
- ✅ 文本反转
- ✅ 边界情况和错误处理

---

## 📁 文件结构

```
emoji_utils/
├── mod.py                      # 主模块
├── emoji_utils_test.py         # 测试套件
├── README.md                   # 本文档
└── examples/
    └── usage_examples.py       # 使用示例
```

---

## 🔧 高级用法

### 自定义类别分类

```python
from emoji_utils.mod import EmojiUtils, EmojiCategory

utils = EmojiUtils()

# 获取所有笑脸类别的表情
text = "😀🐕🍎🚗"
smileys = utils.filter_by_category(text, EmojiCategory.SMILEY)
print(smileys)  # ['😀']
```

### 批量处理

```python
from emoji_utils.mod import EmojiUtils

utils = EmojiUtils()

texts = ["Hello 👋", "World 🌍", "Test"]
results = [utils.analyze(t) for t in texts]

for text, result in zip(texts, results):
    print(f"{text}: {result.total_emojis} emojis")
```

### 表情符号验证

```python
from emoji_utils.mod import EmojiUtils

utils = EmojiUtils()

# 验证输入是否为有效表情符号
def validate_emoji_input(user_input: str) -> bool:
    return utils.is_emoji(user_input.strip())

print(validate_emoji_input("😀"))  # True
print(validate_emoji_input("Hello"))  # False
```

---

## 📝 注意事项

1. **Unicode 范围**: 支持所有标准 Unicode 表情符号范围，包括扩展区
2. **复杂表情**: 支持 ZWJ 序列（如 👨‍👩‍👧‍👦）和变体选择器
3. **性能**: 对于大量文本，建议复用 `EmojiUtils` 实例
4. **兼容性**: Python 3.6+

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 报告 Bug
- 请求新功能
- 改进文档
- 添加测试用例

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 🔗 相关链接

- [AllToolkit 主项目](../../README.md)
- [Python 工具列表](../README.md)
- [Unicode 表情符号标准](https://unicode.org/emoji/charts/full-emoji-list.html)

---

**最后更新**: 2026-04-11
