/**
 ISBN Utils 使用示例
 
 展示如何在实际项目中使用 ISBN 工具库
 */

import Foundation

// MARK: - 示例 1: 图书管理系统中验证 ISBN

struct Book: CustomStringConvertible {
    let title: String
    let author: String
    let isbn: ISBN
    
    var description: String {
        return "《\(title)》- \(author) [\(isbn.formatted)]"
    }
    
    init?(title: String, author: String, isbnString: String) {
        guard case .success(let isbnValue) = ISBNUtils.validate(isbnString) else {
            print("❌ 无效的 ISBN: \(isbnString)")
            return nil
        }
        self.title = title
        self.author = author
        self.isbn = isbnValue
    }
}

func example1_BookManagement() {
    print("\n" + "=" * 50)
    print("示例 1: 图书管理系统中的 ISBN 验证")
    print("=" * 50)
    
    let books = [
        (title: "Clean Code", author: "Robert C. Martin", isbn: "978-0-13-235088-4"),
        (title: "The Pragmatic Programmer", author: "David Thomas", isbn: "9780201616224"),
        (title: "Design Patterns", author: "Gang of Four", isbn: "0-201-63361-2"),
        (title: "无效书籍", author: "测试", isbn: "1234567890"),  // 无效 ISBN
    ]
    
    var library: [Book] = []
    
    for bookInfo in books {
        if let book = Book(title: bookInfo.title, author: bookInfo.author, isbnString: bookInfo.isbn) {
            library.append(book)
            print("✅ 添加成功: \(book)")
        }
    }
    
    print("\n📚 图书馆共有 \(library.count) 本书")
}

// MARK: - 示例 2: 批量转换 ISBN

func example2_BatchConversion() {
    print("\n" + "=" * 50)
    print("示例 2: 批量转换 ISBN-10 到 ISBN-13")
    print("=" * 50)
    
    let isbn10List = [
        "0306406152",
        "0132350884",
        "020161622X",
        "080442957X",
    ]
    
    print("\n转换结果:")
    for isbn10 in isbn10List {
        switch ISBNUtils.toISBN13(isbn10) {
        case .success(let isbn13):
            print("  \(ISBNUtils.formatISBN10(isbn10)) → \(ISBNUtils.formatISBN13(isbn13))")
        case .failure(let error):
            print("  \(isbn10) 转换失败: \(error.localizedDescription)")
        }
    }
}

// MARK: - 示例 3: 从网页抓取的文本中提取 ISBN

func example3_ExtractFromText() {
    print("\n" + "=" * 50)
    print("示例 3: 从文本中提取 ISBN")
    print("=" * 50)
    
    let webpageContent = """
    推荐书单 2024
    
    1. 《代码整洁之道》 - ISBN: 978-0-13-235088-4
       这是一本关于编写清晰、可维护代码的经典著作。
    
    2. 《程序员修炼之道》
       ISBN-13: 9780201616224
       从初学者到专家的修炼指南。
    
    3. 经典旧版: 0-306-40615-2
       某领域的经典教材。
    
    4. 其他书籍: 979-10-91146-13-5 (欧洲书籍)
       注意：以979开头的ISBN-13无法转换为ISBN-10。
    
    购买链接: https://example.com/books?isbn=9780306406157
    """
    
    let extracted = ISBNUtils.extract(from: webpageContent)
    
    print("\n提取到 \(extracted.count) 个有效 ISBN:")
    for isbn in extracted {
        print("  📖 \(isbn.formatted)")
        
        // 尝试转换为另一种格式
        switch isbn.type {
        case .isbn10:
            if case .success(let isbn13) = ISBNUtils.toISBN13(isbn.digits) {
                print("      → ISBN-13: \(ISBNUtils.formatISBN13(isbn13))")
            }
        case .isbn13:
            if case .success(let isbn10) = ISBNUtils.toISBN10(isbn.digits) {
                print("      → ISBN-10: \(ISBNUtils.formatISBN10(isbn10))")
            }
        }
    }
}

// MARK: - 示例 4: 生成测试数据

func example4_GenerateTestData() {
    print("\n" + "=" * 50)
    print("示例 4: 生成测试用 ISBN 数据")
    print("=" * 50)
    
    print("\n生成 10 个随机 ISBN-13:")
    for i in 1...10 {
        let isbn = ISBNUtils.generateRandomISBN13()
        print("  \(i). \(ISBNUtils.formatISBN13(isbn))")
    }
    
    print("\n生成 10 个随机 ISBN-10:")
    for i in 1...10 {
        let isbn = ISBNUtils.generateRandomISBN10()
        print("  \(i). \(ISBNUtils.formatISBN10(isbn))")
    }
}

// MARK: - 示例 5: 用户输入处理

func example5_UserInputHandling() {
    print("\n" + "=" * 50)
    print("示例 5: 处理各种格式的用户输入")
    print("=" * 50)
    
    let userInputs = [
        "9780306406157",           // 纯数字
        "978-0-306-40615-7",      // 带连字符
        "978 0 306 40615 7",       // 带空格
        "ISBN 978-0-306-40615-7",  // 带前缀
        "0-306-40615-2",          // ISBN-10 格式
        "0306406152",             // ISBN-10 纯数字
    ]
    
    print("\n处理各种用户输入:")
    for input in userInputs {
        print("\n输入: '\(input)'")
        
        switch ISBNUtils.validate(input) {
        case .success(let isbn):
            print("  ✅ 有效 ISBN")
            print("  类型: \(isbn.type)")
            print("  标准格式: \(isbn.formatted)")
            print("  纯数字: \(isbn.digits)")
            
        case .failure(let error):
            print("  ❌ 无效: \(error.localizedDescription)")
        }
    }
}

