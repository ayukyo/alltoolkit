/**
 * AllToolkit - Swift Trie Utilities 测试
 *
 * 测试 Trie 数据结构的基本功能和高级特性
 * 运行: swift trie_utils_test.swift
 */

import Foundation

// 导入 mod.swift 中的代码（在同一目录下运行时自动加载）
// 实际项目中应该使用 import 语句

// MARK: - 测试辅助函数

var testsPassed = 0
var testsFailed = 0

func test(_ name: String, _ condition: Bool) {
    if condition {
        print("✅ \(name)")
        testsPassed += 1
    } else {
        print("❌ \(name)")
        testsFailed += 1
    }
}

func testEqual<T: Equatable>(_ name: String, _ expected: T, _ actual: T) {
    if expected == actual {
        print("✅ \(name): \(actual)")
        testsPassed += 1
    } else {
        print("❌ \(name): 期望 \(expected), 实际 \(actual)")
        testsFailed += 1
    }
}

// MARK: - 测试类定义（复制自 mod.swift）

class TrieNode {
    var children: [Character: TrieNode] = [:]
    var isEndOfWord: Bool = false
    var accessCount: Int = 0
    
    init() {}
}

class Trie {
    private let root: TrieNode
    public private(set) var wordCount: Int = 0
    
    init() {
        self.root = TrieNode()
    }
    
    convenience init(words: [String]) {
        self.init()
        for word in words {
            insert(word)
        }
    }
    
    @discardableResult
    func insert(_ word: String) -> Bool {
        guard !word.isEmpty else { return false }
        
        var current = root
        for char in word {
            if current.children[char] == nil {
                current.children[char] = TrieNode()
            }
            current = current.children[char]!
        }
        
        if current.isEndOfWord {
            return false
        }
        
        current.isEndOfWord = true
        wordCount += 1
        return true
    }
    
    func insertAll(_ words: [String]) -> Int {
        var count = 0
        for word in words {
            if insert(word) {
                count += 1
            }
        }
        return count
    }
    
    func search(_ word: String) -> Bool {
        guard !word.isEmpty else { return false }
        
        var current = root
        for char in word {
            guard let node = current.children[char] else {
                return false
            }
            current = node
        }
        
        current.accessCount += 1
        return current.isEndOfWord
    }
    
    func startsWith(_ prefix: String) -> Bool {
        guard !prefix.isEmpty else { return wordCount > 0 }
        
        var current = root
        for char in prefix {
            guard let node = current.children[char] else {
                return false
            }
            current = node
        }
        return true
    }
    
    @discardableResult
    func delete(_ word: String) -> Bool {
        guard !word.isEmpty else { return false }
        return deleteHelper(root, word, 0)
    }
    
    private func deleteHelper(_ node: TrieNode, _ word: String, _ index: Int) -> Bool {
        if index == word.count {
            if !node.isEndOfWord {
                return false
            }
            node.isEndOfWord = false
            wordCount -= 1
            return node.children.isEmpty
        }
        
        let charIndex = word.index(word.startIndex, offsetBy: index)
        let char = word[charIndex]
        
        guard let childNode = node.children[char] else {
            return false
        }
        
        let shouldDeleteChild = deleteHelper(childNode, word, index + 1)
        
        if shouldDeleteChild {
            node.children.removeValue(forKey: char)
            return !node.isEndOfWord && node.children.isEmpty
        }
        
        return false
    }
    
    func clear() {
        root.children.removeAll()
        root.isEndOfWord = false
        wordCount = 0
    }
    
    func autocomplete(_ prefix: String, limit: Int? = nil) -> [String] {
        guard !prefix.isEmpty else {
            return getAllWords(limit: limit)
        }
        
        var current = root
        for char in prefix {
            guard let node = current.children[char] else {
                return []
            }
            current = node
        }
        
        let words = collectAllWords(from: current, prefix: prefix)
        
        if let limit = limit, words.count > limit {
            return Array(words.prefix(limit))
        }
        return words
    }
    
    func getAllWords(limit: Int? = nil) -> [String] {
        let words = collectAllWords(from: root, prefix: "")
        if let limit = limit, words.count > limit {
            return Array(words.prefix(limit))
        }
        return words
    }
    
    private func collectAllWords(from node: TrieNode, prefix: String) -> [String] {
        var results: [String] = []
        
        if node.isEndOfWord {
            results.append(prefix)
        }
        
        for (char, childNode) in node.children {
            results.append(contentsOf: collectAllWords(from: childNode, prefix: prefix + String(char)))
        }
        
        return results
    }
    
