/**
 * AllToolkit - Swift UUID Utils 基础用法示例
 * 
 * 本示例展示 UUID 工具类的基本用法
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// ========================================
// 1. 基本 UUID 生成
// ========================================

print("=== 基本 UUID 生成 ===")

// 生成标准 UUID (v4)
let uuid = UUIDUtils.generate(withHyphens: true)
print("标准 UUID: \(uuid)")

// 无连字符格式
let uuidCompact = UUIDUtils.generate(withHyphens: false)
print("紧凑 UUID: \(uuidCompact)")

// 大写格式
let uuidUpper = UUIDUtils.generate(withHyphens: true, uppercase: true)
print("大写 UUID: \(uuidUpper)")

// 批量生成
let uuids = UUIDUtils.generate(count: 5)
print("批量生成:")
for u in uuids {
    print("  - \(u)")
}

// ========================================
// 2. UUID v7 (时间戳排序)
// ========================================

print("\n=== UUID v7 ===")

// 生成 v7 (基于时间戳)
let v7 = UUIDUtils.generateV7()
print("UUID v7: \(v7)")

// 提取时间戳
if let timestamp = UUIDUtils.extractTimestamp(fromV7: v7) {
    let formatter = DateFormatter()
    formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
    print("生成时间: \(formatter.string(from: timestamp))")
}

// v7 UUID 可以按时间排序
let v7List = (0..<5).map { _ in UUIDUtils.generateV7() }
print("排序前的 v7 UUID:")
for u in v7List {
    print("  - \(u)")
}
let sortedV7 = v7List.sorted { UUIDUtils.compare($0, $1) == .orderedAscending }
print("排序后的 v7 UUID:")
for u in sortedV7 {
    print("  - \(u)")
}

// ========================================
// 3. UUID v5 (确定性生成)
// ========================================

print("\n=== UUID v5 ===")

// 使用 DNS 命名空间
let dnsUUID = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "example.com")
print("DNS UUID: \(dnsUUID)")

// 相同输入产生相同输出
let dnsUUID2 = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "example.com")
print("相同输入: \(dnsUUID2)")
print("是否相同: \(dnsUUID == dnsUUID2)")

// 不同输入产生不同输出
let differentUUID = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "different.com")
print("不同输入: \(differentUUID)")
print("是否不同: \(dnsUUID != differentUUID)")

// 使用 URL 命名空间
let urlUUID = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceURL, name: "https://example.com/path")
print("URL UUID: \(urlUUID)")

// ========================================
// 4. UUID 验证
// ========================================

print("\n=== UUID 验证 ===")

let validUUID = "550e8400-e29b-41d4-a716-446655440000"
let compactUUID = "550e8400e29b41d4a716446655440000"
let invalidUUID = "not-a-uuid"

print("\(validUUID) 有效: \(UUIDUtils.isValid(validUUID))")
print("\(compactUUID) 有效(严格): \(UUIDUtils.isValid(compactUUID))")
print("\(compactUUID) 有效(宽松): \(UUIDUtils.isValidLoose(compactUUID))")
print("\(invalidUUID) 有效: \(UUIDUtils.isValid(invalidUUID))")

// 解析 UUID
if let parsed = UUIDUtils.parseLoose(compactUUID) {
    print("解析结果: \(parsed.uuidString)")
}

// ========================================
// 5. 版本检测
// ========================================

print("\n=== 版本检测 ===")

let v4 = UUID().uuidString
let v7uuid = UUIDUtils.generateV7()
let v5uuid = UUIDUtils.generateV5(namespace: UUIDUtils.namespaceDNS, name: "test")

print("v4 UUID: \(v4), 版本: \(UUIDUtils.getVersion(v4)!)")
print("v5 UUID: \(v5uuid), 版本: \(UUIDUtils.getVersion(v5uuid)!)")
print("v7 UUID: \(v7uuid), 版本: \(UUIDUtils.getVersion(v7uuid)!)")

print("v4 是版本4: \(UUIDUtils.isV4(v4))")
print("v7 是版本7: \(UUIDUtils.isV7(v7uuid))")

// ========================================
// 6. 格式转换
// ========================================

print("\n=== 格式转换 ===")

let standard = "550e8400-e29b-41d4-a716-446655440000"

// 移除连字符
if let compact = UUIDUtils.removeHyphens(standard) {
    print("无连字符: \(compact)")
}

// 添加连字符
if let withHyphens = UUIDUtils.addHyphens(compact) {
    print("有连字符: \(withHyphens)")
}

// 大小写转换
if let upper = UUIDUtils.toUppercase(standard) {
    print("大写: \(upper)")
}
if let lower = UUIDUtils.toLowercase(upper) {
    print("小写: \(lower)")
}

// ========================================
// 7. 文本提取
// ========================================

print("\n=== 文本提取 ===")

let logText = """
[2024-01-15 10:30:45] User login: 550e8400-e29b-41d4-a716-446655440000
[2024-01-15 10:31:12] Order created: 6fa459ea-ee8a-3ca4-894e-db77e160355e
[2024-01-15 10:32:00] Payment processed: 123e4567-e89b-12d3-a456-426614174000
"""

let extracted = UUIDUtils.extract(from: logText)
print("提取到的 UUID:")
for u in extracted {
    print("  - \(u)")
}

if let first = UUIDUtils.extractFirst(from: logText) {
    print("第一个 UUID: \(first)")
}

// ========================================
// 8. UUID 比较
// ========================================

print("\n=== UUID 比较 ===")

let uuid1 = "550e8400-e29b-41d4-a716-446655440000"
let uuid2 = "550E8400-E29B-41D4-A716-446655440000"  // 大写
let uuid3 = "550e8400e29b41d4a716446655440000"     // 无连字符

// 相等比较（忽略大小写和连字符）
print("uuid1 == uuid2: \(UUIDUtils.areEqual(uuid1, uuid2)!)")
print("uuid1 == uuid3: \(UUIDUtils.areEqual(uuid1, uuid3)!)")

// 排序比较
let sortedUUIDs = [uuid1, uuid2, uuid3].sorted { 
    UUIDUtils.compare($0, $1) == .orderedAscending 
}
print("排序后的 UUID:")
for u in sortedUUIDs {
    print("  - \(u)")
}

// ========================================
// 9. 短 UUID
// ========================================

print("\n=== 短 UUID ===")

// Base62 编码短 UUID
let short = UUIDUtils.generateShort()
print("短 UUID: \(short)")

// 指定长度
let short8 = UUIDUtils.generateShort(length: 8)
print("8字符短 ID: \(short8)")

let short12 = UUIDUtils.generateShort(length: 12)
print("12字符短 ID: \(short12)")

// ========================================
// 10. Nil UUID
// ========================================

print("\n=== Nil UUID ===")

let nilUUID = UUIDUtils.nilUUID()
print("Nil UUID: \(nilUUID)")
print("是否为 Nil: \(UUIDUtils.isNil(nilUUID))")

// ========================================
// 11. String 扩展
// ========================================

print("\n=== String 扩展 ===")

let testUUID = "550e8400-e29b-41d4-a716-446655440000"
print("有效 UUID: \(testUUID.isValidUUID)")
print("UUID 值: \(testUUID.uuidValue?.uuidString ?? "nil")")
print("简化: \(testUUID.uuidSimplified ?? "nil")")

let compactStr = "550e8400e29b41d4a716446655440000"
print("宽松有效: \(compactStr.isValidUUIDLoose)")
print("格式化: \(compactStr.uuidFormatted ?? "nil")")

print("\n=== 示例完成 ===")