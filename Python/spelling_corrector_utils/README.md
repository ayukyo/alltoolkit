# spelling_corrector_utils - 拼写纠正工具

提供英文单词拼写检查和自动纠正功能，基于编辑距离和词频统计。

## 功能特性

- ✅ **拼写检查** - 检查单词是否拼写正确
- ✅ **自动纠正** - 自动修复拼写错误
- ✅ **建议列表** - 提供多个可能的正确拼写
- ✅ **批量处理** - 支持批量纠正和文本纠正
- ✅ **自定义词典** - 添加专业术语或新词
- ✅ **常见错误映射** - 内置常见英语拼写错误
- ✅ **零外部依赖** - 纯 Python 实现

## 安装

无需安装，直接复制 `spelling_corrector_utils` 文件夹到项目中即可使用。

## 快速开始

```python
from spelling_corrector_utils.mod import SpellingCorrector

# 创建纠正器实例
corrector = SpellingCorrector()

# 检查拼写
print(corrector.is_correct('hello'))  # True
print(corrector.is_correct('speling'))  # False

# 自动纠正
print(corrector.correct('speling'))  # 'spelling'
print(corrector.correct('wrld'))  # 'world'

# 获取建议
suggestions = corrector.get_suggestions('speling', limit=3)
# [('spelling', 100), ('spine', 50), ('spilling', 30)]
```

## 便捷函数

无需创建实例，直接使用模块级函数：

```python
from spelling_corrector_utils.mod import (
    is_correct, correct, get_suggestions,
    batch_correct, correct_text, add_word
)

# 拼写检查
is_correct('hello')  # True

# 自动纠正
correct('speling')  # 'spelling'

# 获取建议
get_suggestions('wrld', limit=3)

# 批量纠正
batch_correct(['hello', 'wrld', 'pyton'])
# ['hello', 'world', 'python']

# 文本纠正
correct_text("Hello wrld! How are yuo?")
# 'Hello world! How are you?'

# 添加自定义词汇
add_word('pythonista', 5000)
```

## 核心功能

### 拼写检查

```python
corrector = SpellingCorrector()

# 检查单个单词
corrector.is_correct('hello')  # True
corrector.is_correct('speling')  # False
```

### 自动纠正

```python
# 基于编辑距离自动纠正
corrector.correct('speling')  # 'spelling'
corrector.correct('wrld')  # 'world'
corrector.correct('korrecter')  # 'corrector'

# 保持大小写
corrector.correct('SPILING')  # 'SPELLING'
corrector.correct('Speling')  # 'Spelling'
```

### 获取建议

```python
# 获取多个可能的正确拼写
suggestions = corrector.get_suggestions('speling', limit=5)
# 返回: [('spelling', 频率), ('spine', 频率), ...]

# 控制最大编辑距离
suggestions = corrector.get_suggestions('korrecter', max_distance=2)
```

### 批量操作

```python
# 批量纠正单词列表
words = ['hello', 'wrld', 'pyton', 'programing']
corrected = corrector.batch_correct(words)
# ['hello', 'world', 'python', 'programming']

# 纠正整段文本
text = "Hello wrld! Python is an amazing programing languge."
result = corrector.correct_text(text)
# "Hello world! Python is an amazing programming language."
```

## 自定义词典

### 添加单个词汇

```python
corrector = SpellingCorrector()

# 添加专业术语
corrector.add_word('pythonista', frequency=5000)
corrector.add_word('devops', frequency=4000)

# 现在可以识别
corrector.is_correct('pythonista')  # True
```

### 添加拼写错误映射

```python
# 添加自定义的常见错误映射
corrector.add_misspelling('pyton', 'python')
corrector.add_misspelling('js', 'javascript')

# 直接纠正
corrector.correct('pyton')  # 'python'
```

### 从文本学习

```python
# 从文本中提取词汇并添加到词典
text = """
TensorFlow is an open-source machine learning framework.
PyTorch is another popular deep learning library.
"""
corrector.add_words_from_text(text)
```

## 常见拼写错误

内置 100+ 常见英语拼写错误映射：

| 错误拼写 | 正确拼写 |
|---------|---------|
| teh | the |
| thier | their |
| recieve | receive |
| occured | occurred |
| seperate | separate |
| definately | definitely |
| accomodate | accommodate |
| acheive | achieve |
| grammer | grammar |
| neccessary | necessary |

## 原理说明

基于 Peter Norvig 的拼写纠正算法：

1. **编辑距离生成**：生成编辑距离为 1-2 的候选词
   - 删除：`speling` → `peling`
   - 插入：`speling` → `spelling`
   - 替换：`speling` → `speling`
   - 交换：`speling` → `speilng`

2. **候选筛选**：筛选出词典中存在的词汇

3. **词频排序**：按词频选择最可能的正确拼写

4. **常见错误映射**：优先匹配常见拼写错误

## 性能特点

- 内置 ~500 高频英语词汇
- 支持 100+ 常见拼写错误映射
- 编辑距离 1 的纠正速度：~1000 词/秒
- 编辑距离 2 的纠正速度：~100 词/秒

## 运行测试

```bash
# 运行单元测试
python -m spelling_corrector_utils.spelling_corrector_utils_test

# 运行示例
python spelling_corrector_utils/examples/usage_examples.py
```

## 文件结构

```
spelling_corrector_utils/
├── mod.py                      # 核心模块
├── spelling_corrector_utils_test.py  # 单元测试
├── README.md                   # 说明文档
└── examples/
    └── usage_examples.py       # 使用示例
```

## 适用场景

- 文本编辑器的拼写检查
- 搜索查询纠正
- 表单输入验证
- 文档校对工具
- 自然语言处理预处理

## 限制

- 仅支持英文
- 不考虑上下文（同音异义词可能混淆）
- 编辑距离超过 2 的错误可能无法纠正
- 专业术语需要手动添加

## 许可证

MIT License