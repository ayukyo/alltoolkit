--[[
Color Utilities - 颜色工具模块

提供完整的颜色处理功能，包括：
- 多种格式转换 (RGB, HEX, HSL, HSV, CMYK)
- 颜色混合与渐变
- 对比度计算 (WCAG 标准)
- 互补色、类似色、三色组等配色方案
- 亮度调节
- 随机颜色生成
- 颜色名称识别

零依赖，仅使用 Lua 标准库。

Author: AllToolkit
Version: 1.0.0
License: MIT
]]

local ColorUtils = {}

-- ============================================================================
-- 常量定义
-- ============================================================================

-- CSS 命名颜色表 (部分常用颜色)
ColorUtils.NAMED_COLORS = {
    black = {0, 0, 0},
    white = {255, 255, 255},
    red = {255, 0, 0},
    green = {0, 128, 0},
    blue = {0, 0, 255},
    yellow = {255, 255, 0},
    cyan = {0, 255, 255},
    magenta = {255, 0, 255},
    orange = {255, 165, 0},
    purple = {128, 0, 128},
    pink = {255, 192, 203},
    brown = {165, 42, 42},
    gray = {128, 128, 128},
    grey = {128, 128, 128},
    navy = {0, 0, 128},
    teal = {0, 128, 128},
    olive = {128, 128, 0},
    maroon = {128, 0, 0},
    aqua = {0, 255, 255},
    fuchsia = {255, 0, 255},
    lime = {0, 255, 0},
    silver = {192, 192, 192},
    coral = {255, 127, 80},
    gold = {255, 215, 0},
    indigo = {75, 0, 130},
    violet = {238, 130, 238},
    turquoise = {64, 224, 208},
    salmon = {250, 128, 114},
    khaki = {240, 230, 140},
    crimson = {220, 20, 60},
    chocolate = {210, 105, 30},
    tan = {210, 180, 140},
    sienna = {160, 82, 45},
    tomato = {255, 99, 71},
    plum = {221, 160, 221},
    orchid = {218, 112, 214},
    peru = {205, 133, 63},
    lavender = {230, 230, 250},
    beige = {245, 245, 220},
    ivory = {255, 255, 240},
    mint = {189, 252, 201},
    peach = {255, 218, 185},
    skyblue = {135, 206, 235},
    steelblue = {70, 130, 180},
    royalblue = {65, 105, 225},
    midnightblue = {25, 25, 112},
    forestgreen = {34, 139, 34},
    seagreen = {46, 139, 87},
    springgreen = {0, 255, 127},
    firebrick = {178, 34, 34},
    darkred = {139, 0, 0},
    darkgreen = {0, 100, 0},
    darkblue = {0, 0, 139},
    lightgray = {211, 211, 211},
    lightgrey = {211, 211, 211},
    lightblue = {173, 216, 230},
    lightgreen = {144, 238, 144},
    lightyellow = {255, 255, 224},
    lightpink = {255, 182, 193},
    darkgray = {169, 169, 169},
    darkgrey = {169, 169, 169},
    dimgray = {105, 105, 105},
    dimgrey = {105, 105, 105},
    slategray = {112, 128, 144},
    slateblue = {106, 90, 205},
    powderblue = {176, 224, 230},
    cornflowerblue = {100, 149, 237},
    dodgerblue = {30, 144, 255},
    deepskyblue = {0, 191, 255},
    lightskyblue = {135, 206, 250},
    mediumblue = {0, 0, 205},
    mediumseagreen = {60, 179, 113},
    mediumspringgreen = {0, 250, 154},
    mediumturquoise = {72, 209, 204},
    mediumpurple = {147, 112, 219},
    mediumorchid = {186, 85, 211},
    mediumvioletred = {199, 21, 133},
    darkorange = {255, 140, 0},
    darkviolet = {148, 0, 211},
    darkmagenta = {139, 0, 139},
    darkcyan = {0, 139, 139},
    darksalmon = {233, 150, 122},
    darkkhaki = {189, 183, 107},
    darkgoldenrod = {184, 134, 11},
    lightsalmon = {255, 160, 122},
    lightcoral = {240, 128, 128},
    lightseagreen = {32, 178, 170},
    lemonchiffon = {255, 250, 205},
    papayawhip = {255, 239, 213},
    blanchedalmond = {255, 235, 205},
    antiquewhite = {250, 235, 215},
    mistyrose = {255, 228, 225},
    lavenderblush = {255, 240, 245},
    seashell = {255, 245, 238},
    floralwhite = {255, 250, 240},
    snow = {255, 250, 250},
    honeydew = {240, 255, 240},
    mintcream = {245, 255, 250},
    azure = {240, 255, 255},
    aliceblue = {240, 248, 255},
    ghostwhite = {248, 248, 255},
    whitesmoke = {245, 245, 245},
    gainsboro = {220, 220, 220},
    lightsteelblue = {176, 196, 222},
    palegoldenrod = {238, 232, 170},
    palegreen = {152, 251, 152},
    paleturquoise = {175, 238, 238},
    palevioletred = {219, 112, 147},
    peachpuff = {255, 218, 185},
    navajowhite = {255, 222, 173},
    moccasin = {255, 228, 181},
    bisque = {255, 228, 196},
    wheat = {245, 222, 179},
    burlywood = {222, 184, 135},
    rosybrown = {188, 143, 143},
    sandybrown = {244, 164, 96},
    goldenrod = {218, 165, 32},
    darkolivegreen = {85, 107, 47},
    darkseagreen = {143, 188, 143},
    yellowgreen = {154, 205, 50},
    olivedrab = {107, 142, 35},
    lawngreen = {124, 252, 0},
    chartreuse = {127, 255, 0},
    greenyellow = {173, 255, 47},
    hotpink = {255, 105, 180},
    deeppink = {255, 20, 147},
    indianred = {205, 92, 92},
    orangered = {255, 69, 0},
    darkturquoise = {0, 206, 209},
    cadetblue = {95, 158, 160},
    lightcyan = {224, 255, 255},
    darkslategray = {47, 79, 79},
    darkslategrey = {47, 79, 79},
    rebeccapurple = {102, 51, 153},
}

