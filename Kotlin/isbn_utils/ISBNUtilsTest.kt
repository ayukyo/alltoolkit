/**
 * ISBN Utils 单元测试
 * 简化版，不依赖测试框架，可直接运行
 * 
 * @author AllToolkit
 * @date 2026-05-13
 */

package isbn_utils

class ISBNUtilsTest {
    
    private var passed = 0
    private var failed = 0
    
    private fun assertTrue(condition: Boolean, message: String = "") {
        if (!condition) {
            throw AssertionError("Assertion failed: $message")
        }
        passed++
    }
    
    private fun assertFalse(condition: Boolean, message: String = "") {
        if (condition) {
            throw AssertionError("Assertion failed (expected false): $message")
        }
        passed++
    }
    
    private fun assertEquals(expected: Any?, actual: Any?, message: String = "") {
        if (expected != actual) {
            throw AssertionError("Expected: $expected, Actual: $actual. $message")
        }
        passed++
    }
    
    private fun assertNull(value: Any?, message: String = "") {
        if (value != null) {
            throw AssertionError("Expected null but was: $value. $message")
        }
        passed++
    }
    
    private fun assertNotNull(value: Any?, message: String = "") {
        if (value == null) {
            throw AssertionError("Expected non-null. $message")
        }
        passed++
    }
    
    // ==================== ISBN-10 测试 ====================
    
    fun testValidateISBN10_Valid() {
        // 测试有效的 ISBN-10
        assertTrue(ISBNUtils.validateISBN10("0306406152"))   // 科学美国人
        assertTrue(ISBNUtils.validateISBN10("0-306-40615-2")) // 带连字符
        assertTrue(ISBNUtils.validateISBN10("0 306 40615 2")) // 带空格
        assertTrue(ISBNUtils.validateISBN10("0471958697"))   // 数学书
        assertTrue(ISBNUtils.validateISBN10("0-471-95869-7"))
        assertTrue(ISBNUtils.validateISBN10("0836218310"))  // 校验位是 0
        assertTrue(ISBNUtils.validateISBN10("0-8362-1831-0"))
        assertTrue(ISBNUtils.validateISBN10("7115479593"))  // 中国书籍（代码大全）
        assertTrue(ISBNUtils.validateISBN10("7-115-47959-3"))
    }
    
    fun testValidateISBN10_Invalid() {
        // 测试无效的 ISBN-10
        assertFalse(ISBNUtils.validateISBN10("0306406153"))   // 错误的校验位
        assertFalse(ISBNUtils.validateISBN10("030640615"))    // 太短
        assertFalse(ISBNUtils.validateISBN10("03064061521"))  // 太长
        assertFalse(ISBNUtils.validateISBN10("ABCDEFGHIJ"))   // 非数字
        assertFalse(ISBNUtils.validateISBN10("12345678X9"))   // X 在错误位置
        assertFalse(ISBNUtils.validateISBN10(""))             // 空
        assertFalse(ISBNUtils.validateISBN10("123456789"))    // 少一位
    }
    
    fun testCalculateISBN10CheckDigit() {
        assertEquals('2', ISBNUtils.calculateISBN10CheckDigit("030640615"))
        assertEquals('7', ISBNUtils.calculateISBN10CheckDigit("047195869"))
        assertEquals('0', ISBNUtils.calculateISBN10CheckDigit("083621831"))
        assertEquals('3', ISBNUtils.calculateISBN10CheckDigit("711547959"))
        assertEquals('2', ISBNUtils.calculateISBN10CheckDigit("020163361"))
        assertEquals('7', ISBNUtils.calculateISBN10CheckDigit("186197271"))
    }
    
    fun testFormatISBN10() {
        assertEquals("0-30640-615-2", ISBNUtils.formatISBN10("0306406152"))
        assertEquals("0-47195-869-7", ISBNUtils.formatISBN10("0471958697"))
        assertEquals("0-83621-831-0", ISBNUtils.formatISBN10("0836218310"))
        assertEquals("7-11547-959-3", ISBNUtils.formatISBN10("7115479593"))
    }
    
    // ==================== ISBN-13 测试 ====================
    
