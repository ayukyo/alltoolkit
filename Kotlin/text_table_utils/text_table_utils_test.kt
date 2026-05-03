/**
 * Text Table Utils 测试文件
 * 纯 Kotlin 标准库实现，零外部依赖
 * 
 * @author AllToolkit
 * @date 2026-05-03
 */

package text_table_utils

// 简单断言函数
fun assertTrue(condition: Boolean, message: String = "") {
    if (!condition) {
        throw AssertionError("Assertion failed: $message")
    }
}

fun assertFalse(condition: Boolean, message: String = "") {
    if (condition) {
        throw AssertionError("Assertion failed (expected false): $message")
    }
}

fun <T> assertEquals(expected: T, actual: T, message: String = "") {
    if (expected != actual) {
        throw AssertionError("Assertion failed: expected <$expected> but was <$actual>. $message")
    }
}

object TextTableUtilsTest {
    
    fun testBasicTable() {
        println("Testing: testBasicTable")
        val table = TextTable(
            listOf(
                Column("Name", 10),
                Column("Age", 5, Alignment.CENTER),
                Column("City", 15)
            )
        )
        table.addRow("Alice", "25", "New York")
        table.addRow("Bob", "30", "Los Angeles")
        
        val ascii = table.toAscii()
        assertTrue(ascii.contains("Alice"), "Should contain Alice")
        assertTrue(ascii.contains("Bob"), "Should contain Bob")
        assertTrue(ascii.contains("Name"), "Should contain Name")
        assertTrue(ascii.contains("Age"), "Should contain Age")
        assertTrue(ascii.contains("City"), "Should contain City")
        assertTrue(ascii.contains("+"), "Should contain +")
        assertTrue(ascii.contains("-"), "Should contain -")
        assertTrue(ascii.contains("|"), "Should contain |")
        println("  ✓ Passed")
    }
    
    fun testMarkdownTable() {
        println("Testing: testMarkdownTable")
        val table = TextTable(
            listOf(
                Column("Product", alignment = Alignment.LEFT),
                Column("Price", alignment = Alignment.RIGHT),
                Column("Stock", alignment = Alignment.CENTER)
            )
        )
        table.addRow("Apple", "$1.50", "100")
        table.addRow("Banana", "$0.75", "200")
        
        val markdown = table.toMarkdown()
        assertTrue(markdown.contains("|"), "Should contain |")
        assertTrue(markdown.contains("Product"), "Should contain Product")
        assertTrue(markdown.contains("Price"), "Should contain Price")
        assertTrue(markdown.contains("Apple"), "Should contain Apple")
        assertTrue(markdown.contains("Banana"), "Should contain Banana")
        assertTrue(markdown.contains("---"), "Should contain ---")
        println("  ✓ Passed")
    }
    
    fun testHtmlTable() {
        println("Testing: testHtmlTable")
        val table = TextTable(
            listOf(
                Column("ID", alignment = Alignment.CENTER),
                Column("Name"),
                Column("Score", alignment = Alignment.RIGHT)
            )
        )
        table.addRow("1", "John", "95")
        table.addRow("2", "Jane", "88")
        
        val html = table.toHtml()
        assertTrue(html.contains("<table>"), "Should contain <table>")
        assertTrue(html.contains("<thead>"), "Should contain <thead>")
        assertTrue(html.contains("<tbody>"), "Should contain <tbody>")
        assertTrue(html.contains("<th"), "Should contain <th")
        assertTrue(html.contains("<td"), "Should contain <td")
        assertTrue(html.contains("John"), "Should contain John")
        assertTrue(html.contains("Jane"), "Should contain Jane")
        assertTrue(html.contains("text-align"), "Should contain text-align")
        println("  ✓ Passed")
    }
    
    fun testCsvOutput() {
        println("Testing: testCsvOutput")
        val table = TextTable(
            listOf(
                Column("Name"),
                Column("Email"),
                Column("Phone")
            )
        )
        table.addRow("Alice", "alice@example.com", "123-456-7890")
        table.addRow("Bob", "bob@test.org", "098-765-4321")
        
        val csv = table.toCsv()
        assertTrue(csv.contains("Name,Email,Phone"), "Should contain header")
        assertTrue(csv.contains("Alice,alice@example.com,123-456-7890"), "Should contain Alice row")
        assertTrue(csv.contains("Bob,bob@test.org,098-765-4321"), "Should contain Bob row")
        println("  ✓ Passed")
    }
    
    fun testCsvEscape() {
        println("Testing: testCsvEscape")
        val table = TextTable(listOf(Column("Name"), Column("Description")))
        table.addRow("Product A", "Contains, special chars")
        table.addRow("Product B", "Has \"quotes\" inside")
        
        val csv = table.toCsv()
        assertTrue(csv.contains("\"Contains, special chars\""), "Should escape comma")
        assertTrue(csv.contains("\"Has \"\"quotes\"\" inside\""), "Should escape quotes")
        println("  ✓ Passed")
    }
    
