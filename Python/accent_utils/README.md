# Accent Utils - 变音符号处理工具 🌐

[![测试状态](https://img.shields.io/badge/tests-passed-brightgreen)]()
[![覆盖率](https://img.shields.io/badge/coverage-100%25-brightgreen)]()

处理文本中变音符号（diacritical marks）的工具库，支持多语言，零外部依赖。

---

## ✨ 功能特性

### 变音符号移除
- **移除变音符号**：café → cafe
- **特定语言映射**：德语 ü → ue
- **保留指定字符**：选择性保留特定变音字符

### 文本标准化
- **综合标准化**：大小写、变音符号、标点、空白
- **搜索标准化**：用于搜索和比较
- **ASCII 音译**：转换为纯 ASCII 文本

### 检测与分析
- **变音符号检测**：检查文本是否含变音符号
- **位置分析**：获取变音符号位置信息
- **语言检测**：根据变音符号推测语言

### 搜索与比较
- **忽略变音搜索**：café 能匹配 cafe
- **忽略变音比较**：比较时忽略变音差异

---

## 🚀 快速开始

### 移除变音符号

```python
from accent_utils import remove_accents

# 基础移除
print(remove_accents('café'))       # 'cafe'
print(remove_accents('über'))       # 'uber'
print(remove_accents('naïve'))      # 'naive'
print(remove_accents('你好世界'))    # '你好世界'（中文不变）
```

### 特定语言处理

```python
from accent_utils import remove_accents

# 德语特殊映射（ü → ue）
print(remove_accents('über', language='german'))  # 'ueber'

# 法语特殊映射（œ → oe）
print(remove_accents('œuvre', language='french'))  # 'oeuvre'
```

### 文本标准化

```python
from accent_utils import normalize_text

# 综合标准化
text = normalize_text('Café au Lait!',
    lowercase=True,         # 转小写
    remove_accents_flag=True, # 移除变音
    remove_punctuation=True,  # 移除标点
    collapse_whitespace=True  # 合并空白
)
print(text)  # 'cafe au lait'
```

---

## 📚 详细用法

### 变音符号检测

```python
from accent_utils import has_accents, count_accents

# 检测
print(has_accents('café'))    # True
print(has_accents('cafe'))    # False

# 计数
print(count_accents('café résumé'))  # 2
```

### 变音符号位置

```python
from accent_utils import get_accent_positions, find_accented_words

# 位置信息
positions = get_accent_positions('café')
print(positions)  # [(3, 'é', 'e')]

# 找出含变音的单词
words = find_accented_words('The café has a résumé')
print(words)  # ['café', 'résumé']
```

### 忽略变音比较

```python
from accent_utils import compare_accent_insensitive

# 比较
print(compare_accent_insensitive('café', 'cafe'))  # True
print(compare_accent_insensitive('Café', 'cafe'))  # True（默认忽略大小写）
```

### 忽略变音搜索

```python
from accent_utils import accent_insensitive_search

# 搜索
text = 'I love café and Café au lait'
results = accent_insensitive_search(text, 'cafe')
print(results)  # [(7, 11, 'café'), (16, 20, 'Café')]
```

### 语言检测

```python
from accent_utils import detect_language_from_accents

# 根据变音符号推测语言
print(detect_language_from_accents('über'))    # ['german']
print(detect_language_from_accents('café'))    # ['french']
print(detect_language_from_accents('niño'))    # ['spanish']
```

### ASCII 音译

```python
from accent_utils import transliterate_to_ascii

# 转换为 ASCII
print(transliterate_to_ascii('café résumé'))  # 'cafe resume'
print(transliterate_to_ascii('über', language='german'))  # 'ueber'
```

### AccentNormalizer 类

```python
from accent_utils import AccentNormalizer

# 创建规范化器
normalizer = AccentNormalizer(
    language='german',
    lowercase=True
)

# 规范化
print(normalizer.normalize('über'))  # 'ueber'

# 比较
print(normalizer.compare('über', 'ueber'))  # True

# 搜索
results = normalizer.search('über ist groß', 'uber')
```

---

## 🔧 API 参考

### 核心函数

| 函数 | 说明 |
|------|------|
| `remove_accents(text, language)` | 移除变音符号 |
| `normalize_text(text, ...)` | 综合标准化 |
| `has_accents(text)` | 检测变音符号 |
| `count_accents(text)` | 计数变音符号 |
| `is_diacritic(char)` | 判断是否变音符号 |

### 分析函数

| 函数 | 说明 |
|------|------|
| `get_accent_positions(text)` | 获取位置信息 |
| `find_accented_words(text)` | 找含变音单词 |
| `detect_language_from_accents(text)` | 推测语言 |

### 搜索比较

| 函数 | 说明 |
|------|------|
| `compare_accent_insensitive(a, b)` | 忽略变音比较 |
| `accent_insensitive_search(text, q)` | 忽略变音搜索 |
| `transliterate_to_ascii(text)` | ASCII 音译 |

### 类

| 类 | 说明 |
|------|------|
| `AccentNormalizer` | 批量规范化器 |

---

## 🌍 语言支持

| 语言 | 特殊映射 |
|------|----------|
| German | ä→ae, ö→oe, ü→ue, ß→ss |
| French | œ→oe, æ→ae |
| Turkish | İ→I, ı→i |

---

## 📝 Unicode 背景

### 变音符号范围

- `U+0300-U+036F`: Combining Diacritical Marks
- `U+1AB0-U+1AFF`: Extended
- `U+1DC0-U+1DFF`: Supplement

### 规范化形式

- **NFD**: 分解形式（字符 + 组合变音符号）
- **NFC**: 组合形式（预组合字符）

---

## 🧪 测试

```bash
python Python/accent_utils/accent_utils_test.py
```

---

## 📄 许可证

MIT License

---

**最后更新**: 2026-05-19