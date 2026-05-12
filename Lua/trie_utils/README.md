# Trie Utils (前缀树工具库)

完整的前缀树（Trie/字典树）数据结构实现，支持字符串的高效存储、检索和操作。

## 功能特性

- ✅ **基本操作**: 插入、删除、搜索、前缀检查
- ✅ **前缀操作**: 获取前缀单词、统计前缀匹配数
- ✅ **高级操作**: 最长公共前缀、最长前缀匹配
- ✅ **模式匹配**: 通配符搜索（支持 `?` 和 `*`）
- ✅ **统计信息**: 单词数、节点数、深度、内存估算
- ✅ **序列化**: 支持表转换和恢复
- ✅ **遍历**: 遍历所有单词或指定前缀单词
- ✅ **批量操作**: 批量插入、批量删除
- ✅ **工具方法**: 清空、克隆、合并、只读视图

## 安装

```lua
local TrieUtils = dofile("mod.lua")
```

## 快速开始

### 基本使用

```lua
local TrieUtils = dofile("mod.lua")

-- 创建 Trie
local trie = TrieUtils.new()

-- 插入单词
trie:insert("apple")
trie:insert("app")
trie:insert("application")

-- 搜索单词
print(trie:search("apple"))  -- true
print(trie:search("app"))    -- true
print(trie:search("appl"))   -- false (不是完整单词)

-- 前缀检查
print(trie:starts_with("app"))  -- true
print(trie:starts_with("xyz"))  -- false

-- 获取前缀单词
local words = trie:get_words_with_prefix("app")
-- words = {"app", "apple", "application"}

-- 删除单词
trie:delete("apple")
print(trie:search("apple"))  -- false
```

### 关联数据

```lua
local trie = TrieUtils.new()

-- 插入时关联数据
trie:insert("apple", {definition = "一种水果", count = 100})
trie:insert("banana", {definition = "黄色水果", count = 80})

-- 搜索并获取数据
local found, data = trie:search("apple")
if found then
    print(data.definition)  -- "一种水果"
    print(data.count)       -- 100
end

-- 更新数据
trie:update_data("apple", {definition = "红色或绿色水果", count = 120})

-- 仅获取数据
local data = trie:get_data("apple")
```

### 大小写敏感

```lua
-- 区分大小写（默认）
local sensitive = TrieUtils.new(true)
sensitive:insert("Hello")
print(sensitive:search("hello"))  -- false
print(sensitive:search("Hello"))  -- true

-- 不区分大小写
local insensitive = TrieUtils.new(false)
insensitive:insert("Hello")
print(insensitive:search("hello"))  -- true
print(insensitive:search("HELLO"))  -- true
```

### 自动补全

```lua
local trie = TrieUtils.from_words({
    "apple", "application", "apply", "appetite"
})

-- 获取补全建议
local suggestions = trie:get_words_with_prefix("app", 3)
-- suggestions = {"apple", "application", "apply"} (最多 3 个)

-- 统计前缀匹配数
print(trie:count_words_with_prefix("app"))  -- 4
```

### 最长公共前缀

```lua
local trie = TrieUtils.from_words({"flower", "flow", "flight"})
print(trie:longest_common_prefix())  -- "fl"

-- 单独使用
print(TrieUtils.longest_common_prefix_of("apple", "application"))  -- "appl"
print(TrieUtils.longest_common_prefix_of_all({"cat", "car", "card"}))  -- "ca"
```

### 通配符搜索

```lua
local trie = TrieUtils.from_words({"cat", "bat", "rat", "car", "cart"})

-- ? 匹配单个字符
local results = trie:wildcard_search("?at")
-- results = {"cat", "bat", "rat"}

-- * 匹配任意字符序列
local results = trie:wildcard_search("car*")
-- results = {"car", "cart"}
```

### 批量操作

```lua
local trie = TrieUtils.new()

-- 批量插入
local inserted = trie:insert_batch({"apple", "banana", "cherry"})
print(inserted)  -- 3

-- 批量删除
local deleted = trie:delete_batch({"apple", "cherry"})
print(deleted)  -- 2
```

### 序列化

