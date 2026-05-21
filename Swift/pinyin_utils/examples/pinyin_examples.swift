/**
 * AllToolkit - Swift Pinyin Utilities Examples
 *
 * 拼音工具类使用示例
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// ========================================
// 示例 1: 基本拼音转换
// ========================================

print("=== 示例 1: 基本拼音转换 ===\n")

// 将中文转换为拼音
let greeting = "你好世界"
print("原文: \(greeting)")
print("拼音: \(PinyinUtils.toPinyin(greeting))")
// 输出: ni hao shi jie

// 带声调的拼音
print("带声调: \(PinyinUtils.toPinyin(greeting, withTone: true))")
// 输出: nǐ hǎo shì jiè

// 使用不同分隔符
print("下划线分隔: \(PinyinUtils.toPinyin(greeting, separator: "_"))")
// 输出: ni_hao_shi_jie

print("")

// ========================================
// 示例 2: 拼音首字母
// ========================================

print("=== 示例 2: 拼音首字母 ===\n")

let cities = ["北京", "上海", "广州", "深圳", "杭州"]
for city in cities {
    print("\(city) -> \(PinyinUtils.toPinyinInitials(city))")
}
// 输出:
// 北京 -> BJ
// 上海 -> SH
// 广州 -> GZ
// 深圳 -> SZ
// 杭州 -> HZ

print("")

// ========================================
// 示例 3: 中文字符检测
// ========================================

print("=== 示例 3: 中文字符检测 ===\n")

let testStrings = ["中文", "English", "混合Mixed", "123", "中文测试123"]
for str in testStrings {
    print("\"\(str)\":")
    print("  - 全中文: \(PinyinUtils.isAllChinese(str))")
    print("  - 中文数量: \(PinyinUtils.countChinese(str))")
}

print("")

// ========================================
// 示例 4: 声调添加
// ========================================

print("=== 示例 4: 声调添加 ===\n")

let syllables = ["ma", "ni", "hao", "zhong", "guo"]
for syllable in syllables {
    print("\(syllable):")
    for tone in 1...4 {
        let withTone = PinyinUtils.addTone(syllable, tone: tone)
        print("  声调\(tone): \(withTone)")
    }
}

print("")

// ========================================
// 示例 5: 拼音排序
// ========================================

print("=== 示例 5: 拼音排序 ===\n")

let names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]
print("原始顺序: \(names)")
let sorted = PinyinUtils.sortByPinyin(names)
print("拼音排序: \(sorted)")

print("")

// ========================================
// 示例 6: 按首字母分组
// ========================================

print("=== 示例 6: 按首字母分组 ===\n")

let contacts = ["张三", "李四", "王五", "赵六", "钱七", "李明", "王芳", "张伟"]
let grouped = PinyinUtils.groupByInitial(contacts)

for (initial, names) in grouped.sorted(by: { $0.key < $1.key }) {
    print("\(initial): \(names.joined(separator: ", "))")
}

print("")

// ========================================
// 示例 7: 拼音搜索
// ========================================

print("=== 示例 7: 拼音搜索 ===\n")

let products = ["苹果手机", "华为手机", "小米电视", "联想电脑", "三星冰箱", "索尼相机"]
let searchQueries = ["shou", "ji", "dian"]

for query in searchQueries {
    let results = PinyinUtils.searchByPinyin(query, in: products)
    print("搜索 \"\(query)\": \(results)")
}

print("")

// ========================================
// 示例 8: String 扩展使用
// ========================================

print("=== 示例 8: String 扩展使用 ===\n")

let text = "中华人民共和国"
print("原文: \(text)")
print("拼音: \(text.toPinyin())")
print("带声调: \(text.toPinyin(withTone: true))")
print("首字母: \(text.pinyinInitials)")
print("全中文: \(text.isAllChinese)")
print("中文数: \(text.chineseCount)")

print("")

// ========================================
// 示例 9: 混合文本处理
// ========================================

print("=== 示例 9: 混合文本处理 ===\n")

let mixedText = "我在Beijing学习中文study Chinese"
print("混合文本: \(mixedText)")
print("转换为拼音: \(PinyinUtils.toPinyin(mixedText))")
print("首字母提取: \(PinyinUtils.toPinyinInitials(mixedText))")
print("中文字数: \(PinyinUtils.countChinese(mixedText))")

print("")

// ========================================
// 示例 10: 实际应用场景
// ========================================

print("=== 示例 10: 实际应用场景 ===\n")

// 场景 1: 通讯录索引
print("【通讯录索引】")
let addressBook = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十", "郑一", "冯二"]
let indexGroups = PinyinUtils.groupByInitial(addressBook)
let sortedKeys = indexGroups.keys.sorted()

for key in sortedKeys {
    let count = indexGroups[key]?.count ?? 0
    print("  \(key): \(count) 人")
}

// 场景 2: 搜索建议
print("\n【搜索建议】")
let allCities = ["北京", "上海", "广州", "深圳", "杭州", "南京", "苏州", "成都", "武汉", "西安"]
let userInput = "bei"
let suggestions = PinyinUtils.searchByPinyin(userInput, in: allCities)
print("用户输入: \"\(userInput)\"")
print("搜索建议: \(suggestions)")

// 场景 3: 文本处理流水线
print("\n【文本处理流水线】")
let article = "学习使人进步，知识改变命运"
let articlePinyin = article.toPinyin(withTone: true, separator: " | ")
let articleInitials = article.pinyinInitials
print("原文: \(article)")
print("拼音: \(articlePinyin)")
print("首字母: \(articleInitials)")

print("\n" + String(repeating: "=", count: 40))
print("示例演示完成！")