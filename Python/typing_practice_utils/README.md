# Typing Practice Utils - 打字练习工具

零外部依赖的 Python 打字练习工具库，支持多种练习模式、速度计算和准确率分析。

## 安装

无需安装，直接导入使用：

```python
from mod import TypingPractice, TextGenerator, TypingAnalyzer
```

## 快速开始

### 生成练习文本

```python
from mod import TextGenerator, Difficulty, TextType

# 生成简单单词练习（20个单词）
text = TextGenerator.generate_words(20, Difficulty.EASY)
print(text)
# 输出: the be to of and a in that have I it for not on with...

# 生成困难单词练习
text = TextGenerator.generate_words(10, Difficulty.HARD)
print(text)
# 输出: synchronization asynchronous polymorphism encapsulation...

# 生成句子练习
text = TextGenerator.generate_sentence()
print(text)
# 输出: The quick brown fox jumps over the lazy dog.

# 生成代码练习
text = TextGenerator.generate_code(5)
print(text)
# 输出:
# def hello_world():
#     print('Hello, World!')
# for i in range(10):
#     print(i)

# 生成数字练习
text = TextGenerator.generate_numbers(10)
print(text)
# 输出: 123 456.78 9,876,543 000 1234...

# 生成混合练习
text = TextGenerator.generate_mixed(50)
print(text)
# 输出: computer 42 ! keyboard 3.14...
```

### 分析打字结果

```python
from mod import TypingAnalyzer

original = "The quick brown fox"
typed = "The quikc brown fox"  # 有一个拼写错误
time_seconds = 8.5

result = TypingAnalyzer.analyze(original, typed, time_seconds)

print(f"WPM: {result.wpm}")           # 每分钟单词数
print(f"CPM: {result.cpm}")           # 每分钟字符数
print(f"准确率: {result.accuracy}%")   # 准确率
print(f"错误数: {len(result.errors)}") # 错误详情
```

### 完整练习会话

```python
from mod import TypingPractice, TextType, Difficulty

practice = TypingPractice()

# 开始练习会话
text = practice.start_session(TextType.WORDS, Difficulty.MEDIUM, count=15)
print(f"请输入: {text}")

# 用户开始输入时开始计时
practice.begin_typing()

# 假设用户输入了...
typed_text = input("请输入上面的文本: ")

# 结束并分析
result = practice.finish_typing(typed_text)
print(result)

# 查看历史统计
stats = practice.get_statistics()
print(f"平均WPM: {stats['average_wpm']}")
print(f"平均准确率: {stats['average_accuracy']}%")
```

### 使用便捷函数

```python
from mod import generate_practice_text, analyze_typing, quick_practice

# 快速生成练习文本
text = generate_practice_text(TextType.SENTENCES, Difficulty.MEDIUM)
print(text)

# 快速分析
result = analyze_typing("hello world", "hello world", 5.0)
print(f"WPM: {result.wpm}, 准确率: {result.accuracy}%")

# 快速练习（返回文本和完成函数）
text, finish = quick_practice(Difficulty.EASY, 10)
print(f"练习文本: {text}")
# 用户输入后...
result = finish(text)  # 传入用户输入
print(result)
```

## 功能列表

### 文本生成器 (TextGenerator)

| 方法 | 说明 |
|------|------|
| `generate_words(count, difficulty)` | 生成单词练习文本 |
| `generate_sentence(difficulty)` | 生成句子练习文本 |
| `generate_paragraph(sentences)` | 生成段落练习文本 |
| `generate_code(lines)` | 生成代码练习文本 |
| `generate_numbers(count)` | 生成数字练习文本 |
| `generate_mixed(length)` | 生成混合练习文本 |
| `generate(text_type, difficulty, **kwargs)` | 通用生成方法 |

### 打字分析器 (TypingAnalyzer)

| 方法 | 说明 |
|------|------|
| `calculate_wpm(text, time_seconds)` | 计算每分钟单词数 |
| `calculate_cpm(text, time_seconds)` | 计算每分钟字符数 |
| `calculate_accuracy(original, typed)` | 计算准确率 |
| `analyze(original, typed, time_seconds)` | 完整分析，返回 TypingResult |

### TypingPractice 类

| 方法 | 说明 |
|------|------|
| `start_session(text_type, difficulty, **kwargs)` | 开始练习会话 |
| `begin_typing()` | 开始计时 |
| `finish_typing(typed_text)` | 结束并分析 |
| `get_statistics()` | 获取历史统计 |
| `clear_history()` | 清除历史 |
| `get_performance_level(wpm)` | 获取性能等级（静态方法） |

### TypingResult 数据类

| 属性 | 类型 | 说明 |
|------|------|------|
| `original_text` | str | 原始文本 |
| `typed_text` | str | 输入文本 |
| `time_seconds` | float | 用时（秒） |
| `correct_chars` | int | 正确字符数 |
| `total_chars` | int | 总字符数 |
| `errors` | List | 错误列表 [(位置, 期望, 实际)] |
| `wpm` | float | 每分钟单词数 |
| `cpm` | float | 每分钟字符数 |
| `accuracy` | float | 准确率（百分比） |

## 难度等级

```python
class Difficulty(Enum):
    EASY = "easy"       # 简单：常用单词
    MEDIUM = "medium"   # 中等：技术词汇
    HARD = "hard"       # 困难：复杂单词
    EXPERT = "expert"   # 专家：混合难度
```

## 文本类型

```python
class TextType(Enum):
    WORDS = "words"           # 单词
    SENTENCES = "sentences"   # 句子
    PARAGRAPHS = "paragraphs" # 段落
    CODE = "code"             # 代码
    NUMBERS = "numbers"       # 数字
    MIXED = "mixed"           # 混合
```

## 性能等级

根据 WPM（每分钟单词数）评定：

| WPM 范围 | 等级 |
|----------|------|
| < 20 | 初级 (Beginner) |
| 20-29 | 入门 (Elementary) |
| 30-39 | 中级 (Intermediate) |
| 40-49 | 熟练 (Proficient) |
| 50-59 | 精通 (Advanced) |
| 60-79 | 专家 (Expert) |
| ≥ 80 | 大师 (Master) |

## 示例输出

```
练习文本: the be to of and a in that have I it for not on with he as you do
请输入上面的文本: the be to of and a in that have I it for not on with he as you do

TypingResult(
  时间: 12.5秒
  WPM: 36.8
  CPM: 184.0
  准确率: 100.0%
  正确字符: 53/53
  错误数: 0
)

性能等级: 中级 (Intermediate)
```

## 特性

- ✅ 零外部依赖，纯 Python 标准库
- ✅ 支持多种练习模式（单词、句子、代码、数字等）
- ✅ 四个难度等级
- ✅ 精确的 WPM/CPM 计算
- ✅ 详细的错误分析
- ✅ 历史统计功能
- ✅ 性能等级评定

## 许可证

MIT License