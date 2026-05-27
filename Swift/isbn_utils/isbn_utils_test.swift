/**
 ISBN Utils Tests - ISBN 工具库测试
 
 运行方式: swift isbn_utils_test.swift
 */

import Foundation

// 导入 mod.swift 中的代码
// 在实际项目中，这应该是一个 import 语句

// MARK: - Test Framework

struct TestRunner {
    var passed = 0
    var failed = 0
    var total = 0
    
    mutating func runTest(_ name: String, _ test: () -> Bool) {
        total += 1
        if test() {
            passed += 1
            print("✅ \(name)")
        } else {
            failed += 1
            print("❌ \(name)")
        }
    }
    
    mutating func runTestThrows(_ name: String, _ test: () throws -> Bool) {
        total += 1
        do {
            if try test() {
                passed += 1
                print("✅ \(name)")
            } else {
                failed += 1
                print("❌ \(name)")
            }
        } catch {
            failed += 1
            print("❌ \(name) - 抛出异常: \(error)")
        }
    }
    
    func printSummary() {
        print("\n" + String(repeating: "=", count: 50))
        print("测试结果: \(passed)/\(total) 通过")
        if failed > 0 {
            print("⚠️  \(failed) 个测试失败")
        } else {
            print("🎉 所有测试通过!")
        }
        print(String(repeating: "=", count: 50))
    }
}

// MARK: - Copy ISBN Utils Implementation (for standalone test)

public enum ISBNType {
    case isbn10
    case isbn13
}

public enum ISBNError: Error, LocalizedError {
    case invalidFormat
    case invalidCheckDigit(expected: Character, actual: Character)
    case invalidLength
    case conversionError
    
    public var errorDescription: String? {
        switch self {
        case .invalidFormat:
            return "无效的 ISBN 格式"
        case .invalidCheckDigit(let expected, let actual):
            return "校验位错误：期望 \(expected)，实际 \(actual)"
        case .invalidLength:
            return "ISBN 长度无效"
        case .conversionError:
            return "ISBN 转换错误"
        }
    }
}

public enum ISBN {
    case isbn10(String)
    case isbn13(String)
    
    public var digits: String {
        switch self {
        case .isbn10(let s), .isbn13(let s):
            return s
        }
    }
    
    public var type: ISBNType {
        switch self {
        case .isbn10:
            return .isbn10
        case .isbn13:
            return .isbn13
        }
    }
    
    public var formatted: String {
        switch self {
        case .isbn10(let s):
            return ISBNUtils.formatISBN10(s)
        case .isbn13(let s):
            return ISBNUtils.formatISBN13(s)
        }
    }
}

public struct ISBNUtils {
    
    public static func validate(_ isbn: String) -> Result<ISBN, ISBNError> {
        let cleaned = isbn.uppercased().filter { $0.isNumber || $0 == "X" }
        
        if cleaned.count == 10 {
            return validateISBN10(cleaned)
        } else if cleaned.count == 13 {
            return validateISBN13(cleaned)
        } else {
            return .failure(.invalidLength)
        }
    }
    
    public static func validateISBN10(_ isbn: String) -> Result<ISBN, ISBNError> {
        let cleaned = isbn.uppercased().filter { $0.isNumber || $0 == "X" }
        
        guard cleaned.count == 10 else {
            return .failure(.invalidLength)
        }
        
        let chars = Array(cleaned)
        var sum = 0
        
        for i in 0..<9 {
            guard let digit = chars[i].wholeNumberValue else {
                return .failure(.invalidFormat)
            }
            sum += digit * (10 - i)
        }
        
        let lastChar = chars[9]
        let lastDigit: Int
        if lastChar == "X" {
            lastDigit = 10
        } else if let d = lastChar.wholeNumberValue {
            lastDigit = d
        } else {
            return .failure(.invalidFormat)
        }
        sum += lastDigit
        
        let isValid = sum % 11 == 0
        
        if isValid {
            return .success(.isbn10(cleaned))
        } else {
            let expected = calculateISBN10CheckDigit(String(cleaned.prefix(9)))
            return .failure(.invalidCheckDigit(expected: expected, actual: lastChar))
        }
    }
    
