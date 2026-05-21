# Verb Conjugation Utils - 动词变位工具

Python 动词变位工具集，支持英语动词的完整变位功能。零外部依赖，仅使用 Python 标准库。

## 功能列表

### 核心功能

| 功能 | 函数 | 说明 |
|------|------|------|
| 动词变位 | `conjugate()` | 单个时态和人称的变位 |
| 全部变位 | `conjugate_all_forms()` | 获取所有变位形式 |
| 动词信息 | `get_verb_info()` | 获取动词详细信息 |
| 变位表格 | `generate_verb_table()` | 生成完整变位表格 |

### 支持的时态

- **Present Simple** (现在简单时)
- **Present Continuous** (现在进行时)
- **Past Simple** (过去简单时)
- **Past Continuous** (过去进行时)
- **Future Simple** (将来简单时)
- **Future Continuous** (将来进行时)
- **Present Perfect** (现在完成时)
- **Past Perfect** (过去完成时)
- **Future Perfect** (将来完成时)
- **Conditional** (条件句)
- **Conditional Perfect** (条件完成时)
- **Imperative** (祈使句)
- **Gerund** (动名词)
- **Participle** (分词)

### 支持的人称

- **First Singular** (I - 第一人称单数)
- **First Plural** (We - 第一人称复数)
- **Second Singular** (You - 第二人称单数)
- **Second Plural** (You - 第二人称复数)
- **Third Singular** (He/She/It - 第三人称单数)
- **Third Plural** (They - 第三人称复数)

### 辅助功能

| 功能 | 函数 | 说明 |
|------|------|------|
| 不规则动词列表 | `list_irregular_verbs()` | 列出所有内置不规则动词 |
| 检测不规则动词 | `is_irregular_verb()` | 检查动词是否不规则 |
| 分词形式 | `get_participle_forms()` | 获取现在/过去分词 |
| 过去形式 | `get_past_forms()` | 获取过去式/过去分词 |
| 动词类型检测 | `detect_verb_type()` | 检测动词属性 |
| 拼写建议 | `suggest_spelling()` | 建议正确拼写 |
| 动词比较 | `compare_verbs()` | 比较两个动词 |
| 创建句子 | `create_sentence()` | 创建完整句子 |

## 快速开始

```python
from mod import conjugate, Tense, Person, conjugate_all_forms

# 1. 基本变位
result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR)
print(result.conjugated)  # "walks"

# 2. 过去时
result = conjugate("go", Tense.PAST_SIMPLE, Person.FIRST_SINGULAR)
print(result.conjugated)  # "went"

# 3. 现在进行时
result = conjugate("work", Tense.PRESENT_CONTINUOUS, Person.FIRST_SINGULAR)
print(result.conjugated)  # "am working"

# 4. 现在完成时
result = conjugate("write", Tense.PRESENT_PERFECT, Person.THIRD_SINGULAR)
print(result.conjugated)  # "has written"

# 5. 否定形式
result = conjugate("play", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR, negative=True)
print(result.negative)  # "does not play"

# 6. 疑问形式
result = conjugate("play", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, interrogative=True)
print(result.interrogative)  # "Do I play"
```

## 函数详解

### conjugate()

动词变位核心函数。

```python
conjugate(verb, tense, person, language, mood, negative, interrogative)
```

参数：
- `verb`: 动词原形 (str)
- `tense`: 时态 (Tense 枚举)
- `person`: 人称 (Person 枚举)
- `language`: 语言 (Language 枚举，默认 ENGLISH)
- `mood`: 语气 (Mood 枚举，默认 INDICATIVE)
- `negative`: 否定形式 (bool，默认 False)
- `interrogative`: 疑问形式 (bool，默认 False)

返回：
- `ConjugationResult` 数据类，包含变位结果、否定形式、疑问形式

### conjugate_all_forms()

获取动词的所有变位形式。

```python
conjugate_all_forms(verb, language)
```

返回：
- 包含所有时态和人称变位结果的字典

### get_verb_info()

获取动词的详细信息。

```python
get_verb_info(verb, language)
```

返回：
- `VerbInfo` 数据类，包含原形、过去式、过去分词、现在分词等

### create_sentence()

创建完整句子。

```python
create_sentence(verb, tense, person, subject, object, negative, interrogative)
```

参数：
- `verb`: 动词
- `tense`: 时态
- `person`: 人称
- `subject`: 自定义主语（可选）
- `object`: 宾语（可选）
- `negative`: 是否否定
- `interrogative`: 是否疑问

返回：
- 完整句子字符串

## 不规则动词

内置超过 100 个常见英语不规则动词，包括：

- be, have, do, say, go, get, make, know
- think, take, see, come, want, look, use
- find, give, tell, work, call, try, ask
- feel, become, leave, put, mean, keep, let
- begin, seem, help, show, hear, play, run
- 等更多...

规则动词会自动根据拼写规则进行变位。

## 测试

运行测试：

```bash
python -m pytest verb_conjugation_utils_test.py -v
```

或使用 unittest：

```bash
python verb_conjugation_utils_test.py
```

## 使用场景

1. **语言学习应用**: 生成动词变位练习题
2. **自然语言处理**: 语法分析和句子生成
3. **教育软件**: 英语语法教学辅助
4. **写作工具**: 检查动词形式正确性
5. **翻译系统**: 动词变位参考

## 依赖

- Python >= 3.7
- 仅使用标准库 (dataclasses, typing, enum, re)

## 版本历史

- v1.0.0 (2026-05-22): 初始版本，支持英语动词完整变位

## 许可

MIT License