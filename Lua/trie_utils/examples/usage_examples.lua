---
-- Trie Utilities Examples
-- 前缀树工具库使用示例
--
-- @author AllToolkit
-- @version 1.0.0

-- 加载模块
local TrieUtils = dofile("../mod.lua")

print("=" .. string.rep("=", 60))
print("Trie Utilities - 使用示例")
print("=" .. string.rep("=", 60))

-------------------------------------------------------------------------------
-- 示例 1: 基本操作
-------------------------------------------------------------------------------
print("\n[示例 1] 基本操作")
print("-" .. string.rep("-", 60))

local trie = TrieUtils.new()

-- 插入单词
trie:insert("apple")
trie:insert("app")
trie:insert("application")
trie:insert("banana")
trie:insert("band")
trie:insert("bandana")

print("已插入单词: apple, app, application, banana, band, bandana")
print("单词总数: " .. trie:word_count())

-- 搜索单词
print("\n搜索测试:")
print("  搜索 'apple': " .. tostring(trie:search("apple")))
print("  搜索 'app': " .. tostring(trie:search("app")))
print("  搜索 'appl': " .. tostring(trie:search("appl")))
print("  搜索 'orange': " .. tostring(trie:search("orange")))

-- 前缀检查
print("\n前缀检查:")
print("  前缀 'app' 存在: " .. tostring(trie:starts_with("app")))
print("  前缀 'ban' 存在: " .. tostring(trie:starts_with("ban")))
print("  前缀 'xyz' 存在: " .. tostring(trie:starts_with("xyz")))

-------------------------------------------------------------------------------
-- 示例 2: 自动补全
-------------------------------------------------------------------------------
print("\n[示例 2] 自动补全")
print("-" .. string.rep("-", 60))

-- 获取以 "app" 开头的所有单词
local suggestions = trie:get_words_with_prefix("app")
print("前缀 'app' 的补全建议:")
for i, word in ipairs(suggestions) do
    print("  " .. i .. ". " .. word)
end

-- 限制建议数量
local limited = trie:get_words_with_prefix("ban", 2)
print("\n前缀 'ban' 的补全建议（限制 2 个）:")
for i, word in ipairs(limited) do
    print("  " .. i .. ". " .. word)
end

-- 统计前缀匹配数量
print("\n前缀匹配统计:")
print("  'app' 开头的单词数: " .. trie:count_words_with_prefix("app"))
print("  'ban' 开头的单词数: " .. trie:count_words_with_prefix("ban"))

-------------------------------------------------------------------------------
-- 示例 3: 大小写敏感
-------------------------------------------------------------------------------
print("\n[示例 3] 大小写敏感")
print("-" .. string.rep("-", 60))

-- 区分大小写（默认）
local sensitive = TrieUtils.new(true)
sensitive:insert("Hello")
sensitive:insert("hello")
print("区分大小写:")
print("  'Hello' 存在: " .. tostring(sensitive:search("Hello")))
print("  'hello' 存在: " .. tostring(sensitive:search("hello")))
print("  'HELLO' 存在: " .. tostring(sensitive:search("HELLO")))

-- 不区分大小写
local insensitive = TrieUtils.new(false)
insensitive:insert("Hello")
print("\n不区分大小写:")
print("  'Hello' 存在: " .. tostring(insensitive:search("Hello")))
print("  'hello' 存在: " .. tostring(insensitive:search("hello")))
print("  'HELLO' 存在: " .. tostring(insensitive:search("HELLO")))

-------------------------------------------------------------------------------
-- 示例 4: 关联数据
-------------------------------------------------------------------------------
print("\n[示例 4] 关联数据")
print("-" .. string.rep("-", 60))

local dictionary = TrieUtils.new()

-- 插入单词及其定义
dictionary:insert("apple", {definition = "一种红色或绿色的水果", count = 100})
dictionary:insert("banana", {definition = "一种黄色的长形水果", count = 80})
dictionary:insert("cherry", {definition = "一种红色的小型水果", count = 60})