```lua
local trie = TrieUtils.new()
trie:insert("apple", 100)
trie:insert("banana", 80)

-- 转换为表
local t = trie:to_table()

-- 从表恢复
local restored = TrieUtils.from_table(t)
print(restored:search("apple"))  -- true
```

### 遍历

```lua
local trie = TrieUtils.from_words({"apple", "banana", "cherry"})

-- 遍历所有单词
trie:for_each(function(word, data)
    print(word)
end)

-- 遍历指定前缀单词
trie:for_each_prefix("app", function(word)
    print(word)
end)
```

### 克隆与合并

```lua
local trie1 = TrieUtils.from_words({"apple", "banana"})
local trie2 = TrieUtils.from_words({"cherry", "date"})

-- 克隆
local cloned = trie1:clone()

-- 合并
local merged = trie1:merge(trie2)
print(merged)  -- 2
print(trie1:word_count())  -- 4
```

### 只读视图

```lua
local trie = TrieUtils.from_words({"apple", "banana"})
local view = TrieUtils.readonly_view(trie)

-- 只能读取，不能修改
print(view.search("apple"))      -- true
print(view.word_count())          -- 2
print(view.get_all_words()[1])   -- "apple" 或 "banana"
```

## API 参考

### Trie 类方法

| 方法 | 描述 |
|------|------|
| `new(case_sensitive)` | 创建新 Trie |
| `insert(word, data)` | 插入单词，返回是否成功 |
| `delete(word)` | 删除单词，返回是否成功 |
| `search(word)` | 搜索单词，返回 (found, data) |
| `starts_with(prefix)` | 检查前缀是否存在 |
| `get_words_with_prefix(prefix, limit)` | 获取前缀单词列表 |
| `count_words_with_prefix(prefix)` | 统计前缀匹配数 |
| `longest_common_prefix()` | 获取最长公共前缀 |
| `longest_prefix_match(str)` | 获取最长前缀匹配 |
| `all_prefix_matches(str)` | 获取所有前缀匹配 |
| `wildcard_search(pattern)` | 通配符搜索 |
| `word_count()` | 获取单词总数 |
| `node_count()` | 获取节点总数 |
| `depth()` | 获取最大深度 |
| `memory_usage()` | 估算内存使用 |
| `to_table()` | 转换为表 |
| `for_each(callback)` | 遍历所有单词 |
| `for_each_prefix(prefix, callback)` | 遍历前缀单词 |
| `insert_batch(words)` | 批量插入 |
| `delete_batch(words)` | 批量删除 |
| `is_empty()` | 检查是否为空 |
| `clear()` | 清空 Trie |
| `clone()` | 克隆 Trie |
| `merge(other)` | 合并另一个 Trie |
| `get_all_words()` | 获取所有单词 |
| `get_sorted_words()` | 获取排序后的单词 |
| `update_data(word, data)` | 更新关联数据 |
| `get_data(word)` | 获取关联数据 |

### TrieUtils 模块函数

| 函数 | 描述 |
|------|------|
| `new(case_sensitive)` | 创建新 Trie |
| `from_words(words, case_sensitive)` | 从单词列表创建 |
| `from_table(t)` | 从表创建 |
| `longest_common_prefix_of(str1, str2)` | 两个字符串的最长公共前缀 |
| `longest_common_prefix_of_all(words)` | 字符串列表的最长公共前缀 |
| `autocomplete(trie, prefix, max)` | 自动补全建议 |
| `spell_check(trie, word, max_distance)` | 拼写检查建议 |
| `readonly_view(trie)` | 创建只读视图 |

## 时间复杂度

| 操作 | 时间复杂度 |
|------|------------|
| 插入 | O(L) |
| 删除 | O(L) |
| 搜索 | O(L) |
| 前缀检查 | O(L) |
| 获取前缀单词 | O(L + N) |
| 最长公共前缀 | O(L) |

其中 L 是单词/前缀长度，N 是结果数量。

## 应用场景

- 📝 **自动补全**: 搜索框、输入框建议
- 📖 **拼写检查**: 单词验证和建议
- 🔍 **前缀匹配**: IP 路由、字典查找
- 📚 **词频统计**: 单词计数
- 🌐 **URL 路由**: 路径匹配
- 📱 **联系人搜索**: 姓名匹配

## 测试

```bash
lua trie_utils_test.lua
```

## 许可证

MIT License