// MARK: - 示例 6: 扫描验证场景

struct ScanResult {
    let rawValue: String
    let isValid: Bool
    let isbn: ISBN?
    let error: String?
}

func example6_BatchValidation() {
    print("\n" + "=" * 50)
    print("示例 6: 批量扫描验证")
    print("=" * 50)
    
    let scannedCodes = [
        "9780306406157",  // 有效
        "9780306406158",  // 无效校验位
        "12345",          // 太短
        "9780132350884",  // 有效
        "080442957X",     // 有效带X
        "ABCDEFGHIJ",     // 无效格式
    ]
    
    var results: [(raw: String, valid: Bool, message: String)] = []
    
    for code in scannedCodes {
        switch ISBNUtils.validate(code) {
        case .success(let isbn):
            results.append((code, true, "\(isbn.formatted) - 有效"))
        case .failure(let error):
            results.append((code, false, error.localizedDescription))
        }
    }
    
    print("\n扫描结果:")
    print("-" * 50)
    print(String(format: "%-20s | %-6s | %@", "条码", "状态", "信息"))
    print("-" * 50)
    
    for result in results {
        let status = result.valid ? "✅" : "❌"
        print(String(format: "%-20s |   %@   | %@", result.raw, status, result.message))
    }
    
    let validCount = results.filter { $0.valid }.count
    print("-" * 50)
    print("总计: \(results.count) 个条码，\(validCount) 个有效")
}

// MARK: - 示例 7: ISBN 数据清理

func example7_DataCleanup() {
    print("\n" + "=" * 50)
    print("示例 7: ISBN 数据库记录清理")
    print("=" * 50)
    
    struct BookRecord {
        var title: String
        var isbn10: String?
        var isbn13: String?
    }
    
    var records = [
        BookRecord(title: "书籍A", isbn10: "0306406152", isbn13: nil),
        BookRecord(title: "书籍B", isbn10: "0-13-235088-4", isbn13: "978-0-13-235088-4"),
        BookRecord(title: "书籍C", isbn10: nil, isbn13: "9780201616224"),
        BookRecord(title: "书籍D", isbn10: "080442957X", isbn13: nil),
    ]
    
    print("\n清理前:")
    for record in records {
        print("  \(record.title): ISBN-10=\(record.isbn10 ?? "无"), ISBN-13=\(record.isbn13 ?? "无")")
    }
    
    print("\n清理和补全中...")
    for i in 0..<records.count {
        // 补全 ISBN-10
        if records[i].isbn10 == nil, let isbn13 = records[i].isbn13 {
            if case .success(let isbn10) = ISBNUtils.toISBN10(isbn13) {
                records[i].isbn10 = isbn10
                print("  为 '\(records[i].title)' 补全 ISBN-10: \(isbn10)")
            }
        }
        
        // 补全 ISBN-13
        if records[i].isbn13 == nil, let isbn10 = records[i].isbn10 {
            if case .success(let isbn13) = ISBNUtils.toISBN13(isbn10) {
                records[i].isbn13 = isbn13
                print("  为 '\(records[i].title)' 补全 ISBN-13: \(isbn13)")
            }
        }
        
        // 标准化格式
        if let isbn10 = records[i].isbn10 {
            records[i].isbn10 = ISBNUtils.validate(isbn10).map { $0.digits } ?? isbn10
        }
        if let isbn13 = records[i].isbn13 {
            records[i].isbn13 = ISBNUtils.validate(isbn13).map { $0.digits } ?? isbn13
        }
    }
    
    print("\n清理后:")
    for record in records {
        let formatted10 = records.first?.isbn10.flatMap { ISBNUtils.formatISBN10($0) } ?? "无"
        let formatted13 = record.isbn13.flatMap { ISBNUtils.formatISBN13($0) } ?? "无"
        print("  \(record.title):")
        print("    ISBN-10: \(record.isbn10 ?? "无") (\(formatted10))")
        print("    ISBN-13: \(record.isbn13 ?? "无") (\(formatted13))")
    }
}

// MARK: - 运行所有示例

func runAllExamples() {
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " ISBN Utils 实用示例 ".center(48) + "║")
    print("╚" + "=" * 48 + "╝")
    
    example1_BookManagement()
    example2_BatchConversion()
    example3_ExtractFromText()
    example4_GenerateTestData()
    example5_UserInputHandling()
    example6_BatchValidation()
    example7_DataCleanup()
    
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " 所有示例运行完成 ".center(48) + "║")
    print("╚" + "=" * 48 + "╝")
}

// Helper Extensions
extension String {
    static func * (left: String, right: Int) -> String {
        return String(repeating: left, count: right)
    }
    
    func center(_ length: Int) -> String {
        let padding = length - self.count
        guard padding > 0 else { return self }
        let leftPad = padding / 2
        let rightPad = padding - leftPad
        return String(repeating: " ", count: leftPad) + self + String(repeating: " ", count: rightPad)
    }
}

// 运行示例
runAllExamples()