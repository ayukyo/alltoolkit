--[[
Color Utilities Test Suite

测试颜色工具模块的所有功能。

运行方式: lua color_utils_test.lua
]]

local ColorUtils = require("mod")

-- 测试统计
local testsPassed = 0
local testsFailed = 0
local testsTotal = 0

-- 辅助函数: 断言
local function assertEquals(expected, actual, message)
    testsTotal = testsTotal + 1
    if expected == actual then
        testsPassed = testsPassed + 1
        print("✓ " .. message)
    else
        testsFailed = testsFailed + 1
        print("✗ " .. message .. " (expected: " .. tostring(expected) .. ", got: " .. tostring(actual) .. ")")
    end
end

local function assertApproxEquals(expected, actual, tolerance, message)
    testsTotal = testsTotal + 1
    tolerance = tolerance or 0.01
    if math.abs(expected - actual) <= tolerance then
        testsPassed = testsPassed + 1
        print("✓ " .. message)
    else
        testsFailed = testsFailed + 1
        print("✗ " .. message .. " (expected: " .. tostring(expected) .. "±" .. tolerance .. ", got: " .. tostring(actual) .. ")")
    end
end

local function assertNotNil(value, message)
    testsTotal = testsTotal + 1
    if value ~= nil then
        testsPassed = testsPassed + 1
        print("✓ " .. message)
    else
        testsFailed = testsFailed + 1
        print("✗ " .. message .. " (got nil)")
    end
end

print("=" .. string.rep("=", 59))
print("Color Utilities Test Suite")
print("=" .. string.rep("=", 59))
print("")

-- ============================================================================
-- 测试 RGB 颜色创建
-- ============================================================================
print("--- RGB Color Creation ---")

do
    local color = ColorUtils.fromRgb(255, 0, 0)
    assertEquals(255, color.r, "RGB red component")
    assertEquals(0, color.g, "RGB green component")
    assertEquals(0, color.b, "RGB blue component")
    assertEquals(1, color.a, "RGB default alpha")
end

do
    local color = ColorUtils.fromRgb(128, 64, 32, 0.5)
    assertEquals(128, color.r, "RGB custom red")
    assertEquals(64, color.g, "RGB custom green")
    assertEquals(32, color.b, "RGB custom blue")
    assertEquals(0.5, color.a, "RGB custom alpha")
end

-- ============================================================================
-- 测试 HEX 转换
-- ============================================================================
print("")
print("--- HEX Conversion ---")

do
    local color = ColorUtils.fromHex("#FF5733")
    assertEquals(255, color.r, "HEX red from #FF5733")
    assertEquals(87, color.g, "HEX green from #FF5733")
    assertEquals(51, color.b, "HEX blue from #FF5733")
end

do
    local color = ColorUtils.fromHex("#FFF")
    assertEquals(255, color.r, "HEX short format red")
    assertEquals(255, color.g, "HEX short format green")
    assertEquals(255, color.b, "HEX short format blue")
end

do
    local color = ColorUtils.fromRgb(255, 87, 51)
    assertEquals("#FF5733", color:toHex(), "RGB to HEX conversion")
end

-- ============================================================================
-- 测试 HSL 转换
-- ============================================================================
print("")
print("--- HSL Conversion ---")

do
    local color = ColorUtils.fromHsl(0, 100, 50)  -- 红色
    assertEquals(255, color.r, "HSL red: R")
    assertEquals(0, color.g, "HSL red: G")
    assertEquals(0, color.b, "HSL red: B")
end

do
    local color = ColorUtils.fromRgb(255, 0, 0)
    local hsl = color:toHsl()
    assertEquals(0, hsl.h, "Red to HSL hue")
    assertEquals(100, hsl.s, "Red to HSL saturation")
    assertEquals(50, hsl.l, "Red to HSL lightness")
end

-- ============================================================================
-- 测试 HSV 转换
-- ============================================================================
print("")
print("--- HSV Conversion ---")

do
    local color = ColorUtils.fromHsv(0, 100, 100)  -- 红色
    assertEquals(255, color.r, "HSV red: R")
    assertEquals(0, color.g, "HSV red: G")
    assertEquals(0, color.b, "HSV red: B")
end

do
    local color = ColorUtils.fromRgb(255, 0, 0)
    local hsv = color:toHsv()
    assertEquals(0, hsv.h, "Red to HSV hue")
    assertEquals(100, hsv.s, "Red to HSV saturation")
    assertEquals(100, hsv.v, "Red to HSV value")
end

-- ============================================================================
-- 测试 CMYK 转换
-- ============================================================================
print("")
print("--- CMYK Conversion ---")

do
    local color = ColorUtils.fromCmyk(0, 100, 100, 0)  -- 红色
    assertEquals(255, color.r, "CMYK red: R")
    assertEquals(0, color.g, "CMYK red: G")
    assertEquals(0, color.b, "CMYK red: B")
end

-- ============================================================================
-- 测试命名颜色
-- ============================================================================
print("")
print("--- Named Colors ---")

do
    local color = ColorUtils.fromName("red")
    assertEquals(255, color.r, "Named color 'red': R")
    assertEquals(0, color.g, "Named color 'red': G")
    assertEquals(0, color.b, "Named color 'red': B")
end