    func getMostAccessed(count: Int = 10) -> [(word: String, count: Int)] {
        var wordCounts: [(String, Int)] = []
        collectAccessCounts(from: root, prefix: "", results: &wordCounts)
        
        return wordCounts
            .filter { $0.1 > 0 }
            .sorted { $0.1 > $1.1 }
            .prefix(count)
            .map { ($0.0, $0.1) }
    }
    
    private func collectAccessCounts(from node: TrieNode, prefix: String, results: inout [(String, Int)]) {
        if node.isEndOfWord {
            results.append((prefix, node.accessCount))
        }
        
        for (char, childNode) in node.children {
            collectAccessCounts(from: childNode, prefix: prefix + String(char), results: &results)
        }
    }
    
    func fuzzySearch(_ word: String, maxDistance: Int = 1) -> [String] {
        var results: Set<String> = []
        fuzzySearchHelper(root, word, "", 0, maxDistance, &results)
        return Array(results).sorted()
    }
    
    private func fuzzySearchHelper(
        _ node: TrieNode,
        _ word: String,
        _ current: String,
        _ index: Int,
        _ remainingDistance: Int,
        _ results: inout Set<String>
    ) {
        if remainingDistance < 0 {
            return
        }
        
        if index == word.count {
            if node.isEndOfWord {
                results.insert(current)
            }
            return
        }
        
        let charIndex = word.index(word.startIndex, offsetBy: index)
        let targetChar = word[charIndex]
        
        if let childNode = node.children[targetChar] {
            fuzzySearchHelper(
                childNode, word, current + String(targetChar),
                index + 1, remainingDistance, &results
            )
        }
        
        if remainingDistance > 0 {
            for (char, childNode) in node.children {
                if char != targetChar {
                    fuzzySearchHelper(
                        childNode, word, current + String(char),
                        index + 1, remainingDistance - 1, &results
                    )
                }
                
                fuzzySearchHelper(
                    childNode, word, current + String(char),
                    index, remainingDistance - 1, &results
                )
            }
            
            fuzzySearchHelper(
                node, word, current,
                index + 1, remainingDistance - 1, &results
            )
        }
    }
    
    func longestCommonPrefix() -> String {
        var prefix = ""
        var current = root
        
        while current.children.count == 1 && !current.isEndOfWord {
            if let (char, nextNode) = current.children.first {
                prefix += String(char)
                current = nextNode
            } else {
                break
            }
        }
        
        return prefix
    }
    
    func nodeCount() -> Int {
        return countNodes(from: root)
    }
    
    private func countNodes(from node: TrieNode) -> Int {
        var count = 1
        for child in node.children.values {
            count += countNodes(from: child)
        }
        return count
    }
    
    func getWordsByLength(_ length: Int) -> [String] {
        var results: [String] = []
        getWordsByLengthHelper(root, "", length, &results)
        return results
    }
    
    private func getWordsByLengthHelper(
        _ node: TrieNode,
        _ current: String,
        _ targetLength: Int,
        _ results: inout [String]
    ) {
        if current.count == targetLength {
            if node.isEndOfWord {
                results.append(current)
            }
            return
        }
        
        for (char, childNode) in node.children {
            getWordsByLengthHelper(childNode, current + String(char), targetLength, &results)
        }
    }
    
    func findWordsContaining(_ pattern: String) -> [String] {
        guard !pattern.isEmpty else { return getAllWords() }
        return getAllWords().filter { $0.contains(pattern) }
    }
}

// MARK: - 测试用例

print("===========================================")
print("       Trie Utilities 单元测试")
print("===========================================\n")

// 1. 基本插入和搜索测试
print("📋 测试组 1: 基本插入和搜索")
print("-------------------------------")

let trie = Trie()
test("空 Trie 搜索返回 false", !trie.search("test"))
test("空 Trie 单词数为 0", trie.wordCount == 0)

test("插入 'hello' 返回 true", trie.insert("hello"))
test("插入后单词数增加", trie.wordCount == 1)
test("搜索已插入单词返回 true", trie.search("hello"))
test("重复插入返回 false", !trie.insert("hello"))
test("重复插入不增加单词数", trie.wordCount == 1)