-- 查询单词定义
local found, data = dictionary:search("apple")
if found then
    print("apple: " .. data.definition .. " (数量: " .. data.count .. ")")
end

found, data = dictionary:search("banana")
if found then
    print("banana: " .. data.definition .. " (数量: " .. data.count .. ")")
end

-- 更新数据
dictionary:update_data("apple", {definition = "一种红色或绿色的水果", count = 120})
local data = dictionary:get_data("apple")
print("\n更新后 apple 的数量: " .. data.count)

-------------------------------------------------------------------------------
-- 示例 5: 删除操作
-------------------------------------------------------------------------------
print("\n[示例 5] 删除操作")
print("-" .. string.rep("-", 60))

local deleteTrie = TrieUtils.new()
deleteTrie:insert("cat")
deleteTrie:insert("car")
deleteTrie:insert("card")

print("删除前:")
print("  'car' 存在: " .. tostring(deleteTrie:search("car")))
print("  'card' 存在: " .. tostring(deleteTrie:search("card")))

deleteTrie:delete("car")
print("\n删除 'car' 后:")
print("  'car' 存在: " .. tostring(deleteTrie:search("car")))
print("  'card' 存在: " .. tostring(deleteTrie:search("card")))

-------------------------------------------------------------------------------
-- 示例 6: 最长公共前缀
-------------------------------------------------------------------------------
print("\n[示例 6] 最长公共前缀")
print("-" .. string.rep("-", 60))

local lcpTrie = TrieUtils.new()
lcpTrie:insert("application")
lcpTrie:insert("apple")
lcpTrie:insert("apply")
lcpTrie:insert("appetite")

local lcp = lcpTrie:longest_common_prefix()
print("单词: application, apple, apply, appetite")
print("最长公共前缀: '" .. lcp .. "'")

-- 单独的最长公共前缀函数
local prefix1 = TrieUtils.longest_common_prefix_of("hello", "helicopter")
print("\n'hello' 和 'helicopter' 的最长公共前缀: '" .. prefix1 .. "'")

local prefix2 = TrieUtils.longest_common_prefix_of_all({"flower", "flow", "flight"})
print("'flower', 'flow', 'flight' 的最长公共前缀: '" .. prefix2 .. "'")

-------------------------------------------------------------------------------
-- 示例 7: 最长前缀匹配
-------------------------------------------------------------------------------
print("\n[示例 7] 最长前缀匹配")
print("-" .. string.rep("-", 60))

local matchTrie = TrieUtils.new()
matchTrie:insert("app")
matchTrie:insert("apple")
matchTrie:insert("applet")

local match = matchTrie:longest_prefix_match("appletree")
print("输入: 'appletree'")
print("最长前缀匹配: '" .. tostring(match) .. "'")

local allMatches = matchTrie:all_prefix_matches("appletree")
print("\n所有前缀匹配:")
for i, m in ipairs(allMatches) do
    print("  " .. i .. ". '" .. m .. "'")
end

-------------------------------------------------------------------------------
-- 示例 8: 通配符搜索
-------------------------------------------------------------------------------
print("\n[示例 8] 通配符搜索")
print("-" .. string.rep("-", 60))

local wildTrie = TrieUtils.new()
wildTrie:insert("cat")
wildTrie:insert("bat")
wildTrie:insert("rat")
wildTrie:insert("car")
wildTrie:insert("bar")
wildTrie:insert("cart")
wildTrie:insert("carbon")

-- ? 匹配单个字符
print("模式 '?at' 匹配:")
local qResults = wildTrie:wildcard_search("?at")
for i, word in ipairs(qResults) do
    print("  " .. i .. ". " .. word)
end

-- * 匹配任意字符序列
print("\n模式 'car*' 匹配:")
local starResults = wildTrie:wildcard_search("car*")
for i, word in ipairs(starResults) do
    print("  " .. i .. ". " .. word)
