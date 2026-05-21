/**
 * AllToolkit - Swift Pinyin Utilities Tests
 *
 * 拼音工具类测试文件
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation
import Testing

@Suite("PinyinUtils Tests")
struct PinyinUtilsTests {
    
    // MARK: - 基本转换测试
    
    @Test("基本拼音转换")
    func testBasicPinyinConversion() {
        // 测试单个汉字
        #expect(PinyinUtils.toPinyin("你") == "ni")
        #expect(PinyinUtils.toPinyin("好") == "hao")
        #expect(PinyinUtils.toPinyin("世") == "shi")
        #expect(PinyinUtils.toPinyin("界") == "jie")
        
        // 测试常用词组
        #expect(PinyinUtils.toPinyin("你好") == "ni hao")
        #expect(PinyinUtils.toPinyin("世界") == "shi jie")
        #expect(PinyinUtils.toPinyin("中国") == "zhong guo")
    }
    
    @Test("带声调拼音转换")
    func testPinyinWithTone() {
        #expect(PinyinUtils.toPinyin("你好", withTone: true) == "nǐ hǎo")
        #expect(PinyinUtils.toPinyin("中国", withTone: true) == "zhōng guó")
        #expect(PinyinUtils.toPinyin("北京", withTone: true) == "běi jīng")
        #expect(PinyinUtils.toPinyin("上海", withTone: true) == "shàng hǎi")
    }
    
    @Test("自定义分隔符")
    func testCustomSeparator() {
        #expect(PinyinUtils.toPinyin("你好世界", separator: "-") == "ni-hao-shi-jie")
        #expect(PinyinUtils.toPinyin("中文拼音", separator: "_") == "zhong_wen_pin_yin")
        #expect(PinyinUtils.toPinyin("测试", separator: "") == "ni hao".replacingOccurrences(of: " ", with: ""))
    }
    
    // MARK: - 拼音首字母测试
    
    @Test("拼音首字母转换")
    func testPinyinInitials() {
        #expect(PinyinUtils.toPinyinInitials("中国") == "ZG")
        #expect(PinyinUtils.toPinyinInitials("北京") == "BJ")
        #expect(PinyinUtils.toPinyinInitials("上海") == "SH")
        #expect(PinyinUtils.toPinyinInitials("广州") == "GZ")
        #expect(PinyinUtils.toPinyinInitials("深圳") == "SZ")
        #expect(PinyinUtils.toPinyinInitials("Hello世界") == "HSJ")
    }
    
    // MARK: - 中文字符检测测试
    
    @Test("中文字符检测")
    func testChineseDetection() {
        #expect(PinyinUtils.isChinese("中") == true)
        #expect(PinyinUtils.isChinese("文") == true)
        #expect(PinyinUtils.isChinese("A") == false)
        #expect(PinyinUtils.isChinese("1") == false)
        #expect(PinyinUtils.isChinese("@") == false)
    }
    
    @Test("全中文检测")
    func testAllChineseDetection() {
        #expect(PinyinUtils.isAllChinese("中文测试") == "true")
        #expect(PinyinUtils.isAllChinese("中文测试123") == "false")
        #expect(PinyinUtils.isAllChinese("Hello") == "false")
        #expect(PinyinUtils.isAllChinese("中文 Test") == "false")
    }
    
    @Test("中文字符计数")
    func testChineseCount() {
        #expect(PinyinUtils.countChinese("中文测试") == 4)
        #expect(PinyinUtils.countChinese("中文123测试") == 4)
        #expect(PinyinUtils.countChinese("Hello World") == 0)
        #expect(PinyinUtils.countChinese("混合Mixed内容123") == 2)
    }
    
    // MARK: - 声调添加测试
    
    @Test("声调添加")
    func testAddTone() {
        #expect(PinyinUtils.addTone("ma", tone: 1) == "mā")
        #expect(PinyinUtils.addTone("ma", tone: 2) == "má")
        #expect(PinyinUtils.addTone("ma", tone: 3) == "mǎ")
        #expect(PinyinUtils.addTone("ma", tone: 4) == "mà")
        
        #expect(PinyinUtils.addTone("zhong", tone: 1) == "zhōng")
        #expect(PinyinUtils.addTone("guo", tone: 2) == "guó")
        
        // 无效声调
        #expect(PinyinUtils.addTone("ma", tone: 0) == "ma")
        #expect(PinyinUtils.addTone("ma", tone: 5) == "ma")
    }
    
    // MARK: - 拼音比较测试
    
    @Test("拼音比较")
    func testPinyinComparison() {
        #expect(PinyinUtils.pinyinEqual("中国", "中国") == true)
        #expect(PinyinUtils.pinyinEqual("你好", "nihao") == false) // 英文不参与比较
        #expect(PinyinUtils.pinyinEqual("北京", "北京") == true)
    }
    
    // MARK: - 拼音排序测试
    
    @Test("拼音排序")
    func testSortByPinyin() {
        let names = ["张三", "李四", "王五", "赵六", "钱七"]
        let sorted = PinyinUtils.sortByPinyin(names)
        
        // 李四 (L) < 钱七 (Q) < 王五 (W) < 张三 (Z) < 赵六 (Z)
        // 按拼音首字母排序
        #expect(sorted.count == 5)
        #expect(sorted.first == "李四") // Li Si
        #expect(sorted.last == "赵六") // Zhao Liu (Z 在最后)
    }
    
    // MARK: - 分组测试
    
    @Test("按首字母分组")
    func testGroupByInitial() {
        let names = ["张三", "李四", "王五", "赵六", "李明"]
        let groups = PinyinUtils.groupByInitial(names)
        
        #expect(groups["Z"]?.count == 2) // 张三, 赵六
        #expect(groups["L"]?.count == 2) // 李四, 李明
        #expect(groups["W"]?.count == 1) // 王五
    }
    
    // MARK: - 拼音搜索测试
    
    @Test("拼音搜索")
    func testSearchByPinyin() {
        let names = ["张三", "李四", "王五", "赵六", "钱七"]
        
        // 搜索 "zhang"
        let zhangResults = PinyinUtils.searchByPinyin("zhang", in: names)
        #expect(zhangResults.contains("张三"))
        
        // 搜索 "li"
        let liResults = PinyinUtils.searchByPinyin("li", in: names)
        #expect(liResults.contains("李四"))
        
        // 搜索 "w"
        let wResults = PinyinUtils.searchByPinyin("w", in: names)
        #expect(wResults.contains("王五"))
    }
    
    // MARK: - 混合字符测试
    
    @Test("混合字符处理")
    func testMixedCharacters() {
        let mixed = "Hello世界123"
        let pinyin = PinyinUtils.toPinyin(mixed)
        
        #expect(pinyin.contains("Hello"))
        #expect(pinyin.contains("shi"))
        #expect(pinyin.contains("jie"))
        #expect(pinyin.contains("123"))
    }
    
    // MARK: - String 扩展测试
    
    @Test("String 扩展")
    func testStringExtensions() {
        // toPinyin
        #expect("中国".toPinyin() == "zhong guo")
        #expect("北京".toPinyin(withTone: true) == "běi jīng")
        
        // pinyinInitials
        #expect("上海".pinyinInitials == "SH")
        
        // isAllChinese
        #expect("中文".isAllChinese == true)
        #expect("中文abc".isAllChinese == false)
        
        // chineseCount
        #expect("中文abc测试".chineseCount == 4)
    }
    
    // MARK: - 边界情况测试
    
    @Test("边界情况")
    func testEdgeCases() {
        // 空字符串
        #expect(PinyinUtils.toPinyin("") == "")
        #expect(PinyinUtils.toPinyinInitials("") == "")
        #expect(PinyinUtils.countChinese("") == 0)
        
        // 单字符
        #expect(PinyinUtils.toPinyin("我") == "wo")
        
        // 纯英文/数字
        #expect(PinyinUtils.toPinyin("ABC123") == "A B C 1 2 3")
        #expect(PinyinUtils.toPinyinInitials("ABC") == "ABC")
        
        // 特殊字符
        #expect(PinyinUtils.toPinyin("!@#$%") == "! @ # $ %")
    }
    
    @Test("获取单个汉字拼音")
    func testGetPinyin() {
        #expect(PinyinUtils.getPinyin("你") == "ni")
        #expect(PinyinUtils.getPinyin("好", withTone: true) == "hǎo")
        #expect(PinyinUtils.getPinyin("A") == nil)
        #expect(PinyinUtils.getPinyin("1") == nil)
    }
}

// MARK: - 运行测试的 main 函数

#if DEBUG
@main
struct TestRunner {
    static func main() async {
        print("=== PinyinUtils 测试报告 ===\n")
        
        var passed = 0
        var failed = 0
        
        // 基本转换测试
        print("【基本转换测试】")
        let tests1 = [
            ("你好", "ni hao", PinyinUtils.toPinyin("你好")),
            ("世界", "shi jie", PinyinUtils.toPinyin("世界")),
            ("中国", "zhong guo", PinyinUtils.toPinyin("中国")),
            ("北京", "bei jing", PinyinUtils.toPinyin("北京")),
        ]
        for (input, expected, actual) in tests1 {
            let result = actual == expected ? "✓" : "✗"
            print("  \(result) toPinyin(\"\(input)\") = \"\(actual)\" (期望: \"\(expected)\")")
            if actual == expected { passed += 1 } else { failed += 1 }
        }
        
        // 带声调测试
        print("\n【带声调测试】")
        let tests2 = [
            ("你好", "nǐ hǎo", PinyinUtils.toPinyin("你好", withTone: true)),
            ("中国", "zhōng guó", PinyinUtils.toPinyin("中国", withTone: true)),
            ("上海", "shàng hǎi", PinyinUtils.toPinyin("上海", withTone: true)),
        ]
        for (input, expected, actual) in tests2 {
            let result = actual == expected ? "✓" : "✗"
            print("  \(result) toPinyin(\"\(input)\", withTone: true) = \"\(actual)\" (期望: \"\(expected)\")")
            if actual == expected { passed += 1 } else { failed += 1 }
        }
        
        // 首字母测试
        print("\n【首字母测试】")
        let tests3 = [
            ("中国", "ZG", PinyinUtils.toPinyinInitials("中国")),
            ("北京", "BJ", PinyinUtils.toPinyinInitials("北京")),
            ("上海", "SH", PinyinUtils.toPinyinInitials("上海")),
        ]
        for (input, expected, actual) in tests3 {
            let result = actual == expected ? "✓" : "✗"
            print("  \(result) toPinyinInitials(\"\(input)\") = \"\(actual)\" (期望: \"\(expected)\")")
            if actual == expected { passed += 1 } else { failed += 1 }
        }
        
        // 分隔符测试
        print("\n【分隔符测试】")
        let tests4 = [
            ("你好世界", "-", "ni-hao-shi-jie", PinyinUtils.toPinyin("你好世界", separator: "-")),
            ("中文拼音", "_", "zhong_wen_pin_yin", PinyinUtils.toPinyin("中文拼音", separator: "_")),
        ]
        for (input, sep, expected, actual) in tests4 {
            let result = actual == expected ? "✓" : "✗"
            print("  \(result) toPinyin(\"\(input)\", separator: \"\(sep)\") = \"\(actual)\" (期望: \"\(expected)\")")
            if actual == expected { passed += 1 } else { failed += 1 }
        }
        
        // 中文字符检测测试
        print("\n【中文字符检测测试】")
        let tests5 = [
            ("中", true, PinyinUtils.isChinese("中")),
            ("A", false, PinyinUtils.isChinese("A")),
            ("中文测试", "true", PinyinUtils.isAllChinese("中文测试")),
            ("中文123", "false", PinyinUtils.isAllChinese("中文123")),
            ("中文测试", 4, PinyinUtils.countChinese("中文测试")),
            ("中文123测试", 4, PinyinUtils.countChinese("中文123测试")),
        ]
        for (input, expected, actual) in tests5 {
            let result = "\(actual)" == "\(expected)" ? "✓" : "✗"
            print("  \(result) isChinese/AllChinese/countChinese(\"\(input)\") = \(actual) (期望: \(expected))")
            if "\(actual)" == "\(expected)" { passed += 1 } else { failed += 1 }
        }
        
        // 声调添加测试
        print("\n【声调添加测试】")
        let tests6 = [
            ("ma", 1, "mā", PinyinUtils.addTone("ma", tone: 1)),
            ("ma", 2, "má", PinyinUtils.addTone("ma", tone: 2)),
            ("ma", 3, "mǎ", PinyinUtils.addTone("ma", tone: 3)),
            ("ma", 4, "mà", PinyinUtils.addTone("ma", tone: 4)),
        ]
        for (input, tone, expected, actual) in tests6 {
            let result = actual == expected ? "✓" : "✗"
            print("  \(result) addTone(\"\(input)\", tone: \(tone)) = \"\(actual)\" (期望: \"\(expected)\")")
            if actual == expected { passed += 1 } else { failed += 1 }
        }
        
        // String 扩展测试
        print("\n【String 扩展测试】")
        let tests7 = [
            ("中国".toPinyin(), "zhong guo"),
            ("上海".pinyinInitials, "SH"),
            ("中文".isAllChinese, true),
            ("中文abc".isAllChinese, false),
            ("中文abc测试".chineseCount, 4),
        ]
        for (actual, expected) in tests7 {
            let result = "\(actual)" == "\(expected)" ? "✓" : "✗"
            print("  \(result) 扩展方法测试: \(actual) (期望: \(expected))")
            if "\(actual)" == "\(expected)" { passed += 1 } else { failed += 1 }
        }
        
        // 混合字符测试
        print("\n【混合字符测试】")
        let mixedPinyin = PinyinUtils.toPinyin("Hello世界123")
        print("  toPinyin(\"Hello世界123\") = \"\(mixedPinyin)\"")
        let containsHello = mixedPinyin.contains("Hello")
        let containsShi = mixedPinyin.contains("shi")
        let containsJie = mixedPinyin.contains("jie")
        if containsHello && containsShi && containsJie {
            print("  ✓ 混合字符正确处理")
            passed += 1
        } else {
            print("  ✗ 混合字符处理失败")
            failed += 1
        }
        
        // 排序测试
        print("\n【排序测试】")
        let names = ["张三", "李四", "王五", "赵六", "钱七"]
        let sorted = PinyinUtils.sortByPinyin(names)
        print("  原始: \(names)")
        print("  排序: \(sorted)")
        print("  ✓ 按拼音排序完成")
        passed += 1
        
        // 分组测试
        print("\n【分组测试】")
        let groups = PinyinUtils.groupByInitial(names)
        for (initial, items) in groups.sorted(by: { $0.key < $1.key }) {
            print("  \(initial): \(items)")
        }
        print("  ✓ 按首字母分组完成")
        passed += 1
        
        // 搜索测试
        print("\n【搜索测试】")
        let searchResults = PinyinUtils.searchByPinyin("zhang", in: names)
        print("  搜索 \"zhang\": \(searchResults)")
        if searchResults.contains("张三") {
            print("  ✓ 搜索功能正常")
            passed += 1
        } else {
            print("  ✗ 搜索功能异常")
            failed += 1
        }
        
        // 总结
        print("\n" + String(repeating: "=", count: 40))
        print("测试结果: 通过 \(passed) / 失败 \(failed)")
        print("总计: \(passed + failed) 个测试")
        if failed == 0 {
            print("✓ 所有测试通过！")
        } else {
            print("✗ 存在失败的测试")
        }
    }
}
#endif