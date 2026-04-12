---
-- String Utilities Module
-- Lua 字符串处理工具函数库
--
-- @module string_utils
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local StringUtils = {}

-- 导出所有公共函数
local mod = require("mod")
for k, v in pairs(mod) do
    StringUtils[k] = v
end

return StringUtils
