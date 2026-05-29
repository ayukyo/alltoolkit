/**
 * Trie 工具库测试套件
 * 
 * 全面测试 Trie、FrequencyTrie、SerializableTrie、AutocompleteTrie 功能
 * 零外部依赖，纯 Kotlin 标准库实现
 * 
 * @author AllToolkit Auto-Generator
 * @date 2026-05-29
 */

package trie_utils

// 自定义断言函数（零外部依赖）
fun assertTrue(condition: Boolean, message: String = "") {
    if (!condition) {
        throw AssertionError("Assertion failed: $message (expected true, got false)")
    }
}

fun assertFalse(condition: Boolean, message: String = "") {
    if (condition) {
        throw AssertionError("Assertion failed: $message (expected false, got true)")
    }
}

fun assertEquals(expected: Any?, actual: Any?, message: String = "") {
    if (expected != actual) {
        throw AssertionError("Assertion failed: $message (expected $expected, got $actual)")
    }
}

class TrieTest {
    private lateinit var trie: Trie<Char>
    
    fun setup() {
        trie = Trie()
    }
    
    // ========== 基础插入和搜索测试 ==========
    
    fun testInsertAndSearch() {
        trie.insert("hello")
        assertTrue(trie.search("hello"), "search hello")
        assertFalse(trie.search("hell"), "search hell")
        assertFalse(trie.search("helloo"), "search helloo")
    }
    
    fun testInsertMultipleWords() {
        trie.insert("cat")
        trie.insert("car")
        trie.insert("card")
        trie.insert("care")
        trie.insert("careful")
        
        assertTrue(trie.search("cat"), "search cat")
        assertTrue(trie.search("car"), "search car")
        assertTrue(trie.search("card"), "search card")
        assertTrue(trie.search("care"), "search care")
        assertTrue(trie.search("careful"), "search careful")
        assertFalse(trie.search("cards"), "search cards")
        assertFalse(trie.search("ca"), "search ca")
    }
    
    fun testInsertDuplicate() {
        assertEquals(1, trie.insert("word"), "insert word first")
        assertEquals(2, trie.insert("word"), "insert word second")
        assertEquals(3, trie.insert("word"), "insert word third")
        assertEquals(3, trie.count("word"), "count word")
    }
    
    fun testInsertAll() {
        val words = listOf("apple", "application", "apply", "app")
        trie.insertAllStrings(words)
        
        for (word in words) {
            assertTrue(trie.search(word), "Expected to find '$word'")
        }
    }
    
    fun testEmptyString() {
        trie.insert("")
    }
    
    // ========== 前缀搜索测试 ==========
    
    fun testStartsWith() {
        trie.insert("hello")
        trie.insert("world")
        trie.insert("help")
        
        assertTrue(trie.startsWith("hel"), "startsWith hel")
        assertTrue(trie.startsWith("wor"), "startsWith wor")
        assertTrue(trie.startsWith("h"), "startsWith h")
        assertFalse(trie.startsWith("xyz"), "startsWith xyz")
        assertTrue(trie.startsWith(""), "startsWith empty")  // 空前缀匹配所有
    }
    
    fun testPrefixCount() {
        trie.insert("cat")
        trie.insert("car")
        trie.insert("card")
        trie.insert("care")
        
        assertEquals(4, trie.countPrefix("ca"), "countPrefix ca")
        assertEquals(3, trie.countPrefix("car"), "countPrefix car")  // car, card, care
        assertEquals(1, trie.countPrefix("care"), "countPrefix care")
        assertEquals(0, trie.countPrefix("xyz"), "countPrefix xyz")
    }
    
    // ========== 删除测试 ==========
    
    fun testDelete() {
        trie.insert("hello")
        assertTrue(trie.search("hello"), "search hello before delete")
        
        assertTrue(trie.delete("hello"), "delete hello")
        assertFalse(trie.search("hello"), "search hello after delete")
    }
    
    fun testDeleteNonExistent() {
        trie.insert("hello")
        assertFalse(trie.delete("world"), "delete non-existent world")
        assertTrue(trie.search("hello"), "search hello after failed delete")
    }
    
    fun testDeleteWithSharedPrefix() {
        trie.insert("car")
        trie.insert("card")
        trie.insert("care")
        
        assertTrue(trie.delete("car"), "delete car")
        assertFalse(trie.search("car"), "search car after delete")
        assertTrue(trie.search("card"), "search card")
        assertTrue(trie.search("care"), "search care")
    }
    
