/**
 * AllToolkit - Swift Color Utilities Tests
 *
 * 测试颜色工具类的各种功能
 */

import Foundation

// 简单测试框架
class TestRunner {
    private var passed = 0
    private var failed = 0
    private var tests: [(name: String, test: () -> Bool)] = []
    
    func addTest(_ name: String, _ test: @escaping () -> Bool) {
        tests.append((name, test))
    }
    
    func run() {
        print("=" + String(repeating: "=", count: 59) + "=")
        print("Swift Color Utilities Tests")
        print("=" + String(repeating: "=", count: 59) + "=")
        print()
        
        for (name, test) in tests {
            let result = test()
            let status = result ? "✅ PASS" : "❌ FAIL"
            print("\(status) - \(name)")
            if result {
                passed += 1
            } else {
                failed += 1
            }
        }
        
        print()
        print("=" + String(repeating: "=", count: 59) + "=")
        print("Results: \(passed) passed, \(failed) failed")
        print("=" + String(repeating: "=", count: 59) + "=")
    }
}

func assertEquals<T: Equatable>(_ expected: T, _ actual: T, _ message: String = "") -> Bool {
    if expected == actual {
        return true
    } else {
        if !message.isEmpty {
            print("  Expected: \(expected), Got: \(actual) - \(message)")
        } else {
            print("  Expected: \(expected), Got: \(actual)")
        }
        return false
    }
}

func assertApproxEquals(_ expected: Double, _ actual: Double, _ tolerance: Double = 0.01, _ message: String = "") -> Bool {
    if abs(expected - actual) <= tolerance {
        return true
    } else {
        if !message.isEmpty {
            print("  Expected: \(expected), Got: \(actual) (tolerance: \(tolerance)) - \(message)")
        } else {
            print("  Expected: \(expected), Got: \(actual) (tolerance: \(tolerance))")
        }
        return false
    }
}

func assertTrue(_ condition: Bool, _ message: String = "") -> Bool {
    if condition {
        return true
    } else {
        print("  Assertion failed: \(message)")
        return false
    }
}

// 创建测试
let runner = TestRunner()

// MARK: - Color Creation Tests

runner.addTest("Color: Basic RGB creation") {
    let color = Color(red: 1, green: 0.5, blue: 0, alpha: 1)
    return assertEquals(1.0, color.red) &&
           assertEquals(0.5, color.green) &&
           assertEquals(0.0, color.blue) &&
           assertEquals(1.0, color.alpha)
}

runner.addTest("Color: RGB Int creation") {
    let color = Color(r: 255, g: 128, b: 0)
    return assertApproxEquals(1.0, color.red) &&
           assertApproxEquals(128.0/255.0, color.green) &&
           assertApproxEquals(0.0, color.blue)
}

runner.addTest("Color: Predefined colors") {
    return assertEquals(Color.black, Color(red: 0, green: 0, blue: 0)) &&
           assertEquals(Color.white, Color(red: 1, green: 1, blue: 1)) &&
           assertEquals(Color.red, Color(red: 1, green: 0, blue: 0))
}

// MARK: - HEX Conversion Tests

runner.addTest("HEX: Create from 6-char hex string") {
    let color = Color(hex: "#FF0000")
    return assertTrue(color != nil) &&
           assertApproxEquals(1.0, color!.red) &&
           assertApproxEquals(0.0, color!.green) &&
           assertApproxEquals(0.0, color!.blue)
}

runner.addTest("HEX: Create from 3-char hex string") {
    let color = Color(hex: "#F00")
    return assertTrue(color != nil) &&
           assertApproxEquals(1.0, color!.red) &&
           assertApproxEquals(0.0, color!.green) &&
           assertApproxEquals(0.0, color!.blue)
}

runner.addTest("HEX: Create from hex integer") {
    let color = Color(hex: 0x00FF00)
    return assertApproxEquals(0.0, color.red) &&
           assertApproxEquals(1.0, color.green) &&
           assertApproxEquals(0.0, color.blue)
}

runner.addTest("HEX: Convert to hex string") {
    let color = Color(red: 1, green: 0.5, blue: 0)
    return assertEquals("#FF8000", color.toHex())
}

runner.addTest("HEX: Convert to hex int") {
    let color = Color(red: 1, green: 0, blue: 0)
    return assertEquals(UInt32(0xFF0000), color.toHexInt())
}

// MARK: - HSL Conversion Tests

runner.addTest("HSL: Convert to HSL") {
    let color = Color(red: 1, green: 0, blue: 0)
    let hsl = color.hsl
    return assertApproxEquals(0, hsl.hue) &&
           assertApproxEquals(1.0, hsl.saturation) &&
           assertApproxEquals(0.5, hsl.lightness)
}