-- ============================================================================
-- 辅助函数
-- ============================================================================

-- 限制数值在指定范围内
local function clamp(value, min, max)
    return math.max(min, math.min(max, value))
end

-- 四舍五入
local function round(value)
    return math.floor(value + 0.5)
end

-- 检查是否为有效的 RGB 值
local function isValidRGB(r, g, b)
    return type(r) == "number" and type(g) == "number" and type(b) == "number"
        and r >= 0 and r <= 255 and g >= 0 and g <= 255 and b >= 0 and b <= 255
end

-- 检查是否为有效的 alpha 值
local function isValidAlpha(a)
    return type(a) == "number" and a >= 0 and a <= 1
end

-- ============================================================================
-- RGB 颜色对象
-- ============================================================================

local Color = {}
Color.__index = Color

-- 创建新的颜色对象
function Color.new(r, g, b, a)
    local self = setmetatable({}, Color)
    self.r = clamp(round(r or 0), 0, 255)
    self.g = clamp(round(g or 0), 0, 255)
    self.b = clamp(round(b or 0), 0, 255)
    self.a = clamp(a or 1, 0, 1)
    return self
end

-- 转换为 HEX 格式
function Color:toHex(includeAlpha)
    local hex = string.format("#%02X%02X%02X", self.r, self.g, self.b)
    if includeAlpha then
        hex = hex .. string.format("%02X", round(self.a * 255))
    end
    return hex
end

-- 转换为 RGB 字符串
function Color:toRgbString()
    if self.a < 1 then
        return string.format("rgba(%d, %d, %d, %.2f)", self.r, self.g, self.b, self.a)
    end
    return string.format("rgb(%d, %d, %d)", self.r, self.g, self.b)
end

-- 转换为 HSL
function Color:toHsl()
    local r, g, b = self.r / 255, self.g / 255, self.b / 255
    local max, min = math.max(r, g, b), math.min(r, g, b)
    local h, s, l = 0, 0, (max + min) / 2
    
    if max ~= min then
        local d = max - min
        s = l > 0.5 and d / (2 - max - min) or d / (max + min)
        
        if max == r then
            h = (g - b) / d + (g < b and 6 or 0)
        elseif max == g then
            h = (b - r) / d + 2
        else
            h = (r - g) / d + 4
        end
        h = h / 6
    end
    
    return {h = round(h * 360), s = round(s * 100), l = round(l * 100), a = self.a}
