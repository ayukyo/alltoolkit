/**
 ISBN Utils - ISBN-10 和 ISBN-13 验证、转换、校验位计算工具
 
 功能：
 - 验证 ISBN-10 和 ISBN-13 格式
 - 计算校验位
 - ISBN-10 与 ISBN-13 相互转换
 - 从字符串中提取 ISBN
 - 格式化 ISBN 显示
 
 零外部依赖，纯 Swift 标准库实现
 */

import Foundation

// MARK: - ISBN Types

/// ISBN 类型枚举
public enum ISBNType {
    case isbn10
    case isbn13
}

/// ISBN 错误类型
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

/// ISBN 结果类型
public enum ISBN {
    case isbn10(String)
    case isbn13(String)
    
    /// 获取 ISBN 字符串（无分隔符）
    public var digits: String {
        switch self {
        case .isbn10(let s), .isbn13(let s):
            return s
        }
    }
    
    /// 获取 ISBN 类型
    public var type: ISBNType {
        switch self {
        case .isbn10:
            return .isbn10
        case .isbn13:
            return .isbn13
        }
    }
    
    /// 格式化显示（带连字符）
    public var formatted: String {
        switch self {
        case .isbn10(let s):
            return ISBNUtils.formatISBN10(s)
        case .isbn13(let s):
            return ISBNUtils.formatISBN13(s)
        }
    }
}

// MARK: - ISBN Utils

/// ISBN 工具类
public struct ISBNUtils {
    
    // MARK: - 验证
    
    /// 验证 ISBN 字符串
    /// - Parameter isbn: ISBN 字符串（可包含分隔符）
    /// - Returns: ISBN 结果或错误
    public static func validate(_ isbn: String) -> Result<ISBN, ISBNError> {
        // 清理字符串：移除所有非数字和 X 字符
        let cleaned = isbn.uppercased().filter { $0.isNumber || $0 == "X" }
        
        if cleaned.count == 10 {
            return validateISBN10(cleaned)
        } else if cleaned.count == 13 {
            return validateISBN13(cleaned)
        } else {
            return .failure(.invalidLength)
        }
    }
    
    /// 验证 ISBN-10
    /// - Parameter isbn: 10位 ISBN 字符串
    /// - Returns: 验证结果
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
        
        // 最后一位可以是 X（代表10）
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
    
    /// 验证 ISBN-13
    /// - Parameter isbn: 13位 ISBN 字符串
    /// - Returns: 验证结果
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
    
    // MARK: - 校验位计算
    
    /// 计算 ISBN-10 校验位
    /// - Parameter prefix: 前9位数字
    /// - Returns: 校验位字符（0-9 或 X）
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
    
    /// 计算 ISBN-13 校验位
    /// - Parameter prefix: 前12位数字
    /// - Returns: 校验位字符（0-9）
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
    
    // MARK: - 转换
    
    /// 将 ISBN-10 转换为 ISBN-13
    /// - Parameter isbn10: ISBN-10 字符串
    /// - Returns: ISBN-13 字符串或错误
    public static func toISBN13(_ isbn10: String) -> Result<String, ISBNError> {
        let result = validateISBN10(isbn10)
        
        switch result {
        case .success(let isbn):
            let digits = isbn.digits
            // ISBN-13 以 978 开头
            let prefix = "978" + String(digits.prefix(9))
            let checkDigit = calculateISBN13CheckDigit(prefix)
            return .success(prefix + String(checkDigit))
        case .failure(let error):
            return .failure(error)
        }
    }
    