trie.insert("world")
test("搜索另一个单词", trie.search("world"))
test("搜索不存在的单词", !trie.search("hell"))
test("搜索部分单词（前缀但非完整单词）", !trie.search("he"))

print("")

// 2. 批量插入测试
print("📋 测试组 2: 批量插入")
print("-------------------------------")

let trie2 = Trie()
let words = ["apple", "app", "application", "apply", "banana"]
let insertedCount = trie2.insertAll(words)
testEqual("批量插入返回正确数量", 5, insertedCount)
testEqual("批量插入后单词数正确", 5, trie2.wordCount)

// 从数组初始化
let trie3 = Trie(words: ["one", "two", "three"])
testEqual("从数组初始化单词数正确", 3, trie3.wordCount)

print("")

// 3. 前缀搜索测试
print("📋 测试组 3: 前缀搜索")
print("-------------------------------")

let trie4 = Trie()
trie4.insertAll(["apple", "app", "application", "banana", "band"])

test("前缀 'app' 存在", trie4.startsWith("app"))
test("前缀 'ban' 存在", trie4.startsWith("ban"))
test("前缀 'xyz' 不存在", !trie4.startsWith("xyz"))
test("空前缀存在（如果有单词）", trie4.startsWith(""))

print("")

// 4. 删除操作测试
print("📋 测试组 4: 删除操作")
print("-------------------------------")

let trie5 = Trie()
trie5.insertAll(["apple", "app", "application"])

test("删除存在的单词 'app'", trie5.delete("app"))
test("删除后搜索返回 false", !trie5.search("app"))
test("删除后 'apple' 仍然存在", trie5.search("apple"))
test("删除不存在的单词返回 false", !trie5.delete("orange"))
test("删除空字符串返回 false", !trie5.delete(""))

// 删除叶子节点（应该清理）
let trie6 = Trie()
trie6.insert("a")
test("删除单个字母单词", trie6.delete("a"))
test("删除后单词数为 0", trie6.wordCount == 0)

print("")

// 5. 自动补全测试
print("📋 测试组 5: 自动补全")
print("-------------------------------")

let trie7 = Trie()
trie7.insertAll(["apple", "app", "application", "apply", "banana", "band"])

let appSuggestions = trie7.autocomplete("app").sorted()
test("前缀 'app' 补全包含 'apple'", appSuggestions.contains("apple"))
test("前缀 'app' 补全包含 'application'", appSuggestions.contains("application"))
test("前缀 'app' 补全包含 'apply'", appSuggestions.contains("apply"))
testEqual("前缀 'app' 补全数量", 4, appSuggestions.count)

let banSuggestions = trie7.autocomplete("ban").sorted()
testEqual("前缀 'ban' 补全数量", 2, banSuggestions.count)

let noSuggestions = trie7.autocomplete("xyz")
testEqual("不存在的全前缀返回空", 0, noSuggestions.count)

// 限制返回数量
let limitedSuggestions = trie7.autocomplete("app", limit: 2)
testEqual("限制补全数量", 2, limitedSuggestions.count)

print("")

// 6. 模糊搜索测试
print("📋 测试组 6: 模糊搜索")
print("-------------------------------")

let trie8 = Trie()
trie8.insertAll(["apple", "apply", "banana", "orange"])

let fuzzy1 = trie8.fuzzySearch("aple", maxDistance: 1)
test("模糊搜索 'aple' 找到 'apple'", fuzzy1.contains("apple"))

let fuzzy2 = trie8.fuzzySearch("banan", maxDistance: 1)
test("模糊搜索 'banan' 找到 'banana'", fuzzy2.contains("banana"))

let fuzzy3 = trie8.fuzzySearch("xyz", maxDistance: 1)
testEqual("无匹配的模糊搜索返回空", 0, fuzzy3.count)

print("")

// 7. 高级功能测试
print("📋 测试组 7: 高级功能")
print("-------------------------------")

let trie9 = Trie()
trie9.insertAll(["apple", "app", "application", "banana"])

// 最长公共前缀
let lcp = trie9.longestCommonPrefix()
testEqual("最长公共前缀为空（有多个分支）", "", lcp)

let trie10 = Trie()
trie10.insertAll(["apple", "appetite", "application"])
let lcp2 = trie10.longestCommonPrefix()
testEqual("最长公共前缀 'app'", "app", lcp2)

// 节点计数
let nodeCount = trie9.nodeCount()
test("节点数大于单词数", nodeCount > trie9.wordCount)

