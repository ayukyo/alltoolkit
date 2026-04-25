/**
 * AllToolkit - Swift Morse Code Utilities
 *
 * 摩尔斯电码工具类，提供文本与摩尔斯电码之间的编码和解码功能。
 * 零依赖，仅使用 Swift 标准库。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation
import AVFoundation

// MARK: - Morse Code 字符映射

/// 摩尔斯电码字符映射表
public struct MorseCodeMap {
    
    /// 字母映射（A-Z）
    public static let letters: [Character: String] = [
        "A": ".-",     "B": "-...",   "C": "-.-.",   "D": "-..",    "E": ".",
        "F": "..-.",   "G": "--.",    "H": "....",   "I": "..",     "J": ".---",
        "K": "-.-",    "L": ".-..",   "M": "--",     "N": "-.",     "O": "---",
        "P": ".--.",   "Q": "--.-",   "R": ".-.",    "S": "...",    "T": "-",
        "U": "..-",    "V": "...-",   "W": ".--",    "X": "-..-",   "Y": "-.--",
        "Z": "--.."
    ]
    
    /// 数字映射（0-9）
    public static let numbers: [Character: String] = [
        "0": "-----",  "1": ".----",  "2": "..---",  "3": "...--",  "4": "....-",
        "5": ".....",  "6": "-....",  "7": "--...",  "8": "---..",  "9": "----."
    ]
    
    /// 标点符号映射
    public static let punctuation: [Character: String] = [
        ".": ".-.-.-",    ",": "--..--",    "?": "..--..",    "'": ".----.",
        "!": "-.-.--",    "/": "-..-.",     "(": "-.--.",     ")": "-.--.-",
        "&": ".-...",     ":": "---...",    ";": "-.-.-.",    "=": "-...-",
        "+": ".-.-.",     "-": "-....-",    "_": "..--.-",    "\"": ".-..-.",
        "$": "...-..-",   "@": ".--.-.",    "¿": "..-.-",     "¡": "--...-"
    ]
    
    /// 反向映射（摩尔斯电码 -> 字符）
    public static let reverseLetters: [String: Character] = {
        return Dictionary(uniqueKeysWithValues: letters.map { ($1, $0) })
    }()
    
    public static let reverseNumbers: [String: Character] = {
        return Dictionary(uniqueKeysWithValues: numbers.map { ($1, $0) })
    }()
    
    public static let reversePunctuation: [String: Character] = {
        return Dictionary(uniqueKeysWithValues: punctuation.map { ($1, $0) })
    }()
    
    /// 获取所有字符到摩尔斯电码的映射
    public static var allMappings: [Character: String] {
        return letters.merging(numbers) { $1 }.merging(punctuation) { $1 }
    }
    
    /// 获取所有摩尔斯电码到字符的映射
    public static var allReverseMappings: [String: Character] {
        return reverseLetters.merging(reverseNumbers) { $1 }.merging(reversePunctuation) { $1 }
    }
}

// MARK: - 常用 Prosigns（程序信号）

/// 摩尔斯电码程序信号（Prosigns）
public struct MorseProsign {
    /// 信号名称
    public let name: String
    /// 摩尔斯电码表示
    public let code: String
    /// 含义描述
    public let meaning: String
    
    /// 常用程序信号列表
    public static let all: [MorseProsign] = [
        MorseProsign(name: "AA", code: ".-.-", meaning: "新行/分段 (All After)"),
        MorseProsign(name: "AR", code: ".-.-.", meaning: "消息结束 (End of Message)"),
        MorseProsign(name: "AS", code: ".-...", meaning: "等待 (Wait)"),
        MorseProsign(name: "BT", code: "-...-", meaning: "分段符 (Break/Double Dash)"),
        MorseProsign(name: "CL", code: "-.-..-.", meaning: "关闭电台 (Going Off Air)"),
        MorseProsign(name: "CT", code: "-.-.-", meaning: "开始复制 (Starting Signal)"),
        MorseProsign(name: "DO", code: "-..---", meaning: "更改为明文 (Change to Plain Language)"),
        MorseProsign(name: "KN", code: "-.--.", meaning: "仅邀请指定台站 (Go Ahead, Specific Station)"),
        MorseProsign(name: "SK", code: "...-.-", meaning: "通信结束 (End of Contact)"),
        MorseProsign(name: "SN", code: "...-.", meaning: "理解了 (Understood)"),
        MorseProsign(name: "SOS", code: "...---...", meaning: "紧急求救信号 (Distress Signal)"),
        MorseProsign(name: "HH", code: "........", meaning: "错误/取消 (Error/Erase)")
    ]
    
    /// 根据名称查找程序信号
    public static func find(name: String) -> MorseProsign? {
        return all.first { $0.name == name.uppercased() }
    }
    
    /// 根据摩尔斯电码查找程序信号
    public static func find(code: String) -> MorseProsign? {
        return all.first { $0.code == code }
    }
}

// MARK: - 摩尔斯电码编码器

/// 摩尔斯电码编码器
public struct MorseEncoder {
    
    /// 单位时间（点号持续时间，单位：毫秒）
    public var dotDuration: TimeInterval = 60
    
    /// 划号持续时间（通常为点号的 3 倍）
    public var dashDuration: TimeInterval { return dotDuration * 3 }
    
    /// 字符内间隔（点号持续时间）
    public var intraCharSpace: TimeInterval { return dotDuration }
    
    /// 字符间间隔（通常为点号的 3 倍）
    public var interCharSpace: TimeInterval { return dotDuration * 3 }
    
    /// 单词间间隔（通常为点号的 7 倍）
    public var wordSpace: TimeInterval { return dotDuration * 7 }
    
    /// 点号的文本表示
    public var dotSymbol: Character = "."
    
    /// 划号的文本表示
    public var dashSymbol: Character = "-"
    
    /// 字符分隔符
    public var charSeparator: String = " "
    
    /// 单词分隔符
    public var wordSeparator: String = " / "
    
    /// 是否支持小写字母
    public var supportLowercase: Bool = true
    
    /// 是否忽略未知字符
    public var ignoreUnknown: Bool = true
    
    /// 默认编码器
    public init() {}
    
    /// 自定义编码器
    public init(dotDuration: TimeInterval = 60,
                dotSymbol: Character = ".",
                dashSymbol: Character = "-",
                charSeparator: String = " ",
                wordSeparator: String = " / ",
                supportLowercase: Bool = true,
                ignoreUnknown: Bool = true) {
        self.dotDuration = dotDuration
        self.dotSymbol = dotSymbol
        self.dashSymbol = dashSymbol
        self.charSeparator = charSeparator
        self.wordSeparator = wordSeparator
        self.supportLowercase = supportLowercase
        self.ignoreUnknown = ignoreUnknown
    }
    
    /// 将文本编码为摩尔斯电码
    /// - Parameter text: 要编码的文本
    /// - Returns: 摩尔斯电码字符串
    public func encode(_ text: String) -> String {
        var result: [String] = []
        var currentWord: [String] = []
        
        for char in text {
            if char == " " {
                // 单词分隔
                if !currentWord.isEmpty {
                    result.append(currentWord.joined(separator: charSeparator))
                    currentWord = []
                }
                continue
            }
            
            let morseChar = encodeCharacter(char)
            if !morseChar.isEmpty {
                currentWord.append(morseChar)
            } else if !ignoreUnknown {
                currentWord.append("?\(char)?")
            }
        }
        
        // 处理最后一个单词
        if !currentWord.isEmpty {
            result.append(currentWord.joined(separator: charSeparator))
        }
        
        return result.joined(separator: wordSeparator)
    }
    
    /// 编码单个字符
    /// - Parameter char: 要编码的字符
    /// - Returns: 摩尔斯电码表示
    public func encodeCharacter(_ char: Character) -> String {
        let upperChar = char.uppercased().first ?? char
        let lowerChar = char.lowercased().first ?? char
        
        // 先尝试原始字符
        if let code = MorseCodeMap.allMappings[char] {
            return convertSymbols(code)
        }
        
        // 尝试大写
        if let code = MorseCodeMap.allMappings[upperChar] {
            return convertSymbols(code)
        }
        
        // 尝试小写
        if supportLowercase, let code = MorseCodeMap.allMappings[lowerChar] {
            return convertSymbols(code)
        }
        
        return ""
    }
    
    /// 转换符号表示
    private func convertSymbols(_ code: String) -> String {
        return code.map { char in
            switch char {
            case ".":
                return String(dotSymbol)
            case "-":
                return String(dashSymbol)
            default:
                return String(char)
            }
        }.joined()
    }
    
    /// 计算发送指定摩尔斯电码所需的时间
    /// - Parameter morse: 摩尔斯电码字符串
    /// - Returns: 总时间（毫秒）
    public func calculateDuration(_ morse: String) -> TimeInterval {
        var totalDuration: TimeInterval = 0
        var isInChar = false
        
        for char in morse {
            switch char {
            case dotSymbol:
                totalDuration += dotDuration + intraCharSpace
                isInChar = true
            case dashSymbol:
                totalDuration += dashDuration + intraCharSpace
                isInChar = true
            case " ":
                if isInChar {
                    // 字符间间隔（已经加了 intraCharSpace，所以补差值）
                    totalDuration += interCharSpace - intraCharSpace
                    isInChar = false
                }
            default:
                break
            }
        }
        
        return totalDuration
    }
}

// MARK: - 摩尔斯电码解码器

/// 摩尔斯电码解码器
public struct MorseDecoder {
    
    /// 点号的文本表示
    public var dotSymbol: Character = "."
    
    /// 划号的文本表示
    public var dashSymbol: Character = "-"
    
    /// 字符分隔符
    public var charSeparators: Set<Character> = [" "]
    
    /// 单词分隔符
    public var wordSeparators: Set<String> = ["/"]
    
    /// 未知字符的替换字符
    public var unknownChar: Character = ""
    
    /// 默认解码器
    public init() {}
    
    /// 自定义解码器
    public init(dotSymbol: Character = ".",
                dashSymbol: Character = "-",
                charSeparators: Set<Character> = [" "],
                wordSeparators: Set<String> = ["/"],
                unknownChar: Character = "") {
        self.dotSymbol = dotSymbol
        self.dashSymbol = dashSymbol
        self.charSeparators = charSeparators
        self.wordSeparators = wordSeparators
        self.unknownChar = unknownChar
    }
    
    /// 将摩尔斯电码解码为文本
    /// - Parameter morse: 摩尔斯电码字符串
    /// - Returns: 解码后的文本
    public func decode(_ morse: String) -> String {
        var result: [String] = []
        var currentWord: [Character] = []
        var currentCode: [Character] = []
        
        func decodeCurrentCode() {
            if !currentCode.isEmpty {
                let code = String(currentCode)
                let normalizedCode = normalizeCode(code)
                if let char = MorseCodeMap.allReverseMappings[normalizedCode] {
                    currentWord.append(char)
                } else if let prosign = MorseProsign.find(code: normalizedCode) {
                    currentWord.append(contentsOf: "[\(prosign.name)]")
                } else {
                    currentWord.append(unknownChar)
                }
                currentCode = []
            }
        }
        
        func finishWord() {
            decodeCurrentCode()
            if !currentWord.isEmpty {
                result.append(String(currentWord))
                currentWord = []
            }
        }
        
        var i = morse.startIndex
        while i < morse.endIndex {
            let char = morse[i]
            
            // 检查单词分隔符
            var isWordSeparator = false
            for sep in wordSeparators {
                if morse[i...].starts(with: sep) {
                    finishWord()
                    result.append(" ")
                    i = morse.index(i, offsetBy: sep.count)
                    isWordSeparator = true
                    break
                }
            }
            if isWordSeparator { continue }
            
            // 字符分隔符
            if charSeparators.contains(char) {
                decodeCurrentCode()
            } else if char == dotSymbol || char == dashSymbol {
                currentCode.append(char)
            } else if char == "." || char == "-" {
                // 支持标准符号
                currentCode.append(char)
            }
            
            i = morse.index(after: i)
        }
        
        // 处理最后一个
        finishWord()
        
        return result.joined()
    }
    
    /// 解码单个摩尔斯电码
    /// - Parameter code: 摩尔斯电码字符串
    /// - Returns: 解码后的字符，如果无法识别返回 nil
    public func decodeCode(_ code: String) -> Character? {
        let normalizedCode = normalizeCode(code)
        return MorseCodeMap.allReverseMappings[normalizedCode]
    }
    
    /// 规范化摩尔斯电码（统一使用标准符号）
    private func normalizeCode(_ code: String) -> String {
        return code.map { char in
            if char == dotSymbol { return "." }
            if char == dashSymbol { return "-" }
            return char
        }.joined()
    }
}

// MARK: - 摩尔斯电码播放器

/// 摩尔斯电码音频播放器
public class MorsePlayer {
    
    /// 编码器配置
    public var encoder: MorseEncoder
    
    /// 音频频率（赫兹）
    public var frequency: Float = 600
    
    /// 音量（0.0 - 1.0）
    public var volume: Float = 0.5
    
    /// 音频引擎
    private var audioEngine: AVAudioEngine?
    
    /// 音频播放节点
    private var playerNode: AVAudioPlayerNode?
    
    /// 是否正在播放
    public private(set) var isPlaying: Bool = false
    
    /// 默认播放器
    public init() {
        self.encoder = MorseEncoder()
    }
    
    /// 自定义播放器
    public init(encoder: MorseEncoder, frequency: Float = 600, volume: Float = 0.5) {
        self.encoder = encoder
        self.frequency = frequency
        self.volume = max(0, min(1, volume))
    }
    
    /// 播放摩尔斯电码音频
    /// - Parameter morse: 摩尔斯电码字符串
    /// - Parameter completion: 播放完成回调
    public func play(_ morse: String, completion: (() -> Void)? = nil) {
        guard !isPlaying else { return }
        
        isPlaying = true
        
        // 生成音频数据
        let audioData = generateAudioData(for: morse)
        
        // 配置音频引擎
        audioEngine = AVAudioEngine()
        playerNode = AVAudioPlayerNode()
        
        guard let playerNode = playerNode,
              let audioEngine = audioEngine else {
            isPlaying = false
            completion?()
            return
        }
        
        audioEngine.attach(playerNode)
        audioEngine.connect(playerNode, to: audioEngine.mainMixerNode, format: nil)
        
        do {
            try audioEngine.start()
        } catch {
            isPlaying = false
            completion?()
            return
        }
        
        // 创建音频缓冲区
        let format = AVAudioFormat(commonFormat: .pcmFormatFloat32, sampleRate: 44100, channels: 1, interleaved: false)!
        let frameCount = AVAudioFrameCount(audioData.count)
        
        guard let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: frameCount) else {
            isPlaying = false
            completion?()
            return
        }
        
        buffer.frameLength = frameCount
        let channelData = buffer.floatChannelData?[0]
        audioData.withUnsafeBufferPointer { pointer in
            if let baseAddress = pointer.baseAddress {
                channelData?.initialize(from: baseAddress, count: audioData.count)
            }
        }
        
        // 播放完成后的回调
        playerNode.scheduleBuffer(buffer) { [weak self] in
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                self?.stop()
                completion?()
            }
        }
        
        playerNode.play()
    }
    
    /// 播放文本对应的摩尔斯电码
    /// - Parameter text: 要播放的文本
    /// - Parameter completion: 播放完成回调
    public func playText(_ text: String, completion: (() -> Void)? = nil) {
        let morse = encoder.encode(text)
        play(morse, completion: completion)
    }
    
    /// 停止播放
    public func stop() {
        playerNode?.stop()
        audioEngine?.stop()
        audioEngine = nil
        playerNode = nil
        isPlaying = false
    }
    
    /// 生成音频数据
    private func generateAudioData(for morse: String) -> [Float] {
        var samples: [Float] = []
        let sampleRate: Double = 44100
        
        for char in morse {
            switch char {
            case encoder.dotSymbol, ".":
                // 点号
                samples.append(contentsOf: generateTone(duration: encoder.dotDuration, sampleRate: sampleRate))
                samples.append(contentsOf: generateSilence(duration: encoder.intraCharSpace, sampleRate: sampleRate))
                
            case encoder.dashSymbol, "-":
                // 划号
                samples.append(contentsOf: generateTone(duration: encoder.dashDuration, sampleRate: sampleRate))
                samples.append(contentsOf: generateSilence(duration: encoder.intraCharSpace, sampleRate: sampleRate))
                
            case " ":
                // 字符/单词间隔
                samples.append(contentsOf: generateSilence(duration: encoder.interCharSpace - encoder.intraCharSpace, sampleRate: sampleRate))
                
            case "/":
                // 单词分隔符
                samples.append(contentsOf: generateSilence(duration: encoder.wordSpace, sampleRate: sampleRate))
                
            default:
                break
            }
        }
        
        return samples
    }
    
    /// 生成单音
    private func generateTone(duration: TimeInterval, sampleRate: Double) -> [Float] {
        let sampleCount = Int(duration * sampleRate / 1000)
        var samples: [Float] = []
        samples.reserveCapacity(sampleCount)
        
        for i in 0..<sampleCount {
            let t = Double(i) / sampleRate
            let sample = sin(2.0 * Double.pi * Double(frequency) * t)
            // 应用淡入淡出效果
            let fadeIn = min(1.0, Double(i) / (sampleRate * 0.005)) // 5ms 淡入
            let fadeOut = min(1.0, Double(sampleCount - i - 1) / (sampleRate * 0.005)) // 5ms 淡出
            let envelope = fadeIn * fadeOut
            samples.append(Float(sample * Double(volume) * envelope))
        }
        
        return samples
    }
    
    /// 生成静音
    private func generateSilence(duration: TimeInterval, sampleRate: Double) -> [Float] {
        let sampleCount = Int(duration * sampleRate / 1000)
        return [Float](repeating: 0.0, count: max(0, sampleCount))
    }
}

// MARK: - 便捷扩展

public extension String {
    
    /// 将字符串编码为摩尔斯电码
    /// - Parameter encoder: 编码器配置（可选）
    /// - Returns: 摩尔斯电码字符串
    func toMorse(encoder: MorseEncoder = MorseEncoder()) -> String {
        return encoder.encode(self)
    }
    
    /// 从摩尔斯电码解码为字符串
    /// - Parameter decoder: 解码器配置（可选）
    /// - Returns: 解码后的字符串
    func fromMorse(decoder: MorseDecoder = MorseDecoder()) -> String {
        return decoder.decode(self)
    }
}

// MARK: - 统计工具

/// 摩尔斯电码统计工具
public struct MorseStats {
    
    /// 计算文本编码后的摩尔斯电码统计信息
    /// - Parameter text: 原始文本
    /// - Parameter encoder: 编码器配置
    /// - Returns: 统计信息字典
    public static func analyze(_ text: String, encoder: MorseEncoder = MorseEncoder()) -> [String: Any] {
        let morse = encoder.encode(text)
        let dots = morse.filter { $0 == encoder.dotSymbol || $0 == "." }.count
        let dashes = morse.filter { $0 == encoder.dashSymbol || $0 == "-" }.count
        let duration = encoder.calculateDuration(morse)
        let wordCount = text.split(separator: " ").count
        let charCount = text.filter { $0 != " " }.count
        
        return [
            "originalText": text,
            "morseCode": morse,
            "dotCount": dots,
            "dashCount": dashes,
            "totalSignals": dots + dashes,
            "durationMs": duration,
            "durationSeconds": duration / 1000,
            "wordCount": wordCount,
            "characterCount": charCount,
            "averageSignalPerChar": charCount > 0 ? Double(dots + dashes) / Double(charCount) : 0,
            "averageDurationPerChar": charCount > 0 ? duration / Double(charCount) : 0
        ]
    }
    
    /// 获取指定文本的摩尔斯电码表格
    /// - Parameter text: 原始文本
    /// - Parameter encoder: 编码器配置
    /// - Returns: 字符-摩尔斯电码映射数组
    public static func table(_ text: String, encoder: MorseEncoder = MorseEncoder()) -> [(char: String, morse: String)] {
        var result: [(String, String)] = []
        var seen: Set<Character> = []
        
        for char in text.uppercased() {
            if char == " " {
                if !seen.contains(" ") {
                    result.append(("空格", "单词分隔"))
                    seen.insert(" ")
                }
            } else if !seen.contains(char) {
                let morse = encoder.encodeCharacter(char)
                if !morse.isEmpty {
                    result.append((String(char), morse))
                    seen.insert(char)
                }
            }
        }
        
        return result
    }
}