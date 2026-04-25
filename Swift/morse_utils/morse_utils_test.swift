/**
 * AllToolkit - Swift Morse Code Utilities 测试文件
 *
 * 测试摩尔斯电码工具类的各项功能
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation
import XCTest

// 导入模块（实际使用时需要正确配置模块导入）
// @testable import MorseUtils

class MorseUtilsTests: XCTestCase {
    
    // MARK: - 编码器测试
    
    func testEncodeBasicLetters() {
        let encoder = MorseEncoder()
        
        // 测试单个字母
        XCTAssertEqual(encoder.encode("A"), ".-")
        XCTAssertEqual(encoder.encode("B"), "-...")
        XCTAssertEqual(encoder.encode("E"), ".")
        XCTAssertEqual(encoder.encode("T"), "-")
        XCTAssertEqual(encoder.encode("S"), "...")
        XCTAssertEqual(encoder.encode("O"), "---")
    }
    
    func testEncodeNumbers() {
        let encoder = MorseEncoder()
        
        XCTAssertEqual(encoder.encode("0"), "-----")
        XCTAssertEqual(encoder.encode("1"), ".----")
        XCTAssertEqual(encoder.encode("9"), "----.")
    }
    
    func testEncodePunctuation() {
        let encoder = MorseEncoder()
        
        XCTAssertEqual(encoder.encode("."), ".-.-.-")
        XCTAssertEqual(encoder.encode(","), "--..--")
        XCTAssertEqual(encoder.encode("?"), "..--..")
        XCTAssertEqual(encoder.encode("!"), "-.-.--")
    }
    
    func testEncodeWords() {
        let encoder = MorseEncoder()
        
        // 单词测试
        XCTAssertEqual(encoder.encode("SOS"), "... --- ...")
        XCTAssertEqual(encoder.encode("HELLO"), ".... . .-.. .-.. ---")
        XCTAssertEqual(encoder.encode("WORLD"), ".-- --- .-. .-.. -..")
    }
    
    func testEncodeSentences() {
        let encoder = MorseEncoder()
        
        // 句子测试
        XCTAssertEqual(encoder.encode("HELLO WORLD"), ".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
        XCTAssertEqual(encoder.encode("SOS SOS"), "... --- ... / ... --- ...")
    }
    
    func testEncodeLowercase() {
        let encoder = MorseEncoder()
        
        // 小写字母测试
        XCTAssertEqual(encoder.encode("a"), ".-")
        XCTAssertEqual(encoder.encode("hello"), ".... . .-.. .-.. ---")
        XCTAssertEqual(encoder.encode("Hello World"), ".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
    }
    
    func testEncodeWithCustomSymbols() {
        var encoder = MorseEncoder()
        encoder.dotSymbol = "*"
        encoder.dashSymbol = "#"
        
        XCTAssertEqual(encoder.encode("A"), "*#")
        XCTAssertEqual(encoder.encode("S"), "***")
        XCTAssertEqual(encoder.encode("O"), "###")
    }
    
    func testEncodeUnknownChars() {
        var encoder = MorseEncoder()
        encoder.ignoreUnknown = true
        XCTAssertEqual(encoder.encode("HELLO!@#"), ".... . .-.. .-.. --- -.-.--")
        
        encoder.ignoreUnknown = false
        XCTAssertNotNil(encoder.encode("HELLO!@#"))
    }
    
    // MARK: - 解码器测试
    
    func testDecodeBasicLetters() {
        let decoder = MorseDecoder()
        
        XCTAssertEqual(decoder.decode(".-"), "A")
        XCTAssertEqual(decoder.decode("-..."), "B")
        XCTAssertEqual(decoder.decode("."), "E")
        XCTAssertEqual(decoder.decode("-"), "T")
    }
    
    func testDecodeNumbers() {
        let decoder = MorseDecoder()
        
        XCTAssertEqual(decoder.decode("-----"), "0")
        XCTAssertEqual(decoder.decode(".----"), "1")
        XCTAssertEqual(decoder.decode("----."), "9")
    }
    
    func testDecodeWords() {
        let decoder = MorseDecoder()
        
        XCTAssertEqual(decoder.decode("... --- ..."), "SOS")
        XCTAssertEqual(decoder.decode(".... . .-.. .-.. ---"), "HELLO")
    }
    
    func testDecodeSentences() {
        let decoder = MorseDecoder()
        
        XCTAssertEqual(decoder.decode(".... . .-.. .-.. --- / .-- --- .-. .-.. -.."), "HELLO WORLD")
    }
    
    func testDecodeWithCustomSymbols() {
        var decoder = MorseDecoder()
        decoder.dotSymbol = "*"
        decoder.dashSymbol = "#"
        
        XCTAssertEqual(decoder.decode("*#"), "A")
        XCTAssertEqual(decoder.decode("***"), "S")
    }
    
    // MARK: - 编码解码往返测试
    
    func testEncodeDecodeRoundTrip() {
        let encoder = MorseEncoder()
        let decoder = MorseDecoder()
        
        let testCases = [
            "HELLO WORLD",
            "SOS",
            "MORSE CODE",
            "THE QUICK BROWN FOX",
            "12345",
            "TEST 123",
            "A.B,C?D!E"
        ]
        
        for text in testCases {
            let encoded = encoder.encode(text)
            let decoded = decoder.decode(encoded)
            XCTAssertEqual(decoded, text, "Round trip failed for: \(text)")
        }
    }
    
    func testEncodeDecodeWithCustomSettings() {
        var encoder = MorseEncoder()
        encoder.dotSymbol = "*"
        encoder.dashSymbol = "#"
        
        var decoder = MorseDecoder()
        decoder.dotSymbol = "*"
        decoder.dashSymbol = "#"
        
        let text = "HELLO"
        let encoded = encoder.encode(text)
        let decoded = decoder.decode(encoded)
        
        XCTAssertEqual(decoded, text)
        XCTAssertEqual(encoded, "*# *#*# *#*# *#*# ###")
    }
    
    // MARK: - Prosign 测试
    
    func testProsignLookup() {
        // 测试按名称查找
        XCTAssertNotNil(MorseProsign.find(name: "SOS"))
        XCTAssertEqual(MorseProsign.find(name: "SOS")?.code, "...---...")
        
        XCTAssertNotNil(MorseProsign.find(name: "AR"))
        XCTAssertEqual(MorseProsign.find(name: "AR")?.meaning, "消息结束 (End of Message)")
        
        // 测试按代码查找
        XCTAssertNotNil(MorseProsign.find(code: "...---..."))
        XCTAssertEqual(MorseProsign.find(code: "...---...")?.name, "SOS")
        
        XCTAssertNotNil(MorseProsign.find(code: ".-.-."))
        XCTAssertEqual(MorseProsign.find(code: ".-.-.")?.name, "AR")
    }
    
    func testProsignList() {
        XCTAssertEqual(MorseProsign.all.count, 12)
        
        let names = MorseProsign.all.map { $0.name }
        XCTAssertTrue(names.contains("SOS"))
        XCTAssertTrue(names.contains("AR"))
        XCTAssertTrue(names.contains("SK"))
        XCTAssertTrue(names.contains("BT"))
    }
    
    // MARK: - 时长计算测试
    
    func testDurationCalculation() {
        let encoder = MorseEncoder()
        
        // 点号时长：60ms
        // 划号时长：180ms (3 * 60)
        // 字符内间隔：60ms
        // 字符间间隔：180ms (3 * 60)
        
        // "E" = "." = 1个点 + 1个间隔 = 60 + 60 = 120ms
        let eDuration = encoder.calculateDuration(".")
        XCTAssertEqual(eDuration, 120)
        
        // "T" = "-" = 1个划 + 1个间隔 = 180 + 60 = 240ms
        let tDuration = encoder.calculateDuration("-")
        XCTAssertEqual(tDuration, 240)
        
        // "S" = "..." = 3个点 + 3个间隔 = 3*60 + 3*60 = 360ms
        let sDuration = encoder.calculateDuration("...")
        XCTAssertEqual(sDuration, 360)
    }
    
    func testCustomDuration() {
        var encoder = MorseEncoder()
        encoder.dotDuration = 100
        
        // 点号时长：100ms
        // 划号时长：300ms
        // 字符内间隔：100ms
        // 字符间间隔：300ms
        
        // "E" = "." = 100 + 100 = 200ms
        let eDuration = encoder.calculateDuration(".")
        XCTAssertEqual(eDuration, 200)
    }
    
    // MARK: - 统计测试
    
    func testMorseStats() {
        let text = "SOS"
        let stats = MorseStats.analyze(text)
        
        XCTAssertEqual(stats["dotCount"] as? Int, 5)  // SOS = ... --- ... = 5个点
        XCTAssertEqual(stats["dashCount"] as? Int, 3)  // SOS = ... --- ... = 3个划
        XCTAssertEqual(stats["totalSignals"] as? Int, 8)
        XCTAssertEqual(stats["characterCount"] as? Int, 3)
        XCTAssertEqual(stats["wordCount"] as? Int, 1)
        XCTAssertNotNil(stats["morseCode"])
    }
    
    func testMorseStatsTable() {
        let text = "HELLO"
        let table = MorseStats.table(text)
        
        XCTAssertEqual(table.count, 4)  // H, E, L, O (L出现两次只计一次)
        
        let hEntry = table.first { $0.char == "H" }
        XCTAssertNotNil(hEntry)
        XCTAssertEqual(hEntry?.morse, "....")
        
        let eEntry = table.first { $0.char == "E" }
        XCTAssertNotNil(eEntry)
        XCTAssertEqual(eEntry?.morse, ".")
        
        let lEntry = table.first { $0.char == "L" }
        XCTAssertNotNil(lEntry)
        XCTAssertEqual(lEntry?.morse, ".-..")
    }
    
    // MARK: - String 扩展测试
    
    func testStringExtension() {
        let text = "HELLO"
        let morse = text.toMorse()
        
        XCTAssertEqual(morse, ".... . .-.. .-.. ---")
        
        let decoded = morse.fromMorse()
        XCTAssertEqual(decoded, text)
    }
    
    // MARK: - 边界情况测试
    
    func testEmptyString() {
        let encoder = MorseEncoder()
        let decoder = MorseDecoder()
        
        XCTAssertEqual(encoder.encode(""), "")
        XCTAssertEqual(decoder.decode(""), "")
    }
    
    func testWhitespaceOnly() {
        let encoder = MorseEncoder()
        let decoder = MorseDecoder()
        
        XCTAssertEqual(encoder.encode("   "), "")
        XCTAssertEqual(encoder.encode("  HELLO  "), ".... . .-.. .-.. ---")
    }
    
    func testMultipleSpaces() {
        let encoder = MorseEncoder()
        let decoder = MorseDecoder()
        
        // 多个空格应该被视为单词分隔
        let encoded = encoder.encode("HELLO   WORLD")
        XCTAssertEqual(encoded, ".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
    }
    
    func testMixedCase() {
        let encoder = MorseEncoder()
        
        // 混合大小写应该得到相同结果
        XCTAssertEqual(encoder.encode("HeLLo"), encoder.encode("HELLO"))
        XCTAssertEqual(encoder.encode("HeLLo"), encoder.encode("hello"))
    }
    
    func testPunctuationInSentence() {
        let encoder = MorseEncoder()
        let decoder = MorseDecoder()
        
        let text = "HELLO, WORLD!"
        let encoded = encoder.encode(text)
        let decoded = decoder.decode(encoded)
        
        XCTAssertEqual(decoded, text)
        XCTAssertTrue(encoded.contains("--..--"))  // 逗号
        XCTAssertTrue(encoded.contains("-.-.--"))  // 感叹号
    }
    
    // MARK: - 特殊字符测试
    
    func testAtSign() {
        let encoder = MorseEncoder()
        let decoder = MorseDecoder()
        
        XCTAssertEqual(encoder.encode("@"), ".--.-.")
        XCTAssertEqual(decoder.decode(".--.-."), "@")
    }
    
    func testParentheses() {
        let encoder = MorseEncoder()
        let decoder = MorseDecoder()
        
        let text = "(HELLO)"
        let encoded = encoder.encode(text)
        let decoded = decoder.decode(encoded)
        
        XCTAssertEqual(decoded, text)
    }
    
    // MARK: - 性能测试
    
    func testEncodingPerformance() {
        let encoder = MorseEncoder()
        let longText = String(repeating: "HELLO WORLD ", count: 1000)
        
        measure {
            _ = encoder.encode(longText)
        }
    }
    
    func testDecodingPerformance() {
        let decoder = MorseDecoder()
        let encoder = MorseEncoder()
        let longText = String(repeating: "HELLO WORLD ", count: 1000)
        let morse = encoder.encode(longText)
        
        measure {
            _ = decoder.decode(morse)
        }
    }
}

// MARK: - 运行测试的辅助函数

func runAllTests() {
    print("=== Morse Utils Tests ===\n")
    
    // 手动运行关键测试
    let encoder = MorseEncoder()
    let decoder = MorseDecoder()
    
    // 编码测试
    print("1. 编码测试:")
    print("   'SOS' -> \(encoder.encode("SOS"))")
    print("   'HELLO' -> \(encoder.encode("HELLO"))")
    print("   'HELLO WORLD' -> \(encoder.encode("HELLO WORLD"))")
    print("   '你好' -> \(encoder.encode("你好")) (未知字符)")
    
    // 解码测试
    print("\n2. 解码测试:")
    print("   '... --- ...' -> \(decoder.decode("... --- ..."))")
    print("   '.... . .-.. .-.. ---' -> \(decoder.decode(".... . .-.. .-.. ---"))")
    
    // 往返测试
    print("\n3. 往返测试:")
    let testText = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    let encoded = encoder.encode(testText)
    let decoded = decoder.decode(encoded)
    print("   原文: \(testText)")
    print("   编码: \(encoded)")
    print("   解码: \(decoded)")
    print("   匹配: \(testText == decoded ? "✓" : "✗")")
    
    // Prosign 测试
    print("\n4. Prosign 测试:")
    print("   SOS: \(MorseProsign.find(name: "SOS")?.code ?? "") - \(MorseProsign.find(name: "SOS")?.meaning ?? "")")
    print("   AR: \(MorseProsign.find(name: "AR")?.code ?? "") - \(MorseProsign.find(name: "AR")?.meaning ?? "")")
    
    // 统计测试
    print("\n5. 统计测试:")
    let stats = MorseStats.analyze("SOS SOS")
    print("   文本: SOS SOS")
    print("   点号数: \(stats["dotCount"] ?? 0)")
    print("   划号数: \(stats["dashCount"] ?? 0)")
    print("   总时长: \(stats["durationMs"] ?? 0)ms")
    
    // 表格测试
    print("\n6. 字符表格:")
    let table = MorseStats.table("HELLO")
    for entry in table {
        print("   \(entry.char): \(entry.morse)")
    }
    
    print("\n=== 测试完成 ===")
}

// 运行测试
runAllTests()