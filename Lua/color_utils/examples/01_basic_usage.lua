--[[
Example 01: Basic Usage

演示颜色工具模块的基本功能。
]]

local ColorUtils = require("mod")

print("=" .. string.rep("=", 49))
print("Example 01: Basic Usage")
print("=" .. string.rep("=", 49))

-- 创建颜色
print("\n--- Creating Colors ---")
local rgb = ColorUtils.fromRgb(255, 87, 51)
print("From RGB(255, 87, 51): " .. rgb:toHex())

local hex = ColorUtils.fromHex("#3498DB")
print("From HEX #3498DB: " .. hex:toRgbString())

local named = ColorUtils.fromName("coral")
print("From Name 'coral': " .. named:toRgbString())

-- 格式转换
print("\n--- Format Conversion ---")
local color = ColorUtils.fromHex("#FF5733")
local hsl = color:toHsl()
print("HSL: h=" .. hsl.h .. ", s=" .. hsl.s .. "%, l=" .. hsl.l .. "%")

local hsv = color:toHsv()
print("HSV: h=" .. hsv.h .. ", s=" .. hsv.s .. "%, v=" .. hsv.v .. "%")

local cmyk = color:toCmyk()
print("CMYK: c=" .. cmyk.c .. "%, m=" .. cmyk.m .. "%, y=" .. cmyk.y .. "%, k=" .. cmyk.k .. "%")

-- 颜色操作
print("\n--- Color Operations ---")
local base = ColorUtils.fromRgb(128, 64, 32)
print("Base: rgb(128, 64, 32)")
print("Lighten 30%: " .. base:lighten(30):toRgbString())
print("Darken 30%: " .. base:darken(30):toRgbString())
print("Grayscale: " .. base:grayscale():toRgbString())
print("Invert: " .. base:invert():toRgbString())

-- 随机颜色
print("\n--- Random Colors ---")
print("Random: " .. ColorUtils.random():toRgbString())
print("Pastel: " .. ColorUtils.randomPastel():toRgbString())
print("Vibrant: " .. ColorUtils.randomVibrant():toRgbString())

print("\n" .. "=" .. string.rep("=", 49))