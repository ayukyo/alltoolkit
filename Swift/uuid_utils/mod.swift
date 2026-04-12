/**
 * AllToolkit - Swift UUID Utilities
 *
 * 通用 UUID 工具类，提供 UUID 生成、验证、解析和格式转换功能。
 * 零依赖，仅使用 Swift 标准库和 Foundation 框架。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - UUIDUtils 主类

/// UUID 工具类，提供静态方法处理 UUID 相关操作
public enum UUIDUtils {
    
    // MARK: - UUID 版本枚举
    
    /// UUID 版本类型
    public enum UUIDVersion {
        case v1  // 基于时间（模拟）
        case v4  // 随机生成
        case v5  // 基于命名空间（SHA-1）
        case v7  // 基于时间戳（Unix 时间戳）
    }
    
    // MARK: - 预定义命名空间
    
    /// DNS 命名空间 UUID
    public static let namespaceDNS = UUID(uuidString: "6ba7b810-9dad-11d1-80b4-00c04fd430c8")!
    
    /// URL 命名空间 UUID
    public static let namespaceURL = UUID(uuidString: "6ba7b811-9dad-11d1-80b4-00c04fd430c8")!
    
    /// OID 命名空间 UUID
    public static let namespaceOID = UUID(uuidString: "6ba7b812-9dad-11d1-80b4-00c04fd430c8")!
    
    /// X.500 命名空间 UUID
    public static let namespaceX500 = UUID(uuidString: "6ba7b814-9dad-11d1-80b4-00c04fd430c8")!
    
    // MARK: - 生成 UUID
    
    /// 生成一个随机 UUID (v4)
    /// - Returns: UUID 字符串（小写，无连字符）
    public static func generate() -> String {
        return UUID().uuidString.lowercased().replacingOccurrences(of: "-", with: "")
    }
    
    /// 生成一个随机 UUID (v4)，带格式选项
    /// - Parameters:
    ///   - withHyphens: 是否包含连字符，默认 true
    ///   - uppercase: 是否大写，默认 false
    /// - Returns: UUID 字符串
    public static func generate(withHyphens: Bool = true, uppercase: Bool = false) -> String {
        var uuid = UUID().uuidString
        if !withHyphens {
            uuid = uuid.replacingOccurrences(of: "-", with: "")
        }
        return uppercase ? uuid.uppercased() : uuid.lowercased()
    }
    
    /// 生成多个 UUID
    /// - Parameter count: 生成数量
    /// - Returns: UUID 字符串数组
    public static func generate(count: Int) -> [String] {
        guard count > 0 else { return [] }
        return (0..<count).map { _ in generate(withHyphens: true, uppercase: false) }
    }
    
    /// 生成 UUID v7（基于时间戳）
    /// 使用 Unix 毫秒时间戳作为前 48 位，其余随机
    /// - Returns: UUID v7 字符串
    public static func generateV7() -> String {
        let timestamp = UInt64(Date().timeIntervalSince1970 * 1000)
        
        var bytes = [UInt8](repeating: 0, count: 16)
        
        // 时间戳填充前 48 位（6 字节）
        bytes[0] = UInt8((timestamp >> 40) & 0xFF)
        bytes[1] = UInt8((timestamp >> 32) & 0xFF)
        bytes[2] = UInt8((timestamp >> 24) & 0xFF)
        bytes[3] = UInt8((timestamp >> 16) & 0xFF)
        bytes[4] = UInt8((timestamp >> 8) & 0xFF)
        bytes[5] = UInt8(timestamp & 0xFF)
        
        // 随机填充剩余字节
        for i in 6..<16 {
            bytes[i] = UInt8.random(in: 0...255)
        }
        
        // 设置版本为 7 (0111)
        bytes[6] = (bytes[6] & 0x0F) | 0x70
        
        // 设置变体为 RFC 4122 (10xx)
        bytes[8] = (bytes[8] & 0x3F) | 0x80
        
        let uuid = UUID(uuid: (
            bytes[0], bytes[1], bytes[2], bytes[3],
            bytes[4], bytes[5], bytes[6], bytes[7],
            bytes[8], bytes[9], bytes[10], bytes[11],
            bytes[12], bytes[13], bytes[14], bytes[15]
        ))
        
        return uuid.uuidString.lowercased()
    }
    
    /// 生成基于命名空间的 UUID v5
    /// - Parameters:
    ///   - namespace: 命名空间 UUID
    ///   - name: 名称字符串
    /// - Returns: UUID v5 字符串
    public static func generateV5(namespace: UUID, name: String) -> String {
        let namespaceBytes = withUnsafeBytes(of: namespace.uuid) { Data($0) }
        let nameBytes = Data(name.utf8)
        let combined = namespaceBytes + nameBytes
        
        // SHA-1 哈希
        var digest = [UInt8](repeating: 0, count: 20)  // SHA-1 = 20 bytes
        _ = combined.withUnsafeBytes { ptr in
            CC_SHA1(ptr.baseAddress, CC_LONG(combined.count), &digest)
        }
        
        // 取前 16 字节
        var bytes = Array(digest[0..<16])
        
        // 设置版本为 5 (0101)
        bytes[6] = (bytes[6] & 0x0F) | 0x50
        
        // 设置变体为 RFC 4122 (10xx)
        bytes[8] = (bytes[8] & 0x3F) | 0x80
        
        let uuid = UUID(uuid: (
            bytes[0], bytes[1], bytes[2], bytes[3],
            bytes[4], bytes[5], bytes[6], bytes[7],
            bytes[8], bytes[9], bytes[10], bytes[11],
            bytes[12], bytes[13], bytes[14], bytes[15]
        ))
        
        return uuid.uuidString.lowercased()
    }
    
    /// 生成基于命名空间的 UUID v5（使用字符串命名空间）
    /// - Parameters:
    ///   - namespaceString: 命名空间 UUID 字符串
    ///   - name: 名称字符串
    /// - Returns: UUID v5 字符串，命名空间无效时返回 nil
    public static func generateV5(namespaceString: String, name: String) -> String? {
        guard let namespace = UUID(uuidString: namespaceString) else { return nil }
        return generateV5(namespace: namespace, name: name)
    }
    
    // MARK: - 验证 UUID
    
    /// 验证字符串是否为有效的 UUID
    /// - Parameter string: 待验证字符串
    /// - Returns: 是否为有效 UUID
    public static func isValid(_ string: String) -> Bool {
        return UUID(uuidString: string) != nil
    }
    
    /// 验证字符串是否为有效的 UUID（支持无连字符格式）
    /// - Parameter string: 待验证字符串
    /// - Returns: 是否为有效 UUID
    public static func isValidLoose(_ string: String) -> Bool {
        // 标准格式
        if UUID(uuidString: string) != nil {
            return true
        }
        // 无连字符格式
        if string.count == 32 {
            let hyphenated = insertHyphens(string)
            return UUID(uuidString: hyphenated) != nil
        }
        return false
    }
    
    /// 验证并返回 UUID
    /// - Parameter string: UUID 字符串
    /// - Returns: UUID 对象，无效时返回 nil
    public static func parse(_ string: String) -> UUID? {
        return UUID(uuidString: string)
    }
    
    /// 验证并返回 UUID（支持无连字符格式）
    /// - Parameter string: UUID 字符串
    /// - Returns: UUID 对象，无效时返回 nil
    public static func parseLoose(_ string: String) -> UUID? {
        if let uuid = UUID(uuidString: string) {
            return uuid
        }
        if string.count == 32 {
            let hyphenated = insertHyphens(string)
            return UUID(uuidString: hyphenated)
        }
        return nil
    }
    
    // MARK: - UUID 版本检测
    
    /// 获取 UUID 版本
    /// - Parameter uuidString: UUID 字符串
    /// - Returns: 版本号 (1-8)，无效 UUID 返回 nil
    public static func getVersion(_ uuidString: String) -> Int? {
        guard let uuid = UUID(uuidString: uuidString) else { return nil }
        return getVersion(uuid)
    }
    
    /// 获取 UUID 版本
    /// - Parameter uuid: UUID 对象
    /// - Returns: 版本号 (1-8)
    public static func getVersion(_ uuid: UUID) -> Int {
        let bytes = withUnsafeBytes(of: uuid.uuid) { Data($0) }
        // 版本号在第 7 字节的高 4 位
        return Int((bytes[6] >> 4) & 0x0F)
    }
    
    /// 检查是否为 UUID v4
    /// - Parameter uuidString: UUID 字符串
    /// - Returns: 是否为 v4
    public static func isV4(_ uuidString: String) -> Bool {
        return getVersion(uuidString) == 4
    }
    
    /// 检查是否为 UUID v7
    /// - Parameter uuidString: UUID 字符串
    /// - Returns: 是否为 v7
    public static func isV7(_ uuidString: String) -> Bool {
        return getVersion(uuidString) == 7
    }
    
    // MARK: - 格式转换
    
    /// 移除 UUID 中的连字符
    /// - Parameter uuidString: UUID 字符串
    /// - Returns: 无连字符的 UUID 字符串，无效时返回 nil
    public static func removeHyphens(_ uuidString: String) -> String? {
        guard isValid(uuidString) else { return nil }
        return uuidString.replacingOccurrences(of: "-", with: "")
    }
    
    /// 为 UUID 添加连字符
    /// - Parameter uuidString: 无连字符的 UUID 字符串（32 字符）
    /// - Returns: 标准格式 UUID 字符串，无效时返回 nil
    public static func addHyphens(_ uuidString: String) -> String? {
        guard uuidString.count == 32 else { return nil }
        return insertHyphens(uuidString)
    }
    
    /// 转换为大写
    /// - Parameter uuidString: UUID 字符串
    /// - Returns: 大写 UUID 字符串，无效时返回 nil
    public static func toUppercase(_ uuidString: String) -> String? {
        guard isValid(uuidString) else { return nil }
        return uuidString.uppercased()
    }
    
    /// 转换为小写
    /// - Parameter uuidString: UUID 字符串
    /// - Returns: 小写 UUID 字符串，无效时返回 nil
    public static func toLowercase(_ uuidString: String) -> String? {
        guard isValid(uuidString) else { return nil }
        return uuidString.lowercased()
    }
    
    // MARK: - UUID 提取
    
    /// 从字符串中提取所有 UUID
    /// - Parameter text: 包含 UUID 的文本
    /// - Returns: 提取到的 UUID 数组
    public static func extract(from text: String) -> [String] {
        // 匹配带连字符的标准格式
        let pattern = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
        guard let regex = try? NSRegularExpression(pattern: pattern) else { return [] }
        let range = NSRange(location: 0, length: text.utf16.count)
        let matches = regex.matches(in: text, options: [], range: range)
        return matches.compactMap { match in
            guard let range = Range(match.range, in: text) else { return nil }
            return String(text[range])
        }
    }
    
    /// 从字符串中提取第一个 UUID
    /// - Parameter text: 包含 UUID 的文本
    /// - Returns: 第一个 UUID，未找到返回 nil
    public static func extractFirst(from text: String) -> String? {
        return extract(from: text).first
    }
    
    // MARK: - UUID 比较
    
    /// 比较两个 UUID 是否相等
    /// - Parameters:
    ///   - uuid1: 第一个 UUID 字符串
    ///   - uuid2: 第二个 UUID 字符串
    /// - Returns: 是否相等，任一无效返回 nil
    public static func areEqual(_ uuid1: String, _ uuid2: String) -> Bool? {
        guard let u1 = parseLoose(uuid1), let u2 = parseLoose(uuid2) else { return nil }
        return u1 == u2
    }
    
    /// 比较两个 UUID 的排序顺序
    /// - Parameters:
    ///   - uuid1: 第一个 UUID 字符串
    ///   - uuid2: 第二个 UUID 字符串
    /// - Returns: 比较结果，任一无效返回 nil
    public static func compare(_ uuid1: String, _ uuid2: String) -> ComparisonResult? {
        guard let u1 = parseLoose(uuid1), let u2 = parseLoose(uuid2) else { return nil }
        let s1 = u1.uuidString.lowercased()
        let s2 = u2.uuidString.lowercased()
        return s1.compare(s2)
    }
    
    // MARK: - UUID 时间戳提取（v7）
    
    /// 从 UUID v7 提取时间戳
    /// - Parameter uuidString: UUID v7 字符串
    /// - Returns: 时间戳日期，非 v7 或无效返回 nil
    public static func extractTimestamp(fromV7 uuidString: String) -> Date? {
        guard let uuid = UUID(uuidString: uuidString),
              getVersion(uuid) == 7 else { return nil }
        
        let bytes = withUnsafeBytes(of: uuid.uuid) { Data($0) }
        
        // 前 48 位是毫秒时间戳
        var timestamp: UInt64 = 0
        timestamp |= UInt64(bytes[0]) << 40
        timestamp |= UInt64(bytes[1]) << 32
        timestamp |= UInt64(bytes[2]) << 24
        timestamp |= UInt64(bytes[3]) << 16
        timestamp |= UInt64(bytes[4]) << 8
        timestamp |= UInt64(bytes[5])
        
        return Date(timeIntervalSince1970: Double(timestamp) / 1000.0)
    }
    
    // MARK: - Short UUID
    
    /// 生成短 UUID（Base62 编码，22 字符）
    /// - Returns: Base62 编码的短 UUID 字符串
    public static func generateShort() -> String {
        let uuid = UUID()
        let bytes = withUnsafeBytes(of: uuid.uuid) { Data($0) }
        return bytes.base62Encoded()
    }
    
    /// 生成指定长度的短 ID
    /// - Parameter length: 长度（1-32）
    /// - Returns: 短 ID 字符串
    public static func generateShort(length: Int) -> String {
        let maxLength = 32
        let actualLength = min(max(1, length), maxLength)
        let uuid = UUID()
        let bytes = withUnsafeBytes(of: uuid.uuid) { Data($0) }
        let encoded = bytes.base62Encoded()
        return String(encoded.prefix(actualLength))
    }
    
    // MARK: - Nil UUID
    
    /// 获取 Nil UUID
    /// - Returns: 全零 UUID 字符串
    public static func nilUUID() -> String {
        return "00000000-0000-0000-0000-000000000000"
    }
    
    /// 检查是否为 Nil UUID
    /// - Parameter uuidString: UUID 字符串
    /// - Returns: 是否为 Nil UUID
    public static func isNil(_ uuidString: String) -> Bool {
        guard let uuid = UUID(uuidString: uuidString) else { return false }
        return uuid.uuid == UUID(uuidString: "00000000-0000-0000-0000-000000000000")!.uuid
    }
    
    // MARK: - 私有方法
    
    /// 在 32 字符字符串中插入连字符
    private static func insertHyphens(_ string: String) -> String {
        let chars = Array(string.lowercased())
        guard chars.count == 32 else { return string }
        return "\(String(chars[0..<8]))-\(String(chars[8..<12]))-\(String(chars[12..<16]))-\(String(chars[16..<20]))-\(String(chars[20..<32]))"
    }
}

// MARK: - Data 扩展（Base62 编码）

extension Data {
    /// Base62 字符集
    private static let base62Chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    
    /// Base62 编码
    func base62Encoded() -> String {
        var result = ""
        var bytes = self.map { $0 }
        
        while !bytes.allSatisfy({ $0 == 0 }) {
            var remainder: UInt8 = 0
            for i in 0..<bytes.count {
                let value = UInt16(remainder) * 256 + UInt16(bytes[i])
                bytes[i] = UInt8(value / 62)
                remainder = UInt8(value % 62)
            }
            result = String(Self.base62Chars[Self.base62Chars.index(Self.base62Chars.startIndex, offsetBy: Int(remainder))]) + result
        }
        
        // 处理前导零
        for byte in self {
            guard byte == 0 else { break }
            result = "0" + result
        }
        
        return result.isEmpty ? "0" : result
    }
}

// MARK: - String 扩展

public extension String {
    /// 验证是否为有效 UUID
    var isValidUUID: Bool {
        return UUIDUtils.isValid(self)
    }
    
    /// 验证是否为有效 UUID（宽松模式，支持无连字符）
    var isValidUUIDLoose: Bool {
        return UUIDUtils.isValidLoose(self)
    }
    
    /// 解析为 UUID 对象
    var uuidValue: UUID? {
        return UUIDUtils.parseLoose(self)
    }
    
    /// 作为 UUID 格式化（添加连字符）
    var uuidFormatted: String? {
        return UUIDUtils.addHyphens(self)
    }
    
    /// 作为 UUID 简化（移除连字符）
    var uuidSimplified: String? {
        return UUIDUtils.removeHyphens(self)
    }
}

// MARK: - 导入 CommonCrypto（SHA-1 支持）

import CommonCrypto