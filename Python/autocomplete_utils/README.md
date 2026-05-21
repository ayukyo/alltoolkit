# Autocomplete Utils

自动补全工具模块，提供完整的自动补全实现，零外部依赖。

## 功能特性

- **Trie 自动补全**: 前缀匹配、按频率排序、持久化
- **N-gram 自动补全**: 基于 Jaccard 相似度的模糊匹配
- **混合自动补全**: 结合 Trie + N-gram 的优势
- **模糊搜索**: 编辑距离模糊匹配
- **权重排序**: 按频率、热度、相关性排序
- **序列化支持**: JSON 导入/导出

## 快速开始

```python
from autocomplete_utils.mod import TrieAutocomplete, create_autocomplete

# 创建自动补全器
words = ['apple', 'application', 'app', 'banana', 'band', 'bandana']
ac = create_autocomplete(words)

# 前缀搜索
results = ac.search('app')
# [Suggestion(text='app', score=1.0, freq=1),
#  Suggestion(text='apple', score=1.0, freq=1),
#  Suggestion(text='application', score=1.0, freq=1)]
```

## 使用示例

### Trie 自动补全

```python
from autocomplete_utils.mod import TrieAutocomplete

# 创建 Trie 补全器
trie = TrieAutocomplete(case_sensitive=False, max_suggestions=10)

# 插入单词
trie.insert('apple', frequency=100)
trie.insert('application', frequency=50)
trie.insert('app', frequency=200)
trie.insert('banana', frequency=30)

# 前缀搜索
results = trie.search('app')
for r in results:
    print(f"{r.text} (freq={r.frequency}, score={r.score})")

# 检查单词是否存在
trie.contains('apple')  # True

# 获取单词信息
trie.get_word_info('apple')  # {'word': 'apple', 'frequency': 100, 'metadata': {}}

# 增加频率
trie.increment_frequency('apple', 10)
```

### 模糊搜索

```python
# 模糊搜索（允许编辑距离）
results = trie.fuzzy_search('aple', max_distance=2)
# 匹配 'apple'（编辑距离=1）

# 使用 Levenshtein 距离函数
from autocomplete_utils.mod import levenshtein_distance
dist = levenshtein_distance('apple', 'aple')  # 1
```

### N-gram 自动补全

```python
from autocomplete_utils.mod import NGramAutocomplete

# 创建 N-gram 补全器
ngram = NGramAutocomplete(n=2, case_sensitive=False)
ngram.insert_batch(['apple', 'application', 'banana'])

# 搜索（基于 Jaccard 相似度）
results = ngram.search('apl')
# 通过 N-gram 重叠找到相似单词

# 前缀搜索
results = ngram.prefix_search('app')
```

### 混合自动补全

```python
from autocomplete_utils.mod import HybridAutocomplete

# 创建混合补全器（结合 Trie + N-gram）
hybrid = HybridAutocomplete(
    case_sensitive=False,
    max_suggestions=10,
    fuzzy_weight=0.5  # 模糊匹配权重
)

hybrid.insert('apple', frequency=100)
hybrid.insert('application', frequency=50)

# 精确前缀匹配 + 模糊匹配结合
results = hybrid.search('app', fuzzy=True)
```

### 批量操作

```python
# 批量插入
words = ['apple', 'banana', 'cherry']
frequencies = [100, 50, 30]
trie.insert_batch(words, frequencies)

# 获取所有单词
all_words = trie.get_all_words()

# 统计信息
stats = trie.get_stats()
# {'word_count': 3, 'total_frequency': 180, 'avg_frequency': 60, ...}
```

### 序列化

```python
# 导出为 JSON
json_str = trie.to_json()

# 从 JSON 导入
trie2 = TrieAutocomplete.from_json(json_str)

# 导出为字典
data = trie.to_dict()
trie3 = TrieAutocomplete.from_dict(data)
```

### 元数据支持

```python
# 插入带元数据的单词
trie.insert('python', frequency=100, metadata={'category': 'language'})
trie.insert('java', frequency=80, metadata={'category': 'language'})

# 搜索结果包含元数据
results = trie.search('py')
for r in results:
    print(r.metadata)  # {'category': 'language'}
```

## API 参考

### TrieAutocomplete

| 方法 | 说明 |
|------|------|
| `insert(word, frequency=1, metadata=None)` | 插入单词 |
| `insert_batch(words, frequencies=None)` | 批量插入 |
| `search(prefix)` | 前缀搜索 |
| `fuzzy_search(query, max_distance=2)` | 模糊搜索 |
| `contains(word)` | 检查单词是否存在 |
| `remove(word)` | 删除单词 |
| `get_all_words()` | 获取所有单词 |
| `get_word_info(word)` | 获取单词信息 |
| `increment_frequency(word, amount=1)` | 增加频率 |
| `to_json()` / `from_json()` | 序列化 |
| `get_stats()` | 统计信息 |

### NGramAutocomplete

| 方法 | 说明 |
|------|------|
| `insert(word, frequency=1)` | 插入单词 |
| `search(query, min_score=0.1)` | Jaccard 相似度搜索 |
| `prefix_search(prefix)` | 前缀搜索 |
| `contains(word)` | 检查单词是否存在 |
| `remove(word)` | 删除单词 |
| `get_stats()` | 统计信息 |

### HybridAutocomplete

| 方法 | 说明 |
|------|------|
| `insert(word, frequency=1, metadata=None)` | 插入单词 |
| `search(query, fuzzy=True)` | 搜索（精确+模糊） |
| `contains(word)` | 检查单词是否存在 |
| `remove(word)` | 删除单词 |
| `get_stats()` | 统计信息（含 Trie 和 N-gram） |

### Suggestion 数据类

```python
@dataclass
class Suggestion:
    text: str            # 建议文本
    score: float         # 相关性得分 (0-1)
    frequency: int       # 使用频率
    metadata: Dict       # 额外元数据
```

### 工具函数

| 函数 | 说明 |
|------|------|
| `create_autocomplete(words, ...)` | 创建自动补全器 |
| `levenshtein_distance(s1, s2)` | 计算编辑距离 |
| `jaccard_similarity(s1, s2, n=2)` | 计算 Jaccard 相似度 |

## 应用场景

- **命令行工具**: 命令/参数补全
- **搜索框**: 用户输入建议
- **代码编辑器**: 关键字/函数名补全
- **标签系统**: 标签推荐
- **拼写纠错**: 近似词推荐

## 性能特点

- **Trie**: O(m) 前缀搜索，m 为前缀长度
- **N-gram**: O(n) 构建，搜索基于 Jaccard 相似度
- **模糊搜索**: 动态规划，O(m × n) 其中 m、n 为字符串长度

---

**测试覆盖**: 完整测试套件，覆盖所有补全器类型、搜索方法、序列化等