    fun testJsonOutput() {
        println("Testing: testJsonOutput")
        val table = TextTable(
            listOf(Column("Key"), Column("Value"))
        )
        table.addRow("name", "Alice")
        table.addRow("age", "25")
        
        val json = table.toJson()
        assertTrue(json.contains("\"Key\""), "Should contain Key")
        assertTrue(json.contains("\"Value\""), "Should contain Value")
        assertTrue(json.contains("\"name\""), "Should contain name")
        assertTrue(json.contains("\"Alice\""), "Should contain Alice")
        assertTrue(json.startsWith("["), "Should start with [")
        assertTrue(json.endsWith("]"), "Should end with ]")
        println("  ✓ Passed")
    }
    
    fun testSimpleTable() {
        println("Testing: testSimpleTable")
        val table = TextTable(
            listOf(
                Column("A"),
                Column("B"),
                Column("C")
            )
        )
        table.addRow("1", "2", "3")
        table.addRow("4", "5", "6")
        
        val simple = table.toSimple()
        assertTrue(simple.contains("A"), "Should contain A")
        assertTrue(simple.contains("B"), "Should contain B")
        assertTrue(simple.contains("C"), "Should contain C")
        assertFalse(simple.contains("|"), "Should not contain |")
        println("  ✓ Passed")
    }
    
    fun testTableBuilder() {
        println("Testing: testTableBuilder")
        val table = table {
            column("Name")
            rightColumn("Score")
            centerColumn("Grade")
            row("Alice", "95", "A")
            row("Bob", "82", "B")
        }
        
        val ascii = table.toAscii()
        assertTrue(ascii.contains("Alice"), "Should contain Alice")
        assertTrue(ascii.contains("Bob"), "Should contain Bob")
        assertTrue(ascii.contains("95"), "Should contain 95")
        assertTrue(ascii.contains("82"), "Should contain 82")
        println("  ✓ Passed")
    }
    
    fun testQuickTable() {
        println("Testing: testQuickTable")
        val table = quickTable("Col1", "Col2", "Col3")
        table.addRow("A", "B", "C")
        
        val output = table.toAscii()
        assertTrue(output.contains("Col1"), "Should contain Col1")
        assertTrue(output.contains("Col2"), "Should contain Col2")
        assertTrue(output.contains("Col3"), "Should contain Col3")
        println("  ✓ Passed")
    }
    
    fun testArrayToTable() {
        println("Testing: testArrayToTable")
        val headers = listOf("ID", "Name", "Score")
        val data = listOf(
            listOf("1", "Alice", "90"),
            listOf("2", "Bob", "85")
        )
        
        val table = arrayToTable(headers, data)
        val output = table.toAscii()
        
        assertTrue(output.contains("Alice"), "Should contain Alice")
        assertTrue(output.contains("Bob"), "Should contain Bob")
        assertTrue(output.contains("90"), "Should contain 90")
        assertTrue(output.contains("85"), "Should contain 85")
        println("  ✓ Passed")
    }
    
    fun testAlignmentLeft() {
        println("Testing: testAlignmentLeft")
        val table = TextTable(listOf(Column("Test", width = 10, alignment = Alignment.LEFT)))
        table.addRow("abc")
        
        val ascii = table.toAscii()
        assertTrue(ascii.contains("abc"), "Should contain abc")
        println("  ✓ Passed")
    }
    
    fun testAlignmentRight() {
        println("Testing: testAlignmentRight")
        val table = TextTable(listOf(Column("Number", width = 10, alignment = Alignment.RIGHT)))
        table.addRow("123")
        
        val ascii = table.toAscii()
        assertTrue(ascii.contains("123"), "Should contain 123")
        println("  ✓ Passed")
    }
    
    fun testAlignmentCenter() {
        println("Testing: testAlignmentCenter")
        val table = TextTable(listOf(Column("Title", width = 10, alignment = Alignment.CENTER)))
        table.addRow("Hi")
        
        val ascii = table.toAscii()
        assertTrue(ascii.contains("Hi"), "Should contain Hi")
        println("  ✓ Passed")
    }
    
    fun testEmptyTable() {
        println("Testing: testEmptyTable")
        val table = TextTable(listOf(Column("Empty")))
        val output = table.toAscii()
        
        assertTrue(output.contains("Empty"), "Should contain Empty")
        assertTrue(output.contains("+"), "Should contain +")
        println("  ✓ Passed")
    }
    
