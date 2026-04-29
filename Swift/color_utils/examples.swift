/**
 * AllToolkit - Swift Color Utilities Examples
 *
 * 展示颜色工具模块的各种使用场景
 */

import Foundation

// MARK: - 示例 1: 基础颜色创建

print("=" + String(repeating: "=", count: 59) + "=")
print("示例 1: 基础颜色创建")
print("=" + String(repeating: "=", count: 59) + "=")
print()

// RGB 创建
let orange = Color(red: 1, green: 0.5, blue: 0)
print("RGB 创建 (1, 0.5, 0): \(orange.toHex())")

// RGB 整数创建
let purple = Color(r: 128, g: 0, b: 128)
print("RGB Int 创建 (128, 0, 128): \(purple.toHex())")

// HEX 创建
let fromHex = Color(hex: "#00FF00")
print("HEX 创建 (#00FF00): \(fromHex?.toHex() ?? "nil")")

// HSL 创建
let hslColor = Color(hue: 240, saturation: 1.0, lightness: 0.5)
print("HSL 创建 (240°, 100%, 50%): \(hslColor.toHex())")

// CSS 名称创建
let coral = Color(cssName: "coral")
print("CSS 名称创建 (coral): \(coral?.toHex() ?? "nil")")

// 预定义颜色
print("预定义颜色: red=\(Color.red.toHex()), blue=\(Color.blue.toHex())")
print()

// MARK: - 示例 2: 颜色转换

print("=" + String(repeating: "=", count: 59) + "=")
print("示例 2: 颜色转换")
print("=" + String(repeating: "=", count: 59) + "=")
print()

let red = Color.red

print("红色 (#FF0000) 的各种表示:")
print("  RGB: \(red.rgbString)")
print("  RGBA: \(red.rgbaString)")
print("  HEX: \(red.toHex())")
print("  HEX (带 Alpha): \(red.toHex(includeAlpha: true))")

let hsl = red.hsl
print("  HSL: H=\(hsl.hue)°, S=\(hsl.saturation * 100)%, L=\(hsl.lightness * 100)%")

let hsv = red.hsv
print("  HSV: H=\(hsv.hue)°, S=\(hsv.saturation * 100)%, V=\(hsv.value * 100)%")

let cmyk = red.cmyk
print("  CMYK: C=\(cmyk.cyan * 100)%, M=\(cmyk.magenta * 100)%, Y=\(cmyk.yellow * 100)%, K=\(cmyk.key * 100)%")
print()

// MARK: - 示例 3: 颜色操作

print("=" + String(repeating: "=", count: 59) + "=")
print("示例 3: 颜色操作")
print("=" + String(repeating: "=", count: 59) + "=")
print()

let baseGray = Color(red: 0.5, green: 0.5, blue: 0.5)
print("基础颜色: \(baseGray.toHex()) (50% 灰色)")
print("变亮 20%: \(baseGray.lighten(0.2).toHex())")
print("变暗 20%: \(baseGray.darken(0.2).toHex())")

let saturatedColor = Color(hue: 0, saturation: 0.5, lightness: 0.5)
print("\n低饱和度红色: \(saturatedColor.toHex())")
print("增加饱和度 40%: \(saturatedColor.saturate(0.4).toHex())")
print("降低饱和度 30%: \(saturatedColor.desaturate(0.3).toHex())")
print("灰度化: \(saturatedColor.grayscale().toHex())")

let blueColor = Color.blue
print("\n蓝色: \(blueColor.toHex())")
print("反转: \(blueColor.inverted().toHex())")
print("半透明: \(blueColor.withAlpha(0.5).rgbaString)")
print()

// MARK: - 示例 4: 颜色混合

print("=" + String(repeating: "=", count: 59) + "=")
print("示例 4: 颜色混合")
print("=" + String(repeating: "=", count: 59) + "=")
print()

let colorRed = Color.red
let colorBlue = Color.blue

print("红色: \(colorRed.toHex())")
print("蓝色: \(colorBlue.toHex())")
print("混合 (50:50): \(colorRed.mix(with: colorBlue, ratio: 0.5).toHex())")
print("混合 (25:75): \(colorRed.mix(with: colorBlue, ratio: 0.75).toHex())")

print("\n红色 + 白色 (tint):")
for ratio in [0.25, 0.5, 0.75] {
    print("  tint \(ratio * 100)%: \(colorRed.tint(ratio).toHex())")
}

print("\n红色 + 黑色 (shade):")
for ratio in [0.25, 0.5, 0.75] {
    print("  shade \(ratio * 100)%: \(colorRed.shade(ratio).toHex())")
}

// 加权混合
let weightedMix = Color.weightedMix([
    (Color.red, 1.0),
    (Color.green, 2.0),
    (Color.blue, 1.0)
])
print("\n加权混合 (R:1, G:2, B:1): \(weightedMix?.toHex() ?? "nil")")
print()

// MARK: - 示例 5: 对比度计算

print("=" + String(repeating: "=", count: 59) + "=")
print("示例 5: 对比度计算 (WCAG)")
print("=" + String(repeating: "=", count: 59) + "=")
print()

let black = Color.black
let white = Color.white
let midGray = Color.gray

print("黑 vs 白 对比度: \(black.contrastRatio(with: white))")
print("黑 vs 灰 对比度: \(black.contrastRatio(with: midGray))")
print("白 vs 灰 对比度: \(white.contrastRatio(with: midGray))")

