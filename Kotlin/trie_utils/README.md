# Trie Utils - Kotlin 前缀树工具库

高效的字符串前缀匹配和词频统计数据结构实现。

## 特性

- **零外部依赖** - 纯 Kotlin 标准库实现
- **四种 Trie 实现**：
  - `Trie` - 标准前缀树，支持插入、删除、搜索、前缀匹配
  - `FrequencyTrie` - 词频统计专用，支持 Top-K 高频词查询
  - `SerializableTrie` - 可序列化/反序列化，便于持久化
  - `AutocompleteTrie` - 自动补全专用，支持权重排序
- **完整功能**：
  - 单词插入、删除、搜索
  - 前缀匹配、前缀计数
  - 词频统计、自动补全
  - 最长公共前缀
  - 序列化/反序列化
  - 权重排序补全
- **泛型支持** - 支持任意字符类型

## 文件结构

```
trie_utils/
├── Trie.kt           # 核心实现
├── TrieTest.kt       # 测试套件（52 测试）
├── TrieExample.kt    # 使用示例
└── README.md         # 本文档
```

## 快速开始

### 基础用法

```kotlin
import trie_utils.Trie

// 创建 Trie
val trie = Trie<Char>()

// 插入单词
trie.insert("apple")
trie.insert("application")
trie.insert("apply")

// 搜索单词
trie.search("apple")        // true
trie.search("appl")         // false（不是完整单词）

// 前缀搜索
trie.startsWith("app")      // true

// 前缀单词数量
trie.countPrefix("app")     // 3

// 自动补全
trie.autocomplete("app")    // ["apple", "application", "apply"]

// 获取所有以某前缀开头的单词
trie.getWordsWithPrefixAsString("app")  // ["apple", "application", "apply"]

// 删除单词
trie.delete("apple")        // true

// 最长公共前缀
trie.longestCommonPrefixString()  // "app"
```

### 词频统计

```kotlin
import trie_utils.FrequencyTrie

val freqTrie = FrequencyTrie()

// 插入单词（自动统计频率）
freqTrie.insert("hello")
freqTrie.insert("hello")
freqTrie.insert("world")

// 查询词频
freqTrie.frequency("hello")  // 2
freqTrie.frequency("world")  // 1

// 获取高频词 Top K
freqTrie.getTopK(10)  // [("hello", 2), ("world", 1)]
```

### 序列化/反序列化

```kotlin
import trie_utils.SerializableTrie

val trie = SerializableTrie()
trie.insert("apple")
trie.insert("banana")

// 序列化为字符串
val serialized = trie.serialize()  // "apple:1,banana:1"

// 反序列化
val restored = SerializableTrie.fromSerialized(serialized)
restored.search("apple")  // true
```

### 自动补全（带权重）

```kotlin
import trie_utils.AutocompleteTrie

val autoTrie = AutocompleteTrie()

// 插入单词（带权重/热度）
autoTrie.insert("javascript", 100)
autoTrie.insert("java", 80)
autoTrie.insert("javafx", 20)

// 自动补全（按权重排序）
autoTrie.complete("jav")  // ["javascript", "java", "javafx"]

// 用户选择后提升权重
autoTrie.boost("javafx", 70)
autoTrie.complete("jav")  // ["javascript", "javafx", "java"]

// 获取最热门单词
autoTrie.getTopWords(5)  // ["javascript", "java", "javafx"]
```

## API 参考

### Trie<T>

| 方法 | 说明 |
|------|------|
| `insert(word)` | 插入单词，返回词频计数 |
| `insertAll(words)` | 批量插入单词 |
| `search(word)` | 搜索单词是否存在 |
| `startsWith(prefix)` | 检查是否存在以某前缀开头的单词 |
| `count(word)` | 获取单词词频 |
| `countPrefix(prefix)` | 获取以某前缀开头的单词数量 |
| `delete(word)` | 删除单词 |
| `getAllWords()` | 获取所有单词 |
| `getWordsWithPrefix(prefix)` | 获取以某前缀开头的所有单词 |
| `autocomplete(prefix, limit)` | 自动补全 |
| `longestCommonPrefix()` | 获取最长公共前缀 |
| `clear()` | 清空 Trie |
| `isEmpty()` | 是否为空 |
| `size()` | 单词总数（去重） |
| `totalCount()` | 单词总数（含重复） |

### FrequencyTrie

| 方法 | 说明 |
|------|------|
| `insert(word)` | 插入单词 |
| `frequency(word)` | 获取词频 |
| `prefixFrequency(prefix)` | 获取前缀频率 |
| `getTopK(limit)` | 获取 Top-K 高频词 |
| `totalWords()` | 总插入次数 |
| `uniqueWords()` | 唯一单词数 |

### SerializableTrie

| 方法 | 说明 |
|------|------|
| `insert(word)` | 插入单词 |
| `search(word)` | 搜索单词 |
| `serialize()` | 序列化为字符串 |
| `deserialize(data)` | 从字符串反序列化 |
| `fromSerialized(data)` | 静态方法，创建并反序列化 |

### AutocompleteTrie

| 方法 | 说明 |
|------|------|
| `insert(word, weight)` | 插入单词（带权重） |
| `complete(prefix, limit)` | 自动补全（按权重排序） |
| `boost(word, amount)` | 提升单词权重 |
| `weight(word)` | 获取单词权重 |
| `getTopWords(limit)` | 获取最热门单词 |

## 复杂度分析

| 操作 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| 插入 | O(m) | O(m) |
| 搜索 | O(m) | O(1) |
| 删除 | O(m) | O(1) |
| 前缀搜索 | O(m) | O(1) |
| 前缀单词查询 | O(m + n) | O(n) |

其中 m 为单词长度，n 为匹配的单词数量。

## 应用场景

1. **自动补全** - 搜索框、输入框智能提示
2. **拼写检查** - 快速判断单词是否在词典中
3. **词频统计** - 文本分析、关键词提取
4. **IP 路由** - 最长前缀匹配
5. **搜索引擎** - 搜索建议、热门查询
6. **文字游戏** - Scrabble、Wordle 等游戏的单词验证

## 运行测试

```bash
# 编译
kotlinc Trie.kt -d trie.jar

# 运行测试
kotlin -cp trie.jar trie_utils.TrieTestKt

# 运行示例
kotlin -cp trie.jar trie_utils.TrieExampleKt
```

## 性能特点

- **空间换时间**：通过树形结构快速定位前缀
- **高效前缀匹配**：O(m) 时间复杂度查找任意前缀
- **自动去重**：相同单词自动合并，通过计数维护词频
- **内存友好**：共享公共前缀，节省存储空间

## 作者

AllToolkit Auto-Generator

## 日期

2026-05-29