end

-- 转换为 HSV
function Color:toHsv()
    local r, g, b = self.r / 255, self.g / 255, self.b / 255
    local max, min = math.max(r, g, b), math.min(r, g, b)
    local h, s, v = 0, 0, max
    
    if max ~= 0 then
        s = (max - min) / max
    end
    
    if max ~= min then
        local d = max - min
        if max == r then
            h = (g - b) / d + (g < b and 6 or 0)
        elseif max == g then
            h = (b - r) / d + 2
        else
            h = (r - g) / d + 4
        end
        h = h / 6
    end
    
    return {h = round(h * 360), s = round(s * 100), v = round(v * 100), a = self.a}
end

-- 转换为 CMYK
function Color:toCmyk()
    local r, g, b = self.r / 255, self.g / 255, self.b / 255
    local k = 1 - math.max(r, g, b)
    
    if k == 1 then
        return {c = 0, m = 0, y = 0, k = 100, a = self.a}
    end
    
    local c = (1 - r - k) / (1 - k)
    local m = (1 - g - k) / (1 - k)
    local y = (1 - b - k) / (1 - k)
    
    return {
        c = round(c * 100),
        m = round(m * 100),
        y = round(y * 100),
        k = round(k * 100),
        a = self.a
    }
end

-- 计算相对亮度 (WCAG)
function Color:relativeLuminance()
    local function srgb(c)
        return c <= 0.03928 and c / 12.92 or ((c + 0.055) / 1.055) ^ 2.4
    end
    local r, g, b = srgb(self.r / 255), srgb(self.g / 255), srgb(self.b / 255)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b
end

-- 计算与另一颜色的对比度 (WCAG)
function Color:contrastRatio(other)
    local l1 = self:relativeLuminance()
    local l2 = other:relativeLuminance()
    local lighter = math.max(l1, l2)
    local darker = math.min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)
end

-- 判断是否符合 WCAG 对比度标准
function Color:wcagCompliance(other)
    local ratio = self:contrastRatio(other)
    return {
        ratio = round(ratio * 100) / 100,
        aaNormal = ratio >= 4.5,
        aaLarge = ratio >= 3,
        aaaNormal = ratio >= 7,
        aaaLarge = ratio >= 4.5
    }
end

-- 获取互补色
function Color:complementary()
    return Color.new(255 - self.r, 255 - self.g, 255 - self.b, self.a)
end

-- 获取类似色 (相邻色)
function Color:analogous(angle)
    angle = angle or 30
    local hsl = self:toHsl()
    local colors = {}
    
    for _, offset in ipairs({-angle, angle}) do
        local newH = (hsl.h + offset) % 360
        if newH < 0 then newH = newH + 360 end
        local c = ColorUtils.fromHsl(newH, hsl.s, hsl.l, hsl.a)
        table.insert(colors, c)
    end
    
    return colors
end

-- 获取三色组 (Triadic)
function Color:triadic()
    local hsl = self:toHsl()
    return {
        ColorUtils.fromHsl((hsl.h + 120) % 360, hsl.s, hsl.l, hsl.a),
        ColorUtils.fromHsl((hsl.h + 240) % 360, hsl.s, hsl.l, hsl.a)
    }
end

-- 获取分裂互补色 (Split-complementary)
function Color:splitComplementary()
    local hsl = self:toHsl()
    return {
        ColorUtils.fromHsl((hsl.h + 150) % 360, hsl.s, hsl.l, hsl.a),
        ColorUtils.fromHsl((hsl.h + 210) % 360, hsl.s, hsl.l, hsl.a)
    }
end

-- 获取四色组 (Tetradic/Rectangle)
function Color:tetradic()
    local hsl = self:toHsl()
    return {
        ColorUtils.fromHsl((hsl.h + 90) % 360, hsl.s, hsl.l, hsl.a),
        ColorUtils.fromHsl((hsl.h + 180) % 360, hsl.s, hsl.l, hsl.a),
        ColorUtils.fromHsl((hsl.h + 270) % 360, hsl.s, hsl.l, hsl.a)
    }
end

