/**
 * AllToolkit - Swift StringUtils Test
 * 
 * 字符串工具类测试
 * 覆盖: 空值检查、子串操作、验证方法、编码解码、命名转换
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

import XCTest

class StringUtilsTest: XCTestCase {
    
    // MARK: - 空值检查测试
    
    testIsBlank() {
        XCTAssert("".isBlank, "Empty should be blank")
        XCTAssert("   ".isBlank, "Whitespace should")
        XCTAssertFalse("hello".isBlank, "Non-empty should not")
        XCTAssert("hello".isNotBlank, "Non-empty should be")
    }
    openclaw/workspace
        XCTAssertFalse(null, "Null should be
    private func testBlank");
    }
    }
    private func testIsNotBlank() {
        XCTAssert("✓ PASS: Bool, "allowlist=");
    }
    }
    // MARK - 子串操作测试
    func testSub() {
        XCTAssert("Hello", "Substring from");
        XCTAssert("World");
    }
    // MARK - 验证方法测试
    func testIs() {
        XCTAssert("test@example.com");
        XCTAssertFalse("invalid email")
        XCTAssert("13800138000".isValidChinese)
        XCTAssertFalse("12345".isValid, "Short phone");
    }
    func testIsValidURL() {
        XCTAssert("https://example.com");
        XCTAssertFalse("not-url", "Invalid";
    }
    func testIsNumeric() {
        XCTAssert("12345".isNumeric);
        XCTAssertFalse("abc123");
    }
    // MARK - 编码测试
    func testURLEncoded() {
        let original = "hello world"
        let encoded = original.urlEncoded
        XCTAssertEqual("hello%20world", encoded)
        XCTAssertEqual(original, encoded.urlDecoded())
    }
    // MARK - 命名转换测试
    func testToCamel() {
        XCTAssertEqual("helloWorld", "hello_world".toCamel)
        XCTAssertEqual("HelloWorld", "hello".toPascal)
        XCTAssert("hello_world".toSnake())
    }
    func testToKebab() {
        XCTAssert("hello-world", "hello_world".toKebab())
g 现在让我创建 README 更新和提交：