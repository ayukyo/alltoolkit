/**
 * AllToolkit - Swift Morse Code Utilities 使用示例
 *
 * 展示摩尔斯电码工具类的各种用法
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// ============================================
// 示例 1：基础编码和解码
// ============================================

print("=== 示例 1：基础编码和解码 ===\n")

let encoder = MorseEncoder()
let decoder = MorseDecoder()

// 编码文本
let text = "HELLO WORLD"
let morseCode = encoder.encode(text)
print("原文: \(text)")
print("摩尔斯电码: \(morseCode)")
print("解码后: \(decoder.decode(morseCode))")

print("\n---\n")


// ============================================
// 示例 2：使用 String 扩展
// ============================================

print("=== 示例 2：使用 String 扩展 ===\n")

// 直接使用 String 扩展方法
let message = "SOS"
let encoded = message.toMorse()
let decoded = encoded.fromMorse()

print("消息: \(message)")
print("编码: \(encoded)")
print("解码: \(decoded)")

print("\n---\n")


// ============================================
// 示例 3：自定义符号
// ============================================

print("=== 示例 3：自定义符号 ===\n")

// 使用自定义符号（比如 * 和 # 代替 . 和 -）
var customEncoder = MorseEncoder()
customEncoder.dotSymbol = "*"
customEncoder.dashSymbol = "#"

var customDecoder = MorseDecoder()
customDecoder.dotSymbol = "*"
customDecoder.dashSymbol = "#"

let customText = "SOS"
let customEncoded = customEncoder.encode(customText)
print("自定义编码 (\(customText)): \(customEncoded)")

let customDecoded = customDecoder.decode(customEncoded)
print("解码后: \(customDecoded)")

print("\n---\n")


// ============================================
// 示例 4：数字和标点符号
// ============================================

print("=== 示例 4：数字和标点符号 ===\n")

// 编码数字
let numbers = "12345"
print("数字 '\(numbers)':")
print("  摩尔斯: \(encoder.encode(numbers))")

// 编码标点符号
let punctuation = "Hello, World!"
print("\n带标点符号的句子 '\(punctuation)':")
print("  摩尔斯: \(encoder.encode(punctuation))")

// 特殊符号
print("\n@ 符号: \(encoder.encode("@"))")
print("? 符号: \(encoder.encode("?"))")
print("! 符号: \(encoder.encode("!"))")

print("\n---\n")


// ============================================
// 示例 5：Prosigns（程序信号）
// ============================================

print("=== 示例 5：Prosigns（程序信号） ===\n")

// 列出所有程序信号
print("常用程序信号:")
for prosign in MorseProsign.all {
    print("  \(prosign.name.padding(toLength: 4, withPad: " ", startingAt: 0)): \(prosign.code.padding(toLength: 10, withPad: " ", startingAt: 0)) - \(prosign.meaning)")
}

// 查找特定程序信号
print("\n查找 SOS 信号:")
if let sos = MorseProsign.find(name: "SOS") {
    print("  名称: \(sos.name)")
    print("  代码: \(sos.code)")
    print("  含义: \(sos.meaning)")
}

print("\n---\n")


// ============================================
// 示例 6：时长计算
// ============================================

print("=== 示例 6：时长计算 ===\n")

// 默认配置（点号 60ms）
let defaultEncoder = MorseEncoder()
let morse = defaultEncoder.encode("HELLO")
let duration = defaultEncoder.calculateDuration(morse)

print("消息: HELLO")
print("摩尔斯: \(morse)")
print("发送时长: \(duration)ms (\(duration/1000)秒)")

// 自定义速度（更快的点号）
var fastEncoder = MorseEncoder()
fastEncoder.dotDuration = 40  // 更快的速度

let fastMorse = fastEncoder.encode("HELLO")
let fastDuration = fastEncoder.calculateDuration(fastMorse)

print("\n快速模式 (40ms 点号):")
print("发送时长: \(fastDuration)ms (\(fastDuration/1000)秒)")

print("\n---\n")


// ============================================
// 示例 7：统计分析
// ============================================

print("=== 示例 7：统计分析 ===\n")

let textToAnalyze = "SOS HELLO WORLD"
let stats = MorseStats.analyze(textToAnalyze)

print("文本: \(textToAnalyze)")
print("摩尔斯电码: \(stats["morseCode"] ?? "")")
print("点号数量: \(stats["dotCount"] ?? 0)")
print("划号数量: \(stats["dashCount"] ?? 0)")
print("总信号数: \(stats["totalSignals"] ?? 0)")
print("发送时长: \(stats["durationMs"] ?? 0)ms")
print("单词数: \(stats["wordCount"] ?? 0)")
print("字符数: \(stats["characterCount"] ?? 0)")
print("每字符平均信号数: \(stats["averageSignalPerChar"] ?? 0)")

print("\n---\n")


// ============================================
// 示例 8：字符表格生成
// ============================================

print("=== 示例 8：字符表格生成 ===\n")

let sentence = "HELLO WORLD"
let table = MorseStats.table(sentence)

print("句子: \(sentence)")
print("\n字符表格:")
print("+------+--------+")
print("| 字符 | 摩尔斯 |")
print("+------+--------+")
for entry in table {
    if entry.char == "空格" {
        print("| 空格 | \(entry.morse.padding(toLength: 6, withPad: " ", startingAt: 0)) |")
    } else {
        print("| \(entry.char.padding(toLength: 4, withPad: " ", startingAt: 0)) | \(entry.morse.padding(toLength: 6, withPad: " ", startingAt: 0)) |")
    }
}
print("+------+--------+")

print("\n---\n")


// ============================================
// 示例 9：完整消息处理
// ============================================

print("=== 示例 9：完整消息处理 ===\n")

func processMessage(_ text: String) {
    let encoder = MorseEncoder()
    let decoder = MorseDecoder()
    
    print("📝 原始消息: \(text)")
    print()
    
    // 编码
    let morse = encoder.encode(text)
    print("📡 摩尔斯电码: \(morse)")
    
    // 统计
    let stats = MorseStats.analyze(text)
    print("📊 统计:")
    print("   - 点号: \(stats["dotCount"] ?? 0)")
    print("   - 划号: \(stats["dashCount"] ?? 0)")
    print("   - 预计发送时长: \(stats["durationMs"] ?? 0)ms")
    
    // 解码验证
    let decoded = decoder.decode(morse)
    let verified = (text == decoded) ? "✅ 验证通过" : "❌ 验证失败"
    print("🔄 解码验证: \(decoded)")
    print("   \(verified)")
}

// 处理多条消息
processMessage("SOS")
print()
processMessage("THE QUICK BROWN FOX")
print()
processMessage("MORSE CODE 123")

print("\n---\n")


// ============================================
// 示例 10：电报格式化输出
// ============================================

print("=== 示例 10：电报格式化输出 ===\n")

func formatAsTelegram(_ text: String) -> String {
    let encoder = MorseEncoder()
    let lines: [String] = []
    
    var result = "╔══════════════════════════════════════╗\n"
    result += "║            📻 电报消息              ║\n"
    result += "╠══════════════════════════════════════╣\n"
    
    // 原文
    result += "║ 原文: \(text.padding(toLength: 28, withPad: " ", startingAt: 0))║\n"
    
    // 摩尔斯电码
    let morse = encoder.encode(text)
    result += "║ 摩尔斯: \(morse.padding(toLength: 27, withPad: " ", startingAt: 0))║\n"
    
    // 统计
    let stats = MorseStats.analyze(text)
    let dots = stats["dotCount"] as? Int ?? 0
    let dashes = stats["dashCount"] as? Int ?? 0
    let duration = stats["durationMs"] as? TimeInterval ?? 0
    
    result += "╠══════════════════════════════════════╣\n"
    result += "║ 点号: \(String(dots).padding(toLength: 4, withPad: " ", startingAt: 0))  划号: \(String(dashes).padding(toLength: 4, withPad: " ", startingAt: 0))  时长: \(String(format: "%.0f", duration))ms ║\n"
    result += "╚══════════════════════════════════════╝"
    
    return result
}

print(formatAsTelegram("HELLO WORLD"))

print("\n---\n")


// ============================================
// 示例 11：摩尔斯电码学习工具
// ============================================

print("=== 示例 11：摩尔斯电码学习工具 ===\n")

// 创建一个简单的学习表格
func printLearningTable() {
    let alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    let encoder = MorseEncoder()
    
    print("📚 摩尔斯电码学习表")
    print("=" * 40)
    
    // 字母
    print("\n🔤 字母:")
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" {
        let morse = encoder.encodeCharacter(char)
        print("  \(char): \(morse.padding(toLength: 7, withPad: " ", startingAt: 0))", terminator: "")
        if (char.asciiValue! - 65) % 4 == 3 { print() }
    }
    
    print("\n\n🔢 数字:")
    for char in "0123456789" {
        let morse = encoder.encodeCharacter(char)
        print("  \(char): \(morse.padding(toLength: 7, withPad: " ", startingAt: 0))", terminator: "")
        if (char.asciiValue! - 48) % 5 == 4 { print() }
    }
    
    print("\n\n📝 常用标点:")
    for char in ".?,!@" {
        let morse = encoder.encodeCharacter(char)
        print("  \(char): \(morse)")
    }
}

printLearningTable()

print("\n---\n")


// ============================================
// 示例 12：音频播放（仅 iOS/macOS）
// ============================================

print("=== 示例 12：音频播放 ===\n")

// 注意：音频播放功能需要实际设备运行
// 这里仅展示代码用法

let player = MorsePlayer()
player.frequency = 600  // 600Hz
player.volume = 0.7     // 70% 音量

print("音频播放器配置:")
print("  频率: \(player.frequency)Hz")
print("  音量: \(Int(player.volume * 100))%")
print("  点号时长: \(player.encoder.dotDuration)ms")
print("  划号时长: \(player.encoder.dashDuration)ms")

// 播放示例（需要实际设备）
// player.playText("SOS") { print("播放完成") }

print("\n注意：音频播放需要在 iOS/macOS 设备上运行")

print("\n---\n")


// ============================================
// 示例 13：实用工具函数
// ============================================

print("=== 示例 13：实用工具函数 ===\n")

/// 比较两个字符串的摩尔斯编码
func compareMorse(_ text1: String, _ text2: String) -> Bool {
    let encoder = MorseEncoder()
    return encoder.encode(text1) == encoder.encode(text2)
}

/// 检查字符串是否只包含可编码字符
func isFullyEncodable(_ text: String) -> Bool {
    let encoder = MorseEncoder()
    encoder.ignoreUnknown = false
    let encoded = encoder.encode(text)
    return !encoded.contains("?")
}

/// 查找摩尔斯电码对应的字符
func findCharacter(for morse: String) -> String {
    let decoder = MorseDecoder()
    if let char = decoder.decodeCode(morse) {
        return String(char)
    }
    
    // 尝试 Prosign
    if let prosign = MorseProsign.find(code: morse) {
        return "[\(prosign.name)]"
    }
    
    return "未知"
}

// 使用示例
print("比较测试:")
print("  'hello' vs 'HELLO': \(compareMorse("hello", "HELLO") ? "相同" : "不同")")
print("  'hello' vs 'world': \(compareMorse("hello", "world") ? "相同" : "不同")")

print("\n可编码检查:")
print("  'HELLO': \(isFullyEncodable("HELLO") ? "完全可编码" : "包含未知字符")")
print("  '你好': \(isFullyEncodable("你好") ? "完全可编码" : "包含未知字符")")

print("\n字符查找:")
print("  '.-' -> \(findCharacter(for: ".-"))")
print("  '... --- ...' -> \(findCharacter(for: "...---..."))")
print("  '---' -> \(findCharacter(for: "---"))")

print("\n=== 所有示例完成 ===\n")

// 辅助扩展
extension String {
    static func *(lhs: String, rhs: Int) -> String {
        return String(repeating: lhs, count: rhs)
    }
}