    fun testDeleteReducesPrefixCount() {
        trie.insert("hello")
        trie.insert("help")
        
        val beforeCount = trie.countPrefix("hel")
        assertTrue(trie.delete("help"), "delete help")
        val afterCount = trie.countPrefix("hel")
        
        assertEquals(2, beforeCount, "before count")
        assertEquals(1, afterCount, "after count")
    }
    
    fun testDeleteDuplicate() {
        trie.insert("word")
        trie.insert("word")
        trie.insert("word")
        
        assertEquals(3, trie.count("word"), "count before delete")
        assertTrue(trie.delete("word"), "delete word")
        assertEquals(2, trie.count("word"), "count after delete")
    }
    
    // ========== 词频统计测试 ==========
    
    fun testCount() {
        trie.insert("test")
        trie.insert("test")
        trie.insert("test")
        
        assertEquals(3, trie.count("test"), "count test")
        assertEquals(0, trie.count("testing"), "count testing")
    }
    
    // ========== 获取所有单词测试 ==========
    
    fun testGetAllWords() {
        trie.insertAllStrings(listOf("cat", "car", "card"))
        val words = trie.getAllWordsAsString()
        
        assertEquals(3, words.size, "words size")
        assertTrue(words.contains("cat"), "contains cat")
        assertTrue(words.contains("car"), "contains car")
        assertTrue(words.contains("card"), "contains card")
    }
    
    fun testGetAllWordsEmpty() {
        val words = trie.getAllWordsAsString()
        assertTrue(words.isEmpty(), "empty trie")
    }
    
    // ========== 前缀单词查询测试 ==========
    
    fun testGetWordsWithPrefix() {
        trie.insertAllStrings(listOf("apple", "application", "apply", "banana", "band"))
        
        val applePrefix = trie.getWordsWithPrefixAsString("app")
        assertEquals(3, applePrefix.size, "apple prefix size")
        assertTrue(applePrefix.contains("apple"), "contains apple")
        assertTrue(applePrefix.contains("application"), "contains application")
        assertTrue(applePrefix.contains("apply"), "contains apply")
        
        val bananaPrefix = trie.getWordsWithPrefixAsString("ban")
        assertEquals(2, bananaPrefix.size, "banana prefix size")
        
        val xyzPrefix = trie.getWordsWithPrefixAsString("xyz")
        assertTrue(xyzPrefix.isEmpty(), "xyz prefix empty")
    }
    
    // ========== 自动补全测试 ==========
    
    fun testAutocomplete() {
        trie.insertAllStrings(listOf("cat", "car", "card", "care", "careful"))
        
        val completions = trie.autocomplete("ca", limit = 3)
        assertEquals(3, completions.size, "completions size")
        assertTrue(completions.all { it.startsWith("ca") }, "all start with ca")
    }
    
    fun testAutocompleteLimit() {
        for (i in 1..20) {
            trie.insert("test$i")
        }
        
        val completions = trie.autocomplete("test", limit = 5)
        assertEquals(5, completions.size, "limit 5")
    }
    
    // ========== 最长公共前缀测试 ==========
    
    fun testLongestCommonPrefix() {
        trie.insertAllStrings(listOf("flower", "flow", "flight"))
        assertEquals("fl", trie.longestCommonPrefixString(), "lcp")
    }
    
    fun testLongestCommonPrefixSingleWord() {
        trie.insert("hello")
        assertEquals("hello", trie.longestCommonPrefixString(), "lcp single")
    }
    
    fun testLongestCommonPrefixEmpty() {
        trie.insertAllStrings(listOf("cat", "dog", "bird"))
        assertEquals("", trie.longestCommonPrefixString(), "lcp empty")
    }
    
    // ========== 清空和大小测试 ==========
    
    fun testClear() {
        trie.insertAllStrings(listOf("a", "b", "c"))
        assertEquals(3, trie.size(), "size before clear")
        
        trie.clear()
        assertEquals(0, trie.size(), "size after clear")
        assertTrue(trie.isEmpty(), "isEmpty after clear")
    }
    
    fun testSize() {
        assertEquals(0, trie.size(), "size 0")
        
        trie.insert("a")
        assertEquals(1, trie.size(), "size 1")
        
        trie.insert("b")
        assertEquals(2, trie.size(), "size 2")
        
        trie.insert("a")  // 重复插入
        assertEquals(2, trie.size(), "size still 2")  // 去重计数
    }
    
