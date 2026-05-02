# Anagram Utils - 变位词工具模块

提供变位词检测、生成、求解等功能。变位词(Anagram)是指通过重新排列字母顺序而形成的新词或短语。

## 功能特性

- ✅ **变位词检测** - 判断两个字符串是否为变位词
- ✅ **变位词查找** - 在单词列表中查找变位词
- ✅ **变位词分组** - 将单词按变位词分组
- ✅ **排列生成** - 生成文本的所有排列组合
- ✅ **字母组成检测** - 判断是否可以用给定字母组成单词
- ✅ **变位距离计算** - 计算两个字符串的变位距离
- ✅ **变位词求解器** - 高级求解功能，支持索引和批量处理
- ✅ **零外部依赖** - 仅使用 Python 标准库

## 安装使用

```python
# 直接导入使用
from anagram_utils.mod import is_anagram, find_anagrams, AnagramSolver

# 判断变位词
print(is_anagram("listen", "silent"))  # True

# 查找变位词
words = ["listen", "silent", "enlist", "hello"]
print(find_anagrams("listen", words))  # ['silent', 'enlist']
```

## API 参考

### 基本函数

#### `is_anagram(text1, text2, strict=False)`
检测两个字符串是否为变位词。

```python
>>> is_anagram("listen", "silent")
True
>>> is_anagram("A gentleman", "Elegant man")
True
>>> is_anagram("Listen", "silent", strict=True)
False  # 严格模式区分大小写
```

#### `find_anagrams(word, word_list, strict=False)`
在单词列表中查找给定单词的变位词。

```python
>>> find_anagrams("listen", ["listen", "silent", "enlist", "hello"])
['silent', 'enlist']
```

#### `group_anagrams(words)`
将单词列表按变位词分组。

```python
>>> group_anagrams(["listen", "silent", "enlist", "hello", "world"])
[['listen', 'silent', 'enlist'], ['hello'], ['world']]
```

### 生成函数

#### `generate_anagrams(text, min_length=2)`
生成文本的所有可能变位词。

```python
>>> generate_anagrams("abc")
['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
```

#### `generate_permutations(text, max_length=None)`
生成文本的所有排列组合（可跨长度）。

```python
>>> generate_permutations("abc", max_length=2)
['a', 'b', 'c', 'ab', 'ac', 'ba', 'bc', 'ca', 'cb']
```

### 字母组成函数

#### `can_form_word(letters, word)`
判断是否可以用给定字母组成目标单词。

```python
>>> can_form_word("abcdef", "cab")
True
>>> can_form_word("abc", "abcd")
False
```

#### `find_formable_words(letters, word_list, min_length=1)`
从字母池中找出所有可以组成的单词。

```python
>>> find_formable_words("abcde", ["cab", "bad", "ace", "deed"])
['cab', 'bad', 'ace']
```

### 分析函数

#### `anagram_distance(text1, text2)`
计算变位距离（需要移除多少字符才能成为变位词）。

```python
>>> anagram_distance("listen", "silent")
0  # 完全相同
>>> anagram_distance("listen", "list")
2  # 需要移除 e, n
```

#### `anagram_similarity(text1, text2)`
计算变位相似度（0-1）。

```python
>>> anagram_similarity("listen", "silent")
1.0
>>> anagram_similarity("abc", "def")
0.0
```

#### `get_anagram_info(text)`
获取文本的变位词信息。

```python
>>> info = get_anagram_info("listen")
>>> info['length']
6
>>> info['unique_chars']
5
>>> info['permutation_count']
720  # 6!
```

### 工具函数

#### `anagram_signature(text)`
获取变位词签名（排序后的字符），用于快速识别变位词。

```python
>>> anagram_signature("listen")
'eilnst'
>>> anagram_signature("silent")
'eilnst'  # 相同签名 = 变位词
```

#### `subtract_chars(text, to_remove)`
从文本中移除指定字符。

```python
>>> subtract_chars("listen", "sil")
'ten'
```

### AnagramSolver 类

高级变位词求解器，支持索引和批量处理。

```python
>>> solver = AnagramSolver(["listen", "silent", "enlist", "hello"])
>>> solver.find_anagrams("listen")
['silent', 'enlist']
>>> solver.get_stats()
{'total_words': 4, 'anagram_groups_count': 1, ...}
```

## 使用场景

### 1. Scrabble/拼字游戏辅助

```python
letters = "aelrst"
dictionary = ["star", "rats", "slate", "stale", "steal", "alert"]

formable = find_formable_words(letters, dictionary)
print(f"可组成的单词: {formable}")
```

### 2. 文字谜题求解

```python
puzzle = "aelpp"  # apple
from anagram_utils.mod import generate_anagrams
candidates = generate_anagrams(puzzle, min_length=5)
print(f"可能的答案: {candidates}")
```

### 3. 单词分组整理

```python
words = ["race", "care", "acre", "heart", "earth", "python", "typhon"]
groups = group_anagrams(words)
for group in groups:
    if len(group) > 1:
        print(f"变位词组: {group}")
```

### 4. 批量变位词分析

```python
solver = AnagramSolver(word_list)
for group in solver.get_all_anagram_groups():
    print(f"{len(group)} 个变位词: {group}")
```

## 经典变位词示例

| 原词 | 变位词 |
|------|--------|
| listen | silent |
| race | care, acre |
| heart | earth, hater |
| astronomer | moon starer |
| A gentleman | Elegant man |
| William Shakespeare | I am a weakish speller |

## 测试

```bash
python anagram_utils_test.py
```

测试覆盖：
- 基本变位词检测（30+ 测试）
- 变位词查找和分组（15+ 测试）
- 排列生成（10+ 测试）
- 字母组成检测（10+ 测试）
- 变位距离和相似度（10+ 测试）
- AnagramSolver 类（10+ 测试）
- 边界值测试（空字符串、单字符、Unicode 等）

## 许可证

MIT License