    fun testValidateISBN13_Valid() {
        // 测试有效的 ISBN-13
        assertTrue(ISBNUtils.validateISBN13("9780306406157"))  // 标准
        assertTrue(ISBNUtils.validateISBN13("978-0-306-40615-7")) // 带连字符
        assertTrue(ISBNUtils.validateISBN13("978 0 306 40615 7")) // 带空格
        assertTrue(ISBNUtils.validateISBN13("9780471958697"))
        assertTrue(ISBNUtils.validateISBN13("978-0-471-95869-7"))
        assertTrue(ISBNUtils.validateISBN13("9791091146135"))  // 979 前缀
        assertTrue(ISBNUtils.validateISBN13("979-10-91146-13-5"))
        assertTrue(ISBNUtils.validateISBN13("9787115479594"))  // 中国书籍（代码大全）
        assertTrue(ISBNUtils.validateISBN13("978-7-115-47959-4"))
    }
    
    fun testValidateISBN13_Invalid() {
        // 测试无效的 ISBN-13
        assertFalse(ISBNUtils.validateISBN13("9780306406158"))   // 错误的校验位
        assertFalse(ISBNUtils.validateISBN13("978030640615"))    // 太短
        assertFalse(ISBNUtils.validateISBN13("97803064061577"))  // 太长
        assertFalse(ISBNUtils.validateISBN13("9770306406157"))   // 错误前缀
        assertFalse(ISBNUtils.validateISBN13("ABCDEFGHIJKLM"))   // 非数字
        assertFalse(ISBNUtils.validateISBN13(""))               // 空
        assertFalse(ISBNUtils.validateISBN13("123456789012"))   // 错误前缀
    }
    
    fun testCalculateISBN13CheckDigit() {
        assertEquals('7', ISBNUtils.calculateISBN13CheckDigit("978030640615"))
        assertEquals('7', ISBNUtils.calculateISBN13CheckDigit("978047195869"))
        assertEquals('5', ISBNUtils.calculateISBN13CheckDigit("979109114613"))
        assertEquals('4', ISBNUtils.calculateISBN13CheckDigit("978711547959"))
        assertEquals('2', ISBNUtils.calculateISBN13CheckDigit("978186197271"))
    }
    
    fun testFormatISBN13() {
        assertEquals("978-0-30640-615-7", ISBNUtils.formatISBN13("9780306406157"))
        assertEquals("978-0-47195-869-7", ISBNUtils.formatISBN13("9780471958697"))
        assertEquals("979-1-09114-613-5", ISBNUtils.formatISBN13("9791091146135"))
        assertEquals("978-7-11547-959-4", ISBNUtils.formatISBN13("9787115479594"))
    }
    
    // ==================== 类型检测测试 ====================
    
    fun testDetectType() {
        assertEquals(ISBNType.ISBN_10, ISBNUtils.detectType("0306406152"))
        assertEquals(ISBNType.ISBN_10, ISBNUtils.detectType("0-306-40615-2"))
        assertEquals(ISBNType.ISBN_13, ISBNUtils.detectType("9780306406157"))
        assertEquals(ISBNType.ISBN_13, ISBNUtils.detectType("978-0-306-40615-7"))
        assertEquals(ISBNType.INVALID, ISBNUtils.detectType("123"))
        assertEquals(ISBNType.INVALID, ISBNUtils.detectType("ABCDEFGHIJ"))
        assertEquals(ISBNType.INVALID, ISBNUtils.detectType(""))
    }
    
    // ==================== 验证测试 ====================
    
    fun testValidate() {
        assertTrue(ISBNUtils.validate("0306406152"))
        assertTrue(ISBNUtils.validate("9780306406157"))
        assertFalse(ISBNUtils.validate("12345"))
        assertFalse(ISBNUtils.validate("0306406153"))
        assertFalse(ISBNUtils.validate("9780306406158"))
    }
    
    // ==================== 转换测试 ====================
    
    fun testConvertToISBN13() {
        assertEquals("9780306406157", ISBNUtils.convertToISBN13("0306406152"))
        assertEquals("9780471958697", ISBNUtils.convertToISBN13("0471958697"))
        assertEquals("9781861972712", ISBNUtils.convertToISBN13("1861972717"))
        assertEquals("9787115479594", ISBNUtils.convertToISBN13("7115479593"))
        
        // 无效的 ISBN-10 应该返回 null
        assertNull(ISBNUtils.convertToISBN13("0306406153"))
        assertNull(ISBNUtils.convertToISBN13("12345"))
    }
    