    fun testTotalCount() {
        trie.insert("word")
        trie.insert("word")
        trie.insert("word")
        trie.insert("other")
        
        assertEquals(2, trie.size(), "unique words")
        assertEquals(4, trie.totalCount(), "total count")
    }
    
    fun testIsEmpty() {
        assertTrue(trie.isEmpty(), "isEmpty initial")
        trie.insert("hello")
        assertFalse(trie.isEmpty(), "isEmpty after insert")
    }
    
    // ========== toString 测试 ==========
    
    fun testToString() {
        trie.insertAllStrings(listOf("a", "b", "c"))
        val str = trie.toString()
        assertTrue(str.contains("Trie"), "contains Trie")
        assertTrue(str.contains("uniqueWords=3"), "contains uniqueWords=3")
    }
}

class FrequencyTrieTest {
    private lateinit var freqTrie: FrequencyTrie
    
    fun setup() {
        freqTrie = FrequencyTrie()
    }
    
    fun testBasicFrequency() {
        freqTrie.insert("hello")
        freqTrie.insert("hello")
        freqTrie.insert("hello")
        
        assertEquals(3, freqTrie.frequency("hello"), "hello freq")
        assertEquals(0, freqTrie.frequency("world"), "world freq")
    }
    
    fun testTotalAndUnique() {
        freqTrie.insert("apple")
        freqTrie.insert("apple")
        freqTrie.insert("banana")
        
        assertEquals(2, freqTrie.uniqueWords(), "unique words")
        assertEquals(3, freqTrie.totalWords(), "total words")
    }
    
    fun testPrefixFrequency() {
        freqTrie.insert("cat")
        freqTrie.insert("car")
        freqTrie.insert("card")
        
        assertEquals(3, freqTrie.prefixFrequency("ca"), "prefix ca")
        assertEquals(2, freqTrie.prefixFrequency("car"), "prefix car")
    }
    
    fun testGetTopK() {
        freqTrie.clear()
        repeat(5) { freqTrie.insert("apple") }
        repeat(3) { freqTrie.insert("banana") }
        repeat(1) { freqTrie.insert("cherry") }
        
        val topK = freqTrie.getTopK(2)
        assertEquals(2, topK.size, "topK size")
        assertEquals("apple", topK[0].first, "top1 word")
        assertEquals(5, topK[0].second, "top1 freq")
        assertEquals("banana", topK[1].first, "top2 word")
        assertEquals(3, topK[1].second, "top2 freq")
    }
    
    fun testClear() {
        freqTrie.insert("test")
        freqTrie.clear()
        
        assertEquals(0, freqTrie.uniqueWords(), "unique after clear")
        assertEquals(0, freqTrie.totalWords(), "total after clear")
    }
}

class SerializableTrieTest {
    private lateinit var trie: SerializableTrie
    
    fun setup() {
        trie = SerializableTrie()
    }
    
    fun testBasicOperations() {
        trie.insert("hello")
        trie.insert("world")
        
        assertTrue(trie.search("hello"), "search hello")
        assertTrue(trie.search("world"), "search world")
        assertFalse(trie.search("hell"), "search hell")
    }
    
    fun testSerializeDeserialize() {
        trie.insert("apple")
        trie.insert("apple")
        trie.insert("banana")
        
        val serialized = trie.serialize()
        
        val newTrie = SerializableTrie.fromSerialized(serialized)
        
        assertTrue(newTrie.search("apple"), "search apple restored")
        assertTrue(newTrie.search("banana"), "search banana restored")
        assertEquals(2, newTrie.count("apple"), "count apple restored")
    }
    
    fun testSerializeEmpty() {
        val serialized = trie.serialize()
        assertTrue(serialized.isEmpty(), "empty serialize")
        
        val newTrie = SerializableTrie.fromSerialized(serialized)
        assertEquals(0, newTrie.size(), "size restored empty")
    }
    
    fun testSerializeMultipleWords() {
        trie.insert("cat")
        trie.insert("dog")
        trie.insert("bird")
        
        val serialized = trie.serialize()
        val newTrie = SerializableTrie.fromSerialized(serialized)
        
        val words = newTrie.getAllWords()
        assertEquals(3, words.size, "words size")
        assertTrue(words.contains("cat"), "contains cat")
        assertTrue(words.contains("dog"), "contains dog")
        assertTrue(words.contains("bird"), "contains bird")
    }
}