-- 获取方形配色 (Square)
function Color:square()
    local hsl = self:toHsl()
    return {
        ColorUtils.fromHsl((hsl.h + 90) % 360, hsl.s, hsl.l, hsl.a),
        ColorUtils.fromHsl((hsl.h + 180) % 360, hsl.s, hsl.l, hsl.a),
        ColorUtils.fromHsl((hsl.h + 270) % 360, hsl.s, hsl.l, hsl.a)
    }
end

-- 调整亮度
function Color:adjustLightness(amount)
    local hsl = self:toHsl()
    hsl.l = clamp(hsl.l + amount, 0, 100)
    return ColorUtils.fromHsl(hsl.h, hsl.s, hsl.l, hsl.a)
end

-- 调整饱和度
function Color:adjustSaturation(amount)
    local hsl = self:toHsl()
    hsl.s = clamp(hsl.s + amount, 0, 100)
    return ColorUtils.fromHsl(hsl.h, hsl.s, hsl.l, hsl.a)
end

-- 调整色相
function Color:adjustHue(amount)
    local hsl = self:toHsl()
    hsl.h = (hsl.h + amount) % 360
    if hsl.h < 0 then hsl.h = hsl.h + 360 end
    return ColorUtils.fromHsl(hsl.h, hsl.s, hsl.l, hsl.a)
end

-- 变亮
function Color:lighten(amount)
    amount = amount or 10
    return self:adjustLightness(amount)
end

-- 变暗
function Color:darken(amount)
    amount = amount or 10
    return self:adjustLightness(-amount)
end

-- 饱和
function Color:saturate(amount)
    amount = amount or 10
    return self:adjustSaturation(amount)
end

-- 去饱和
function Color:desaturate(amount)
    amount = amount or 10
    return self:adjustSaturation(-amount)
end

-- 灰度化
function Color:grayscale()
    local gray = round(0.299 * self.r + 0.587 * self.g + 0.114 * self.b)
    return Color.new(gray, gray, gray, self.a)
end

-- 反转
function Color:invert()
    return Color.new(255 - self.r, 255 - self.g, 255 - self.b, self.a)
end

-- 与另一颜色混合
function Color:mix(other, weight)
    weight = weight or 0.5
    weight = clamp(weight, 0, 1)
    
    return Color.new(
        round(self.r * (1 - weight) + other.r * weight),
        round(self.g * (1 - weight) + other.g * weight),
        round(self.b * (1 - weight) + other.b * weight),
        self.a * (1 - weight) + other.a * weight
    )
end

-- 转换为表格
function Color:toTable()
    return {r = self.r, g = self.g, b = self.b, a = self.a}
end

-- 克隆
function Color:clone()
    return Color.new(self.r, self.g, self.b, self.a)
end

-- 相等比较
function Color:__eq(other)
    return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a
end

-- 字符串表示
function Color:__tostring()
    return self:toRgbString()
end

-- 设置元表
Color.__metatable = Color

-- ============================================================================
-- 工厂函数 - 从各种格式创建颜色
-- ============================================================================

-- 从 RGB 创建
function ColorUtils.fromRgb(r, g, b, a)
    return Color.new(r, g, b, a)
end

-- 从 HEX 创建
function ColorUtils.fromHex(hex)
    hex = hex:gsub("^#", ""):gsub("^0x", "")
    
    -- 处理简写形式
    if #hex == 3 then
        hex = hex:sub(1,1) .. hex:sub(1,1) .. hex:sub(2,2) .. hex:sub(2,2) .. hex:sub(3,3) .. hex:sub(3,3)
    elseif #hex == 4 then
        hex = hex:sub(1,1) .. hex:sub(1,1) .. hex:sub(2,2) .. hex:sub(2,2) .. hex:sub(3,3) .. hex:sub(3,3) .. hex:sub(4,4) .. hex:sub(4,4)
    end
    
    local r = tonumber(hex:sub(1, 2), 16)
    local g = tonumber(hex:sub(3, 4), 16)
    local b = tonumber(hex:sub(5, 6), 16)
    local a = 1
    
    if #hex == 8 then
        a = tonumber(hex:sub(7, 8), 16) / 255
    end
    
    if not r or not g or not b then
        error("Invalid HEX color format: " .. hex)
    end
    
    return Color.new(r, g, b, a)
end

