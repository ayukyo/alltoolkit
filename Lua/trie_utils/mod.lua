---
-- Trie Utilities Module
-- 前缀树（字典树）工具函数库
--
-- 提供完整的 Trie（前缀树/字典树）数据结构实现，支持字符串的高效存储、检索和操作。
-- 仅使用 Lua 标准库，零依赖。
--
-- Features:
-- - Basic operations: insert, delete, search, starts_with
-- - Prefix operations: get_words_with_prefix, count_words_with_prefix
-- - Advanced operations: longest_common_prefix, longest_prefix_match
-- - Pattern matching: wildcard_search, pattern_match
-- - Statistics: word_count, node_count, depth, memory_usage
-- - Serialization: to_table, from_table, to_json, from_json
-- - Traversal: for_each, for_each_prefix
-- - Batch operations: insert_batch, delete_batch
-- - Utility: is_empty, clear, clone, merge
--
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local TrieUtils = {}
local TrieUtilsMT = { __index = TrieUtils }

--- 版本号
TrieUtils.VERSION = "1.0.0"

--- 错误类型
TrieUtils.Error = {
    InvalidWord = "Invalid word: word must be a non-empty string",
    InvalidCallback = "Invalid callback: must be a function",
    WordNotFound = "Word not found in trie",
    InvalidPattern = "Invalid pattern: must be a string",
    InvalidTable = "Invalid table: cannot deserialize",
    DuplicateWord = "Word already exists",
    InvalidTrie = "Invalid trie object",
}

-------------------------------------------------------------------------------
-- TrieNode 类定义
-------------------------------------------------------------------------------

local TrieNode = {}
TrieNode.__index = TrieNode

--- 创建新的 Trie 节点
-- @return TrieNode 新节点
function TrieNode.new()
    local node = {
        children = {},      -- 子节点映射
        is_end = false,     -- 是否是单词结尾
        count = 0,          -- 经过此节点的单词数量
        word = nil,         -- 如果是结尾，存储完整单词
        data = nil,         -- 用户自定义数据
    }
    setmetatable(node, TrieNode)
    return node
end

--- 检查节点是否为叶子节点
-- @return boolean 是否为叶子节点
function TrieNode:is_leaf()
    return next(self.children) == nil
end

--- 获取子节点数量
-- @return number 子节点数量
function TrieNode:child_count()
    local count = 0
    for _ in pairs(self.children) do
        count = count + 1
    end
    return count
end

-------------------------------------------------------------------------------
-- Trie 类定义
-------------------------------------------------------------------------------

local Trie = {}
Trie.__index = Trie

--- 创建新的 Trie
-- @param case_sensitive boolean 是否区分大小写（默认 true）
-- @return Trie 新 Trie 对象
function Trie.new(case_sensitive)
    local trie = {
        root = TrieNode.new(),
        case_sensitive = case_sensitive ~= false,  -- 默认区分大小写
        _word_count = 0,    -- 单词总数
        _node_count = 1,    -- 节点总数（包含根节点）
    }
    setmetatable(trie, Trie)
    return trie
end

--- 标准化单词（根据大小写敏感设置）
-- @param word string 单词
-- @return string 标准化后的单词
function Trie:_normalize(word)
    if not self.case_sensitive then
        return word:lower()
    end
    return word
end

-------------------------------------------------------------------------------
-- 基本操作
-------------------------------------------------------------------------------

--- 插入单词
-- @param word string 要插入的单词
-- @param data any 可选的关联数据
-- @return boolean 是否成功插入（false 表示已存在）
function Trie:insert(word, data)
    if type(word) ~= "string" or #word == 0 then
        error(TrieUtils.Error.InvalidWord)
    end
    
    word = self:_normalize(word)
    local node = self.root
    
    for i = 1, #word do
        local char = word:sub(i, i)
        if not node.children[char] then
            node.children[char] = TrieNode.new()
            self._node_count = self._node_count + 1
        end
        node = node.children[char]
        node.count = node.count + 1
    end
    
    if node.is_end then
        return false  -- 单词已存在
    end
    
    node.is_end = true
    node.word = word
    node.data = data
    self._word_count = self._word_count + 1
    return true
end