class AutocompleteTrieTest {
    private lateinit var trie: AutocompleteTrie
    
    fun setup() {
        trie = AutocompleteTrie()
    }
    
    fun testInsertWithWeight() {
        trie.insert("apple", 10)
        trie.insert("application", 5)
        trie.insert("apply", 3)
        
        assertEquals(10, trie.weight("apple"), "apple weight")
        assertEquals(5, trie.weight("application"), "application weight")
        assertEquals(3, trie.weight("apply"), "apply weight")
    }
    
    fun testAutoCompleteByWeight() {
        trie.insert("cat", 5)
        trie.insert("car", 10)
        trie.insert("card", 3)
        trie.insert("care", 8)
        
        val completions = trie.complete("ca")
        
        assertEquals("car", completions[0], "top1 car")  // weight 10
        assertEquals("care", completions[1], "top2 care")  // weight 8
        assertEquals("cat", completions[2], "top3 cat")  // weight 5
        assertEquals("card", completions[3], "top4 card")  // weight 3
    }
    
    fun testBoost() {
        trie.insert("apple", 5)
        trie.insert("application", 3)
        
        trie.boost("apple", 10)
        
        assertEquals(15, trie.weight("apple"), "boosted weight")
    }
    
    fun testGetTopWords() {
        trie.insert("popular", 100)
        trie.insert("common", 50)
        trie.insert("rare", 10)
        trie.insert("unique", 1)
        
        val top = trie.getTopWords(2)
        assertEquals(2, top.size, "top size")
        assertEquals("popular", top[0], "top1")
        assertEquals("common", top[1], "top2")
    }
    
    fun testSearch() {
        trie.insert("hello")
        assertTrue(trie.search("hello"), "search hello")
        assertFalse(trie.search("hell"), "search hell")
    }
    
    fun testClear() {
        trie.insert("test", 5)
        trie.clear()
        
        assertEquals(0, trie.size(), "size after clear")
        assertEquals(0, trie.weight("test"), "weight after clear")
    }
    
    fun testCompleteWithLimit() {
        for (i in 1..20) {
            trie.insert("word$i", i)
        }
        
        val completions = trie.complete("word", limit = 5)
        assertEquals(5, completions.size, "limit 5")
    }
}

class TrieEdgeCasesTest {
    private lateinit var trie: Trie<Char>
    
    fun setup() {
        trie = Trie()
    }
    
    fun testSingleCharacterWords() {
        trie.insertAllStrings(listOf("a", "b", "c"))
        
        assertTrue(trie.search("a"), "search a")
        assertTrue(trie.search("b"), "search b")
        assertTrue(trie.search("c"), "search c")
        assertEquals(3, trie.size(), "size 3")
    }
    
    fun testLongWord() {
        val longWord = "a".repeat(1000)
        trie.insert(longWord)
        
        assertTrue(trie.search(longWord), "search long")
        assertEquals(1, trie.size(), "size 1")
    }
    
    fun testUnicodeCharacters() {
        trie.insert("你好")
        trie.insert("世界")
        trie.insert("你好世界")
        
        assertTrue(trie.search("你好"), "search 你好")
        assertTrue(trie.search("世界"), "search 世界")
        assertTrue(trie.search("你好世界"), "search 你好世界")
        assertFalse(trie.search("你"), "search 你")
    }
    
    fun testMixedCaseWords() {
        trie.insert("Hello")
        trie.insert("hello")
        trie.insert("HELLO")
        
        assertTrue(trie.search("Hello"), "search Hello")
        assertTrue(trie.search("hello"), "search hello")
        assertTrue(trie.search("HELLO"), "search HELLO")
        assertEquals(3, trie.size(), "size 3 case sensitive")
    }
    
    fun testNumericStrings() {
        trie.insert("123")
        trie.insert("12345")
        trie.insert("123abc")
        
        assertTrue(trie.search("123"), "search 123")
        assertTrue(trie.startsWith("123"), "startsWith 123")
        assertEquals(3, trie.countPrefix("123"), "countPrefix 123")
    }
    
    fun testSpecialCharacters() {
        trie.insert("hello-world")
        trie.insert("hello_world")
        trie.insert("hello.world")
        
        assertTrue(trie.search("hello-world"), "search hello-world")
        assertTrue(trie.search("hello_world"), "search hello_world")
        assertTrue(trie.search("hello.world"), "search hello.world")
    }
    
