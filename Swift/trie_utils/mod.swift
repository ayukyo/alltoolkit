/**
 * AllToolkit - Swift Trie Utilities
 *
 * Trie（前缀树）工具类，提供高效的字符串存储、前缀搜索和自动补全功能。
 * 零依赖，仅使用 Swift 标准库。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - Trie 节点

/// Trie 树的节点类
public class TrieNode {
    /// 子节点字典
    public var children: [Character: TrieNode] = [:]
    
    /// 标记是否为单词结尾
    public var isEndOfWord: Bool = false
    
    /// 该节点的访问计数（用于热门词统计）
    public var accessCount: Int = 0
    
    public init() {}
}

// MARK: - Trie 类

/// Trie（前缀树）数据结构
/// 适用于字符串存储、前缀搜索、自动补全等场景
public class Trie {
    
    /// 根节点
    private let root: TrieNode
    
    /// 单词数量
    public private(set) var wordCount: Int = 0
    
    /// 初始化空 Trie
    public init() {
        self.root = TrieNode()
    }
    
    /// 从字符串数组初始化 Trie
    /// - Parameter words: 初始单词列表
    public convenience init(words: [String]) {
        self.init()
        for word in words {
            insert(word)
        }
    }
    
    // MARK: - 基本操作
    
    /// 插入单词到 Trie
    /// - Parameter word: 要插入的单词
    /// - Returns: true 如果是新单词，false 如果单词已存在
    @discardableResult
    public func insert(_ word: String) -> Bool {
        guard !word.isEmpty else { return false }
        
        var current = root
        for char in word {
            if current.children[char] == nil {
                current.children[char] = TrieNode()
            }
            current = current.children[char]!
        }
        
        if current.isEndOfWord {
            return false // 单词已存在
        }
        
        current.isEndOfWord = true
        wordCount += 1
        return true
    }
    
    /// 批量插入单词
    /// - Parameter words: 单词列表
    /// - Returns: 成功插入的新单词数量
    public func insertAll(_ words: [String]) -> Int {
        var count = 0
        for word in words {
            if insert(word) {
                count += 1
            }
        }
        return count
    }
    
    /// 搜索单词是否存在于 Trie
    /// - Parameter word: 要搜索的单词
    /// - Returns: true 如果单词存在
    public func search(_ word: String) -> Bool {
        guard !word.isEmpty else { return false }
        
        var current = root
        for char in word {
            guard let node = current.children[char] else {
                return false
            }
            current = node
        }
        
        current.accessCount += 1 // 增加访问计数
        return current.isEndOfWord
    }
    
    /// 检查是否存在以给定前缀开头的单词
    /// - Parameter prefix: 前缀字符串
    /// - Returns: true 如果存在以该前缀开头的单词
    public func startsWith(_ prefix: String) -> Bool {
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
    
    /// 删除单词
    /// - Parameter word: 要删除的单词
    /// - Returns: true 如果删除成功
    @discardableResult
    public func delete(_ word: String) -> Bool {
        guard !word.isEmpty else { return false }
        return deleteHelper(root, word, 0)
    }
    
    /// 递归删除辅助函数
    private func deleteHelper(_ node: TrieNode, _ word: String, _ index: Int) -> Bool {
        if index == word.count {
            if !node.isEndOfWord {
                return false // 单词不存在
            }
            node.isEndOfWord = false
            wordCount -= 1
            // 如果节点没有子节点，可以被删除
            return node.children.isEmpty
        }
        
        let charIndex = word.index(word.startIndex, offsetBy: index)
        let char = word[charIndex]
        
        guard let childNode = node.children[char] else {
            return false // 单词不存在
        }
        
        let shouldDeleteChild = deleteHelper(childNode, word, index + 1)
        
        if shouldDeleteChild {
            node.children.removeValue(forKey: char)
            // 当前节点不是单词结尾且没有其他子节点时可以删除
            return !node.isEndOfWord && node.children.isEmpty
        }
        
        return false
    }
    
    /// 清空 Trie
    public func clear() {
        root.children.removeAll()
        root.isEndOfWord = false
        wordCount = 0
    }
    
    // MARK: - 自动补全
    
    /// 获取所有以给定前缀开头的单词
    /// - Parameters:
    ///   - prefix: 前缀字符串
    ///   - limit: 最大返回数量，默认不限制
    /// - Returns: 匹配的单词列表
    public func autocomplete(_ prefix: String, limit: Int? = nil) -> [String] {
        guard !prefix.isEmpty else {
            return getAllWords(limit: limit)
        }
        
        // 找到前缀对应的节点
        var current = root
        for char in prefix {
            guard let node = current.children[char] else {
                return [] // 前缀不存在
            }
            current = node
        }
        
        // 从该节点开始收集所有单词
        let words = collectAllWords(from: current, prefix: prefix)
        
        if let limit = limit, words.count > limit {
            return Array(words.prefix(limit))
        }
        return words
    }
    
    /// 获取 Trie 中所有单词
    /// - Parameter limit: 最大返回数量
    /// - Returns: 所有单词列表
    public func getAllWords(limit: Int? = nil) -> [String] {
        let words = collectAllWords(from: root, prefix: "")
        if let limit = limit, words.count > limit {
            return Array(words.prefix(limit))
        }
        return words
    }
    
    /// 从指定节点收集所有单词
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
    
    // MARK: - 高级功能
    
    /// 获取最热门的单词（基于访问计数）
    /// - Parameter count: 返回数量
    /// - Returns: 热门单词列表（单词, 访问次数）
    public func getMostAccessed(count: Int = 10) -> [(word: String, count: Int)] {
        var wordCounts: [(String, Int)] = []
        collectAccessCounts(from: root, prefix: "", results: &wordCounts)
        
        return wordCounts
            .filter { $0.1 > 0 }
            .sorted { $0.1 > $1.1 }
            .prefix(count)
            .map { ($0.0, $0.1) }
    }
    
    /// 收集所有单词的访问计数
    private func collectAccessCounts(from node: TrieNode, prefix: String, results: inout [(String, Int)]) {
        if node.isEndOfWord {
            results.append((prefix, node.accessCount))
        }
        
        for (char, childNode) in node.children {
            collectAccessCounts(from: childNode, prefix: prefix + String(char), results: &results)
        }
    }
    
    /// 模糊搜索 - 允许指定数量的字符不匹配
    /// - Parameters:
    ///   - word: 搜索的单词
    ///   - maxDistance: 最大编辑距离
    /// - Returns: 匹配的单词列表
    public func fuzzySearch(_ word: String, maxDistance: Int = 1) -> [String] {
        var results: Set<String> = []
        fuzzySearchHelper(root, word, "", 0, maxDistance, &results)
        return Array(results).sorted()
    }
    
    /// 模糊搜索辅助函数
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
        
        // 尝试匹配当前字符
        if let childNode = node.children[targetChar] {
            fuzzySearchHelper(
                childNode, word, current + String(targetChar),
                index + 1, remainingDistance, &results
            )
        }
        
        // 如果还有剩余距离，尝试替换、插入、删除
        if remainingDistance > 0 {
            for (char, childNode) in node.children {
                // 替换：跳过当前字符，使用其他字符
                if char != targetChar {
                    fuzzySearchHelper(
                        childNode, word, current + String(char),
                        index + 1, remainingDistance - 1, &results
                    )
                }
                
                // 插入：在当前位置插入新字符，不推进 word 的索引
                fuzzySearchHelper(
                    childNode, word, current + String(char),
                    index, remainingDistance - 1, &results
                )
            }
            
            // 删除：跳过当前字符，不添加任何字符
            fuzzySearchHelper(
                node, word, current,
                index + 1, remainingDistance - 1, &results
            )
        }
    }
    
    /// 获取最长公共前缀
    /// - Returns: 所有单词的最长公共前缀
    public func longestCommonPrefix() -> String {
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
    
    /// 统计 Trie 中的节点数量
    /// - Returns: 节点总数
    public func nodeCount() -> Int {
        return countNodes(from: root)
    }
    
    private func countNodes(from node: TrieNode) -> Int {
        var count = 1
        for child in node.children.values {
            count += countNodes(from: child)
        }
        return count
    }
    
    /// 获取指定长度的所有单词
    /// - Parameter length: 单词长度
    /// - Returns: 指定长度的单词列表
    public func getWordsByLength(_ length: Int) -> [String] {
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
    
    /// 查找包含指定字符序列的所有单词
    /// - Parameter pattern: 字符序列
    /// - Returns: 包含该序列的单词列表
    public func findWordsContaining(_ pattern: String) -> [String] {
        guard !pattern.isEmpty else { return getAllWords() }
        
        return getAllWords().filter { $0.contains(pattern) }
    }
}

// MARK: - Trie 扩展：序列协议支持

extension Trie: Sequence {
    public typealias Iterator = AnyIterator<String>
    
    public func makeIterator() -> Iterator {
        var words = getAllWords().makeIterator()
        return AnyIterator { words.next() }
    }
}

// MARK: - Trie 扩展：自定义描述

extension Trie: CustomStringConvertible {
    public var description: String {
        return "Trie(words: \(wordCount), nodes: \(nodeCount()))"
    }
}

// MARK: - Trie 扩展：可编码支持

extension Trie: Codable {
    enum CodingKeys: String, CodingKey {
        case words
    }
    
    public convenience init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        let words = try container.decode([String].self, forKey: .words)
        self.init(words: words)
    }
    
    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(getAllWords(), forKey: .words)
    }
}

// MARK: - 示例用法

/// 演示 Trie 的基本用法
public func demonstrateTrieUsage() {
    print("=== Trie (前缀树) 工具演示 ===\n")
    
    // 1. 基本操作
    print("1. 基本操作")
    print("-----------")
    let trie = Trie()
    
    // 插入单词
    trie.insert("apple")
    trie.insert("app")
    trie.insert("application")
    trie.insert("apply")
    trie.insert("banana")
    trie.insert("band")
    trie.insert("bandage")
    
    print("插入单词: apple, app, application, apply, banana, band, bandage")
    print("单词总数: \(trie.wordCount)")
    print()
    
    // 搜索单词
    print("搜索 'apple': \(trie.search("apple"))")      // true
    print("搜索 'app': \(trie.search("app"))")          // true
    print("搜索 'appl': \(trie.search("appl"))")        // false
    print("搜索 'orange': \(trie.search("orange"))")    // false
    print()
    
    // 前缀搜索
    print("前缀 'app' 存在: \(trie.startsWith("app"))")   // true
    print("前缀 'ban' 存在: \(trie.startsWith("ban"))")   // true
    print("前缀 'ora' 存在: \(trie.startsWith("ora"))")   // false
    print()
    
    // 2. 自动补全
    print("2. 自动补全")
    print("-----------")
    let appSuggestions = trie.autocomplete("app")
    print("前缀 'app' 的补全建议: \(appSuggestions)")
    
    let banSuggestions = trie.autocomplete("ban", limit: 3)
    print("前缀 'ban' 的补全建议（限制3个）: \(banSuggestions)")
    
    let allWords = trie.getAllWords()
    print("所有单词: \(allWords)")
    print()
    
    // 3. 删除操作
    print("3. 删除操作")
    print("-----------")
    print("删除 'app': \(trie.delete("app"))")
    print("搜索 'app' 删除后: \(trie.search("app"))")    // false
    print("搜索 'apple' 删除后: \(trie.search("apple"))") // true (未受影响)
    print("单词总数: \(trie.wordCount)")
    print()
    
    // 4. 模糊搜索
    print("4. 模糊搜索")
    print("-----------")
    let fuzzyResults = trie.fuzzySearch("aple", maxDistance: 1)
    print("模糊搜索 'aple' (距离1): \(fuzzyResults)")
    
    let fuzzyResults2 = trie.fuzzySearch("banaa", maxDistance: 2)
    print("模糊搜索 'banaa' (距离2): \(fuzzyResults2)")
    print()
    
    // 5. 高级功能
    print("5. 高级功能")
    print("-----------")
    print("最长公共前缀: '\(trie.longestCommonPrefix())'")
    print("节点数量: \(trie.nodeCount())")
    print("指定长度为5的单词: \(trie.getWordsByLength(5))")
    print("包含 'lic' 的单词: \(trie.findWordsContaining("lic"))")
    print()
    
    // 6. 访问统计（多次搜索同一单词后）
    print("6. 访问统计")
    print("-----------")
    trie.search("apple")
    trie.search("apple")
    trie.search("banana")
    
    let hotWords = trie.getMostAccessed(count: 3)
    print("热门单词（按访问次数）: \(hotWords)")
    print()
    
    // 7. 序列化
    print("7. 序列化")
    print("-----------")
    do {
        let encoder = JSONEncoder()
        encoder.outputFormatting = .prettyPrinted
        let jsonData = try encoder.encode(trie)
        if let jsonString = String(data: jsonData, encoding: .utf8) {
            print("JSON 序列化（前100字符）:")
            print(String(jsonString.prefix(100)) + "...")
        }
        
        let decoder = JSONDecoder()
        let decodedTrie = try decoder.decode(Trie.self, from: jsonData)
        print("反序列化后单词数: \(decodedTrie.wordCount)")
    } catch {
        print("序列化错误: \(error)")
    }
    print()
    
    // 8. 遍历
    print("8. 遍历（Sequence 协议）")
    print("-----------")
    print("遍历前5个单词:")
    for (index, word) in trie.enumerated().prefix(5) {
        print("  \(index + 1). \(word)")
    }
    print()
    
    print("=== 演示完成 ===")
}

// MARK: - TrieBuilder 辅助类

/// Trie 构建器，用于链式构建 Trie
public class TrieBuilder {
    private var trie: Trie
    
    public init() {
        self.trie = Trie()
    }
    
    /// 添加单个单词
    @discardableResult
    public func add(_ word: String) -> TrieBuilder {
        trie.insert(word)
        return self
    }
    
    /// 批量添加单词
    @discardableResult
    public func addAll(_ words: String...) -> TrieBuilder {
        for word in words {
            trie.insert(word)
        }
        return self
    }
    
    /// 从文件加载单词（每行一个）
    @discardableResult
    public func loadFromFile(_ path: String) -> TrieBuilder {
        guard let content = try? String(contentsOfFile: path, encoding: .utf8) else {
            return self
        }
        let words = content.components(separatedBy: .newlines)
            .map { $0.trimmingCharacters(in: .whitespaces) }
            .filter { !$0.isEmpty }
        trie.insertAll(words)
        return self
    }
    
    /// 构建最终 Trie
    public func build() -> Trie {
        return trie
    }
}

// MARK: - 示例：使用构建器

/// 演示 TrieBuilder 用法
public func demonstrateTrieBuilder() {
    print("=== TrieBuilder 演示 ===\n")
    
    let trie = TrieBuilder()
        .add("hello")
        .add("help")
        .add("helper")
        .add("helpful")
        .addAll("world", "word", "work", "worker")
        .build()
    
    print("Trie 信息: \(trie)")
    print("'help' 前缀补全: \(trie.autocomplete("help"))")
    print("'wor' 前缀补全: \(trie.autocomplete("wor"))")
}

// 执行演示（取消注释以运行）
// demonstrateTrieUsage()
// demonstrateTrieBuilder()