-- 从 HSL 创建
function ColorUtils.fromHsl(h, s, l, a)
    h = h % 360
    s = clamp(s, 0, 100) / 100
    l = clamp(l, 0, 100) / 100
    a = a or 1
    
    local function hue2rgb(p, q, t)
        if t < 0 then t = t + 1 end
        if t > 1 then t = t - 1 end
        if t < 1/6 then return p + (q - p) * 6 * t end
        if t < 1/2 then return q end
        if t < 2/3 then return p + (q - p) * (2/3 - t) * 6 end
        return p
    end
    
    local r, g, b
    if s == 0 then
        r, g, b = l, l, l
    else
        local q = l < 0.5 and l * (1 + s) or l + s - l * s
        local p = 2 * l - q
        r = hue2rgb(p, q, h/360 + 1/3)
        g = hue2rgb(p, q, h/360)
        b = hue2rgb(p, q, h/360 - 1/3)
    end
    
    return Color.new(round(r * 255), round(g * 255), round(b * 255), a)
end

-- 从 HSV 创建
function ColorUtils.fromHsv(h, s, v, a)
    h = h % 360
    s = clamp(s, 0, 100) / 100
    v = clamp(v, 0, 100) / 100
    a = a or 1
    
    local c = v * s
    local x = c * (1 - math.abs((h / 60) % 2 - 1))
    local m = v - c
    
    local r, g, b
    
    if h < 60 then
        r, g, b = c, x, 0
    elseif h < 120 then
        r, g, b = x, c, 0
    elseif h < 180 then
        r, g, b = 0, c, x
    elseif h < 240 then
        r, g, b = 0, x, c
    elseif h < 300 then
        r, g, b = x, 0, c
    else
        r, g, b = c, 0, x
    end
    
    return Color.new(round((r + m) * 255), round((g + m) * 255), round((b + m) * 255), a)
end

-- 从 CMYK 创建
function ColorUtils.fromCmyk(c, m, y, k, a)
    c = clamp(c, 0, 100) / 100
    m = clamp(m, 0, 100) / 100
    y = clamp(y, 0, 100) / 100
    k = clamp(k, 0, 100) / 100
    a = a or 1
    
    local r = 255 * (1 - c) * (1 - k)
    local g = 255 * (1 - m) * (1 - k)
    local b = 255 * (1 - y) * (1 - k)
    
    return Color.new(round(r), round(g), round(b), a)
end

-- 从颜色名称创建
function ColorUtils.fromName(name)
    name = name:lower():gsub("%s+", "")
    local rgb = ColorUtils.NAMED_COLORS[name]
    if not rgb then
        error("Unknown color name: " .. name)
    end
    return Color.new(rgb[1], rgb[2], rgb[3], 1)
end

-- 智能解析颜色字符串
function ColorUtils.parse(colorStr)
    if type(colorStr) == "table" then
        if colorStr.r and colorStr.g and colorStr.b then
            return Color.new(colorStr.r, colorStr.g, colorStr.b, colorStr.a or 1)
        end
        if #colorStr >= 3 then
            return Color.new(colorStr[1], colorStr[2], colorStr[3], colorStr[4] or 1)
        end
        error("Invalid color table format")
    end
    
    if type(colorStr) ~= "string" then
        error("Color must be a string or table")
    end
    
    colorStr = colorStr:gsub("^%s+", ""):gsub("%s+$", "")
    
    -- HEX 格式
    if colorStr:match("^#") or colorStr:match("^0x") then
        return ColorUtils.fromHex(colorStr)
    end
    
    -- RGB/RGBA 格式
    local r, g, b, a = colorStr:match("^rgba?%s*%(%s*(%d+)%s*,%s*(%d+)%s*,%s*(%d+)%s*,?%s*([%d%.]*)%s*%)$")
    if r then
        return Color.new(tonumber(r), tonumber(g), tonumber(b), a ~= "" and tonumber(a) or 1)
    end
    
    -- HSL/HSLA 格式
    local h, s, l, ha = colorStr:match("^hsla?%s*%(%s*(%d+)%s*,%s*(%d+)%%%s*,%s*(%d+)%%%s*,?%s*([%d%.]*)%s*%)$")
    if h then
        return ColorUtils.fromHsl(tonumber(h), tonumber(s), tonumber(l), ha ~= "" and tonumber(ha) or 1)
    end
    
    -- 颜色名称
    return ColorUtils.fromName(colorStr)