    public static func validateISBN13(_ isbn: String) -> Result<ISBN, ISBNError> {
        let cleaned = isbn.filter { $0.isNumber }
        
        guard cleaned.count == 13 else {
            return .failure(.invalidLength)
        }
        
        let chars = Array(cleaned)
        var sum = 0
        
        for i in 0..<12 {
            guard let digit = chars[i].wholeNumberValue else {
                return .failure(.invalidFormat)
            }
            sum += digit * (i % 2 == 0 ? 1 : 3)
        }
        
        guard let lastDigit = chars[12].wholeNumberValue else {
            return .failure(.invalidFormat)
        }
        
        let checkDigit = (10 - (sum % 10)) % 10
        let isValid = checkDigit == lastDigit
        
        if isValid {
            return .success(.isbn13(cleaned))
        } else {
            let expected = Character("\(checkDigit)")
            return .failure(.invalidCheckDigit(expected: expected, actual: chars[12]))
        }
    }
    
    public static func calculateISBN10CheckDigit(_ prefix: String) -> Character {
        let cleaned = prefix.filter { $0.isNumber }
        guard cleaned.count == 9 else {
            return "?"
        }
        
        let chars = Array(cleaned)
        var sum = 0
        
        for i in 0..<9 {
            if let digit = chars[i].wholeNumberValue {
                sum += digit * (10 - i)
            }
        }
        
        let remainder = sum % 11
        let checkDigit = (11 - remainder) % 11
        
        if checkDigit == 10 {
            return "X"
        } else {
            return Character("\(checkDigit)")
        }
    }
    
    public static func calculateISBN13CheckDigit(_ prefix: String) -> Character {
        let cleaned = prefix.filter { $0.isNumber }
        guard cleaned.count == 12 else {
            return "?"
        }
        
        let chars = Array(cleaned)
        var sum = 0
        
        for i in 0..<12 {
            if let digit = chars[i].wholeNumberValue {
                sum += digit * (i % 2 == 0 ? 1 : 3)
            }
        }
        
        let checkDigit = (10 - (sum % 10)) % 10
        return Character("\(checkDigit)")
    }
    
    public static func toISBN13(_ isbn10: String) -> Result<String, ISBNError> {
        let result = validateISBN10(isbn10)
        
        switch result {
        case .success(let isbn):
            let digits = isbn.digits
            let prefix = "978" + String(digits.prefix(9))
            let checkDigit = calculateISBN13CheckDigit(prefix)
            return .success(prefix + String(checkDigit))
        case .failure(let error):
            return .failure(error)
        }
    }
    
    public static func toISBN10(_ isbn13: String) -> Result<String, ISBNError> {
        let result = validateISBN13(isbn13)
        
        switch result {
        case .success(let isbn):
            let digits = isbn.digits
            guard digits.hasPrefix("978") else {
                return .failure(.conversionError)
            }
            let prefix = String(digits.dropFirst(3).prefix(9))
            let checkDigit = calculateISBN10CheckDigit(prefix)
            return .success(prefix + String(checkDigit))
        case .failure(let error):
            return .failure(error)
        }
    }
    
    public static func extract(from text: String) -> [ISBN] {
        var results: [ISBN] = []
        
        let isbn13Pattern = #"97[89][0-9]{10}"#
        if let regex13 = try? NSRegularExpression(pattern: isbn13Pattern) {
            let range = NSRange(text.startIndex..., in: text)
            let matches = regex13.matches(in: text, range: range)
            
            for match in matches {
                if let matchRange = Range(match.range, in: text) {
                    let candidate = String(text[matchRange])
                    if case .success(let isbn) = validateISBN13(candidate) {
                        results.append(isbn)
                    }
                }
            }
        }
        
        let isbn10Pattern = #"[0-9]{9}[0-9Xx]"#
        if let regex10 = try? NSRegularExpression(pattern: isbn10Pattern) {
            let range = NSRange(text.startIndex..., in: text)
            let matches = regex10.matches(in: text, range: range)
            
            for match in matches {
                if let matchRange = Range(match.range, in: text) {
                    let candidate = String(text[matchRange])
                    let isAlreadyFound = results.contains { existing in
                        candidate == existing.digits
                    }
                    if !isAlreadyFound {
                        if case .success(let isbn) = validateISBN10(candidate) {
                            results.append(isbn)
                        }
                    }
                }
            }
        }
        
        return results
    }
    
    public static func formatISBN10(_ isbn: String) -> String {
        let cleaned = isbn.uppercased().filter { $0.isNumber || $0 == "X" }
        guard cleaned.count == 10 else { return isbn }
        
        let chars = Array(cleaned)
        return "\(chars[0])-\(chars[1])\(chars[2])\(chars[3])\(chars[4])\(chars[5])-\(chars[6])\(chars[7])\(chars[8])-\(chars[9])"
    }
    
