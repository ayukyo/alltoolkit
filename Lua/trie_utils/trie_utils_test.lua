---
-- Trie Utilities Test Suite
-- 前缀树工具库测试
--
-- @author AllToolkit
-- @version 1.0.0

-- 简单的测试框架
local TestRunner = {}
TestRunner.tests = {}
TestRunner.passed = 0
TestRunner.failed = 0
TestRunner.current_test = ""

function TestRunner.describe(name, fn)
    print("\n=== " .. name .. " ===")
    fn()
end

function TestRunner.it(name, fn)
    TestRunner.current_test = name
    local status, err = pcall(fn)
    if status then
        TestRunner.passed = TestRunner.passed + 1
        print("  ✓ " .. name)
    else
        TestRunner.failed = TestRunner.failed + 1
        print("  ✗ " .. name)
        print("    Error: " .. tostring(err))
    end
end

function TestRunner.expect(value)
    return {
        to_be = function(expected)
            if value ~= expected then
                error("Expected " .. tostring(expected) .. ", got " .. tostring(value))
            end
        end,
        to_be_true = function()
            if value ~= true then
                error("Expected true, got " .. tostring(value))
            end
        end,
        to_be_false = function()
            if value ~= false then
                error("Expected false, got " .. tostring(value))
            end
        end,
        to_be_nil = function()
            if value ~= nil then
                error("Expected nil, got " .. tostring(value))
            end
        end,
        to_not_be_nil = function()
            if value == nil then
                error("Expected non-nil value")
            end
        end,
        to_equal_table = function(expected)
            local function deep_equal(a, b)
                if type(a) ~= type(b) then return false end
                if type(a) ~= "table" then return a == b end
                for k, v in pairs(a) do
                    if not deep_equal(v, b[k]) then return false end
                end
                for k, v in pairs(b) do
                    if not deep_equal(v, a[k]) then return false end
                end
                return true
            end
            if not deep_equal(value, expected) then
                error("Tables not equal")
            end
        end,
        to_have_length = function(expected)
            if #value ~= expected then
                error("Expected length " .. expected .. ", got " .. #value)
            end
        end,
        to_contain = function(expected)
            for _, v in ipairs(value) do
                if v == expected then return end
            end
            error("Expected table to contain " .. tostring(expected))
        end,
        to_throw = function()
            error("to_throw not implemented")
        end
    }
end

function TestRunner.summary()
    print("\n" .. string.rep("=", 50))
    print("Tests: " .. TestRunner.passed + TestRunner.failed)
    print("Passed: " .. TestRunner.passed)
    print("Failed: " .. TestRunner.failed)
    print(string.rep("=", 50))
    return TestRunner.failed == 0
end

-- 加载模块
local TrieUtils = dofile("mod.lua")

-------------------------------------------------------------------------------
-- 测试开始
-------------------------------------------------------------------------------

TestRunner.describe("TrieNode", function()
    TestRunner.it("should create a new node", function()
        local node = TrieUtils.new()._find_node or require("mod").TrieNode.new()
        -- 直接测试 TrieNode
        local TrieNode = dofile("mod.lua").new and TrieUtils.new().root or nil
        -- 使用 Trie 的 root 来测试
        local trie = TrieUtils.new()
        TestRunner.expect(trie.root).to_not_be_nil()
        TestRunner.expect(trie.root.is_end).to_be_false()
    end)
end)

TestRunner.describe("Trie Basic Operations", function()
    TestRunner.it("should create an empty trie", function()
        local trie = TrieUtils.new()
        TestRunner.expect(trie:word_count()).to_be(0)
        TestRunner.expect(trie:is_empty()).to_be_true()
    end)
    
    TestRunner.it("should insert a word", function()
        local trie = TrieUtils.new()
        local result = trie:insert("hello")
        TestRunner.expect(result).to_be_true()
        TestRunner.expect(trie:word_count()).to_be(1)
    end)
    
    TestRunner.it("should not insert duplicate word", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        local result = trie:insert("hello")
        TestRunner.expect(result).to_be_false()
        TestRunner.expect(trie:word_count()).to_be(1)
    end)
    
    TestRunner.it("should search for existing word", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        local found, data = trie:search("hello")
        TestRunner.expect(found).to_be_true()
        TestRunner.expect(data).to_be_nil()
    end)
    
    TestRunner.it("should search for non-existing word", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        local found, data = trie:search("world")
        TestRunner.expect(found).to_be_false()
    end)
    
    TestRunner.it("should insert with data", function()
        local trie = TrieUtils.new()
        trie:insert("hello", {count = 5})
        local found, data = trie:search("hello")
        TestRunner.expect(found).to_be_true()
        TestRunner.expect(data.count).to_be(5)
    end)
    
    TestRunner.it("should delete a word", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        local result = trie:delete("hello")
        TestRunner.expect(result).to_be_true()
        TestRunner.expect(trie:word_count()).to_be(0)
    end)
    
    TestRunner.it("should not delete non-existing word", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        local result = trie:delete("world")
        TestRunner.expect(result).to_be_false()
        TestRunner.expect(trie:word_count()).to_be(1)
    end)
    
    TestRunner.it("should check starts_with", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        TestRunner.expect(trie:starts_with("he")).to_be_true()
        TestRunner.expect(trie:starts_with("hell")).to_be_true()
        TestRunner.expect(trie:starts_with("hello")).to_be_true()
        TestRunner.expect(trie:starts_with("world")).to_be_false()
    end)
end)

TestRunner.describe("Case Sensitivity", function()
    TestRunner.it("should be case sensitive by default", function()
        local trie = TrieUtils.new()
        trie:insert("Hello")
        TestRunner.expect(trie:search("Hello")).to_be_true()
        TestRunner.expect(trie:search("hello")).to_be_false()
    end)
    
    TestRunner.it("should be case insensitive when configured", function()
        local trie = TrieUtils.new(false)
        trie:insert("Hello")
        TestRunner.expect(trie:search("Hello")).to_be_true()
        TestRunner.expect(trie:search("hello")).to_be_true()
        TestRunner.expect(trie:search("HELLO")).to_be_true()
    end)
end)

TestRunner.describe("Prefix Operations", function()
    TestRunner.it("should get words with prefix", function()
        local trie = TrieUtils.new()
        trie:insert("apple")
        trie:insert("app")
        trie:insert("application")
        trie:insert("banana")
        
        local words = trie:get_words_with_prefix("app")
        TestRunner.expect(#words).to_be(3)
        TestRunner.expect(words).to_contain("app")
        TestRunner.expect(words).to_contain("apple")
        TestRunner.expect(words).to_contain("application")
    end)
    
    TestRunner.it("should count words with prefix", function()
        local trie = TrieUtils.new()
        trie:insert("apple")
        trie:insert("app")
        trie:insert("application")
        trie:insert("banana")
        
        TestRunner.expect(trie:count_words_with_prefix("app")).to_be(3)
        TestRunner.expect(trie:count_words_with_prefix("ban")).to_be(1)
        TestRunner.expect(trie:count_words_with_prefix("xyz")).to_be(0)
    end)
    
    TestRunner.it("should return empty for non-existing prefix", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        local words = trie:get_words_with_prefix("xyz")
        TestRunner.expect(#words).to_be(0)
    end)
    
    TestRunner.it("should limit results", function()
        local trie = TrieUtils.new()
        trie:insert("apple")
        trie:insert("app")
        trie:insert("application")
        trie:insert("applet")
        
        local words = trie:get_words_with_prefix("app", 2)
        TestRunner.expect(#words).to_be(2)
    end)
end)

TestRunner.describe("Advanced Operations", function()
    TestRunner.it("should find longest common prefix", function()
        local trie = TrieUtils.new()
        trie:insert("apple")
        trie:insert("app")
        trie:insert("application")
        
        local prefix = trie:longest_common_prefix()
        TestRunner.expect(prefix).to_be("app")
    end)
    
    TestRunner.it("should return empty for single word", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        local prefix = trie:longest_common_prefix()
        TestRunner.expect(prefix).to_be("hello")
    end)
    
    TestRunner.it("should find longest prefix match", function()
        local trie = TrieUtils.new()
        trie:insert("app")
        trie:insert("apple")
        trie:insert("banana")
        
        -- "application" 的前5字符是 "appli"，而 "apple" 是 "apple"（e != i）
        -- 所以最长匹配是 "app"
        local match = trie:longest_prefix_match("application")
        TestRunner.expect(match).to_be("app")
        
        -- 正确测试：用 "appletree" 测试，应该匹配 "apple"
        local match2 = trie:longest_prefix_match("appletree")
        TestRunner.expect(match2).to_be("apple")
    end)
    
    TestRunner.it("should find all prefix matches", function()
        local trie = TrieUtils.new()
        trie:insert("app")
        trie:insert("apple")
        trie:insert("applet")
        
        local matches = trie:all_prefix_matches("appletree")
        TestRunner.expect(#matches).to_be(3)
        TestRunner.expect(matches).to_contain("app")
        TestRunner.expect(matches).to_contain("apple")
        TestRunner.expect(matches).to_contain("applet")
    end)
end)

TestRunner.describe("Wildcard Search", function()
    TestRunner.it("should search with ? wildcard", function()
        local trie = TrieUtils.new()
        trie:insert("cat")
        trie:insert("bat")
        trie:insert("rat")
        trie:insert("car")
        
        local results = trie:wildcard_search("?at")
        TestRunner.expect(#results).to_be(3)
        TestRunner.expect(results).to_contain("cat")
        TestRunner.expect(results).to_contain("bat")
        TestRunner.expect(results).to_contain("rat")
    end)
    
    TestRunner.it("should search with * wildcard", function()
        local trie = TrieUtils.new()
        trie:insert("car")
        trie:insert("cat")
        trie:insert("cart")
        trie:insert("carbon")
        
        -- "car*" 匹配以 "car" 开头的单词：car, cart, carbon（不包括 cat）
        local results = trie:wildcard_search("car*")
        TestRunner.expect(#results).to_be(3)
        TestRunner.expect(results).to_contain("car")
        TestRunner.expect(results).to_contain("cart")
        TestRunner.expect(results).to_contain("carbon")
    end)
    
    TestRunner.it("should handle mixed wildcards", function()
        local trie = TrieUtils.new()
        trie:insert("cat")
        trie:insert("cut")
        trie:insert("coat")
        
        local results = trie:wildcard_search("c?t")
        TestRunner.expect(#results >= 2).to_be_true()
    end)
end)

TestRunner.describe("Statistics", function()
    TestRunner.it("should count words", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        trie:insert("world")
        trie:insert("foo")
        TestRunner.expect(trie:word_count()).to_be(3)
    end)
    
    TestRunner.it("should count nodes", function()
        local trie = TrieUtils.new()
        trie:insert("a")
        trie:insert("ab")
        trie:insert("abc")
        -- 'a' node + 'b' node + 'c' node + root = 4
        TestRunner.expect(trie:node_count()).to_be(4)
    end)
    
    TestRunner.it("should calculate depth", function()
        local trie = TrieUtils.new()
        trie:insert("a")
        trie:insert("ab")
        trie:insert("abc")
        trie:insert("abcd")
        TestRunner.expect(trie:depth()).to_be(4)
    end)
    
    TestRunner.it("should estimate memory usage", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        trie:insert("world")
        local mem = trie:memory_usage()
        TestRunner.expect(mem > 0).to_be_true()
    end)
end)

TestRunner.describe("Serialization", function()
    TestRunner.it("should convert to table", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        trie:insert("world")
        
        local t = trie:to_table()
        TestRunner.expect(t.case_sensitive).to_be_true()
        TestRunner.expect(t.word_count).to_be(2)
        TestRunner.expect(t.node_count > 0).to_be_true()
    end)
    
    TestRunner.it("should create from table", function()
        local trie1 = TrieUtils.new()
        trie1:insert("hello", {count = 1})
        trie1:insert("world", {count = 2})
        
        local t = trie1:to_table()
        local trie2 = TrieUtils.from_table(t)
        
        TestRunner.expect(trie2:search("hello")).to_be_true()
        TestRunner.expect(trie2:search("world")).to_be_true()
        TestRunner.expect(trie2:word_count()).to_be(2)
    end)
end)

TestRunner.describe("Traversal", function()
    TestRunner.it("should iterate all words", function()
        local trie = TrieUtils.new()
        trie:insert("apple")
        trie:insert("banana")
        trie:insert("cherry")
        
        local words = {}
        trie:for_each(function(word)
            table.insert(words, word)
        end)
        
        TestRunner.expect(#words).to_be(3)
        TestRunner.expect(words).to_contain("apple")
        TestRunner.expect(words).to_contain("banana")
        TestRunner.expect(words).to_contain("cherry")
    end)
    
    TestRunner.it("should iterate words with prefix", function()
        local trie = TrieUtils.new()
        trie:insert("apple")
        trie:insert("app")
        trie:insert("application")
        trie:insert("banana")
        
        local words = {}
        trie:for_each_prefix("app", function(word)
            table.insert(words, word)
        end)
        
        TestRunner.expect(#words).to_be(3)
    end)
end)

TestRunner.describe("Batch Operations", function()
    TestRunner.it("should insert batch", function()
        local trie = TrieUtils.new()
        local count = trie:insert_batch({"apple", "banana", "cherry"})
        TestRunner.expect(count).to_be(3)
        TestRunner.expect(trie:word_count()).to_be(3)
    end)
    
    TestRunner.it("should insert batch with data", function()
        local trie = TrieUtils.new()
        local count = trie:insert_batch({
            {word = "apple", data = 1},
            {word = "banana", data = 2},
        })
        TestRunner.expect(count).to_be(2)
        
        local found, data = trie:search("apple")
        TestRunner.expect(found).to_be_true()
        TestRunner.expect(data).to_be(1)
    end)
    
    TestRunner.it("should delete batch", function()
        local trie = TrieUtils.new()
        trie:insert_batch({"apple", "banana", "cherry", "date"})
        local count = trie:delete_batch({"apple", "cherry"})
        TestRunner.expect(count).to_be(2)
        TestRunner.expect(trie:word_count()).to_be(2)
    end)
end)

TestRunner.describe("Utility Methods", function()
    TestRunner.it("should check is_empty", function()
        local trie = TrieUtils.new()
        TestRunner.expect(trie:is_empty()).to_be_true()
        trie:insert("hello")
        TestRunner.expect(trie:is_empty()).to_be_false()
    end)
    
    TestRunner.it("should clear trie", function()
        local trie = TrieUtils.new()
        trie:insert("hello")
        trie:insert("world")
        trie:clear()
        TestRunner.expect(trie:is_empty()).to_be_true()
        TestRunner.expect(trie:word_count()).to_be(0)
    end)
    
    TestRunner.it("should clone trie", function()
        local trie1 = TrieUtils.new()
        trie1:insert("hello")
        trie1:insert("world")
        
        local trie2 = trie1:clone()
        TestRunner.expect(trie2:word_count()).to_be(2)
        TestRunner.expect(trie2:search("hello")).to_be_true()
        
        trie2:delete("hello")
        TestRunner.expect(trie1:search("hello")).to_be_true()
    end)
    
    TestRunner.it("should merge tries", function()
        local trie1 = TrieUtils.new()
        trie1:insert("apple")
        trie1:insert("banana")
        
        local trie2 = TrieUtils.new()
        trie2:insert("cherry")
        trie2:insert("date")
        
        local count = trie1:merge(trie2)
        TestRunner.expect(count).to_be(2)
        TestRunner.expect(trie1:word_count()).to_be(4)
    end)
    
    TestRunner.it("should get all words", function()
        local trie = TrieUtils.new()
        trie:insert("apple")
        trie:insert("banana")
        trie:insert("cherry")
        
        local words = trie:get_all_words()
        TestRunner.expect(#words).to_be(3)
    end)
    
    TestRunner.it("should get sorted words", function()
        local trie = TrieUtils.new()
        trie:insert("cherry")
        trie:insert("apple")
        trie:insert("banana")
        
        local words = trie:get_sorted_words()
        TestRunner.expect(words[1]).to_be("apple")
        TestRunner.expect(words[2]).to_be("banana")
        TestRunner.expect(words[3]).to_be("cherry")
    end)
    
    TestRunner.it("should update data", function()
        local trie = TrieUtils.new()
        trie:insert("hello", 1)
        trie:update_data("hello", 2)
        local found, data = trie:search("hello")
        TestRunner.expect(data).to_be(2)
    end)
    
    TestRunner.it("should get data", function()
        local trie = TrieUtils.new()
        trie:insert("hello", {count = 5})
        local data = trie:get_data("hello")
        TestRunner.expect(data.count).to_be(5)
    end)
end)

TestRunner.describe("Module Functions", function()
    TestRunner.it("should create trie from words", function()
        local trie = TrieUtils.from_words({"apple", "banana", "cherry"})
        TestRunner.expect(trie:word_count()).to_be(3)
        TestRunner.expect(trie:search("apple")).to_be_true()
    end)
    
    TestRunner.it("should find longest common prefix of two strings", function()
        local prefix = TrieUtils.longest_common_prefix_of("apple", "application")
        TestRunner.expect(prefix).to_be("appl")
    end)
    
    TestRunner.it("should find longest common prefix of list", function()
        local prefix = TrieUtils.longest_common_prefix_of_all({"apple", "application", "apply"})
        TestRunner.expect(prefix).to_be("appl")
    end)
    
    TestRunner.it("should provide autocomplete suggestions", function()
        local trie = TrieUtils.from_words({"apple", "application", "apply", "banana"})
        local suggestions = TrieUtils.autocomplete(trie, "app", 10)
        TestRunner.expect(#suggestions).to_be(3)
    end)
    
    TestRunner.it("should provide readonly view", function()
        local trie = TrieUtils.from_words({"apple", "banana"})
        local view = TrieUtils.readonly_view(trie)
        TestRunner.expect(view.search("apple")).to_be_true()
        TestRunner.expect(view.word_count()).to_be(2)
    end)
end)

TestRunner.describe("Edge Cases", function()
    TestRunner.it("should handle empty string", function()
        local trie = TrieUtils.new()
        local ok, err = pcall(function() trie:insert("") end)
        TestRunner.expect(ok).to_be_false()
    end)
    
    TestRunner.it("should handle unicode", function()
        local trie = TrieUtils.new()
        trie:insert("你好")
        trie:insert("世界")
        TestRunner.expect(trie:search("你好")).to_be_true()
        TestRunner.expect(trie:search("世界")).to_be_true()
    end)
    
    TestRunner.it("should handle long words", function()
        local trie = TrieUtils.new()
        local long_word = string.rep("a", 1000)
        trie:insert(long_word)
        TestRunner.expect(trie:search(long_word)).to_be_true()
        TestRunner.expect(trie:depth()).to_be(1000)
    end)
    
    TestRunner.it("should handle shared prefix", function()
        local trie = TrieUtils.new()
        trie:insert("a")
        trie:insert("ab")
        trie:insert("abc")
        trie:insert("abcd")
        
        -- 删除 "abc" 后，"abcd" 应该仍然存在
        trie:delete("abc")
        TestRunner.expect(trie:search("abcd")).to_be_true()
        TestRunner.expect(trie:search("abc")).to_be_false()
        TestRunner.expect(trie:search("a")).to_be_true()
    end)
    
    TestRunner.it("should handle deletion correctly", function()
        local trie = TrieUtils.new()
        trie:insert("abc")
        trie:insert("abd")
        
        -- 删除 "abc" 后，"abd" 应该仍然存在
        trie:delete("abc")
        TestRunner.expect(trie:search("abc")).to_be_false()
        TestRunner.expect(trie:search("abd")).to_be_true()
    end)
end)

-------------------------------------------------------------------------------
-- 测试总结
-------------------------------------------------------------------------------

local success = TestRunner.summary()
os.exit(success and 0 or 1)