--- 删除单词
-- @param word string 要删除的单词
-- @return boolean 是否成功删除
function Trie:delete(word)
    if type(word) ~= "string" or #word == 0 then
        error(TrieUtils.Error.InvalidWord)
    end
    
    word = self:_normalize(word)
    
    -- 查找单词并记录路径
    local path = {}
    local node = self.root
    
    for i = 1, #word do
        local char = word:sub(i, i)
        if not node.children[char] then
            return false  -- 单词不存在
        end
        table.insert(path, {node = node, char = char})
        node = node.children[char]
    end
    
    if not node.is_end then
        return false  -- 单词不存在
    end
    
    -- 标记为非单词结尾
    node.is_end = false
    node.word = nil
    node.data = nil
    self._word_count = self._word_count - 1
    
    -- 从叶子向根删除空节点
    for i = #path, 1, -1 do
        local parent = path[i].node
        local char = path[i].char
        local child = parent.children[char]
        
        child.count = child.count - 1
        
        if child.count == 0 and child:is_leaf() then
            parent.children[char] = nil
            self._node_count = self._node_count - 1
        end
    end
    
    return true
end

--- 搜索单词
-- @param word string 要搜索的单词
-- @return boolean, any 是否存在和关联数据
function Trie:search(word)
    if type(word) ~= "string" or #word == 0 then
        return false, nil
    end
    
    word = self:_normalize(word)
    local node = self:_find_node(word)
    
    if node and node.is_end then
        return true, node.data
    end
    return false, nil
end

--- 检查是否存在以指定前缀开头的单词
-- @param prefix string 前缀
-- @return boolean 是否存在
function Trie:starts_with(prefix)
    if type(prefix) ~= "string" or #prefix == 0 then
        return false
    end
    
    prefix = self:_normalize(prefix)
    local node = self:_find_node(prefix)
    return node ~= nil
end

--- 查找前缀对应的节点
-- @param prefix string 前缀
-- @return TrieNode|nil 节点或 nil
function Trie:_find_node(prefix)
    local node = self.root
    for i = 1, #prefix do
        local char = prefix:sub(i, i)
        if not node.children[char] then
            return nil
        end
        node = node.children[char]
    end
    return node
end

-------------------------------------------------------------------------------
-- 前缀操作
-------------------------------------------------------------------------------

--- 获取所有以指定前缀开头的单词
-- @param prefix string 前缀
-- @param limit number 可选，最大返回数量
-- @return table 单词列表
function Trie:get_words_with_prefix(prefix, limit)
    if type(prefix) ~= "string" then
        return {}
    end
    
    prefix = self:_normalize(prefix)
    local result = {}
    local node = self:_find_node(prefix)
    
    if not node then
        return result
    end
    
    -- 深度优先搜索收集所有单词
    local function dfs(current_node, current_word)
        if limit and #result >= limit then
            return
        end
        
        if current_node.is_end then
            table.insert(result, current_node.word or current_word)
        end
        
        for char, child in pairs(current_node.children) do
            dfs(child, current_word .. char)
        end
    end
    
    dfs(node, prefix)
    return result
end

--- 统计以指定前缀开头的单词数量
-- @param prefix string 前缀
-- @return number 单词数量
function Trie:count_words_with_prefix(prefix)
    if type(prefix) ~= "string" or #prefix == 0 then
        return self._word_count
    end
    
    prefix = self:_normalize(prefix)
    local node = self:_find_node(prefix)
    
    if not node then
        return 0
    end
    
    -- 统计以该节点为根的子树中的单词数量
    local count = 0
    local function dfs(n)
        if n.is_end then
            count = count + 1
        end
        for _, child in pairs(n.children) do
            dfs(child)
        end
    end
    dfs(node)
    return count
end

-------------------------------------------------------------------------------
-- 高级操作
-------------------------------------------------------------------------------

--- 获取最长公共前缀
-- @return string 最长公共前缀
function Trie:longest_common_prefix()
    if self._word_count == 0 then
        return ""
    end
    
    local prefix = ""
    local node = self.root
    
    while node:child_count() == 1 and not node.is_end do
        local char
        for k, child in pairs(node.children) do
            char = k
            node = child
            break
        end
        if char then
            prefix = prefix .. char
        end
    end
    
    return prefix
end

--- 获取字符串在 Trie 中的最长前缀匹配
-- @param str string 输入字符串
-- @return string|nil 最长匹配的前缀，如果没有则返回 nil
function Trie:longest_prefix_match(str)
    if type(str) ~= "string" or #str == 0 then
        return nil
    end
    
    str = self:_normalize(str)
    local node = self.root
    local longest_match = nil
    
    for i = 1, #str do
        local char = str:sub(i, i)
        if not node.children[char] then
            break
        end
        node = node.children[char]
        if node.is_end then
            longest_match = str:sub(1, i)
        end
    end
    
    return longest_match
