# Manacher's Algorithm Utils

高效回文检测工具包 - 使用 Manacher 算法在 O(n) 时间复杂度内解决回文相关问题。

## 简介

Manacher 算法是一种经典的字符串算法，专门用于高效处理回文相关问题。相比朴素方法的 O(n²) 复杂度，Manacher 算法能在 O(n) 时间内：

- 找到最长回文子串
- 统计回文子串总数
- 找出所有回文子串
- 检查特定位置的最长回文

## 核心功能

### 1. longest_palindromic_substring(s)
找到字符串中最长的回文子串。

```python
from manacher_utils import longest_palindromic_substring

result = longest_palindromic_substring("babad")
print(result)  # 输出: 'bab' 或 'aba'

result = longest_palindromic_substring("cbbd")
print(result)  # 输出: 'bb'

result = longest_palindromic_substring("racecar")
print(result)  # 输出: 'racecar'
```

### 2. count_palindromic_substrings(s)
统计字符串中回文子串的总数（每个单字符也算一个回文）。

```python
from manacher_utils import count_palindromic_substrings

count = count_palindromic_substrings("abc")
print(count)  # 输出: 3 ('a', 'b', 'c')

count = count_palindromic_substrings("aaa")
print(count)  # 输出: 6 ('a'×3, 'aa'×2, 'aaa'×1)

count = count_palindromic_substrings("aba")
print(count)  # 输出: 4 ('a', 'b', 'a', 'aba')
```

### 3. all_palindromic_substrings(s)
找出所有唯一的回文子串，按长度降序排列。

```python
from manacher_utils import all_palindromic_substrings

palindromes = all_palindromic_substrings("abaab")
print(palindromes)  # 输出: ['aba', 'baab', 'aa', 'a', 'b']
```

### 4. palindrome_info(s)
获取字符串的完整回文信息。

```python
from manacher_utils import palindrome_info

info = palindrome_info("babad")
print(info)
# 输出:
# {
#     'longest': 'bab',
#     'length': 3,
#     'count': 7,
#     'centers': [...],  # 详细回文中心信息
#     'has_palindrome': True
# }
```

### 5. find_palindromes_by_length(s, min_length)
找出满足最小长度要求的回文子串。

```python
from manacher_utils import find_palindromes_by_length

# 找出长度 >= 3 的回文
palindromes = find_palindromes_by_length("abaab", 3)
print(palindromes)  # 输出: ['aba', 'baab']

# 找出长度 >= 4 的回文
palindromes = find_palindromes_by_length("abaab", 4)
print(palindromes)  # 输出: ['baab']
```

### 6. longest_palindrome_at(s, position)
找出以特定位置为中心的最长回文。

```python
from manacher_utils import longest_palindrome_at

# 以位置 1 为中心的最长回文
result = longest_palindrome_at("babad", 1)
print(result)  # 输出: 'bab'

# 以位置 3 为中心的最长回文
result = longest_palindrome_at("racecar", 3)
print(result)  # 输出: 'racecar'
```

### 7. is_palindrome(s, start, end)
检查子串是否为回文。

```python
from manacher_utils import is_palindrome

result = is_palindrome("abaab", 0, 3)
print(result)  # 输出: True ('aba' 是回文)

result = is_palindrome("abaab", 1, 4)
print(result)  # 输出: False ('baa' 不是回文)
```

## 算法原理

Manacher 算法的核心思想：

1. **预处理**：在原字符串中插入特殊字符，统一处理奇偶长度回文
   - `"abc"` → `"^#a#b#c#$"` （添加边界哨兵避免越界检查）

2. **利用对称性**：当当前位置在已知回文范围内时，利用镜像位置的已知信息

3. **动态扩展**：对于超出当前范围的回文，逐个比较扩展

### 时间复杂度分析

- **预处理**：O(n)
- **主算法**：每个位置最多被访问两次，总 O(n)
- **查询操作**：O(1) 或 O(n)，取决于是否需要预处理

### 空间复杂度

- O(n) 用于存储预处理后的字符串和半径数组

## 适用场景

- 字符串分析
- 文本处理
- DNA/RNA 序列分析（回文结构常见）
- 数据验证
- 算法竞赛

## 性能对比

| 字符串长度 | 朴素方法 O(n²) | Manacher O(n) |
|-----------|---------------|---------------|
| 1,000     | ~1ms          | ~0.1ms        |
| 10,000    | ~100ms        | ~1ms          |
| 100,000   | ~10s          | ~10ms         |
| 1,000,000 | ~1000s        | ~100ms        |

## 运行测试

```bash
python manacher_utils_test.py
```

测试覆盖：
- 边界情况（空字符串、单字符）
- 基本功能测试
- 性能测试（10000+ 字符）
- 正确性验证

## 技术细节

- **零外部依赖**：纯 Python 实现
- **兼容性**：Python 3.6+
- **无副作用**：所有函数不修改输入

## 作者

AllToolkit 自动生成模块
日期：2026-05-01