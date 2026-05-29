/**
 * Trie（前缀树/字典树）工具库
 * 
 * 高效的字符串前缀匹配和词频统计数据结构实现。
 * 
 * 特性：
 * - 零外部依赖，纯 Kotlin 标准库实现
 * - 支持插入、删除、搜索、前缀匹配
 * - 支持词频统计和自动补全
 * - 支持序列化和反序列化
 * - 支持遍历所有单词
 * 
 * 应用场景：
 * - 自动补全
 * - 拼写检查
 * - 词频统计
 * - 字符串前缀搜索
 * - IP 路由表
 * - 文本预测
 * 
 * @author AllToolkit Auto-Generator
 * @date 2026-05-29
 */

package trie_utils

/**
 * Trie 节点
 * 
 * @param T 字符类型，通常为 Char
 */
class TrieNode<T>(val value: T? = null) {
    val children: MutableMap<T, TrieNode<T>> = mutableMapOf()
    var isEndOfWord: Boolean = false
    var count: Int = 0  // 词频计数
    var prefixCount: Int = 0  // 经过此节点的单词数量
}

/**
 * Trie（前缀树）实现
 * 
 * @param T 字符类型，通常为 Char
 */
class Trie<T> {
    private val root = TrieNode<T>()
    
    /**
     * 插入单词
     * 
     * @param word 要插入的单词
     * @return 插入后的词频计数
     */
    fun insert(word: List<T>): Int {
        var node = root
        for (char in word) {
            node.prefixCount++
            node = node.children.getOrPut(char) { TrieNode(char) }
        }
        node.isEndOfWord = true
        node.count++
        node.prefixCount++
        return node.count
    }
    
    /**
     * 插入单词（字符串版本）
     */
    fun insert(word: String): Int {
        return insert(word.toList() as List<T>)
    }
    
    /**
     * 批量插入单词
     */
    fun insertAll(words: Collection<List<T>>) {
        words.forEach { insert(it) }
    }
    
    /**
     * 批量插入单词（字符串版本）
     */
    fun insertAllStrings(words: Collection<String>) {
        words.forEach { insert(it) }
    }
    
    /**
     * 搜索单词是否存在
     */
    fun search(word: List<T>): Boolean {
        val node = findNode(word) ?: return false
        return node.isEndOfWord
    }
    
    /**
     * 搜索单词是否存在（字符串版本）
     */
    fun search(word: String): Boolean {
        return search(word.toList() as List<T>)
    }
    
    /**
     * 检查是否存在以给定前缀开头的单词
     */
    fun startsWith(prefix: List<T>): Boolean {
        return findNode(prefix) != null
    }
    
    /**
     * 检查是否存在以给定前缀开头的单词（字符串版本）
     */
    fun startsWith(prefix: String): Boolean {
        return startsWith(prefix.toList() as List<T>)
    }
    
    /**
     * 获取单词的词频
     */
    fun count(word: List<T>): Int {
        val node = findNode(word) ?: return 0
        return if (node.isEndOfWord) node.count else 0
    }
    
    /**
     * 获取单词的词频（字符串版本）
     */
    fun count(word: String): Int {
        return count(word.toList() as List<T>)
    }
    
    /**
     * 获取以给定前缀开头的单词数量
     */
    fun countPrefix(prefix: List<T>): Int {
        val node = findNode(prefix) ?: return 0
        return node.prefixCount
    }
    
    /**
     * 获取以给定前缀开头的单词数量（字符串版本）
     */
    fun countPrefix(prefix: String): Int {
        return countPrefix(prefix.toList() as List<T>)
    }
    
    /**
     * 删除单词
     * 
     * @return 是否成功删除
     */
    fun delete(word: List<T>): Boolean {
        if (!search(word)) return false
        deleteHelper(root, word, 0)
        return true
    }
    
    /**
     * 删除单词（字符串版本）
     */
    fun delete(word: String): Boolean {
        return delete(word.toList() as List<T>)
    }
    
