# Pinyin Utils


AllToolkit - Pinyin Utilities Module
=====================================
A comprehensive Chinese Pinyin utility module with zero external dependencies.

Features:
    - Hanzi (Chinese character) to Pinyin conversion
    - Polyphonic character handling with context-aware disambiguation
    - Multiple output formats (with tones, without tones, numbered tones)
    - Pinyin sorting for Chinese text
    - Word segmentation for accurate conversion
    - Initial/final extraction
    - Tone conversion utilities

Author: AllToolkit Contributors
License: MIT


## 功能

### 函数

- **is_hanzi(char**) - Check if a character is a Chinese character (Hanzi).
- **get_pinyin(char, default**) - Get all possible pinyin readings for a Chinese character.
- **get_pinyin_with_tone(char**) - Get pinyin readings with tone numbers for a Chinese character.
- **to_pinyin(text, format, heteronym**, ...) - Convert Chinese text to Pinyin.
- **to_pinyin_initials(text**) - Get the initials (consonants) of pinyin for each Chinese character.
- **to_pinyin_finals(text, with_tone**) - Get the finals (vowels + endings) of pinyin for each Chinese character.
- **sort_by_pinyin(items, reverse**) - Sort Chinese strings by their pinyin representation.
- **sort_by_stroke(items, reverse**) - Sort Chinese strings by approximate complexity.
- **contains_hanzi(text**) - Check if text contains any Chinese characters.
- **count_hanzi(text**) - Count the number of Chinese characters in text.

... 共 22 个函数

## 使用示例

```python
from mod import is_hanzi

# 使用 is_hanzi
result = is_hanzi()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