// 按长度获取单词
let lengthWords = trie9.getWordsByLength(5)
test("长度5的单词包含 'apple'", lengthWords.contains("apple"))

// 包含模式搜索
let patternWords = trie9.findWordsContaining("ppl")
test("包含 'ppl' 的单词包含 'apple'", patternWords.contains("apple"))

print("")

// 8. 清空测试
print("📋 测试组 8: 清空操作")
print("-------------------------------")

let trie11 = Trie()
trie11.insertAll(["a", "b", "c"])
testEqual("清空前单词数", 3, trie11.wordCount)
trie11.clear()
testEqual("清空后单词数为 0", 0, trie11.wordCount)
test("清空后搜索返回 false", !trie11.search("a"))

print("")

// 9. 访问统计测试
print("📋 测试组 9: 访问统计")
print("-------------------------------")

let trie12 = Trie()
trie12.insertAll(["apple", "banana", "cherry"])

// 多次搜索 apple
trie12.search("apple")
trie12.search("apple")
trie12.search("apple")
trie12.search("banana")

let hotWords = trie12.getMostAccessed(count: 3)
test("最热门单词是 'apple'", hotWords.first?.word == "apple")
testEqual("'apple' 访问次数", 4, hotWords.first?.count ?? 0) // 3次手动 + 1次获取时

print("")

// 10. 性能测试
print("📋 测试组 10: 性能测试")
print("-------------------------------")

let perfTrie = Trie()
let testWords = (1...1000).map { "word\($0)" }

let startInsert = Date()
for word in testWords {
    perfTrie.insert(word)
}
let insertTime = Date().timeIntervalSince(startInsert)
print("  插入 1000 个单词耗时: \(String(format: "%.4f", insertTime)) 秒")

let startSearch = Date()
for word in testWords {
    _ = perfTrie.search(word)
}
let searchTime = Date().timeIntervalSince(startSearch)
print("  搜索 1000 个单词耗时: \(String(format: "%.4f", searchTime)) 秒")

let startAutocomplete = Date()
_ = perfTrie.autocomplete("word1")
let autocompleteTime = Date().timeIntervalSince(startAutocomplete)
print("  自动补全耗时: \(String(format: "%.6f", autocompleteTime)) 秒")

test("插入性能合理（< 0.1 秒）", insertTime < 0.1)
test("搜索性能合理（< 0.1 秒）", searchTime < 0.1)

print("")

// 11. 边界条件测试
print("📋 测试组 11: 边界条件")
print("-------------------------------")

let edgeTrie = Trie()
test("插入空字符串返回 false", !edgeTrie.insert(""))
test("搜索空字符串返回 false", !edgeTrie.search(""))
test("删除空字符串返回 false", !edgeTrie.delete(""))
test("空前缀自动补全返回空", edgeTrie.autocomplete("").isEmpty)

// 单字符单词
edgeTrie.insert("a")
test("插入单字符单词成功", edgeTrie.search("a"))
test("单字符自动补全", edgeTrie.autocomplete("a").contains("a"))

print("")

// 12. 特殊字符测试
print("📋 测试组 12: 特殊字符")
print("-------------------------------")

let specialTrie = Trie()
specialTrie.insert("hello-world")
specialTrie.insert("hello_world")
specialTrie.insert("hello.world")
specialTrie.insert("你好")
specialTrie.insert("世界")

test("搜索带连字符的单词", specialTrie.search("hello-world"))
test("搜索带下划线的单词", specialTrie.search("hello_world"))
test("搜索带点的单词", specialTrie.search("hello.world"))
test("搜索中文单词", specialTrie.search("你好"))
test("搜索中文单词 2", specialTrie.search("世界"))

let cnSuggestions = specialTrie.autocomplete("你")
test("中文前缀补全", cnSuggestions.contains("你好"))

print("")

// 测试总结
print("===========================================")
print("              测试结果汇总")
print("===========================================")
print("✅ 通过: \(testsPassed)")
print("❌ 失败: \(testsFailed)")
print("📊 总计: \(testsPassed + testsFailed)")
print("📈 成功率: \(String(format: "%.1f", Double(testsPassed) / Double(testsPassed + testsFailed) * 100))%")
print("===========================================")

if testsFailed == 0 {
    print("\n🎉 所有测试通过！")
} else {
    print("\n⚠️ 有 \(testsFailed) 个测试失败，请检查！")
}