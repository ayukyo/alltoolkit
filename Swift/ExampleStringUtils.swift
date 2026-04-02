/**
 * AllToolkit - Swift StringUtils 使用示例
 *
 * 演示 StringUtils 扩展的各种功能用法
 *
 * 运行方式:
 * 1. 在 Xcode 中创建 Swift 项目
 * 2. 将 StringUtils.swift 和本文件添加到项目中
 * 3. 在需要时 import Foundation
 * 4. 直接调用 String 的扩展方法
 */

import Foundation

// MARK: - 示例运行函数

func runStringUtilsExamples() {
    print("=== Swift StringUtils 使用示例 ===\n")
    
    // MARK: 空值检查
    print("--- 空值检查 ---")
    let emptyStr = ""
    let blankStr = "   "
    let contentStr = "Hello"
    
    print("\"\(emptyStr)\".isBlank = \(emptyStr.isBlank)")      // true
    print("\"\(blankStr)\".isBlank = \(blankStr.isBlank)")      // true
    print("\"\(contentStr)\".isBlank = \(contentStr.isBlank)")  // false
    print("\"\(contentStr)\".isNotBlank = \(contentStr.isNotBlank)")  // true
    print()
    
    // MARK: 子串操作
    print("--- 子串操作 ---")
    let text = "Hello, World!"
    print("原文: \"\(text)\"")
    print("substring(start: 0, end: 5) = \"\(text.substring(start: 0, end: 5))\"")  // "Hello"
    print("substring(from: 7) = \"\(text.substring(from: 7))\"")  // "World!"
    print("substring(to: 5) = \"\(text.substring(to: 5))\"")  // "Hello"
    print("truncate(8) = \"\(text.truncate(8))\"")  // "Hello..."
    print()
    
    // MARK: 空白处理
    print("--- 空白处理 ---")
    let messyText = "  Hello   World  "
    print("原文: \"\(messyText)\"")
    print("trimmed() = \"\(messyText.trimmed())\"")  // "Hello   World"
    print("removeAllWhitespaces() = \"\(messyText.removeAllWhitespaces())\"")  // "HelloWorld"
    print("normalizeWhitespaces() = \"\(messyText.normalizeWhitespaces())\"")  // "Hello World"
    print()
    
    // MARK: 验证方法
    print("--- 验证方法 ---")
    let email = "user@example.com"
    let phone = "13800138000"
    let url = "https://www.example.com"
    let idCard = "110101199001011234"
    let ip = "192.168.1.1"
    
    print("\"\(email)\".isValidEmail = \(email.isValidEmail)")
    print("\"\(phone)\".isValidChinesePhone = \(phone.isValidChinesePhone)")
    print("\"\(url)\".isValidURL = \(url.isValidURL)")
    print("\"12345\".isNumeric = \("12345".isNumeric)")
    print("\"abc\".isAlphabetic = \("abc".isAlphabetic)")
    print("\"abc123\".isAlphanumeric = \("abc123".isAlphanumeric)")
    print("\"\(ip)\".isValidIPv4 = \(ip.isValidIPv4)")
    print()
    
    // MARK: 正则匹配
    print("--- 正则匹配 ---")
    let htmlText = "<p>Hello <b>World</b></p>"
    print("原文: \"\(htmlText)\"")
    print("matches(pattern: \"<[^>]+>\") = \(htmlText.matches(pattern: "<[^>]+>"))")
    print("firstMatch(pattern: \"\\b[A-Z][a-z]+\\b\") = \(htmlText.firstMatch(pattern: "\\b[A-Z][a-z]+\\b") ?? "nil")")
    print("strippingHTML() = \"\(htmlText.strippingHTML())\"")
    print()
    
    // MARK: 编码/解码
    print("--- 编码/解码 ---")
    let rawUrl = "https://example.com/search?q=hello world"
    print("原文: \"\(rawUrl)\"")
    let encoded = rawUrl.urlEncoded()
    print("urlEncoded() = \"\(encoded)\"")
    print("urlDecoded() = \"\(encoded.urlDecoded())\"")
    
    let originalText = "Hello, World!"
    let base64 = originalText.base64Encoded()
    print("\"\(originalText)\".base64Encoded() = \"\(base64)\"")
    print("base64Decoded() = \"\(base64.base64Decoded() ?? "nil")\"")
    print()
    
    // MARK: 大小写转换
    print("--- 大小写转换 ---")
    let snakeCase = "user_name"
    let camelCase = "userName"
    print("\"\(snakeCase)\".toCamelCase() = \"\(snakeCase.toCamelCase())\"")  // "userName"
    print("\"\(snakeCase)\".toPascalCase() = \"\(snakeCase.toPascalCase())\"")  // "UserName"
    print("\"\(camelCase)\".toSnakeCase() = \"\(camelCase.toSnakeCase())\"")  // "user_name"
    print("\"\(camelCase)\".toKebabCase() = \"\(camelCase.toKebabCase())\"")  // "user-name"
    print()
    
    // MARK: 其他工具方法
    print("--- 其他工具方法 ---")
    print("\"*\".repeated(5) = \"\("*".repeated(5))\"")  // "*****"
    print("\"42\".leftPadded(to: 5, with: \"0\") = \"\("42".leftPadded(to: 5, with: "0"))\"")  // "00042"
    print("\"42\".rightPadded(to: 5, with: \"0\") = \"\("42".rightPadded(to: 5, with: "0"))\"")  // "42000"
    print("\"Hello\".reversed() = \"\("Hello".reversed())\"")  // "olleH"
    print("\"Hello World\".containsCaseInsensitive(\"world\") = \("Hello World".containsCaseInsensitive("world"))")  // true
    print()
    
    // MARK: 类型转换
    print("--- 类型转换 ---")
    print("\"123\".toInt() = \("123".toInt() ?? 0)")
    print("\"3.14\".toDouble() = \("3.14".toDouble() ?? 0.0)")
    print("\"true\".toBool() = \("true".toBool() ?? false)")
    print("\"yes\".toBool() = \("yes".toBool() ?? false)")
    print("\"1\".toBool() = \("1".toBool() ?? false)")
    print()
    
    print("=== 示例运行完成 ===")
}

// MARK: - 运行示例

runStringUtilsExamples()
