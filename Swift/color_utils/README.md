# Swift Color Utilities

通用颜色工具模块，提供完整的颜色处理、转换和生成功能。

## 功能特性

### 颜色表示
- **Color 结构体**: RGBA 颜色表示
- **预定义颜色**: 常用颜色常量（black, white, red, green, blue 等）
- **HSL/HSV/CMYK**: 多种颜色空间表示

### 颜色转换
- **HEX 转换**: 十六进制字符串/整数 ↔ Color
  - 支持 3/4/6/8 位 HEX 格式
  - 支持 CSS HEX 格式 (#RGB, #RGBA, #RRGGBB, #RRGGBBAA)
- **RGB 转换**: RGB 整数/字符串 ↔ Color
- **HSL 转换**: HSL ↔ Color
- **HSV/HSB 转换**: HSV ↔ Color
- **CMYK 换**: CMYK ↔ Color
- **CSS 颜色名称**: 140+ CSS 标准颜色名称支持

### 颜色操作
- **亮度调整**: `lighten()`, `darken()`, `adjustBrightness()`
- **饱和度调整**: `saturate()`, `desaturate()`, `adjustSaturation()`
- **灰度化**: `grayscale()`
- **反转**: `inverted()`
- **透明度**: `withAlpha()`

### 颜色混合
- **混合**: `mix(with: ratio:)`
- **Tint/Shade**: 与白色/黑色混合
- **加权混合**: `weightedMix()`
- **平均颜色**: `average()`

### 对比度计算（WCAG 标准）
- **相对亮度**: `relativeLuminance`
- **对比度**: `contrastRatio(with:)`
- **WCAG 检查**: AA/AAA 级别对比度验证
- **文字颜色推荐**: `textColor` 自动选择适合的文字颜色

### 调色板生成
- **类似色**: `analogousPalette()`
- **互补色**: `complementaryPalette()`
- **三色**: `triadicPalette()`
- **分裂互补色**: `splitComplementaryPalette()`
- **四色**: `tetradicPalette()`
- **单色**: `monochromaticPalette()`
- **Material Design**: `materialPalette()`
- **和谐调色板**: `harmoniousPalette()`

### 颜色生成
- **随机颜色**: `random()`
- **种子颜色**: `fromSeed()` - 从字符串生成一致的颜色
- **渐变**: `gradient(from: to: steps:)`

## 使用示例

### 创建颜色

```swift
// RGB 创建
let color1 = Color(red: 1.0, green: 0.5, blue: 0.0)
let color2 = Color(r: 255, g: 128, b: 0)  // 整数形式

// HEX 创建
let color3 = Color(hex: "#FF8000")
let color4 = Color(hex: 0xFF8000)  // 整数形式

// HSL 创建
let color5 = Color(hue: 30, saturation: 1.0, lightness: 0.5)

// HSV 创建
let color6 = Color(hue: 30, saturation: 1.0, value: 1.0)

// CMYK 创建
let color7 = Color(cyan: 0, magenta: 1.0, yellow: 1.0, key: 0)

// CSS 颜色名称
let color8 = Color(cssName: "coral")

// 预定义颜色
let color9 = Color.red
let color10 = Color.orange
```

### 颜色转换

```swift
let color = Color.red

// 转换为 HEX
print(color.toHex())               // "#FF0000"
print(color.toHex(includeAlpha: true)) // "#FF0000FF"
print(color.toHexInt())            // 0xFF0000

// 转换为 HSL
let hsl = color.hsl
print("H: \(hsl.hue), S: \(hsl.saturation), L: \(hsl.lightness)")

// 转换为 HSV
let hsv = color.hsv
print("H: \(hsv.hue), S: \(hsv.saturation), V: \(hsv.value)")

// 转换为 CMYK
let cmyk = color.cmyk
print("C: \(cmyk.cyan), M: \(cmyk.magenta), Y: \(cmyk.yellow), K: \(cmyk.key)")

// RGB 字符串
print(color.rgbString)   // "rgb(255, 0, 0)"
print(color.rgbaString)  // "rgba(255, 0, 0, 1.0)"
```

### 颜色操作

```swift
let base = Color(red: 0.5, green: 0.5, blue: 0.5)

// 亮度调整
let lighter = base.lighten(0.2)   // 变亮 20%
let darker = base.darken(0.2)     // 变暗 20%

// 饱和度调整
let saturated = base.saturate(0.3)    // 增加饱和度
let desaturated = base.desaturate(0.3) // 降低饱和度

// 灰度化
let gray = Color.red.grayscale()

// 反转
let inverted = Color.blue.inverted()  // 变成黄色

// 透明度
let transparent = Color.red.withAlpha(0.5)
```

### 颜色混合

```swift
let red = Color.red
let blue = Color.blue

// 均等混合
let purple = red.mix(with: blue, ratio: 0.5)

// 与白色混合 (变亮)
let pink = Color.red.tint(0.5)

// 与黑色混合 (变暗)
let darkRed = Color.red.shade(0.3)

// 加权混合多个颜色
let avg = Color.weightedMix([
    (Color.red, 1.0),
    (Color.green, 2.0),
    (Color.blue, 1.0)
])
```

### 对比度计算

```swift
let black = Color.black
let white = Color.white

// 对比度
let ratio = black.contrastRatio(with: white)  // ~21.0

// WCAG 验证
print(black.passesWCAGAA(with: white))  // true (>= 4.5)
print(black.passesWCAGAAA(with: white)) // true (>= 7.0)

// 自动选择文字颜色
let background = Color(red: 0.2, green: 0.2, blue: 0.2)
let textColor = background.textColor  // 白色（因为背景是暗色）

// 判断明暗
print(Color.white.isLight)  // true
print(Color.black.isDark)   // true
```

### 调色板生成

```swift
let base = Color(hue: 0, saturation: 1.0, lightness: 0.5)

// 类似色调色板
let analogous = base.analogousPalette(count: 5)

// 互补色
let complementary = base.complementaryPalette()

// 三色
let triadic = base.triadicPalette()

// 分裂互补色
let split = base.splitComplementaryPalette()

// 四色
let tetradic = base.tetradicPalette()

// 单色调色板
let mono = base.monochromaticPalette(steps: 5)

// Material Design 调色板
let material = ColorUtils.materialPalette(from: Color(cssName: "blue")!)
print(material["500"])  // 基础颜色
print(material["100"])  // 浅色变体
print(material["900"])  // 深色变体
```

### 随机和种子颜色

```swift
// 随机颜色
let random1 = Color.random()
let random2 = Color.random(opaque: false)  // 包含随机透明度

// 从种子生成（相同种子生成相同颜色）
let avatar1 = Color.fromSeed("user123")
let avatar2 = Color.fromSeed("user123")  // 与 avatar1 相同

// 随机调色板
let palette = ColorUtils.randomPalette(count: 5)
```

### 颜色解析

```swift
// 支持多种格式
let parsed1 = ColorUtils.parse("#FF0000")      // HEX
let parsed2 = ColorUtils.parse("rgb(255,0,0)") // RGB
let parsed3 = ColorUtils.parse("rgba(255,0,0,0.5)") // RGBA
let parsed4 = ColorUtils.parse("hsl(0,100%,50%)") // HSL
let parsed5 = ColorUtils.parse("red")          // CSS 名称
```

### 渐变生成

```swift
// 创建渐变
let gradient = ColorUtils.gradient(
    from: Color.red,
    to: Color.blue,
    steps: 10
)

// 遍历渐变颜色
for (index, color) in gradient.enumerated() {
    print("Step \(index): \(color.toHex())")
}
```

## API 参考

### Color 结构体

| 属性 | 类型 | 描述 |
|------|------|------|
| `red` | Double | 红色分量 (0-1) |
| `green` | Double | 绿色分量 (0-1) |
| `blue` | Double | 蓝色分量 (0-1) |
| `alpha` | Double | 透明度 (0-1) |

### 初始化方法

| 方法 | 描述 |
|------|------|
| `init(red:, green:, blue:, alpha:)` | 从 RGB 值创建 |
| `init(r:, g:, b:, a:)` | 从 RGB 整数创建 |
| `init?(hex:)` | 从 HEX 字符串创建 |
| `init(hex:, alpha:)` | 从 HEX 整数创建 |
| `init(hsl:)` | 从 HSL 创建 |
| `init(hue:, saturation:, lightness:, alpha:)` | 从 HSL 值创建 |
| `init(hsv:)` | 从 HSV 创建 |
| `init(hue:, saturation:, value:, alpha:)` | 从 HSV 值创建 |
| `init(cmyk:)` | 从 CMYK 创建 |
| `init(cyan:, magenta:, yellow:, key:, alpha:)` | 从 CMYK 值创建 |
| `init?(cssName:)` | 从 CSS 颜色名称创建 |
| `static func random()` | 生成随机颜色 |
| `static func fromSeed()` | 从种子生成颜色 |

### 转换方法

| 方法 | 描述 |
|------|------|
| `toHex()` | 转换为 HEX 字符串 |
| `toHexInt()` | 转换为 HEX 整数 |
| `hsl` | 获取 HSL 表示 |
| `hsv` | 获取 HSV 表示 |
| `cmyk` | 获取 CMYK 表示 |
| `rgbInt` | 获取 RGB 整数 |
| `rgbString` | RGB 字符串表示 |
| `rgbaString` | RGBA 字符串表示 |
| `cssName` | CSS 颜色名称（如果存在） |

### 操作方法

| 方法 | 描述 |
|------|------|
| `lighten()` | 变亮 |
| `darken()` | 变暗 |
| `adjustBrightness()` | 调整亮度 |
| `saturate()` | 增加饱和度 |
| `desaturate()` | 降低饱和度 |
| `adjustSaturation()` | 调整饱和度 |
| `grayscale()` | 灰度化 |
| `inverted()` | 反转颜色 |
| `withAlpha()` | 设置透明度 |

### 混合方法

| 方法 | 描述 |
|------|------|
| `mix(with:, ratio:)` | 与另一个颜色混合 |
| `tint()` | 与白色混合 |
| `shade()` | 与黑色混合 |
| `static func weightedMix()` | 加权混合 |
| `static func average()` | 平均混合 |

### 对比度方法

| 方法 | 描述 |
|------|------|
| `relativeLuminance` | 相对亮度（WCAG） |
| `contrastRatio(with:)` | 对比度 |
| `isLight` | 是否为亮色 |
| `isDark` | 是否为暗色 |
| `textColor` | 适合的文字颜色 |
| `passesWCAGAA(with:)` | WCAG AA 验证 |
| `passesWCAGAALarge(with:)` | WCAG AA 大文本验证 |
| `passesWCAGAAA(with:)` | WCAG AAA 验证 |

### 调色板方法

| 方法 | 描述 |
|------|------|
| `analogousPalette()` | 类似色调色板 |
| `complementaryPalette()` | 互补色调色板 |
| `triadicPalette()` | 三色调色板 |
| `splitComplementaryPalette()` | 分裂互补色调色板 |
| `tetradicPalette()` | 四色调色板 |
| `monochromaticPalette()` | 单色调色板 |

### ColorUtils 工具类

| 方法 | 描述 |
|------|------|
| `parse()` | 解析颜色字符串 |
| `gradient(from:, to:, steps:)` | 生成渐变 |
| `palette(hue:, count:)` | 生成色调调色板 |
| `materialPalette(from:)` | Material Design 调色板 |
| `randomPalette()` | 随机调色板 |
| `harmoniousPalette(from:)` | 和谐调色板 |
| `bestContrast()` | 选择最佳对比颜色 |
| `passesWCAGAA()` | WCAG AA 检查 |
| `passesWCAGAAA()` | WCAG AAA 检查 |

## 平台兼容性

- iOS 13.0+
- macOS 10.15+
- watchOS 6.0+
- tvOS 13.0+

## 零依赖

本模块仅使用 Swift 标准库，无任何第三方依赖。

## 测试

运行测试：

```bash
swift ColorUtilsTest.swift
```

## 作者

AllToolkit

## 版本

1.0.0