    fun testConvertToISBN10() {
        assertEquals("0306406152", ISBNUtils.convertToISBN10("9780306406157"))
        assertEquals("0471958697", ISBNUtils.convertToISBN10("9780471958697"))
        assertEquals("1861972717", ISBNUtils.convertToISBN10("9781861972712"))
        assertEquals("7115479593", ISBNUtils.convertToISBN10("9787115479594"))
        
        // 979 前缀的 ISBN-13 不能转换为 ISBN-10
        assertNull(ISBNUtils.convertToISBN10("9791091146135"))
        
        // 无效的 ISBN-13 应该返回 null
        assertNull(ISBNUtils.convertToISBN10("9780306406158"))
        assertNull(ISBNUtils.convertToISBN10("12345"))
    }
    
    // ==================== 解析测试 ====================
    
    fun testParse_ValidISBN10() {
        val info = ISBNUtils.parse("0306406152")
        
        assertTrue(info.isValid)
        assertEquals(ISBNType.ISBN_10, info.type)
        assertEquals("0306406152", info.original)
        assertEquals("9780306406157", info.isbn13)
        assertEquals("0306406152", info.isbn10)
        assertEquals('2', info.checkDigit)
        assertNull(info.prefix) // ISBN-10 没有前缀
    }
    
    fun testParse_ValidISBN13() {
        val info = ISBNUtils.parse("9780306406157")
        
        assertTrue(info.isValid)
        assertEquals(ISBNType.ISBN_13, info.type)
        assertEquals("9780306406157", info.original)
        assertEquals("9780306406157", info.isbn13)
        assertEquals("0306406152", info.isbn10)
        assertEquals('7', info.checkDigit)
        assertEquals("978", info.prefix)
    }
    
    fun testParse_ValidISBN13_979Prefix() {
        val info = ISBNUtils.parse("9791091146135")
        
        assertTrue(info.isValid)
        assertEquals(ISBNType.ISBN_13, info.type)
        assertEquals("9791091146135", info.isbn13)
        assertNull(info.isbn10) // 979 前缀不能转换为 ISBN-10
        assertEquals("979", info.prefix)
    }
    
    fun testParse_InvalidISBN() {
        val info = ISBNUtils.parse("12345")
        
        assertFalse(info.isValid)
        assertEquals(ISBNType.INVALID, info.type)
        assertNull(info.isbn10)
        assertNull(info.isbn13)
    }
    
    // ==================== 生成测试 ====================
    
    fun testGenerateRandomISBN10() {
        val isbn = ISBNUtils.generateRandomISBN10()
        
        assertEquals(10, isbn.length)
        assertTrue(ISBNUtils.validateISBN10(isbn))
    }
    
    fun testGenerateRandomISBN13() {
        val isbn = ISBNUtils.generateRandomISBN13()
        
        assertEquals(13, isbn.length)
        assertTrue(ISBNUtils.validateISBN13(isbn))
        assertTrue(isbn.startsWith("978") || isbn.startsWith("979"))
    }
    
    fun testGenerateMultipleRandomISBNs() {
        // 生成多个随机 ISBN，确保它们都是有效的
        repeat(100) {
            val isbn10 = ISBNUtils.generateRandomISBN10()
            val isbn13 = ISBNUtils.generateRandomISBN13()
            
            assertTrue(ISBNUtils.validateISBN10(isbn10), "Invalid ISBN-10: $isbn10")
            assertTrue(ISBNUtils.validateISBN13(isbn13), "Invalid ISBN-13: $isbn13")
        }
    }
    
    // ==================== 批量验证测试 ====================
    
    fun testValidateBatch() {
        val isbns = listOf(
            "0306406152",   // 有效 ISBN-10
            "9780306406157", // 有效 ISBN-13
            "12345",        // 无效
            "0306406153",   // 无效 ISBN-10（错误校验位）
            "9780306406158"  // 无效 ISBN-13（错误校验位）
        )
        
        val results = ISBNUtils.validateBatch(isbns)
        
        assertTrue(results["0306406152"]!!)
        assertTrue(results["9780306406157"]!!)
        assertFalse(results["12345"]!!)
        assertFalse(results["0306406153"]!!)
        assertFalse(results["9780306406158"]!!)
    }
    
    // ==================== 文本提取测试 ====================
    