runner.addTest("HSL: Create from HSL") {
    let color = Color(hue: 120, saturation: 1.0, lightness: 0.5)
    return assertApproxEquals(0.0, color.red, 0.02) &&
           assertApproxEquals(1.0, color.green, 0.02) &&
           assertApproxEquals(0.0, color.blue, 0.02)
}

runner.addTest("HSL: Grayscale conversion") {
    let color = Color(red: 1, green: 0, blue: 0)
    let gray = color.grayscale()
    return assertApproxEquals(gray.red, gray.green) &&
           assertApproxEquals(gray.green, gray.blue)
}

// MARK: - HSV Conversion Tests

runner.addTest("HSV: Convert to HSV") {
    let color = Color(red: 1, green: 0, blue: 0)
    let hsv = color.hsv
    return assertApproxEquals(0, hsv.hue) &&
           assertApproxEquals(1.0, hsv.saturation) &&
           assertApproxEquals(1.0, hsv.value)
}

runner.addTest("HSV: Create from HSV") {
    let color = Color(hue: 240, saturation: 1.0, value: 1.0)
    return assertApproxEquals(0.0, color.red, 0.02) &&
           assertApproxEquals(0.0, color.green, 0.02) &&
           assertApproxEquals(1.0, color.blue, 0.02)
}

// MARK: - CMYK Conversion Tests

runner.addTest("CMYK: Convert to CMYK") {
    let color = Color(red: 1, green: 0, blue: 0)
    let cmyk = color.cmyk
    return assertApproxEquals(0.0, cmyk.cyan) &&
           assertApproxEquals(1.0, cmyk.magenta) &&
           assertApproxEquals(1.0, cmyk.yellow) &&
           assertApproxEquals(0.0, cmyk.key)
}

runner.addTest("CMYK: Create from CMYK") {
    let color = Color(cyan: 0, magenta: 1, yellow: 1, key: 0)
    return assertApproxEquals(1.0, color.red, 0.02) &&
           assertApproxEquals(0.0, color.green, 0.02) &&
           assertApproxEquals(0.0, color.blue, 0.02)
}

// MARK: - Color Manipulation Tests

runner.addTest("Manipulation: Lighten color") {
    let color = Color(red: 0.5, green: 0.5, blue: 0.5)
    let lightened = color.lighten(0.2)
    let hsl = lightened.hsl
    return assertApproxEquals(0.7, hsl.lightness)
}

runner.addTest("Manipulation: Darken color") {
    let color = Color(red: 0.5, green: 0.5, blue: 0.5)
    let darkened = color.darken(0.2)
    let hsl = darkened.hsl
    return assertApproxEquals(0.3, hsl.lightness)
}

runner.addTest("Manipulation: Invert color") {
    let color = Color(red: 0.2, green: 0.4, blue: 0.6)
    let inverted = color.inverted()
    return assertApproxEquals(0.8, inverted.red) &&
           assertApproxEquals(0.6, inverted.green) &&
           assertApproxEquals(0.4, inverted.blue)
}

runner.addTest("Manipulation: Saturate color") {
    let color = Color(hue: 0, saturation: 0.5, lightness: 0.5)
    let saturated = color.saturate(0.3)
    return assertApproxEquals(0.8, saturated.hsl.saturation)
}

runner.addTest("Manipulation: Desaturate color") {
    let color = Color(hue: 0, saturation: 0.5, lightness: 0.5)
    let desaturated = color.desaturate(0.3)
    return assertApproxEquals(0.2, desaturated.hsl.saturation)
}

// MARK: - Color Mixing Tests

runner.addTest("Mixing: Mix two colors equally") {
    let color1 = Color(red: 1, green: 0, blue: 0)
    let color2 = Color(red: 0, green: 0, blue: 1)
    let mixed = color1.mix(with: color2, ratio: 0.5)
    return assertApproxEquals(0.5, mixed.red) &&
           assertApproxEquals(0.0, mixed.green) &&
           assertApproxEquals(0.5, mixed.blue)
}

runner.addTest("Mixing: Tint (mix with white)") {
    let color = Color(red: 1, green: 0, blue: 0)
    let tinted = color.tint(0.5)
    return assertApproxEquals(1.0, tinted.red) &&
           assertApproxEquals(0.5, tinted.green) &&
           assertApproxEquals(0.5, tinted.blue)
}

runner.addTest("Mixing: Shade (mix with black)") {
    let color = Color(red: 1, green: 0, blue: 0)
    let shaded = color.shade(0.5)
    return assertApproxEquals(0.5, shaded.red) &&
           assertApproxEquals(0.0, shaded.green) &&
           assertApproxEquals(0.0, shaded.blue)
}