    public static func formatISBN13(_ isbn: String) -> String {
        let cleaned = isbn.filter { $0.isNumber }
        guard cleaned.count == 13 else { return isbn }
        
        let chars = Array(cleaned)
        return "\(chars[0])\(chars[1])\(chars[2])-\(chars[3])\(chars[4])\(chars[5])\(chars[6])\(chars[7])\(chars[8])\(chars[9])\(chars[10])\(chars[11])-\(chars[12])"
    }
    
    public static func generateRandomISBN13() -> String {
        let prefix = Bool.random() ? "978" : "979"
        
        var randomDigits = prefix
        for _ in 0..<9 {
            randomDigits += "\(Int.random(in: 0...9))"
        }
        
        let checkDigit = calculateISBN13CheckDigit(randomDigits)
        return randomDigits + String(checkDigit)
    }
    
    public static func generateRandomISBN10() -> String {
        var randomDigits = ""
        for _ in 0..<9 {
            randomDigits += "\(Int.random(in: 0...9))"
        }
        
        let checkDigit = calculateISBN10CheckDigit(randomDigits)
        return randomDigits + String(checkDigit)
    }
}

extension String {
    var isValidISBN: Bool {
        if case .success = ISBNUtils.validate(self) {
            return true
        }
        return false
    }
    
    var formattedISBN: String {
        if case .success(let isbn) = ISBNUtils.validate(self) {
            return isbn.formatted
        }
        return self
    }
}

// MARK: - Tests

var tests = TestRunner()

print("=" * 60)
print("ISBN Utils 单元测试")
print("=" * 60)
print("")

// ============= ISBN-10 验证测试 =============
print("【ISBN-10 验证测试】")

tests.runTest("验证有效 ISBN-10: 0306406152") {
    if case .success(let isbn) = ISBNUtils.validate("0306406152") {
        return isbn.digits == "0306406152"
    }
    return false
}

tests.runTest("验证有效 ISBN-10 带X: 080442957X") {
    if case .success(let isbn) = ISBNUtils.validate("080442957X") {
        return isbn.digits == "080442957X"
    }
    return false
}

tests.runTest("验证有效 ISBN-10 带小写x: 080442957x") {
    if case .success(let isbn) = ISBNUtils.validate("080442957x") {
        return isbn.digits == "080442957X"  // 应该大写
    }
    return false
}

tests.runTest("验证带分隔符的 ISBN-10") {
    if case .success(let isbn) = ISBNUtils.validate("0-306-40615-2") {
        return isbn.digits == "0306406152"
    }
    return false
}

tests.runTest("拒绝无效校验位的 ISBN-10") {
    if case .failure = ISBNUtils.validate("0306406153") {
        return true
    }
    return false
}

tests.runTest("拒绝长度错误的 ISBN-10") {
    if case .failure(.invalidLength) = ISBNUtils.validate("123456789") {
        return true
    }
    return false
}

// ============= ISBN-13 验证测试 =============
print("\n【ISBN-13 验证测试】")

tests.runTest("验证有效 ISBN-13: 9780306406157") {
    if case .success(let isbn) = ISBNUtils.validate("9780306406157") {
        return isbn.digits == "9780306406157"
    }
    return false
}

tests.runTest("验证有效 ISBN-13: 9780132350884") {
    if case .success(let isbn) = ISBNUtils.validate("9780132350884") {
        return isbn.digits == "9780132350884"
    }
    return false
}

tests.runTest("验证带分隔符的 ISBN-13") {
    if case .success(let isbn) = ISBNUtils.validate("978-0-13-235088-4") {
        return isbn.digits == "9780132350884"
    }
    return false
}

tests.runTest("拒绝无效校验位的 ISBN-13") {
    if case .failure = ISBNUtils.validate("9780306406158") {
        return true
    }
    return false
}

tests.runTest("拒绝长度错误的 ISBN-13") {
    if case .failure(.invalidLength) = ISBNUtils.validate("978030640615") {
        return true
    }
    return false
}

// ============= 校验位计算测试 =============
print("\n【校验位计算测试】")

tests.runTest("计算 ISBN-10 校验位 (普通数字)") {
    return ISBNUtils.calculateISBN10CheckDigit("030640615") == "2"
}

tests.runTest("计算 ISBN-10 校验位 (结果为X)") {
    return ISBNUtils.calculateISBN10CheckDigit("080442957") == "X"
}

tests.runTest("计算 ISBN-13 校验位") {
    return ISBNUtils.calculateISBN13CheckDigit("978030640615") == "7"
}

tests.runTest("计算 ISBN-13 校验位 (另一个值)") {
    return ISBNUtils.calculateISBN13CheckDigit("978013235088") == "4"
}

// ============= 转换测试 =============
print("\n【转换测试】")

