/**
 * Trie 工具库使用示例
 * 
 * 展示 Trie、FrequencyTrie、SerializableTrie、AutocompleteTrie 的典型用法
 * 
 * @author AllToolkit Auto-Generator
 * @date 2026-05-29
 */

package trie_utils

fun main() {
    println("========================================")
    println("   Trie（前缀树/字典树）工具库示例")
    println("========================================\n")
    
    // ========== 基础 Trie 示例 ==========
    println("【1. 基础 Trie 操作】")
    println("-".repeat(40))
    
    val trie = Trie<Char>()
    
    // 插入单词
    trie.insert("apple")
    trie.insert("application")
    trie.insert("apply")
    trie.insert("app")
    trie.insert("banana")
    trie.insert("band")
    trie.insert("bandana")
    
    println("插入单词: apple, application, apply, app, banana, band, bandana")
    println()
    
    // 搜索单词
    println("搜索测试:")
    println("  search(\"apple\") → ${trie.search("apple")}")
    println("  search(\"app\") → ${trie.search("app")}")
    println("  search(\"appl\") → ${trie.search("appl")} (不是完整单词)")
    println("  search(\"orange\") → ${trie.search("orange")}")
    println()
    
    // 前缀搜索
    println("前缀搜索:")
    println("  startsWith(\"app\") → ${trie.startsWith("app")}")
    println("  startsWith(\"ban\") → ${trie.startsWith("ban")}")
    println("  startsWith(\"xyz\") → ${trie.startsWith("xyz")}")
    println()
    
    // 前缀单词数量
    println("前缀单词数量:")
    println("  countPrefix(\"app\") → ${trie.countPrefix("app")}")
    println("  countPrefix(\"ban\") → ${trie.countPrefix("ban")}")
    println("  countPrefix(\"band\") → ${trie.countPrefix("band")}")
    println()
    
    // 自动补全
    println("自动补全:")
    println("  autocomplete(\"app\") → ${trie.autocomplete("app")}")
    println("  autocomplete(\"ban\") → ${trie.autocomplete("ban")}")
    println()
    
    // 获取所有以某前缀开头的单词
    println("获取所有 app 开头的单词:")
    val appWords = trie.getWordsWithPrefixAsString("app")
    println("  $appWords")
    println()
    
    // 最长公共前缀
    println("最长公共前缀: \"${trie.longestCommonPrefixString()}\"")
    println()
    
    // ========== 词频统计示例 ==========
    println("\n【2. 词频统计 Trie】")
    println("-".repeat(40))
    
    val freqTrie = FrequencyTrie()
    
    // 插入单词（带重复）
    freqTrie.insert("hello")
    freqTrie.insert("world")
    freqTrie.insert("hello")
    freqTrie.insert("kotlin")
    freqTrie.insert("hello")
    freqTrie.insert("world")
    freqTrie.insert("trie")
    freqTrie.insert("trie")
    freqTrie.insert("trie")
    
    println("词频统计:")
    println("  \"hello\" 频率: ${freqTrie.frequency("hello")}")
    println("  \"world\" 频率: ${freqTrie.frequency("world")}")
    println("  \"trie\" 频率: ${freqTrie.frequency("trie")}")
    println("  \"kotlin\" 频率: ${freqTrie.frequency("kotlin")}")
    println()
    
    println("统计信息:")
    println("  唯一单词数: ${freqTrie.uniqueWords()}")
    println("  总插入次数: ${freqTrie.totalWords()}")
    println()
    
    println("Top 3 高频词:")
    val topWords = freqTrie.getTopK(3)
    topWords.forEach { (word, freq) ->
        println("  \"$word\": $freq 次")
    }
    println()
    
    // ========== 可序列化 Trie 示例 ==========
    println("\n【3. 可序列化 Trie】")
    println("-".repeat(40))
    
    val serialTrie = SerializableTrie()
    serialTrie.insert("cache")
    serialTrie.insert("cache")
    serialTrie.insert("data")
    serialTrie.insert("database")
    serialTrie.insert("date")
    
    println("原始数据:")
    println("  单词: cache(2), data(1), database(1), date(1)")
    println()
    
    // 序列化
    val serialized = serialTrie.serialize()
    println("序列化结果:")
    println("  $serialized")
    println()
    
    // 反序列化
    val restoredTrie = SerializableTrie.fromSerialized(serialized)
    println("反序列化验证:")
    println("  search(\"cache\") → ${restoredTrie.search("cache")}")
    println("  count(\"cache\") → ${restoredTrie.count("cache")}")
    println("  search(\"database\") → ${restoredTrie.search("database")}")
    println("  所有单词: ${restoredTrie.getAllWords()}")
    println()
    
    // ========== 自动补全 Trie 示例 ==========
    println("\n【4. 自动补全 Trie（带权重排序）】")
    println("-".repeat(40))
    
    val autoTrie = AutocompleteTrie()
    
    // 插入单词（带权重/热度）
    autoTrie.insert("javascript", 100)
    autoTrie.insert("java", 80)
    autoTrie.insert("javafx", 20)
    autoTrie.insert("javascript教程", 50)
    autoTrie.insert("python", 90)
    autoTrie.insert("pytorch", 60)
    autoTrie.insert("python教程", 40)
    
    println("插入单词（带权重）:")
    println("  javascript: 100")
    println("  java: 80")
    println("  javafx: 20")
    println("  javascript教程: 50")
    println("  python: 90")
    println("  pytorch: 60")
    println("  python教程: 40")
    println()
    
    // 自动补全（按权重排序）
    println("自动补全 \"jav\":")
    val javCompletions = autoTrie.complete("jav")
    javCompletions.forEachIndexed { i, word ->
        println("  ${i + 1}. $word (权重: ${autoTrie.weight(word)})")
    }
    println()
    
    println("自动补全 \"py\":")
    val pyCompletions = autoTrie.complete("py")
    pyCompletions.forEachIndexed { i, word ->
        println("  ${i + 1}. $word (权重: ${autoTrie.weight(word)})")
    }
    println()
    
    // 模拟用户选择后提升权重
    println("模拟用户选择 \"javafx\" 后提升权重:")
    autoTrie.boost("javafx", 70)
    println("  javafx 新权重: ${autoTrie.weight("javafx")}")
    println()
    
    println("再次自动补全 \"jav\":")
    autoTrie.complete("jav").forEachIndexed { i, word ->
        println("  ${i + 1}. $word (权重: ${autoTrie.weight(word)})")
    }
    println()
    
    // 最热门单词
    println("最热门的 3 个单词:")
    autoTrie.getTopWords(3).forEachIndexed { i, word ->
        println("  ${i + 1}. $word (权重: ${autoTrie.weight(word)})")
    }
    println()
    
    // ========== 删除操作示例 ==========
    println("\n【5. 删除操作】")
    println("-".repeat(40))
    
    val deleteTrie = Trie<Char>()
    deleteTrie.insert("car")
    deleteTrie.insert("card")
    deleteTrie.insert("care")
    deleteTrie.insert("careful")
    
    println("初始单词: car, card, care, careful")
    println("前缀 \"car\" 单词数: ${deleteTrie.countPrefix("car")}")
    println()
    
    println("删除 \"car\":")
    val deleted = deleteTrie.delete("car")
    println("  删除结果: $deleted")
    println("  search(\"car\"): ${deleteTrie.search("car")}")
    println("  search(\"card\"): ${deleteTrie.search("card")}")
    println("  search(\"care\"): ${deleteTrie.search("care")}")
    println("  前缀 \"car\" 单词数: ${deleteTrie.countPrefix("car")}")
    println()
    
    println("删除 \"careful\":")
    deleteTrie.delete("careful")
    println("  前缀 \"care\" 单词数: ${deleteTrie.countPrefix("care")}")
    println()
    
    // ========== 实际应用场景示例 ==========
    println("\n【6. 实际应用场景】")
    println("-".repeat(40))
    
    // 拼写检查
    println("场景 1: 拼写检查")
    val dictionary = Trie<Char>()
    val englishWords = listOf(
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she"
    )
    dictionary.insertAllStrings(englishWords)
    
    val testWords = listOf("the", "teh", "apple", "and", "annd")
    println("检查单词:")
    for (word in testWords) {
        val exists = dictionary.search(word)
        println("  \"$word\" → ${if (exists) "✓ 存在" else "✗ 不存在（可能拼写错误）"}")
    }
    println()
    
    // IP 地址前缀匹配
    println("场景 2: IP 路由前缀匹配")
    val ipTrie = Trie<Char>()
    ipTrie.insertAllStrings(listOf(
        "192.168.1.0/24",
        "192.168.1.0/25",
        "192.168.2.0/24",
        "10.0.0.0/8"
    ))
    
    val ip = "192.168.1.100"
    println("IP: $ip")
    println("匹配的路由前缀:")
    val matchingRoutes = ipTrie.getAllWordsAsString().filter { ip.startsWith(it.removeSuffix("/24").removeSuffix("/25").removeSuffix("/8")) }
    matchingRoutes.forEach { println("  $it") }
    println()
    
    // 搜索建议
    println("场景 3: 搜索建议")
    val searchTrie = AutocompleteTrie()
    searchTrie.insert("如何学习kotlin", 100)
    searchTrie.insert("如何学习python", 90)
    searchTrie.insert("kotlin教程", 80)
    searchTrie.insert("kotlin协程", 70)
    searchTrie.insert("python爬虫", 60)
    
    println("用户输入: \"如何\"")
    println("搜索建议:")
    searchTrie.complete("如何").forEach { println("  - $it") }
    println()
    
    println("用户输入: \"kotlin\"")
    println("搜索建议:")
    searchTrie.complete("kotlin").forEach { println("  - $it") }
    println()
    
    println("\n========================================")
    println("           示例运行完成!")
    println("========================================")
}