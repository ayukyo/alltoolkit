# TrieUtils - C# Trie (前缀树) 工具库

高效的前缀树数据结构实现，适用于自动补全、拼写检查、字典查找等场景。

## 特性

- ✅ **零外部依赖** - 仅使用 .NET 标准库
- ✅ **线程安全** - 使用 ReaderWriterLockSlim 支持并发访问
- ✅ **完整功能** - 插入、搜索、删除、前缀匹配、模式匹配
- ✅ **泛型支持** - Trie<T> 支持存储自定义值类型
- ✅ **Unicode 支持** - 支持中文、日文、Emoji 等多语言字符
- ✅ **频率统计** - 支持单词频率计数和排序

## 核心功能

| 方法 | 说明 |
|------|------|
| `Insert(word)` | 插入单词 |
| `Insert(word, value)` | 插入单词并关联值 |
| `Search(word)` | 搜索单词是否存在 |
| `SearchWithValue(word, out value)` | 搜索单词并返回值 |
| `StartsWith(prefix)` | 检查是否存在指定前缀的单词 |
| `Delete(word)` | 删除单词 |
| `WordsWithPrefix(prefix)` | 获取所有前缀匹配的单词 |
| `AutoComplete(prefix, limit)` | 自动补全建议 |
| `PatternMatch(pattern)` | 通配符模式匹配 (? 和 *) |
| `LongestCommonPrefix()` | 获取最长公共前缀 |
| `GetWordsByFrequency()` | 按频率排序获取单词 |
| `ContainsAnyPrefixOf(s)` | 检查是否有单词是字符串的前缀 |
| `LongestPrefixOf(s)` | 获取最长前缀匹配单词 |

## 快速开始

### 基础用法

```csharp
using AllToolkit.TrieUtils;

// 创建 Trie
var trie = new Trie();

// 插入单词
trie.Insert("hello");
trie.Insert("help");
trie.Insert("world");

// 搜索
bool found = trie.Search("hello");  // true
bool prefix = trie.StartsWith("hel");  // true

// 自动补全
var suggestions = trie.AutoComplete("hel", 10);
// ["hello", "help"]

// 删除
trie.Delete("hello");
```

### 带值的 Trie

```csharp
// 存储单词和关联值
trie.Insert("score1", 100);
trie.Insert("score2", 200);

// 搜索并获取值
int value;
if (trie.SearchWithValue<int>("score1", out value))
{
    Console.WriteLine($"值: {value}");  // 100
}
```

### 泛型 Trie

```csharp
// 泛型版本，存储自定义类型
var productTrie = new Trie<Product>();

productTrie.Insert("laptop", new Product { Name = "笔记本电脑", Price = 999.99 });

Product product;
if (productTrie.Search("laptop", out product))
{
    Console.WriteLine($"{product.Name}: ${product.Price}");
}
```

### 模式匹配

```csharp
trie.Insert("cat");
trie.Insert("bat");
trie.Insert("rat");
trie.Insert("car");

// ? 匹配任意单个字符
var matches = trie.PatternMatch("?at");
// ["cat", "bat", "rat"]

// * 匹配零个或多个字符
matches = trie.PatternMatch("ca*");
// ["car", "cat"]
```

### 单词频率统计

```csharp
// 多次插入同一单词会增加频率
trie.Insert("hello");
trie.Insert("hello");
trie.Insert("hello");
trie.Insert("world");

Console.WriteLine(trie.GetCount("hello"));  // 3

// 按频率排序
var freqList = trie.GetWordsByFrequency();
// [{"hello", 3}, {"world", 1}]
```

## 使用场景

### 1. 自动补全

```csharp
// 加载关键词字典
var trie = new Trie();
trie.BatchInsert(GetKeywords());

// 用户输入时提供补全建议
var suggestions = trie.AutoComplete(userInput, 10);
```

### 2. 拼写检查

```csharp
var dictionary = new Trie();
dictionary.BatchInsert(GetDictionaryWords());

bool isValid = dictionary.Search(word);
if (!isValid)
{
    // 提供相似词建议
    var suggestions = dictionary.AutoComplete(word.Substring(0, 2), 5);
}
```

### 3. URL 路由匹配

```csharp
var routes = new Trie<string>();
routes.Insert("/api/users", "UserController");
routes.Insert("/api/products", "ProductController");

// 找到最长匹配路由
string controller = routes.LongestPrefixOf("/api/users/123");
```

### 4. 词典/翻译

```csharp
var dict = new Trie<string>();
dict.Insert("hello", "你好");
dict.Insert("world", "世界");

string translation;
if (dict.Search("hello", out translation))
{
    Console.WriteLine(translation);  // "你好"
}
```

## 性能特点

- **插入**: O(L)，L 为单词长度
- **搜索**: O(L)
- **删除**: O(L)
- **前缀搜索**: O(L + N)，N 为匹配单词数
- **内存**: 比哈希表更节省空间（共享前缀）

## 运行测试

```bash
cd C#/trie_utils
dotnet run TrieUtilsTest.cs
```

## 运行示例

```bash
cd C#/trie_utils/examples
dotnet run UsageExamples.cs
```

## 文件结构

```
C#/trie_utils/
├── TrieUtils.cs          # 主实现
├── TrieUtilsTest.cs      # 单元测试
├── README.md             # 文档
└── examples/
    └── UsageExamples.cs  # 使用示例
```

## 许可证

MIT License