    fun testExtractFromText() {
        val text = """
            这本书的 ISBN 是 978-7-115-47959-4，另一本是 ISBN-10: 0-306-40615-2。
            还有 9780471958697 和 0836218310 也在这里。
            无效的：12345 和 978-0-306-40615-8（校验位错误）
        """.trimIndent()
        
        val extracted = ISBNUtils.extractFromText(text)
        
        assertTrue(extracted.contains("9787115479594"))
        assertTrue(extracted.contains("0306406152"))
        assertTrue(extracted.contains("9780471958697"))
        assertTrue(extracted.contains("0836218310"))
        // 无效的 ISBN 不应该被提取
        assertFalse(extracted.any { it.contains("12345") || it.contains("9780306406158") })
    }
    
    fun testExtractFromText_Empty() {
        val extracted = ISBNUtils.extractFromText("没有 ISBN 的文本")
        assertTrue(extracted.isEmpty())
    }
    
    // ==================== 等价性比较测试 ====================
    
    fun testAreEquivalent() {
        // 同一 ISBN 的不同格式应该是等价的
        assertTrue(ISBNUtils.areEquivalent("0306406152", "9780306406157"))
        assertTrue(ISBNUtils.areEquivalent("0-306-40615-2", "978-0-306-40615-7"))
        assertTrue(ISBNUtils.areEquivalent("0471958697", "9780471958697"))
        assertTrue(ISBNUtils.areEquivalent("7115479593", "9787115479594"))
        
        // 不同的 ISBN 不应该等价
        assertFalse(ISBNUtils.areEquivalent("0306406152", "0471958697"))
        assertFalse(ISBNUtils.areEquivalent("9780306406157", "9780471958697"))
        
        // 无效的 ISBN 不应该等价
        assertFalse(ISBNUtils.areEquivalent("12345", "9780306406157"))
        assertFalse(ISBNUtils.areEquivalent("0306406152", "12345"))
    }
    
    // ==================== 清理测试 ====================
    
    fun testCleanISBN() {
        assertEquals("0306406152", ISBNUtils.cleanISBN("0-306-40615-2"))
        assertEquals("0306406152", ISBNUtils.cleanISBN("0 306 40615 2"))
        assertEquals("0306406152", ISBNUtils.cleanISBN("ISBN: 0-306-40615-2"))
        assertEquals("9780306406157", ISBNUtils.cleanISBN("978-0-306-40615-7"))
        assertEquals("083621831X", ISBNUtils.cleanISBN("0-8362-1831-X"))
        assertEquals("083621831X", ISBNUtils.cleanISBN("083621831x")) // 小写 x
    }
    
    // ==================== 扩展函数测试 ====================
    
    fun testExtensionFunctions() {
        // String.isValidISBN()
        assertTrue("0306406152".isValidISBN())
        assertTrue("9780306406157".isValidISBN())
        assertFalse("12345".isValidISBN())
        
        // String.formatISBN()
        assertEquals("0-30640-615-2", "0306406152".formatISBN())
        assertEquals("978-0-30640-615-7", "9780306406157".formatISBN())
        
        // String.parseISBN()
        val info = "0306406152".parseISBN()
        assertTrue(info.isValid)
        assertEquals(ISBNType.ISBN_10, info.type)
    }
    
    // ==================== 边界条件测试 ====================
    
    fun testEdgeCases() {
        // 最小的有效 ISBN-10（数字）
        assertTrue(ISBNUtils.validateISBN10("0000000000"))
        
        // 测试不同格式的输入
        assertTrue(ISBNUtils.validate("ISBN 0-306-40615-2"))
        assertTrue(ISBNUtils.validate("ISBN:978-0-306-40615-7"))
    }
    
    fun testChineseISBN() {
        // 中国 ISBN（前缀 7）
        val chineseISBN10 = "7115479593"
        val chineseISBN13 = "9787115479594"
        
        assertTrue(ISBNUtils.validateISBN10(chineseISBN10))
        assertTrue(ISBNUtils.validateISBN13(chineseISBN13))
        
        val info10 = ISBNUtils.parse(chineseISBN10)
        assertTrue(info10.isValid)
        assertEquals("7", info10.registrationGroup)
        
        val info13 = ISBNUtils.parse(chineseISBN13)
        assertTrue(info13.isValid)
        assertEquals("7", info13.registrationGroup)
        assertEquals("978", info13.prefix)
    }
    