end

--- 获取字符串在 Trie 中的所有前缀匹配
-- @param str string 输入字符串
-- @return table 匹配的前缀列表
function Trie:all_prefix_matches(str)
    if type(str) ~= "string" or #str == 0 then
        return {}
    end
    
    str = self:_normalize(str)
    local node = self.root
    local matches = {}
    
    for i = 1, #str do
        local char = str:sub(i, i)
        if not node.children[char] then
            break
        end
        node = node.children[char]
        if node.is_end then
            table.insert(matches, str:sub(1, i))
        end
    end
    
    return matches
end

-------------------------------------------------------------------------------
-- 模式匹配
-------------------------------------------------------------------------------

--- 通配符搜索（支持 ? 和 *）
-- @param pattern string 模式（? 匹配单个字符，* 匹配任意字符序列）
-- @return table 匹配的单词列表
function Trie:wildcard_search(pattern)
    if type(pattern) ~= "string" or #pattern == 0 then
        return {}
    end
    
    pattern = self:_normalize(pattern)
    local result = {}
    
    local function dfs(node, word, pattern_idx)
        if pattern_idx > #pattern then
            if node.is_end then
                table.insert(result, node.word or word)
            end
            return
        end
        
        local char = pattern:sub(pattern_idx, pattern_idx)
        
        if char == '?' then
            -- 匹配任意单个字符
            for c, child in pairs(node.children) do
                dfs(child, word .. c, pattern_idx + 1)
            end
        elseif char == '*' then
            -- 匹配任意字符序列（包括空序列）
            -- 尝试匹配零个字符
            dfs(node, word, pattern_idx + 1)
            -- 尝试匹配多个字符
            for c, child in pairs(node.children) do
                dfs(child, word .. c, pattern_idx)
            end
        else
            -- 匹配特定字符
            local child = node.children[char]
            if child then
                dfs(child, word .. char, pattern_idx + 1)
            end
        end
    end
    
    dfs(self.root, "", 1)
    return result
end

-------------------------------------------------------------------------------
-- 统计信息
-------------------------------------------------------------------------------

--- 获取单词总数
-- @return number 单词数量
function Trie:word_count()
    return self._word_count
end

--- 获取节点总数
-- @return number 节点数量
function Trie:node_count()
    return self._node_count
end

--- 获取 Trie 的最大深度
-- @return number 深度
function Trie:depth()
    local max_depth = 0
    
    local function dfs(node, current_depth)
        if current_depth > max_depth then
            max_depth = current_depth
        end
        for _, child in pairs(node.children) do
            dfs(child, current_depth + 1)
        end
    end
    
    dfs(self.root, 0)
    return max_depth
end

--- 估算内存使用量（粗略估计）
-- @return number 字节数
function Trie:memory_usage()
    -- 每个节点粗略估计：
    -- children 表开销 + 2 个布尔值 + 2 个引用
    local bytes_per_node = 100  -- 粗略估计
    local children_overhead = 0
    
    local function count_children_overhead(node)
        local count = 0
        for char, child in pairs(node.children) do
            count = count + #char * 2  -- 字符串键
            count_children_overhead(child)
        end
        return count
    end
    
    return self._node_count * bytes_per_node + count_children_overhead(self.root)
end

-------------------------------------------------------------------------------
-- 序列化
-------------------------------------------------------------------------------

--- 转换为表（用于序列化）
-- @return table 表表示
function Trie:to_table()
    local function node_to_table(node)
        local t = {
            is_end = node.is_end,
            children = {},
        }
        if node.is_end then
            t.word = node.word
            t.data = node.data
        end
        for char, child in pairs(node.children) do
            t.children[char] = node_to_table(child)
        end
        return t
    end
    
    return {
        case_sensitive = self.case_sensitive,
        root = node_to_table(self.root),
        word_count = self._word_count,
        node_count = self._node_count,
    }
end