tests.runTest("ISBN-10 转 ISBN-13") {
    if case .success(let result) = ISBNUtils.toISBN13("0306406152") {
        return result == "9780306406157"
    }
    return false
}

tests.runTest("ISBN-13 转 ISBN-10") {
    if case .success(let result) = ISBNUtils.toISBN10("9780306406157") {
        return result == "0306406152"
    }
    return false
}

tests.runTest("ISBN-10 带 X 转 ISBN-13") {
    if case .success(let result) = ISBNUtils.toISBN13("080442957X") {
        return result == "9780804429577"
    }
    return false
}

tests.runTest("不能转换以 979 开头的 ISBN-13") {
    if case .failure(.conversionError) = ISBNUtils.toISBN10("9791091146135") {
        return true
    }
    return false
}

tests.runTest("双向转换一致性") {
    let originalISBN10 = "0132350884"
    if case .success(let isbn13) = ISBNUtils.toISBN13(originalISBN10) {
        if case .success(let backToISBN10) = ISBNUtils.toISBN10(isbn13) {
            return backToISBN10 == originalISBN10
        }
    }
    return false
}

// ============= 格式化测试 =============
print("\n【格式化测试】")

tests.runTest("格式化 ISBN-10") {
    let formatted = ISBNUtils.formatISBN10("0306406152")
    return formatted == "0-30640-615-2"
}

tests.runTest("格式化 ISBN-10 带X") {
    let formatted = ISBNUtils.formatISBN10("080442957X")
    return formatted == "0-80442-957-X"
}

tests.runTest("格式化 ISBN-13") {
    let formatted = ISBNUtils.formatISBN13("9780306406157")
    return formatted == "978-030640615-7"
}

// ============= 提取测试 =============
print("\n【提取测试】")

tests.runTest("从文本提取 ISBN") {
    let text = "书籍 ISBN: 9780306406157 和 0306406152"
    let extracted = ISBNUtils.extract(from: text)
    return extracted.count == 2
}

tests.runTest("提取正确的 ISBN 类型") {
    let text = "9780306406157"
    let extracted = ISBNUtils.extract(from: text)
    if extracted.count == 1, case .isbn13 = extracted[0] {
        return true
    }
    return false
}

tests.runTest("忽略无效 ISBN") {
    let text = "1234567890"  // 无效的 ISBN
    let extracted = ISBNUtils.extract(from: text)
    return extracted.isEmpty
}

// ============= 随机生成测试 =============
print("\n【随机生成测试】")

tests.runTest("生成有效的随机 ISBN-13") {
    let randomISBN = ISBNUtils.generateRandomISBN13()
    if case .success = ISBNUtils.validateISBN13(randomISBN) {
        return true
    }
    return false
}

tests.runTest("生成有效的随机 ISBN-10") {
    let randomISBN = ISBNUtils.generateRandomISBN10()
    if case .success = ISBNUtils.validateISBN10(randomISBN) {
        return true
    }
    return false
}

tests.runTest("随机 ISBN-13 长度正确") {
    let randomISBN = ISBNUtils.generateRandomISBN13()
    return randomISBN.count == 13
}

tests.runTest("随机 ISBN-10 长度正确") {
    let randomISBN = ISBNUtils.generateRandomISBN10()
    return randomISBN.count == 10
}

// ============= String 扩展测试 =============
print("\n【String 扩展测试】")

tests.runTest("String.isValidISBN 扩展") {
    return "9780306406157".isValidISBN && !"invalid".isValidISBN
}

tests.runTest("String.formattedISBN 扩展") {
    return "9780306406157".formattedISBN == "978-030640615-7"
}

// ============= 边界情况测试 =============
print("\n【边界情况测试】")

tests.runTest("空字符串处理") {
    if case .failure(.invalidLength) = ISBNUtils.validate("") {
        return true
    }
    return false
}

tests.runTest("只有分隔符的字符串") {
    if case .failure(.invalidLength) = ISBNUtils.validate("---") {
        return true
    }
    return false
}

tests.runTest("包含空格的 ISBN") {
    if case .success(let isbn) = ISBNUtils.validate(" 0 3 0 6 4 0 6 1 5 2 ") {
        return isbn.digits == "0306406152"
    }
    return false
}

tests.runTest("校验位为 0 的情况") {
    // ISBN-10: 校验位可以是 0
    // 测试一个校验位为 0 的有效 ISBN-10
    if case .success = ISBNUtils.validate("0140449130") {
        return true
    }
    return false
}

// 打印测试结果
tests.printSummary()

// 执行示例
print("\n")
runISBNUtilsExamples()

// MARK: - Example Function (from mod.swift)