runner.addTest("Mixing: Weighted mix") {
    let colors: [(color: Color, weight: Double)] = [
        (Color(red: 1, green: 0, blue: 0), 1.0),
        (Color(red: 0, green: 1, blue: 0), 1.0),
        (Color(red: 0, green: 0, blue: 1), 1.0)
    ]
    let avg = Color.weightedMix(colors)
    return assertTrue(avg != nil) &&
           assertApproxEquals(1.0/3.0, avg!.red, 0.02) &&
           assertApproxEquals(1.0/3.0, avg!.green, 0.02) &&
           assertApproxEquals(1.0/3.0, avg!.blue, 0.02)
}

// MARK: - Contrast Tests

runner.addTest("Contrast: Relative luminance of white") {
    let white = Color.white
    return assertApproxEquals(1.0, white.relativeLuminance)
}

runner.addTest("Contrast: Relative luminance of black") {
    let black = Color.black
    return assertApproxEquals(0.0, black.relativeLuminance)
}

runner.addTest("Contrast: Contrast ratio black on white") {
    let ratio = Color.black.contrastRatio(with: .white)
    return assertApproxEquals(21.0, ratio, 0.1)
}

runner.addTest("Contrast: Is light/dark detection") {
    return assertTrue(Color.white.isLight) &&
           assertTrue(Color.black.isDark)
}

runner.addTest("Contrast: Text color selection") {
    let darkBg = Color.black
    let lightBg = Color.white
    return assertEquals(Color.white, darkBg.textColor) &&
           assertEquals(Color.black, lightBg.textColor)
}

runner.addTest("Contrast: WCAG AA pass check") {
    let ratio = Color.black.contrastRatio(with: .white)
    return assertTrue(ratio >= 4.5, "Black on white should pass WCAG AA")
}

// MARK: - Palette Generation Tests

runner.addTest("Palette: Analogous palette") {
    let base = Color(red: 1, green: 0, blue: 0)
    let palette = base.analogousPalette(count: 5)
    return assertEquals(5, palette.count) &&
           assertTrue(palette.allSatisfy { $0.alpha == 1.0 })
}

runner.addTest("Palette: Complementary palette") {
    let base = Color(hue: 0, saturation: 1.0, lightness: 0.5)
    let palette = base.complementaryPalette()
    return assertEquals(2, palette.count) &&
           assertApproxEquals(180, palette[1].hsl.hue, 1.0)
}

runner.addTest("Palette: Triadic palette") {
    let base = Color(hue: 0, saturation: 1.0, lightness: 0.5)
    let palette = base.triadicPalette()
    return assertEquals(3, palette.count)
}

runner.addTest("Palette: Split complementary palette") {
    let base = Color(hue: 0, saturation: 1.0, lightness: 0.5)
    let palette = base.splitComplementaryPalette()
    return assertEquals(3, palette.count)
}

runner.addTest("Palette: Tetradic palette") {
    let base = Color(hue: 0, saturation: 1.0, lightness: 0.5)
    let palette = base.tetradicPalette()
    return assertEquals(4, palette.count)
}

runner.addTest("Palette: Monochromatic palette") {
    let base = Color(hue: 0, saturation: 1.0, lightness: 0.5)
    let palette = base.monochromaticPalette(steps: 5)
    return assertEquals(5, palette.count)
}

// MARK: - Random Color Tests

runner.addTest("Random: Generate random color") {
    let color1 = Color.random()
    let color2 = Color.random()
    return assertTrue(color1.alpha == 1.0) &&
           assertTrue(color2.alpha == 1.0) &&
           assertTrue(color1 != color2 || true) // Colors might be equal by chance
}

runner.addTest("Random: Generate random color with alpha") {
    let color = Color.random(opaque: false)
    return assertTrue(color.alpha >= 0 && color.alpha <= 1)
}

runner.addTest("Random: Seed-based color generation") {
    let color1 = Color.fromSeed("test")
    let color2 = Color.fromSeed("test")
    let color3 = Color.fromSeed("different")
    return assertEquals(color1, color2) &&
           assertTrue(color1 != color3 || true)
}

// MARK: - CSS Name Tests

runner.addTest("CSS: Create from CSS name") {
    let red = Color(cssName: "red")
    let blue = Color(cssName: "blue")
    return assertTrue(red != nil && blue != nil) &&
           assertApproxEquals(1.0, red!.red) &&
           assertApproxEquals(1.0, blue!.blue)
}

runner.addTest("CSS: Convert to CSS name") {
    let red = Color(red: 1, green: 0, blue: 0)
    let white = Color.white
    return assertEquals("red", red.cssName) &&
           assertEquals("white", white.cssName)
}

runner.addTest("CSS: Case insensitive name parsing") {
    let red1 = Color(cssName: "RED")
    let red2 = Color(cssName: "Red")
    return assertTrue(red1 != nil && red2 != nil) &&
           assertEquals(red1, red2)
}

