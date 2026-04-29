# transliteration_utils - 音译工具

[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](./transliteration_utils_test.py)

零依赖的文字音译转换工具。

## 特性

- **中文音译**: 拼音、注音符号
- **日文音译**: 平假名→罗马字、片假名→罗马字
- **韩文音译**: 韩文→罗马字
- **俄文音译**: 俄文→拉丁字母
- **双向转换**: 支持反向音译
- **多音字处理**: 基于上下文的多音字识别
- **零依赖**: 纯 Python 实现

## 安装

```python
from transliteration_utils import (
    to_pinyin,
    to_romaji,
    transliterate
)
```

## 快速开始

### 中文拼音

```python
from transliteration_utils import to_pinyin

# 转换为拼音
pinyin = to_pinyin("你好")
print(pinyin)  # "nǐ hǎo"

# 无声调
pinyin = to_pinyin("你好", tone=False)
print(pinyin)  # "ni hao"

# 带音调符号
pinyin = to_pinyin("你好", tone_marks=True)
print(pinyin)  # "nǐ hǎo"
```

### 日文罗马字

```python
from transliteration_utils import to_romaji

# 平假名转罗马字
romaji = to_romaji("こんにちは")
print(romaji)  # "konnichiha"

# 片假名转罗马字
romaji = to_romaji("コンピューター")
print(romaji)  # "konpyuuta"
```

### 通用音译

```python
from transliteration_utils import transliterate

# 自动检测语言并音译
result = transliterate("你好", target="latin")
result = transliterate("こんにちは", target="latin")
result = transliterate("안녕하세요", target="latin")
```

## API 参考

### 中文相关

| 函数 | 说明 |
|-----|------|
| `to_pinyin(text, tone, tone_marks)` | 中文转拼音 |
| `to_bopomofo(text)` | 中文转注音符号 |
| `pinyin_to_hanzi(pinyin)` | 拼音转汉字（候选） |

### 日文相关

| 函数 | 说明 |
|-----|------|
| `to_romaji(text, system)` | 日文转罗马字 |
| `hiragana_to_romaji(text)` | 平假名转罗马字 |
| `katakana_to_romaji(text)` | 片假名转罗马字 |

### 其他语言

| 函数 | 说明 |
|-----|------|
| `korean_to_latin(text)` | 韩文转拉丁字母 |
| `russian_to_latin(text)` | 俄文转拉丁字母 |

### 通用函数

| 函数 | 说明 |
|-----|------|
| `transliterate(text, source, target)` | 通用音译 |

## 测试

```bash
python -m pytest transliteration_utils_test.py -v
```

## 许可证

MIT License