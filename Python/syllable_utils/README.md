# 音节计数工具 (Syllable Counter Utils)

英文单词和句子的音节分析工具，支持诗歌韵律分析、语音合成预处理等场景。

## 功能特性

- ✅ **单词音节计数** - 使用字典 + 启发式混合算法
- ✅ **句子音节分析** - 总音节、音节模式
- ✅ **诗歌韵律分析** - 韵脚模式、格律判断
- ✅ **俳句建议** - 自动检测 5-7-5 模式
- ✅ **可读性分析** - 简化版 Flesch-Kincaid 指标
- ✅ **复杂词统计** - 多音节词识别
- ✅ **音节拆分** - 简化版音节拆分
- ✅ **重音模式** - 估计单词重音位置
- ✅ **节奏表示** - 用符号表示节奏模式
- ✅ **批量处理** - 批量音节计数和统计

## 安装

```python
from syllable_utils.mod import count_syllables
```

## 快速开始

### 基本用法

```python
from syllable_utils.mod import count_syllables, count_sentence_syllables

# 单词音节计数
print(count_syllables("hello"))       # 2
print(count_syllables("beautiful"))   # 3
print(count_syllables("communication")) # 5

# 句子音节计数
print(count_sentence_syllables("Hello world"))  # 3
print(count_sentence_syllables("I love Python")) # 4
```

### 音节模式

```python
from syllable_utils.mod import get_syllable_pattern

# 获取每个单词的音节
pattern = get_syllable_pattern("Beautiful weather today")
print(pattern)  # [3, 2, 2]
```

### 诗歌分析

```python
from syllable_utils.mod import analyze_rhyme_scheme

poem = """The stars shine bright
In the quiet night
Dreams take their flight
With all their might"""

result = analyze_rhyme_scheme(poem)
print(result['rhyme_scheme'])  # AABB
print(result['meter'])         # Regular (4 syllables per line)
```

### 俳句建议

```python
from syllable_utils.mod import suggest_haiku_lines

text = "The gentle rain falls soft upon the ground below my feet"
haikus = suggest_haiku_lines(text)

for haiku in haikus:
    print(haiku['first_line'])   # 5音节
    print(haiku['second_line'])  # 7音节
    print(haiku['third_line'])   # 5音节
```

### 可读性分析

```python
from syllable_utils.mod import readability_score

text = "The cat sat on the mat"
score = readability_score(text)
print(score['difficulty'])  # easy
print(score['avg_syllables'])  # 1.0
```

### 批量处理

```python
from syllable_utils.mod import batch_count_syllables, get_syllable_stats

words = ["hello", "world", "beautiful", "programming"]
results = batch_count_syllables(words)
print(results)  # {'hello': 2, 'world': 1, 'beautiful': 3, 'programming': 3}

stats = get_syllable_stats("Hello beautiful world")
print(stats['distribution'])  # {1: 1, 2: 1, 3: 1}
```

## API 参考

### `count_syllables(word: str) -> int`
计算单个英文单词的音节数。

### `count_sentence_syllables(sentence: str) -> int`
计算句子的总音节数。

### `get_syllable_pattern(sentence: str) -> List[int]`
获取句子中每个单词的音节数列表。

### `get_syllable_breakdown(word: str) -> Dict`
获取单词的详细音节分析。

### `analyze_rhyme_scheme(text: str) -> Dict`
分析多行文本的韵律结构。

### `get_stress_pattern(word: str) -> List[int]`
估计单词的重音模式。

### `suggest_haiku_lines(text: str) -> List[Dict]`
从文本中提取可能的俳句结构（5-7-5）。

### `readability_score(text: str) -> Dict`
计算文本的可读性分数。

### `count_complex_words(text: str, threshold: int = 3) -> Dict`
统计文本中的复杂词（多音节词）。

### `split_into_syllables(word: str) -> List[str]`
将单词拆分为音节（简化版本）。

### `batch_count_syllables(words: List[str]) -> Dict[str, int]`
批量计算多个单词的音节数。

### `get_syllable_stats(text: str) -> Dict`
获取文本的音节统计信息。

## 算法说明

本工具使用混合策略：

1. **字典匹配** - 内置常用词音节字典，确保常用词准确性
2. **启发式规则** - 对于不在字典中的词，使用规则估计：
   - 元音组计数
   - 静默字母处理
   - 后缀调整规则

## 局限性

- 音节拆分是简化版本，不处理所有复杂情况
- 重音模式是估计，不保证100%准确
- 部分特殊词可能需要手动校正

## 应用场景

- 诗歌创作辅助
- 语音合成预处理
- 文本可读性分析
- 教育材料难度评估
- 自然语言处理预处理

## 测试

```bash
python syllable_utils_test.py
```

## 许可证

MIT License