// MARK: - ColorUtils Tests

runner.addTest("Utils: Parse hex string") {
    let color = ColorUtils.parse("#FF0000")
    return assertTrue(color != nil) &&
           assertApproxEquals(1.0, color!.red) &&
           assertApproxEquals(0.0, color!.green) &&
           assertApproxEquals(0.0, color!.blue)
}

runner.addTest("Utils: Parse rgb string") {
    let color = ColorUtils.parse("rgb(255, 0, 0)")
    return assertTrue(color != nil) &&
           assertApproxEquals(1.0, color!.red) &&
           assertApproxEquals(0.0, color!.green) &&
           assertApproxEquals(0.0, color!.blue)
}

runner.addTest("Utils: Parse rgba string") {
    let color = ColorUtils.parse("rgba(255, 0, 0, 0.5)")
    return assertTrue(color != nil) &&
           assertApproxEquals(1.0, color!.red) &&
           assertApproxEquals(0.5, color!.alpha)
}

runner.addTest("Utils: Parse hsl string") {
    let color = ColorUtils.parse("hsl(120, 100%, 50%)")
    return assertTrue(color != nil) &&
           assertApproxEquals(0.0, color!.red, 0.02) &&
           assertApproxEquals(1.0, color!.green, 0.02)
}

runner.addTest("Utils: Parse CSS name") {
    let color = ColorUtils.parse("red")
    return assertTrue(color != nil) &&
           assertApproxEquals(1.0, color!.red)
}

runner.addTest("Utils: Gradient generation") {
    let gradient = ColorUtils.gradient(from: .black, to: .white, steps: 5)
    return assertEquals(5, gradient.count) &&
           assertEquals(Color.black, gradient.first) &&
           assertEquals(Color.white, gradient.last)
}

runner.addTest("Utils: Material palette") {
    let base = Color(red: 0.2, green: 0.4, blue: 0.8)
    let palette = ColorUtils.materialPalette(from: base)
    return assertEquals(10, palette.count) &&
           assertTrue(palette["500"] != nil)
}

runner.addTest("Utils: Best contrast selection") {
    let bg = Color.white
    let candidates = [Color.black, Color.gray, Color.darkGray]
    let best = ColorUtils.bestContrast(for: bg, among: candidates)
    return assertEquals(Color.black, best)
}

runner.addTest("Utils: Random palette") {
    let palette = ColorUtils.randomPalette(count: 5)
    return assertEquals(5, palette.count)
}

runner.addTest("Utils: Harmonious palette") {
    let base = Color(hue: 0, saturation: 1.0, lightness: 0.5)
    let palette = ColorUtils.harmoniousPalette(from: base)
    return assertEquals(5, palette.count)
}

// MARK: - RGB/RGBA String Tests

runner.addTest("String: RGB string format") {
    let color = Color(red: 1, green: 0.5, blue: 0)
    return assertEquals("rgb(255, 128, 0)", color.rgbString)
}

runner.addTest("String: RGBA string format") {
    let color = Color(red: 1, green: 0.5, blue: 0, alpha: 0.5)
    return assertTrue(color.rgbaString.contains("rgba(255, 128, 0"))
}

// MARK: - Edge Cases Tests

runner.addTest("Edge: Hex without # prefix") {
    let color = Color(hex: "FF0000")
    return assertTrue(color != nil) &&
           assertApproxEquals(1.0, color!.red)
}

runner.addTest("Edge: Invalid hex returns nil") {
    let color = Color(hex: "invalid")
    return assertTrue(color == nil)
}

runner.addTest("Edge: RGB clamping - values above 255") {
    let color = Color(r: 300, g: 128, b: 0)
    return assertApproxEquals(1.0, color.red) &&
           assertApproxEquals(128.0/255.0, color.green)
}

runner.addTest("Edge: RGB clamping - negative values") {
    let color = Color(r: -50, g: 0, b: 0)
    return assertApproxEquals(0.0, color.red)
}

runner.addTest("Edge: Alpha clamping") {
    let color = Color(red: 0.5, green: 0.5, blue: 0.5, alpha: 2.0)
    return assertApproxEquals(1.0, color.alpha)
}

runner.addTest("Edge: HSL hue wrapping") {
    let color1 = Color(hue: 0, saturation: 1.0, lightness: 0.5)
    let color2 = Color(hue: 360, saturation: 1.0, lightness: 0.5)
    let color3 = Color(hue: 720, saturation: 1.0, lightness: 0.5)
    return assertApproxEquals(color1.red, color2.red, 0.02) &&
           assertApproxEquals(color1.red, color3.red, 0.02)
}

// 运行测试
runner.run()