    // ==================== 摘要输出测试 ====================
    
    fun testGetSummary() {
        val summary = ISBNUtils.getSummary("9787115479594")
        
        assertTrue(summary.contains("ISBN-13"))
        assertTrue(summary.contains("9787115479594"))
        assertTrue(summary.contains("978"))
        assertTrue(summary.contains("校验位"))
    }
    
    fun testGetSummary_Invalid() {
        val summary = ISBNUtils.getSummary("12345")
        
        assertTrue(summary.contains("无效"))
    }
    
    // ==================== 性能测试 ====================
    
    fun testPerformance() {
        val startTime = System.currentTimeMillis()
        
        // 验证 10000 次
        repeat(10000) {
            ISBNUtils.validateISBN10("0306406152")
            ISBNUtils.validateISBN13("9780306406157")
        }
        
        val endTime = System.currentTimeMillis()
        val duration = endTime - startTime
        
        // 应该在合理时间内完成（通常 < 100ms）
        println("验证 20000 次 ISBN 耗时: ${duration}ms")
        assertTrue(duration < 1000, "性能测试失败: ${duration}ms")
    }
    
    // ==================== 运行所有测试 ====================
    
    fun runAllTests() {
        println("=" .repeat(60))
        println("ISBN Utils 单元测试")
        println("=".repeat(60))
        
        val tests = listOf(
            Pair("testValidateISBN10_Valid", { testValidateISBN10_Valid() }),
            Pair("testValidateISBN10_Invalid", { testValidateISBN10_Invalid() }),
            Pair("testCalculateISBN10CheckDigit", { testCalculateISBN10CheckDigit() }),
            Pair("testFormatISBN10", { testFormatISBN10() }),
            Pair("testValidateISBN13_Valid", { testValidateISBN13_Valid() }),
            Pair("testValidateISBN13_Invalid", { testValidateISBN13_Invalid() }),
            Pair("testCalculateISBN13CheckDigit", { testCalculateISBN13CheckDigit() }),
            Pair("testFormatISBN13", { testFormatISBN13() }),
            Pair("testDetectType", { testDetectType() }),
            Pair("testValidate", { testValidate() }),
            Pair("testConvertToISBN13", { testConvertToISBN13() }),
            Pair("testConvertToISBN10", { testConvertToISBN10() }),
            Pair("testParse_ValidISBN10", { testParse_ValidISBN10() }),
            Pair("testParse_ValidISBN13", { testParse_ValidISBN13() }),
            Pair("testParse_ValidISBN13_979Prefix", { testParse_ValidISBN13_979Prefix() }),
            Pair("testParse_InvalidISBN", { testParse_InvalidISBN() }),
            Pair("testGenerateRandomISBN10", { testGenerateRandomISBN10() }),
            Pair("testGenerateRandomISBN13", { testGenerateRandomISBN13() }),
            Pair("testGenerateMultipleRandomISBNs", { testGenerateMultipleRandomISBNs() }),
            Pair("testValidateBatch", { testValidateBatch() }),
            Pair("testExtractFromText", { testExtractFromText() }),
            Pair("testExtractFromText_Empty", { testExtractFromText_Empty() }),
            Pair("testAreEquivalent", { testAreEquivalent() }),
            Pair("testCleanISBN", { testCleanISBN() }),
            Pair("testExtensionFunctions", { testExtensionFunctions() }),
            Pair("testEdgeCases", { testEdgeCases() }),
            Pair("testChineseISBN", { testChineseISBN() }),
            Pair("testGetSummary", { testGetSummary() }),
            Pair("testGetSummary_Invalid", { testGetSummary_Invalid() }),
            Pair("testPerformance", { testPerformance() })
        )
        
        tests.forEach { (name, test) ->
            try {
                test()
                println("✓ $name")
            } catch (e: AssertionError) {
                failed++
                println("✗ $name: ${e.message}")
            }
        }
        
        println("\n" + "=".repeat(60))
        println("测试结果: $passed 通过, $failed 失败")
        println("=".repeat(60))
        
        if (failed > 0) {
            throw AssertionError("有 $failed 个测试失败")
        }
    }
}

fun main() {
    val test = ISBNUtilsTest()
    test.runAllTests()
}