    /// 将 ISBN-13 转换为 ISBN-10
    /// - Parameter isbn13: ISBN-13 字符串
    /// - Returns: ISBN-10 字符串或错误
    /// - Note: 只有以 978 开头的 ISBN-13 才能转换为 ISBN-10
    public static func toISBN10(_ isbn13: String) -> Result<String, ISBNError> {
        let result = validateISBN13(isbn13)
        
        switch result {
        case .success(let isbn):
            let digits = isbn.digits
            // 只有以 978 开头的 ISBN-13 可以转换
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
    
    // MARK: - 提取
    
    /// 从文本中提取所有 ISBN
    /// - Parameter text: 输入文本
    /// - Returns: 找到的 ISBN 列表
    public static func extract(from text: String) -> [ISBN] {
        var results: [ISBN] = []
        
        // 匹配 ISBN-10 和 ISBN-13 的正则模式
        // ISBN-10: 10位数字，最后一位可以是 X
        // ISBN-13: 13位数字，以 978 或 979 开头
        
        // 先尝试匹配 ISBN-13
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
        
        // 再匹配 ISBN-10
        let isbn10Pattern = #"[0-9]{9}[0-9Xx]"#
        if let regex10 = try? NSRegularExpression(pattern: isbn10Pattern) {
            let range = NSRange(text.startIndex..., in: text)
            let matches = regex10.matches(in: text, range: range)
            
            for match in matches {
                if let matchRange = Range(match.range, in: text) {
                    let candidate = String(text[matchRange])
                    // 跳过已经被识别为 ISBN-13 的部分
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
    
    // MARK: - 格式化
    
    /// 格式化 ISBN-10（带连字符）
    /// - Parameter isbn: ISBN-10 数字字符串
    /// - Returns: 格式化后的字符串
    public static func formatISBN10(_ isbn: String) -> String {
        let cleaned = isbn.uppercased().filter { $0.isNumber || $0 == "X" }
        guard cleaned.count == 10 else { return isbn }
        
        // ISBN-10 格式: X-XXXXX-XXX-X
        let chars = Array(cleaned)
        return "\(chars[0])-\(chars[1])\(chars[2])\(chars[3])\(chars[4])\(chars[5])-\(chars[6])\(chars[7])\(chars[8])-\(chars[9])"
    }
    
    /// 格式化 ISBN-13（带连字符）
    /// - Parameter isbn: ISBN-13 数字字符串
    /// - Returns: 格式化后的字符串
    public static func formatISBN13(_ isbn: String) -> String {
        let cleaned = isbn.filter { $0.isNumber }
        guard cleaned.count == 13 else { return isbn }
        
        // ISBN-13 格式: XXX-X-XXXXX-XXX-X (EAN 前缀-组号-出版社号-书序号-校验码)
        // 简化格式: XXX-XXXXXXXXXX
        let chars = Array(cleaned)
        return "\(chars[0])\(chars[1])\(chars[2])-\(chars[3])\(chars[4])\(chars[5])\(chars[6])\(chars[7])\(chars[8])\(chars[9])\(chars[10])\(chars[11])-\(chars[12])"
    }
    
    /// 生成随机 ISBN-13
    /// - Returns: 随机生成的有效 ISBN-13
    public static func generateRandomISBN13() -> String {
        // 以 978 或 979 开头
        let prefix = Bool.random() ? "978" : "979"
        
        // 生成9位随机数字
        var randomDigits = prefix
        for _ in 0..<9 {
            randomDigits += "\(Int.random(in: 0...9))"
        }
        
        let checkDigit = calculateISBN13CheckDigit(randomDigits)
        return randomDigits + String(checkDigit)
    }
    
    /// 生成随机 ISBN-10
    /// - Returns: 随机生成的有效 ISBN-10
    public static func generateRandomISBN10() -> String {
        // 生成9位随机数字
        var randomDigits = ""
        for _ in 0..<9 {
            randomDigits += "\(Int.random(in: 0...9))"
        }
        
        let checkDigit = calculateISBN10CheckDigit(randomDigits)
        return randomDigits + String(checkDigit)
    }
}

// MARK: - Convenience Extensions

extension String {
    /// 检查字符串是否为有效的 ISBN
    public var isValidISBN: Bool {
        if case .success = ISBNUtils.validate(self) {
            return true
        }
        return false
    }
    
    /// 获取格式化的 ISBN
    public var formattedISBN: String {
        if case .success(let isbn) = ISBNUtils.validate(self) {
            return isbn.formatted
        }
        return self
    }
}

// MARK: - Usage Example (run directly)

/// 运行示例
public func runISBNUtilsExamples() {
    print("=" * 60)
    print("ISBN Utils - ISBN 工具库示例")
    print("=" * 60)
    
    // 示例 ISBN
    let testISBN10 = "0306406152"      // 有效的 ISBN-10
    let testISBN13 = "9780306406157"   // 对应的 ISBN-13
    let testISBN10X = "080442957X"     // 以 X 结尾的 ISBN-10
    
    print("\n【验证测试】")
    print("-" * 40)
    
    // 验证 ISBN-10
    switch ISBNUtils.validate(testISBN10) {
    case .success(let isbn):
        print("✅ ISBN-10 '\(testISBN10)' 验证通过")
        print("   类型: \(isbn.type)")
        print("   格式化: \(isbn.formatted)")
    case .failure(let error):
        print("❌ 验证失败: \(error.localizedDescription)")
    }
    
    // 验证 ISBN-13
    switch ISBNUtils.validate(testISBN13) {
    case .success(let isbn):
        print("✅ ISBN-13 '\(testISBN13)' 验证通过")
        print("   类型: \(isbn.type)")
        print("   格式化: \(isbn.formatted)")
    case .failure(let error):
        print("❌ 验证失败: \(error.localizedDescription)")
    }
    
    // 验证带 X 的 ISBN-10
    switch ISBNUtils.validate(testISBN10X) {
    case .success(let isbn):
        print("✅ ISBN-10 '\(testISBN10X)' 验证通过（带X校验位）")
        print("   格式化: \(isbn.formatted)")
    case .failure(let error):
        print("❌ 验证失败: \(error.localizedDescription)")
    }
    
    // 验证无效 ISBN
    let invalidISBN = "1234567890"
    switch ISBNUtils.validate(invalidISBN) {
    case .success(let isbn):
        print("❌ 意外通过: \(isbn.digits)")
    case .failure(let error):
        print("✅ 正确识别无效 ISBN: \(error.localizedDescription)")
    }
    
    print("\n【校验位计算】")
    print("-" * 40)
    
    // 计算校验位
    let prefix10 = "030640615"
    let checkDigit10 = ISBNUtils.calculateISBN10CheckDigit(prefix10)
    print("ISBN-10 '\(prefix10)' 的校验位: \(checkDigit10)")
    
    let prefix13 = "978030640615"
    let checkDigit13 = ISBNUtils.calculateISBN13CheckDigit(prefix13)
    print("ISBN-13 '\(prefix13)' 的校验位: \(checkDigit13)")
    
    print("\n【转换测试】")
    print("-" * 40)
    
    // ISBN-10 -> ISBN-13
    switch ISBNUtils.toISBN13(testISBN10) {
    case .success(let isbn13Result):
        print("ISBN-10 '\(testISBN10)' → ISBN-13: \(isbn13Result)")
    case .failure(let error):
        print("转换失败: \(error.localizedDescription)")
    }
    
    // ISBN-13 -> ISBN-10
    switch ISBNUtils.toISBN10(testISBN13) {
    case .success(let isbn10Result):
        print("ISBN-13 '\(testISBN13)' → ISBN-10: \(isbn10Result)")
    case .failure(let error):
        print("转换失败: \(error.localizedDescription)")
    }
    
    // 不能转换的 ISBN-13（以979开头）
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

// Helper
extension String {
    static func * (left: String, right: Int) -> String {
        return String(repeating: left, count: right)
    }
}