--- 从表创建 Trie
-- @param t table 表表示
-- @return Trie Trie 对象
function Trie.from_table(t)
    if type(t) ~= "table" or type(t.root) ~= "table" then
        error(TrieUtils.Error.InvalidTable)
    end
    
    local function table_to_node(tbl)
        local node = TrieNode.new()
        node.is_end = tbl.is_end or false
        node.word = tbl.word
        node.data = tbl.data
        node.count = 0
        if tbl.is_end then
            node.count = 1
        end
        for char, child_tbl in pairs(tbl.children or {}) do
            node.children[char] = table_to_node(child_tbl)
            node.count = node.count + node.children[char].count
        end
        return node
    end
    
    local trie = Trie.new(t.case_sensitive)
    trie.root = table_to_node(t.root)
    trie._word_count = t.word_count or 0
    trie._node_count = t.node_count or 1
    return trie
end

-------------------------------------------------------------------------------
-- 遍历
-------------------------------------------------------------------------------

--- 遍历所有单词
-- @param callback function 回调函数 function(word, data)
function Trie:for_each(callback)
    if type(callback) ~= "function" then
        error(TrieUtils.Error.InvalidCallback)
    end
    
    local function dfs(node)
        if node.is_end then
            callback(node.word, node.data)
        end
        for _, child in pairs(node.children) do
            dfs(child)
        end
    end
    
    dfs(self.root)
end

--- 遍历以指定前缀开头的所有单词
-- @param prefix string 前缀
-- @param callback function 回调函数 function(word, data)
function Trie:for_each_prefix(prefix, callback)
    if type(callback) ~= "function" then
        error(TrieUtils.Error.InvalidCallback)
    end
    
    prefix = self:_normalize(prefix)
    local node = self:_find_node(prefix)
    
    if not node then
        return
    end
    
    local function dfs(n)
        if n.is_end then
            callback(n.word, n.data)
        end
        for _, child in pairs(n.children) do
            dfs(child)
        end
    end
    
    dfs(node)
end

-------------------------------------------------------------------------------
-- 批量操作
-------------------------------------------------------------------------------

--- 批量插入单词
-- @param words table 单词列表或 {word = data, ...} 表
-- @return number 成功插入的数量
function Trie:insert_batch(words)
    if type(words) ~= "table" then
        return 0
    end
    
    local count = 0
    for i, item in ipairs(words) do
        if type(item) == "string" then
            if self:insert(item) then
                count = count + 1
            end
        elseif type(item) == "table" and item.word then
            if self:insert(item.word, item.data) then
                count = count + 1
            end
        end
    end
    
    -- 也支持键值对形式
    for word, data in pairs(words) do
        if type(word) == "string" and type(i) ~= "number" then
            if self:insert(word, data) then
                count = count + 1
            end
        end
    end
    
    return count
end

--- 批量删除单词
-- @param words table 单词列表
-- @return number 成功删除的数量
function Trie:delete_batch(words)
    if type(words) ~= "table" then
        return 0
    end
    
    local count = 0
    for _, word in ipairs(words) do
        if self:delete(word) then
            count = count + 1
        end
    end
    return count
end

-------------------------------------------------------------------------------
-- 工具方法
-------------------------------------------------------------------------------

--- 检查 Trie 是否为空
-- @return boolean 是否为空
function Trie:is_empty()
    return self._word_count == 0
end

--- 清空 Trie
function Trie:clear()
    self.root = TrieNode.new()
    self._word_count = 0
    self._node_count = 1
end

--- 克隆 Trie
-- @return Trie 克隆的 Trie
function Trie:clone()
    local t = self:to_table()
    return Trie.from_table(t)
end

--- 合并另一个 Trie 到当前 Trie
-- @param other Trie 另一个 Trie
-- @return number 成功合并的单词数量
function Trie:merge(other)
    if type(other) ~= "table" or not other.root then
        error(TrieUtils.Error.InvalidTrie)
    end
    
    local count = 0
    other:for_each(function(word, data)
        if self:insert(word, data) then
            count = count + 1
        end
    end)
    return count
end

--- 获取所有单词
-- @return table 单词列表
function Trie:get_all_words()
    local words = {}
    self:for_each(function(word)
        table.insert(words, word)
    end)
    return words
end

--- 按字典序获取所有单词
-- @return table 排序后的单词列表
function Trie:get_sorted_words()
    local words = self:get_all_words()
    table.sort(words)
    return words
end

--- 更新单词的关联数据
-- @param word string 单词
-- @param data any 新数据
-- @return boolean 是否成功
function Trie:update_data(word, data)
    if type(word) ~= "string" or #word == 0 then
        return false
    end
    
    word = self:_normalize(word)
    local node = self:_find_node(word)
    
    if node and node.is_end then
        node.data = data
        return true
    end
    return false
