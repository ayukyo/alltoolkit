# readability_utils - 文本可读性分析工具

[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](./readability_utils_test.py)

零依赖的文本可读性分析工具，支持英文和中文文本。

## 特性

- **多指标分析**: 支持 6 种主流可读性指标
- **英文支持**: Flesch Reading Ease、Flesch-Kincaid、Gunning Fog、SMOG、Coleman-Liau、ARI
- **中文支持**: 基于句长、标点密度等特征的难度评估
- **零依赖**: 纯 Python 实现，无需外部库

## 安装

```python
from readability_utils import (
    analyze_readability,
    get_grade_level,
    count_syllables,
    ReadabilityAnalyzer,
    ChineseReadabilityAnalyzer,
    TextStats
)
```

## 快速开始

### 英文文本分析

```python
from readability_utils import analyze_readability, get_grade_level

text = "The quick brown fox jumps over the lazy dog. This is a simple sentence."

# 完整分析
result = analyze_readability(text, 'en')
print(f"Flesch Reading Ease: {result['flesch_reading_ease']}")
print(f"Grade Level: {result['grade_level']}")

# 快速获取年级水平
level = get_grade_level(text, 'en')
print(f"年级水平: {level}")
```

### 中文文本分析

```python
from readability_utils import analyze_readability, get_grade_level

text = "人工智能技术的快速发展对社会经济结构产生了深远影响。"

# 完整分析
result = analyze_readability(text, 'zh')
print(f"难度分数: {result['difficulty_score']}")
print(f"难度等级: {result['difficulty_level']}")

# 快速获取难度等级
level = get_grade_level(text, 'zh')
print(f"难度等级: {level}")
```

### 高级用法

```python
from readability_utils import ReadabilityAnalyzer, TextStats

text = "Your text here..."

# 使用分析器类
analyzer = ReadabilityAnalyzer(text)

# 单独获取各项指标
fre = analyzer.flesch_reading_ease()
fkg = analyzer.flesch_kincaid_grade()
fog = analyzer.gunning_fog_index()
smog = analyzer.smog_index()
cli = analyzer.coleman_liau_index()
ari = analyzer.automated_readability_index()

# 完整分析结果
result = analyzer.analyze()
```

## API 参考

### 主要函数

#### `analyze_readability(text, language='en')`
分析文本可读性，返回字典形式的完整结果。

**参数:**
- `text` (str): 要分析的文本
- `language` (str): 语言代码，'en' 为英文，'zh' 为中文

**返回:** 包含可读性指标的字典

#### `get_grade_level(text, language='en')`
获取文本年级水平/难度描述。

**返回:** 年级水平字符串，如 "标准（8-9年级）"

#### `count_syllables(word)`
计算英文单词音节数。

### 核心类

#### `ReadabilityAnalyzer`
英文文本可读性分析器。

**方法:**
- `flesch_reading_ease()` → float: 0-100 分数
- `flesch_kincaid_grade()` → float: 美国年级水平
- `gunning_fog_index()` → float: 迷雾指数
- `smog_index()` → float: SMOG 指数
- `coleman_liau_index()` → float: Coleman-Liau 指数
- `automated_readability_index()` → float: ARI 指数
- `analyze()` → ReadabilityResult: 完整分析结果

#### `ChineseReadabilityAnalyzer`
中文文本可读性分析器。

**方法:**
- `get_difficulty()` → Tuple[float, str]: 难度分数和描述
- `analyze()` → Dict: 完整分析结果

## 可读性指标说明

### Flesch Reading Ease (弗莱施易读性指数)

| 分数范围 | 难度等级 |
|---------|---------|
| 90-100 | 非常容易（5年级） |
| 80-90 | 容易（6年级） |
| 70-80 | 较容易（7年级） |
| 60-70 | 标准（8-9年级） |
| 50-60 | 较难（10-12年级） |
| 30-50 | 困难（大学水平） |
| 0-30 | 非常困难（专业水平） |

### Flesch-Kincaid Grade Level

返回美国年级水平，例如 8.0 表示 8 年级学生可以理解。

## 测试

```bash
python -m pytest readability_utils_test.py -v
```

## 许可证

MIT License