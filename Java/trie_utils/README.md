# Trie (前缀树) 工具模块

高效的字符串存储和检索数据结构，适用于自动补全、拼写检查、前缀搜索等场景。

## 文件结构

```
Java/trie_utils/
├── TrieNode.java    # 前缀树节点类
├── Trie.java        # 前缀树主类
├── TrieTest.java    # 单元测试
├── TrieExample.java # 使用示例
└── README.md        # 说明文档
```

## 核心功能

### 基本操作
| 方法 | 说明 | 时间复杂度 |
|------|------|-----------|
| `insert(word)` | 插入单词 | O(m) |
| `search(word)` | 搜索单词 | O(m) |
| `startsWith(prefix)` | 前缀检查 | O(m) |
| `delete(word)` | 删除单词 | O(m) |
| `clear()` | 清空 Trie | O(1) |

### 自动补全
| 方法 | 说明 |
|------|------|
| `autocomplete(prefix)` | 获取所有补全建议 |
| `autocomplete(prefix, max)` | 获取前 N 个建议 (按词频排序) |
| `getWordsWithPrefix(prefix)` | 获取指定前缀的所有单词 |

### 词频统计
| 方法 | 说明 |
|------|------|
| `getWordCount(word)` | 获取单词出现次数 |
| `size()` | 获取不同单词总数 |
| `countWordsWithPrefix(prefix)` | 统计前缀单词数 |
| `getAllWords()` | 获取所有单词列表 |

### 高级功能
| 方法 | 说明 |
|------|------|
| `getLongestCommonPrefix()` | 计算最长公共前缀 |
| `fuzzySearch(word, maxDistance)` | 模糊搜索 (编辑距离) |

## 使用方法

### 编译

```bash
# 编译所有文件
javac trie_utils/*.java

# 或单独编译
javac trie_utils/TrieNode.java
javac trie_utils/Trie.java
javac trie_utils/TrieTest.java
javac trie_utils/TrieExample.java
```

### 运行测试

```bash
java trie_utils.TrieTest
```

### 运行示例

```bash
java trie_utils.TrieExample
```

## 代码示例

### 基本使用

```java
Trie trie = new Trie();

// 插入单词
trie.insert("apple");
trie.insert("application");
trie.insert("app");

// 搜索
trie.search("apple");    // true
trie.search("app");      // true
trie.search("appl");     // false

// 前缀检查
trie.startsWith("app");  // true
trie.startsWith("ban");   // false

// 删除
trie.delete("apple");
```

### 自动补全

```java
Trie trie = new Trie();
trie.insert("apple");
trie.insert("app");
trie.insert("app");
trie.insert("application");
trie.insert("append");

// 获取补全建议 (按词频排序)
List<String> suggestions = trie.autocomplete("app", 3);
// ["app", "apple", "append"]  (app 排第一因为词频最高)
```

### 词频统计

```java
Trie trie = new Trie();
trie.insert("hello");
trie.insert("hello");
trie.insert("world");

trie.getWordCount("hello");  // 2
trie.getWordCount("world");  // 1
trie.size();                  // 2 (不同单词数)
```

### 拼写检查

```java
Trie dictionary = new Trie();
dictionary.insert("hello");
dictionary.insert("help");
dictionary.insert("held");

String word = "helo";
if (!dictionary.search(word)) {
    // 模糊搜索找相似词
    List<String> suggestions = dictionary.fuzzySearch(word, 1);
    // ["hello", "help", "held"]
}
```

## 应用场景

1. **搜索引擎** - 自动补全、搜索建议
2. **输入法** - 联想词、纠错
3. **拼写检查** - 词典匹配、相似词推荐
4. **路由匹配** - URL 前缀路由
5. **IP 路由** - 最长前缀匹配
6. **基因序列** - DNA 序列匹配

## 性能特点

- **空间换时间**: 通过额外空间换取高效查询
- **前缀共享**: 相同前缀的单词共享节点
- **适合场景**: 大量字符串、频繁前缀查询

## 零依赖

本模块仅使用 Java 标准库，无需任何外部依赖。

## 测试覆盖

测试类 `TrieTest.java` 包含以下测试:
- 基本操作 (插入、搜索、删除)
- 词频统计
- 自动补全
- 模糊搜索
- 边界情况 (null、空值)
- Unicode 支持 (中文、日文、韩文)

---

**创建日期**: 2026-04-20
**语言**: Java
**版本**: 1.0