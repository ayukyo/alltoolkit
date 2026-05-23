# Palindrome Utils

回文检测和处理工具模块。

## 功能

- **回文检测** - 判断字符串是否为回文
- **子串查找** - 查找所有回文子串
- **最长回文** - 查找最长回文子串
- **回文计数** - 统计文本中的回文数量
- **回文生成** - 通过最小添加生成回文
- **多语言支持** - 支持中文、英文等多种语言
- **灵活配置** - 大小写敏感、忽略标点等选项

## 安装

```python
from palindrome_utils.mod import is_palindrome, find_palindromes, longest_palindrome
```

## 快速开始

### 回文检测

```python
from palindrome_utils.mod import is_palindrome

# 基本检测
print(is_palindrome("racecar"))  # True
print(is_palindrome("hello"))    # False

# 忽略标点和空格
print(is_palindrome("A man, a plan, a canal: Panama"))  # True

# 大小写敏感
print(is_palindrome("Race Car", case_sensitive=True))  # False
print(is_palindrome("Race Car", case_sensitive=False)) # True

# 中文回文
print(is_palindrome("上海自来水来自海上"))  # True
print(is_palindrome("黄山落叶松叶落山黄"))  # True
```

### 查找回文子串

```python
from palindrome_utils.mod import find_palindromes, PalindromeMatch

# 查找所有回文子串
matches = find_palindromes("ababa")
for match in matches:
    print(f"'{match.text}' at position {match.start}-{match.end}")

# 输出:
# 'a' at position 0-0
# 'aba' at position 0-2
# 'ababa' at position 0-4
# 'b' at position 1-1
# 'bab' at position 1-3
# ...

# 查找最长回文
longest = find_palindromes("ababa", longest_only=True)
print(longest)  # PalindromeMatch('ababa', pos=0-4)
```

### 最长回文子串

```python
from palindrome_utils.mod import longest_palindrome

# 使用 Manacher 算法 O(n)
result = longest_palindrome("babad")
print(result)  # "bab" 或 "aba"

result = longest_palindrome("cbbd")
print(result)  # "bb"
```

### 回文生成

```python
from palindrome_utils.mod import make_palindrome

# 通过添加最少字符生成回文
result = make_palindrome("abc")
print(result)  # "abcba"

result = make_palindrome("ab")
print(result)  # "aba" 或 "bab"

# 添加到前面
result = make_palindrome("abc", prepend=True)
print(result)  # "cbabc"
```

### 统计回文

```python
from palindrome_utils.mod import count_palindromes

# 统计所有回文子串数量
count = count_palindromes("aaa")
print(count)  # 6 (a, a, a, aa, aa, aaa)

# 统计不重复回文子串
count = count_palindromes("aaa", unique=True)
print(count)  # 3 (a, aa, aaa)
```

### 回文评分

```python
from palindrome_utils.mod import palindrome_score

# 评估字符串的"回文度"
score = palindrome_score("racecar")
print(score)  # 1.0 (完全回文)

score = palindrome_score("hello")
print(score)  # 较低分数

score = palindrome_score("abccba")
print(score)  # 1.0
```

## API 参考

### 主要函数

| 函数 | 说明 |
|------|------|
| `is_palindrome(s, ...)` | 判断是否为回文 |
| `find_palindromes(s, ...)` | 查找所有回文子串 |
| `longest_palindrome(s)` | 查找最长回文子串 |
| `count_palindromes(s, ...)` | 统计回文数量 |
| `make_palindrome(s, ...)` | 生成回文 |
| `palindrome_score(s)` | 计算回文度评分 |

### PalindromeMatch

| 属性 | 说明 |
|------|------|
| `text` | 回文文本 |
| `start` | 起始位置 |
| `end` | 结束位置 |
| `length` | 长度 |

### 选项参数

```python
is_palindrome(
    s,                    # 要检测的字符串
    case_sensitive=False, # 是否区分大小写
    alnum_only=True,      # 是否只考虑字母数字
    ignore_spaces=True,   # 是否忽略空格
    ignore_punctuation=True # 是否忽略标点
)
```

## 算法

- **Manacher 算法** - O(n) 时间查找最长回文子串
- **中心扩展法** - O(n²) 时间查找所有回文子串
- **动态规划** - 用于回文生成和计数

## 测试

```bash
cd Python/palindrome_utils
python palindrome_utils_test.py
```

测试覆盖率：
- 基本回文检测
- 大小写敏感/不敏感
- 忽略标点和空格
- 中文回文
- 回文子串查找
- 最长回文
- 回文生成
- 边界值测试

## 许可证

MIT License