-- ============================================================================
-- 测试智能解析
-- ============================================================================
print("")
print("--- Smart Parsing ---")

do
    local color = ColorUtils.parse("#FF0000")
    assertEquals(255, color.r, "Parse HEX")
end

do
    local color = ColorUtils.parse("blue")
    assertEquals(0, color.r, "Parse color name 'blue': R")
    assertEquals(0, color.g, "Parse color name 'blue': G")
    assertEquals(255, color.b, "Parse color name 'blue': B")
end

-- ============================================================================
-- 测试颜色操作
-- ============================================================================
print("")
print("--- Color Operations ---")

do
    local color = ColorUtils.fromRgb(255, 0, 0)
    local gray = color:grayscale()
    assertApproxEquals(gray.r, gray.g, 0, "Grayscale R=G")
    assertApproxEquals(gray.g, gray.b, 0, "Grayscale G=B")
end

do
    local color = ColorUtils.fromRgb(255, 0, 0)
    local inverted = color:invert()
    assertEquals(0, inverted.r, "Invert red: R")
    assertEquals(255, inverted.g, "Invert red: G")
    assertEquals(255, inverted.b, "Invert red: B")
end

-- ============================================================================
-- 测试颜色混合
-- ============================================================================
print("")
print("--- Color Mixing ---")

do
    local red = ColorUtils.fromRgb(255, 0, 0)
    local blue = ColorUtils.fromRgb(0, 0, 255)
    local mixed = red:mix(blue, 0.5)
    assertApproxEquals(127.5, mixed.r, 1, "Mix red and blue: R")
    assertEquals(0, mixed.g, "Mix red and blue: G")
    assertApproxEquals(127.5, mixed.b, 1, "Mix red and blue: B")
end

-- ============================================================================
-- 测试配色方案
-- ============================================================================
print("")
print("--- Color Schemes ---")

do
    local red = ColorUtils.fromRgb(255, 0, 0)
    local comp = red:complementary()
    assertEquals(0, comp.r, "Complementary of red: R")
    assertEquals(255, comp.g, "Complementary of red: G")
    assertEquals(255, comp.b, "Complementary of red: B")
end

do
    local color = ColorUtils.fromRgb(255, 0, 0)
    local triad = color:triadic()
    assertEquals(2, #triad, "Triadic scheme returns 2 colors")
end

-- ============================================================================
-- 测试渐变生成
-- ============================================================================
print("")
print("--- Gradient Generation ---")

do
    local gradient = ColorUtils.gradient({"#FF0000", "#0000FF"}, 5)
    assertEquals(5, #gradient, "Gradient has 5 steps")
    assertEquals(255, gradient[1].r, "Gradient starts with red")
end

-- ============================================================================
-- 测试对比度计算
-- ============================================================================
print("")
print("--- Contrast & WCAG ---")

do
    local white = ColorUtils.fromRgb(255, 255, 255)
    local black = ColorUtils.fromRgb(0, 0, 0)
    local contrast = white:contrastRatio(black)
    assertApproxEquals(21, contrast, 0.1, "Black/white contrast ratio is 21:1")
end

do
    local white = ColorUtils.fromRgb(255, 255, 255)
    local black = ColorUtils.fromRgb(0, 0, 0)
    local compliance = white:wcagCompliance(black)
    assertEquals(true, compliance.aaNormal, "Black/white passes AA Normal")
end

-- ============================================================================
-- 测试随机颜色
-- ============================================================================
print("")
print("--- Random Colors ---")

do
    local color = ColorUtils.random()
    assertNotNil(color.r, "Random color has R")
    assertNotNil(color.g, "Random color has G")
    assertNotNil(color.b, "Random color has B")
end

do
    local color1 = ColorUtils.fromSeed(42)
    local color2 = ColorUtils.fromSeed(42)
    assertEquals(color1.r, color2.r, "Seeded colors have same R")
    assertEquals(color1.g, color2.g, "Seeded colors have same G")
end

-- ============================================================================
-- 测试实用工具
-- ============================================================================
print("")
print("--- Utility Functions ---")

do
    local name = ColorUtils.findClosestName(ColorUtils.fromRgb(255, 0, 0))
    assertEquals("red", name, "Find closest name for red")
end

do
    local isLight = ColorUtils.isLight("#FFFFFF")
    assertEquals(true, isLight, "White is light")
end

do
    local contrast = ColorUtils.getContrastColor("#000000")
    assertEquals(255, contrast.r, "Contrast for black is white: R")
end

do
    local temp = ColorUtils.getTemperature("#FF0000")
    assertEquals("warm", temp, "Red is warm")
end

-- ============================================================================
-- 测试边界情况
-- ============================================================================
print("")
print("--- Edge Cases ---")

do
    local color = ColorUtils.fromRgb(300, -50, 128)
    assertEquals(255, color.r, "Clamp R to 255")
    assertEquals(0, color.g, "Clamp G to 0")
end

-- ============================================================================
-- 测试结果汇总
-- ============================================================================
print("")
print("=" .. string.rep("=", 59))
print(string.format("Test Results: %d passed, %d failed, %d total", testsPassed, testsFailed, testsTotal))
print("=" .. string.rep("=", 59))

if testsFailed > 0 then
    os.exit(1)
else
    print("All tests passed! ✓")
    os.exit(0)
end