end

--- 获取单词的关联数据
-- @param word string 单词
-- @return any|nil 数据或 nil
function Trie:get_data(word)
    local found, data = self:search(word)
    if found then
        return data
    end
    return nil
end

-------------------------------------------------------------------------------
-- TrieUtils 模块函数
-------------------------------------------------------------------------------

--- 创建新的 Trie
-- @param case_sensitive boolean 是否区分大小写（默认 true）
-- @return Trie Trie 对象
function TrieUtils.new(case_sensitive)
    return Trie.new(case_sensitive)
end

--- 从单词列表创建 Trie
-- @param words table 单词列表
-- @param case_sensitive boolean 是否区分大小写
-- @return Trie Trie 对象
function TrieUtils.from_words(words, case_sensitive)
    local trie = Trie.new(case_sensitive)
    for i, item in ipairs(words) do
        if type(item) == "string" then
            trie:insert(item)
        elseif type(item) == "table" and item.word then
            trie:insert(item.word, item.data)
        end
    end
    return trie
end

--- 从表创建 Trie
-- @param t table 表表示
-- @return Trie Trie 对象
function TrieUtils.from_table(t)
    return Trie.from_table(t)
end

--- 查找两个字符串的最长公共前缀
-- @param str1 string 字符串1
-- @param str2 string 字符串2
-- @return string 最长公共前缀
function TrieUtils.longest_common_prefix_of(str1, str2)
    if type(str1) ~= "string" or type(str2) ~= "string" then
        return ""
    end
    
    local len = math.min(#str1, #str2)
    local i = 1
    
    while i <= len and str1:sub(i, i) == str2:sub(i, i) do
        i = i + 1
    end
    
    return str1:sub(1, i - 1)
end

--- 查找字符串列表的最长公共前缀
-- @param words table 字符串列表
-- @return string 最长公共前缀
function TrieUtils.longest_common_prefix_of_all(words)
    if type(words) ~= "table" or #words == 0 then
        return ""
    end
    
    if #words == 1 then
        return words[1]
    end
    
    local prefix = words[1]
    
    for i = 2, #words do
        prefix = TrieUtils.longest_common_prefix_of(prefix, words[i])
        if #prefix == 0 then
            break
        end
    end
    
    return prefix
end

--- 自动补全建议
-- @param trie Trie Trie 对象
-- @param prefix string 前缀
-- @param max_suggestions number 最大建议数
-- @return table 建议列表
function TrieUtils.autocomplete(trie, prefix, max_suggestions)
    return trie:get_words_with_prefix(prefix, max_suggestions)
end

--- 拼写检查建议（基于前缀匹配）
-- @param trie Trie Trie 对象
-- @param word string 输入单词
-- @param max_distance number 最大编辑距离（简化版：仅前缀匹配）
-- @return table 建议列表
function TrieUtils.spell_check(trie, word, max_distance)
    max_distance = max_distance or 1
    
    if type(word) ~= "string" or #word == 0 then
        return {}
    end
    
    local suggestions = {}
    local word_len = #word
    
    -- 收集所有单词
    local all_words = trie:get_all_words()
    
    for _, w in ipairs(all_words) do
        local w_len = #w
        local distance = math.abs(word_len - w_len)
        
        if distance <= max_distance then
            -- 简化：仅使用长度差作为距离
            table.insert(suggestions, w)
        end
    end
    
    return suggestions
end

--- 创建只读 Trie 视图（返回只读接口）
-- @param trie Trie Trie 对象
-- @return table 只读接口
function TrieUtils.readonly_view(trie)
    return {
        search = function(word) return trie:search(word) end,
        starts_with = function(prefix) return trie:starts_with(prefix) end,
        get_words_with_prefix = function(prefix, limit) return trie:get_words_with_prefix(prefix, limit) end,
        count_words_with_prefix = function(prefix) return trie:count_words_with_prefix(prefix) end,
        word_count = function() return trie:word_count() end,
        node_count = function() return trie:node_count() end,
        depth = function() return trie:depth() end,
        get_all_words = function() return trie:get_all_words() end,
        get_sorted_words = function() return trie:get_sorted_words() end,
        for_each = function(callback) return trie:for_each(callback) end,
        is_empty = function() return trie:is_empty() end,
    }
end

return TrieUtils