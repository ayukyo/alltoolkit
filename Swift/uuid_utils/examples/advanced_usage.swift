/**
 * AllToolkit - Swift UUID Utils 高级用法示例
 * 
 * 本示例展示 UUID 工具类的高级用法和实际应用场景
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// ========================================
// 1. 分布式系统 ID 生成
// ========================================

print("=== 分布式系统 ID 生成 ===")

// 使用 v7 UUID 作为分布式系统的主键
// v7 UUID 按时间排序，非常适合数据库索引
struct DistributedIDGenerator {
    static func generateID() -> String {
        return UUIDUtils.generateV7()
    }
    
    static func generateIDs(count: Int) -> [String] {
        return (0..<count).map { _ in generateID() }
    }
    
    static func getGenerationTime(id: String) -> Date? {
        return UUIDUtils.extractTimestamp(fromV7: id)
    }
}

// 模拟生成订单 ID
let orderIDs = DistributedIDGenerator.generateIDs(count: 10)
print("订单 ID 列表:")
for (index, id) in orderIDs.enumerated() {
    if let time = DistributedIDGenerator.getGenerationTime(id: id) {
        let formatter = DateFormatter()
        formatter.dateFormat = "HH:mm:ss.SSS"
        print("  订单 \(index + 1): \(id) [\(formatter.string(from: time))]")
    }
}

// ========================================
// 2. 用户追踪和去重
// ========================================

print("\n=== 用户追踪和去重 ===")

// 使用 v5 UUID 为用户生成稳定标识符
class UserIdentifier {
    static func generateUserUUID(email: String) -> String {
        return UUIDUtils.generateV5(namespace: UUIDUtils.namespaceURL, name: email.lowercased())
    }
    
    static func generateDeviceUUID(deviceId: String) -> String {
        return UUIDUtils.generateV5(namespace: UUIDUtils.namespaceOID, name: deviceId)
    }
}

// 同一邮箱始终生成相同 UUID
let email = "user@example.com"
let userUUID1 = UserIdentifier.generateUserUUID(email: email)
let userUUID2 = UserIdentifier.generateUserUUID(email: email)
let userUUID3 = UserIdentifier.generateUserUUID(email: "USER@EXAMPLE.COM")  // 大写

print("邮箱: \(email)")
print("UUID 1: \(userUUID1)")
print("UUID 2: \(userUUID2)")
print("UUID 3 (大写邮箱): \(userUUID3)")
print("一致性验证: \(userUUID1 == userUUID2 && userUUID1 == userUUID3)")

// ========================================
// 3. 日志分析 - UUID 提取
// ========================================

print("\n=== 日志分析 - UUID 提取 ===")

let serverLog = """
2024-01-15 ERROR [550e8400-e29b-41d4-a716-446655440000] Connection failed
2024-01-15 INFO  [6fa459ea-ee8a-3ca4-894e-db77e160355e] Request processed
2024-01-15 WARN  [123e4567-e89b-12d3-a456-426614174000] Timeout detected
2024-01-15 DEBUG [invalid-uuid-format] Debug message
2024-01-15 INFO  [abcdef12-3456-7890-abcd-ef1234567890] Success
"""

// 提取所有有效的 UUID
let uuids = UUIDUtils.extract(from: serverLog)
print("提取到 \(uuids.count) 个有效 UUID:")
for uuid in uuids {
    let version = UUIDUtils.getVersion(uuid) ?? 0
    print("  - \(uuid) (v\(version))")
}

// 统计版本分布
let versionCounts = uuids.reduce(into: [Int: Int]() { counts, uuid in
    let version = UUIDUtils.getVersion(uuid) ?? 0
    counts[version, default: 0] += 1
})
print("版本分布:")
for (version, count) in versionCounts.sorted(by: { $0.key < $1.key }) {
    print("  - v\(version): \(count) 个")
}

// ========================================
// 4. 缓存键生成
// ========================================

print("\n=== 缓存键生成 ===")

// 使用短 UUID 作为缓存键
class CacheKeyGenerator {
    static func generateSessionKey() -> String {
        return "session:" + UUIDUtils.generateShort(length: 12)
    }
    
    static func generateTempKey() -> String {
        return "temp:" + UUIDUtils.generateShort(length: 8)
    }
    
    static func generateFileKey(filename: String) -> String {
        // 使用 v5 确保同一文件名产生相同键
        let hash = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceURL, name: filename)
        return "file:" + UUIDUtils.removeHyphens(hash)!
    }
}

let sessionKey = CacheKeyGenerator.generateSessionKey()
let tempKey = CacheKeyGenerator.generateTempKey()
let fileKey1 = CacheKeyGenerator.generateFileKey(filename: "document.pdf")
let fileKey2 = CacheKeyGenerator.generateFileKey(filename: "document.pdf")

print("会话键: \(sessionKey)")
print("临时键: \(tempKey)")
print("文件键 1: \(fileKey1)")
print("文件键 2: \(fileKey2)")
print("文件键一致性: \(fileKey1 == fileKey2)")

// ========================================
// 5. API 请求追踪
// ========================================

print("\n=== API 请求追踪 ===")

struct APIRequest {
    let id: String
    let timestamp: Date
    let endpoint: String
    
    init(endpoint: String) {
        self.id = UUIDUtils.generateV7()
        self.timestamp = Date()
        self.endpoint = endpoint
    }
    
    func log() {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss.SSS"
        print("[\(id)] \(formatter.string(from: timestamp)) - \(endpoint)")
    }
}

// 模拟 API 请求
let requests = [
    APIRequest(endpoint: "/api/users"),
    APIRequest(endpoint: "/api/orders"),
    APIRequest(endpoint: "/api/products"),
    APIRequest(endpoint: "/api/payments")
]

print("API 请求追踪:")
for req in requests {
    req.log()
}

// ========================================
// 6. 数据库批量插入优化
// ========================================

print("\n=== 数据库批量插入优化 ===")

// 使用 v7 UUID 可以提高数据库插入性能（减少索引重排）
struct BatchInsertDemo {
    static func generateBatchIDs(count: Int) -> [String] {
        // v7 UUID 按时间生成，接近顺序插入
        return (0..<count).map { _ in UUIDUtils.generateV7() }
    }
    
    static func measureSortPerformance(ids: [String]) -> TimeInterval {
        let start = Date()
        _ = ids.sorted { UUIDUtils.compare($0, $1) == .orderedAscending }
        return Date().timeIntervalSince(start)
    }
}

let batchV7 = BatchInsertDemo.generateBatchIDs(count: 1000)
let batchV4 = UUIDUtils.generate(count: 1000).map { UUIDUtils.addHyphens($0)! }

let v7SortTime = BatchInsertDemo.measureSortPerformance(ids: batchV7)
let v4SortTime = BatchInsertDemo.measureSortPerformance(ids: batchV4)

print("1000 个 UUID 排序性能:")
print("  v7 UUID: \(String(format: "%.4f", v7SortTime)) 秒")
print("  v4 UUID: \(String(format: "%.4f", v4SortTime)) 秒")

// ========================================
// 7. URL 安全标识符
// ========================================

print("\n=== URL 安全标识符 ===")

// 短 UUID 可用于 URL 安全的标识符
class URLSafeID {
    static func generateShareLink() -> String {
        return "https://app.com/share/" + UUIDUtils.generateShort(length: 8)
    }
    
    static func generateVerificationCode() -> String {
        // 生成 6 字符验证码
        return UUIDUtils.generateShort(length: 6)
    }
    
    static func generateTempPassword() -> String {
        return UUIDUtils.generateShort(length: 12)
    }
}

print("分享链接: \(URLSafeID.generateShareLink())")
print("验证码: \(URLSafeID.generateVerificationCode())")
print("临时密码: \(URLSafeID.generateTempPassword())")

// ========================================
// 8. 多语言环境 UUID 处理
// ========================================

print("\n=== 多语言环境 UUID 处理 ===")

// 处理来自不同系统的 UUID（可能有不同格式）
let mixedFormats = [
    "550e8400-e29b-41d4-a716-446655440000",  // 标准
    "550E8400E29B41D4A716446655440000",       // 无连字符大写
    "550e8400e29b41d4a716446655440000",       // 无连字符小写
    "550e8400-E29B-41d4-a716-446655440000",   // 混合大小写
]

print("标准化不同格式的 UUID:")
for format in mixedFormats {
    if let normalized = UUIDUtils.parseLoose(format)?.uuidString.lowercased() {
        print("  原始: \(format)")
        print("  标准化: \(normalized)")
        print("")
    }
}

// ========================================
// 9. UUID 唯一性验证
// ========================================

print("\n=== UUID 唯一性验证 ===")

// 验证一批 UUID 是否唯一
func validateUniqueIDs(ids: [String]) -> Bool {
    let set = Set(ids.map { UUIDUtils.parseLoose($0)?.uuidString.lowercased() ?? $0 })
    return set.count == ids.count
}

let testIDs = UUIDUtils.generate(count: 100)
print("100 个 UUID 是否全部唯一: \(validateUniqueIDs(ids: testIDs))")

// 添加重复 UUID 测试
let duplicateIDs = testIDs + [testIDs.first!]
print("包含重复的 101 个 ID 是否唯一: \(validateUniqueIDs(ids: duplicateIDs))")

// ========================================
// 10. 性能基准测试
// ========================================

print("\n=== 性能基准测试 ===")

// 测试不同生成方法的性能
func benchmark(label: String, iterations: Int, operation: () -> String) {
    let start = Date()
    for _ in 0..<iterations {
        _ = operation()
    }
    let elapsed = Date().timeIntervalSince(start)
    print("\(label): \(iterations) 次, \(String(format: "%.4f", elapsed)) 秒, \(String(format: "%.2f", iterations/elapsed)) 次/秒")
}

benchmark(label: "v4 生成", iterations: 10000, operation: { UUIDUtils.generate() })
benchmark(label: "v7 生成", iterations: 10000, operation: { UUIDUtils.generateV7() })
benchmark(label: "v5 生成", iterations: 1000, operation: { UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "test") })
benchmark(label: "短 UUID", iterations: 10000, operation: { UUIDUtils.generateShort() })
benchmark(label: "验证", iterations: 10000, operation: { UUIDUtils.isValid(UUID().uuidString) ? "valid" : "invalid" })

print("\n=== 高级示例完成 ===")