--[[
Color Utilities - 颜色工具模块

提供完整的颜色处理功能，包括格式转换、配色方案生成、对比度计算等。

使用方法:
    local ColorUtils = require("color_utils")
    local color = ColorUtils.fromHex("#FF5733")
    print(color:toRgbString())
]]

local color_utils = require("color_utils.mod")
return color_utils