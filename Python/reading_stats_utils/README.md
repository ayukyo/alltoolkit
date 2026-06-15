# Reading Stats Utils 📖

文本可读性统计分析工具，支持多种语言（中文、日文、韩文、英文）。

## 特性

- ✅ **音节计数** - 单词音节数计算
- ✅ **多语言检测** - 中/日/朝/英自动检测
- ✅ **可读性指标** - 句子数、段落数、词数统计
- ✅ **FLASHR/W袋** - 文本复杂度分析
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

### 基本统计

```python
from reading_stats_utils import ReadingStats, count_words, count_sentences

stats = ReadingStats()
text = "Hello world. This is a test."

# 词数统计
word_count = count_words(text)
print(word_count)  # 6

# 句子统计
sentence_count = count_sentences(text)
print(sentence_count)  # 2

# 完整统计
result = stats.analyze(text)
print(f"单词: {result['word_count']}")
print(f"句子: {result['sentence_count']}")
```

### 语言检测

```python
from reading_stats_utils import detect_language

lang = detect_language("你好世界")
print(lang)  # {'zh': 1.0}

lang = detect_language("Hello 世界")
print(lang)  # {'en': 0.5, 'zh': 0.5}
```

## API 参考

### 核心函数

| 函数 | 说明 |
|------|------|
| `ReadingStats.analyze(text)` | 完整文本分析 |
| `count_words(text)` | 词数统计 |
| `count_sentences(text)` | 句子统计 |
| `count_paragraphs(text)` | 段落统计 |
| `detect_language(text)` | 语言检测 |