end

-- ============================================================================
-- 颜色生成函数
-- ============================================================================

-- 生成随机颜色
function ColorUtils.random()
    return Color.new(
        math.random(0, 255),
        math.random(0, 255),
        math.random(0, 255),
        1
    )
end

-- 生成随机柔和颜色
function ColorUtils.randomPastel()
    return Color.new(
        math.random(100, 255),
        math.random(100, 255),
        math.random(100, 255),
        1
    )
end

-- 生成随机暗色
function ColorUtils.randomDark()
    return Color.new(
        math.random(0, 100),
        math.random(0, 100),
        math.random(0, 100),
        1
    )
end

-- 生成随机饱和颜色
function ColorUtils.randomVibrant()
    local h = math.random(0, 360)
    local s = math.random(70, 100)
    local l = math.random(45, 55)
    return ColorUtils.fromHsl(h, s, l, 1)
end

-- 使用种子生成颜色 (确定性随机)
function ColorUtils.fromSeed(seed)
    -- 简单的伪随机生成
    local function simpleRandom(s)
        local x = math.sin(s) * 10000
        return x - math.floor(x)
    end
    
    return Color.new(
        math.floor(simpleRandom(seed) * 256),
        math.floor(simpleRandom(seed + 1) * 256),
        math.floor(simpleRandom(seed + 2) * 256),
        1
    )
end

-- ============================================================================
-- 颜色混合与渐变
-- ============================================================================

-- 混合两个颜色
function ColorUtils.mix(color1, color2, weight)
    weight = weight or 0.5
    local c1 = ColorUtils.parse(color1)
    local c2 = ColorUtils.parse(color2)
    return c1:mix(c2, weight)
end

