/**
 * Bloom Filter 使用示例
 * 
 * 展示布隆过滤器在各种场景下的实际应用
 * 
 * @author AllToolkit Auto-Generator
 * @date 2026-04-13
 */

package bloom_filter_utils

/**
 * 示例：URL去重爬虫
 * 演示布隆过滤器在爬虫URL去重中的应用
 */
class CrawlerUrlFilter {
    private val filter = ScalableBloomFilter<String>(initialCapacity = 100000, fpp = 0.001)
    
    /**
     * 检查URL是否需要爬取
     * @return true表示URL可能已爬取过，false表示一定没爬取过
     */
    fun shouldCrawl(url: String): Boolean {
        if (filter.mightContain(url)) {
            // URL可能已存在（可能有假阳性，但不影响爬虫）
            return false
        }
        filter.add(url)
        return true
    }
    
    fun getStats(): String {
        return "已过滤URL数: ${filter.size()}, 内存: ${filter.memoryUsage() / 1024} KB"
    }
}

/**
 * 示例：用户名检查器
 * 演示布隆过滤器在快速检查用户名是否已存在中的应用
 */
class UsernameChecker {
    private val filter = BloomFilter<String>(expectedInsertions = 1000000, fpp = 0.01)
    private val existingUsers = mutableSetOf<String>() // 实际存储（可选）
    
    /**
     * 添加用户名
     */
    fun addUsername(username: String) {
        filter.add(username)
        existingUsers.add(username)
    }
    
    /**
     * 快速检查用户名是否可能已存在
     * 如果返回false，用户名一定不存在
     * 如果返回true，需要进一步验证
     */
    fun mightExist(username: String): Boolean {
        return filter.mightContain(username)
    }
    
    /**
     * 精确检查用户名是否存在
     */
    fun definitelyExists(username: String): Boolean {
        return existingUsers.contains(username)
    }
    
    fun getStats(): String {
        return "过滤器大小: ${filter.size()}, 内存: ${filter.memoryUsage() / 1024} KB"
    }
}

/**
 * 示例：缓存穿透防护
 * 演示布隆过滤器在防止缓存穿透中的应用
 */
class CachePenetrationGuard<T> {
    private val filter = ScalableBloomFilter<T>(initialCapacity = 100000, fpp = 0.001)
    
    /**
     * 记录已缓存的键
     */
    fun recordKey(key: T) {
        filter.add(key)
    }
    
    /**
     * 检查键是否可能在缓存中
     * 如果返回false，键一定不在缓存中，可以直接返回或查询数据库
     * 如果返回true，键可能在缓存中，应该查询缓存
     */
    fun mightBeCached(key: T): Boolean {
        return filter.mightContain(key)
    }
    
    fun getStats(): String = filter.toString()
}

/**
 * 示例：垃圾邮件URL检测
 * 演示布隆过滤器在黑名单过滤中的应用
 */
class SpamUrlDetector {
    private val spamFilter = BloomFilter<String>(expectedInsertions = 500000, fpp = 0.0001)
    
    /**
     * 添加垃圾邮件URL
     */
    fun addSpamUrl(url: String) {
        spamFilter.add(url)
    }
    
    /**
     * 批量添加垃圾邮件URL
     */
    fun addSpamUrls(urls: Collection<String>) {
        spamFilter.addAll(urls)
    }
    
    /**
     * 检查URL是否可能是垃圾链接
     * @return true表示可能是垃圾链接（需要进一步验证）
     *         false表示一定不是垃圾链接
     */
    fun mightBeSpam(url: String): Boolean {
        return spamFilter.mightContain(url)
    }
    
    /**
     * 检查URL是否安全
     */
    fun isSafe(url: String): Boolean {
        return spamFilter.definitelyNotContains(url)
    }
    
    fun getStats(): String = spamFilter.toString()
}

/**
 * 示例：实时去重计数器
 * 演示布隆过滤器在UV统计中的应用
 */
class UniqueVisitorCounter {
    private val filter = CountingBloomFilter<String>(expectedInsertions = 100000, fpp = 0.01)
    private var totalVisits = 0L
    
    /**
     * 记录访问
     * @return 是否是新访客
     */
    fun recordVisit(userId: String): Boolean {
        totalVisits++
        if (filter.definitelyNotContains(userId)) {
            filter.add(userId)
            return true
        }
        return false
    }
    
    /**
     * 获取唯一访客估计数
     */
    fun getUniqueVisitorCount(): Int = filter.size()
    
    /**
     * 获取总访问数
     */
    fun getTotalVisits(): Long = totalVisits
    
    fun getStats(): String {
        return "UV: ${getUniqueVisitorCount()}, PV: $totalVisits"
    }
}

/**
 * 示例：词典拼写检查
 * 演示布隆过滤器在拼写检查中的应用
 */
class SpellChecker {
    private val dictionary = BloomFilter<String>(expectedInsertions = 200000, fpp = 0.001)
    
    /**
     * 加载词典
     */
    fun loadDictionary(words: Collection<String>) {
        words.forEach { dictionary.add(it.lowercase()) }
    }
    