print("\nWCAG AA 检查 (>= 4.5):")
print("  黑/白: \(black.passesWCAGAA(with: white) ? "PASS ✓" : "FAIL ✗")")
print("  黑/灰: \(black.passesWCAGAA(with: midGray) ? "PASS ✓" : "FAIL ✗")")

print("\nWCAG AAA 检查 (>= 7.0):")
print("  黑/白: \(black.passesWCAGAAA(with: white) ? "PASS ✓" : "FAIL ✗")")

// 自动选择文字颜色
let darkBg = Color(red: 0.2, green: 0.2, blue: 0.2)
let lightBg = Color(red: 0.9, green: 0.9, blue: 0.9)
print("\n暗色背景推荐文字颜色: \(darkBg.textColor.toHex())")
print("亮色背景推荐文字颜色: \(lightBg.textColor.toHex())")
print()

// MARK: - 示例 6: 调色板生成

print("=" + String(repeating: "=", count: 59) + "=")
print("示例 6: 调色板生成")
print("=" + String(repeating: "=", count: 59) + "=")
print()

let baseRed = Color(hue: 0, saturation: 1.0, lightness: 0.5)

print("类似色调色板 (基于红色):")
for color in baseRed.analogousPalette(count: 5) {
    print("  \(color.toHex()) - H: \(color.hsl.hue)°")
}

print("\n互补色调色板:")
for color in baseRed.complementaryPalette() {
    print("  \(color.toHex()) - H: \(color.hsl.hue)°")
}

print("\n三色调色板:")
for color in baseRed.triadicPalette() {
    print("  \(color.toHex()) - H: \(color.hsl.hue)°")
}

print("\n单色调色板 (红色系):")
for (i, color) in baseRed.monochromaticPalette(steps: 5).enumerated() {
    print("  Level \(i + 1): \(color.toHex()) - L: \(color.hsl.lightness * 100)%")
}

// Material Design 调色板
let blueBase = Color(cssName: "blue")!
let materialPalette = ColorUtils.materialPalette(from: blueBase)
print("\nMaterial Design 调色板 (基于蓝色):")
for (level, color) in materialPalette.sorted(by: { $0.key < $1.key }) {
    print("  \(level): \(color.toHex())")
}
print()

// MARK: - 示例 7: 随机和种子颜色

print("=" + String(repeating: "=", count: 59) + "=")
print("示例 7: 随机和种子颜色")
print("=" + String(repeating: "=", count: 59) + "=")
print()

print("随机颜色:")
for _ in 0..<5 {
    print("  \(Color.random().toHex())")
}

print("\n种子颜色 (相同种子生成相同颜色):")
let seed1 = Color.fromSeed("user-alice")
let seed2 = Color.fromSeed("user-alice")
let seed3 = Color.fromSeed("user-bob")
print("  user-alice: \(seed1.toHex())")
print("  user-alice (再次): \(seed2.toHex())")
print("  user-bob: \(seed3.toHex())")

print("\n随机调色板:")
for color in ColorUtils.randomPalette(count: 5) {
    print("  \(color.toHex())")
}
print()

// MARK: - 示例 8: 颜色解析

print("=" + String(repeating: "=", count: 59) + "=")
print("示例 8: 颜色解析 (多格式支持)")
print("=" + String(repeating: "=", count: 59) + "=")
print()

let formats = [
    "#FF0000",
    "rgb(255, 0, 0)",
    "rgba(255, 0, 0, 0.5)",
    "hsl(0, 100%, 50%)",
    "red",
    "coral",
    "#F00",
    "#FF0000FF"
]

for format in formats {
    let parsed = ColorUtils.parse(format)
    let hex = parsed?.toHex(includeAlpha: true) ?? "解析失败"
    print("  \"\(format)\" → \(hex)")
}
print()

// MARK: - 示例 9: 渐变生成

print("=" + String(repeating: "=", count: 59) + "=")
print("示例 9: 渐变生成")
print("=" + String(repeating: "=", count: 59) + "=")
print()

let gradient = ColorUtils.gradient(from: Color.red, to: Color.blue, steps: 10)
print("从红色到蓝色的 10 步渐变:")
for (i, color) in gradient.enumerated() {
    print("  Step \(i): \(color.toHex())")
}

print("\n从黑色到白色的 5 步渐变:")
let bwGradient = ColorUtils.gradient(from: Color.black, to: Color.white, steps: 5)
for (i, color) in bwGradient.enumerated() {
    print("  Step \(i): \(color.toHex())")
}
print()

// MARK: - 示例 10: 和谐调色板

print("=" + String(repeating: "=", count: 59) + "=")
print("示例 10: 和谐调色板")
print("=" + String(repeating: "=", count: 59) + "=")
print()

let harmoniousBase = Color(hue: 200, saturation: 0.7, lightness: 0.5)
print("和谐调色板 (基于青色):")
for (i, color) in ColorUtils.harmoniousPalette(from: harmoniousBase).enumerated() {
    print("  Color \(i + 1): \(color.toHex()) - H: \(color.hsl.hue)°, S: \(color.hsl.saturation * 100)%")
}
print()

print("=" + String(repeating: "=", count: 59) + "=")
print("所有示例运行完成!")
print("=" + String(repeating: "=", count: 59) + "=")