# Color Utilities - Lua 颜色工具模块

完整的颜色处理工具集，零外部依赖，仅使用 Lua 标准库。

## 功能特性

### 格式转换
- RGB → HEX, HSL, HSV, CMYK
- HEX → RGB, HSL, HSV
- HSL → RGB, HEX, HSV
- HSV → RGB, HEX, HSL
- CMYK → RGB
- 智能解析多种格式字符串

### 颜色操作
- 混合颜色 (任意权重)
- 渐变生成 (多颜色平滑过渡)
- 调整亮度、饱和度、色相
- 变亮/变暗
- 饱和/去饱和
- 灰度化、反转

### 配色方案
- 互补色 (Complementary)
- 类似色 (Analogous)
- 三色组 (Triadic)
- 分裂互补色 (Split-complementary)
- 四色组 (Tetradic)
- 方形配色 (Square)
- 单色方案 (Monochromatic)

### 对比度计算
- WCAG 相对亮度计算
- 对比度比例计算
- WCAG 合规性检查 (AA/AAA)

### 随机颜色
- 任意随机颜色
- 柔和色 (Pastel)
- 暗色
- 鲜艳色 (Vibrant)
- 基于种子生成 (确定性)

### 实用工具
- 命名颜色识别 (140+ CSS 颜色名称)
- 最近颜色名称查找
- 颜色差异计算
- 明暗判断
- 对比色推荐 (黑/白)
- 温度判断 (暖色/冷色/中性)
- 和谐度评分

## 快速开始

```lua
local ColorUtils = require("color_utils")

-- 创建颜色 (多种方式)
local color1 = ColorUtils.fromRgb(255, 87, 51)
local color2 = ColorUtils.fromHex("#FF5733")
local color3 = ColorUtils.fromHsl(11, 100, 60)
local color4 = ColorUtils.fromName("coral")

-- 智能解析
local color = ColorUtils.parse("#FF5733")
local color = ColorUtils.parse("rgb(255, 87, 51)")
local color = ColorUtils.parse("coral")

-- 格式转换
print(color:toHex())           -- #FF5733
print(color:toRgbString())     -- rgb(255, 87, 51)
print(color:toHsl())           -- {h=11, s=100, l=60}

-- 配色方案
local comp = color:complementary()
local triad = color:triadic()
local scheme = ColorUtils.triadicScheme(color)

-- 渐变生成
local gradient = ColorUtils.gradient({"#FF0000", "#00FF00", "#0000FF"}, 10)

-- 对比度检查
local wcag = color:wcagCompliance(otherColor)
print(wcag.aaNormal)    -- true/false
```

## 测试

```bash
cd color_utils
lua color_utils_test.lua
```

## 依赖

- 无外部依赖
- 仅使用 Lua 标准库
- 兼容 Lua 5.1+

## License

MIT