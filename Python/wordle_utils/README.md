# Wordle 游戏辅助工具

零依赖的 Wordle 游戏辅助 Python 模块，提供单词过滤、最优猜测计算、自动求解等功能。

## 功能特性

- ✅ **单词过滤** - 根据正确位置、存在字母、不存在字母等条件过滤候选词
- ✅ **最优猜测计算** - 支持多种方法（频率法、位置法、熵法、综合法）
- ✅ **自动求解** - 自动玩 Wordle 游戏
- ✅ **字母频率分析** - 计算字母频率和位置频率
- ✅ **内置词库** - 约500个常见5字母英语单词
- ✅ **零外部依赖** - 纯 Python 实现

## 安装使用

```python
from wordle_utils import WordleHelper, WordleSolver, filter_words, get_best_guess
```

## 快速示例

### 基本过滤

```python
from wordle_utils import filter_words

# 第3位是 'a'
result = filter_words(correct="..a..")

# 含 'e' 但不含 'xyz'
result = filter_words(present="e", absent="xyz")

# 组合过滤
result = filter_words(correct="..a..", present="e", absent="xyz")
```

### 获取最优猜测

```python
from wordle_utils import get_best_guess

# 使用默认方法
word, score = get_best_guess()
print(f"推荐: {word}")

# 指定方法
word, score = get_best_guess(method="entropy")  # 信息熵法
```

### 使用 WordleHelper 类

```python
from wordle_utils import WordleHelper

helper = WordleHelper()

# 获取最优首词
best_word, score = helper.get_best_guess(method="combined")

# 根据反馈过滤
candidates = helper.filter_words(
    correct="..n..",  # 第3位是 n
    present="ae",     # 包含 a 和 e
    absent="xyz"      # 不含 x, y, z
)

# 获取候选词中的最优
word, score = helper.get_best_guess(candidates=candidates)
```

### 自动求解

```python
from wordle_utils import WordleSolver

solver = WordleSolver()

# 自动求解指定答案
success, attempts, history = solver.auto_solve("apple", verbose=True)
# 输出: 🎉 成功！用了 X 次猜中！

# 自定义首次猜测
solver.auto_solve("crane", first_guess="crane", verbose=True)
```

### 反馈分析

```python
helper = WordleHelper()

# 分析反馈: y=黄色(存在位置错), g=绿色(正确), b=灰色(不存在)
conditions = helper.analyze_feedback("crane", "yybgb")
# 返回: {correct, pattern, present, absent, yellow_positions}

# 获取下一个推荐猜测
word, candidates, count = helper.suggest_next_guess([
    ("crane", "yybgb")
])
```

## API 文档

### WordleHelper

主要的辅助类。

**方法:**

- `filter_words(**kwargs)` - 过滤单词
  - `correct` / `pattern`: 正确位置的字母（用 `.` 表示未知）
  - `present`: 存在但位置错误的字母
  - `absent` / `not_contains`: 不存在的字母
  - `contains`: 必须包含的字母
  - `starts_with`: 开头字母
  - `ends_with`: 结尾字母
  - `regex`: 正则表达式

- `get_best_guess(candidates, method)` - 获取最优猜测
  - `method`: `"frequency"` | `"position"` | `"entropy"` | `"combined"`

- `analyze_feedback(guess, feedback)` - 分析反馈
  - 反馈格式: `g`/`2`/`=`=绿色, `y`/`1`/`?`=黄色, `b`/`0`/`x`=灰色

- `suggest_next_guess(history)` - 建议下一猜测

### WordleSolver

自动求解器。

**方法:**

- `get_first_guess(method)` - 获取首次猜测
- `submit_feedback(guess, feedback)` - 提交反馈
- `get_next_guess(method)` - 获取下一猜测
- `auto_solve(answer, max_attempts, first_guess, method, verbose)` - 自动求解

### 便捷函数

- `filter_words(words, **kwargs)` - 快速过滤
- `get_best_guess(words, method)` - 快速获取最优
- `calculate_letter_frequency(words)` - 计算字母频率

## 算法说明

### 频率法 (frequency)

基于字母在词库中的出现频率，优先选择高频字母多的词。

### 位置法 (position)

基于字母在各位置的频率分布，优先选择每个位置最常见的字母。

### 熵法 (entropy)

基于信息熵计算，选择能最大化减少候选词数量的词。

### 综合法 (combined)

综合频率、位置和字母多样性，平衡各项指标。

## 自定义词库

```python
custom_words = ["apple", "beach", "crane", "dream", "eagle"]
helper = WordleHelper(custom_words)
solver = WordleSolver(custom_words)
```

## 运行测试

```bash
python -m pytest wordle_utils_test.py
# 或
python wordle_utils_test.py
```

## 运行示例

```bash
python examples.py
```

## 词库说明

内置约500个常见5字母英语单词，包括常用动词、名词等。词库可通过自定义扩展。

## License

MIT