end

-------------------------------------------------------------------------------
-- 示例 9: 批量操作
-------------------------------------------------------------------------------
print("\n[示例 9] 批量操作")
print("-" .. string.rep("-", 60))

-- 批量插入
local batchTrie = TrieUtils.new()
local words = {"dog", "cat", "bird", "fish", "lion", "tiger"}
local inserted = batchTrie:insert_batch(words)
print("批量插入 " .. #words .. " 个单词，成功: " .. inserted)

-- 批量删除
local deleted = batchTrie:delete_batch({"cat", "fish"})
print("批量删除 2 个单词，成功: " .. deleted)
print("剩余单词数: " .. batchTrie:word_count())

-------------------------------------------------------------------------------
-- 示例 10: 序列化
-------------------------------------------------------------------------------
print("\n[示例 10] 序列化")
print("-" .. string.rep("-", 60))

local serTrie = TrieUtils.new()
serTrie:insert("hello")
serTrie:insert("world")
serTrie:insert("lua")

-- 转换为表
local table = serTrie:to_table()
print("序列化信息:")
print("  单词数: " .. table.word_count)
print("  节点数: " .. table.node_count)
print("  区分大小写: " .. tostring(table.case_sensitive))

-- 从表恢复
local restored = TrieUtils.from_table(table)
print("\n从表恢复后:")
print("  'hello' 存在: " .. tostring(restored:search("hello")))
print("  'world' 存在: " .. tostring(restored:search("world")))
print("  'lua' 存在: " .. tostring(restored:search("lua")))

-------------------------------------------------------------------------------
-- 示例 11: 遍历
-------------------------------------------------------------------------------
print("\n[示例 11] 遍历")
print("-" .. string.rep("-", 60))

local iterTrie = TrieUtils.new()
iterTrie:insert("apple")
iterTrie:insert("banana")
iterTrie:insert("cherry")
iterTrie:insert("date")

print("遍历所有单词:")
iterTrie:for_each(function(word)
    print("  - " .. word)
end)

print("\n遍历以 'b' 开头的单词:")
iterTrie:for_each_prefix("b", function(word)
    print("  - " .. word)
end)

-------------------------------------------------------------------------------
-- 示例 12: 克隆和合并
-------------------------------------------------------------------------------
print("\n[示例 12] 克隆和合并")
print("-" .. string.rep("-", 60))

local trie1 = TrieUtils.new()
trie1:insert("apple")
trie1:insert("banana")

local trie2 = TrieUtils.new()
trie2:insert("cherry")
trie2:insert("date")

-- 克隆
local cloned = trie1:clone()
print("克隆 trie1:")
print("  单词数: " .. cloned:word_count())
print("  'apple' 存在: " .. tostring(cloned:search("apple")))

-- 合并
local merged = trie1:merge(trie2)
print("\n合并 trie1 和 trie2:")
print("  成功合并数: " .. merged)
print("  总单词数: " .. trie1:word_count())

-------------------------------------------------------------------------------
-- 示例 13: 统计信息
-------------------------------------------------------------------------------
print("\n[示例 13] 统计信息")
print("-" .. string.rep("-", 60))

local statTrie = TrieUtils.new()
statTrie:insert("a")
statTrie:insert("ab")
statTrie:insert("abc")
statTrie:insert("abcd")

print("单词: a, ab, abc, abcd")
print("统计信息:")
print("  单词数: " .. statTrie:word_count())
print("  节点数: " .. statTrie:node_count())
print("  深度: " .. statTrie:depth())
print("  内存估算: " .. statTrie:memory_usage() .. " bytes")

-------------------------------------------------------------------------------
-- 示例 14: 只读视图
-------------------------------------------------------------------------------
print("\n[示例 14] 只读视图")
print("-" .. string.rep("-", 60))

local roTrie = TrieUtils.from_words({"apple", "banana", "cherry"})
local view = TrieUtils.readonly_view(roTrie)

print("只读视图操作:")
print("  search('apple'): " .. tostring(view.search("apple")))
print("  word_count(): " .. view.word_count())
print("  is_empty(): " .. tostring(view.is_empty()))

print("\n所有单词:")
local words = view.get_all_words()
for i, word in ipairs(words) do
    print("  " .. i .. ". " .. word)
end

-------------------------------------------------------------------------------
-- 示例 15: 排序单词
-------------------------------------------------------------------------------
print("\n[示例 15] 排序单词")
print("-" .. string.rep("-", 60))

local sortTrie = TrieUtils.new()
sortTrie:insert("zebra")
sortTrie:insert("apple")
sortTrie:insert("mango")
sortTrie:insert("banana")
sortTrie:insert("cherry")

local sorted = sortTrie:get_sorted_words()
print("按字典序排序:")
for i, word in ipairs(sorted) do
    print("  " .. i .. ". " .. word)
end

-------------------------------------------------------------------------------
-- 示例 16: Unicode 支持
-------------------------------------------------------------------------------
print("\n[示例 16] Unicode 支持")
print("-" .. string.rep("-", 60))

local unicodeTrie = TrieUtils.new()
unicodeTrie:insert("你好")
unicodeTrie:insert("世界")
unicodeTrie:insert("你好世界")
unicodeTrie:insert("hello")
unicodeTrie:insert("héllo")

print("Unicode 单词测试:")
print("  '你好' 存在: " .. tostring(unicodeTrie:search("你好")))
print("  '世界' 存在: " .. tostring(unicodeTrie:search("世界")))
print("  '你好世' 开头的单词:")
local unicodeWords = unicodeTrie:get_words_with_prefix("你好世")
for i, word in ipairs(unicodeWords) do
    print("    " .. i .. ". " .. word)
end

-------------------------------------------------------------------------------
-- 示例 17: 实际应用 - 搜索建议系统
-------------------------------------------------------------------------------
print("\n[示例 17] 实际应用 - 搜索建议系统")
print("-" .. string.rep("-", 60))

-- 创建搜索引擎索引
local searchIndex = TrieUtils.new()

-- 插入搜索词及其热度
searchIndex:insert("lua programming", {popularity = 100})
searchIndex:insert("lua tutorial", {popularity = 85})
searchIndex:insert("lua game development", {popularity = 70})
searchIndex:insert("python programming", {popularity = 95})
searchIndex:insert("python tutorial", {popularity = 80})

-- 用户输入 "lua" 时的建议
print("用户输入 'lua' 时的搜索建议:")
local luaSuggestions = searchIndex:get_words_with_prefix("lua", 5)
for i, suggestion in ipairs(luaSuggestions) do
    local data = searchIndex:get_data(suggestion)
    print("  " .. i .. ". " .. suggestion .. " (热度: " .. data.popularity .. ")")
end

-------------------------------------------------------------------------------
-- 示例 18: 实际应用 - 联系人自动补全
-------------------------------------------------------------------------------
print("\n[示例 18] 实际应用 - 联系人自动补全")
print("-" .. string.rep("-", 60))

local contacts = TrieUtils.new(false)  -- 不区分大小写

contacts:insert("Alice", {phone = "123-456-7890", email = "alice@example.com"})
contacts:insert("alice smith", {phone = "123-456-7891", email = "alice.s@example.com"})
contacts:insert("Bob", {phone = "123-456-7892", email = "bob@example.com"})
contacts:insert("Charlie", {phone = "123-456-7893", email = "charlie@example.com"})

print("搜索联系人 'ali':")
local aliResults = contacts:get_words_with_prefix("ali")
for i, name in ipairs(aliResults) do
    local info = contacts:get_data(name)
    print("  " .. i .. ". " .. name)
    print("     电话: " .. info.phone)
    print("     邮箱: " .. info.email)
end

print("\n" .. string.rep("=", 62))
print("所有示例完成!")
print(string.rep("=", 62))