    /**
     * 检查单词拼写
     * @return true表示单词可能在词典中（拼写可能正确）
     *         false表示单词一定不在词典中（拼写错误）
     */
    fun mightBeCorrect(word: String): Boolean {
        return dictionary.mightContain(word.lowercase())
    }
    
    /**
     * 检查单词是否一定错误
     */
    fun definitelyWrong(word: String): Boolean {
        return dictionary.definitelyNotContains(word.lowercase())
    }
    
    fun getStats(): String = dictionary.toString()
}

// ============================================
// 实际使用示例
// ============================================

fun main() {
    println("========================================")
    println("  Bloom Filter 实用示例")
    println("========================================\n")
    
    // 示例1：URL去重
    println("【示例1】爬虫URL去重:")
    println("-".repeat(40))
    val crawler = CrawlerUrlFilter()
    
    val urls = listOf(
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page1", // 重复
        "https://example.com/page2"  // 重复
    )
    
    urls.forEach { url ->
        val shouldCrawl = crawler.shouldCrawl(url)
        println("  $url -> ${if (shouldCrawl) "需要爬取" else "跳过(重复)"}")
    }
    println("  ${crawler.getStats()}\n")
    
    // 示例2：缓存穿透防护
    println("【示例2】缓存穿透防护:")
    println("-".repeat(40))
    val cacheGuard = CachePenetrationGuard<String>()
    
    // 模拟已缓存的键
    val cachedKeys = listOf("user:1", "user:2", "product:1")
    cachedKeys.forEach { cacheGuard.recordKey(it) }
    
    val testKeys = listOf("user:1", "user:3", "product:2", "order:1")
    testKeys.forEach { key ->
        val mightBeCached = cacheGuard.mightBeCached(key)
        println("  $key -> ${if (mightBeCached) "查询缓存" else "直接返回空(避免穿透)"}")
    }
    println("  ${cacheGuard.getStats()}\n")
    
    // 示例3：垃圾链接检测
    println("【示例3】垃圾链接检测:")
    println("-".repeat(40))
    val spamDetector = SpamUrlDetector()
    
    // 模拟已知的垃圾链接
    spamDetector.addSpamUrls(listOf(
        "http://spam-site1.com",
        "http://spam-site2.com",
        "http://malicious-link.net"
    ))
    
    val testUrls = listOf(
        "http://spam-site1.com",
        "http://google.com",
        "http://malicious-link.net",
        "http://github.com"
    )
    
    testUrls.forEach { url ->
        val isSpam = spamDetector.mightBeSpam(url)
        val isSafe = spamDetector.isSafe(url)
        println("  $url -> ${if (isSpam) "可疑(需验证)" else if (isSafe) "安全" else "未知"}")
    }
    println("  ${spamDetector.getStats()}\n")
    
    // 示例4：UV统计
    println("【示例4】UV/PV统计:")
    println("-".repeat(40))
    val visitorCounter = UniqueVisitorCounter()
    
    val visits = listOf("user1", "user2", "user1", "user3", "user2", "user1", "user4")
    visits.forEach { userId ->
        val isNew = visitorCounter.recordVisit(userId)
        println("  访客 $userId -> ${if (isNew) "新访客" else "老访客"}")
    }
    println("  ${visitorCounter.getStats()}\n")
    
    // 示例5：拼写检查
    println("【示例5】拼写检查:")
    println("-".repeat(40))
    val spellChecker = SpellChecker()
    
    // 模拟词典
    spellChecker.loadDictionary(listOf(
        "hello", "world", "kotlin", "bloom", "filter", "algorithm", "data", "structure"
    ))
    
    val testWords = listOf("hello", "wrld", "kotlin", "bloomm", "data", "struktur")
    testWords.forEach { word ->
        val correct = spellChecker.mightBeCorrect(word)
        val wrong = spellChecker.definitelyWrong(word)
        println("  \"$word\" -> ${if (wrong) "❌ 拼写错误" else if (correct) "✓ 可能正确" else "未知"}")
    }
    println("  ${spellChecker.getStats()}\n")
    
    // 示例6：序列化与持久化
    println("【示例6】序列化与持久化:")
    println("-".repeat(40))
    
    // 创建并填充过滤器
    val originalFilter = BloomFilter<String>(1000, 0.01)
    val testData = (1..100).map { "item_$it" }
    testData.forEach { originalFilter.add(it) }
    
    // 序列化
    val serialized = originalFilter.toByteArray()
    println("  序列化大小: ${serialized.size} bytes")
    
    // 反序列化
    val restoredFilter = BloomFilter.fromByteArray<String>(serialized)
    println("  恢复后大小: ${restoredFilter.size()}")
    
    // 验证
    var allCorrect = true
    testData.forEach { item ->
        if (!restoredFilter.mightContain(item)) {
            allCorrect = false
        }
    }
    println("  数据一致性: ${if (allCorrect) "✓ 正确" else "✗ 错误"}")
    
    println("\n========================================")
    println("  所有示例完成")
    println("========================================")
}