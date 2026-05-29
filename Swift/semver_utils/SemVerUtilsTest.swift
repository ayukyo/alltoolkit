/**
 * AllToolkit - Swift SemVerUtils Test
 * 
 * 语义版本工具类测试
 * 覆盖: 解析、比较、验证、范围检查、版本递增
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation
import XCTest

class SemVerUtilsTest: XCTestCase {
    
    // MARK: - 版本解析测试
    
    /// 测试基本解析
    func testParse() {
        let v = SemVerUtils.parse("1.2.3")
        XCTAssertNotNil(v)
        XCTAssertEqual(v?.major, 1)
        XCTAssertEqual(v?.minor, 2)
        XCTAssertEqual(v?.patch, 3)
        XCTAssertNil(v?.prerelease)
        XCTAssertNil(v?.buildMetadata)
    }
    
    /// 测试带前缀解析
    func testParseWithPrefix() {
        let v = SemVerUtils.parse("v2.0.0")
        XCTAssertNotNil(v)
        XCTAssertEqual(v?.major, 2)
        XCTAssertEqual(v?.minor, 0)
        XCTAssertEqual(v?.patch, 0)
    }
    
    /// 测试预发布版本
    func testParsePrerelease() {
        let v1 = SemVerUtils.parse("1.0.0-alpha")
        XCTAssertNotNil(v1)
        XCTAssertEqual(v1?.prerelease, "alpha")
        XCTAssertFalse(v1!.isStable)
        XCTAssertTrue(v1!.isPrerelease)
        
        let v2 = SemVerUtils.parse("1.0.0-beta.1")
        XCTAssertEqual(v2?.prerelease, "beta.1")
        
        let v3 = SemVerUtils.parse("1.0.0-rc.1.2.3")
        XCTAssertEqual(v3?.prerelease, "rc.1.2.3")
    }
    
    /// 测试构建元数据
    func testParseBuildMetadata() {
        let v = SemVerUtils.parse("1.0.0+build.123")
        XCTAssertNotNil(v)
        XCTAssertEqual(v?.buildMetadata, "build.123")
        XCTAssertEqual(v?.prerelease, nil)
        
        let v2 = SemVerUtils.parse("1.0.0-alpha+build.456")
        XCTAssertEqual(v2?.prerelease, "alpha")
        XCTAssertEqual(v2?.buildMetadata, "build.456")
    }
    
    /// 测试完整版本
    func testParseFullVersion() {
        let v = SemVerUtils.parse("2.3.4-beta.2+build.789")
        XCTAssertNotNil(v)
        XCTAssertEqual(v?.major, 2)
        XCTAssertEqual(v?.minor, 3)
        XCTAssertEqual(v?.patch, 4)
        XCTAssertEqual(v?.prerelease, "beta.2")
        XCTAssertEqual(v?.buildMetadata, "build.789")
    }
    
    /// 测试无效版本
    func testParseInvalid() {
        XCTAssertNil(SemVerUtils.parse(""))
        XCTAssertNil(SemVerUtils.parse("invalid"))
        XCTAssertNil(SemVerUtils.parse("1"))
        XCTAssertNil(SemVerUtils.parse("1.2"))
        XCTAssertNil(SemVerUtils.parse("a.b.c"))
        XCTAssertNil(SemVerUtils.parse("-1.0.0"))
    }
    
    /// 测试宽松解析
    func testParseLoose() {
        let v1 = SemVerUtils.parseLoose("1")
        XCTAssertNotNil(v1)
        XCTAssertEqual(v1?.major, 1)
        XCTAssertEqual(v1?.minor, 0)
        XCTAssertEqual(v1?.patch, 0)
        
        let v2 = SemVerUtils.parseLoose("1.2")
        XCTAssertNotNil(v2)
        XCTAssertEqual(v2?.major, 1)
        XCTAssertEqual(v2?.minor, 2)
        
        let v3 = SemVerUtils.parseLoose("v1.2.3")
        XCTAssertEqual(v3?.major, 1)
        XCTAssertEqual(v3?.minor, 2)
        XCTAssertEqual(v3?.patch, 3)
    }
    
    // MARK: - 版本验证测试
    
    /// 测试验证
    func testIsValid() {
        XCTAssertTrue(SemVerUtils.isValid("1.0.0"))
        XCTAssertTrue(SemVerUtils.isValid("1.2.3"))
        XCTAssertTrue(SemVerUtils.isValid("0.0.1"))
        XCTAssertTrue(SemVerUtils.isValid("10.20.30"))
        XCTAssertTrue(SemVerUtils.isValid("1.0.0-alpha"))
        XCTAssertTrue(SemVerUtils.isValid("1.0.0+build"))
        XCTAssertTrue(SemVerUtils.isValid("v1.0.0"))
        
        XCTAssertFalse(SemVerUtils.isValid(""))
        XCTAssertFalse(SemVerUtils.isValid("1"))
        XCTAssertFalse(SemVerUtils.isValid("1.2"))
        XCTAssertFalse(SemVerUtils.isValid("invalid"))
    }
    
    /// 测试宽松验证
    func testIsValidLoose() {
        XCTAssertTrue(SemVerUtils.isValidLoose("1.0.0"))
        XCTAssertTrue(SemVerUtils.isValidLoose("1"))
        XCTAssertTrue(SemVerUtils.isValidLoose("1.2"))
        XCTAssertTrue(SemVerUtils.isValidLoose("v1.2.3"))
        
        XCTAssertFalse(SemVerUtils.isValidLoose(""))
        XCTAssertFalse(SemVerUtils.isValidLoose("invalid"))
    }
    
    // MARK: - SemVer 结构体测试
    
    /// 测试核心版本
    func testCoreVersion() {
        let v = SemVerUtils.parse("1.2.3-beta+build")!
        XCTAssertEqual(v.coreVersion, "1.2.3")
    }
    
    /// 测试完整版本
    func testFullVersion() {
        let v1 = SemVerUtils.parse("1.2.3")!
        XCTAssertEqual(v1.fullVersion, "1.2.3")
        
        let v2 = SemVerUtils.parse("1.2.3-alpha")!
        XCTAssertEqual(v2.fullVersion, "1.2.3-alpha")
        
        let v3 = SemVerUtils.parse("1.2.3-beta+build")!
        XCTAssertEqual(v3.fullVersion, "1.2.3-beta+build")
    }
    
    /// 测试稳定/预发布判断
    func testStablePrerelease() {
        let stable = SemVerUtils.parse("1.0.0")!
        XCTAssertTrue(stable.isStable)
        XCTAssertFalse(stable.isPrerelease)
        
        let prerelease = SemVerUtils.parse("1.0.0-alpha")!
        XCTAssertFalse(prerelease.isStable)
        XCTAssertTrue(prerelease.isPrerelease)
    }
    
    // MARK: - 版本比较测试
    
    /// 测试基本比较
    func testCompare() {
        XCTAssertEqual(SemVerUtils.compare("1.0.0", "1.0.0"), .orderedSame)
        XCTAssertEqual(SemVerUtils.compare("1.0.0", "2.0.0"), .orderedAscending)
        XCTAssertEqual(SemVerUtils.compare("2.0.0", "1.0.0"), .orderedDescending)
        XCTAssertEqual(SemVerUtils.compare("1.0.0", "1.1.0"), .orderedAscending)
        XCTAssertEqual(SemVerUtils.compare("1.0.0", "1.0.1"), .orderedAscending)
        
        XCTAssertNil(SemVerUtils.compare("invalid", "1.0.0"))
    }
    
    /// 测试预发布比较
    func testComparePrerelease() {
        // 预发布版本低于正式版本
        XCTAssertEqual(SemVerUtils.compare("1.0.0-alpha", "1.0.0"), .orderedAscending)
        XCTAssertEqual(SemVerUtils.compare("1.0.0", "1.0.0-alpha"), .orderedDescending)
        
        // 预发布标识符比较
        XCTAssertEqual(SemVerUtils.compare("1.0.0-alpha", "1.0.0-beta"), .orderedAscending)
        XCTAssertEqual(SemVerUtils.compare("1.0.0-alpha.1", "1.0.0-alpha.2"), .orderedAscending)
        XCTAssertEqual(SemVerUtils.compare("1.0.0-alpha.1", "1.0.0-alpha.beta"), .orderedAscending)
    }
    
    /// 测试比较方法
    func testComparisonMethods() {
        XCTAssertTrue(SemVerUtils.isGreater("2.0.0", than: "1.0.0")!)
        XCTAssertTrue(SemVerUtils.isLess("1.0.0", than: "2.0.0")!)
        XCTAssertTrue(SemVerUtils.isGreaterOrEqual("2.0.0", to: "2.0.0")!)
        XCTAssertTrue(SemVerUtils.isLessOrEqual("1.0.0", to: "1.0.0")!)
        XCTAssertTrue(SemVerUtils.isEqual("1.0.0", "1.0.0")!)
        
        XCTAssertNil(SemVerUtils.isGreater("invalid", than: "1.0.0"))
    }
    
    /// 测试 SemVer Comparable
    func testSemVerComparable() {
        let v1 = SemVerUtils.parse("1.0.0")!
        let v2 = SemVerUtils.parse("2.0.0")!
        let v3 = SemVerUtils.parse("1.0.0")!
        
        XCTAssertTrue(v1 < v2)
        XCTAssertTrue(v2 > v1)
        XCTAssertTrue(v1 == v3)
        XCTAssertTrue(v1 <= v3)
        XCTAssertTrue(v1 >= v3)
    }
    
    // MARK: - 版本排序测试
    
    /// 测试排序
    func testSort() {
        let versions = ["2.0.0", "1.0.0", "1.1.0", "0.1.0", "1.0.0-alpha", "1.0.0"]
        let sorted = SemVerUtils.sort(versions)
        
        XCTAssertEqual(sorted.count, 6)
        XCTAssertEqual(sorted[0].fullVersion, "1.0.0-alpha")
        XCTAssertEqual(sorted[1].fullVersion, "0.1.0")
        XCTAssertEqual(sorted[2].fullVersion, "1.0.0")
        XCTAssertEqual(sorted[3].fullVersion, "1.0.0")
        XCTAssertEqual(sorted[4].fullVersion, "1.1.0")
        XCTAssertEqual(sorted[5].fullVersion, "2.0.0")
    }
    
    /// 测试排序字符串
    func testSortStrings() {
        let versions = ["3.0.0", "1.0.0", "2.0.0"]
        let sorted = SemVerUtils.sortStrings(versions)
        
        XCTAssertEqual(sorted, ["1.0.0", "2.0.0", "3.0.0"])
    }
    
    /// 测试最新版本
    func testLatest() {
        let versions = ["1.0.0", "3.0.0", "2.0.0", "2.5.0"]
        let latest = SemVerUtils.latest(versions)
        
        XCTAssertEqual(latest?.major, 3)
        
        XCTAssertNil(SemVerUtils.latest([]))
    }
    
    /// 测试最旧版本
    func testOldest() {
        let versions = ["3.0.0", "1.0.0", "2.0.0"]
        let oldest = SemVerUtils.oldest(versions)
        
        XCTAssertEqual(oldest?.major, 1)
        
        XCTAssertNil(SemVerUtils.oldest([]))
    }
    
    // MARK: - 版本范围测试
    
    /// 测试范围检查
    func testIsInRange() {
        XCTAssertTrue(SemVerUtils.isInRange("1.5.0", min: "1.0.0", max: "2.0.0")!)
        XCTAssertTrue(SemVerUtils.isInRange("1.0.0", min: "1.0.0", max: "2.0.0")!)
        XCTAssertTrue(SemVerUtils.isInRange("2.0.0", min: "1.0.0", max: "2.0.0")!)
        XCTAssertFalse(SemVerUtils.isInRange("0.9.0", min: "1.0.0", max: "2.0.0")!)
        XCTAssertFalse(SemVerUtils.isInRange("2.1.0", min: "1.0.0", max: "2.0.0")!)
        
        XCTAssertNil(SemVerUtils.isInRange("invalid", min: "1.0.0", max: "2.0.0"))
    }
    
    /// 测试约束满足 - 精确匹配
    func testSatisfiesExact() {
        XCTAssertTrue(SemVerUtils.satisfies("1.2.3", constraint: "1.2.3")!)
        XCTAssertFalse(SemVerUtils.satisfies("1.2.4", constraint: "1.2.3")!)
        XCTAssertFalse(SemVerUtils.satisfies("1.2.2", constraint: "1.2.3")!)
    }
    
    /// 测试约束满足 - 比较操作符
    func testSatisfiesOperators() {
        // >=
        XCTAssertTrue(SemVerUtils.satisfies("1.2.3", constraint: ">=1.0.0")!)
        XCTAssertTrue(SemVerUtils.satisfies("1.0.0", constraint: ">=1.0.0")!)
        XCTAssertFalse(SemVerUtils.satisfies("0.9.9", constraint: ">=1.0.0")!)
        
        // <=
        XCTAssertTrue(SemVerUtils.satisfies("0.9.9", constraint: "<=1.0.0")!)
        XCTAssertFalse(SemVerUtils.satisfies("1.0.1", constraint: "<=1.0.0")!)
        
        // >
        XCTAssertTrue(SemVerUtils.satisfies("1.0.1", constraint: ">1.0.0")!)
        XCTAssertFalse(SemVerUtils.satisfies("1.0.0", constraint: ">1.0.0")!)
        
        // <
        XCTAssertTrue(SemVerUtils.satisfies("0.9.9", constraint: "<1.0.0")!)
        XCTAssertFalse(SemVerUtils.satisfies("1.0.0", constraint: "<1.0.0")!)
        
        // =
        XCTAssertTrue(SemVerUtils.satisfies("1.2.3", constraint: "=1.2.3")!)
        XCTAssertFalse(SemVerUtils.satisfies("1.2.4", constraint: "=1.2.3")!)
    }
    
    /// 测试约束满足 - 脱字符
    func testSatisfiesCaret() {
        // ^1.2.3 允许 >=1.2.3 且 <2.0.0
        XCTAssertTrue(SemVerUtils.satisfies("1.2.3", constraint: "^1.2.3")!)
        XCTAssertTrue(SemVerUtils.satisfies("1.9.9", constraint: "^1.2.3")!)
        XCTAssertFalse(SemVerUtils.satisfies("2.0.0", constraint: "^1.2.3")!)
        XCTAssertFalse(SemVerUtils.satisfies("1.2.2", constraint: "^1.2.3")!)
        
        // ^0.2.3 允许 >=0.2.3 且 <0.3.0
        XCTAssertTrue(SemVerUtils.satisfies("0.2.3", constraint: "^0.2.3")!)
        XCTAssertTrue(SemVerUtils.satisfies("0.2.9", constraint: "^0.2.3")!)
        XCTAssertFalse(SemVerUtils.satisfies("0.3.0", constraint: "^0.2.3")!)
    }
    
    /// 测试约束满足 - 波浪号
    func testSatisfiesTilde() {
        // ~1.2.3 允许 >=1.2.3 且 <1.3.0
        XCTAssertTrue(SemVerUtils.satisfies("1.2.3", constraint: "~1.2.3")!)
        XCTAssertTrue(SemVerUtils.satisfies("1.2.9", constraint: "~1.2.3")!)
        XCTAssertFalse(SemVerUtils.satisfies("1.3.0", constraint: "~1.2.3")!)
        XCTAssertFalse(SemVerUtils.satisfies("1.2.2", constraint: "~1.2.3")!)
    }
    
    /// 测试约束满足 - X 范围
    func testSatisfiesXRange() {
        // 1.x.x
        XCTAssertTrue(SemVerUtils.satisfies("1.0.0", constraint: "1.x.x")!)
        XCTAssertTrue(SemVerUtils.satisfies("1.9.9", constraint: "1.x")!)
        XCTAssertFalse(SemVerUtils.satisfies("2.0.0", constraint: "1.x.x")!)
        
        // 1.2.x
        XCTAssertTrue(SemVerUtils.satisfies("1.2.0", constraint: "1.2.x")!)
        XCTAssertTrue(SemVerUtils.satisfies("1.2.9", constraint: "1.2.*")!)
        XCTAssertFalse(SemVerUtils.satisfies("1.3.0", constraint: "1.2.x")!)
    }
    
    /// 测试无效约束
    func testSatisfiesInvalid() {
        XCTAssertNil(SemVerUtils.satisfies("invalid", constraint: "1.0.0"))
        XCTAssertNil(SemVerUtils.satisfies("1.0.0", constraint: "invalid"))
    }
    
    // MARK: - 版本递增测试
    
    /// 测试主版本递增
    func testIncrementMajor() {
        let v = SemVerUtils.incrementMajor("1.2.3")
        XCTAssertEqual(v?.major, 2)
        XCTAssertEqual(v?.minor, 0)
        XCTAssertEqual(v?.patch, 0)
        
        XCTAssertNil(SemVerUtils.incrementMajor("invalid"))
    }
    
    /// 测试次版本递增
    func testIncrementMinor() {
        let v = SemVerUtils.incrementMinor("1.2.3")
        XCTAssertEqual(v?.major, 1)
        XCTAssertEqual(v?.minor, 3)
        XCTAssertEqual(v?.patch, 0)
        
        XCTAssertNil(SemVerUtils.incrementMinor("invalid"))
    }
    
    /// 测试补丁版本递增
    func testIncrementPatch() {
        let v = SemVerUtils.incrementPatch("1.2.3")
        XCTAssertEqual(v?.major, 1)
        XCTAssertEqual(v?.minor, 2)
        XCTAssertEqual(v?.patch, 4)
        
        XCTAssertNil(SemVerUtils.incrementPatch("invalid"))
    }
    
    /// 测试设置预发布
    func testSetPrerelease() {
        let v = SemVerUtils.setPrerelease("1.2.3", prerelease: "beta.1")
        XCTAssertEqual(v?.prerelease, "beta.1")
        XCTAssertEqual(v?.fullVersion, "1.2.3-beta.1")
        
        XCTAssertNil(SemVerUtils.setPrerelease("invalid", prerelease: "beta"))
    }
    
    /// 测试移除预发布
    func testRemovePrerelease() {
        let v = SemVerUtils.removePrerelease("1.2.3-beta.1")
        XCTAssertEqual(v?.prerelease, nil)
        XCTAssertEqual(v?.fullVersion, "1.2.3")
        
        XCTAssertNil(SemVerUtils.removePrerelease("invalid"))
    }
    
    // MARK: - 版本差异测试
    
    /// 测试差异计算
    func testDiff() {
        XCTAssertEqual(SemVerUtils.diff("1.0.0", "1.0.0"), .none)
        XCTAssertEqual(SemVerUtils.diff("1.0.0", "2.0.0"), .major)
        XCTAssertEqual(SemVerUtils.diff("1.0.0", "1.1.0"), .minor)
        XCTAssertEqual(SemVerUtils.diff("1.0.0", "1.0.1"), .patch)
        XCTAssertEqual(SemVerUtils.diff("1.0.0", "1.0.0-alpha"), .downgrade)
        XCTAssertEqual(SemVerUtils.diff("1.0.0-alpha", "1.0.0-beta"), .prerelease)
        
        XCTAssertNil(SemVerUtils.diff("invalid", "1.0.0"))
    }
    
    // MARK: - 版本提取测试
    
    /// 测试从文本提取
    func testExtract() {
        let text = "We use v1.2.3 and v2.0.0-beta in production, while v0.1.0 is deprecated"
        let versions = SemVerUtils.extract(from: text)
        
        XCTAssertEqual(versions.count, 3)
        XCTAssertTrue(versions.contains { $0.fullVersion == "1.2.3" })
        XCTAssertTrue(versions.contains { $0.fullVersion == "2.0.0-beta" })
        XCTAssertTrue(versions.contains { $0.fullVersion == "0.1.0" })
    }
    
    /// 测试提取第一个
    func testExtractFirst() {
        let text = "Version v1.2.3 released"
        let v = SemVerUtils.extractFirst(from: text)
        
        XCTAssertEqual(v?.fullVersion, "1.2.3")
        
        XCTAssertNil(SemVerUtils.extractFirst(from: "No version here"))
    }
    
    /// 测试提取空文本
    func testExtractEmpty() {
        let versions = SemVerUtils.extract(from: "")
        XCTAssertEqual(versions.count, 0)
        
        let versions2 = SemVerUtils.extract(from: "No semver in this text")
        XCTAssertEqual(versions2.count, 0)
    }
    
    // MARK: - 工厂方法测试
    
    /// 测试初始版本
    func testInitial() {
        let v = SemVerUtils.initial()
        XCTAssertEqual(v.major, 0)
        XCTAssertEqual(v.minor, 0)
        XCTAssertEqual(v.patch, 1)
    }
    
    /// 测试零版本
    func testZero() {
        let v = SemVerUtils.zero()
        XCTAssertEqual(v.major, 0)
        XCTAssertEqual(v.minor, 0)
        XCTAssertEqual(v.patch, 0)
    }
    
    /// 测试版本创建
    func testVersion() {
        let v1 = SemVerUtils.version(1)
        XCTAssertEqual(v1.fullVersion, "1.0.0")
        
        let v2 = SemVerUtils.version(1, 2)
        XCTAssertEqual(v2.fullVersion, "1.2.0")
        
        let v3 = SemVerUtils.version(1, 2, 3)
        XCTAssertEqual(v3.fullVersion, "1.2.3")
    }
    
    // MARK: - String 扩展测试
    
    /// 测试 String 扩展
    func testStringExtension() {
        let v = "1.2.3".semver
        XCTAssertNotNil(v)
        XCTAssertEqual(v?.major, 1)
        
        let vLoose = "1".semverLoose
        XCTAssertNotNil(vLoose)
        XCTAssertEqual(vLoose?.major, 1)
        
        XCTAssertTrue("1.2.3".isValidSemVer)
        XCTAssertFalse("invalid".isValidSemVer)
        
        XCTAssertTrue("1.2.5".satisfiesSemVer(">=1.2.3")!)
        XCTAssertFalse("1.2.0".satisfiesSemVer(">=1.2.3")!)
    }
    
    // MARK: - Array 扩展测试
    
    /// 测试 Array 扩展
    func testArrayExtension() {
        let versions = ["3.0.0", "1.0.0", "2.0.0"]
        
        XCTAssertEqual(versions.sortedSemVer, ["1.0.0", "2.0.0", "3.0.0"])
        
        XCTAssertEqual(versions.latestSemVer?.major, 3)
        XCTAssertEqual(versions.oldestSemVer?.major, 1)
    }
    
    // MARK: - Codabe 测试
    
    /// 测试 Codable
    func testCodable() {
        let v = SemVerUtils.parse("1.2.3-beta+build")!
        
        let encoder = JSONEncoder()
        let data = try! encoder.encode(v)
        let json = String(data: data, encoding: .utf8)!
        
        XCTAssertTrue(json.contains("\"major\":1"))
        XCTAssertTrue(json.contains("\"minor\":2"))
        XCTAssertTrue(json.contains("\"patch\":3"))
        XCTAssertTrue(json.contains("\"prerelease\":\"beta\""))
        
        let decoder = JSONDecoder()
        let decoded = try! decoder.decode(SemVer.self, from: data)
        
        XCTAssertEqual(decoded.major, 1)
        XCTAssertEqual(decoded.minor, 2)
        XCTAssertEqual(decoded.patch, 3)
        XCTAssertEqual(decoded.prerelease, "beta")
        XCTAssertEqual(decoded.buildMetadata, "build")
    }
    
    // MARK: - Hashable 测试
    
    /// 测试 Hashable
    func testHashable() {
        let v1 = SemVerUtils.parse("1.0.0")!
        let v2 = SemVerUtils.parse("1.0.0")!
        let v3 = SemVerUtils.parse("1.0.1")!
        
        let set: Set<SemVer> = [v1, v2, v3]
        XCTAssertEqual(set.count, 2)
    }
    
    // MARK: - 性能测试
    
    /// 测试解析性能
    func testParsePerformance() {
        measure {
            for _ in 0..<10000 {
                _ = SemVerUtils.parse("1.2.3-beta.1+build.123")
            }
        }
    }
    
    /// 测试比较性能
    func testComparePerformance() {
        let v1 = "1.0.0"
        let v2 = "2.0.0"
        
        measure {
            for _ in 0..<10000 {
                _ = SemVerUtils.compare(v1, v2)
            }
        }
    }
    
    /// 测试排序性能
    func testSortPerformance() {
        let versions = (0..<100).map { _ in
            "\(Int.random(in: 0...9)).\(Int.random(in: 0...99)).\(Int.random(in: 0...999))"
        }
        
        measure {
            _ = SemVerUtils.sort(versions)
        }
    }
    
    /// 测试约束检查性能
    func testSatisfiesPerformance() {
        let version = "1.2.3"
        let constraint = "^1.0.0"
        
        measure {
            for _ in 0..<10000 {
                _ = SemVerUtils.satisfies(version, constraint: constraint)
            }
        }
    }
}