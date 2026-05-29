/**
 * AllToolkit - Swift SemVer Utilities Example
 *
 * 基本使用示例
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - 基本解析示例

print("=== 基本解析示例 ===")

// 解析标准版本
let v1 = SemVerUtils.parse("1.2.3")
print("解析 '1.2.3': \(v1?.fullVersion ?? "无效")")

// 解析带前缀版本
let v2 = SemVerUtils.parse("v2.0.0")
print("解析 'v2.0.0': \(v2?.fullVersion ?? "无效")")

// 解析预发布版本
let v3 = SemVerUtils.parse("1.0.0-beta.1")
print("解析 '1.0.0-beta.1': \(v3?.fullVersion ?? "无效")")
print("是否为预发布版本: \(v3?.isPrerelease ?? false)")

// 解析带构建元数据版本
let v4 = SemVerUtils.parse("1.0.0+build.123")
print("解析 '1.0.0+build.123': \(v4?.fullVersion ?? "无效")")

// 宽松解析
let v5 = SemVerUtils.parseLoose("1")
print("宽松解析 '1': \(v5?.fullVersion ?? "无效")")

print("")

// MARK: - 版本比较示例

print("=== 版本比较示例 ===")

// 基本比较
let compare1 = SemVerUtils.compare("1.0.0", "2.0.0")
print("比较 1.0.0 vs 2.0.0: \(compare1 == .orderedAscending ? "小于" : compare1 == .orderedDescending ? "大于" : "相等")")

// 比较方法
let isGreater = SemVerUtils.isGreater("2.0.0", than: "1.0.0")
print("2.0.0 > 1.0.0: \(isGreater ?? false)")

// 预发布版本比较
let compare2 = SemVerUtils.compare("1.0.0-alpha", "1.0.0")
print("比较 1.0.0-alpha vs 1.0.0: \(compare2 == .orderedAscending ? "小于" : "大于")")
print("(预发布版本优先级低于正式版本)")

let compare3 = SemVerUtils.compare("1.0.0-alpha.1", "1.0.0-alpha.2")
print("比较 1.0.0-alpha.1 vs 1.0.0-alpha.2: \(compare3 == .orderedAscending ? "小于" : "大于")")

print("")

// MARK: - 版本排序示例

print("=== 版本排序示例 ===")

let versions = ["3.0.0", "1.0.0-alpha", "1.0.0", "2.0.0", "1.1.0", "1.0.0-beta"]
print("原始版本列表: \(versions)")

let sorted = SemVerUtils.sortStrings(versions)
print("排序后: \(sorted)")

let latest = SemVerUtils.latest(versions)
print("最新版本: \(latest?.fullVersion ?? "无")")

let oldest = SemVerUtils.oldest(versions)
print("最旧版本: \(oldest?.fullVersion ?? "无")")

print("")

// MARK: - 约束检查示例

print("=== 约束检查示例 ===")

// 精确匹配
let exactMatch = SemVerUtils.satisfies("1.2.3", constraint: "1.2.3")
print("1.2.3 精确匹配 1.2.3: \(exactMatch ?? false)")

// 比较操作符
let greaterThan = SemVerUtils.satisfies("1.5.0", constraint: ">=1.0.0")
print("1.5.0 >= 1.0.0: \(greaterThan ?? false)")

let lessThan = SemVerUtils.satisfies("0.9.0", constraint: "<1.0.0")
print("0.9.0 < 1.0.0: \(lessThan ?? false)")

// 脱字符约束 (^)
let caretMatch = SemVerUtils.satisfies("1.5.0", constraint: "^1.0.0")
print("1.5.0 匹配 ^1.0.0: \(caretMatch ?? false)")

let caretFail = SemVerUtils.satisfies("2.0.0", constraint: "^1.0.0")
print("2.0.0 匹配 ^1.0.0: \(caretFail ?? false)")

// 波浪号约束 (~)
let tildeMatch = SemVerUtils.satisfies("1.2.9", constraint: "~1.2.3")
print("1.2.9 匹配 ~1.2.3: \(tildeMatch ?? false)")

let tildeFail = SemVerUtils.satisfies("1.3.0", constraint: "~1.2.3")
print("1.3.0 匹配 ~1.2.3: \(tildeFail ?? false)")

// X 范围
let xRangeMatch = SemVerUtils.satisfies("1.5.0", constraint: "1.x")
print("1.5.0 匹配 1.x: \(xRangeMatch ?? false)")

print("")

// MARK: - 版本递增示例

print("=== 版本递增示例 ===")

let original = "1.2.3"
print("原始版本: \(original)")

let majorInc = SemVerUtils.incrementMajor(original)
print("递增主版本: \(majorInc?.fullVersion ?? "无效")")

let minorInc = SemVerUtils.incrementMinor(original)
print("递增次版本: \(minorInc?.fullVersion ?? "无效")")

let patchInc = SemVerUtils.incrementPatch(original)
print("递增补丁版本: \(patchInc?.fullVersion ?? "无效")")

let withPrerelease = SemVerUtils.setPrerelease(original, prerelease: "beta.1")
print("设置预发布: \(withPrerelease?.fullVersion ?? "无效")")

let withoutPrerelease = SemVerUtils.removePrerelease("1.2.3-beta.1")
print("移除预发布: \(withoutPrerelease?.fullVersion ?? "无效")")

print("")

// MARK: - 版本差异示例

print("=== 版本差异示例 ===")

let diff1 = SemVerUtils.diff("1.0.0", "2.0.0")
print("1.0.0 -> 2.0.0: \(diff1?.rawValue ?? "无效")")

let diff2 = SemVerUtils.diff("1.0.0", "1.1.0")
print("1.0.0 -> 1.1.0: \(diff2?.rawValue ?? "无效")")

let diff3 = SemVerUtils.diff("1.0.0", "1.0.1")
print("1.0.0 -> 1.0.1: \(diff3?.rawValue ?? "无效")")

let diff4 = SemVerUtils.diff("1.0.0-alpha", "1.0.0-beta")
print("1.0.0-alpha -> 1.0.0-beta: \(diff4?.rawValue ?? "无效")")

print("")

// MARK: - 版本提取示例

print("=== 版本提取示例 ===")

let text = "项目依赖: v1.2.3 (核心), v2.0.0-beta (实验), v0.1.0 (已弃用)"
print("文本: \(text)")

let extracted = SemVerUtils.extract(from: text)
print("提取到的版本: \(extracted.map { $0.fullVersion })")

let firstExtracted = SemVerUtils.extractFirst(from: text)
print("第一个版本: \(firstExtracted?.fullVersion ?? "无")")

print("")

// MARK: - String 扩展示例

print("=== String 扩展示例 ===")

let versionStr = "1.2.3"
print("字符串: \(versionStr)")
print("解析为 SemVer: \(versionStr.semver?.fullVersion ?? "无效")")
print("是否有效: \(versionStr.isValidSemVer)")
print("满足 >=1.0.0: \(versionStr.satisfiesSemVer(">=1.0.0") ?? false)")

print("")

// MARK: - Array 扩展示例

print("=== Array 扩展示例 ===")

let versionArray = ["3.0.0", "1.0.0", "2.0.0", "1.5.0"]
print("数组: \(versionArray)")
print("排序后: \(versionArray.sortedSemVer)")
print("最新版本: \(versionArray.latestSemVer?.fullVersion ?? "无")")
print("最旧版本: \(versionArray.oldestSemVer?.fullVersion ?? "无")")

print("")

// MARK: - SemVer 结构体示例

print("=== SemVer 结构体示例 ===")

let semver = SemVerUtils.parse("2.3.4-beta.2+build.789")!
print("版本: \(semver.fullVersion)")
print("主版本: \(semver.major)")
print("次版本: \(semver.minor)")
print("补丁版本: \(semver.patch)")
print("预发布: \(semver.prerelease ?? "无")")
print("构建元数据: \(semver.buildMetadata ?? "无")")
print("核心版本: \(semver.coreVersion)")
print("是否稳定: \(semver.isStable)")
print("是否预发布: \(semver.isPrerelease)")

print("")

// MARK: - 工厂方法示例

print("=== 工厂方法示例 ===")

print("初始版本: \(SemVerUtils.initial().fullVersion)")
print("零版本: \(SemVerUtils.zero().fullVersion)")
print("快速创建 1.0.0: \(SemVerUtils.version(1).fullVersion)")
print("快速创建 1.2.0: \(SemVerUtils.version(1, 2).fullVersion)")
print("快速创建 1.2.3: \(SemVerUtils.version(1, 2, 3).fullVersion)")

print("")
print("=== 示例完成 ===")