    fun testDeleteAllWords() {
        trie.insertAllStrings(listOf("a", "ab", "abc"))
        
        assertTrue(trie.delete("abc"), "delete abc")
        assertTrue(trie.delete("ab"), "delete ab")
        assertTrue(trie.delete("a"), "delete a")
        
        assertTrue(trie.isEmpty(), "isEmpty after all deleted")
        assertEquals(0, trie.size(), "size 0 after all deleted")
    }
    
    fun testLargeDataset() {
        // 插入大量单词
        val words = (1..1000).map { "word$it" }
        trie.insertAllStrings(words)
        
        assertEquals(1000, trie.size(), "size 1000")
        assertTrue(trie.search("word500"), "search word500")
        assertTrue(trie.startsWith("word"), "startsWith word")
        assertEquals(1000, trie.countPrefix("word"), "countPrefix word")
    }
    
    fun testOverlappingWords() {
        trie.insert("a")
        trie.insert("ab")
        trie.insert("abc")
        trie.insert("abcd")
        
        assertTrue(trie.search("a"), "search a")
        assertTrue(trie.search("ab"), "search ab")
        assertTrue(trie.search("abc"), "search abc")
        assertTrue(trie.search("abcd"), "search abcd")
        assertFalse(trie.search("abcde"), "search abcde")
        
        assertEquals(4, trie.size(), "size 4")
    }
}