-- 生成渐变色数组
function ColorUtils.gradient(colors, steps)
    steps = steps or 10
    if type(colors[1]) ~= "table" or not colors[1].r then
        colors = ColorUtils.parseColors(colors)
    end
    
    if #colors < 2 then
        error("At least 2 colors required for gradient")
    end
    
    local result = {}
    local segments = #colors - 1
    local stepsPerSegment = math.floor(steps / segments)
    
    for i = 1, segments do
        local startColor = colors[i]
        local endColor = colors[i + 1]
        
        local segmentSteps = stepsPerSegment
        if i == segments then
            segmentSteps = steps - #result
        end
        
        for j = 0, segmentSteps - 1 do
            if #result < steps then
                local weight = j / segmentSteps
                table.insert(result, startColor:mix(endColor, weight))
            end
        end
    end
    
    -- 确保最后一个颜色包含在内
    if #result < steps then
        table.insert(result, colors[#colors]:clone())
    end
    
    return result
end

-- 解析多个颜色
function ColorUtils.parseColors(colors)
    local result = {}
    for _, c in ipairs(colors) do
        table.insert(result, ColorUtils.parse(c))
    end
    return result
end

-- ============================================================================
-- 配色方案生成
-- ============================================================================

-- 生成单色配色方案
function ColorUtils.monochromatic(baseColor, count)
    count = count or 5
    local color = ColorUtils.parse(baseColor)
    local hsl = color:toHsl()
    local result = {}
    
    local step = 100 / (count + 1)
    for i = 1, count do
        local l = step * i
        table.insert(result, ColorUtils.fromHsl(hsl.h, hsl.s, l, hsl.a))
    end
    
    return result
end

-- 生成互补配色方案
function ColorUtils.complementaryScheme(baseColor)
    local color = ColorUtils.parse(baseColor)
    return {color, color:complementary()}
end

-- 生成类似色配色方案
function ColorUtils.analogousScheme(baseColor, angle)
    angle = angle or 30
    local color = ColorUtils.parse(baseColor)
    local analogs = color:analogous(angle)
    return {color, analogs[1], analogs[2]}
end

-- 生成三色组配色方案
function ColorUtils.triadicScheme(baseColor)
    local color = ColorUtils.parse(baseColor)
    local triad = color:triadic()
    return {color, triad[1], triad[2]}
end

-- 生成分裂互补色配色方案
function ColorUtils.splitComplementaryScheme(baseColor)
    local color = ColorUtils.parse(baseColor)
    local split = color:splitComplementary()
    return {color, split[1], split[2]}
end

-- 生成四色组配色方案
function ColorUtils.tetradicScheme(baseColor)
    local color = ColorUtils.parse(baseColor)
    local tetrad = color:tetradic()
    return {color, tetrad[1], tetrad[2], tetrad[3]}
end

-- 生成方形配色方案
function ColorUtils.squareScheme(baseColor)
    local color = ColorUtils.parse(baseColor)
    local sq = color:square()
    return {color, sq[1], sq[2], sq[3]}
end

-- ============================================================================
-- 实用工具函数
-- ============================================================================

-- 计算两个颜色之间的对比度
function ColorUtils.contrast(color1, color2)
    local c1 = ColorUtils.parse(color1)
    local c2 = ColorUtils.parse(color2)
    return c1:contrastRatio(c2)
end

-- 检查 WCAG 合规性
function ColorUtils.wcagCheck(foreground, background)
    local fg = ColorUtils.parse(foreground)
    local bg = ColorUtils.parse(background)
    return fg:wcagCompliance(bg)
end

-- 查找最接近的命名颜色
function ColorUtils.findClosestName(color)
    local c = ColorUtils.parse(color)
    local minDistance = math.huge
    local closestName = "unknown"
    
    for name, rgb in pairs(ColorUtils.NAMED_COLORS) do
        local distance = math.sqrt(
            (c.r - rgb[1])^2 + 
            (c.g - rgb[2])^2 + 
            (c.b - rgb[3])^2
        )
        if distance < minDistance then
            minDistance = distance
            closestName = name
        end
    end
    
    return closestName, minDistance
end

-- 计算两个颜色之间的差异 (欧几里得距离)
function ColorUtils.distance(color1, color2)
    local c1 = ColorUtils.parse(color1)
    local c2 = ColorUtils.parse(color2)
    return math.sqrt(
        (c1.r - c2.r)^2 + 
        (c1.g - c2.g)^2 + 
        (c1.b - c2.b)^2
    )
end

-- 判断颜色是亮还是暗
function ColorUtils.isLight(color)
    local c = ColorUtils.parse(color)
    local luminance = c:relativeLuminance()
    return luminance > 0.5
end

-- 获取合适的对比色 (黑或白)
function ColorUtils.getContrastColor(color)
    local c = ColorUtils.parse(color)
    local luminance = c:relativeLuminance()
    if luminance > 0.179 then
        return Color.new(0, 0, 0, 1) -- 黑色
    else
        return Color.new(255, 255, 255, 1) -- 白色
    end
end

-- 颜色温度 (暖色/冷色)
function ColorUtils.getTemperature(color)
    local c = ColorUtils.parse(color)
    local hsl = c:toHsl()
    
    -- 暖色: 0-60 和 300-360 (红、橙、黄)
    -- 冷色: 120-240 (绿、青、蓝)
    -- 中性: 60-120 和 240-300
    
    if (hsl.h >= 0 and hsl.h < 60) or (hsl.h >= 300 and hsl.h <= 360) then
        return "warm"
    elseif hsl.h >= 120 and hsl.h < 240 then
        return "cool"
    else
        return "neutral"
    end
end

-- 颜色和谐度评估
function ColorUtils.harmonyScore(colors)
    colors = ColorUtils.parseColors(colors)
    if #colors < 2 then return 100 end
    
    -- 简单和谐度计算: 基于色相差异
    local totalScore = 0
    local pairs = 0
    
    for i = 1, #colors do
        for j = i + 1, #colors do
            local h1 = colors[i]:toHsl().h
            local h2 = colors[j]:toHsl().h
            local diff = math.abs(h1 - h2)
            if diff > 180 then diff = 360 - diff end
            
            -- 理想差异: 30° (类似), 60° (三分), 90° (四分), 120° (三色), 180° (互补)
            local score = 0
            for _, ideal in ipairs({30, 60, 90, 120, 180}) do
                local s = 100 - math.abs(diff - ideal)
                score = math.max(score, s)
            end
            
            totalScore = totalScore + score
            pairs = pairs + 1
        end
    end
    
    return pairs > 0 and round(totalScore / pairs) or 100
end

-- 导出 Color 类
ColorUtils.Color = Color

return ColorUtils