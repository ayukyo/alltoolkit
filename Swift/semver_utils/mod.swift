/**
 * AllToolkit - Swift SemVer Utilities
 *
 * 语义版本控制工具类，提供版本解析、比较、验证和操作功能。
 * 完全符合 Semantic Versioning 2.0.0 规范。
 * 零依赖，仅使用 Swift 标准库和 Foundation 框架。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - SemVer 结构体

/// 语义版本号结构体，符合 SemVer 2.0.0 规范
public struct SemVer: Equatable, Comparable, Hashable, Codable {
    
    /// 主版本号（不兼容的 API 变更）
    public let major: Int
    
    /// 次版本号（向后兼容的功能新增）
    public let minor: Int
    
    /// 补丁版本号（向后兼容的问题修复）
    public let patch: Int
    
    /// 预发布标识符（如 "alpha", "beta.1", "rc.2"）
    public let prerelease: String?
    
    /// 构建元数据（如 "build.123", "20240101"）
    public let buildMetadata: String?
    
    /// 原始版本字符串
    public let original: String?
    
    // MARK: - 初始化
    
    /// 初始化语义版本
    /// - Parameters:
    ///   - major: 主版本号
    ///   - minor: 次版本号
    ///   - patch: 补丁版本号
    ///   - prerelease: 预发布标识符
    ///   - buildMetadata: 构建元数据
    ///   - original: 原始字符串
    public init(
        major: Int,
        minor: Int = 0,
        patch: Int = 0,
        prerelease: String? = nil,
        buildMetadata: String? = nil,
        original: String? = nil
    ) {
        self.major = max(0, major)
        self.minor = max(0, minor)
        self.patch = max(0, patch)
        self.prerelease = prerelease?.isEmpty == true ? nil : prerelease
        self.buildMetadata = buildMetadata?.isEmpty == true ? nil : buildMetadata
        self.original = original
    }
    
    // MARK: - 计算属性
    
    /// 是否为预发布版本
    public var isPrerelease: Bool {
        return prerelease != nil
    }
    
    /// 是否为稳定版本
    public var isStable: Bool {
        return prerelease == nil
    }
    
    /// 主版本号字符串表示（不含预发布和构建信息）
    public var coreVersion: String {
        return "\(major).\(minor).\(patch)"
    }
    
    /// 完整版本字符串
    public var fullVersion: String {
        var result = coreVersion
        if let pre = prerelease {
            result += "-\(pre)"
        }
        if let build = buildMetadata {
            result += "+\(build)"
        }
        return result
    }
    
    // MARK: - Comparable
    
    public static func < (lhs: SemVer, rhs: SemVer) -> Bool {
        // 比较主版本号
        if lhs.major != rhs.major {
            return lhs.major < rhs.major
        }
        // 比较次版本号
        if lhs.minor != rhs.minor {
            return lhs.minor < rhs.minor
        }
        // 比较补丁版本号
        if lhs.patch != rhs.patch {
            return lhs.patch < rhs.patch
        }
        
        // 预发布版本优先级低于正式版本
        // 有预发布标识符 < 无预发布标识符
        if lhs.prerelease == nil && rhs.prerelease != nil {
            return false
        }
        if lhs.prerelease != nil && rhs.prerelease == nil {
            return true
        }
        
        // 都有预发布标识符时，按标识符比较
        if let lhsPre = lhs.prerelease, let rhsPre = rhs.prerelease {
            return comparePrerelease(lhsPre, rhsPre) < 0
        }
        
        return false
    }
    
    // MARK: - Equatable (自动合成，但构建元数据不参与比较)
    
    public static func == (lhs: SemVer, rhs: SemVer) -> Bool {
        return lhs.major == rhs.major &&
               lhs.minor == rhs.minor &&
               lhs.patch == rhs.patch &&
               lhs.prerelease == rhs.prerelease
        // 注意：buildMetadata 不参与相等比较
    }
    
    // MARK: - 预发布标识符比较
    
    /// 比较预发布标识符
    /// - Returns: 负数表示 lhs < rhs，0 表示相等，正数表示 lhs > rhs
    private static func comparePrerelease(_ lhs: String, _ rhs: String) -> Int {
        let lhsParts = lhs.split(separator: ".").map { String($0) }
        let rhsParts = rhs.split(separator: ".").map { String($0) }
        
        for i in 0..<max(lhsParts.count, rhsParts.count) {
            // 较少标识符的版本优先级较低
            if i >= lhsParts.count {
                return -1
            }
            if i >= rhsParts.count {
                return 1
            }
            
            let lhsPart = lhsParts[i]
            let rhsPart = rhsParts[i]
            
            let lhsIsNum = Int(lhsPart) != nil
            let rhsIsNum = Int(rhsPart) != nil
            
            // 数字标识符比字符串标识符优先级低
            if lhsIsNum && !rhsIsNum {
                return -1
            }
            if !lhsIsNum && rhsIsNum {
                return 1
            }
            
            if lhsIsNum && rhsIsNum {
                // 数值比较
                let lhsNum = Int(lhsPart)!
                let rhsNum = Int(rhsPart)!
                if lhsNum != rhsNum {
                    return lhsNum < rhsNum ? -1 : 1
                }
            } else {
                // 字符串比较
                if lhsPart != rhsPart {
                    return lhsPart < rhsPart ? -1 : 1
                }
            }
        }
        
        return 0
    }
}

// MARK: - SemVerUtils 主类

/// 语义版本工具类
public enum SemVerUtils {
    
    // MARK: - 版本解析
    
    /// 解析版本字符串
    /// - Parameter version: 版本字符串
    /// - Returns: SemVer 对象，解析失败返回 nil
    public static func parse(_ version: String) -> SemVer? {
        let trimmed = version.trimmingCharacters(in: .whitespaces)
        let pattern = #"^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*))?(?:\+([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*))?$"#
        
        guard let regex = try? NSRegularExpression(pattern: pattern),
              let match = regex.firstMatch(in: trimmed, range: NSRange(trimmed.startIndex..., in: trimmed)) else {
            return nil
        }
        
        func extractGroup(_ index: Int) -> String? {
            guard match.range(at: index).location != NSNotFound,
                  let range = Range(match.range(at: index), in: trimmed) else {
                return nil
            }
            return String(trimmed[range])
        }
        
        guard let majorStr = extractGroup(1),
              let minorStr = extractGroup(2),
              let patchStr = extractGroup(3),
              let major = Int(majorStr),
              let minor = Int(minorStr),
              let patch = Int(patchStr) else {
            return nil
        }
        
        let prerelease = extractGroup(4)
        let buildMetadata = extractGroup(5)
        
        return SemVer(
            major: major,
            minor: minor,
            patch: patch,
            prerelease: prerelease,
            buildMetadata: buildMetadata,
            original: version
        )
    }
    
    /// 宽松解析版本字符串（支持不完整版本）
    /// - Parameter version: 版本字符串
    /// - Returns: SemVer 对象
    public static func parseLoose(_ version: String) -> SemVer? {
        let trimmed = version.trimmingCharacters(in: .whitespaces)
        
        // 先尝试标准解析
        if let semver = parse(trimmed) {
            return semver
        }
        
        // 宽松模式：支持 "1", "1.2", "v1.2" 等格式
        let digits = trimmed.filter { $0.isNumber || $0 == "." }
        let parts = digits.split(separator: ".").compactMap { Int(String($0)) }
        
        guard !parts.isEmpty else { return nil }
        
        let major = parts.count > 0 ? parts[0] : 0
        let minor = parts.count > 1 ? parts[1] : 0
        let patch = parts.count > 2 ? parts[2] : 0
        
        return SemVer(major: major, minor: minor, patch: patch, original: version)
    }
    
    // MARK: - 版本验证
    
    /// 验证版本字符串是否有效
    /// - Parameter version: 版本字符串
    /// - Returns: 是否为有效的语义版本
    public static func isValid(_ version: String) -> Bool {
        return parse(version) != nil
    }
    
    /// 验证版本字符串是否为有效或宽松有效
    /// - Parameter version: 版本字符串
    /// - Returns: 是否可解析
    public static func isValidLoose(_ version: String) -> Bool {
        return parseLoose(version) != nil
    }
    
    // MARK: - 版本比较
    
    /// 比较两个版本
    /// - Parameters:
    ///   - v1: 第一个版本
    ///   - v2: 第二个版本
    /// - Returns: 比较结果，任一无效返回 nil
    public static func compare(_ v1: String, _ v2: String) -> ComparisonResult? {
        guard let semver1 = parse(v1), let semver2 = parse(v2) else { return nil }
        
        if semver1 < semver2 {
            return .orderedAscending
        } else if semver1 > semver2 {
            return .orderedDescending
        } else {
            return .orderedSame
        }
    }
    
    /// 判断 v1 是否大于 v2
    /// - Returns: v1 > v2，任一无效返回 nil
    public static func isGreater(_ v1: String, than v2: String) -> Bool? {
        guard let semver1 = parse(v1), let semver2 = parse(v2) else { return nil }
        return semver1 > semver2
    }
    
    /// 判断 v1 是否大于等于 v2
    /// - Returns: v1 >= v2，任一无效返回 nil
    public static func isGreaterOrEqual(_ v1: String, to v2: String) -> Bool? {
        guard let semver1 = parse(v1), let semver2 = parse(v2) else { return nil }
        return semver1 >= semver2
    }
    
    /// 判断 v1 是否小于 v2
    /// - Returns: v1 < v2，任一无效返回 nil
    public static func isLess(_ v1: String, than v2: String) -> Bool? {
        guard let semver1 = parse(v1), let semver2 = parse(v2) else { return nil }
        return semver1 < semver2
    }
    
    /// 判断 v1 是否小于等于 v2
    /// - Returns: v1 <= v2，任一无效返回 nil
    public static func isLessOrEqual(_ v1: String, to v2: String) -> Bool? {
        guard let semver1 = parse(v1), let semver2 = parse(v2) else { return nil }
        return semver1 <= semver2
    }
    
    /// 判断两个版本是否相等
    /// - Returns: v1 == v2，任一无效返回 nil
    public static func isEqual(_ v1: String, _ v2: String) -> Bool? {
        guard let semver1 = parse(v1), let semver2 = parse(v2) else { return nil }
        return semver1 == semver2
    }
    
    // MARK: - 版本排序
    
    /// 对版本列表排序
    /// - Parameter versions: 版本字符串数组
    /// - Returns: 排序后的 SemVer 数组（无效版本被过滤）
    public static func sort(_ versions: [String]) -> [SemVer] {
        return versions.compactMap { parse($0) }.sorted()
    }
    
    /// 对版本列表排序（返回字符串）
    /// - Parameter versions: 版本字符串数组
    /// - Returns: 排序后的版本字符串数组
    public static func sortStrings(_ versions: [String]) -> [String] {
        return sort(versions).map { $0.fullVersion }
    }
    
    /// 获取最新版本
    /// - Parameter versions: 版本字符串数组
    /// - Returns: 最新版本，空数组返回 nil
    public static func latest(_ versions: [String]) -> SemVer? {
        return sort(versions).last
    }
    
    /// 获取最旧版本
    /// - Parameter versions: 版本字符串数组
    /// - Returns: 最旧版本，空数组返回 nil
    public static func oldest(_ versions: [String]) -> SemVer? {
        return sort(versions).first
    }
    
    // MARK: - 版本范围检查
    
    /// 检查版本是否在范围内
    /// - Parameters:
    ///   - version: 待检查版本
    ///   - min: 最小版本（包含）
    ///   - max: 最大版本（包含）
    /// - Returns: 是否在范围内
    public static func isInRange(_ version: String, min: String, max: String) -> Bool? {
        guard let v = parse(version),
              let minV = parse(min),
              let maxV = parse(max) else { return nil }
        return v >= minV && v <= maxV
    }
    
    /// 检查版本是否满足约束
    /// - Parameters:
    ///   - version: 版本字符串
    ///   - constraint: 约束字符串（如 ">=1.0.0", "^1.2.3", "~2.0.0"）
    /// - Returns: 是否满足约束
    public static func satisfies(_ version: String, constraint: String) -> Bool? {
        guard let semver = parse(version) else { return nil }
        
        let constraint = constraint.trimmingCharacters(in: .whitespaces)
        
        // 精确匹配
        if constraint.first?.isNumber ?? false {
            guard let target = parse(constraint) else { return nil }
            return semver == target
        }
        
        // 带操作符的约束
        if constraint.hasPrefix(">=") {
            guard let target = parse(String(constraint.dropFirst(2))) else { return nil }
            return semver >= target
        }
        
        if constraint.hasPrefix("<=") {
            guard let target = parse(String(constraint.dropFirst(2))) else { return nil }
            return semver <= target
        }
        
        if constraint.hasPrefix(">") {
            guard let target = parse(String(constraint.dropFirst(1))) else { return nil }
            return semver > target
        }
        
        if constraint.hasPrefix("<") {
            guard let target = parse(String(constraint.dropFirst(1))) else { return nil }
            return semver < target
        }
        
        if constraint.hasPrefix("=") {
            guard let target = parse(String(constraint.dropFirst(1))) else { return nil }
            return semver == target
        }
        
        // 脱字符约束 (^) - 允许次版本和补丁版本变更
        if constraint.hasPrefix("^") {
            guard let target = parse(String(constraint.dropFirst(1))) else { return nil }
            if target.major == 0 {
                // ^0.x.y 允许补丁变更
                return semver.major == 0 && semver.minor == target.minor && semver.patch >= target.patch
            }
            return semver.major == target.major && semver >= target
        }
        
        // 波浪号约束 (~) - 只允许补丁版本变更
        if constraint.hasPrefix("~") {
            guard let target = parse(String(constraint.dropFirst(1))) else { return nil }
            return semver.major == target.major && semver.minor == target.minor && semver.patch >= target.patch
        }
        
        // X 范围 (1.2.x, 1.x)
        let xPattern = constraint.lowercased().replacingOccurrences(of: "*", with: "x")
        if xPattern.contains("x") {
            return satisfiesXRange(semver, pattern: xPattern)
        }
        
        return nil
    }
    
    /// 处理 X 范围约束
    private static func satisfiesXRange(_ semver: SemVer, pattern: String) -> Bool {
        let parts = pattern.split(separator: ".").map { String($0) }
        
        if parts.isEmpty { return true }
        
        // 主版本
        if parts[0].lowercased() != "x" {
            guard let major = Int(parts[0]), semver.major == major else { return false }
        }
        
        if parts.count < 2 { return true }
        
        // 次版本
        if parts[1].lowercased() != "x" {
            guard let minor = Int(parts[1]), semver.minor == minor else { return false }
        }
        
        if parts.count < 3 { return true }
        
        // 补丁版本
        if parts[2].lowercased() != "x" {
            guard let patch = Int(parts[2]), semver.patch == patch else { return false }
        }
        
        return true
    }
    
    // MARK: - 版本递增
    
    /// 递增主版本号
    /// - Parameter version: 版本字符串
    /// - Returns: 递增后的 SemVer，无效返回 nil
    public static func incrementMajor(_ version: String) -> SemVer? {
        guard let semver = parse(version) else { return nil }
        return SemVer(major: semver.major + 1, minor: 0, patch: 0)
    }
    
    /// 递增次版本号
    /// - Parameter version: 版本字符串
    /// - Returns: 递增后的 SemVer，无效返回 nil
    public static func incrementMinor(_ version: String) -> SemVer? {
        guard let semver = parse(version) else { return nil }
        return SemVer(major: semver.major, minor: semver.minor + 1, patch: 0)
    }
    
    /// 递增补丁版本号
    /// - Parameter version: 版本字符串
    /// - Returns: 递增后的 SemVer，无效返回 nil
    public static func incrementPatch(_ version: String) -> SemVer? {
        guard let semver = parse(version) else { return nil }
        return SemVer(major: semver.major, minor: semver.minor, patch: semver.patch + 1)
    }
    
    /// 设置预发布标识符
    /// - Parameters:
    ///   - version: 版本字符串
    ///   - prerelease: 预发布标识符
    /// - Returns: 新的 SemVer，无效返回 nil
    public static func setPrerelease(_ version: String, prerelease: String) -> SemVer? {
        guard let semver = parse(version) else { return nil }
        return SemVer(
            major: semver.major,
            minor: semver.minor,
            patch: semver.patch,
            prerelease: prerelease
        )
    }
    
    /// 移除预发布标识符
    /// - Parameter version: 版本字符串
    /// - Returns: 新的 SemVer，无效返回 nil
    public static func removePrerelease(_ version: String) -> SemVer? {
        guard let semver = parse(version) else { return nil }
        return SemVer(
            major: semver.major,
            minor: semver.minor,
            patch: semver.patch
        )
    }
    
    // MARK: - 版本差异
    
    /// 计算两个版本的差异类型
    /// - Parameters:
    ///   - v1: 旧版本
    ///   - v2: 新版本
    /// - Returns: 差异类型，任一无效返回 nil
    public static func diff(_ v1: String, _ v2: String) -> SemVerDiff? {
        guard let semver1 = parse(v1), let semver2 = parse(v2) else { return nil }
        
        if semver1 == semver2 {
            return .none
        }
        
        if semver2.major > semver1.major {
            return .major
        }
        
        if semver2.minor > semver1.minor {
            return .minor
        }
        
        if semver2.patch > semver1.patch {
            return .patch
        }
        
        // 版本降低了或预发布变化
        if semver2 < semver1 {
            return .downgrade
        }
        
        return .prerelease
    }
    
    // MARK: - 版本提取
    
    /// 从字符串中提取所有版本号
    /// - Parameter text: 包含版本的文本
    /// - Returns: SemVer 数组
    public static func extract(from text: String) -> [SemVer] {
        let pattern = #"v?\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?(?:\+[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?"#
        
        guard let regex = try? NSRegularExpression(pattern: pattern) else { return [] }
        
        let range = NSRange(location: 0, length: text.utf16.count)
        let matches = regex.matches(in: text, options: [], range: range)
        
        return matches.compactMap { match in
            guard let range = Range(match.range, in: text) else { return nil }
            return parse(String(text[range]))
        }
    }
    
    /// 从字符串中提取第一个版本号
    /// - Parameter text: 包含版本的文本
    /// - Returns: 第一个 SemVer，未找到返回 nil
    public static func extractFirst(from text: String) -> SemVer? {
        return extract(from: text).first
    }
    
    // MARK: - 工厂方法
    
    /// 创建初始版本 (0.0.1)
    public static func initial() -> SemVer {
        return SemVer(major: 0, minor: 0, patch: 1)
    }
    
    /// 创建零版本 (0.0.0)
    public static func zero() -> SemVer {
        return SemVer(major: 0, minor: 0, patch: 0)
    }
    
    /// 创建版本
    /// - Parameter major: 主版本号
    /// - Returns: SemVer 实例
    public static func version(_ major: Int, _ minor: Int = 0, _ patch: Int = 0) -> SemVer {
        return SemVer(major: major, minor: minor, patch: patch)
    }
}

// MARK: - 差异类型枚举

/// 版本差异类型
public enum SemVerDiff: String, CaseIterable {
    case none = "无变化"
    case patch = "补丁更新"
    case minor = "次版本更新"
    case major = "主版本更新"
    case prerelease = "预发布变化"
    case downgrade = "版本降级"
}

// MARK: - String 扩展

public extension String {
    /// 解析为 SemVer
    var semver: SemVer? {
        return SemVerUtils.parse(self)
    }
    
    /// 宽松解析为 SemVer
    var semverLoose: SemVer? {
        return SemVerUtils.parseLoose(self)
    }
    
    /// 是否为有效语义版本
    var isValidSemVer: Bool {
        return SemVerUtils.isValid(self)
    }
    
    /// 是否满足约束
    func satisfiesSemVer(_ constraint: String) -> Bool? {
        return SemVerUtils.satisfies(self, constraint: constraint)
    }
}

// MARK: - Array 扩展

public extension Array where Element == String {
    /// 排序版本字符串
    var sortedSemVer: [String] {
        return SemVerUtils.sortStrings(self)
    }
    
    /// 获取最新版本
    var latestSemVer: SemVer? {
        return SemVerUtils.latest(self)
    }
    
    /// 获取最旧版本
    var oldestSemVer: SemVer? {
        return SemVerUtils.oldest(self)
    }
}