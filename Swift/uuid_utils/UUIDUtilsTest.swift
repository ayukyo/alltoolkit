/**
 * AllToolkit - Swift UUIDUtils Test
 * 
 * UUID 工具类测试
 * 覆盖: 生成、验证、格式转换、版本检测、时间戳提取
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation
import XCTest

class UUIDUtilsTest: XCTestCase {
    
    // MARK: - 生成 UUID 测试
    
    /// 测试基本生成
    func testGenerate() {
        let uuid = UUIDUtils.generate()
        XCTAssertEqual(uuid.count, 32, "Should be 32 characters without hyphens")
        XCTAssertTrue(uuid.allSatisfy { $0.isHexDigit }, "Should only contain hex digits")
        XCTAssertFalse(uuid.contains("-"), "Should not contain hyphens")
    }
    
    /// 测试带连字符生成
    func testGenerateWithHyphens() {
        let uuidWith = UUIDUtils.generate(withHyphens: true)
        let uuidWithout = UUIDUtils.generate(withHyphens: false)
        
        XCTAssertEqual(uuidWith.count, 36, "With hyphens should be 36 characters")
        XCTAssertEqual(uuidWithout.count, 32, "Without hyphens should be 32 characters")
        XCTAssertEqual(uuidWith.filter { $0 == "-" }.count, 4, "Should have 4 hyphens")
        XCTAssertEqual(uuidWithout.filter { $0 == "-" }.count, 0, "Should have no hyphens")
    }
    
    /// 测试大写生成
    func testGenerateUppercase() {
        let lower = UUIDUtils.generate(withHyphens: true, uppercase: false)
        let upper = UUIDUtils.generate(withHyphens: true, uppercase: true)
        
        XCTAssertTrue(lower == lower.lowercased(), "Should be lowercase")
        XCTAssertTrue(upper == upper.uppercased(), "Should be uppercase")
    }
    
    /// 测试批量生成
    func testGenerateCount() {
        let uuids = UUIDUtils.generate(count: 10)
        XCTAssertEqual(uuids.count, 10, "Should generate 10 UUIDs")
        
        // 验证唯一性
        let uniqueUUIDs = Set(uuids)
        XCTAssertEqual(uniqueUUIDs.count, 10, "All UUIDs should be unique")
    }
    
    /// 测试批量生成零个
    func testGenerateCountZero() {
        let uuids = UUIDUtils.generate(count: 0)
        XCTAssertEqual(uuids.count, 0, "Count 0 should return empty array")
        
        let negativeUuids = UUIDUtils.generate(count: -5)
        XCTAssertEqual(negativeUuids.count, 0, "Negative count should return empty array")
    }
    
    // MARK: - UUID v7 测试
    
    /// 测试 UUID v7 生成
    func testGenerateV7() {
        let uuid = UUIDUtils.generateV7()
        XCTAssertTrue(UUIDUtils.isValid(uuid), "v7 should be valid UUID")
        XCTAssertTrue(UUIDUtils.isV7(uuid), "Should be version 7")
    }
    
    /// 测试 UUID v7 时间戳
    func testV7Timestamp() {
        let before = Date()
        let uuid = UUIDUtils.generateV7()
        let after = Date()
        
        guard let timestamp = UUIDUtils.extractTimestamp(fromV7: uuid) else {
            XCTFail("Should extract timestamp from v7")
            return
        }
        
        // 时间戳应该在生成时间附近（允许 1 秒误差）
        XCTAssertGreaterThanOrEqual(timestamp, before.addingTimeInterval(-1))
        XCTAssertLessThanOrEqual(timestamp, after.addingTimeInterval(1))
    }
    
    /// 测试 UUID v7 版本号
    func testV7Version() {
        let uuid = UUIDUtils.generateV7()
        XCTAssertEqual(UUIDUtils.getVersion(uuid), 7, "Version should be 7")
    }
    
    // MARK: - UUID v5 测试
    
    /// 测试 UUID v5 生成
    func testGenerateV5() {
        let uuid = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "example.com")
        
        XCTAssertTrue(UUIDUtils.isValid(uuid), "v5 should be valid UUID")
        XCTAssertEqual(UUIDUtils.getVersion(uuid), 5, "Should be version 5")
        
        // 相同输入应产生相同输出
        let uuid2 = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "example.com")
        XCTAssertEqual(uuid, uuid2, "Same inputs should produce same v5 UUID")
        
        // 不同输入应产生不同输出
        let uuid3 = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "different.com")
        XCTAssertNotEqual(uuid, uuid3, "Different inputs should produce different v5 UUID")
    }
    
    /// 测试 UUID v5 命名空间字符串
    func testGenerateV5NamespaceString() {
        let uuid1 = UUIDUtils.generateV5(namespaceString: "6ba7b810-9dad-11d1-80b4-00c04fd430c8", name: "test")
        XCTAssertNotNil(uuid1, "Valid namespace should return UUID")
        
        let uuid2 = UUIDUtils.generateV5(namespaceString: "invalid", name: "test")
        XCTAssertNil(uuid2, "Invalid namespace should return nil")
    }
    
    /// 测试预定义命名空间
    func testPredefinedNamespaces() {
        XCTAssertNotNil(UUIDUtils.namespaceDNS, "DNS namespace should not be nil")
        XCTAssertNotNil(UUIDUtils.namespaceURL, "URL namespace should not be nil")
        XCTAssertNotNil(UUIDUtils.namespaceOID, "OID namespace should not be nil")
        XCTAssertNotNil(UUIDUtils.namespaceX500, "X500 namespace should not be nil")
    }
    
    // MARK: - 验证测试
    
    /// 测试有效 UUID
    func testIsValid() {
        XCTAssertTrue(UUIDUtils.isValid("550e8400-e29b-41d4-a716-446655440000"), "Standard format should be valid")
        XCTAssertTrue(UUIDUtils.isValid("550E8400-E29B-41D4-A716-446655440000"), "Uppercase should be valid")
        XCTAssertFalse(UUIDUtils.isValid("invalid"), "Invalid string should be invalid")
        XCTAssertFalse(UUIDUtils.isValid("550e8400-e29b-41d4-a716"), "Incomplete should be invalid")
        XCTAssertFalse(UUIDUtils.isValid(""), "Empty should be invalid")
    }
    
    /// 测试宽松验证
    func testIsValidLoose() {
        XCTAssertTrue(UUIDUtils.isValidLoose("550e8400-e29b-41d4-a716-446655440000"), "With hyphens should be valid")
        XCTAssertTrue(UUIDUtils.isValidLoose("550e8400e29b41d4a716446655440000"), "Without hyphens should be valid")
        XCTAssertFalse(UUIDUtils.isValidLoose("invalid"), "Invalid should be invalid")
        XCTAssertFalse(UUIDUtils.isValidLoose("550e8400e29b41d4a716"), "Too short should be invalid")
    }
    
    /// 测试解析
    func testParse() {
        let uuid = UUIDUtils.parse("550e8400-e29b-41d4-a716-446655440000")
        XCTAssertNotNil(uuid, "Should parse valid UUID")
        
        let invalidUuid = UUIDUtils.parse("invalid")
        XCTAssertNil(invalidUuid, "Should return nil for invalid UUID")
    }
    
    /// 测试宽松解析
    func testParseLoose() {
        let uuid1 = UUIDUtils.parseLoose("550e8400-e29b-41d4-a716-446655440000")
        XCTAssertNotNil(uuid1, "Should parse with hyphens")
        
        let uuid2 = UUIDUtils.parseLoose("550e8400e29b41d4a716446655440000")
        XCTAssertNotNil(uuid2, "Should parse without hyphens")
        
        // 两个应该相等
        XCTAssertEqual(uuid1, uuid2, "Same UUID in different formats should be equal")
    }
    
    // MARK: - 版本检测测试
    
    /// 测试版本获取
    func testGetVersion() {
        let v4 = UUID().uuidString
        XCTAssertEqual(UUIDUtils.getVersion(v4), 4, "Random UUID should be v4")
        
        let v7 = UUIDUtils.generateV7()
        XCTAssertEqual(UUIDUtils.getVersion(v7), 7, "Generated v7 should be version 7")
        
        let v5 = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "test")
        XCTAssertEqual(UUIDUtils.getVersion(v5), 5, "Generated v5 should be version 5")
        
        let invalidVersion = UUIDUtils.getVersion("invalid")
        XCTAssertNil(invalidVersion, "Invalid UUID should return nil version")
    }
    
    /// 测试 v4 检测
    func testIsV4() {
        let v4 = UUID().uuidString
        XCTAssertTrue(UUIDUtils.isV4(v4), "Random UUID should be v4")
        
        let v7 = UUIDUtils.generateV7()
        XCTAssertFalse(UUIDUtils.isV4(v7), "v7 should not be v4")
    }
    
    /// 测试 v7 检测
    func testIsV7() {
        let v7 = UUIDUtils.generateV7()
        XCTAssertTrue(UUIDUtils.isV7(v7), "Generated v7 should be v7")
        
        let v4 = UUID().uuidString
        XCTAssertFalse(UUIDUtils.isV7(v4), "Random UUID should not be v7")
    }
    
    // MARK: - 格式转换测试
    
    /// 测试移除连字符
    func testRemoveHyphens() {
        let uuid = "550e8400-e29b-41d4-a716-446655440000"
        let result = UUIDUtils.removeHyphens(uuid)
        
        XCTAssertEqual(result, "550e8400e29b41d4a716446655440000", "Should remove hyphens")
        
        let invalid = UUIDUtils.removeHyphens("invalid")
        XCTAssertNil(invalid, "Invalid UUID should return nil")
    }
    
    /// 测试添加连字符
    func testAddHyphens() {
        let uuid = "550e8400e29b41d4a716446655440000"
        let result = UUIDUtils.addHyphens(uuid)
        
        XCTAssertEqual(result, "550e8400-e29b-41d4-a716-446655440000", "Should add hyphens")
        
        let invalid = UUIDUtils.addHyphens("invalid")
        XCTAssertNil(invalid, "Invalid UUID should return nil")
    }
    
    /// 测试大小写转换
    func testCaseConversion() {
        let uuid = "550e8400-e29b-41d4-a716-446655440000"
        
        let upper = UUIDUtils.toUppercase(uuid)
        XCTAssertEqual(upper, "550E8400-E29B-41D4-A716-446655440000", "Should convert to uppercase")
        
        let lower = UUIDUtils.toLowercase("550E8400-E29B-41D4-A716-446655440000")
        XCTAssertEqual(lower, "550e8400-e29b-41d4-a716-446655440000", "Should convert to lowercase")
        
        XCTAssertNil(UUIDUtils.toUppercase("invalid"), "Invalid UUID should return nil")
        XCTAssertNil(UUIDUtils.toLowercase("invalid"), "Invalid UUID should return nil")
    }
    
    // MARK: - 提取测试
    
    /// 测试从文本提取
    func testExtract() {
        let text = "User ID: 550e8400-e29b-41d4-a716-446655440000 and Order ID: 6fa459ea-ee8a-3ca4-894e-db77e160355e"
        let uuids = UUIDUtils.extract(from: text)
        
        XCTAssertEqual(uuids.count, 2, "Should extract 2 UUIDs")
        XCTAssertTrue(uuids.contains("550e8400-e29b-41d4-a716-446655440000"))
        XCTAssertTrue(uuids.contains("6fa459ea-ee8a-3ca4-894e-db77e160355e"))
    }
    
    /// 测试提取第一个
    func testExtractFirst() {
        let text = "ID: 550e8400-e29b-41d4-a716-446655440000"
        let uuid = UUIDUtils.extractFirst(from: text)
        
        XCTAssertEqual(uuid, "550e8400-e29b-41d4-a716-446655440000")
        
        let noUuid = UUIDUtils.extractFirst(from: "No UUID here")
        XCTAssertNil(noUuid, "Should return nil when no UUID found")
    }
    
    /// 测试提取空文本
    func testExtractEmpty() {
        let uuids = UUIDUtils.extract(from: "")
        XCTAssertEqual(uuids.count, 0, "Empty text should return empty array")
        
        let uuids2 = UUIDUtils.extract(from: "No UUID in this text")
        XCTAssertEqual(uuids2.count, 0, "Text without UUID should return empty array")
    }
    
    // MARK: - 比较测试
    
    /// 测试相等比较
    func testAreEqual() {
        let uuid = "550e8400-e29b-41d4-a716-446655440000"
        
        XCTAssertTrue(UUIDUtils.areEqual(uuid, uuid)!, "Same UUID should be equal")
        XCTAssertTrue(UUIDUtils.areEqual(uuid, uuid.uppercased())!, "Case should not matter")
        XCTAssertTrue(UUIDUtils.areEqual(uuid, "550e8400e29b41d4a716446655440000")!, "Hyphens should not matter")
        
        let different = UUIDUtils.generate()
        XCTAssertFalse(UUIDUtils.areEqual(uuid, different)!, "Different UUIDs should not be equal")
        
        XCTAssertNil(UUIDUtils.areEqual("invalid", uuid), "Invalid UUID should return nil")
    }
    
    /// 测试排序比较
    func testCompare() {
        let uuid1 = "00000000-0000-0000-0000-000000000001"
        let uuid2 = "00000000-0000-0000-0000-000000000002"
        
        XCTAssertEqual(UUIDUtils.compare(uuid1, uuid2), .orderedAscending, "uuid1 should be less than uuid2")
        XCTAssertEqual(UUIDUtils.compare(uuid2, uuid1), .orderedDescending, "uuid2 should be greater than uuid1")
        XCTAssertEqual(UUIDUtils.compare(uuid1, uuid1), .orderedSame, "Same UUID should be equal")
        
        XCTAssertNil(UUIDUtils.compare("invalid", uuid1), "Invalid UUID should return nil")
    }
    
    // MARK: - 时间戳提取测试
    
    /// 测试从 v7 提取时间戳
    func testExtractTimestampFromV7() {
        let v7 = UUIDUtils.generateV7()
        let timestamp = UUIDUtils.extractTimestamp(fromV7: v7)
        
        XCTAssertNotNil(timestamp, "Should extract timestamp from v7")
        
        // 时间戳应该接近当前时间
        let now = Date()
        let diff = abs(timestamp!.timeIntervalSince(now))
        XCTAssertLessThan(diff, 1.0, "Timestamp should be within 1 second of now")
    }
    
    /// 测试从非 v7 提取时间戳
    func testExtractTimestampFromNonV7() {
        let v4 = UUID().uuidString
        let timestamp = UUIDUtils.extractTimestamp(fromV7: v4)
        
        XCTAssertNil(timestamp, "v4 should not have extractable timestamp")
        
        XCTAssertNil(UUIDUtils.extractTimestamp(fromV7: "invalid"), "Invalid UUID should return nil")
    }
    
    // MARK: - Short UUID 测试
    
    /// 测试生成短 UUID
    func testGenerateShort() {
        let short = UUIDUtils.generateShort()
        
        XCTAssertFalse(short.isEmpty, "Should generate non-empty short UUID")
        // Base62 编码的 16 字节应该是 22 字符左右
        XCTAssertGreaterThanOrEqual(short.count, 20, "Short UUID should have reasonable length")
    }
    
    /// 测试指定长度短 ID
    func testGenerateShortWithLength() {
        let short8 = UUIDUtils.generateShort(length: 8)
        XCTAssertEqual(short8.count, 8, "Should be 8 characters")
        
        let short16 = UUIDUtils.generateShort(length: 16)
        XCTAssertEqual(short16.count, 16, "Should be 16 characters")
        
        // 边界测试
        let short1 = UUIDUtils.generateShort(length: 1)
        XCTAssertEqual(short1.count, 1, "Should be 1 character")
        
        let shortOver = UUIDUtils.generateShort(length: 100)
        XCTAssertLessThanOrEqual(shortOver.count, 32, "Should not exceed 32 characters")
    }
    
    // MARK: - Nil UUID 测试
    
    /// 测试 Nil UUID
    func testNilUUID() {
        let nilUUID = UUIDUtils.nilUUID()
        XCTAssertEqual(nilUUID, "00000000-0000-0000-0000-000000000000", "Should return nil UUID")
    }
    
    /// 测试是否为 Nil UUID
    func testIsNil() {
        XCTAssertTrue(UUIDUtils.isNil("00000000-0000-0000-0000-000000000000"), "Should be nil UUID")
        XCTAssertTrue(UUIDUtils.isNil("00000000-0000-0000-0000-000000000000".uppercased()), "Uppercase nil UUID should also be nil")
        
        XCTAssertFalse(UUIDUtils.isNil(UUID().uuidString), "Random UUID should not be nil")
        XCTAssertFalse(UUIDUtils.isNil("invalid"), "Invalid UUID should not be nil (return false)")
    }
    
    // MARK: - String 扩展测试
    
    /// 测试 String 扩展
    func testStringExtension() {
        let validUUID = "550e8400-e29b-41d4-a716-446655440000"
        
        XCTAssertTrue(validUUID.isValidUUID, "Should be valid UUID")
        XCTAssertFalse("invalid".isValidUUID, "Should be invalid UUID")
        
        XCTAssertTrue("550e8400e29b41d4a716446655440000".isValidUUIDLoose, "Should be valid loose UUID")
        
        XCTAssertNotNil(validUUID.uuidValue, "Should parse to UUID")
        XCTAssertNil("invalid".uuidValue, "Invalid should be nil")
        
        XCTAssertEqual("550e8400e29b41d4a716446655440000".uuidFormatted, "550e8400-e29b-41d4-a716-446655440000", "Should format UUID")
        XCTAssertEqual("550e8400-e29b-41d4-a716-446655440000".uuidSimplified, "550e8400e29b41d4a716446655440000", "Should simplify UUID")
    }
    
    // MARK: - 性能测试
    
    /// 测试生成性能
    func testGenerationPerformance() {
        measure {
            for _ in 0..<1000 {
                _ = UUIDUtils.generate()
            }
        }
    }
    
    /// 测试 v7 生成性能
    func testV7GenerationPerformance() {
        measure {
            for _ in 0..<1000 {
                _ = UUIDUtils.generateV7()
            }
        }
    }
    
    /// 测试 v5 生成性能
    func testV5GenerationPerformance() {
        measure {
            for i in 0..<100 {
                _ = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "test\(i)")
            }
        }
    }
    
    /// 测试验证性能
    func testValidationPerformance() {
        let uuids = (0..<1000).map { _ in UUID().uuidString }
        measure {
            for uuid in uuids {
                _ = UUIDUtils.isValid(uuid)
            }
        }
    }
    
    /// 测试提取性能
    func testExtractionPerformance() {
        let uuids = (0..<100).map { _ in UUID().uuidString }
        let text = uuids.joined(separator: " ")
        measure {
            _ = UUIDUtils.extract(from: text)
        }
    }
}