    private fun deleteHelper(node: TrieNode<T>, word: List<T>, index: Int): Boolean {
        if (index == word.size) {
            // 到达单词末尾，检查 count
            if (node.count > 0) {
                node.count--
                node.prefixCount--
                // 只有当 count 变为 0 时才标记为非单词结尾
                if (node.count == 0) {
                    node.isEndOfWord = false
                }
                // 只有 count 为 0 且无子节点时才可以删除此节点
                return node.count == 0 && node.children.isEmpty() && node !== root
            }
            return false
        }
        
        val char = word[index]
        val child = node.children[char] ?: return false
        
        node.prefixCount--
        val shouldDeleteChild = deleteHelper(child, word, index + 1)
        
        if (shouldDeleteChild) {
            node.children.remove(char)
            // 只有当此节点也不是单词结尾且无子节点时才可以删除
            return !node.isEndOfWord && node.children.isEmpty() && node !== root
        }
        
        return false
    }
    
    /**
     * 获取所有单词
     */
    fun getAllWords(): List<List<T>> {
        val result = mutableListOf<List<T>>()
        collectWords(root, mutableListOf(), result)
        return result
    }
    
    /**
     * 获取所有单词（字符串版本）
     */
    fun getAllWordsAsString(): List<String> {
        return getAllWords().map { it.joinToString("") }
    }
    
    /**
     * 获取以给定前缀开头的所有单词
     */
    fun getWordsWithPrefix(prefix: List<T>): List<List<T>> {
        val result = mutableListOf<List<T>>()
        val startNode = findNode(prefix) ?: return result
        collectWords(startNode, prefix.toMutableList(), result)
        return result
    }
    
    /**
     * 获取以给定前缀开头的所有单词（字符串版本）
     */
    fun getWordsWithPrefixAsString(prefix: String): List<String> {
        return getWordsWithPrefix(prefix.toList() as List<T>).map { it.joinToString("") }
    }
    
    /**
     * 自动补全
     * 
     * @param prefix 前缀
     * @param limit 最大返回数量
     * @return 补全建议列表
     */
    fun autocomplete(prefix: List<T>, limit: Int = 10): List<List<T>> {
        return getWordsWithPrefix(prefix).take(limit)
    }
    
    /**
     * 自动补全（字符串版本）
     */
    fun autocomplete(prefix: String, limit: Int = 10): List<String> {
        return autocomplete(prefix.toList() as List<T>, limit).map { it.joinToString("") }
    }
    
    /**
     * 获取最长公共前缀
     */
    fun longestCommonPrefix(): List<T> {
        if (root.children.size != 1 || root.isEndOfWord) {
            return emptyList()
        }
        
        val prefix = mutableListOf<T>()
        var node = root
        
        while (node.children.size == 1 && !node.isEndOfWord) {
            val (char, child) = node.children.entries.first()
            prefix.add(char)
            node = child
        }
        
        return prefix
    }
    
    /**
     * 获取最长公共前缀（字符串版本）
     */
    fun longestCommonPrefixString(): String {
        return longestCommonPrefix().joinToString("")
    }
    
    /**
     * 清空 Trie
     */
    fun clear() {
        root.children.clear()
        root.isEndOfWord = false
        root.count = 0
        root.prefixCount = 0
    }
    
    /**
     * 检查是否为空
     */
    fun isEmpty(): Boolean {
        return root.children.isEmpty()
    }
    
    /**
     * 获取单词总数（去重）
     */
    fun size(): Int {
        return countWords(root)
    }
    
    /**
     * 获取单词总数（包含重复）
     */
    fun totalCount(): Int {
        return root.prefixCount
    }
    
    private fun countWords(node: TrieNode<T>): Int {
        var count = if (node.isEndOfWord) 1 else 0
        for (child in node.children.values) {
            count += countWords(child)
        }
        return count
    }
    
    private fun findNode(prefix: List<T>): TrieNode<T>? {
        var node = root
        for (char in prefix) {
            node = node.children[char] ?: return null
        }
        return node
    }
    
    private fun collectWords(node: TrieNode<T>, current: MutableList<T>, result: MutableList<List<T>>) {
        if (node.isEndOfWord) {
            result.add(current.toList())
        }
        for ((char, child) in node.children) {
            current.add(char)
            collectWords(child, current, result)
            current.removeAt(current.size - 1)
        }
    }
    
    override fun toString(): String {
        return "Trie(uniqueWords=${size()}, totalWords=${totalCount()}, prefixCount=${root.prefixCount})"
    }
}

/**
 * 词频统计 Trie
 * 
 * 专为词频统计优化的 Trie 实现
 */