func runISBNUtilsExamples() {
    print("=" * 60)
    print("ISBN Utils - ISBN 工具库示例")
    print("=" * 60)
    
    let testISBN10 = "0306406152"
    let testISBN13 = "9780306406157"
    let testISBN10X = "080442957X"
    
    print("\n【验证测试】")
    print("-" * 40)
    
    switch ISBNUtils.validate(testISBN10) {
    case .success(let isbn):
        print("✅ ISBN-10 '\(testISBN10)' 验证通过")
        print("   类型: \(isbn.type)")
        print("   格式化: \(isbn.formatted)")
    case .failure(let error):
        print("❌ 验证失败: \(error.localizedDescription)")
    }
    
    switch ISBNUtils.validate(testISBN13) {
    case .success(let isbn):
        print("✅ ISBN-13 '\(testISBN13)' 验证通过")
        print("   类型: \(isbn.type)")
        print("   格式化: \(isbn.formatted)")
    case .failure(let error):
        print("❌ 验证失败: \(error.localizedDescription)")
    }
    
    switch ISBNUtils.validate(testISBN10X) {
    case .success(let isbn):
        print("✅ ISBN-10 '\(testISBN10X)' 验证通过（带X校验位）")
        print("   格式化: \(isbn.formatted)")
    case .failure(let error):
        print("❌ 验证失败: \(error.localizedDescription)")
    }
    
    let invalidISBN = "1234567890"
    switch ISBNUtils.validate(invalidISBN) {
    case .success(let isbn):
        print("❌ 意外通过: \(isbn.digits)")
    case .failure(let error):
        print("✅ 正确识别无效 ISBN: \(error.localizedDescription)")
    }
    
    print("\n【校验位计算】")
    print("-" * 40)
    
    let prefix10 = "030640615"
    let checkDigit10 = ISBNUtils.calculateISBN10CheckDigit(prefix10)
    print("ISBN-10 '\(prefix10)' 的校验位: \(checkDigit10)")
    
    let prefix13 = "978030640615"
    let checkDigit13 = ISBNUtils.calculateISBN13CheckDigit(prefix13)
    print("ISBN-13 '\(prefix13)' 的校验位: \(checkDigit13)")
    
    print("\n【转换测试】")
    print("-" * 40)
    
    switch ISBNUtils.toISBN13(testISBN10) {
    case .success(let isbn13Result):
        print("ISBN-10 '\(testISBN10)' → ISBN-13: \(isbn13Result)")
    case .failure(let error):
        print("转换失败: \(error.localizedDescription)")
    }
    
    switch ISBNUtils.toISBN10(testISBN13) {
    case .success(let isbn10Result):
        print("ISBN-13 '\(testISBN13)' → ISBN-10: \(isbn10Result)")
    case .failure(let error):
        print("转换失败: \(error.localizedDescription)")
    }
    
    let isbn979 = "9791091146135"
    switch ISBNUtils.toISBN10(isbn979) {
    case .success(let result):
        print("❌ 意外转换成功: \(result)")
    case .failure:
        print("✅ 正确识别不可转换的 ISBN-13（以979开头）")
    }
    
    print("\n【从文本提取】")
    print("-" * 40)
    
    let sampleText = """
    我最近在读几本书：
    - ISBN-10: 0306406152
    - ISBN-13: 978-0-13-235088-4 (Clean Code)
    - 还有一本 978-1-59327-584-6
    带X的: 0-8044-2957-X
    
    一些随机文本中可能包含 9780306406157 这样的号码。
    """
    
    let extracted = ISBNUtils.extract(from: sampleText)
    print("从文本中提取到 \(extracted.count) 个 ISBN:")
    for isbn in extracted {
        print("  - \(isbn.formatted) (\(isbn.type))")
    }
    
    print("\n【随机生成】")
    print("-" * 40)
    
    for _ in 0..<3 {
        let randomISBN13 = ISBNUtils.generateRandomISBN13()
        print("随机 ISBN-13: \(ISBNUtils.formatISBN13(randomISBN13))")
    }
    
    for _ in 0..<3 {
        let randomISBN10 = ISBNUtils.generateRandomISBN10()
        print("随机 ISBN-10: \(ISBNUtils.formatISBN10(randomISBN10))")
    }
    
    print("\n【String 扩展】")
    print("-" * 40)
    
    let testStr = "9780306406157"
    print("'\(testStr)' isValidISBN: \(testStr.isValidISBN)")
    print("'\(testStr)' formatted: \(testStr.formattedISBN)")
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)
}

extension String {
    static func * (left: String, right: Int) -> String {
        return String(repeating: left, count: right)
    }
}