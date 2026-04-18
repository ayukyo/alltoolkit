# Rolling Hash Utils 模块报告

## 模块信息
- **模块名称**: rolling_hash_utils
- **位置**: Python/rolling_hash_utils/
- **语言**: Python 3.6+
- **日期**: 2026-04-19

## 核心功能列表

### 类
1. **RollingHash** - 基础滚动哈希类
   - O(1) 时间添加/移除字符
   - 支持自定义基数和模数
   - 支持窗口滑动查看

2. **DoubleRollingHash** - 双重滚动哈希
   - 使用两个不同的哈希函数
   - 碰撞概率极低
   - 返回元组 (hash1, hash2)

3. **RabinKarp** - Rabin-Karp 字符串匹配算法
   - 平均 O(n+m) 时间复杂度
   - 支持 find_all, find_first, count, contains

4. **MultiPatternMatcher** - 多模式匹配器
   - 同时搜索多个模式字符串
   - 按长度分组优化

5. **RollingHashIterator** - 滚动哈希迭代器
   - 遍历所有窗口哈希值
   - 支持单/双重哈希模式

6. **DuplicateDetector** - 重复内容检测器
   - 查找重复内容
   - 统计唯一子串数量

7. **FileFingerprint** - 文件指纹生成器
   - 计算文件/文本指纹
   - Jaccard 相似度计算

### 便捷函数
- `find_all_occurrences(text, pattern)` - 快速查找所有位置
- `find_first_occurrence(text, pattern)` - 快速查找首个位置
- `compute_rolling_hash(text, window_size)` - 计算所有窗口哈希
- `longest_repeated_substring(text)` - 查找最长重复子串

## 测试结果
- **测试数量**: 66 个单元测试
- **测试状态**: 全部通过 ✅
- **测试覆盖**: 10 个测试类
  - TestRollingHash (9 tests)
  - TestDoubleRollingHash (5 tests)
  - TestRabinKarp (11 tests)
  - TestMultiPatternMatcher (10 tests)
  - TestRollingHashIterator (4 tests)
  - TestDuplicateDetector (7 tests)
  - TestFileFingerprint (6 tests)
  - TestConvenienceFunctions (6 tests)
  - TestEdgeCases (6 tests)
  - TestPerformance (3 tests)

## 使用示例

### 基础滚动哈希
```python
from rolling_hash_utils.mod import RollingHash

rh = RollingHash(window_size=5)
rh.extend("hello")
print(rh.get_hash())  # 窗口哈希值
print(rh.get_window())  # "hello"

rh.append('w')
print(rh.get_window())  # "ellow"
```

### Rabin-Karp 搜索
```python
from rolling_hash_utils.mod import RabinKarp, find_all_occurrences

rk = RabinKarp("pattern")
matches = rk.find_all("text with pattern here")
# [10]

# 或使用便捷函数
find_all_occurrences("hello world hello", "hello")  # [0, 12]
```

### 重复检测
```python
from rolling_hash_utils.mod import DuplicateDetector

detector = DuplicateDetector(min_length=10)
duplicates = detector.find_duplicates("repeated text repeated text")
# {'repeated text': [0, 14]}
```

### 文件指纹比较
```python
from rolling_hash_utils.mod import FileFingerprint

fp = FileFingerprint(chunk_size=4096)
fp1 = fp.fingerprint_string("file content A")
fp2 = fp.fingerprint_string("file content B")
similarity = fp.similarity(fp1, fp2)  # 0.0 ~ 1.0
```

## 适用场景
- 大文本搜索匹配
- 代码重复检测
- 文件相似度比较
- DNA/RNA 序列分析
- 抄袭检测
- 日志分析
- 文本差异比对

## 特点
- **零外部依赖** - 纯 Python 标准库实现
- **高效** - O(1) 滚动哈希操作
- **可靠** - 双重哈希减少碰撞
- **Unicode 支持** - 支持中文、日文等任意字符