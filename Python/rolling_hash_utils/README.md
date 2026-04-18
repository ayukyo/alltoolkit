# Rolling Hash Utils

Python 滚动哈希工具模块，提供高效的字符串匹配、重复检测、文件指纹等功能。

## 功能特性

### 核心类

- **RollingHash** - 基础滚动哈希，支持 O(1) 窗口滑动
- **DoubleRollingHash** - 双重哈希，极大减少碰撞概率
- **RabinKarp** - Rabin-Karp 字符串匹配算法
- **MultiPatternMatcher** - 多模式同时匹配
- **RollingHashIterator** - 滚动窗口迭代器
- **DuplicateDetector** - 重复内容检测器
- **FileFingerprint** - 文件指纹生成器

### 主要功能

1. **高效字符串匹配** - Rabin-Karp 算法平均 O(n+m) 复杂度
2. **多模式匹配** - 同时搜索多个模式字符串
3. **重复检测** - 快速发现重复内容
4. **文件指纹** - 计算和比较文件相似度
5. **最长重复子串** - 自动查找最长重复片段
6. **Unicode 支持** - 支持中文、日文等任意字符

## 安装

```python
# 无需安装，直接导入使用
from rolling_hash_utils.mod import RollingHash, RabinKarp
```

## 快速使用

### 基础滚动哈希

```python
from rolling_hash_utils.mod import RollingHash

rh = RollingHash(window_size=5)
rh.extend("hello")
print(rh.get_hash())  # 当前窗口哈希值
print(rh.get_window())  # "hello"

rh.append('w')  # 添加新字符
print(rh.get_window())  # "ellow"  # 自动滑动
```

### Rabin-Karp 搜索

```python
from rolling_hash_utils.mod import RabinKarp

rk = RabinKarp("pattern")
matches = rk.find_all("text with pattern here and pattern there")
print(matches)  # [10, 30]  # 所有匹配位置

# 便捷函数
from rolling_hash_utils.mod import find_all_occurrences
find_all_occurrences("hello world hello", "hello")  # [0, 12]
```

### 多模式匹配

```python
from rolling_hash_utils.mod import MultiPatternMatcher

matcher = MultiPatternMatcher(["error", "warning", "info"])
results = matcher.find_all("error: failed, warning: check, info: ok")
# {'error': [0], 'warning': [17], 'info': [36]}
```

### 重复检测

```python
from rolling_hash_utils.mod import DuplicateDetector

detector = DuplicateDetector(min_length=10)
duplicates = detector.find_duplicates("some repeated text repeated text here")
# {'repeated text': [5, 22]}
```

### 文件指纹比较

```python
from rolling_hash_utils.mod import FileFingerprint

fp = FileFingerprint(chunk_size=4096)
fp1 = fp.fingerprint_string("file content A")
fp2 = fp.fingerprint_string("file content B")
similarity = fp.similarity(fp1, fp2)  # 0.0 ~ 1.0
```

## API 文档

### RollingHash

```python
RollingHash(window_size, base=256, mod=2**61-1)
```

- `append(char)` - 添加字符，返回新哈希值
- `extend(text)` - 批量添加文本
- `reset()` - 重置状态
- `get_hash()` - 获取当前哈希值
- `get_window()` - 获取当前窗口内容
- `is_full()` - 窗口是否已满

### RabinKarp

```python
RabinKarp(pattern)
```

- `find_all(text)` - 查找所有匹配位置
- `find_first(text)` - 查找第一个匹配位置
- `count(text)` - 统计匹配次数
- `contains(text)` - 检查是否包含模式

### DuplicateDetector

```python
DuplicateDetector(min_length=10, double_hash=True)
```

- `find_duplicates(text)` - 查找所有重复内容
- `has_duplicates(text)` - 检查是否有重复
- `count_unique_substrings(text)` - 统计唯一子串数量

### 便捷函数

- `find_all_occurrences(text, pattern)` - 快速查找所有位置
- `find_first_occurrence(text, pattern)` - 快速查找首个位置
- `compute_rolling_hash(text, window_size)` - 计算所有窗口哈希
- `longest_repeated_substring(text)` - 查找最长重复子串

## 性能特点

- **滚动哈希** - O(1) 添加/移除字符
- **Rabin-Karp** - 平均 O(n+m) 搜索
- **双重哈希** - 碰撞概率极低
- **零依赖** - 纯 Python 标准库实现

## 适用场景

- 大文本搜索匹配
- 代码重复检测
- 文件相似度比较
- DNA/RNA 序列分析
- 抄袭检测
- 日志分析
- 文本差异比对

## 许可证

MIT License