    fun testAddMultipleRows() {
        println("Testing: testAddMultipleRows")
        val table = quickTable("A", "B")
        table.addRows(
            listOf(
                listOf("1", "2"),
                listOf("3", "4"),
                listOf("5", "6")
            )
        )
        
        val rows = table.getRows()
        assertEquals(3, rows.size, "Should have 3 rows")
        assertEquals(listOf("1", "2"), rows[0], "First row should be [1, 2]")
        assertEquals(listOf("5", "6"), rows[2], "Third row should be [5, 6]")
        println("  ✓ Passed")
    }
    
    fun testHtmlEscape() {
        println("Testing: testHtmlEscape")
        val table = TextTable(listOf(Column("Text")))
        table.addRow("<script>alert('xss')</script>")
        table.addRow("A & B")
        table.addRow("\"quoted\"")
        
        val html = table.toHtml()
        assertTrue(html.contains("&lt;script&gt;"), "Should escape < and >")
        assertTrue(html.contains("&amp;"), "Should escape &")
        assertTrue(html.contains("&quot;"), "Should escape quotes")
        assertFalse(html.contains("<script>"), "Should not contain raw <script>")
        println("  ✓ Passed")
    }
    
    fun testChineseCharacters() {
        println("Testing: testChineseCharacters")
        val table = TextTable(listOf(Column("姓名"), Column("年龄")))
        table.addRow("张三", "25")
        table.addRow("李四", "30")
        
        val ascii = table.toAscii()
        assertTrue(ascii.contains("张三"), "Should contain 张三")
        assertTrue(ascii.contains("李四"), "Should contain 李四")
        println("  ✓ Passed")
    }
    
    fun testChainedOperations() {
        println("Testing: testChainedOperations")
        val table = quickTable("A", "B")
            .addRow("1", "2")
            .addRow("3", "4")
        
        val rows = table.getRows()
        assertEquals(2, rows.size, "Should have 2 rows")
        println("  ✓ Passed")
    }
    
    fun testShortColumnValues() {
        println("Testing: testShortColumnValues")
        val table = TextTable(
            listOf(
                Column("Long Title Name", alignment = Alignment.CENTER),
                Column("X", alignment = Alignment.CENTER)
            )
        )
        table.addRow("A", "B")
        
        val ascii = table.toAscii()
        assertTrue(ascii.contains("Long Title Name"), "Should contain Long Title Name")
        println("  ✓ Passed")
    }
    
    fun testFixedWidthColumns() {
        println("Testing: testFixedWidthColumns")
        val table = TextTable(
            listOf(
                Column("Name", width = 15),
                Column("Value", width = 10)
            )
        )
        table.addRow("Short", "X")
        
        val lines = table.toAscii().split("\n")
        // 检查所有行长度应该一致
        val lineWidths = lines.map { it.length }.distinct()
        assertTrue(lineWidths.size <= 2, "Line widths should be consistent") // 允许空行的差异
        println("  ✓ Passed")
    }
    
    fun testAlignConstants() {
        println("Testing: testAlignConstants")
        assertEquals(Alignment.LEFT, Align.LEFT, "Align.LEFT should equal Alignment.LEFT")
        assertEquals(Alignment.CENTER, Align.CENTER, "Align.CENTER should equal Alignment.CENTER")
        assertEquals(Alignment.RIGHT, Align.RIGHT, "Align.RIGHT should equal Alignment.RIGHT")
        println("  ✓ Passed")
    }
    
    fun testTableToString() {
        println("Testing: testTableToString")
        val table = quickTable("A", "B")
        table.addRow("1", "2")
        
        // toString 应该返回 ASCII 格式
        val output = table.toString()
        assertTrue(output.contains("A"), "Should contain A")
        assertTrue(output.contains("+"), "Should contain +")
        assertTrue(output.contains("|"), "Should contain |")
        println("  ✓ Passed")
    }
    
    fun testJsonEscape() {
        println("Testing: testJsonEscape")
        val table = TextTable(listOf(Column("Text")))
        table.addRow("Line1\nLine2")
        table.addRow("Tab\there")
        table.addRow("Quote\"test")
        
        val json = table.toJson()
        assertTrue(json.contains("\\n"), "Should escape newline")
        assertTrue(json.contains("\\t"), "Should escape tab")
        assertTrue(json.contains("\\\""), "Should escape quote")
        println("  ✓ Passed")
    }
    
    fun testLargeTable() {
        println("Testing: testLargeTable")
        val builder = TableBuilder()
        builder.column("ID", alignment = Alignment.CENTER)
        builder.column("Name")
        builder.column("Score", alignment = Alignment.RIGHT)
        
        for (i in 1..100) {
            builder.row(i.toString(), "User$i", (i * 10).toString())
        }
        
        val table = builder.build()
        val ascii = table.toAscii()
        
        assertTrue(ascii.contains("User1"), "Should contain User1")
        assertTrue(ascii.contains("User50"), "Should contain User50")
        assertTrue(ascii.contains("User100"), "Should contain User100")
        println("  ✓ Passed")
    }
    
