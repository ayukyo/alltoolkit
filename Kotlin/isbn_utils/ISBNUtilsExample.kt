/**
 * ISBN Utils 使用示例
 * 
 * 展示 ISBN 工具的各种使用场景
 * 
 * @author AllToolkit
 * @date 2026-05-13
 */

package isbn_utils

fun main() {
    println("=" .repeat(60))
    println("ISBN Utils 使用示例")
    println("=".repeat(60))
    
    // ==================== 示例 1: ISBN 验证 ====================
    println("\n【示例 1: ISBN 验证】")
    println("-".repeat(40))
    
    val validISBN10 = "0-306-40615-2"
    val validISBN13 = "978-7-115-21210-5"
    val invalidISBN = "123-456-789-X"
    
    println("验证 ISBN-10 '$validISBN10': ${ISBNUtils.validate(validISBN10)}")
    println("验证 ISBN-13 '$validISBN13': ${ISBNUtils.validate(validISBN13)}")
    println("验证无效 ISBN '$invalidISBN': ${ISBNUtils.validate(invalidISBN)}")
    
    // 使用扩展函数
    println("\n使用扩展函数:")
    println("'$validISBN10'.isValidISBN() = ${validISBN10.isValidISBN()}")
    println("'$validISBN13'.isValidISBN() = ${validISBN13.isValidISBN()}")
    
    // ==================== 示例 2: ISBN 格式化 ====================
    println("\n【示例 2: ISBN 格式化】")
    println("-".repeat(40))
    
    val rawISBN10 = "0306406152"
    val rawISBN13 = "9780306406157"
    
    println("格式化 ISBN-10 '$rawISBN10':")
    println("  -> ${ISBNUtils.format(rawISBN10)}")
    
    println("\n格式化 ISBN-13 '$rawISBN13':")
    println("  -> ${ISBNUtils.format(rawISBN13)}")
    
    // 使用扩展函数
    println("\n使用扩展函数:")
    println("'$rawISBN10'.formatISBN() = ${rawISBN10.formatISBN()}")
    
    // ==================== 示例 3: ISBN 转换 ====================
    println("\n【示例 3: ISBN-10 与 ISBN-13 互相转换】")
    println("-".repeat(40))
    
    val isbn10 = "0471958697"
    val isbn13 = "9780471958697"
    
    println("ISBN-10 转 ISBN-13:")
    println("  $isbn10 -> ${ISBNUtils.convertToISBN13(isbn10)}")
    
    println("\nISBN-13 转 ISBN-10:")
    println("  $isbn13 -> ${ISBNUtils.convertToISBN10(isbn13)}")
    
    // 979 前缀的 ISBN-13 不能转换为 ISBN-10
    val isbn13_979 = "9791091146135"
    println("\n979 前缀的 ISBN-13 不能转换为 ISBN-10:")
    println("  $isbn13_979 -> ${ISBNUtils.convertToISBN10(isbn13_979) ?: "无法转换"}")
    
    // ==================== 示例 4: ISBN 解析 ====================
    println("\n【示例 4: ISBN 解析详细信息】")
    println("-".repeat(40))
    
    val chineseISBN = "9787115212105"
    val info = ISBNUtils.parse(chineseISBN)
    
    println("解析 ISBN: $chineseISBN")
    println("  有效: ${info.isValid}")
    println("  类型: ${info.type}")
    println("  格式化: ${info.formatted}")
    println("  GS1 前缀: ${info.prefix}")
    println("  注册组: ${info.registrationGroup}")
    println("  出版者代码: ${info.registrant}")
    println("  校验位: ${info.checkDigit}")
    println("  ISBN-10: ${info.isbn10}")
    println("  ISBN-13: ${info.isbn13}")
    
    // ==================== 示例 5: 从文本提取 ISBN ====================
    println("\n【示例 5: 从文本提取 ISBN】")
    println("-".repeat(40))
    
    val text = """
        推荐书籍列表：
        1. 《代码大全》ISBN: 978-7-115-21210-5
        2. 《编程珠玑》ISBN-10: 0-201-03336-1
        3. 《算法导论》ISBN: 978-7-111-40701-0
        4. 《深入理解计算机系统》ISBN-13: 978-7-111-40665-5
        
        无效的 ISBN（仅供参考）: 123-456-789-X
    """.trimIndent()
    
    val extractedISBNs = ISBNUtils.extractFromText(text)
    println("提取到的有效 ISBN:")
    extractedISBNs.forEach { isbn ->
        println("  - $isbn (${if (isbn.length == 10) "ISBN-10" else "ISBN-13"})")
    }
    
    // ==================== 示例 6: 批量验证 ====================
    println("\n【示例 6: 批量验证 ISBN】")
    println("-".repeat(40))
    
    val isbnList = listOf(
        "0306406152",      // 有效 ISBN-10
        "9780306406157",   // 有效 ISBN-13
        "1234567890",      // 无效 ISBN-10
        "9781234567890",   // 无效 ISBN-13
        "0471958697",      // 有效 ISBN-10
        "9791091146135",   // 有效 ISBN-13（979 前缀）
        "ABCDEFGHIJ"       // 无效
    )
    
    val results = ISBNUtils.validateBatch(isbnList)
    println("批量验证结果:")
    results.forEach { (isbn, isValid) ->
        val status = if (isValid) "✓ 有效" else "✗ 无效"
        println("  $isbn: $status")
    }
    
    // ==================== 示例 7: 生成随机 ISBN ====================
    println("\n【示例 7: 生成随机 ISBN】")
    println("-".repeat(40))
    
    println("生成 5 个随机 ISBN-10:")
    repeat(5) {
        val isbn = ISBNUtils.generateRandomISBN10()
        println("  $isbn (验证: ${ISBNUtils.validateISBN10(isbn)})")
    }
    
    println("\n生成 5 个随机 ISBN-13:")
    repeat(5) {
        val isbn = ISBNUtils.generateRandomISBN13()
        println("  $isbn (验证: ${ISBNUtils.validateISBN13(isbn)})")
    }
    
    // ==================== 示例 8: ISBN 等价性比较 ====================
    println("\n【示例 8: ISBN 等价性比较】")
    println("-".repeat(40))
    
    val pairs = listOf(
        Pair("0306406152", "9780306406157"),  // 同一书的 ISBN-10 和 ISBN-13
        Pair("0-306-40615-2", "978-0-306-40615-7"),  // 格式不同
        Pair("0471958697", "9780471958697"),  // 同一本书
        Pair("0306406152", "0471958697")       // 不同的书
    )
    
    println("比较两个 ISBN 是否等价（同一本书）:")
    pairs.forEach { (isbn1, isbn2) ->
        val equivalent = ISBNUtils.areEquivalent(isbn1, isbn2)
        println("  '$isbn1' vs '$isbn2': ${if (equivalent) "等价 ✓" else "不等价 ✗"}")
    }
    
    // ==================== 示例 9: 计算 ISBN 校验位 ====================
    println("\n【示例 9: 计算 ISBN 校验位】")
    println("-".repeat(40))
    
    // ISBN-10 校验位计算
    val isbn10Base = "030640615"
    val checkDigit10 = ISBNUtils.calculateISBN10CheckDigit(isbn10Base)
    println("ISBN-10 校验位计算:")
    println("  基础号码: $isbn10Base (9位)")
    println("  校验位: $checkDigit10")
    println("  完整 ISBN: $isbn10Base$checkDigit10")
    
    // ISBN-13 校验位计算
    val isbn13Base = "978030640615"
    val checkDigit13 = ISBNUtils.calculateISBN13CheckDigit(isbn13Base)
    println("\nISBN-13 校验位计算:")
    println("  基础号码: $isbn13Base (12位)")
    println("  校验位: $checkDigit13")
    println("  完整 ISBN: $isbn13Base$checkDigit13")
    
    // ==================== 示例 10: 获取 ISBN 摘要 ====================
    println("\n【示例 10: 获取 ISBN 摘要】")
    println("-".repeat(40))
    
    val summaryISBN = "9787115212105"
    println(ISBNUtils.getSummary(summaryISBN))
    
    println("\n无效 ISBN 的摘要:")
    println(ISBNUtils.getSummary("12345"))
    
    // ==================== 示例 11: 处理中国图书 ISBN ====================
    println("\n【示例 11: 处理中国图书 ISBN】")
    println("-".repeat(40))
    
    val chineseBooks = listOf(
        "978-7-115-21210-5",  // 人民邮电出版社
        "978-7-111-40701-0",  // 机械工业出版社
        "978-7-302-33056-6",  // 清华大学出版社
        "978-7-5086-4348-3"   // 中信出版社
    )
    
    println("中国图书 ISBN 解析:")
    chineseBooks.forEach { isbn ->
        val info = ISBNUtils.parse(isbn)
        println("\n${info.formatted}")
        println("  注册组: ${info.registrationGroup} (中国)")
        println("  校验位: ${info.checkDigit}")
        if (info.isbn10 != null) {
            println("  ISBN-10: ${info.isbn10}")
        }
    }
    
    // ==================== 示例 12: 实际应用场景 ====================
    println("\n【示例 12: 实际应用场景】")
    println("-".repeat(40))
    
    // 场景：图书库存管理
    println("场景：图书库存管理系统")
    
    data class Book(
        val title: String,
        val isbn: String,
        val author: String
    )
    
    val inventory = listOf(
        Book("代码大全", "9787115212105", "Steve McConnell"),
        Book("编程珠玑", "0201033361", "Jon Bentley"),
        Book("算法导论", "9787111407010", "Thomas H. Cormen"),
        Book("深入理解计算机系统", "9787111406655", "Randal E. Bryant")
    )
    
    // 验证库存中的 ISBN
    println("\n验证库存中的 ISBN:")
    inventory.forEach { book ->
        val info = ISBNUtils.parse(book.isbn)
        val status = if (info.isValid) "✓ 有效" else "✗ 无效"
        println("  《${book.title}》ISBN: ${book.isbn} - $status")
    }
    
    // 查找重复书籍（不同 ISBN 格式但同一本书）
    println("\n检查可能的重复书籍:")
    val seenBooks = mutableMapOf<String, String>()
    inventory.forEach { book ->
        val normalizedISBN = when (ISBNUtils.detectType(book.isbn)) {
            ISBNType.ISBN_10 -> ISBNUtils.convertToISBN13(book.isbn)
            ISBNType.ISBN_13 -> ISBNUtils.cleanISBN(book.isbn)
            ISBNType.INVALID -> null
        }
        
        normalizedISBN?.let { isbn ->
            if (seenBooks.containsKey(isbn)) {
                println("  发现重复: 《${book.title}》与《${seenBooks[isbn]}》")
            } else {
                seenBooks[isbn] = book.title
            }
        }
    }
    
    // ==================== 示例 13: 数据清洗 ====================
    println("\n【示例 13: 数据清洗应用】")
    println("-".repeat(40))
    
    val rawInput = listOf(
        "ISBN: 978-7-115-21210-5",
        "0-306-40615-2",
        "978 0 306 40615 7",
        "ISBN-13: 978-0-471-95869-7",
        "123-456-789-X",  // 无效
        "ISBN10: 083621831X"
    )
    
    println("原始输入数据清洗:")
    rawInput.forEach { input ->
        val cleaned = ISBNUtils.cleanISBN(input)
        val type = ISBNUtils.detectType(cleaned)
        val isValid = ISBNUtils.validate(cleaned)
        
        println("  '$input'")
        println("    -> 清理后: '$cleaned'")
        println("    -> 类型: $type")
        println("    -> 有效: $isValid")
        println()
    }
    
    println("\n" + "=".repeat(60))
    println("示例演示完成！")
    println("=".repeat(60))
}