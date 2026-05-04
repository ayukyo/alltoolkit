# Color Utils

一个零外部依赖的 Go 语言颜色转换和处理工具库。

## 功能特性

### 颜色格式转换
- **RGB ↔ Hex**: RGB 与十六进制字符串互转
- **RGB ↔ HSL**: RGB 与 HSL（色相、饱和度、亮度）互转
- **RGB ↔ HSV**: RGB 与 HSV（色相、饱和度、明度）互转
- **RGB ↔ CMYK**: RGB 与 CMYK（青、品红、黄、黑）互转

### 颜色操作
- `Complementary(rgb)` - 获取互补色
- `Lighten(rgb, percent)` - 变亮
- `Darken(rgb, percent)` - 变暗
- `Saturate(rgb, percent)` - 增加饱和度
- `Desaturate(rgb, percent)` - 降低饱和度
- `Mix(c1, c2, weight)` - 混合两种颜色
- `Grayscale(rgb)` - 转灰度
- `Invert(rgb)` - 反转颜色

### 颜色分析
- `IsLight(rgb)` - 判断是否为浅色
- `IsDark(rgb)` - 判断是否为深色
- `Luminance(rgb)` - 计算相对亮度（WCAG）
- `ContrastRatio(c1, c2)` - 计算对比度比率（WCAG）

### 命名颜色
- 内置 140+ CSS 颜色名称
- `NameToRGB(name)` - 颜色名转 RGB
- `RGBToName(rgb)` - 查找最接近的颜色名
- `SearchColorsByName(query)` - 按名称搜索颜色

### 调色板生成
- `GenerateScheme(base, scheme)` - 生成配色方案
  - `Mono` - 单色
  - `Complementary_` - 互补色
  - `Analogous` - 类似色
  - `Triadic` - 三色组
  - `SplitComp` - 分裂互补
  - `Tetradic` - 四色组
- `Gradient(start, end, steps)` - 生成渐变色
- `Shades(rgb, count)` - 生成明暗变化
- `Tints(rgb, count)` - 生成色彩（与白色混合）
- `Tones(rgb, count)` - 生成色调（与灰色混合）
- `Warm(count)` - 暖色系调色板
- `Cool(count)` - 冷色系调色板

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/color_utils
```

## 使用示例

```go
package main

import (
    "fmt"
    color "github.com/ayukyo/alltoolkit/Go/color_utils"
)

func main() {
    // RGB <-> Hex
    rgb := color.NewRGB(255, 128, 64)
    hex := color.RGBToHex(rgb)  // "#ff8040"

    // RGB <-> HSL
    hsl := color.RGBToHSL(rgb)
    backToRGB := color.HSLToRGB(hsl)

    // 命名颜色
    coral, _ := color.NameToRGB("coral")  // RGB{255, 127, 80}
    name := color.RGBToName(rgb)           // 查找最接近的颜色名

    // 颜色操作
    complementary := color.Complementary(rgb)
    lighter := color.Lighten(rgb, 20)
    gray := color.Grayscale(rgb)
    mixed := color.Mix(color.NewRGB(255,0,0), color.NewRGB(0,0,255), 0.5)

    // 对比度检查
    bgColor := color.NewRGB(50, 50, 100)
    textColor := color.NewRGB(255, 255, 255)
    ratio := color.ContrastRatio(bgColor, textColor)  // WCAG 对比度

    // 配色方案
    triadic := color.GenerateScheme(rgb, color.Triadic)  // 三色组

    // 渐变
    gradient := color.Gradient(
        color.NewRGB(255, 0, 0),
        color.NewRGB(0, 0, 255),
        5,
    )
}
```

## API 参考

### 类型

```go
type RGB struct {
    R uint8  // 红 (0-255)
    G uint8  // 绿 (0-255)
    B uint8  // 蓝 (0-255)
}

type HSL struct {
    H float64  // 色相 (0-360)
    S float64  // 饱和度 (0-100)
    L float64  // 亮度 (0-100)
}

type HSV struct {
    H float64  // 色相 (0-360)
    S float64  // 饱和度 (0-100)
    V float64  // 明度 (0-100)
}

type CMYK struct {
    C float64  // 青 (0-100)
    M float64  // 品红 (0-100)
    Y float64  // 黄 (0-100)
    K float64  // 黑 (0-100)
}
```

### 构造函数

```go
func NewRGB(r, g, b uint8) RGB
func NewHSL(h, s, l float64) HSL
func NewHSV(h, s, v float64) HSV
func NewCMYK(c, m, y, k float64) CMYK
```

### 转换函数

```go
func RGBToHex(rgb RGB) string
func HexToRGB(hex string) (RGB, error)
func RGBToHSL(rgb RGB) HSL
func HSLToRGB(hsl HSL) RGB
func RGBToHSV(rgb RGB) HSV
func HSVToRGB(hsv HSV) RGB
func RGBToCMYK(rgb RGB) CMYK
func CMYKToRGB(cmyk CMYK) RGB
```

## 测试

```bash
cd Go/color_utils
go test -v
```

## 性能

```bash
go test -bench=.
```

## 许可证

MIT License