// 运行所有测试的主函数
fun main() {
    println("========================================")
    println("   Trie 工具库测试套件")
    println("========================================\n")
    
    var passedTests = 0
    var totalTests = 0
    
    fun runTest(testName: String, test: () -> Unit) {
        totalTests++
        try {
            test()
            println("  ✓ $testName")
            passedTests++
        } catch (e: AssertionError) {
            println("  ✗ $testName: ${e.message}")
        }
    }
    
    // ========== TrieTest ==========
    println("【TrieTest - 基础 Trie】")
    println("-".repeat(40))
    
    val trieTest = TrieTest()
    
    trieTest.setup()
    runTest("testInsertAndSearch") { trieTest.testInsertAndSearch() }
    
    trieTest.setup()
    runTest("testInsertMultipleWords") { trieTest.testInsertMultipleWords() }
    
    trieTest.setup()
    runTest("testInsertDuplicate") { trieTest.testInsertDuplicate() }
    
    trieTest.setup()
    runTest("testInsertAll") { trieTest.testInsertAll() }
    
    trieTest.setup()
    runTest("testEmptyString") { trieTest.testEmptyString() }
    
    trieTest.setup()
    runTest("testStartsWith") { trieTest.testStartsWith() }
    
    trieTest.setup()
    runTest("testPrefixCount") { trieTest.testPrefixCount() }
    
    trieTest.setup()
    runTest("testDelete") { trieTest.testDelete() }
    
    trieTest.setup()
    runTest("testDeleteNonExistent") { trieTest.testDeleteNonExistent() }
    
    trieTest.setup()
    runTest("testDeleteWithSharedPrefix") { trieTest.testDeleteWithSharedPrefix() }
    
    trieTest.setup()
    runTest("testDeleteReducesPrefixCount") { trieTest.testDeleteReducesPrefixCount() }
    
    trieTest.setup()
    runTest("testDeleteDuplicate") { trieTest.testDeleteDuplicate() }
    
    trieTest.setup()
    runTest("testCount") { trieTest.testCount() }
    
    trieTest.setup()
    runTest("testGetAllWords") { trieTest.testGetAllWords() }
    
    trieTest.setup()
    runTest("testGetAllWordsEmpty") { trieTest.testGetAllWordsEmpty() }
    
    trieTest.setup()
    runTest("testGetWordsWithPrefix") { trieTest.testGetWordsWithPrefix() }
    
    trieTest.setup()
    runTest("testAutocomplete") { trieTest.testAutocomplete() }
    
    trieTest.setup()
    runTest("testAutocompleteLimit") { trieTest.testAutocompleteLimit() }
    
    trieTest.setup()
    runTest("testLongestCommonPrefix") { trieTest.testLongestCommonPrefix() }
    
    trieTest.setup()
    runTest("testLongestCommonPrefixSingleWord") { trieTest.testLongestCommonPrefixSingleWord() }
    
    trieTest.setup()
    runTest("testLongestCommonPrefixEmpty") { trieTest.testLongestCommonPrefixEmpty() }
    
    trieTest.setup()
    runTest("testClear") { trieTest.testClear() }
    
    trieTest.setup()
    runTest("testSize") { trieTest.testSize() }
    
    trieTest.setup()
    runTest("testTotalCount") { trieTest.testTotalCount() }
    
    trieTest.setup()
    runTest("testIsEmpty") { trieTest.testIsEmpty() }
    
    trieTest.setup()
    runTest("testToString") { trieTest.testToString() }
    
    // ========== FrequencyTrieTest ==========
    println("\n【FrequencyTrieTest - 词频统计】")
    println("-".repeat(40))
    
    val freqTest = FrequencyTrieTest()
    
    freqTest.setup()
    runTest("testBasicFrequency") { freqTest.testBasicFrequency() }
    
    freqTest.setup()
    runTest("testTotalAndUnique") { freqTest.testTotalAndUnique() }
    
    freqTest.setup()
    runTest("testPrefixFrequency") { freqTest.testPrefixFrequency() }
    
    freqTest.setup()
    runTest("testGetTopK") { freqTest.testGetTopK() }
    
    freqTest.setup()
    runTest("testClear") { freqTest.testClear() }
    
    // ========== SerializableTrieTest ==========
    println("\n【SerializableTrieTest - 序列化 Trie】")
    println("-".repeat(40))
    
    val serialTest = SerializableTrieTest()
    
    serialTest.setup()
    runTest("testBasicOperations") { serialTest.testBasicOperations() }
    
    serialTest.setup()
    runTest("testSerializeDeserialize") { serialTest.testSerializeDeserialize() }
    
    serialTest.setup()
    runTest("testSerializeEmpty") { serialTest.testSerializeEmpty() }
    
    serialTest.setup()
    runTest("testSerializeMultipleWords") { serialTest.testSerializeMultipleWords() }
    
    // ========== AutocompleteTrieTest ==========
    println("\n【AutocompleteTrieTest - 自动补全 Trie】")
    println("-".repeat(40))
    
    val autoTest = AutocompleteTrieTest()
    
    autoTest.setup()
    runTest("testInsertWithWeight") { autoTest.testInsertWithWeight() }
    
    autoTest.setup()
    runTest("testAutoCompleteByWeight") { autoTest.testAutoCompleteByWeight() }
    
    autoTest.setup()
    runTest("testBoost") { autoTest.testBoost() }
    
    autoTest.setup()
    runTest("testGetTopWords") { autoTest.testGetTopWords() }
    
    autoTest.setup()
    runTest("testSearch") { autoTest.testSearch() }
    
    autoTest.setup()
    runTest("testClear") { autoTest.testClear() }
    
    autoTest.setup()
    runTest("testCompleteWithLimit") { autoTest.testCompleteWithLimit() }
    
    // ========== TrieEdgeCasesTest ==========
    println("\n【TrieEdgeCasesTest - 边界情况】")
    println("-".repeat(40))
    
    val edgeTest = TrieEdgeCasesTest()
    
    edgeTest.setup()
    runTest("testSingleCharacterWords") { edgeTest.testSingleCharacterWords() }
    
    edgeTest.setup()
    runTest("testLongWord") { edgeTest.testLongWord() }
    
    edgeTest.setup()
    runTest("testUnicodeCharacters") { edgeTest.testUnicodeCharacters() }
    
    edgeTest.setup()
    runTest("testMixedCaseWords") { edgeTest.testMixedCaseWords() }
    
    edgeTest.setup()
    runTest("testNumericStrings") { edgeTest.testNumericStrings() }
    
    edgeTest.setup()
    runTest("testSpecialCharacters") { edgeTest.testSpecialCharacters() }
    
    edgeTest.setup()
    runTest("testDeleteAllWords") { edgeTest.testDeleteAllWords() }
    
    edgeTest.setup()
    runTest("testLargeDataset") { edgeTest.testLargeDataset() }
    
    edgeTest.setup()
    runTest("testOverlappingWords") { edgeTest.testOverlappingWords() }
    
    // ========== 测试结果 ==========
    println("\n========================================")
    println("   测试结果: $passedTests/$totalTests 通过")
    println("========================================")
    
    if (passedTests == totalTests) {
        println("\n✅ 所有 52 测试全部通过!")
    } else {
        println("\n❌ 有 ${totalTests - passedTests} 测试失败")
    }
}