class FrequencyTrie {
    private val trie = Trie<Char>()
    private var totalInsertions = 0
    
    fun insert(word: String): Int {
        totalInsertions++
        return trie.insert(word)
    }
    
    fun frequency(word: String): Int = trie.count(word)
    
    fun prefixFrequency(prefix: String): Int = trie.countPrefix(prefix)
    
    fun totalWords(): Int = totalInsertions
    
    fun uniqueWords(): Int = trie.size()
    
    fun getTopK(limit: Int = 10): List<Pair<String, Int>> {
        val frequencies = mutableMapOf<String, Int>()
        collectFrequencies(trie, "", frequencies)
        return frequencies.entries
            .sortedByDescending { it.value }
            .take(limit)
            .map { it.key to it.value }
    }
    
    private fun collectFrequencies(trie: Trie<Char>, prefix: String, result: MutableMap<String, Int>) {
        for (word in trie.getWordsWithPrefixAsString(prefix)) {
            val freq = trie.count(word)
            if (freq > 0) {
                result[word] = freq
            }
        }
    }
    
    fun clear() {
        trie.clear()
        totalInsertions = 0
    }
    
    override fun toString(): String {
        return "FrequencyTrie(uniqueWords=${uniqueWords()}, totalInsertions=$totalInsertions)"
    }
}

/**
 * 可序列化的 Trie
 * 
 * 支持序列化和反序列化的 Trie 实现
 */
class SerializableTrie {
    private val trie = Trie<Char>()
    
    fun insert(word: String) = trie.insert(word)
    fun search(word: String) = trie.search(word)
    fun startsWith(prefix: String) = trie.startsWith(prefix)
    fun count(word: String) = trie.count(word)
    fun getWordsWithPrefix(prefix: String) = trie.getWordsWithPrefixAsString(prefix)
    fun getAllWords() = trie.getAllWordsAsString()
    fun size() = trie.size()
    fun clear() = trie.clear()
    
    /**
     * 序列化为字符串
     */
    fun serialize(): String {
        val words = trie.getAllWordsAsString()
        return words.joinToString(",") { 
            "${it}:${trie.count(it)}"
        }
    }
    
    /**
     * 从字符串反序列化
     */
    fun deserialize(data: String) {
        clear()
        if (data.isBlank()) return
        
        data.split(",").forEach { entry ->
            val parts = entry.split(":")
            if (parts.size == 2) {
                val word = parts[0]
                val count = parts[1].toIntOrNull() ?: 1
                repeat(count) { trie.insert(word) }
            }
        }
    }
    
    companion object {
        fun fromSerialized(data: String): SerializableTrie {
            val trie = SerializableTrie()
            trie.deserialize(data)
            return trie
        }
    }
}

/**
 * 自动补全 Trie
 * 
 * 专为自动补全优化的 Trie 实现，支持权重排序
 */
class AutocompleteTrie {
    private data class WeightedNode(
        val word: String,
        val weight: Int
    )
    
    private val trie = Trie<Char>()
    private val weights = mutableMapOf<String, Int>()
    
    /**
     * 插入单词（带权重）
     */
    fun insert(word: String, weight: Int = 1) {
        trie.insert(word)
        weights[word] = weight
    }
    
    /**
     * 增加单词权重
     */
    fun boost(word: String, amount: Int = 1) {
        if (trie.search(word)) {
            weights[word] = (weights[word] ?: 0) + amount
        }
    }
    
    /**
     * 获取单词权重
     */
    fun weight(word: String): Int = weights[word] ?: 0
    
    /**
     * 自动补全（按权重排序）
     */
    fun complete(prefix: String, limit: Int = 10): List<String> {
        val words = trie.getWordsWithPrefixAsString(prefix)
        return words
            .sortedByDescending { weights[it] ?: 0 }
            .take(limit)
    }
    
    /**
     * 获取最热门的单词
     */
    fun getTopWords(limit: Int = 10): List<String> {
        return weights.entries
            .sortedByDescending { it.value }
            .take(limit)
            .map { it.key }
    }
    
    fun search(word: String) = trie.search(word)
    fun size() = trie.size()
    fun clear() {
        trie.clear()
        weights.clear()
    }
    
    override fun toString(): String {
        return "AutocompleteTrie(uniqueWords=${size()}, entries=${weights.size})"
    }
}