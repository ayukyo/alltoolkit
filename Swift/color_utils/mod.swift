/**
 * AllToolkit - Swift Color Utilities
 *
 * 通用颜色工具类，提供颜色格式转换、混合、对比度计算等功能。
 * 零依赖，仅使用 Swift 标准库。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation
#if canImport(AppKit)
import AppKit
public typealias PlatformColor = NSColor
#elseif canImport(UIKit)
import UIKit
public typealias PlatformColor = UIColor
#endif

// MARK: - Color 结构体

/// 表示一个 RGBA 颜色
public struct Color: Equatable, Hashable, Codable {
    public var red: Double      // 0.0 - 1.0
    public var green: Double    // 0.0 - 1.0
    public var blue: Double     // 0.0 - 1.0
    public var alpha: Double    // 0.0 - 1.0
    
    public init(red: Double, green: Double, blue: Double, alpha: Double = 1.0) {
        self.red = min(max(red, 0), 1)
        self.green = min(max(green, 0), 1)
        self.blue = min(max(blue, 0), 1)
        self.alpha = min(max(alpha, 0), 1)
    }
    
    public init(r: Int, g: Int, b: Int, a: Double = 1.0) {
        self.red = Double(min(max(r, 0), 255)) / 255.0
        self.green = Double(min(max(g, 0), 255)) / 255.0
        self.blue = Double(min(max(b, 0), 255)) / 255.0
        self.alpha = min(max(a, 0), 1)
    }
}

// MARK: - 预定义颜色

public extension Color {
    static let black = Color(red: 0, green: 0, blue: 0)
    static let white = Color(red: 1, green: 1, blue: 1)
    static let red = Color(red: 1, green: 0, blue: 0)
    static let green = Color(red: 0, green: 1, blue: 0)
    static let blue = Color(red: 0, green: 0, blue: 1)
    static let yellow = Color(red: 1, green: 1, blue: 0)
    static let cyan = Color(red: 0, green: 1, blue: 1)
    static let magenta = Color(red: 1, green: 0, blue: 1)
    static let orange = Color(red: 1, green: 0.5, blue: 0)
    static let purple = Color(red: 0.5, green: 0, blue: 0.5)
    static let gray = Color(red: 0.5, green: 0.5, blue: 0.5)
    static let lightGray = Color(red: 0.75, green: 0.75, blue: 0.75)
    static let darkGray = Color(red: 0.25, green: 0.25, blue: 0.25)
    static let transparent = Color(red: 0, green: 0, blue: 0, alpha: 0)
}

// MARK: - HEX 转换

public extension Color {
    
    /// 从十六进制字符串创建颜色
    /// - Parameters:
    ///   - hex: 十六进制字符串，支持 #RGB, #RGBA, #RRGGBB, #RRGGBBAA 格式
    /// - Returns: 颜色对象，解析失败返回 nil
    init?(hex: String) {
        var hexString = hex.trimmingCharacters(in: .whitespacesAndNewlines)
        hexString = hexString.replacingOccurrences(of: "#", with: "")
        
        var r: Double = 0
        var g: Double = 0
        var b: Double = 0
        var a: Double = 1
        
        let length = hexString.count
        
        guard [3, 4, 6, 8].contains(length) else { return nil }
        
        let scanner = Scanner(string: hexString)
        var hexValue: UInt64 = 0
        guard scanner.scanHexInt64(&hexValue) else { return nil }
        
        switch length {
        case 3: // RGB
            r = Double((hexValue & 0xF00) >> 8) / 15.0
            g = Double((hexValue & 0x0F0) >> 4) / 15.0
            b = Double(hexValue & 0x00F) / 15.0
        case 4: // RGBA
            r = Double((hexValue & 0xF000) >> 12) / 15.0
            g = Double((hexValue & 0x0F00) >> 8) / 15.0
            b = Double((hexValue & 0x00F0) >> 4) / 15.0
            a = Double(hexValue & 0x000F) / 15.0
        case 6: // RRGGBB
            r = Double((hexValue & 0xFF0000) >> 16) / 255.0
            g = Double((hexValue & 0x00FF00) >> 8) / 255.0
            b = Double(hexValue & 0x0000FF) / 255.0
        case 8: // RRGGBBAA
            r = Double((hexValue & 0xFF000000) >> 24) / 255.0
            g = Double((hexValue & 0x00FF0000) >> 16) / 255.0
            b = Double((hexValue & 0x0000FF00) >> 8) / 255.0
            a = Double(hexValue & 0x000000FF) / 255.0
        default:
            return nil
        }
        
        self.init(red: r, green: g, blue: b, alpha: a)
    }
    
    /// 从十六进制整数创建颜色
    /// - Parameter hex: 十六进制整数，如 0xFF0000 表示红色
    init(hex: UInt32, alpha: Double = 1.0) {
        let r = Double((hex & 0xFF0000) >> 16) / 255.0
        let g = Double((hex & 0x00FF00) >> 8) / 255.0
        let b = Double(hex & 0x0000FF) / 255.0
        self.init(red: r, green: g, blue: b, alpha: alpha)
    }
    
    /// 转换为十六进制字符串
    /// - Parameter includeAlpha: 是否包含透明度
    /// - Returns: 十六进制字符串，如 "#FF0000"
    func toHex(includeAlpha: Bool = false) -> String {
        let r = Int(red * 255)
        let g = Int(green * 255)
        let b = Int(blue * 255)
        
        if includeAlpha {
            let a = Int(alpha * 255)
            return String(format: "#%02X%02X%02X%02X", r, g, b, a)
        } else {
            return String(format: "#%02X%02X%02X", r, g, b)
        }
    }
    
    /// 转换为十六进制整数
    func toHexInt() -> UInt32 {
        let r = UInt32(red * 255) << 16
        let g = UInt32(green * 255) << 8
        let b = UInt32(blue * 255)
        return r | g | b
    }
}

// MARK: - RGB 转换

public extension Color {
    
    /// RGB 整数值 (0-255)
    var rgbInt: (r: Int, g: Int, b: Int, a: Int) {
        return (
            Int(red * 255),
            Int(green * 255),
            Int(blue * 255),
            Int(alpha * 255)
        )
    }
    
    /// RGB 字符串，如 "rgb(255, 0, 0)"
    var rgbString: String {
        return "rgb(\(Int(red * 255)), \(Int(green * 255)), \(Int(blue * 255)))"
    }
    
    /// RGBA 字符串，如 "rgba(255, 0, 0, 1.0)"
    var rgbaString: String {
        return "rgba(\(Int(red * 255)), \(Int(green * 255)), \(Int(blue * 255)), \(alpha))"
    }
}

// MARK: - HSL 转换

public extension Color {
    
    /// HSL 颜色表示
    struct HSL: Equatable, Hashable, Codable {
        public var hue: Double        // 0.0 - 360.0
        public var saturation: Double // 0.0 - 1.0
        public var lightness: Double  // 0.0 - 1.0
        public var alpha: Double      // 0.0 - 1.0
        
        public init(hue: Double, saturation: Double, lightness: Double, alpha: Double = 1.0) {
            self.hue = hue.truncatingRemainder(dividingBy: 360)
            if self.hue < 0 { self.hue += 360 }
            self.saturation = min(max(saturation, 0), 1)
            self.lightness = min(max(lightness, 0), 1)
            self.alpha = min(max(alpha, 0), 1)
        }
    }
    
    /// 转换为 HSL
    var hsl: HSL {
        let max = Swift.max(red, green, blue)
        let min = Swift.min(red, green, blue)
        let delta = max - min
        
        var h: Double = 0
        var s: Double = 0
        let l = (max + min) / 2.0
        
        if delta != 0 {
            s = l > 0.5 ? delta / (2.0 - max - min) : delta / (max + min)
            
            if max == red {
                h = ((green - blue) / delta) + (green < blue ? 6.0 : 0.0)
            } else if max == green {
                h = ((blue - red) / delta) + 2.0
            } else {
                h = ((red - green) / delta) + 4.0
            }
            h *= 60
        }
        
        return HSL(hue: h, saturation: s, lightness: l, alpha: alpha)
    }
    
    /// 从 HSL 创建颜色
    init(hsl: HSL) {
        let h = hsl.hue / 360.0
        let s = hsl.saturation
        let l = hsl.lightness
        
        if s == 0 {
            self.init(red: l, green: l, blue: l, alpha: hsl.alpha)
            return
        }
        
        let q = l < 0.5 ? l * (1.0 + s) : l + s - l * s
        let p = 2.0 * l - q
        
        func hueToRGB(_ p: Double, _ q: Double, _ t: Double) -> Double {
            var t = t
            if t < 0 { t += 1 }
            if t > 1 { t -= 1 }
            if t < 1.0/6.0 { return p + (q - p) * 6.0 * t }
            if t < 1.0/2.0 { return q }
            if t < 2.0/3.0 { return p + (q - p) * (2.0/3.0 - t) * 6.0 }
            return p
        }
        
        let r = hueToRGB(p, q, h + 1.0/3.0)
        let g = hueToRGB(p, q, h)
        let b = hueToRGB(p, q, h - 1.0/3.0)
        
        self.init(red: r, green: g, blue: b, alpha: hsl.alpha)
    }
    
    /// 从 HSL 值创建颜色
    init(hue: Double, saturation: Double, lightness: Double, alpha: Double = 1.0) {
        let hsl = HSL(hue: hue, saturation: saturation, lightness: lightness, alpha: alpha)
        self.init(hsl: hsl)
    }
}

// MARK: - HSV/HSB 转换

public extension Color {
    
    /// HSV/HSB 颜色表示
    struct HSV: Equatable, Hashable, Codable {
        public var hue: Double        // 0.0 - 360.0
        public var saturation: Double // 0.0 - 1.0
        public var value: Double      // 0.0 - 1.0 (brightness)
        public var alpha: Double      // 0.0 - 1.0
        
        public init(hue: Double, saturation: Double, value: Double, alpha: Double = 1.0) {
            self.hue = hue.truncatingRemainder(dividingBy: 360)
            if self.hue < 0 { self.hue += 360 }
            self.saturation = min(max(saturation, 0), 1)
            self.value = min(max(value, 0), 1)
            self.alpha = min(max(alpha, 0), 1)
        }
    }
    
    /// 转换为 HSV
    var hsv: HSV {
        let max = Swift.max(red, green, blue)
        let min = Swift.min(red, green, blue)
        let delta = max - min
        
        var h: Double = 0
        let s = max == 0 ? 0 : delta / max
        let v = max
        
        if delta != 0 {
            if max == red {
                h = ((green - blue) / delta) + (green < blue ? 6.0 : 0.0)
            } else if max == green {
                h = ((blue - red) / delta) + 2.0
            } else {
                h = ((red - green) / delta) + 4.0
            }
            h *= 60
        }
        
        return HSV(hue: h, saturation: s, value: v, alpha: alpha)
    }
    
    /// 从 HSV 创建颜色
    init(hsv: HSV) {
        let h = hsv.hue / 60.0
        let s = hsv.saturation
        let v = hsv.value
        
        if s == 0 {
            self.init(red: v, green: v, blue: v, alpha: hsv.alpha)
            return
        }
        
        let i = floor(h)
        let f = h - i
        let p = v * (1.0 - s)
        let q = v * (1.0 - s * f)
        let t = v * (1.0 - s * (1.0 - f))
        
        let r, g, b: Double
        switch Int(i) % 6 {
        case 0: r = v; g = t; b = p
        case 1: r = q; g = v; b = p
        case 2: r = p; g = v; b = t
        case 3: r = p; g = q; b = v
        case 4: r = t; g = p; b = v
        default: r = v; g = p; b = q
        }
        
        self.init(red: r, green: g, blue: b, alpha: hsv.alpha)
    }
    
    /// 从 HSV 值创建颜色
    init(hue: Double, saturation: Double, value: Double, alpha: Double = 1.0) {
        let hsv = HSV(hue: hue, saturation: saturation, value: value, alpha: alpha)
        self.init(hsv: hsv)
    }
}

// MARK: - CMYK 转换

public extension Color {
    
    /// CMYK 颜色表示
    struct CMYK: Equatable, Hashable, Codable {
        public var cyan: Double    // 0.0 - 1.0
        public var magenta: Double // 0.0 - 1.0
        public var yellow: Double  // 0.0 - 1.0
        public var key: Double     // 0.0 - 1.0 (black)
        public var alpha: Double   // 0.0 - 1.0
        
        public init(cyan: Double, magenta: Double, yellow: Double, key: Double, alpha: Double = 1.0) {
            self.cyan = min(max(cyan, 0), 1)
            self.magenta = min(max(magenta, 0), 1)
            self.yellow = min(max(yellow, 0), 1)
            self.key = min(max(key, 0), 1)
            self.alpha = min(max(alpha, 0), 1)
        }
    }
    
    /// 转换为 CMYK
    var cmyk: CMYK {
        let r = red
        let g = green
        let b = blue
        
        let k = 1.0 - Swift.max(r, g, b)
        
        if k == 1.0 {
            return CMYK(cyan: 0, magenta: 0, yellow: 0, key: 1, alpha: alpha)
        }
        
        let c = (1.0 - r - k) / (1.0 - k)
        let m = (1.0 - g - k) / (1.0 - k)
        let y = (1.0 - b - k) / (1.0 - k)
        
        return CMYK(cyan: c, magenta: m, yellow: y, key: k, alpha: alpha)
    }
    
    /// 从 CMYK 创建颜色
    init(cmyk: CMYK) {
        let k = cmyk.key
        let r = (1.0 - cmyk.cyan) * (1.0 - k)
        let g = (1.0 - cmyk.magenta) * (1.0 - k)
        let b = (1.0 - cmyk.yellow) * (1.0 - k)
        self.init(red: r, green: g, blue: b, alpha: cmyk.alpha)
    }
    
    /// 从 CMYK 值创建颜色
    init(cyan: Double, magenta: Double, yellow: Double, key: Double, alpha: Double = 1.0) {
        let cmyk = CMYK(cyan: cyan, magenta: magenta, yellow: yellow, key: key, alpha: alpha)
        self.init(cmyk: cmyk)
    }
}

// MARK: - 颜色操作

public extension Color {
    
    /// 调整亮度
    /// - Parameter amount: 调整量，正数变亮，负数变暗 (-1.0 ~ 1.0)
    /// - Returns: 调整后的颜色
    func adjustBrightness(_ amount: Double) -> Color {
        let hsl = self.hsl
        return Color(hue: hsl.hue, 
                     saturation: hsl.saturation, 
                     lightness: min(max(hsl.lightness + amount, 0), 1),
                     alpha: hsl.alpha)
    }
    
    /// 变亮
    /// - Parameter amount: 变亮程度 (0.0 ~ 1.0)
    /// - Returns: 变亮后的颜色
    func lighten(_ amount: Double = 0.1) -> Color {
        return adjustBrightness(amount)
    }
    
    /// 变暗
    /// - Parameter amount: 变暗程度 (0.0 ~ 1.0)
    /// - Returns: 变暗后的颜色
    func darken(_ amount: Double = 0.1) -> Color {
        return adjustBrightness(-amount)
    }
    
    /// 调整饱和度
    /// - Parameter amount: 调整量，正数增加饱和度，负数降低饱和度
    /// - Returns: 调整后的颜色
    func adjustSaturation(_ amount: Double) -> Color {
        let hsl = self.hsl
        return Color(hue: hsl.hue,
                     saturation: min(max(hsl.saturation + amount, 0), 1),
                     lightness: hsl.lightness,
                     alpha: hsl.alpha)
    }
    
    /// 饱和化
    /// - Parameter amount: 饱和化程度 (0.0 ~ 1.0)
    /// - Returns: 饱和化后的颜色
    func saturate(_ amount: Double = 0.1) -> Color {
        return adjustSaturation(amount)
    }
    
    /// 去饱和
    /// - Parameter amount: 去饱和程度 (0.0 ~ 1.0)
    /// - Returns: 去饱和后的颜色
    func desaturate(_ amount: Double = 0.1) -> Color {
        return adjustSaturation(-amount)
    }
    
    /// 灰度化
    /// - Returns: 灰度颜色
    func grayscale() -> Color {
        let gray = 0.299 * red + 0.587 * green + 0.114 * blue
        return Color(red: gray, green: gray, blue: gray, alpha: alpha)
    }
    
    /// 反转颜色
    /// - Returns: 反转后的颜色
    func inverted() -> Color {
        return Color(red: 1.0 - red, green: 1.0 - green, blue: 1.0 - blue, alpha: alpha)
    }
    
    /// 设置透明度
    /// - Parameter alpha: 新的透明度 (0.0 ~ 1.0)
    /// - Returns: 新颜色
    func withAlpha(_ alpha: Double) -> Color {
        return Color(red: red, green: green, blue: blue, alpha: alpha)
    }
}

// MARK: - 颜色混合

public extension Color {
    
    /// 与另一个颜色混合
    /// - Parameters:
    ///   - other: 另一个颜色
    ///   - ratio: 混合比例 (0.0 = 完全是自己, 1.0 = 完全是另一个颜色)
    /// - Returns: 混合后的颜色
    func mix(with other: Color, ratio: Double = 0.5) -> Color {
        let t = min(max(ratio, 0), 1)
        return Color(
            red: red + (other.red - red) * t,
            green: green + (other.green - green) * t,
            blue: blue + (other.blue - blue) * t,
            alpha: alpha + (other.alpha - alpha) * t
        )
    }
    
    /// 与白色混合
    /// - Parameter ratio: 混合比例
    /// - Returns: 混合后的颜色
    func tint(_ ratio: Double = 0.1) -> Color {
        return mix(with: .white, ratio: ratio)
    }
    
    /// 与黑色混合
    /// - Parameter ratio: 混合比例
    /// - Returns: 混合后的颜色
    func shade(_ ratio: Double = 0.1) -> Color {
        return mix(with: .black, ratio: ratio)
    }
    
    /// 多个颜色按比例混合
    /// - Parameter colors: 颜色和权重的数组
    /// - Returns: 混合后的颜色
    static func weightedMix(_ colors: [(color: Color, weight: Double)]) -> Color? {
        guard !colors.isEmpty else { return nil }
        
        var totalWeight = 0.0
        var r = 0.0, g = 0.0, b = 0.0, a = 0.0
        
        for (color, weight) in colors {
            r += color.red * weight
            g += color.green * weight
            b += color.blue * weight
            a += color.alpha * weight
            totalWeight += weight
        }
        
        guard totalWeight > 0 else { return nil }
        
        return Color(
            red: r / totalWeight,
            green: g / totalWeight,
            blue: b / totalWeight,
            alpha: a / totalWeight
        )
    }
    
    /// 多个颜色平均混合
    /// - Parameter colors: 颜色数组
    /// - Returns: 平均颜色
    static func average(_ colors: [Color]) -> Color? {
        let weighted = colors.map { ($0, 1.0) }
        return weightedMix(weighted)
    }
}

// MARK: - 对比度和亮度

public extension Color {
    
    /// 计算相对亮度 (WCAG 标准)
    var relativeLuminance: Double {
        func gamma(_ v: Double) -> Double {
            return v <= 0.03928 ? v / 12.92 : pow((v + 0.055) / 1.055, 2.4)
        }
        return 0.2126 * gamma(red) + 0.7152 * gamma(green) + 0.0722 * gamma(blue)
    }
    
    /// 计算与另一个颜色的对比度 (WCAG 标准)
    /// - Parameter other: 另一个颜色
    /// - Returns: 对比度 (1.0 ~ 21.0)
    func contrastRatio(with other: Color) -> Double {
        let l1 = relativeLuminance
        let l2 = other.relativeLuminance
        let lighter = max(l1, l2)
        let darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)
    }
    
    /// 判断是否为亮色
    var isLight: Bool {
        return relativeLuminance > 0.5
    }
    
    /// 判断是否为暗色
    var isDark: Bool {
        return !isLight
    }
    
    /// 获取适合在当前颜色上显示的文字颜色
    var textColor: Color {
        return isLight ? .black : .white
    }
    
    /// WCAG AA 级别对比度检查 (正常文本)
    func passesWCAGAA(with other: Color) -> Bool {
        return contrastRatio(with: other) >= 4.5
    }
    
    /// WCAG AA 级别对比度检查 (大文本)
    func passesWCAGAALarge(with other: Color) -> Bool {
        return contrastRatio(with: other) >= 3.0
    }
    
    /// WCAG AAA 级别对比度检查 (正常文本)
    func passesWCAGAAA(with other: Color) -> Bool {
        return contrastRatio(with: other) >= 7.0
    }
}

// MARK: - 颜色生成

public extension Color {
    
    /// 生成随机颜色
    static func random(opaque: Bool = true) -> Color {
        return Color(
            red: Double.random(in: 0...1),
            green: Double.random(in: 0...1),
            blue: Double.random(in: 0...1),
            alpha: opaque ? 1.0 : Double.random(in: 0...1)
        )
    }
    
    /// 从种子生成一致的颜色
    static func fromSeed(_ seed: String) -> Color {
        var hash: UInt64 = 5381
        for char in seed.unicodeScalars {
            hash = ((hash << 5) &+ hash) &+ UInt64(char.value)
        }
        
        let r = Double((hash & 0xFF0000) >> 16) / 255.0
        let g = Double((hash & 0x00FF00) >> 8) / 255.0
        let b = Double(hash & 0x0000FF) / 255.0
        return Color(red: r, green: g, blue: b)
    }
    
    /// 生成调色板（基于当前颜色的类似色）
    /// - Parameter count: 调色板颜色数量
    /// - Returns: 颜色数组
    func analogousPalette(count: Int = 5) -> [Color] {
        let hsl = self.hsl
        var colors: [Color] = []
        let step = 30.0
        
        for i in 0..<count {
            let offset = Double(i - count / 2) * step
            colors.append(Color(hue: hsl.hue + offset, saturation: hsl.saturation, lightness: hsl.lightness))
        }
        
        return colors
    }
    
    /// 生成互补色调色板
    func complementaryPalette() -> [Color] {
        let hsl = self.hsl
        return [
            self,
            Color(hue: hsl.hue + 180, saturation: hsl.saturation, lightness: hsl.lightness)
        ]
    }
    
    /// 生成三色调色板
    func triadicPalette() -> [Color] {
        let hsl = self.hsl
        return [
            self,
            Color(hue: hsl.hue + 120, saturation: hsl.saturation, lightness: hsl.lightness),
            Color(hue: hsl.hue + 240, saturation: hsl.saturation, lightness: hsl.lightness)
        ]
    }
    
    /// 生成分裂互补色调色板
    func splitComplementaryPalette() -> [Color] {
        let hsl = self.hsl
        return [
            self,
            Color(hue: hsl.hue + 150, saturation: hsl.saturation, lightness: hsl.lightness),
            Color(hue: hsl.hue + 210, saturation: hsl.saturation, lightness: hsl.lightness)
        ]
    }
    
    /// 生成四色调色板
    func tetradicPalette() -> [Color] {
        let hsl = self.hsl
        return [
            self,
            Color(hue: hsl.hue + 90, saturation: hsl.saturation, lightness: hsl.lightness),
            Color(hue: hsl.hue + 180, saturation: hsl.saturation, lightness: hsl.lightness),
            Color(hue: hsl.hue + 270, saturation: hsl.saturation, lightness: hsl.lightness)
        ]
    }
    
    /// 生成单色调色板
    /// - Parameter steps: 步数
    /// - Returns: 单色调色板
    func monochromaticPalette(steps: Int = 5) -> [Color] {
        let hsl = self.hsl
        var colors: [Color] = []
        let step = 1.0 / Double(steps + 1)
        
        for i in 1...steps {
            let lightness = step * Double(i)
            colors.append(Color(hue: hsl.hue, saturation: hsl.saturation, lightness: lightness))
        }
        
        return colors
    }
}

// MARK: - CSS 颜色名称

public extension Color {
    
    /// 从 CSS 颜色名称创建颜色
    init?(cssName: String) {
        let namedColors: [String: UInt32] = [
            "aliceblue": 0xF0F8FF,
            "antiquewhite": 0xFAEBD7,
            "aqua": 0x00FFFF,
            "aquamarine": 0x7FFFD4,
            "azure": 0xF0FFFF,
            "beige": 0xF5F5DC,
            "bisque": 0xFFE4C4,
            "black": 0x000000,
            "blanchedalmond": 0xFFEBCD,
            "blue": 0x0000FF,
            "blueviolet": 0x8A2BE2,
            "brown": 0xA52A2A,
            "burlywood": 0xDEB887,
            "cadetblue": 0x5F9EA0,
            "chartreuse": 0x7FFF00,
            "chocolate": 0xD2691E,
            "coral": 0xFF7F50,
            "cornflowerblue": 0x6495ED,
            "cornsilk": 0xFFF8DC,
            "crimson": 0xDC143C,
            "cyan": 0x00FFFF,
            "darkblue": 0x00008B,
            "darkcyan": 0x008B8B,
            "darkgoldenrod": 0xB8860B,
            "darkgray": 0xA9A9A9,
            "darkgreen": 0x006400,
            "darkgrey": 0xA9A9A9,
            "darkkhaki": 0xBDB76B,
            "darkmagenta": 0x8B008B,
            "darkolivegreen": 0x556B2F,
            "darkorange": 0xFF8C00,
            "darkorchid": 0x9932CC,
            "darkred": 0x8B0000,
            "darksalmon": 0xE9967A,
            "darkseagreen": 0x8FBC8F,
            "darkslateblue": 0x483D8B,
            "darkslategray": 0x2F4F4F,
            "darkslategrey": 0x2F4F4F,
            "darkturquoise": 0x00CED1,
            "darkviolet": 0x9400D3,
            "deeppink": 0xFF1493,
            "deepskyblue": 0x00BFFF,
            "dimgray": 0x696969,
            "dimgrey": 0x696969,
            "dodgerblue": 0x1E90FF,
            "firebrick": 0xB22222,
            "floralwhite": 0xFFFAF0,
            "forestgreen": 0x228B22,
            "fuchsia": 0xFF00FF,
            "gainsboro": 0xDCDCDC,
            "ghostwhite": 0xF8F8FF,
            "gold": 0xFFD700,
            "goldenrod": 0xDAA520,
            "gray": 0x808080,
            "green": 0x008000,
            "greenyellow": 0xADFF2F,
            "grey": 0x808080,
            "honeydew": 0xF0FFF0,
            "hotpink": 0xFF69B4,
            "indianred": 0xCD5C5C,
            "indigo": 0x4B0082,
            "ivory": 0xFFFFF0,
            "khaki": 0xF0E68C,
            "lavender": 0xE6E6FA,
            "lavenderblush": 0xFFF0F5,
            "lawngreen": 0x7CFC00,
            "lemonchiffon": 0xFFFACD,
            "lightblue": 0xADD8E6,
            "lightcoral": 0xF08080,
            "lightcyan": 0xE0FFFF,
            "lightgoldenrodyellow": 0xFAFAD2,
            "lightgray": 0xD3D3D3,
            "lightgreen": 0x90EE90,
            "lightgrey": 0xD3D3D3,
            "lightpink": 0xFFB6C1,
            "lightsalmon": 0xFFA07A,
            "lightseagreen": 0x20B2AA,
            "lightskyblue": 0x87CEFA,
            "lightslategray": 0x778899,
            "lightslategrey": 0x778899,
            "lightsteelblue": 0xB0C4DE,
            "lightyellow": 0xFFFFE0,
            "lime": 0x00FF00,
            "limegreen": 0x32CD32,
            "linen": 0xFAF0E6,
            "magenta": 0xFF00FF,
            "maroon": 0x800000,
            "mediumaquamarine": 0x66CDAA,
            "mediumblue": 0x0000CD,
            "mediumorchid": 0xBA55D3,
            "mediumpurple": 0x9370DB,
            "mediumseagreen": 0x3CB371,
            "mediumslateblue": 0x7B68EE,
            "mediumspringgreen": 0x00FA9A,
            "mediumturquoise": 0x48D1CC,
            "mediumvioletred": 0xC71585,
            "midnightblue": 0x191970,
            "mintcream": 0xF5FFFA,
            "mistyrose": 0xFFE4E1,
            "moccasin": 0xFFE4B5,
            "navajowhite": 0xFFDEAD,
            "navy": 0x000080,
            "oldlace": 0xFDF5E6,
            "olive": 0x808000,
            "olivedrab": 0x6B8E23,
            "orange": 0xFFA500,
            "orangered": 0xFF4500,
            "orchid": 0xDA70D6,
            "palegoldenrod": 0xEEE8AA,
            "palegreen": 0x98FB98,
            "paleturquoise": 0xAFEEEE,
            "palevioletred": 0xDB7093,
            "papayawhip": 0xFFEFD5,
            "peachpuff": 0xFFDAB9,
            "peru": 0xCD853F,
            "pink": 0xFFC0CB,
            "plum": 0xDDA0DD,
            "powderblue": 0xB0E0E6,
            "purple": 0x800080,
            "rebeccapurple": 0x663399,
            "red": 0xFF0000,
            "rosybrown": 0xBC8F8F,
            "royalblue": 0x4169E1,
            "saddlebrown": 0x8B4513,
            "salmon": 0xFA8072,
            "sandybrown": 0xF4A460,
            "seagreen": 0x2E8B57,
            "seashell": 0xFFF5EE,
            "sienna": 0xA0522D,
            "silver": 0xC0C0C0,
            "skyblue": 0x87CEEB,
            "slateblue": 0x6A5ACD,
            "slategray": 0x708090,
            "slategrey": 0x708090,
            "snow": 0xFFFAFA,
            "springgreen": 0x00FF7F,
            "steelblue": 0x4682B4,
            "tan": 0xD2B48C,
            "teal": 0x008080,
            "thistle": 0xD8BFD8,
            "tomato": 0xFF6347,
            "turquoise": 0x40E0D0,
            "violet": 0xEE82EE,
            "wheat": 0xF5DEB3,
            "white": 0xFFFFFF,
            "whitesmoke": 0xF5F5F5,
            "yellow": 0xFFFF00,
            "yellowgreen": 0x9ACD32
        ]
        
        let lowerName = cssName.lowercased().replacingOccurrences(of: " ", with: "")
        
        guard let hexValue = namedColors[lowerName] else {
            return nil
        }
        
        self.init(hex: hexValue)
    }
    
    /// CSS 颜色名称
    var cssName: String? {
        let hex = toHexInt()
        let namedColors: [UInt32: String] = [
            0xF0F8FF: "aliceblue", 0xFAEBD7: "antiquewhite", 0x00FFFF: "aqua",
            0x7FFFD4: "aquamarine", 0xF0FFFF: "azure", 0xF5F5DC: "beige",
            0xFFE4C4: "bisque", 0x000000: "black", 0xFFEBCD: "blanchedalmond",
            0x0000FF: "blue", 0x8A2BE2: "blueviolet", 0xA52A2A: "brown",
            0xDEB887: "burlywood", 0x5F9EA0: "cadetblue", 0x7FFF00: "chartreuse",
            0xD2691E: "chocolate", 0xFF7F50: "coral", 0x6495ED: "cornflowerblue",
            0xFFF8DC: "cornsilk", 0xDC143C: "crimson", 0x008B8B: "darkcyan",
            0xB8860B: "darkgoldenrod", 0xA9A9A9: "darkgray", 0x006400: "darkgreen",
            0xBDB76B: "darkkhaki", 0x8B008B: "darkmagenta", 0x556B2F: "darkolivegreen",
            0xFF8C00: "darkorange", 0x9932CC: "darkorchid", 0x8B0000: "darkred",
            0xE9967A: "darksalmon", 0x8FBC8F: "darkseagreen", 0x483D8B: "darkslateblue",
            0x2F4F4F: "darkslategray", 0x00CED1: "darkturquoise", 0x9400D3: "darkviolet",
            0xFF1493: "deeppink", 0x00BFFF: "deepskyblue", 0x696969: "dimgray",
            0x1E90FF: "dodgerblue", 0xB22222: "firebrick", 0xFFFAF0: "floralwhite",
            0x228B22: "forestgreen", 0xFF00FF: "fuchsia", 0xDCDCDC: "gainsboro",
            0xF8F8FF: "ghostwhite", 0xFFD700: "gold", 0xDAA520: "goldenrod",
            0x808080: "gray", 0x008000: "green", 0xADFF2F: "greenyellow",
            0xF0FFF0: "honeydew", 0xFF69B4: "hotpink", 0xCD5C5C: "indianred",
            0x4B0082: "indigo", 0xFFFFF0: "ivory", 0xF0E68C: "khaki",
            0xE6E6FA: "lavender", 0xFFF0F5: "lavenderblush", 0x7CFC00: "lawngreen",
            0xFFFACD: "lemonchiffon", 0xADD8E6: "lightblue", 0xF08080: "lightcoral",
            0xE0FFFF: "lightcyan", 0xFAFAD2: "lightgoldenrodyellow", 0xD3D3D3: "lightgray",
            0x90EE90: "lightgreen", 0xFFB6C1: "lightpink", 0xFFA07A: "lightsalmon",
            0x20B2AA: "lightseagreen", 0x87CEFA: "lightskyblue", 0x778899: "lightslategray",
            0xB0C4DE: "lightsteelblue", 0xFFFFE0: "lightyellow", 0x00FF00: "lime",
            0x32CD32: "limegreen", 0xFAF0E6: "linen", 0xFF00FF: "magenta",
            0x800000: "maroon", 0x66CDAA: "mediumaquamarine", 0x0000CD: "mediumblue",
            0xBA55D3: "mediumorchid", 0x9370DB: "mediumpurple", 0x3CB371: "mediumseagreen",
            0x7B68EE: "mediumslateblue", 0x00FA9A: "mediumspringgreen", 0x48D1CC: "mediumturquoise",
            0xC71585: "mediumvioletred", 0x191970: "midnightblue", 0xF5FFFA: "mintcream",
            0xFFE4E1: "mistyrose", 0xFFE4B5: "moccasin", 0xFFDEAD: "navajowhite",
            0x000080: "navy", 0xFDF5E6: "oldlace", 0x808000: "olive", 0x6B8E23: "olivedrab",
            0xFFA500: "orange", 0xFF4500: "orangered", 0xDA70D6: "orchid",
            0xEEE8AA: "palegoldenrod", 0x98FB98: "palegreen", 0xAFEEEE: "paleturquoise",
            0xDB7093: "palevioletred", 0xFFEFD5: "papayawhip", 0xFFDAB9: "peachpuff",
            0xCD853F: "peru", 0xFFC0CB: "pink", 0xDDA0DD: "plum", 0xB0E0E6: "powderblue",
            0x800080: "purple", 0x663399: "rebeccapurple", 0xFF0000: "red",
            0xBC8F8F: "rosybrown", 0x4169E1: "royalblue", 0x8B4513: "saddlebrown",
            0xFA8072: "salmon", 0xF4A460: "sandybrown", 0x2E8B57: "seagreen",
            0xFFF5EE: "seashell", 0xA0522D: "sienna", 0xC0C0C0: "silver",
            0x87CEEB: "skyblue", 0x6A5ACD: "slateblue", 0x708090: "slategray",
            0xFFFAFA: "snow", 0x00FF7F: "springgreen", 0x4682B4: "steelblue",
            0xD2B48C: "tan", 0x008080: "teal", 0xD8BFD8: "thistle",
            0xFF6347: "tomato", 0x40E0D0: "turquoise", 0xEE82EE: "violet",
            0xF5DEB3: "wheat", 0xFFFFFF: "white", 0xF5F5F5: "whitesmoke",
            0xFFFF00: "yellow", 0x9ACD32: "yellowgreen"
        ]
        return namedColors[hex]
    }
}

// MARK: - 平台颜色转换

#if canImport(AppKit) || canImport(UIKit)
public extension Color {
    
    /// 从平台颜色创建
    init(platform color: PlatformColor) {
        var r: CGFloat = 0
        var g: CGFloat = 0
        var b: CGFloat = 0
        var a: CGFloat = 0
        
        #if canImport(AppKit)
        color.usingColorSpace(.sRGB)?.getRed(&r, green: &g, blue: &b, alpha: &a)
        #else
        color.getRed(&r, green: &g, blue: &b, alpha: &a)
        #endif
        
        self.init(red: Double(r), green: Double(g), blue: Double(b), alpha: Double(a))
    }
    
    /// 转换为平台颜色
    func toPlatformColor() -> PlatformColor {
        #if canImport(AppKit)
        return PlatformColor(red: CGFloat(red), green: CGFloat(green), blue: CGFloat(blue), alpha: CGFloat(alpha))
        #else
        return PlatformColor(red: CGFloat(red), green: CGFloat(green), blue: CGFloat(blue), alpha: CGFloat(alpha))
        #endif
    }
}
#endif

// MARK: - ColorUtils 工具类

/// 颜色工具类
public final class ColorUtils {
    
    private init() {}
    
    // MARK: 解析颜色
    
    /// 从字符串解析颜色，支持多种格式
    /// - Parameter string: 颜色字符串
    /// - Returns: 颜色对象
    public static func parse(_ string: String) -> Color? {
        let trimmed = string.trimmingCharacters(in: .whitespacesAndNewlines)
        
        // 尝试 CSS 名称
        if let color = Color(cssName: trimmed) {
            return color
        }
        
        // 尝试 HEX
        if let color = Color(hex: trimmed) {
            return color
        }
        
        // 尝试 rgb(r, g, b)
        let rgbPattern = #"rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"#
        if let match = trimmed.range(of: rgbPattern, options: .regularExpression) {
            let values = trimmed[match]
                .replacingOccurrences(of: #"rgb\s*\(\s*"#, with: "", options: .regularExpression)
                .replacingOccurrences(of: #"\s*\)"#, with: "", options: .regularExpression)
                .split(separator: ",")
                .map { Int($0.trimmingCharacters(in: .whitespaces)) ?? 0 }
            if values.count == 3 {
                return Color(r: values[0], g: values[1], b: values[2])
            }
        }
        
        // 尝试 rgba(r, g, b, a)
        let rgbaPattern = #"rgba\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)"#
        if let match = trimmed.range(of: rgbaPattern, options: .regularExpression) {
            let values = trimmed[match]
                .replacingOccurrences(of: #"rgba\s*\(\s*"#, with: "", options: .regularExpression)
                .replacingOccurrences(of: #"\s*\)"#, with: "", options: .regularExpression)
                .split(separator: ",")
            if values.count == 4 {
                let r = Int(values[0].trimmingCharacters(in: .whitespaces)) ?? 0
                let g = Int(values[1].trimmingCharacters(in: .whitespaces)) ?? 0
                let b = Int(values[2].trimmingCharacters(in: .whitespaces)) ?? 0
                let a = Double(values[3].trimmingCharacters(in: .whitespaces)) ?? 1.0
                return Color(r: r, g: g, b: b, a: a)
            }
        }
        
        // 尝试 hsl(h, s%, l%)
        let hslPattern = #"hsl\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*\)"#
        if let match = trimmed.range(of: hslPattern, options: .regularExpression) {
            let values = trimmed[match]
                .replacingOccurrences(of: #"hsl\s*\(\s*"#, with: "", options: .regularExpression)
                .replacingOccurrences(of: #"\s*\)"#, with: "", options: .regularExpression)
                .replacingOccurrences(of: "%", with: "")
                .split(separator: ",")
            if values.count == 3 {
                let h = Double(values[0].trimmingCharacters(in: .whitespaces)) ?? 0
                let s = (Double(values[1].trimmingCharacters(in: .whitespaces)) ?? 0) / 100.0
                let l = (Double(values[2].trimmingCharacters(in: .whitespaces)) ?? 0) / 100.0
                return Color(hue: h, saturation: s, lightness: l)
            }
        }
        
        return nil
    }
    
    // MARK: 调色板生成
    
    /// 生成渐变调色板
    /// - Parameters:
    ///   - start: 起始颜色
    ///   - end: 结束颜色
    ///   - steps: 步数
    /// - Returns: 渐变颜色数组
    public static func gradient(from start: Color, to end: Color, steps: Int) -> [Color] {
        guard steps > 1 else { return [start] }
        
        return (0..<steps).map { i in
            let ratio = Double(i) / Double(steps - 1)
            return start.mix(with: end, ratio: ratio)
        }
    }
    
    /// 生成指定色调的调色板
    /// - Parameters:
    ///   - hue: 色调 (0-360)
    ///   - count: 颜色数量
    /// - Returns: 调色板
    public static func palette(hue: Double, count: Int = 5) -> [Color] {
        let base = Color(hue: hue, saturation: 0.7, lightness: 0.5)
        return base.analogousPalette(count: count)
    }
    
    /// 生成 Material Design 风格调色板
    /// - Parameter base: 基础颜色
    /// - Returns: Material Design 调色板
    public static func materialPalette(from base: Color) -> [String: Color] {
        return [
            "50": base.mix(with: .white, ratio: 0.9),
            "100": base.mix(with: .white, ratio: 0.7),
            "200": base.mix(with: .white, ratio: 0.5),
            "300": base.mix(with: .white, ratio: 0.3),
            "400": base.mix(with: .white, ratio: 0.1),
            "500": base,
            "600": base.mix(with: .black, ratio: 0.1),
            "700": base.mix(with: .black, ratio: 0.2),
            "800": base.mix(with: .black, ratio: 0.3),
            "900": base.mix(with: .black, ratio: 0.4)
        ]
    }
    
    /// 生成随机调色板
    /// - Parameter count: 颜色数量
    /// - Returns: 随机调色板
    public static func randomPalette(count: Int = 5) -> [Color] {
        let baseHue = Double.random(in: 0...360)
        return (0..<count).map { i in
            let hueOffset = Double(i) * (360.0 / Double(count))
            return Color(hue: baseHue + hueOffset, saturation: 0.7, lightness: 0.5)
        }
    }
    
    /// 生成和谐调色板
    /// - Parameter base: 基础颜色
    /// - Returns: 和谐调色板
    public static func harmoniousPalette(from base: Color) -> [Color] {
        let hsl = base.hsl
        return [
            Color(hue: hsl.hue, saturation: hsl.saturation, lightness: hsl.lightness),
            Color(hue: hsl.hue + 30, saturation: hsl.saturation, lightness: hsl.lightness),
            Color(hue: hsl.hue + 60, saturation: hsl.saturation * 0.8, lightness: hsl.lightness),
            Color(hue: hsl.hue + 180, saturation: hsl.saturation, lightness: hsl.lightness),
            Color(hue: hsl.hue + 210, saturation: hsl.saturation * 0.9, lightness: hsl.lightness * 0.8)
        ]
    }
    
    // MARK: 对比度计算
    
    /// 找出与背景色对比度最高的前景色
    /// - Parameters:
    ///   - background: 背景色
    ///   - candidates: 候选前景色
    /// - Returns: 对比度最高的前景色
    public static func bestContrast(for background: Color, among candidates: [Color]) -> Color? {
        return candidates.max { $0.contrastRatio(with: background) < $1.contrastRatio(with: background) }
    }
    
    /// 检查两个颜色是否符合 WCAG AA 标准
    public static func passesWCAGAA(foreground: Color, background: Color) -> Bool {
        return foreground.contrastRatio(with: background) >= 4.5
    }
    
    /// 检查两个颜色是否符合 WCAG AAA 标准
    public static func passesWCAGAAA(foreground: Color, background: Color) -> Bool {
        return foreground.contrastRatio(with: background) >= 7.0
    }
}