    fun runAll() {
        println("=" .repeat(60))
        println("Running TextTable Utils Tests")
        println("=" .repeat(60))
        println()
        
        val tests = listOf(
            { testBasicTable() },
            { testMarkdownTable() },
            { testHtmlTable() },
            { testCsvOutput() },
            { testCsvEscape() },
            { testJsonOutput() },
            { testSimpleTable() },
            { testTableBuilder() },
            { testQuickTable() },
            { testArrayToTable() },
            { testAlignmentLeft() },
            { testAlignmentRight() },
            { testAlignmentCenter() },
            { testEmptyTable() },
            { testAddMultipleRows() },
            { testHtmlEscape() },
            { testChineseCharacters() },
            { testChainedOperations() },
            { testShortColumnValues() },
            { testFixedWidthColumns() },
            { testAlignConstants() },
            { testTableToString() },
            { testJsonEscape() },
            { testLargeTable() }
        )
        
        var passed = 0
        var failed = 0
        
        tests.forEach { test ->
            try {
                test()
                passed++
            } catch (e: AssertionError) {
                println("  ✗ Failed: ${e.message}")
                failed++
            } catch (e: Exception) {
                println("  ✗ Error: ${e.message}")
                failed++
            }
        }
        
        println()
        println("=" .repeat(60))
        println("Results: $passed passed, $failed failed")
        println("=" .repeat(60))
    }
}

/**
 * 主函数 - 运行测试和演示
 */
fun main() {
    // 运行测试
    TextTableUtilsTest.runAll()
    println()
    
    // 演示示例
    println("=" .repeat(60))
    println("Text Table Utils - 功能演示")
    println("=" .repeat(60))
    println()
    
    // 示例1: 基本表格
    println("1. 基本 ASCII 表格:")
    println("-" .repeat(40))
    val table1 = TextTable(
        listOf(
            Column("姓名", 12),
            Column("年龄", 6, Alignment.CENTER),
            Column("城市", 15)
        )
    )
    table1.addRow("张三", "25", "北京")
    table1.addRow("李四", "30", "上海")
    table1.addRow("王五", "28", "广州")
    println(table1.toAscii())
    println()
    
    // 示例2: Markdown 表格
    println("2. Markdown 格式表格:")
    println("-" .repeat(40))
    val table2 = table {
        column("产品")
        rightColumn("价格")
        centerColumn("库存")
        row("苹果", "¥5.50", "100")
        row("香蕉", "¥3.20", "200")
        row("橙子", "¥4.80", "150")
    }
    println(table2.toMarkdown())
    println()
    
    // 示例3: HTML 表格
    println("3. HTML 格式表格:")
    println("-" .repeat(40))
    val table3 = quickTable("ID", "名称", "状态")
    table3.addRow("001", "任务A", "完成")
    table3.addRow("002", "任务B", "进行中")
    println(table3.toHtml("data-table"))
    println()
    
    // 示例4: CSV 输出
    println("4. CSV 格式输出:")
    println("-" .repeat(40))
    val table4 = TextTable(listOf(Column("Name"), Column("Email"), Column("Role")))
    table4.addRow("Alice", "alice@example.com", "Admin")
    table4.addRow("Bob", "bob@test.org", "User")
    println(table4.toCsv())
    println()
    
    // 示例5: JSON 输出
    println("5. JSON 格式输出:")
    println("-" .repeat(40))
    val table5 = table {
        centerColumn("Key")
        column("Value")
        row("version", "1.0.0")
        row("name", "TextTable")
    }
    println(table5.toJson())
    println()
    
    // 示例6: 简单格式
    println("6. 简单格式表格:")
    println("-" .repeat(40))
    val table6 = quickTable("部门", "人数", "平均年龄")
    table6.addRow("研发部", "50", "28")
    table6.addRow("市场部", "20", "32")
    table6.addRow("财务部", "10", "35")
    println(table6.toSimple())
    println()
    
    // 示例7: 使用构建器
    println("7. 使用构建器创建复杂表格:")
    println("-" .repeat(40))
    val table7 = TableBuilder()
        .centerColumn("#", width = 5)
        .leftColumn("名称", width = 20)
        .rightColumn("分数", width = 8)
        .centerColumn("等级", width = 6)
        .row("1", "数学", "95", "A")
        .row("2", "英语", "88", "B")
        .row("3", "物理", "92", "A")
        .build()
    println(table7.toAscii())
    println()
    
    println("=" .repeat(60))
    println("所有演示完成!")
    println("=" .repeat(60))
}